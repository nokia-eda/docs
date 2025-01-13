# Kafka Exporter

| <nbsp> {: .hide-th } |                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------ |
| **Description**      | Kafka Exporter publishes network data to a Kafka broker.                                            |
| **Author**           | Nokia                                                                                                  |
| **Supported OS**     | SR Linux, SR OS                                                                                        |
| **Catalog**          | [nokia-eda/catalog][catalog]                                                                           |
| **Language**         | Go                                                                                                     |
| **Source Code**      | <small>coming soon</small>                                                                             |

[catalog]: https://github.com/nokia-eda/catalog

## Installation

The Kafka Exporter app can be installed using [EDA App Store](app-store.md) or by running the `app-install` workflow with `kubectl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/kafka-exporter/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/kafka-exporter/install.yml"
EOF
```

///

## Configuration

After installation, you can configure the Kafka Exporter using a `Producer` Custom Resource (CR).
The CR specifies the data to be exported, the Kafka broker settings and the messages delivery behavior.

### What to export

Define the data to be exported.

- **Export Paths**: `.spec.exports[].path`

    Specifies the paths in the state DB to export, e.g., `.namespace.node.srl.interface`

- **Fields**: `.spec.exports[].fields`

    Lists the fields to include in the exported data. If not specified, all fields under the path are included.

- **Where Query**: `.spec.exports[].where`

    A filter for the data, e.g., `oper-state = down`. Only matching data will be exported.

### Where are we exporting it

Specify the destination and security settings for the export

- **Broker Addresses**: `.spec.brokers`

    Comma-separated list of Kafka broker addresses to connect to, e.g., `broker1:9092,broker2:9092`.

- **Security Settings**:
    - **SASL**: `.spec.sasl`
        - `user`: Kafka username.
        - `password`: Kafka password.
        - `mechanism`: Authentication mechanisms such as `plain`, `scram-sha-256`,`scram-sha-512` or `oauthbearer`.
        - `token-url`: The token URL when `mechanism` is `oauthbearer`.

    - **TLS**: `.spec.tls`

        Certificate-based authentication for secure communication. Includes:

        - `cert-file`: Path to the client certificate file.
        - `key-file`: Path to the client private key file.
        - `ca-file`: Path to the certificate authority file.
        - `skip-verify`: whether the producer should verify the broker's certificate

### How are we doing all that?

Set how often or when data is exported and what kind of acknowledgment is required.

- **Message Delivery Mode**: 

    - `.spec.sync-producer`: Use synchronous messaging (`true`) or asynchronous messaging (`false`).
    - `.spec.flush-frequency`: Defines how long messages can sit in the producer's buffer before being batch sent to the broker.

- **Acknowledgment Level**: `.spec.required-acks`

    - `no-response`: No acknowledgment required.
    - `wait-for-local`: Acknowledged by the leader broker only.
    - `wait-for-all`: Acknowledged by all in-sync replicas.

- **Compression Codec**: `.spec.compression-codec`

    - Options: `none`, `gzip`, `snappy`, `zstd`, `lz4`.

- **Retry and Timeout**:

    - `.spec.max-retry`: Number of retries for failed message delivery (default: 3).
    - `.spec.timeout`: Timeout duration for producer operations (default: 10 seconds).

- **Export Frequency**: `.spec.exports[].period`

    - Interval for periodic exports (minimum: 10 seconds).

- **Export Triggers**: `.spec.exports[].mode`

    - `on-change`: Export data when it changes.
    - `periodic`: Export data at regular intervals.
    - `periodic-on-change`: Combine both periodic and change-based exports.

**Example**:

/// tab | YAML

```yaml
--8<-- "docs/apps/kafka-exporter/kafka_producer.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/kafka-exporter/kafka_producer.yml"
EOF
```

///
