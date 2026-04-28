# User management

/// Caution
This page covers access control of the Nokia Event-Driven Automation (EDA) API server.
The Nokia Config Engine can also be operated via the Kubernetes API. Kubernetes access control should be considered when securing a Nokia EDA deployment.
///

Role-based access control (RBAC) restricts API requests based on the user's role in your organization. Nokia EDA uses the [OAuth 2.0](https://oauth.net/2/) standard for authorization.

Nokia EDA uses [Keycloak](https://www.keycloak.org/) as the OAuth 2.0 identity provider, authenticating users and group membership. The Nokia EDA API server validates request authorization based on the role(s) assigned to the user's group(s).

Common Keyclock administrative actions including user and user group management, are available via the Nokia EDA API and UI.

## Users and user groups

Nokia EDA users and user groups are stored in Keycloak.

In the Nokia EDA UI, you can find Users and User Groups in the `System Administration` panel under `User Management` > `User Management`.

/// admonition | Note
    type: subtle-note
Changes to users and user groups are passed through from Nokia EDA to Keycloak. These changes are not processed as Nokia EDA transactions.
///

User passwords set by an administrator can be flagged as temporary; this will prompt the user to change the password on first login. Administrators can also perform password resets, which sends the user an email with a password reset link.

/// admonition | Note
    type: subtle-note
Email server configuration is not exposed in the Nokia EDA API/UI. This must be configured directly in KeyCloak.
///

Nokia EDA comes with a default local user called `admin`. The admin user is assigned to the `system-administrator` group.

### Federations

Federations configure users and user group synchronization with remote directories such as OpenLDAP or Active Directory.

Nokia EDA supports:

- The configuration of up to five directories
- LDAP and Active Directory directories
- User synchronization from the directory
- Group synchronization from the directory and user group membership mapping
- Limiting imported users and groups using LDAP filters

Federated users are imported into Keycloak the first time a user logs in or when the user list is read via the Nokia EDA API and UI. Additionally, you can configure periodic sync of created and updates users.

In the Nokia EDA UI, federated users are identified in the **Federated User** field in users list.

When a federation is configured, system administrators can continue to create local users and groups in Nokia EDA.

The Nokia EDA API server server blocks all edits to federated users except for adding or removing the user to local groups. Local changes to federated groups are not supported; federated group membership must be configured on the LDAP server.

/// admonition | Note
    type: subtle-note
Nokia EDA only configures federation providers in Keycloak using unsynchronized mode. This mode imports users and groups into Nokia EDA's Keycloak database, but does not write local changes back to the Lightweight Directory Access Protocol (LDAP) server.
///

When connecting a federation provider using LDAPS or STARTTLS, Keycloak must trust the server's TLS certificate. To add certificate authorities to the EDA Keycloak truststore, create a Kubernetes secret named `ldap-ca-secret` of type `Opaque` in the EDA base namespace with a base64 encoded PEM certificate in the `ca` field. For example:

```yaml
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: ldap-ca-secret
  namespace: eda-system #Enter the base namespace of your EDA installation
data:
  ca: <base64 certificate> # Base64 encoded PEM certificate
```

Nokia EDA monitors this secret and if it changes, Nokia EDA updates the certificate authority information used by Keycloak. Modifying the authority information results in a restart of the Keycloak server.

### Password policies

The system enforces a password policy for local users. The password policy does not apply to users authenticated from remote directories.

The password policy options includes password aging rules, password complexity rules, password history, and user lockout rules. An admin user can update the policy settings as needed. The policy also applies to the admin user.

/// admonition | Note
    type: subtle-note
Nokia recommends that system administrators configure a password policy for production deployments.
///

### User Sessions

Keycloak maintains a list of active sessions. Each of these sessions have are associated to a short-lived access token, and a longer lived refresh token.

Session information includes:

- Username
- Start time
- User's source IP address
- Clients (for example, the Nokia EDA UI)

From the Nokia EDA API and UI, you can:

- View a system-wide list of active sessions
- View per-user list of active sessions
- Logout a specific session

/// admonition | Note
    type: subtle-note

Session logout prevents the user from using a refresh token to get a new access token. The existing access token remains valid until its expiration time. The default lifespan of the access token is 5 minutes.

///

## Roles

Nokia EDA `ClusterRole` and `Role` resources define user permissions.

Roles define permissions within a specific namespace, whereas Cluster Role permissions apply to all namespaces.

Non-namespaced Nokia EDA API endpoints can only be enforced by Cluster Roles. This includes cluster-wide resources (for example, `LogOutputs`), Nokia EDA administrative APIs, and transaction results. In general, any API that doesn't specify a namespace in the path or payload is enforced by Cluster Roles.

/// admonition | Note
    type: subtle-note
While similar in concept, Nokia EDA `Role` and `ClusterRole` resources are not the same as Kubernetes `Role` and `ClusterRole`.
///

For `ClusterRole` and `Role`, the following rule types are supported:

- **Resource Rules**: defined Nokia EDA resource and workflow permissions using Group-Version-Kind (GVK) semantics.
- **Table Rules**: defines permissions for queries to EDB.
- **URL Rules**: defines permissions for Nokia EDA API endpoints based on their URL path. URL Rule permission is not required for API endpoints which are Resource Rule or Table Rule enforced.

### Resource rules

Resource rules define access to Nokia EDA resources and Nokia EDA workflows. These rules are relevant for resource-aware Nokia EDA API endpoints including:

- `/core/transaction/..`
- `/apps/..`
- `/workflows/..`

A resource rule is defined by the following parameters:

- **API groups**: Identifies the Nokia EDA API groups for the resources controlled by the rule, in the format `{group}/{version}`.

    An asterisk `*` indicates wildcard of any API group. A `*` wildcard can also be used for the group version, for example, `core.eda.nokia.com/*`.

- **Permissions**: Specifies `none`, `read`, `readWrite`, or `readPropose` permissions for the Nokia EDA resources matching the rule.

    `readPropose` allows users to [dry-run](../transactions.md#dry-runs) transactions, create [merge requests](../merge-requests.md), and commit in a branch. It does not allow the user to commit directly to the main Nokia EDA cluster.

- **Resources**: The resource names of the resources controlled by the rule. For example `toponodes`.

    An asterisk `*` indicates wildcard, which means match any resource in the specified API group.

/// admonition | Transaction result RBAC
    type: subtle-note

Access to transaction results is based on a user's access to the *input resources* of that transaction:

  - If a user has read permission for **all** the input resources of a transaction, the user can list all changed resources (both input and derived) and view the resource diffs.
  - If a user has read permission for **none** or **some** of the input resources, that user cannot list any derived resources or view their diffs.
  - Access to Node Configuration diffs require a URL rule. This is because the Node Configuration diff API returns the full node config, and not limited to the scope of the transaction.
  - To revert a transaction, a user must have `readWrite` permission for **all** input resources of the transaction.
  - To restore the Nokia EDA cluster to a specific transaction, a user must have `readWrite` permission to the restore API from a `ClusterRole` URL rule. Restore is a powerful action which should be limited to trusted administrators.

///

/// admonition | Workflow result RBAC
    type: subtle-note

Access to workflow results is based on the user's access to the *root parent workflow*

For example, a `DeployImage` workflow creates `Ping` subflows during it's pre and post check stages. If user A has read permission to the `DeployImage` workflow definition they will be able to read the subflow results even if they do not have access to the `Ping` workflow definition.

///

### Table rules

Table rules are similar to resource rules, except that they are relevant to the API endpoints used for querying the Nokia EDA database (EDB). A table rule is defined by the following parameters:

- **Path**: Specifies the path of the database table for which this rule applies.

    Table Rules support wildcarding of the final Nokia EDA path segment (`.*`) or multiple Nokia EDA path segments (`.**`)

- **Permissions**: Specifies `none` or `read` permissions for the EDB table.


/// admonition | Implicit table rules for resource paths
    type: subtle-note
To simplify user access to resource-related dashboards and queries, users are implicitly granted `read` permission to the following paths when they have an equivalent resource rule:

  - `.namespace.resources.cr.{group}.{version}.{kind}.**`
  - `.namespace.node.normal.{group}.{version}.{kind}.**`
  - `.namespace.apps.cr.{group}.{version}.{kind}.**`

///

### URL rules

URL rules define generic enforcement of URL paths exposed by an API server. URL rules are needed for API endpoints that are not associated to resources or EDB tables.

- **Path**: Specifies the API URL path to which this rule applies.

    `/*` at the end of the path indicates the final portion of the URL path can be anything, if the prefix matches.

    `/**` at the end of the path indicates that the URL path can be anything if the prefix matches.

- **Permissions**: Specifies `none`, `read`, or `readwrite` permissions for the URL path.

### Multiple rule behavior

Nokia EDA rules are additive. Users are granted the combined permission of all rules in the roles assigned to their user groups. If a request does not match any rule, it is implicitly denied.

The `None` permission acts as an override; these are enforced before any other rule.

/// admonition | Best-practice recommendations
    type: code-example

Create explicit read/readWrite rules for the resource, table, and URLs required for a role, avoiding wildcard rules where possible. A wildcard gives access to resources that exist today and resources that may exist in the future.

Avoid `None` rules where possible. If resource, table, or URL access is not required for a role, do not include a matching rule for that resource/table/URL (that is, implicit deny). 'None' rules are explicit denials. They have priority over all permissive rules assigned to the user, including the rules defined in other groups and roles.
///

### Examples

/// details | Default system-administrator `ClusterRole`
    type: code-example

Nokia EDA provides a default `system-administrator` cluster role with the following configuration:

```yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterRole
metadata:
  name: system-administrator
spec:
  description: >-
    This is the default administrator role for Nokia EDA. It cannot be deleted.  A
    user with this role can do anything.
  resourceRules:
    - apiGroups:
        - '*'
      permissions: readWrite
      resources:
        - '*'
  tableRules:
    - path: .**
      permissions: read
  urlRules:
    - path: /**
      permissions: readWrite
```

///

/// details | Example `ClusterRole`
    type: code-example

```yaml
kind: ClusterRole
metadata:
  name: basic
  labels: {}
  annotations: {}
spec:
  description: ''
  resourceRules:
    - apiGroups:
        - core.eda.nokia.com/v1
      permissions: read
      resources:
        - '*'
    - apiGroups:
        - fabrics.eda.nokia.com/v1
      resources:
        - fabrics
      permissions: readWrite
    - apiGroups:
        - fabrics.eda.nokia.com/v1
      resources:
        - '*'
      permissions: read
```

///

/// details | Example `Role`
    type: code-example

```yaml
apiVersion: core.eda.nokia.com/v1
kind: Role
metadata:
  name: ns-admin
  namespace: eda
spec:
  resourceRules:
    - apiGroups:
        - '*'
      permissions: readWrite
      resources:
        - '*'
  tableRules:
    - path: .**
      permissions: read
  urlRules:
    - path: /**
      permissions: readWrite
```

///

/// details | Example `ClusterRole` - Read-only everything
    type: code-example

``` yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterRole
metadata:
  name: readonly
  namespace: eda-system
  labels: null
spec:
  description: Read only for everything
  resourceRules:
    - apiGroups:
      - '*'
      permissions: read
      resources:
        - '*'
  tableRules:
    - path: .**
      permissions: read
  urlRules:
    - path: /**
      permissions: read
```

///

/// details | Example `ClusterRole` - Read and write fabric resources and read-only related resources
    type: code-example

``` yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterRole
metadata:
  name: fabric
  namespace: eda-system
  labels: null
spec:
  description: Read and Write for Fabrics and read-only for related resources
  resourceRules:
    - apiGroups:
      - fabrics.eda.nokia.com/v1alpha1
      permissions: readWrite
      resources:
        - '*'
    - apiGroups:
        - routing.eda.nokia.com/v1alpha1
        - protocols.eda.nokia.com/v1alpha1
        - core.eda.nokia.com/v1
      permissions: read
      resources:
        - '*'
  urlRules:
    - path: /openapi/**
      permissions: read

```

///

/// details | Example `ClusterRole` - Read all EDB tables and act on alarms (ack/delete/suppress/etc)
    type: code-example

``` yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterRole
metadata:
  name: queryandalarms
  labels: null
  namespace: eda-system
spec:
  description: 'Permission to run queries and update alarms (ack/delete/suppress/etc)'
  tableRules:
    - path: .**
      permissions: read
  urlRules:
    - path: /core/alarm/**
      permissions: readWrite
```

///

/// details | Example - Topologies access in specific namespace
    type: code-example

Topology diagrams and their overlays are defined cluster-wide in Nokia EDA, but the state data which populates the topology diagrams is namespaced. Therefore, to limit topologies access to specific namespaces requires a combination of ClusterRoles and Roles.

/// details | ClusterRole - Physical topology
    type: code-example

``` yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterRole
metadata:
  name: topology-definitions
  namespace: eda-system
spec:
  description: Access descriptions of physical topology and its overlays
  resourceRules:
    - apiGroups:
        - topologies.eda.nokia.com/v1alpha1
      permissions: read
      resources:
        - topologygroupings
  urlRules:
    - path: /core/topology/v1
      permissions: read
    - path: /core/topology/v1/topologies.eda.nokia.com_v1alpha1_physical
      permissions: read
    - path: /core/topology/v1/topologies.eda.nokia.com_v1alpha1_physical/overlay
      permissions: read
    - path: /core/topology/v1/topologies.eda.nokia.com_v1alpha1_physical/groupings
      permissions: read
```

///

/// details | Role - Physical topology
    type: code-example

``` yaml
apiVersion: core.eda.nokia.com/v1
kind: Role
metadata:
  name: ns-topo
  namespace: eda
spec:
  description: Access physical topology state in namespace 'eda'
  urlRules:
    - path: /core/topology/v1/topologies.eda.nokia.com_v1alpha1_physical/state
      permissions: readWrite
```

///

///

## User management in the Nokia EDA UI

### Users page

The **Users** page in the UI lists all local and remote Nokia EDA users and a provides a summary of user details. You can sort and filter for users using the typical mechanisms.

|Column|Description|
|------|-----------|
|Username|The login name for the user.|
|First Name|The first name of the user.|
|Last Name|The last name of the user.|
|Enabled|Indicates whether the user account is active or disabled.|
|Last Successful Login|The timestamp for the user's last successful login.|
|Federated User|The federation provider, if the user is a federation user.|
|Failed Logins Since Successful Login|The number of failed log in attempts after a user successfully logs in. This counter resets to 0 after the user successfully logs in again.|
|Last Failed Login|The timestamp for the user's last login failure.|
|Temporarily Disabled|Indicates if a user is temporarily disabled because of exceeding the allowed number of failed log in attempts.|

### Creating a new local user

/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT** and select **User Management**.

2. From the **User Management** drop-down list, click **Users**.

3. Click **Create**.

4. In the **User Information** section, enter the required information for the new user.

    - a username
    - the user's first and last name
    - the user's email address
  
5. Click **Set Password**.

    In the form that opens, provide a password and confirm it. By default, the password is temporary and a user must log in and provide a new password for the newly created account.

6. Assign this user to one or more user groups.

    From the **Assigned User Groups** drop-down list, select an existing user group. Optionally, you can create a user without assigning the user to a user group. Later, you can add the user to a user group.

7. Click **Save**.

///

### Managing user accounts

/// admonition | Note
    type: subtle-note
A user with system-administrator privileges cannot delete the built-in admin user or modify its groups or roles.
///

/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT** and click **User Management**.

2. Click **Users** from the **User Management** drop-down list.

3. You can act on a single user or many users.

    - To manage a single user, locate the user and click the action that you want to take from the **Table row actions** menu.
        - Click **Edit** to update details for a user such as user first name and last name, and assigned user groups. You can also enable or disable a user.
        - Click **Set Password** to set a new password.
    - Alternatively, you can select more than one user, then click the **Table settings &amp; actions button** icon. You can perform one of the following multi-row actions:
        - Delete the selected users.
        - Set passwords for the selected users.
        - Disable or enable the selected users.
4. Click **Save**.

///

### Managing user sessions

To display all user sessions, from the **System Administration** navigation panel, expand **USER MANAGEMENT** and select **User Sessions**.

- To filter sessions for a specific user, enter the user name in the filter box.
- To terminate the a session for a user, click the **Table row actions** menu and select **Logout**.

### Changing your password

Perform this task from any page on Nokia EDA UI.

/// html | div.steps

1. Click the user icon at the upper right of the screen and select **Change Password**.

2. When prompted, log in again with your credentials.

3. Enter your new password and confirm it.

4. Click **Save**.

///

### Viewing user groups

From the **System Administration** navigation panel, expand **USER MANAGEMENT** and click **User Management**. Select **User Groups** from the drop-down list.

/// admonition | Note
    type: subtle-note
LDAP groups are displayed in the **User Groups** page only after they are imported from an LDAP server.
///

### Creating a user group

/// html | div.steps

1. From the **System Administration** navigation panel, expand the **USER MANAGEMENT** group, then click **User Management**.

2. Click **User Groups** from the **User Management** drop-down list.

3. Click **Create**.

4. Provide a name for this user group.

5. In the **Assigned Users** section, click **+ Add**.

    Select the users that you want to assign to this user group, then click **Save**.

6. From the **Assigned Roles** drop-down list, select a role to assign to the user group.

    You can only select one role.

7. Click **Save**.

///

### Deleting user groups

/// html | div.steps

1. From the **System Administration** navigation panel, expand the **USER MANAGEMENT** group, then click **User Management**.

2. Click **User Groups** from the **User Management** drop-down list.

3. Delete one or more user groups.

    - To delete one user group, locate the user group that you want to delete and click **Delete** from the **Table row actions** menu.
    - Alternatively, you can click one or more user groups. Then, click **Delete** from the **Table settings &amp; actions** menu.

4. Click **Save**.

///

### Configuring a federation <span id="configure-federation"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT** and select **User Management**.

2. From the **User Management** drop-down list, click **Federations**.

3. Click **Create**.

4. Configure settings for this federation instance.

    - a unique name
    - the LDAP provider Vendor
    - **Enabled**
    - **Import Users**: By default, this field is set to True; this field is ready-only.

5. Configure LDAP server settings.

    Set the following parameters:

    - **Connection URL**
    - **Use TLS**: If this field is set to True, the certificate should be established on the LDAP server side. After configuring certificate from LDAP server, create the LDAP CA secret (`ldap-ca-secret`) on the platform where Nokia EDA is managed.
    - **Bind Type**
    - **User DN**
    - **Username LDAP Attribute**
    - **Timeout**

        Click **Test Connection** to test the connection to the LDAP server.

    - **RDN LDAP Attribute**
    - **ID Attribute**
    - **User Object Classes**
    - **User Search Filter**
    - **Search Scope**
    - **Pagination**
    - **Periodic Sync**
    - **Read Only**
  
6. Enable and configure support for bind credentials.

    Set the following parameters:

    - **Bind Credential**
    - **Bind DN**
  
    Click **Test Authentication** to verify that the credentials are valid.

7. Enable and configure group federation support.

    If group support is disabled, groups are not synchronized with Nokia EDA. If group support is enabled, set the following parameters:

    - **Object Classes**
    - **Group LDAP DN**
    - **Name LDAP Attribute**
    - **Member Attribute**
    - **Membership Attribute Type**
    - **Membership User Attribute**
    - **Filter**
    - **Retrieval Strategy**
    - **Member Of Attribute**

8. Click **Save**.

///

### Deleting a federation <span id="delete-federation"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT** and click **User Management**.

2. From the **User Management** drop-down list, click **Federations**.

3. You can delete one federation or multiple federations at a time.

    - Locate the federation that you want to delete and at click **Delete** from the **Table row actions** menu.
    - Alternatively, you can select more than one federation, then, click the **Table settings &amp; actions** menu on the upper right of the page and select **Delete**. Click **Save**.

4. Click **Save**.
///

### Modifying the password policy

/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT**, click **Password Policy**, then click **Edit**.

    You can restore the default settings at this point or modify the password properties and lockout policy settings.

2. Modify any of the following password properties:

    - the minimum length of a password
    - the minimum number of lowercase characters
    - the minimum number of symbols or special characters
    - the number of passwords to keep and validate against
    - the minimum number of uppercase characters
    - the minimum number of numerical characters
    - whether the username can be used as a password
    - the duration, in days, for a password to remain valid
    - the hashing algorithm: **ARGON2** (the default), **PBKDF2-SHA512**, **PBKDF2-SHA256**, or **PBKDF2**

3. Modify any of the lockout policy settings:

    - the maximum consecutive failed login attempts before account lockout
    - duration, in seconds, to wait after reaching the maximum login failures before retry is allowed
    - whether to lock the account permanently after maximum number of failed logins
    - duration, in seconds, after which failed login attempts are reset

///

### Creating a cluster role <span id="create-cluster-roles"></span>

/// html | div.steps

A `ClusterRole` resource defines a set of permissions to access Nokia EDA resources. Use this procedure to create a cluster role from the Nokia EDA UI.

1. From the **System Administration** navigation panel, expand the **USER MANAGEMENT** group, then select **Cluster Roles**.

2. If not already selected, click **Resources** from the **Cluster Roles** drop-down list.

3. Click **Create**.

4. Provide a name  for the `ClusterRole` resource:

5. Provide an optional description for this `ClusterRole` resource.

6. Create the list of resource rules.

    In the Resource Rules section, click **+ Add**.

    1. Under **API Groups**, click **Add Item** to create the list of API groups.

    2. Click **None**, **read**, or **readWrite** in the **Permissions** drop-down list.

    3. Under **Resources**, click **+ Add** to specify the resources on which this rule applies.

        You can enter the `*` character, which means match any resource in the matching API groups.

    4. Click **Save**.

7. In the Table Rules section, click **+ Add**.

    1. Provide the path to the database table to which this rule applies.

    2. Under **Permissions**, from the drop-down list, select **None** or **read**.

    3. Click **Save**.

8. In the URL Rules section, click **+ Add**. Create resource rules for this cluster group.

    1. Provide the path to the API server proxied URL to which this rule applies.

    2. Under **Permissions**, select **None**, **read**, or **readWrite** from the drop-down list.

    3. Click **Save**.

///

### Creating a role <span id="create-roles"></span>

The `Role` resource defines a set of permissions to access Nokia EDA resources. The `Role` resource exists within a namespace.

/// html | div.steps

1. From the **System Administration** navigation panel, expand the **USER MANAGEMENT** group, then click **Roles**.

2. If not already selected, click **Resources** from the **Roles** drop-down list.

3. Click **Create**.

4. Provide the following metadata for this resource:

    - name
    - namespace (if none is selected)
  
5. Provide an optional description for this cluster role.

6. In the **Resource Rules** section, click **+ Add**. Create resource rules for this cluster group.

    1. Under **API Groups**, click **Add Item** to create the list of API groups.

    2. Under **Permissions**, from the drop-down list, select **None**, **Read**, or **ReadWrite**.

    3. Under **Resources**, click **+ Add** to specify the resources on which this rule applies.

        You can enter the `*` character, which means match any resource in the matching API groups.

    4. Click **Add**.

7. In the **Table Rules** section, click **+ Add**.

    1. Provide the path to the database table to which this rule applies.

    2. In the **Permissions** drop-down list, select **None** or **Read**.

    3. Click **Save**.

8. In the **URL Rules** section, click **+ Add**. Create resource rules for this cluster group.

    1. Provide the path to the API server proxied URL to which this rule applies.

    2. Under **Permissions**, select **None**, **Read**, or **ReadWrite** from the drop-down list.

    3. Click **Save**.

9. Click **Commit** to commit your change immediately or click **Add To Transaction** to add this item to transactions to commit later.

## Privacy considerations

From a privacy perspective, Nokia EDA stores user information securely in a database. This information
includes the username, password, email, first name, last name, and login times of each user in
the system. Additionally, user activity is logged securely for security and support perspectives. The
information is not processed or shared outside of the deployed Nokia EDA environment. A backup contains
the same information for the purpose of restoring the users if a restore is required.
/// Caution
Ensure that you store the backup information securely and limit access to both the running environment and any backup storage environment.

Handle all environments containing privacy sensitive information according to the regulations that apply
to the location and users of the system and the data.
///
