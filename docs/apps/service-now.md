# ServiceNow

| <nbsp> {: .hide-th } |                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| **Description**      | ServiceNow creates incidents from EDA query results.                                             |
| **Author**           | Nokia                                                                                             |
| **Supported OS**     | N/A                                                                                               |
| **Catalog**          | [nokia-eda/catalog][catalog]                                                                      |
| **Language**         | Go                                                                                                |

[catalog]: https://github.com/nokia-eda/catalog

## Overview

The ServiceNow app connects EDA to a ServiceNow instance and creates incidents from matching EDA state.

It exposes four resources:

* `Instance`: namespace-scoped connection details for a ServiceNow instance.
* `Incident`: namespace-scoped incident generator that references one or more `Instance` objects.
* `ClusterInstance`: cluster-scoped connection details created in the EDA base namespace.
* `ClusterIncident`: cluster-scoped incident generator created in the EDA base namespace.

## Installation

Install the app from [EDA Store](../apps/index.md#nokia-eda-store) or with `kubectl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/service-now/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/service-now/install.yml"
EOF
```

///

## Getting Started

The setup has two steps:

1. Create an `Instance` or `ClusterInstance` that can authenticate to ServiceNow.
2. Create an `Incident` or `ClusterIncident` that references that instance and defines a query source.

/// admonition | Namespace behavior
    type: subtle-note

    `Instance` and `Incident` resources must be created outside the EDA base namespace. `ClusterInstance` and `ClusterIncident` resources must be created in the EDA base namespace.
///

### ServiceNow Credentials Secret

Each instance references a Kubernetes secret through `spec.clientCredentials`.

The secret must contain these keys:

* `client_id`
* `client_secret`
* `username`
* `password`

When the secret is referenced by name, the app looks for it in the namespace where Instance is defined. You can also refer to a secret by `namespace/name` to explicitly set the namespace the secret resides in.

Example credentials secret in namespace `eda`:

/// tab | YAML

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: sn-creds
  namespace: eda
type: Opaque
data:
  client_id: <base64-encoded-client-id>
  client_secret: <base64-encoded-client-secret>
  username: <base64-encoded-username>
  password: <base64-encoded-password>
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: sn-creds
  namespace: eda
type: Opaque
data:
  client_id: <base64-encoded-client-id>
  client_secret: <base64-encoded-client-secret>
  username: <base64-encoded-username>
  password: <base64-encoded-password>
EOF
```

///

### Instance Resource

An instance defines how EDA connects to ServiceNow.

Important fields:

* `url`: base URL of the ServiceNow instance.
* `version`: optional ServiceNow API version, for example `v2`.
* `clientCredentials`: secret reference containing OAuth and user credentials.
* `timeout`, `retryInterval`, `retryCount`: request behavior for ServiceNow API calls.

After the resource is created, the controller continuously checks connectivity and updates:

* `status.reachable`
* `status.errorReason`
* `status.lastChecked`

Example namespace-scoped `Instance`:

/// tab | YAML

```yaml
--8<-- "docs/apps/service-now/instance.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/service-now/instance.yml"
EOF
```

///

### Incident Resource

An `Incident` or `ClusterIncident` subscribes to EDA state and creates incidents in all referenced ServiceNow instances.

Important fields:

* `enabled`: whether the incident generator is active.
* `instance`: list of instance names to use as destinations.
* `sources.query.table`: the EDA table to watch.
* `sources.query.where`: filter applied to the subscription.
* `sources.query.fields`: optional list of fields to fetch. If omitted, all fields of the subscribed table are used.
* `sources.query.autoResolve`: resolves matching ServiceNow incidents when the object disappears.

The controller generates a deterministic `correlation_id` from the incident name and object path. When `autoResolve` is enabled, it looks up incidents with that correlation ID and updates them to a resolved state.

### Query Templates

The query source builds the ServiceNow incident body using [Go templates](https://pkg.go.dev/text/template). Common fields include:

* `shortDescription`
* `description`
* `callerId`
* `assignedTo`
* `assignmentGroup`
* `state`
* `priority`
* `urgency`
* `impact`
* `category`
* `subCategory`
* `closeCode`
* `closeNotes`
* `resolutionCode`
* `cmdbci`
* `location`
* `customFields[]`

Because many returned keys contain dots, `index` is usually the easiest way to reference them, for example `{{ index . "node.name" }}`.

For a namespace-scoped `Incident`, paths that start with `.namespace` are automatically rewritten so the subscription stays inside that namespace.

Example `Incident`:

/// tab | YAML

```yaml
--8<-- "docs/apps/service-now/incident.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/service-now/incident.yml"
EOF
```

///

## Cluster-Scoped Resources

Use `ClusterInstance` and `ClusterIncident` when you want to manage ServiceNow integration from the EDA base namespace.

The fields are the same as the namespace-scoped resources, but:

* `ClusterInstance` must exist in the EDA base namespace.
* `ClusterIncident` references `ClusterInstance` names.
* Query subscriptions are not namespace-rewritten, so they can watch cross-namespace data.

## Advanced Configuration

The app installer exposes the following runtime settings:

* `snowCpuLimit`: CPU limit for the controller.
* `snowMemoryLimit`: memory limit for the controller.
* `snowProxyConfig`: config map name used for `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`.

If you need a proxy, create or reuse a config map such as `proxy-config` in the EDA base namespace with those standard keys.
