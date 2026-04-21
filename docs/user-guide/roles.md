# Roles

A role specifies which network resources users or associated user group members can access.

In EDA, a `Role` resource lives within a namespace, while a `ClusterRole` resource applies cluster-wide and spans namespaces.

   **Note:** While similar in concept, EDA roles and cluster roles are not the same roles and cluster roles in Kubernetes.

`Role` and `ClusterRole` resources are created by a system administrator and are referenced in groups that exist in Keycloak (or a remote directory), which are in turn associated with users. As with Kubernetes, a cluster role spans namespaces, while a role lives within a namespace.

A role controls access to EDA resources by defining one or more match rules and corresponding action to take when there is a match.

**Parent topic:** [Securing access to EDA](secure-access-eda.md)

## Rules <span id="rules"></span>

EDA supports the following types of rules for `Role` and `Cluster Role` resources:

- Resource rules: control access to EDA API resources.
- Table rules: control access to the database tables.

    **Note:** Write access is not supported on a table rule.

- URL rules: control access to API endpoints that are not specific to resources or tables.

### Resource rules

Resource rules define access to EDA and Kubernetes resources exposed via the API server. These rules are relevant for resource-aware API endpoints including:

- `/openapi/v3/apps/..`
- `/core/transaction/v1`
- `/apps/..`
- `/workflows/..`

A resource rule is defined by the following parameters in the `Role` or `ClusterRole` resource:

- **API groups**: Identifies the EDA API groups for the resources controlled by the rule, in the format `apigroup/version`. An asterisk `*` indicates match any API group. `apiGroups` can include a \* wildcard for the group version, for example, `core.eda.nokia.com/*`.
- **Permissions**: Specifies the permissions for the EDA resources specified by the rule. Set to **none**, **read**, or **readwrite**.
- **Resources**: The resource names of the resources controlled by the rule.

    An asterisk `*` indicates wildcard, which means match any resource in the specified API group.

### Table rules

Table rules are similar to resource rules, except that they are relevant to the API endpoints used for querying the EDA database. A table rule is defined by the following parameters:

- **Path**: Specifies the path to the database table for which this rule applies.

    The `/` character at the end of the path indicates the final portion of the URL path can be anything, if the prefix matches.

    `*//` at the end of the path indicates that the URL path can be anything if the prefix matches.

- **Permissions**: Specifies the permissions for the EDA resources specified by the rule. Set to **none** or **read**; writing to the database tables is not allowed.

To simplify user access to resource-related dashboards and queries, users are granted read permission to the following paths when they have the equivalent resource rules:

- `.namespace.resources.cr.{group}.{version}.{kind}.**`
- `.namespace.node.normal.{group}.{version}.{kind}.**`
- `.namespace.apps.cr.{group}.{version}.{kind}`.\*\*

### URL rules

URL rules define generic enforcement of URL paths exposed by an API server. A URL rule is defined by the following parameters:

- **Path**: the API server-proxied URL path to which this rule applies.

    The `/` character at the end of the path indicates the final portion of the URL path can be anything, if the prefix matches.

    `*//` at the end of the path indicates that the URL path can be anything if the prefix matches.

    A `path` may contain a single asterisk `*` to include fields (but not children) of the path. In the following example, the path includes all fields available directly under `admin`, but would not include child paths like `/core/admin/groups/{uuid}`:

    `/core/admin/*`

- **Permissions**: Specifies the permissions for the API server-proxied URL path for the rule. Set to **none**, **read**, or **readwrite**

### Rule behavior

EDA rules are additive. Users are granted the combined permission of all rules in the roles assigned to their user groups. If a request does not match any rule, it is implicitly denied.

'None' permission rules act as an override; these are enforced before any other rule.

EDA supports the principles of additive permissions and least permission, aligning with Kubernetes recommendation described in [https://kubernetes.io/docs/concepts/security/rbac-good-practices/\#least-privilege](https://kubernetes.io/docs/concepts/security/rbac-good-practices/#least-privilege).

The following are best-practice recommendations for administrators:

- Create explicit read/readWrite rules for the resource, table, and URLs required for a role.
- Avoid wildcard read/readWrite rules where possible. A wildcard gives access to resources that exist today and resources that may exist in the future.
- Avoid ‘None’ rules where possible. If resource, table, or URL access is not required for a role, do not include a matching rule for that resource/table/URL (that is, implicit deny). 'None' rules are explicit denials. They have priority over all permissive rules assigned to the user, including the rules defined in other groups and roles.

## Creating a cluster role <span id="create-cluster-roles"></span>

/// html | div.steps

A `ClusterRole` resource defines a set of permissions to access EDA resources.

1. From the **System Administration** navigation panel, expand the **USER MANAGEMENT** group, then select **Cluster Roles**.

2. If not already selected, click **Resources** from the **Cluster Roles** drop-down list.

3. Click **Create**.

4. Provide the following metadata for the `ClusterRole` resource:

    - name
    - namespace (if none is selected)
    - labels
    - annotations

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

### `ClusterRole` resource

```
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
        - fabrics.eda.nokia.com/v1alpha1
      resources:
        - fabrics
      permissions: readWrite
    - apiGroups:
        - fabrics.eda.nokia.com/v1alpha1
      resources:
        - '*'
      permissions: read
  urlRules:
    - path: /core/transaction/v1/**
      permissions: read
  tableRules:
    - path: .namespace.node.**
      permissions: read
```

## Default cluster role <span id="default-cluster-role"></span>

EDA provides a default `system-administrator` cluster role with the following configuration:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: system-administrator
rules:
- apiGroups:
  - "*"
  resources:
  - "*"
  permissions: readWrite
urlRules:
- path: "/**"
  permissions: readWrite
tableRules:
- table: ".**"
  permissions: read
```

## Creating a role <span id="create-roles"></span>

The Role resource defines a set of permissions to access EDA resources. The Role resource exists within a namespace.

/// html | div.steps

1. From the **System Administration** navigation panel, expand the **USER MANAGEMENT** group, then click **Roles**.

2. If not already selected, click **Resources** from the **Roles** drop-down list.

3. Click **Create**.

4. Provide the following metadata for this resource:

    - name
    - namespace \(if none is selected\)
    - labels
    - annotations
  
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

///

### `Role` resource

```
apiVersion: core.eda.nokia.com/v1
kind: Role
metadata:
  annotations: {}
  name: ns-admin
  namespace: eda
  labels: {}
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
  description: ''
status: {}
```
