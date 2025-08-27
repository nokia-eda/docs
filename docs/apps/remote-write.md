# Remote Write

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------- |
| **Description**      | The Remote Write app exports metrics to servers adhering to Prometheus Remote-Write Specifications |
| **Author**           | Nokia                                                                                                   |
| **Supported OS**     | N/A                                                                                            |
| **Catalog**          | [nokia-eda/catalog][catalog]                                                                            |
| **Source Code**      | <small>coming soon</small>                                                                              |

[catalog]: https://github.com/nokia-eda/catalog

---

## Overview

The Remote Write app enables exporting network and EDA metrics to remote Prometheus-compatible servers using the [Remote-Write specification v1.0](https://prometheus.io/docs/specs/prw/remote_write_spec/). The app provides resources to define the metrics to export and the destinations to send them to.

Application components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>
-{{icons.default_category_icon("REMOTEWRITE")}}-

* Cluster Destinations
* Cluster Exporters
* Destinations
* Exporters

</div>
</div>
///

## Installation

Notifier app can be installed using [EDA Store](app-store.md) or by running the app-installer workflow with `kubectl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/remote-write/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/remote-write/install.yml"
EOF
```

///

## Getting Started

After installing the app, you can configure:

* **Export** and **ClusterExport**: Define metrics to collect (with filtering, mapping, renaming, labels, etc.).
* **Destination** and **ClusterDestination**: Define remote write endpoints (with TLS, authentication, and buffering).

## Example Resources

### Destination

Defines a remote server to which metrics are written. Supports optional TLS, authentication, custom headers, retries, and timeouts.

/// tab | YAML

```yaml
--8<-- "docs/apps/remote-write/destination.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/remote-write/destination.yml"
EOF
```

///

### Export: Interfaces Statistics

Defines what metrics to export and to which destinations. Metrics are retrieved from the state DB at the given `path` and can include optional filtering, labeling, and transformation.

/// tab | YAML

```yaml
--8<-- "docs/apps/remote-write/export.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/remote-write/export.yml"
EOF
```

///

---

## Advanced Configuration

### Destination Resource Options

* **authentication**: `username`/`password` for basic auth.
* **authorization**: `type` (for example, Bearer) and token-based credentials.
* **tls**: Provide CA/cert/key file paths and `skipVerify` flag.
* **writeOptions**: Tune buffer size, flush interval, custom HTTP headers, retries, and timeouts.
* **metadata**:

    * `include`: Whether to send metadata.
    * `interval`: Frequency of metadata updates.
    * `maxEntriesPerWrite`: Limit per request.

### Export Resource Options

* **path** (required): State DB path to collect from.
* **mode**: `periodic`, `on-change`, or `periodic-on-change`.
* **interval**: Polling interval for metric collection.
* **fields**: Optional subset of fields to export.
* **labels**: Static and dynamic labels.
* **mappings**: Transform field values using regex and numeric replacements.
* **metricName**: Rename metrics using regex.
* **resource**: Use a CR as source; metric value is `1`, and CR labels are used as metric labels.
* **where**: Filtering condition (e.g., `admin-state = enable`).
