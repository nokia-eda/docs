---
resource_name: VirtualNetwork
resource_name_plural: virtualnetworks
resource_name_plural_title: Virtual Networks
resource_name_acronym: VN
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_virtualnetworks.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Virtual Network

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A virtual network is a collection of network connectivity services like [`BridgeDomains`](./bridgedomain.md) and [`Routers`](./router.md). It doesn't bring any new functionality, but rather serves as a logical grouping of connectivity services that belong together, for example to the same customer or to the same application.

Some examples:

- Virtual network 'my-app' contains a [`Router`](./router.md) and two [`BridgeDomain`](./bridgedomain.md) services with accompanying [`IRBInterfaces`](./irbinterface.md) and [`VLANs`](./vlan.md)
- Virtual network 'internet-services' contains a [`Router`](./router.md) connected to the internet via a [`BGPPeer`](-{{ ref_app_doc('protocols', 'bgppeer') }}-), and [`BridgeDomain`](./bridgedomain.md) services that are allowed to access the internet

The connectivity services that the `VirtualNetwork` manages are still visible in the user interface, as derived resources. To modify them, the operator should modify the `VirtualNetwork` those services belong to instead. 

Refer to the [referenced resources](#referenced-resources) for a list of EDA resources that can be created and managed by the `VirtualNetwork`. Any dependencies of those resources are detailed in their respective documentation articles.

## Dependencies

The `VirtualNetwork` serves as a top-level abstraction for connectivity services, just like the [`Fabric`](-{{ ref_app_doc('fabrics', 'fabric') }}-) is a top-level abstraction of the physical layout of a datacenter and the required elements to support virtualized connectivity services. Therefore, the `VirtualNetwork` has no dependencies.

## Referenced resources

### [`BridgeDomain`](./bridgedomain.md)

Bridge domains are virtual services that provide layer-2 connectivity between hosts in the same subnet. These virtual broadcast domains may be local to a specific node, or distributed with EVPN.

### [`BridgeInterface`](./bridgeinterface.md)

To connect an [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) to a [`BridgeDomain`](./bridgedomain.md), a [`BridgeInterface`](./bridgeinterface.md) or [`VLAN`](./vlan.md) resource must be created.

### [`Router`](./router.md)

[`Routers`](./router.md) are virtual services that provide layer-3 connectivity between hosts and [`BridgeDomain`](./bridgedomain.md) services. The routing table of a [`Router`](./router.md) service may be local to a specific node, or distributed with EVPN.

### [`RoutedInterface`](./routedinterface.md)

To connect an [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) to a [`Router`](./router.md), a [`RoutedInterface`](./routedinterface.md) resource must be created. Typically this [`RoutedInterface`](./routedinterface.md) is configured with an IP address in a point-to-point (`/31` or `/30`) subnet.

### [`IRBInterface`](./irbinterface.md)

To connect a [`BridgeDomain`](./bridgedomain.md) to a [`Router`](./router.md), an [`IRBInterface`](./irbinterface.md) resource must be created. Typically this [`IRBInterface`](./irbinterface.md) is configured with a gateway IP address, often the first host in a large (e.g. `/24`) subnet.

### [`StaticRoute`](-{{ ref_app_doc('protocols', 'staticroute') }}-)

To configure reachability information for a particular subnet towards an external next-hop, a [`StaticRoute`](-{{ ref_app_doc('protocols', 'staticroute') }}-) resource may be created.

### BGP

To exchange reachability information between the virtual [`Router`](./router.md) service and an external endpoint (e.g. a firewall or datacenter gateway) using the BGP protocol, the `VirtualNetwork` allows for the creation of the following resources:

- [`BGPGroups`](-{{ ref_app_doc('protocols', 'bgpgroup') }}-)
- [`BGPPeers`](-{{ ref_app_doc('protocols', 'bgppeer') }}-)

### OSPF

To exchange reachability information between the virtual [`Router`](./router.md) service and an external endpoint (e.g. a firewall or datacenter gateway) using the OSPF protocol, the `VirtualNetwork` allows for the creation of the following resources: 

- [`OSPFAreas`](-{{ ref_app_doc('protocols', 'ospfarea') }}-)
- [`OSPFInstances`](-{{ ref_app_doc('protocols', 'ospfinstance') }}-)
- [`OSPFInterface`](-{{ ref_app_doc('protocols', 'ospfinterface') }}-)

### IS-IS

To exchange reachability information between the virtual [`Router`](./router.md) service and an external endpoint using the IS-IS protocol, the `VirtualNetwork` allows for the creation of the following resources: 

- [`ISISInstance`](-{{ ref_app_doc('protocols', 'isisinstance') }}-)
- [`ISISInterface`](-{{ ref_app_doc('protocols', 'isisinterface') }}-)

### Routing policies

To control which reachability information is imported into / exported out of the virtualized [`Router`](./router.md) services, [`Policy`](-{{ ref_app_doc('routingpolicies', 'policy') }}-) resources may be configured that can be referenced by the [BGP](#bgp), [OSPF](#ospf), or [IS-IS](#is-is) resources.

Routing [policies](-{{ ref_app_doc('routingpolicies', 'policy') }}-) can filter routes based on many criteria, including pre-defined [`PrefixSets`](-{{ ref_app_doc('routingpolicies', 'prefixset') }}-) containing lists of subnets that need to be accepted or rejected.

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
