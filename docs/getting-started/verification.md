# Verifying an install

When using the [`make try-eda`](try-eda.md) command you will hopefully have a running EDA instance in under 10 minutes without any manual intervention. We embedded necessary checks in the Makefile to ensure that the steps are executed in the correct order and that the system is in a healthy state.

However, while testing the setup process on several different platforms, we couldn't cover all the possible cases. If you encounter installation issues, this section may help you pinpoint the issue.

## EDA core

You should be able to use `kubectl -n eda-system get pods` to verify that EDA core components have started and in the Ready state:

```{.shell .no-select}
kubectl -n eda-system get pods | awk 'NR==1 || /eda/'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                                  READY   STATUS    RESTARTS   AGE
cx-eda--leaf1-sim-864b97d58d-g9zq2    2/2     Running   0          12h
cx-eda--leaf2-sim-6698fc668f-4blcm    2/2     Running   0          12h
cx-eda--spine1-sim-677f5499cf-fn2pg   2/2     Running   0          12h
eda-api-9985cb78-gphnk                1/1     Running   0          12h
eda-appstore-8d679c5b-fqmt6           1/1     Running   0          12h
eda-asvr-dc9877c8d-5j62k              1/1     Running   0          12h
eda-bsvr-6bf77b64c-9l2zx              1/1     Running   0          12h
eda-ce-84c6486cb7-f8jzc               1/1     Running   0          12h
eda-cx-5dc6cf9d96-dcrrf               1/1     Running   0          12h
eda-fe-54d8db877f-xk7l8               1/1     Running   0          12h
eda-fluentbit-hkwvd                   1/1     Running   0          12h
eda-fluentd-54cf4bd5d7-j98zg          1/1     Running   0          12h
eda-git-754df68df5-8kgx4              1/1     Running   0          12h
eda-git-replica-784dbdbfc8-5zdzz      1/1     Running   0          12h
eda-keycloak-5d569565b7-2gmc7         1/1     Running   0          12h
eda-metrics-server-799d54cb7-688nz    1/1     Running   0          12h
eda-npp-eda-leaf1                     1/1     Running   0          12h
eda-npp-eda-leaf2                     1/1     Running   0          12h
eda-npp-eda-spine1                    1/1     Running   0          12h
eda-postgres-cd89bfc57-q56cc          1/1     Running   0          12h
eda-sa-576c98865f-66vq9               1/1     Running   0          12h
eda-sc-84546648c5-djr49               1/1     Running   0          12h
eda-se-1                              1/1     Running   0          12h
eda-toolbox-84c95bd8c6-lqxh7          1/1     Running   0          12h
```
</div>

You can also check the `EngineConfig` to verify the ConfigEngine has started correctly, checking the `.status.run-status` field:

```{.shell .no-select}
kubectl -n eda-system get engineconfig engine-config \
-o jsonpath='{.status.run-status}{"\n"}'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
Started
```
</div>

`Started` is good, anything else is bad!

## Node connectivity

The example topology deployed as part of the [quickstart](virtual-network.md) resulted in creation of topology nodes, with each node represented by an SR Linux simulator. The topology nodes in EDA are represented by the `TopoNode` resource, and this resource has a status field to indicate its health.

