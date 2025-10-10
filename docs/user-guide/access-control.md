# Access Control

/// warning
This page covers access control of the EDA API Server and GUI.
The EDA Config Engine can also be operated via the Kubernetes API. Kubernetes RBAC configuration should be considered when securing EDA Config Engine access.
///

Role-based access control (RBAC) restricts access to resources based on the user's role in your organization.
EDA uses [KeyCloak](https://www.keycloak.org/) to authenticate users and group membership, and the EDA API server handles request authorization based on the role(s) assigned to user group(s).

## Users & User Groups

EDA users and user groups are stored in KeyCloak. The EDA API (and GUI) exposes the most common KeyClock administrative actions including User and User Group management. In the EDA UI, you'll find Users and User Groups in the `System Administration` panel under `User Management` > `User Management`.

User passwords set by an administrator can be flagged as temporary; this will prompt the user to change the password on first login. Administrators can also perform password resets, which sends the user an email with a password reset link.

/// Note
Email server configuration is not exposed in the EDA API/GUI. This must be configured directly in KeyCloak.
///

### Federations

Federations configure users and user group synchronization with remote directories such as OpenLDAP or Active Directory. In the GUI, federation providers can be configured in the `System Administration` panel under `User Management` > `User Management`.

### Password Policy

A password policy allows a system administrator to define requirements around local user password complexity & brute force protection. Note that these requirements do not apply to users sourced from a remote directory. In the GUI, you'll find Users and User Groups in the `System Administration` panel under `User Management` > `Password Policy`.

## Roles

EDA `Cluster Roles` and `Roles` define the which permissions users have for the EDA API/GUI[^1].

`Roles` define permissions within a specific namespace, whereas `Cluster Roles` apply to all namespaces.

Non-namespaced API endpoints can only be enforced by `Cluster Roles`. This includes cluster-wide resources (e.g. httpproxies), EDA administrative APIs, transaction results, etc. Basically, any API that doesn't specify a namespace in the path or payload is enforced by `Cluster Roles`.

The EDA UI allows you to switch between 'All Namespaces' and specific namespace views. In the 'All Namespaces' view, requests use cluster-wide APIs which require ClusterRole permission. Users with permission only for specific namespaces will not see their resources in the 'All Namespaces' view.

### Access Rule Types

Both `ClusterRoles` & `Roles` provide the following rule types:

* **Resource Rules** controls EDA resource and workflow permissions using Group-Version-Kind (GVK) semantics.
Each Resource Rule can include one or more API Groups in group/version format (e.g. "core.eda.nokia.com/v1") and one or more Resources (i.e. Kind). Either can be an exact match or wildcard (`*`).

* **Table Rules** provides a fine-tuning of permissions for queries to EDB.
Table Rules support wildcarding of the final EDA path segment (`.*`) or multiple EDA path segments (`.**`)

* **URL Rules** define permission for EDA API endpoints based on their URL path.
URL Rules support wildcarding of the final URL segment (`/*`) or multiple URL segments (`/**`).
URL Rule permission is not required for API endpoints which are Resource Rule or Table Rule enforced.

### Requests Matching Multiple Rules

Rules in EDA are additive. If a request matches both a `read` and `read write` rule, the user is granted `read write` access.
If no rule is matched, the request is implicitly denied.

`None` permissions act as an override. If there is a matching `none` rule, access is always denied.

/// admonition | Avoid `None` Rules
    type: subtle-note
If resource/table/URL access is not required for a role, the best practice is to not include a matching rule for that resource/table/URL. This ensures that users with multiple roles receives all required permissions.
///

## Assigning Roles to Users

Roles are associated to Users via User Groups. A User can be part of multiple User Groups, and each User Group may have multiple Roles.

## Tips and Tricks

### Transaction Result Access

Access to Transaction results is based on the user's access to the input resources of that transaction.  
If the user has read permission for **all** the input resources of a transaction, they can list all changed resources (both input and derived) and view the resource diffs.  
If the user has read permission for **none** or **some** of the input resources, they can not list any derived resources or view their diffs.  
Access to Node Configuration diffs must be opted-in using a urlRule. This is because the Node Configuration diff API returns the full node config, and not limited to the scope of the transaction.

To revert a transaction, the user must has readWrite permission for all input resources of the transaction.  
To restore the EDA cluster to a specific transaction, the user must have readWrite permission to the restore API from a ClusterRole URL Rule. Restore is a powerful action which should be limited to trusted administrators.

### Workflow Access

Just like EDA Resources, EDA Workflows follow the Kubernetes Group-Version-Kind (GVK) resource model. resourceRules grant read and readWrite permission to workflows.

Additionally, users inherit access to subflows based on their access to the top-level parent flow.  
For example, a `DeployImage` workflow creates `Ping` subflows during it's pre and post check stages. If user A has read permission to the 'DeployImage' workflow definition they will be able to read the subflow results even if they do not have access to the `Ping` workflow definition.

### Topology Access in Specific Namespaces

Topology diagrams and their overlays are defined cluster-wide in EDA, but the state data which populates the topology diagrams is namespaced. Therefore, to view topologies in the UI for specific namespaces a combination of ClusterRoles and Roles is required.

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
  tableRules: []
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
  resourceRules: []
  tableRules: []
```

///

### More Example Roles

/// details | ClusterRole - Read only everything
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

/// details | ClusterRole - Read and write fabric resources and read-only related resources
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
  tableRules: []
```

///

/// details | ClusterRole - run queries and update alarms (ack/delete/suppress/etc)
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
  resourceRules: []
  tableRules:
    - path: .**
      permissions: read
  urlRules:
    - path: /core/alarm/**
      permissions: readWrite
```

///

[^1]: EDA `ClusterRoles` & `Roles` are not the same as Kubernetes `ClusterRoles` & `Roles`. Kubernetes RBAC controls are not used by the EDA API.
