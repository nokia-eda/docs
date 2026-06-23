# PagerDuty

| <nbsp> {: .hide-th } |                                                                                              |
| -------------------- | -------------------------------------------------------------------------------------------- |
| **Description**      | PagerDuty creates incidents from EDA alarms and query results.                               |
| **Author**           | Nokia                                                                                        |
| **Supported OS**     | N/A                                                                                          |
| **Catalog**          | [nokia-eda/catalog][catalog]                                                                 |
| **Language**         | Go                                                                                           |

[catalog]: https://github.com/nokia-eda/catalog

## Overview

The PagerDuty app connects EDA to PagerDuty and creates or resolves PagerDuty incidents from EDA alarms and query results.

The app exposes two resources:

* `Pager`: namespace-scoped incident generator created in a user namespace such as `eda`.
* `ClusterPager`: cluster-scoped incident generator created in the EDA base namespace.

Each `Pager` or `ClusterPager` references a Kubernetes `Secret` that contains the PagerDuty service integration routing key under `data.key`.

## Installation

Before installing the app, create a secret containing the PagerDuty REST API key in the EDA base namespace. The controller uses this key when communicating with PagerDuty.

/// tab | YAML

```yaml
--8<-- "docs/apps/pager-duty/api-key-secret.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/pager-duty/api-key-secret.yaml"
EOF
```

///

Install the app from [EDA Store](../apps/index.md#nokia-eda-store) or by running an `AppInstaller` workflow with `kubectl` or `edactl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/pager-duty/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/pager-duty/install.yml"
EOF
```

///

### Install Settings

The app exposes the following install-time settings:

* `pdApiKeySecretName`: name of the secret containing the PagerDuty REST API key.
* `proxyConfigMapName`: ConfigMap name used for `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`.
* `pdConfigMapName`: ConfigMap name used for runtime tuning.
* `pdCPULimit`: CPU limit for the controller pod.
* `pdMemoryLimit`: memory limit for the controller pod.

These settings control the deployment in the EDA base namespace and can be provided through `spec.apps[].appSettings` in the `AppInstaller` workflow or directly in the EDA UI.

If you provide the ConfigMap named by `pdConfigMapName`, the controller can tune rate limiting and logging with these keys:

* `PD_APIKEY_REQ_PER_MIN`
* `PD_APIKEY_BURST_REQUESTS`
* `PD_RKEY_REQ_PER_MIN`
* `PD_RKEY_BURST_REQUESTS`
* `PD_RKEY_BUFFER_SIZE`
* `PD_RKEY_ENQ_TIMEOUT`
* `PD_LOG_STATS`
* `PD_LOG_STATS_INTERVAL`
* `LOG_LEVEL`
* `ENABLE_WEBHOOKS`

## Getting Started

The setup has two steps:

1. Store the PagerDuty service integration routing key in a Kubernetes `Secret`.
2. Create a `Pager` or `ClusterPager` that references the routing key secret and defines an alarm or query source.

If the secret reference is just a name, the app looks for it in the same namespace as the `Pager` or `ClusterPager` resource. You can also use `namespace/name` to reference a secret in another namespace.

/// admonition | Namespace behavior
    type: subtle-note

    `Pager` resources must be created outside the EDA base namespace. `ClusterPager` resources must be created in the EDA base namespace.
///

### PagerDuty Routing Key Secret

Each resource references a Kubernetes secret through `spec.routingKeySecret`.

The secret must contain this key:

* `key`

For a namespace-scoped `Pager`, create the secret in the same namespace as the `Pager`, or use `namespace/name` in `routingKeySecret`. For `ClusterPager`, create the secret in the EDA base namespace, or use an explicit `namespace/name` reference.

Example routing key secret in namespace `eda`:

/// tab | YAML

```yaml
--8<-- "docs/apps/pager-duty/routing-key-secret.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/pager-duty/routing-key-secret.yaml"
EOF
```

///

## Alarm Sources

Use `sources.alarms` to create PagerDuty events for matching EDA alarms.

Notable specification fields:

* `sources.alarms.include`: alarm types that create PagerDuty events.
* `sources.alarms.exclude`: alarm types to ignore.
* `sources.alarms.autoResolve`: sends a PagerDuty `resolve` event when the alarm clears.
* `sources.alarms.namespaces`: limits which namespaces are watched by a `ClusterPager`.

Payload behavior:

* `summary`: `<namespace> - <alarm type> - <resource>`
* `source`: `EDA-ALARMS`
* `component`: `<namespace>/<resource>`
* `group`: alarm `kind`
* `severity`: mapped from the EDA alarm severity. `major` and `minor` are sent as `error`.

Example `ClusterPager` watching interface alarms:

/// tab | YAML

```yaml title="Example ClusterPager alarm resource"
--8<-- "docs/apps/pager-duty/clusterpager-alarms.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/pager-duty/clusterpager-alarms.yml"
EOF
```

///

## Query Sources

Use `sources.query` to subscribe to an EDA table and generate a PagerDuty event whenever a matching object appears or changes.

Notable specification fields:

* `sources.query.table`: the EDA table to watch.
* `sources.query.where`: filter applied to the subscription.
* `sources.query.fields`: optional list of fields to fetch. If omitted, all fields of the subscribed table are used.
* `sources.query.autoResolve`: resolves the PagerDuty incident when the matching object disappears.
* `sources.query.includeDetails`: copies the returned query data into PagerDuty `custom_details`.
* `sources.query.summary`, `sources.query.source`, and `sources.query.severity`: required templates.
* `sources.query.component`, `sources.query.group`, and `sources.query.class`: optional templates.

### Query Templates

Use Go templates to build the PagerDuty payload. Because many keys contain dots, `index` is usually the easiest way to reference them, for example `{{ index . "node.name" }}`.

The `severity` template must render to one of `critical`, `error`, `warning`, or `info`.

For a namespace-scoped `Pager`, the controller automatically rewrites `.namespace...` paths so the subscription stays inside the Pager's namespace.

Example `Pager` that raises an incident when an interface goes down:

/// tab | YAML

```yaml title="Example Pager query resource"
--8<-- "docs/apps/pager-duty/pager-interface-down.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/pager-duty/pager-interface-down.yml"
EOF
```

///

## Cluster-Scoped Resources

Use `ClusterPager` from the EDA base namespace when you want centralized paging across namespaces.

The fields are the same as the namespace-scoped `Pager`, but:

* `ClusterPager` must exist in the EDA base namespace.
* Alarm sources can watch selected namespaces through `sources.alarms.namespaces`.
* Query subscriptions are not namespace-rewritten, so they can watch cross-namespace data with fully qualified `.namespace` paths.

## Validation Notes

When creating resources, follow these rules:

* You must configure at least one source: `alarms` or `query`.
* Alarm sources must define at least one of `include` or `exclude`.
* Query sources must define `table`, `summary`, `source`, and `severity`.
* Query severity templates must render to one of `critical`, `error`, `warning`, or `info`.
* Query templates are validated when the resource is created or updated.
