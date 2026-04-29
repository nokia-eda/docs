# InfluxDB Exporter

| <nbsp> {: .hide-th } |                                                                 |
| -------------------- | --------------------------------------------------------------- |
| **Description**      | InfluxDB Exporter exports alarms, resources, or query results to InfluxDB. |
| **Author**           | Nokia                                                           |
| **Catalog**          | [nokia-eda/catalog][catalog]                                    |
| **Language**         | Go                                                              |

[catalog]: https://github.com/nokia-eda/catalog

## Overview

The InfluxDB Exporter app exports Nokia EDA data into an InfluxDB server. It provides two groups of resources:

* `Server` and `ClusterServer`: define the InfluxDB destination and connection settings
* `Export` and `ClusterExport`: define what data to write and which server and bucket should receive it

The current app API is `influxdb.eda.nokia.com/v1alpha1`.

## Installation

The InfluxDB Exporter app can be installed using [Nokia EDA Store](../apps/index.md#nokia-eda-store) or by running an `AppInstaller` workflow with `kubectl` or `edactl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/influxdb-exporter/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/influxdb-exporter/install.yml"
EOF
```

///

### Install Settings

The app supports install-time settings through `spec.apps[].appSettings` in the `AppInstaller` workflow spec:

* `influxDBExporterCPULimit`: CPU limit for the exporter pod. Default: `"1"`
* `influxDBExporterMemoryLimit`: memory limit for the exporter pod. Default: `"1Gi"`
* `influxDBProxyConfig`: ConfigMap name used for `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`. Default: `proxy-config`

> The default requests are set to `500m` CPU and `500Mi` memory.

These settings control the deployment in the Nokia EDA base namespace and can be provided through `spec.apps[].appSettings` in the `AppInstaller` workflow or directly in the Nokia EDA UI.

/// tab | YAML

```yaml
--8<-- "docs/apps/influxdb-exporter/install-with-settings.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/influxdb-exporter/install-with-settings.yml"
EOF
```

///

## Getting Started

After installation, create:

* a `Server` or `ClusterServer` to define how to connect to InfluxDB instance
* an `Export` or `ClusterExport` to define what data should be exported and which InfluxDB bucket to write to

Namespace rules:

* `Server` and `Export` are used within a user namespace such as `eda`
* `ClusterServer` and `ClusterExport` are used from the EDA base namespace for centralized exports

## Server Resources

A server resource defines the target InfluxDB connection.

Notable specification fields:

* `url`: InfluxDB base URL
* `org`: InfluxDB organization
* `credentialsSecret`: Secret containing either `token` or both `username` and `password`
* `batchSize`: number of points buffered per write request
* `flushTimer`: flush interval for buffered writes
* `timestampPrecision`: `seconds`, `milliseconds`, `microseconds`, or `nanoseconds`
* `useGzip`: enable gzip compression on write requests
* `tls`: optional TLS configuration

TLS options:

* `tls.fromFiles`: read `caFile`, `certFile`, and `keyFile` from mounted files
* `tls.fromSecret.name`: read `tls.crt`, `tls.key`, and optional `ca.crt` from a Secret in the same namespace as the server resource

The resource status contains the fields related to the connectivity parameters of this instance:

* `connected`
* `error`
* `lastChecked`

/// tab | YAML

```yaml title="Example Server resource"
--8<-- "docs/apps/influxdb-exporter/server.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/influxdb-exporter/server.yml"
EOF
```

///

## Export Resources

An export resource defines what data is written and which server and bucket receive it.

Each `spec.servers[]` entry references:

* `name`: the `Server` or `ClusterServer` resource
* `bucket`: the InfluxDB bucket to write to

Supported sources:

* `spec.exports.alarms`
* `spec.exports.resource`
* `spec.exports.query`

### Alarm Source

Use `spec.exports.alarms` to export Nokia EDA alarms.

Important fields:

* `include`: list of alarm types to include, or `["*"]` for all alarms
* `exclude`: optional list of alarm types to suppress

For `ClusterExport`, `spec.exports.alarms.namespaces` optionally limits which namespaces contribute alarms.

Alarm points are written with:

* measurement name `alarms`
* tags such as `group`, `kind`, `type`, `resource`, `severity`, `sourceGroup`, `sourceKind`, and `sourceResource`
* remaining alarm fields stored as Influx fields

### Resource Source

Use `spec.exports.resource[]` to stream resource data from Nokia EDA resources.

Important fields:

* `group`, `version`, `kind`: identify the CR type to export
* `name`: optional single resource name
* `namespaces`: cluster export only; limit which namespaces contribute resources

Resource points are written with:

* measurement name equal to the lowercased resource kind
* tags built from JsPath keys and Kubernetes labels
* flattened object content as fields

### Query Source

Use `spec.exports.query[]` to write arbitrary state DB query results.

Important fields:

* `path`: JsPath to export
* `fields`: optional list of fields; if omitted, all fields are exported
* `where`: optional EQL filter
* `mode`: `on-change`, `periodic`, or `both`
* `period`: required for periodic behavior
* `customization`: optional regex-based measurement, tag, and field renaming

Path behavior:

* for `Export`, omit the `.namespace...` prefix because the exporter automatically scopes the path to the export namespace
* for `ClusterExport`, use the full path, typically including `.namespace...` when you want cross-namespace data

Query points are written with:

* measurement name derived from the JsPath, joined with underscores
* tags derived from JsPath keys
* flattened object content as fields

/// tab | YAML

```yaml title="Example Export resource"
--8<-- "docs/apps/influxdb-exporter/export.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/influxdb-exporter/export.yml"
EOF
```

///

## Cluster-Scoped Resources

Use `ClusterServer` and `ClusterExport` when you want centralized writes from the Nokia EDA base namespace.

Cluster-specific behavior:

* `ClusterExport` supports namespace filters for alarm and resource sources
* `ClusterExport` can query across namespaces
* `ClusterServer` uses the same connection model as `Server`, but is intended for centralized use

/// tab | YAML

```yaml title="Example ClusterServer resource"
--8<-- "docs/apps/influxdb-exporter/clusterserver.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/influxdb-exporter/clusterserver.yml"
EOF
```

///

/// tab | YAML

```yaml title="Example ClusterExport resource"

/// tab | YAML

```yaml
--8<-- "docs/apps/influxdb-exporter/clusterexport.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/influxdb-exporter/clusterexport.yml"
EOF
```

///

## Connectivity Alarm

The app raises an EDA alarm when it cannot connect to a configured InfluxDB server.

Alarm details:

* Alarm type: `InfluxDBServerConnectionFailed`
* Severity: `major`
* Resource kind: `Server` or `ClusterServer`
* Resource: server name

Typical causes:

* wrong InfluxDB URL or port
* invalid token or username/password secret
* bad TLS certificate, key, or CA configuration
* network connectivity or proxy configuration issues

The alarm clears automatically after successful connectivity checks.

## Validation Notes

When creating resources, follow these rules:

* `flushTimer` must be at least `1s`
* `batchSize` must be at least `1`
* if a TLS client certificate or key is set in `tls.fromFiles`, the matching key or certificate must also be set
* every export must define at least one source and at least one server
* alarm exports must set `include` or `exclude`
* resource exports must set `group`, `version`, and `kind`
* query customizations use regexes, so invalid regex patterns are rejected
