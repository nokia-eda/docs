# OTLP Exporter

| <nbsp> {: .hide-th } |                                                                                                      |
| -------------------- | ---------------------------------------------------------------------------------------------------- |
| **Description**      | OTLP Exporter publishes EDA metrics to an OpenTelemetry receiver.                                    |
| **Author**           | Nokia                                                                                                |
| **Supported OS**     | N/A                                                                                                  |
| **Catalog**          | [nokia-eda/catalog][catalog]                                                                         |
| **Language**         | Go                                                                                                   |

[catalog]: https://github.com/nokia-eda/catalog

## Overview

The OTLP Exporter app converts EDA state into OpenTelemetry metrics and sends them to one or more OTLP receivers.

It exposes four resources:

* `Receiver`: namespace-scoped OTLP receiver (destination for OpenTelemetry metrics).
* `MetricExport`: namespace-scoped export definition that references one or more `Receiver` objects.
* `ClusterReceiver`: cluster-scoped OTLP destination created in the EDA base namespace.
* `ClusterMetricExport`: cluster-scoped export definition created in the EDA base namespace.

The app supports both OTLP/HTTP and OTLP/gRPC receivers, optional authorization headers, and TLS options. It also raises an EDA alarm if a configured receiver becomes unreachable.

## Installation

Install the app from [EDA Store](../apps/index.md#eda-store) or with `kubectl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/otlp-exporter/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/otlp-exporter/install.yml"
EOF
```

///

## Configuration

The setup consists of two steps:

1. Create a `Receiver` or `ClusterReceiver` resource that defines where metrics should be sent.
2. Create a `MetricExport` or `ClusterMetricExport` resource that defines what to export and which receivers to use.

/// admonition | Namespace behavior
    type: subtle-note

    `Receiver` and `MetricExport` resources must be created outside the EDA base namespace. `ClusterReceiver` and `ClusterMetricExport` resources must be created in the EDA base namespace.
///

### ClusterReceiver and Receiver Resources

A receiver defines the OTLP destination and transport settings.

Important fields:

* `endpoint`: receiver URL or host endpoint.
* `protocol`: `http` or `grpc`.
* `authorization`: optional authorization type and credentials.
* `writeOptions.flushInterval`: how often buffered metrics are flushed.
* `writeOptions.bufferSize`: local buffer threshold.
* `writeOptions.maxMetricsPerExport`: maximum metrics per export request.
* `writeOptions.timeout`: export timeout.
* `writeOptions.retries`: retry behavior.
* `tls`: optional TLS configuration from files, a secret, or a trust bundle.

The controller updates the receiver status with reachability information:

* `status.reachable`
* `status.error`
* `status.lastChecked`

Example namespace-scoped `Receiver`:

/// tab | YAML

```yaml
--8<-- "docs/apps/otlp-exporter/receiver.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/otlp-exporter/receiver.yml"
EOF
```

///

### Receiver Validation

The receiver admission webhooks enforce several important rules:

* `flushInterval` must be at least `1s`.
* `timeout` must be at least `1s`.
* If `tls.fromFiles.certFile` is set, `tls.fromFiles.keyFile` must also be set, and vice versa.
* If `tls.fromFiles.skipVerify` is `false`, `tls.fromFiles.caFile` must be provided.

If `skipVerify` is `true` and a CA file is also set, the webhook accepts the resource but returns a warning that the CA file will not be used.

### ClusterMetricExport and MetricExport Resources

A `MetricExport` or `ClusterMetricExport` defines which data becomes metrics and where those metrics are sent.

Each entry under `spec.exports` can export metrics from either:

* a state DB path in `path`, or
* a custom resource source in `resource`

If `path` is omitted, `resource.group`, `resource.version`, and `resource.kind` must be provided.

Important fields:

* `path`: EDA state path to watch.
* `fields`: fields to export and whether each should be a `Gauge` or `Sum`.
* `where`: optional filter expression.
* `mode`: `on-change`, `periodic`, or `periodic-on-change`.
* `interval`: polling interval for periodic modes.
* `metricName.regex` and `metricName.replacement`: optional metric renaming.
* `attributes.static`: add fixed attributes to every metric.
* `attributes.dynamic`: derive attributes from another state path and field.
* `mappings`: map source values such as `enable`/`disable` to numeric values.
* `receivers`: one or more receiver names.

For namespace-scoped `MetricExport` resources, the controller automatically rewrites `.namespace...` paths so they stay inside the export namespace.

Example namespace-scoped `MetricExport`:

/// tab | YAML

```yaml
--8<-- "docs/apps/otlp-exporter/metricexport.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/otlp-exporter/metricexport.yml"
EOF
```

///

### Export Modes

The exporter supports three collection modes:

* `on-change`: export when matching data changes.
* `periodic`: poll and export at the configured `interval`.
* `periodic-on-change`: combine both behaviors.

For the `periodic` and `periodic-on-change`modes, the webhook requires an interval of at least `1s`.

### Value Mapping And Attributes

Metric values must become numeric before they can be sent as OTLP metrics.

Use `mappings` when the source value is text, for example:

* `enable -> 1`
* `disable -> 0`

You can also enrich exported metrics with:

* static attributes from `attributes.static`
* dynamic attributes from `attributes.dynamic`
* CR-derived metadata when using `resource`

## Receiver Alarm

The app raises an EDA alarm when it cannot connect to a configured OTLP receiver.

Alarm details:

* Alarm type: `OpenTelemetryReceiverConnectionFailed`
* Severity: `major`
* Resource: receiver name
* Group/kind: `Receiver` or `ClusterReceiver`, depending on the failing resource

The alarm description indicates that the OpenTelemetry receiver is unreachable or that the receiver resource is misconfigured.

Typical causes:

* receiver endpoint is wrong
* OTLP service is down or unreachable
* TLS settings are invalid
* authorization or custom headers are incorrect

The alarm is automatically cleared when the receiver becomes reachable again.

## Cluster-Scoped Resources

Use the `ClusterReceiver` and `ClusterMetricExport` resources when you want centralized exports from the EDA base namespace.

The field model is the same as the namespace-scoped resources, but:

* `ClusterReceiver` must exist in the EDA base namespace.
* `ClusterMetricExport` references `ClusterReceiver` names.
* cluster-scoped exports can watch cross-namespace data.
* resource-backed exports can optionally narrow to a specific namespace with `resource.namespace`.

## Advanced Configuration

The app installer exposes a few runtime settings:

* `otelCPULimit`: CPU limit for the controller.
* `otelMemoryLimit`: memory limit for the controller.
* `proxyConfigName`: config map name used for `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`.
* `otelLogLevel`: controller log level.

If you need a proxy, create or reuse a config map such as `proxy-config` in the EDA base namespace with the standard proxy keys.
