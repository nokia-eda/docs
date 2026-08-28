---
resource_name: NetworksClientProviderInstance
resource_name_plural: networksclientproviderinstances
resource_name_plural_title: Network Client Provider Instances
resource_name_acronym: NCI
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_networksclientproviderinstances.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Network Client Provider Instance

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The Network Client Provider is an operator that continuously discovers hosts and devices attached to the network fabric. It reads endpoint information from managed SRL and SROS nodes — MAC tables, ARP and neighbor tables — and correlates that data with services topology to produce a unified inventory of connected endpoints.

Each record in the inventory includes the endpoint's MAC and IP address, the [`BridgeDomain`](./bridgedomain.md) or [`Router`](./router.md) through which it is reachable, and the node and interface where the endpoint is learned. Dual-homed or multi-homed endpoints appear as multiple records, one per node and subinterface attachment point.

The operator is opt-in: it does not run until a `NetworksClientProviderInstance` CR is created. Each instance monitors a single EDA namespace and spawns one operator pod. Discovered endpoints are written to the `networks` Client Table in that namespace.

/// note | Viewing discovered endpoints

Use the **Discovered Networks Endpoints** dashboard in the EDA UI to browse the client table populated by the Network Client Provider.

///

## Instance configuration

Each `NetworksClientProviderInstance` declares which EDA namespace the operator monitors through the `namespace` property. Create one instance per namespace that requires endpoint discovery. The operator pod reads node state and services topology only within that namespace.

The optional `confidenceLevelOffset` property adjusts the confidence level reported for IP addresses that are inferred from another provider's client-table entry rather than observed directly on the node. The base confidence for such cross-table borrow entries is 80%; the offset is added to this value and the result is clamped to the range `[0, 100]`.

## Operational status

The `status.operationalStatus` field reports the health of the operator instance:

- `Pending` — the provider has been created but has not yet completed its startup scan of existing client-table entries
- `Operational` — the provider has completed startup and is actively discovering endpoints
- `Error` — the provider encountered a fatal error; see `status.errorMessage` for details

## Discovery behavior

The Network Client Provider correlates layer-2 and layer-3 information from each managed node to build complete client records. Endpoints are indexed in the `networks` client table by MAC address, IP address, [`BridgeDomain`](./bridgedomain.md), and [`Router`](./router.md).

For endpoints learned on a [`BridgeDomain`](./bridgedomain.md), the provider correlates MAC table entries with proxy-ARP, proxy-ND, and IRB neighbor tables to resolve the IP address and associated [`Router`](./router.md). For endpoints reachable only through a [`Router`](./router.md) — for example on a [`RoutedInterface`](./routedinterface.md) — the provider uses the router-only path and leaves the `bridgeDomain` key empty.

Endpoints that have a known MAC address but no discoverable IP address are not written to the client table. The inventory is updated automatically when endpoints connect or disconnect from the fabric.

To discover IP addresses in a [`BridgeDomain`](./bridgedomain.md) the following spec attributes should be set:
```yaml
l2ProxyARPND:
  proxyARP: true          
  proxyND: true           
  dynamicLearning:
    enabled: true         
```
To discover IP addresses in a routed context, in the [`IRBInterface`](./irbinterface.md) the following spec attributes should be set:
```yaml
l3ProxyARPND:
  proxyARP: true
  proxyND: true
```

## Dependencies

The Network Client Provider has no required CR dependencies. However, endpoint discovery requires a deployed [`Fabric`](-{{ ref_app_doc('fabrics', 'fabric') }}-) with managed leaf and/or border-leaf nodes running SRL or SROS in the monitored namespace.

Services resources such as [`BridgeDomains`](./bridgedomain.md), [`Routers`](./router.md), [`VLANs`](./vlan.md), and [`RoutedInterfaces`](./routedinterface.md) must be deployed in the monitored namespace so the provider can enrich discovered endpoints with topology-canonical interface and VLAN names.

## Referenced resources

### EDA Namespace

The `namespace` property selects the EDA namespace whose fabric nodes and services topology the provider monitors.

## Examples

/// tab | YAML

```yaml
-{{ include_snippet(resource_name) }}-
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
-{{ include_snippet(resource_name) }}-
EOF
```

///

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
