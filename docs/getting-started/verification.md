# Verifying an install

When using the [`make try-eda`](try-eda.md) command you will hopefully have a running EDA instance in under 10 minutes without any manual intervention. We embedded necessary checks in the Makefile to ensure that the steps are executed in the correct order and that the system is in a healthy state.

However, while testing the setup process on several different platforms, we couldn't cover all the possible cases. If you encounter installation issues, this section may help you pinpoint the issue.

## EDA core

You should be able to use `kubectl get pods` to verify that EDA core components have started and in the Ready state:

```{.shell .no-select}
kubectl get pods | awk 'NR==1 || /eda/'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                              READY   STATUS    RESTARTS   AGE
eda-api-b9ddf7784-pdc8w           1/1     Running   0          35h
eda-appstore-7b5cd7d767-kjjpg     1/1     Running   0          35h
eda-asvr-84d77c756b-cqsnt         1/1     Running   0          35h
eda-bsvr-574c497c57-smx9q         1/1     Running   0          35h
eda-ce-6c6589847-lm52x            1/1     Running   0          35h
eda-cx-8bb6cc546-fl9ff            1/1     Running   0          35h
eda-fe-84454cc45c-c9mvm           1/1     Running   0          35h
eda-fluentbit-5kvkz               1/1     Running   0          35h
eda-fluentd-678c7c6bb6-xg9d4      1/1     Running   0          35h
eda-git-546b7b86f8-79xf7          1/1     Running   0          35h
eda-git-replica-b998dfd5-26ss7    1/1     Running   0          35h
eda-keycloak-5886554ff9-2ffdl     1/1     Running   0          35h
eda-npp-dut1                      1/1     Running   0          14h
eda-npp-dut2                      1/1     Running   0          14h
eda-npp-dut3                      1/1     Running   0          14h
eda-postgres-676fb9994-2vmps      1/1     Running   0          35h
eda-sa-8d9b8b7b-pd46s             1/1     Running   0          35h
eda-sc-85b9987c68-27bh8           1/1     Running   0          35h
eda-se-1                          1/1     Running   0          35h
eda-sim-dut1-1-5bc5797b99-zndgm   2/2     Running   0          14h
eda-sim-dut2-1-5f77844fcc-5z7kh   2/2     Running   0          14h
eda-sim-dut3-1-75786fc95-9xw6f    2/2     Running   0          14h
eda-toolbox-754bcd8564-fcq96      1/1     Running   0          35h
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

## Node connectivity

The example topology deployed as part of the [quickstart](virtual-network.md) resulted in creation of topology nodes, with each node represented by an SR Linux simulator. The topology nodes in EDA are represented by the `TopoNode` resource, and this resource has a status field to indicate its health.

The easiest way to tell the current state of nodes is via the [UI](try-eda.md#web-ui), or via `kubectl`:

/// tab | :octicons-check-circle-24: All nodes are healthy

```{.shell .no-select}
kubectl get toponodes
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME   PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE     AGE
dut1   7220 IXR-D3L   24.7.1    srl   true        normal   Connected   Synced   14h
dut2   7220 IXR-D3L   24.7.1    srl   true        normal   Connected   Synced   14h
dut3   7220 IXR-D5    24.7.1    srl   true        normal   Connected   Synced   14h
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

## Transactions

The EDA's brain - Config Engine - works off a sequential transaction log, processing transactions as they come in. "in" here is doing some heavy lifting, as items for processing may come in via:

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

The transaction details will give you a hint as to what went wrong. In the example above NPP Pod for `dut1` and `dut3` did not start, and so the transaction to push the configs failed.

## UI access

As covered in the [Configure your deployment](installation-process.md#configure-your-deployment) section, the EDA service requires a user to provide the desired DNS name/IP and port for external access. These parameters become the part of the Engine Config resource that, as the name suggests, configures the central part of EDA - the Config Engine.

The values you provided in the pref.mk file or in the CLI can be found in the Engine Config resource:

```{.shell .no-select}
kubectl get engineconfig engine-config -o jsonpath='{.spec.cluster.external}' \
| yq -p json #(1)!
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