The easiest way to tell the current state of nodes is via the [UI](try-eda.md#web-ui), or via `kubectl`:

/// tab | :octicons-check-circle-24: All nodes are healthy

```{.shell .no-select}
kubectl -n eda get toponodes #(1)!
```

1. `TopoNode` resources are scoped in the `eda` namespace, hence the `-n eda` flag.

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME     PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE     AGE
leaf1    7220 IXR-D3L   24.10.1   srl   true        normal   Connected   Synced   12h
leaf2    7220 IXR-D3L   24.10.1   srl   true        normal   Connected   Synced   12h
spine1   7220 IXR-D5    24.10.1   srl   true        normal   Connected   Synced   12h
```
</div>
///
/// tab | :octicons-x-circle-24: Not all nodes are healthy
In this example the `leaf1` and `spine1` nodes are not healthy, since the NPP components are not connected to the nodes and the nodes are not synced:
```{.shell .no-select}
kubectl get toponodes
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME     PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE     AGE
leaf1    7220 IXR-D3L   24.7.1    srl   true        normal                        23h
leaf2    7220 IXR-D3L   24.7.1    srl   true        normal   Connected   Synced   23h
spine1   7220 IXR-D5    24.7.1    srl   true        normal   Connected   Synced   23h
```
</div>
///

In particular, the `NPP` and `NODE` columns define the state of the ConfigEngine to NPP connection, and the NPP to node connection. A node must be `Synced` or it will reject transactions.

It is useful to verify the underlying Pod resources for the network simulator nodes have been created - this can take a while if it is your first time starting a simulator of a given version. You should see all your sims and the associated NPP (Node Push Pull) pods running:

/// tab | :octicons-check-circle-24: All pods running

```{.shell .no-select}
kubectl -n eda-system get pod | awk 'NR==1 || /cx-eda|npp/'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                                  READY   STATUS    RESTARTS   AGE
cx-eda--leaf1-sim-864b97d58d-g9zq2    2/2     Running   0          14h
cx-eda--leaf2-sim-6698fc668f-4blcm    2/2     Running   0          14h
cx-eda--spine1-sim-677f5499cf-fn2pg   2/2     Running   0          14h
eda-npp-eda-leaf1                     1/1     Running   0          14h
eda-npp-eda-leaf2                     1/1     Running   0          14h
eda-npp-eda-spine1                    1/1     Running   0          14h
```
</div>
///
/// tab | :octicons-x-circle-24: Not all pods running

```{.shell .no-select}
kubectl -n eda-system get pod | awk 'NR==1 || /cx-eda|npp/'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                                 READY   STATUS    RESTARTS      AGE
cx-eda--leaf1-sim-864b97d58d-g9zq2    2/2     Running   0          14h
cx-eda--leaf2-sim-6698fc668f-4blcm    2/2     Running   0          14h
cx-eda--spine1-sim-677f5499cf-fn2pg   2/2     Running   0          14h
eda-npp-eda-leaf1                     1/1     Running   0          14h
```
</div>
///

Note the `cx-eda-*` Pods (one for each `TopoNode` in the topology), these pods are SR Linux container images. You should also note there are three NPP Pods (also one for each `TopoNode`) each designated to a corresponding `TopoNode`.

## Transactions

The EDA's brain - Config Engine - works off a sequential transaction log, processing transactions as they come in. "in" here is doing some heavy lifting, as items for processing may come in via:

* the UI.
* the API.
* the Kubernetes API.

For items coming in via the UI and API, a failed transaction does not impact future transactions. For Kubernetes this behavior is inverse - the ConfigEngine will always try to ingest the full set of changes available for processing, and so an object that can never transact can cause other items to fail. You can verify transactions in the system with:

```{.shell .no-select}
kubectl -n eda-system get transactionresults
```

<div class="embed-result highlight">
```{.bash .no-select .no-copy}
NAME                    RESULT   AGE    DRYRUN   DESCRIPTION
transaction-000000001   OK       151m            startup - no core manifest
transaction-000000002   OK       129m            Installing core:{v1.0.0+24.8.1-rc semver} (from eda-catalog-builtin-apps)
-- snip --
transaction-000000013   OK       10m
transaction-000000014   OK       10m
-- snip --
transaction-000000069   Failed   2m
```
</div>

If you see any transactions with a result of `Failed`, these should be investigated - especially if they came in via the Kubernetes interface. Like in the example the last transaction has a `Failed` result.

You can investigate the transaction further with:

```{.shell .no-select}
kubectl -n eda-system get transactionresults transaction-000000069 -o yaml
```

<div class="embed-result highlight">
```{.yaml .no-select .no-copy}
apiVersion: core.eda.nokia.com/v1
kind: TransactionResult
metadata:
  creationTimestamp: "2024-04-29T22:17:40Z"
  generation: 3
  name: transaction-000000069
  namespace: default
  resourceVersion: "600591"
  uid: fc0ce238-dfed-44a5-badd-7b3a56f14706
spec:
  execution-summary: 'input-crs: 2, intents-run: 12, nodes-changed: 0, engine-time=725.396191ms,
    push-to-node=10m0.052663836s'
  general-errors:
  - 'pod is not running or does not have an IP address ''spine1'': NPP pod ''eda-npp-spine1''
    did not spin up'
  - 'pod is not running or does not have an IP address ''leaf1'': NPP pod ''eda-npp-leaf1''
    did not spin up'
# -- snip --
```
</div>

The transaction details will give you a hint as to what went wrong. In the example above NPP Pod for `leaf1` and `spine1` did not start, and so the transaction to push the configs failed.

## UI access

As covered in the [Configure your deployment](installation-process.md#configure-your-deployment) section, the EDA service requires a user to provide the desired DNS name/IP and port for external access. These parameters become the part of the Engine Config resource that, as the name suggests, configures the central part of EDA - the Config Engine.

The values you provided in the prefs.mk file or in the CLI can be found in the Engine Config resource:

```{.shell .no-select}
kubectl -n eda-system get engineconfig engine-config \
-o jsonpath='{.spec.cluster.external}' | yq -p json #(1)!
```

1. The `yq` CLI tool is installed in the `./tools` directory of the playground repo.

<div class="embed-result highlight">
```{.console .no-select .no-copy}
domainName: vm.home.lab
httpPort: 9200
httpsPort: 9443
ipv4Address: 10.1.0.11
ipv6Address: fd7a:115c:a1e0::be01:ff2f
```
</div>

The configuration above means that the EDA UI client (a browser) should use `https://vm.home.lab:9443` to access the EDA UI. You can change the `engine-config` resource post-install and change the `domainName` and/or port numbers, the changes will be in effect immediately without requiring a redeploy of the EDA.

--8<-- "docs/getting-started/try-eda.md:ext-name-note-1"

/// admonition | Secure-by-design
    type: subtle-note
In the secure-by-design paradigm, EDA exposes APIs and UI for its users only over the secure transport. That makes HTTPS the only supported transport for UI access.

EDA UI is exposed in the k8s cluster via the `eda-api` service
///
