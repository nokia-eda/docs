---
resource_name: Router
resource_name_plural: routers
resource_name_plural_title: Routers
resource_name_acronym: R
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_routers.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Router

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `Router` resource is a distributed service that maintains a routing table. Any traffic received by the `Router` service uses its routing table to determine the next-hop for that traffic. Synonyms for a `Router` service are "VPRN", "IP-VRF", or simply "VRF".

Although the `nodeSelectors` label selector property can be specified to determine where the `Router` service is deployed, this is optional: by default, the `Router` service will automatically be deployed wherever it is required.

Physical interfaces can be connected to the `Router` service through the following resources:

- [`RoutedInterfaces`](./routedinterface.md) connect a single `Interface` resource to the Router. 
- [`IRBInterfaces`](./irbinterface.md) connect an entire [`BridgeDomain`](./bridgedomain.md) to the Router.

Typically, a [`RoutedInterface`](./routedinterface.md) connects to a single host, and is configured with an IP that belongs to a point-to-point subnet with a `/30` or `/31` subnet mask. [`IRBInterfaces`](./irbinterface.md) on the other hand are typically configured with an anycast gateway IP address that is used as the next-hop for many hosts connected to a [`BridgeDomain`](./bridgedomain.md).

## Router types

A `Router` is a virtual network service, and can be local-only or distributed over multiple nodes. There are 4 types of `Routers`:

- `Simple`: creates a local-only `Router` service, where connectivity is enabled only between interfaces on the node where the service is configured.
- `EVPNVXLAN`: creates a distributed `Router` service, where connectivity between local and remotely attached interfaces is encapsulated in an **EVPN** service tunnel over a **VxLAN** transport tunnel.
- `EVPNMPLS`: creates a distributed `Router` service, where connectivity between local and remotely attached interfaces is encapsulated in an **EVPN** service tunnel over an **MPLS** transport tunnel.
- `IPVPN`: creates a distributed `Router` service, where connectivity between local and remotely attached interfaces is encapsulated in a **BGP-IPVPN** service tunnel over an **MPLS** transport tunnel.

### Service tunnel requirements

If the type of the `Router` is either `EVPNVXLAN` or `EVPNMPLS`, EVPN routes must be exchanged via the [underlay](-{{ ref_app_doc('routing', 'index.md') }}-#underlay-routing) for the establishment of the service tunnels.

If the type of the `Router` is `IPVPN`, BGP-IPVPN routes must be exchanged via the [underlay](-{{ ref_app_doc('routing', 'index.md') }}-#underlay-routing) for the establishment of the service tunnels.

### Transport tunnel requirements

If the type of the `Router` is `EVPNVXLAN`, IP reachability is required to all system IP addresses of the nodes that participate in the service (unless a [`RouterInterconnect`](./routerinterconnect.md) is used).

If the type of the `Router` is `EVPNMPLS` or `IPVPN`, label-switched transport tunnels must be established between all nodes that participate in the service (unless a [`RouterInterconnect`](./routerinterconnect.md) is used).

## EVIs and VNIs

An Ethernet Virtual Instance or EVI is an EVPN concept, while a VXLAN Network Identifier (VNI) is a VxLAN concept. A thorough explanation of both protocols and related concepts is beyond the scope of this article, but it is worth talking about the assignment of these identifiers. 

Both are integer numbers and are globally significant, meaning that all nodes must use the same values for the same service. To avoid accidentally assigning the same identifier to two different services, it is recommended to use the `eviPool` and `encapOptions.vxlan.vniPool` properties to let EDA take care of ensuring global uniqueness.

/// note

    Technically, the VNIs are only significant within an EVPN domain, and may be reused in different EVPN domains. However, due to the large number of VNIs available, it is recommended to use each VNI only once within your entire network. 
///

If the `Router` service is meant to inter-op with network elements that are not managed by EDA, consider using a static EVI (property `evi`) and VNI (property `encapOptions.vxlan.vni`) instead of a pool.

## Router ID

The BGP container must be configured if the `Router` service is used to exchange routes with external clients through a [`BGPPeer`](-{{ ref_app_doc('protocols', 'bgppeer') }}-) connected to a [`RoutedInterface`](./routedinterface.md) or [`IRBInterface`](./irbinterface.md).

A router ID must be configured before the BGP session can be established. This can either be explicitly configured for all nodes in the `Router`, or implicitly derived from the [`SystemInterface`](-{{ ref_app_doc('routing', 'systeminterface') }}-) of the node.

## Advanced options

/// note 

These options are hidden behind the "advanced" toggle in the UI.
///

### IP receive checks

Some operating systems discard all IPv4 packets that are received on an IPv6-only subinterface (that is, a subinterface with no configured IPv4 addresses). To enable IPv4 forwarding in this scenario, the `forwardingOptions.ipv4RxCheck` option should be disabled on the `Router`.

## Dependencies

### [`SystemInterface`](-{{ ref_app_doc('routing', 'systeminterface') }}-)

If the BGP container is enabled for the `Router` and the [`routerID`](#router-id) parameter is not configured, a [`SystemInterface`](-{{ ref_app_doc('routing', 'systeminterface') }}-) must be configured on every `TopoNode` that participates in the `Router` service and is actively or dynamically establishing BGP sessions through [`BGPPeer`](-{{ ref_app_doc('protocols', 'bgppeer') }}-) or [`BGPGroup`](-{{ ref_app_doc('protocols', 'bgpgroup') }}-) resources.

## Referenced resources

### `IndexAllocationPool`

The EVI and VNI numbers can be allocated by EDA from an index allocation pool, which ensures that every index is only used once. For more information, check the [EVIs and VNIs](#evis-and-vnis) section of this article.

### `TopoNode`

The nodes where this service is deployed can optionally be specified manually through the `nodeSelectors` property. If not set, the `Router` resource will be deployed wherever necessary.

### [`Policy`](-{{ ref_app_doc('routingpolicies', 'policy') }}-)

Routing policies can be specified to:

- determine which routes are leaked into or out of the default VRF
- determine which routes are imported from or exported to BGP peers and/or OSPF neighbors

### [`Keychain`](-{{ ref_app_doc('security', 'keychain') }}-)

When setting up BGP sessions from this `Router`, a [`Keychain`](-{{ ref_app_doc('security', 'keychain') }}-) may be used to secure these BGP sessions. This default setting may be overridden by the [`BGPGroup`](-{{ ref_app_doc('protocols', 'bgpgroup') }}-) and [`BGPPeer`](-{{ ref_app_doc('protocols', 'bgppeer') }}-).

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
