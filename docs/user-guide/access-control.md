# Access Control

/// warning
This page covers access control of the EDA API Server and GUI.
The EDA Config Engine can also be operated via the Kubernetes API. Kubernetes RBAC configuration should be considered when securing EDA Config Engine access.
///

Role-based access control (RBAC) restricts access to resources based on the user's role in your organization.
EDA uses [KeyCloak](https://www.keycloak.org/) to authenticate users and group membership, and the EDA API server handles request authorization based on the role(s) assigned to user group(s).

## Local Users

EDA Users are stored in KeyCloak. The EDA API (and GUI) provides a front-end to manage local users. In the GUI, you'll find Users in the `System Administration` panel under `RBAC` > `User Management` > `Users`.

User passwords set by an administrator can be flagged as temporary; this will prompt the user to change the password on first login. Administrators can also perform password resets, which sends the user an email with a password reset link.

/// Note
In 24.12, email server configuration is not exposed in the EDA API/GUI. This must be configured directly in KeyCloak.
///

## Role Permissions

EDA `Cluster Roles` and `Roles` define the which permissions users have for the EDA API/GUI[^1].

`Roles` define permissions within a specific namespace, whereas `Cluster Roles` apply to all namespaces.

Non-namespaced API endpoints can only be enforced by `Cluster Roles`. This includes cluster-wide resources (e.g. httpproxies), EDA administrative APIs, transaction results, etc. Basicly, any API that doesn't specify a namespace in the path or payload is enforced by `Cluster Roles`.

The EDA UI allows you to switch between 'All Namespaces' and specific namespace views. In the 'All Namespaces' view, requests use cluster-wide APIs which require ClusterRole permission. Users with permission only for specific namespaces will not see their resources in the 'All Namespaces' view.

### Access Rule Types

Each `ClusterRoles` & `Roles` provide the following rule types:

* **Resource Rules** controls EDA resource permissions using Group-Version-Kind (GVK) semantics.
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

## User Groups & Role Bindings

User Groups in EDA associate users to roles. A User can be part of multiple User Groups, and each User Group may have multiple Roles.

EDA User Groups are stored in KeyCloak. The EDA API (and GUI) provides a front-end to manage User Groups. You'll find User Groups in the `System Administration` panel under `RBAC` > `Users & Groups` > `User Groups`.

## Remote Directories

Remote directories such as OpenLDAP or Active Directory can be used to sync users and groups with KeyCloak.

/// admonition | Directory Configuration
    type: subtle-note
In 24.12, directory configuration is only available via the EDA API (i.e. not available in the GUI)
///

## Password Policy

A password policy allows a system administrator to define requirements around local user password complexity & brute force protection. Note that these requirements do not apply to users sourced from a remote directory.

## Tips and Tricks

### UI Required Rules

In 24.12, to work with resources in the EDA GUI, users require these rules in a ClusterRole:

* URL Rule read on path `/openapi/**` - This allows the GUI to display resource schemas
* Resource Rule read group `core.eda.nokia.com/v1` resource `namespaces` - This allows the GUI to populate the namespace selector

/// details | ClusterRole - Basic UI permissions
    type: code-example

``` yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterRole
metadata:
  name: basic
  labels: null
  namespace: default
spec:
  description: 'Basic permissions for EDA UI'
  resourceRules:
    - apiGroups:
        - core.eda.nokia.com/v1
      permissions: read
      resources:
        - namespaces
  urlRules:
    - path: /openapi/**
      permissions: readWrite
  tableRules: []

```

///

### Derived Resource and Node Config Access

Users can submit a transaction only if they have readWrite permission for all input CRs in the transaction.
However, EDA apps triggered by the transaction may derive resources for which the user does not have direct permission.

All resources updated/created/deleted during a transaction are visible in the transaction result diff, this may include full node configs. 
The following ClusterRole can be used to block user access to this information:

/// details | ClusterRole - Deny access to transaction diffs and node config
    type: code-example

``` yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterRole
metadata:
  name: deny-nodeconfig
  labels: null
  namespace: default
spec:
  description: 'Deny access to transaction diffs and node config APIs'
  resourceRules: []
  tableRules:
    - path: .**
      permissions: read
  urlRules:
    - path: /core/alltransaction/v1/diffs/**
      permissions: none
    - path: /core/transaction/v1/diffs/**
      permissions: none
    - path: /core/nodeconfig/**
      permissions: none
```

///

### Topology Access in Specific Namespaces

In 24.12, topology and overlay descriptions are cluster-wide but the topology state is namespaced.
Viewing Topologies in the UI for specific namespaces requires a combination of ClusterRoles and Roles.

/// details | ClusterRole - Physical topology
    type: code-example

``` yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterRole
metadata:
  name: topology-definitions
  labels: {}
  annotations: {}
spec:
  description: Access descriptions of physical topology and its overlays
  urlRules:
    - path: /core/topology/v1
      permissions: read
    - path: /core/topology/v1/topologies.eda.nokia.com_v1alpha1_physical
      permissions: read
    - path: /core/topology/v1/topologies.eda.nokia.com_v1alpha1_physical/overlay
      permissions: read
    - path: /core/topology/v1/topologies.eda.nokia.com_v1alpha1_physical/overlay/**
      permissions: read
  resourceRules: []
  tableRules: []
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
  labels: {}
  annotations: {}
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
  namespace: default
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
  namespace: default
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
  namespace: default
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
