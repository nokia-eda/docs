# Verifying an install

We have provided a set of commands to verify the installation of EDA throughout the quickstart guide. This page provides a consolidated view of the verification steps.

## Verifying the EDA core

You should be able to use `kubectl get deploy` to verify that EDA deployments have started and in the Running mode:

```{.shell .no-select}
kubectl get deploy | awk 'NR==1 || /eda/'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
eda-api           1/1     1            1           10h
eda-appstore      1/1     1            1           10h
eda-asvr          1/1     1            1           10h
eda-bsvr          1/1     1            1           10h
eda-ce            1/1     1            1           10h
eda-cx            1/1     1            1           10h
eda-fe            1/1     1            1           10h
eda-fluentd       1/1     1            1           10h
eda-git           1/1     1            1           10h
eda-git-replica   1/1     1            1           10h
eda-kc            1/1     1            1           10h
eda-pg            1/1     1            1           10h
eda-sa            1/1     1            1           10h
eda-sc            1/1     1            1           10h
eda-sim-dut1-1    1/1     1            1           10h
eda-sim-dut2-1    1/1     1            1           10h
eda-sim-dut3-1    1/1     1            1           10h
eda-toolbox       1/1     1            1           10h
```
</div>

You can also check the `EngineConfig` to verify the ConfigEngine has started correctly, checking the `.status.run-status` field:

```{.shell .no-select}
kubectl get engineconfig engine-config -o jsonpath='{.status.run-status}{"\n"}'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
Started
```
</div>

`Started` is good, anything else is bad!

## Verifying node connectivity

The example topology deployed in the [previous step](onboarding-nodes.md#example-topology) resulted in creation of Nodes, with each Node represented by a simulator NOS. The Nodes in EDA are represented by the `TopoNode` resource, and this resource carries some status to indicate their health.

The easiest way to tell the current state of nodes is via the [UI](accessing-the-ui.md), or via `kubectl`:

/// tab | :octicons-check-circle-24: All nodes are healthy

```{.shell .no-select}
kubectl get toponodes
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME   PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE     AGE
dut1   7220 IXR-D3L   24.7.1    srl   true        normal   Connected   Synced   23h
dut2   7220 IXR-D3L   24.7.1    srl   true        normal   Connected   Synced   23h
dut3   7220 IXR-D5    24.7.1    srl   true        normal   Connected   Synced   23h
```
</div>
///
/// tab | :octicons-x-circle-24: Not all nodes are healthy
In this example the `dut1` and `dut3` nodes are not healthy, since the NPP components are not connected to the nodes and the nodes are not synced:
```{.shell .no-select}
kubectl get toponodes
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME   PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE     AGE
dut1   7220 IXR-D3L   24.7.1    srl   true        normal                        23h
dut2   7220 IXR-D3L   24.7.1    srl   true        normal   Connected   Synced   23h
dut3   7220 IXR-D5    24.7.1    srl   true        normal   Connected   Synced   23h
```
</div>
///

In particular the `NPP` and `NODE` columns define the state of the ConfigEngine to NPP connection, and the NPP to node connection. A node must be `Synced` or it will reject transactions.

It may also be useful to verify the Pod being launched to simulate the node is starting - this can take a while if it is your clusters first time starting a simulator of a given version. As well as the respective NPP Pod for the node:

/// tab | :octicons-check-circle-24: All pods running

```{.shell .no-select}
kubectl get pod | awk 'NR==1 || /eda-sim|npp/'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                               READY   STATUS    RESTARTS        AGE
eda-npp-dut1                       1/1     Running   0               3d20h
eda-npp-dut2                       1/1     Running   0               3d20h
eda-npp-dut3                       1/1     Running   0               3d20h
eda-sim-dut1-1-68f9c944b4-6hzgl    2/2     Running   0               3d20h
eda-sim-dut2-1-7bbf7d5b8-cn94f     2/2     Running   0               3d20h
eda-sim-dut3-1-5dcf8c99c9-m48r2    2/2     Running   0               3d20h
```
</div>
///
/// tab | :octicons-x-circle-24: Not all pods running

```{.shell .no-select}
kubectl get pod | awk 'NR==1 || /eda-sim|npp/'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                               READY   STATUS    RESTARTS      AGE
eda-npp-dut2                       1/1     Running   0             10h
eda-npp-dut3                       0/1     Pending   0             10h
eda-sim-dut1-1-78dbd5655-pkfgw     2/2     Running   0             10h
eda-sim-dut2-1-657c5579f-r7l4j     2/2     Running   0             10h
eda-sim-dut3-1-58ff56b9f5-dj6jx    2/2     Running   0             10h
```
</div>
///

Note the `eda-sim-*` Pods, one for each TopoNode in the topology. You should also note there are three NPPs, also one for each `TopoNode`.

## Verifying transactions

The ConfigEngine works off a sequential transaction log, processing transactions as they come in. "in" here is doing some heavy lifting, as items for processing may come in via:

* the UI.
* the API.
* the Kubernetes API.

For items coming in via the UI and API, a failed transaction does not impact future transactions. For Kubernetes this behavior is inverse - the ConfigEngine will always try to ingest the full set of changes available for processing, and so an object that can never transact can cause other items to fail. You can verify transactions in the system with:

```{.shell .no-select}
kubectl get transactionresults
```

<div class="embed-result highlight">
```{.bash .no-select .no-copy}
NAME                    RESULT   AGE    DRYRUN   DESCRIPTION
transaction-000000001   OK       151m            startup - final load
transaction-000000002   OK       129m            Installing core:{v0.1.0+24.4.0-a1 semver} (from eda-catalog-builtin-apps)
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
kubectl get transactionresults transaction-000000069 -o yaml
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
  - 'pod is not running or does not have an IP address ''dut3'': NPP pod ''eda-npp-dut3''
    did not spin up'
  - 'pod is not running or does not have an IP address ''dut1'': NPP pod ''eda-npp-dut1''
    did not spin up'
# -- snip --
```
</div>
