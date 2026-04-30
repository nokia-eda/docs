# NATS Importer

| <nbsp> {: .hide-th } |                                                             |
| -------------------- | ----------------------------------------------------------- |
| **Description**      | NATS Importer subscribes to NATS or JetStream and writes messages into EDA state. |
| **Author**           | Nokia                                                       |
| **Catalog**          | [nokia-eda/catalog][catalog]                                |
| **Language**         | Go                                                          |

[catalog]: https://github.com/nokia-eda/catalog

## Overview

The NATS Importer app consumes messages from NATS Core or JetStream, optionally filters them with CEL, renders EDA paths and payloads with Go templates, and writes the result into the EDA state database.

The app provides two resources:

* `Subscriber`: namespace-scoped subscriber intended for a user namespace
* `ClusterSubscriber`: intended for use from the EDA base namespace for centralized imports

Each subscriber:

* connects to one or more NATS servers
* subscribes to a subject
* can use standard NATS or JetStream
* optionally authenticates with a username/password Secret
* optionally secures the connection with TLS
* optionally filters messages with `spec.condition`
* renders `spec.path` and `spec.data`
* updates EDA state with the rendered output

## Installation

The NATS Importer app can be installed using [EDA Store](../apps/index.md#nokia-eda-store) or by running an `AppInstaller` with `kubectl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/nats-importer/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/nats-importer/install.yml"
EOF
```

///

### Configuration Notes

The controller deployment uses fixed resource settings in the shipped manifest:

* CPU limit: `"1"`
* memory limit: `1Gi`
* CPU request: `500m`
* memory request: `500Mi`

Unlike some other apps, this app does not currently expose install-time `appSettings` for CPU or memory overrides.

## Getting Started

Before creating a subscriber, make sure the NATS servers, subject, and any referenced Secrets or ConfigMaps already exist.

Namespace behavior:

* `Subscriber` is created in a user namespace and its rendered path is normalized into that namespace automatically
* `ClusterSubscriber` is intended to be created in the EDA base namespace and writes to the rendered path as-is
* despite its name, `ClusterSubscriber` is currently used as an EDA base namespace resource rather than as a true cluster-scoped Kubernetes object

## Subscriber Resources

Use `Subscriber` when you want to import NATS data into a single namespace.

Important fields:

* `spec.servers`: list of NATS server URLs
* `spec.subject`: NATS subject to subscribe to
* `spec.type`: `NATS` or `Jetstream`
* `spec.clientName`: NATS client name. For non-JetStream subscribers, if omitted it defaults to `eda-subscriber-<namespace>-<name>`. For JetStream, when set it is also used as the durable consumer name; if omitted, the controller uses an `eda-ephemeral-client-<namespace>-<name>` connection name and lets JetStream create an ephemeral consumer
* `spec.credentialsSecretName`: Secret with `username` and `password`
* `spec.condition`: optional CEL filter expression
* `spec.path`: Go template used to compute the EDA path
* `spec.data`: Go template used to compute the JSON payload written to EDA state

### JetStream Options

When `spec.type` is `Jetstream`, the app also supports:

* `spec.mode`: `push` or `pull`
* `spec.deliverPolicy`: `all`, `last`, or `new`
* `spec.ack.ackPolicy`: `all`, `explicit`, or `none`
* `spec.ack.ackWait`
* `spec.ack.maxRetries`
* `spec.batchSize`, `spec.pullTimeout`, and `spec.maxBytes` for pull mode

At runtime, the app resolves the JetStream stream from the configured subject and then starts either push or pull consumption.

JetStream consumer naming behavior:

* if `spec.clientName` is set, the app creates or updates a durable consumer with that name
* if `spec.clientName` is omitted, the app uses an `eda-ephemeral-client-<namespace>-<name>` NATS connection name and lets JetStream create an ephemeral consumer

### Template Data Model

The Go templates are evaluated against the consumed NATS message JSON, exposed under the root variable `.msg` (matching the CEL `msg` variable used by `spec.condition`).

Available fields in templates:

* `.msg.subject`: NATS subject
* `.msg.data`: parsed message payload
* `.msg.headers`: message headers

Examples:

* `.msg.data.user_id`
* `{{ index .msg.headers "Content-Type" 0 }}`
* `.msg.subject`

For namespace-scoped `Subscriber` resources, the rendered path is normalized into the subscriber namespace. For example, if your template renders `.alerts[id="123"]`, the controller writes it under `.namespace{.name=="<subscriber namespace>"}.alerts[id="123"]`.

### CEL Filtering

If `spec.condition` is set, the message is evaluated as CEL before any state update.

CEL sees the message as:

* `msg.subject`
* `msg.data`
* `msg.headers`

Typical examples:

* `msg.subject.startsWith("events.")`
* `msg.data.status == "active"`
* `has(msg.headers.Authorization)`

If the condition evaluates to `false`, the message is skipped.

### Security Options

The subscriber supports:

* username/password authentication from `credentialsSecretName`
* TLS from certificate files
* TLS from a Secret containing `tls.crt`, `tls.key`, and optional `ca.crt`
* trust-bundle verification via a ConfigMap containing `trust-bundle.pem`

Validation notes:

* `servers` must not be empty
* `subject` is required
* `path` and `data` must be valid Go templates
* `condition` must be a valid CEL boolean expression
* only one of `tls.fromSecret` or `tls.fromFiles` can be set
* JetStream pull-mode `batchSize` and `maxBytes` must be greater than zero when set

### Example Subscriber

/// tab | YAML

```yaml
--8<-- "docs/apps/nats-importer/subscriber.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/nats-importer/subscriber.yml"
EOF
```

///

## ClusterSubscriber

Use `ClusterSubscriber` when you want a centrally managed subscriber from the EDA base namespace.

Behavior differences from `Subscriber`:

* it is intended to run from the EDA base namespace
* the rendered path is written exactly as rendered, without namespace normalization
* this allows writing directly to fully qualified paths such as `.namespace{.name=="eda"}.events[...]`

### Example ClusterSubscriber

/// tab | YAML

```yaml
--8<-- "docs/apps/nats-importer/clustersubscriber.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/nats-importer/clustersubscriber.yml"
EOF
```

///

## Status

Both `Subscriber` and `ClusterSubscriber` report runtime status through:

* `status.connected`
* `status.lastSeenTime`
* `status.stream`
* `status.consumer`
* `status.ackPendingCount`
* `status.lastReconnectedTime`
* `status.error`

For JetStream subscribers, `stream`, `consumer`, and `ackPendingCount` help verify which stream and consumer are currently active.

## Known Limitations

The app does not currently raise a dedicated EDA alarm for NATS connectivity failures. Connection and processing issues are reflected through resource status fields instead.

Some repository examples use helper functions such as `toJson`, but the runtime template processor currently supports basic Go templates plus a small set of string and formatting helpers. The examples in this page are written to match the actual runtime behavior.
