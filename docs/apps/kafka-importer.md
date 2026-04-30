# Kafka Importer

| <nbsp> {: .hide-th } |                                                                 |
| -------------------- | --------------------------------------------------------------- |
| **Description**      | Kafka Importer consumes Kafka messages and writes them into EDA state. |
| **Author**           | Nokia                                                           |
| **Catalog**          | [nokia-eda/catalog][catalog]                                    |
| **Language**         | Go                                                              |

[catalog]: https://github.com/nokia-eda/catalog

## Overview

The Kafka Importer app subscribes to Kafka topics, optionally filters messages with CEL, renders EDA paths and payloads with Go templates, and writes the result into the EDA state database.

The app provides two resources:

* `Consumer`: namespace-scoped consumer intended for a user namespace
* `ClusterConsumer`: intended for use from the EDA base namespace for centralized imports

Each consumer:

* connects to one or more Kafka brokers
* joins a Kafka consumer group using `clientName`
* consumes from a single topic
* optionally applies SASL and TLS settings
* optionally filters messages with `spec.condition`
* renders `spec.path` and `spec.data`
* updates EDA state with the rendered output

## Installation

The Kafka Importer app can be installed using [EDA Store](../apps/index.md#nokia-eda-store) or by running an `AppInstaller` with `kubectl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/kafka-importer/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/kafka-importer/install.yml"
EOF
```

///

### Install Settings

The app supports install-time settings through `spec.apps[].appSettings` in the `AppInstaller`.

Available settings:

* `cpuLimit`: CPU limit for the controller pod. Default: `"1"`
* `memoryLimit`: memory limit for the controller pod. Default: `"1Gi"`

The deployment keeps requests fixed at `500m` CPU and `500Mi` memory.

### Example Install With Settings

/// tab | YAML

```yaml
--8<-- "docs/apps/kafka-importer/install-with-settings.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/kafka-importer/install-with-settings.yml"
EOF
```

///

## Getting Started

Before creating a consumer, make sure the Kafka brokers, topic, and any referenced Secrets or ConfigMaps already exist.

Namespace behavior:

* `Consumer` is created in a user namespace and its rendered path is normalized into that namespace automatically
* `ClusterConsumer` is intended to be created in the EDA base namespace and writes to the rendered path as-is
* despite its name, `ClusterConsumer` is currently used as an EDA base namespace resource rather than as a true cluster-scoped Kubernetes object

## Consumer Resources

Use `Consumer` when you want to import Kafka data into a single namespace.

Important fields:

* `spec.brokers`: list of Kafka broker addresses
* `spec.topic`: topic to consume
* `spec.clientName`: consumer-group name. If omitted, defaults to `eda-consumer-<namespace>-<name>`
* `spec.offsetResetPolicy`: `latest`, `earliest`, or `resume`
* `spec.deliveryMode`: `AtMostOnce` or `AtLeastOnce`
* `spec.condition`: optional CEL filter expression
* `spec.path`: Go template used to compute the EDA path
* `spec.data`: Go template used to compute the JSON payload written to EDA state

### Template Data Model

The Go templates are evaluated against the consumed Kafka message JSON, exposed under the root variable `.msg` (matching the CEL `msg` variable used by `spec.condition`).

Available fields in templates:

* `.msg.key`: Kafka key
* `.msg.value`: Kafka value
* `.msg.is_tombstone`: whether the Kafka message had a null value

The key may be:

* a plain string, accessible as `.msg.key`
* a JSON object, accessible with fields such as `.msg.key.user_id`

For namespace-scoped `Consumer` resources, the rendered path is normalized into the consumer namespace. For example, if your template renders `.interfaces[name="eth0"]`, the controller writes it under `.namespace{.name=="<consumer namespace>"}.interfaces[name="eth0"]`.

### CEL Filtering

If `spec.condition` is set, the message is evaluated as CEL before any state update.

CEL sees the message as:

* `msg.key`
* `msg.value`
* `msg.is_tombstone`

Typical examples:

* `msg.value.status == "active"`
* `!msg.is_tombstone`
* `msg.key.region == "us-west" && msg.value.severity >= 3`

If the condition evaluates to `false`, the message is skipped.

### Security Options

The consumer supports:

* SASL `plain`, `scram-sha-256`, `scram-sha-512`, and `oauthbearer`
* TLS from certificate files
* TLS from a Secret containing `tls.crt`, `tls.key`, and optional `ca.crt`
* trust-bundle verification via a ConfigMap containing `trust-bundle.pem`

Validation notes for security:

* `tokenUrl` must be set when using SASL `oauthbearer`
* only one of `tls.fromSecret` or `tls.fromFiles` can be set

### Example Consumer

/// tab | YAML

```yaml
--8<-- "docs/apps/kafka-importer/consumer.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/kafka-importer/consumer.yml"
EOF
```

///

## ClusterConsumer

Use `ClusterConsumer` when you want a centrally managed consumer from the EDA base namespace.

Behavior differences from `Consumer`:

* it is intended to run from the EDA base namespace
* the rendered path is written exactly as rendered, without namespace normalization
* this allows writing directly to fully qualified paths such as `.namespace{.name=="eda"}.alerts[...]`

### Example ClusterConsumer

/// tab | YAML

```yaml
--8<-- "docs/apps/kafka-importer/clusterconsumer.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/kafka-importer/clusterconsumer.yml"
EOF
```

///

## Status

Both `Consumer` and `ClusterConsumer` report runtime status through:

* `status.connected`
* `status.message`
* `status.lastError`
* `status.lastSeen`
* `status.offsets`

The controller updates status while the consumer runs, including per-partition offsets and the last successful message time.

## Configuration Notes

When creating a consumer, keep these rules in mind:

* `brokers` must contain at least one address
* `topic` is required
* `path` and `data` must be valid Go templates
* `condition` must be a valid CEL boolean expression
* for SASL `oauthbearer`, `tokenUrl` is required
* `tls.fromSecret` and `tls.fromFiles` cannot be used together

## Known Limitation

The app does not currently raise a dedicated EDA alarm for Kafka connectivity failures. Connection and processing issues are reflected through resource status fields instead.
