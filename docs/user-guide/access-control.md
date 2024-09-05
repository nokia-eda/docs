# Access Control

/// warning
This page covers access control of the EDA API Server and GUI.
The EDA Config Engine can also be operated via the Kubernetes API. Kubernetes RBAC configuration should be considered when securing EDA Config Engine access.
///

Role-based access control (RBAC) restricts access to resources based on the user's role in your organization.
EDA uses [KeyCloak](https://www.keycloak.org/) to authenticate users and group membership, and the EDA API server handles request authorization based on the role(s) assigned to user group(s).

## Create a Local User

EDA Users are stored in KeyCloak. The EDA API (and GUI) provides a front-end to manage local users. In the GUI, you'll find Users in the `System Administration` panel under `RBAC` > `User Management` > `Users`.

User passwords set by an administrator can be flagged as temporary; this will prompt the user to change the password on first login. Administrators can also perform password resets, which sends the user an email with a password reset link.

/// Note
In 24.8.1, email server configuration is not exposed in the EDA API/GUI. This must be configured directly in KeyCloak.
///

## Define Role Permissions

EDA `Cluster Roles` define the which permissions users have for the EDA API/GUI. Each ClusterRole can include URL, Resource, and Table rule sets.

/// Note
A future release will introduce `Roles` for namespace specific permissions. Cluster Roles are cluster wide.

EDA `ClusterRoles` & `Roles` are not the same as Kubernetes `ClusterRoles` & `Roles`. Kubernetes RBAC controls are not used by the EDA API.
///

### ClusterRoles Rule Types

* **Resource Rules** controls EDA resource permissions using Group-Version-Kind (GVK) semantics.
Each Resource Rule can include one or more API Groups in group/version format (e.g. "core.eda.nokia.com/v1") and one or more Resources (i.e. Kind). Either can be an exact match or wildcard (`*`).

* **Table Rules** provides a fine-tuning of permissions for queries to EDB.
URL Rules support wildcarding of the final EDA path segment (`.*`) or multiple EDA path segments (`.**`)
When wildcards are used, the rule with the longest (i.e. most specific) match takes priority.

* **URL Rules** allows you to set API server URL path to Read, Read Write, or None.
URL Rules support wildcarding of the final URL segment (`/*`) or multiple URL segments (`/**`)
When wildcards are used, the rule with the longest (i.e. most specific) match takes priority.

/// warning | Required URL Rules

In 24.8.1, there are a few gotchas when configuring Resource and Table permissions.

To work with resources in the EDA GUI users require these additional URL Rules:

* read on path `/openapi/**` - This allow the GUI to display resource schemas
* readWrite on path `/core/user-storage/**` - This provide access to UI setting and transaction basket
* readWrite on path `/core/transaction/**` - This lets the user execute transactions

To execute queries on a table, a readWrite URL Rule on path `/core/query/**` is required.
///

### Example ClusterRoles

/// admonition | Example 1: Read only for everything
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

/// details | Example 2: Read and Write for Fabric resources and read-only for related resources
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
    - path: /core/user-storage/**
      permissions: readWrite
    - path: /core/transaction/**
      permissions: readWrite
  tableRules: []
```

///

/// details | Example 3: Permission to run queries and update alarms (ack/delete/suppress/etc)
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
    - path: /core/query/**
      permissions: readWrite
```

///

## Bind Roles and Users Together in a Group

User Groups in EDA are what connects a User to a Role. A User can be part of multiple Groups, and each Group may have multiple Roles.

EDA User Groups are stored in KeyCloak. The EDA API (and GUI) provides a front-end to manage User Groups. You'll find User Groups in the `System Administration` panel under `RBAC` > `User Management` > `User Groups`.

## Remote Directories

Remote directories such as OpenLDAP or Active Directory can be used to sync users and groups with KeyCloak.

/// Note
In 24.8.1 directory configuration is only available via the EDA API (i.e. not available in the GUI)
///

## Password Policy

A password policy allows a system administrator to define requirements around local user password complexity. Note that these requirements do not apply to users sourced from a remote directory.

/// Note
In 24.8.1 password policy configuration is only available via the EDA API (i.e. not available in the GUI)
///
