# NATS Exporter

| <nbsp> {: .hide-th } |                                                                 |
| -------------------- | --------------------------------------------------------------- |
| **Description**      | NATS Exporter publishes EDA alarms or query results to NATS or JetStream. |
| **Author**           | Nokia                                                           |
| **Supported OS**     | N/A                                                             |
| **Catalog**          | [nokia-eda/catalog][catalog]                                    |
| **Language**         | Go                                                              |

[catalog]: https://github.com/nokia-eda/catalog

## Overview

The NATS Exporter app lets you publish EDA alarms or query results into a NATS or JetStream server. It supports two kinds of resources:

* `Publisher` and `ClusterPublisher`: define how to connect to a NATS or JetStream server.
* `Export` and `ClusterExport`: define what data to publish and which publishers should receive it.

Use namespace-scoped resources when you want to export data only from a single user namespace. Use cluster-scoped resources in the EDA base namespace when you want centralized exports across namespaces.

## Installation

The NATS Exporter app can be installed using [EDA Store](app-store.md) or by running an `AppInstaller` workflow with `kubectl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/nats-exporter/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/nats-exporter/install.yml"
EOF
```

///

### Install Settings

The app supports install-time sizing through `spec.apps[].appSettings` in the `AppInstaller` workflow spec.

Available settings:

* `exporterCPULimit`: CPU limit for the NATS exporter pod. Default: `"1"`
* `exporterMemoryLimit`: memory limit for the NATS exporter pod. Default: `"1Gi"`

These settings control the pod resource limits for the exporter deployment in the EDA base namespace.

The shipped deployment currently keeps resource requests fixed at:

* CPU request: `500m`
* memory request: `500Mi`

### Example Install With Settings

/// tab | YAML

```yaml
--8<-- "docs/apps/nats-exporter/install-with-settings.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/nats-exporter/install-with-settings.yml"
EOF
```

///

## Getting Started

After the app is installed, create:

* a `Publisher` or `ClusterPublisher` to define the destination NATS connection
* an `Export` or `ClusterExport` to define the data to publish

Use the `nats.eda.nokia.com/v1` API for new resources. The older `v1alpha1` API is still served for compatibility, but it is now deprecated and is marked for removal in a future release.

Namespace rules:

* `Publisher` and `Export` are namespace-scoped. Create them in a user namespace such as `eda`.
* `ClusterPublisher` and `ClusterExport` are intended for the EDA base namespace. The controller only activates cluster-scoped resources from its own namespace.

## Publisher Resources

A publisher defines how the app connects to the NATS or JetStream server.

Important fields:

* `spec.address`: comma-separated NATS server addresses
* `spec.type`: `NATS` or `Jetstream`
* `spec.clientName`: NATS client name
* `spec.credentialsSecretName`: optional Secret containing `username` and `password`
* `spec.maxPendingAcks` and `spec.maxWait`: JetStream-specific publish tuning
* `spec.tls`: optional TLS settings

TLS options:

* `tls.fromFiles`: read `caFile`, `certFile`, and `keyFile` from mounted files
* `tls.fromSecret`: read `tls.crt`, `tls.key`, and optional `ca.crt` from a Secret in the same namespace as the publisher
* `tls.trustBundle`: read `trust-bundle.pem` from a ConfigMap in the same namespace as the publisher

The publisher status reports whether the connection is currently established through `status.connected`, `status.error`, and `status.lastChecked`.

### Example Publisher

/// tab | YAML

```yaml
--8<-- "docs/apps/nats-exporter/publisher.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/nats-exporter/publisher.yml"
EOF
```

///

## Export Resources

An export defines what data is exported and where it is sent.

Supported sources:

* `spec.exports.alarms`: stream alarms from EDA
* `spec.exports.query`: stream query results from the state DB

Each destination references a publisher and defines how to derive the NATS subject:

* `subject`: use a fixed subject
* `subjectFromJsPath: true`: derive the subject from the JsPath of each update
* `subjectPrefix`: prepend a prefix when `subjectFromJsPath` is enabled

When a static `subject` is configured, the exporter also sends a sync message after the initial state sync for on-change streams.

### Alarm Source

Use `spec.exports.alarms` to stream alarms.

Important fields:

* `include`: list of alarm types to include, or `["*"]` for all alarms
* `exclude`: optional list of alarm types to suppress

For namespace-scoped `Export`, alarms come only from the export namespace.

### Query Source

Use `spec.exports.query[]` to publish arbitrary state DB data.

Important fields:

* `path`: JsPath to query. For `Export`, omit the `.namespace` prefix because the controller adds the export namespace automatically.
* `fields`: optional list of fields to include. If omitted, all fields are exported.
* `where`: optional EQL filter
* `mode`: `on-change`, `periodic`, or `both`
* `period`: required for `periodic` and `both`; minimum 10 seconds
* `includeTimestamps`: include the export timestamp in the published message

Published messages contain:

* `path`: the resolved JsPath without keys
* `entries[].keys`: path keys flattened into a map
* `entries[].fields`: exported object fields
* optional `timestamp`

### Example Export

/// tab | YAML

```yaml
--8<-- "docs/apps/nats-exporter/export.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/nats-exporter/export.yml"
EOF
```

///

## Cluster-Scoped Resources

Use `ClusterPublisher` and `ClusterExport` when you want centralized exports from the EDA base namespace.

Cluster-specific behavior:

* `ClusterPublisher` must be created in the EDA base namespace
* `ClusterExport` can stream data across namespaces
* `spec.exports.alarms.namespaces` limits which namespaces contribute alarms
* `spec.exports.query[].path` should include the full `.namespace.` prefix when you want cross-namespace query exports

### Example ClusterPublisher

/// tab | YAML

```yaml
--8<-- "docs/apps/nats-exporter/clusterpublisher.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/nats-exporter/clusterpublisher.yml"
EOF
```

///

### Example ClusterExport

/// tab | YAML

```yaml
--8<-- "docs/apps/nats-exporter/clusterexport.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/nats-exporter/clusterexport.yml"
EOF
```

///

## Connectivity Alarm

The app raises an EDA alarm when a configured NATS destination cannot be reached.

Alarm details:

* Alarm type: `NATSServerConnectionFailed`
* Severity: `major`
* Resource kind: `Publisher` or `ClusterPublisher`
* Resource: publisher name

Typical causes:

* wrong NATS server address or port
* invalid username or password secret
* TLS secret, trust bundle, or certificate paths are incorrect
* the NATS or JetStream service is down or unreachable

The alarm is cleared automatically when the publisher reconnects successfully.

## Configuration Notes

When creating resources, follow these rules:

* publisher `address` is required
* JetStream `maxPendingAcks` and `maxWait` must be at least `1`
* if TLS client certificate or key is set, the matching key or certificate must also be set
* every export must define at least one source and at least one destination
* every destination must set either `subject` or `subjectFromJsPath`
