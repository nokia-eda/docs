---
resource_name: BridgeDomain
resource_name_plural: bridgedomains
resource_name_plural_title: Bridge Domains
resource_name_acronym: BD
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_bridgedomains.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Bridge Domain

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A bridge or broadcast domain is a collection of hosts that can talk to each other using switched (layer 2) packets, rather than routed (layer 3) packets. A `BridgeDomain` resource is the EDA abstraction of a broadcast domain: it provides connectivity between hosts connected to two or more (sub-)interfaces.

One or more hosts can be connected to a `BridgeDomain` service through a sub-interface, which is the combination of a physical interface and a VLAN tag. In EDA, there are two objects that create sub-interfaces:

- The [`BridgeInterface`](./bridgeinterface.md) resource combines one [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) with one VLAN tag and attaches it to a single `BridgeDomain`
- The [`VLAN`](./vlan.md) resource combines a set of [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) resources with one VLAN tag each, and attaches them to a single `BridgeDomain`

<figure markdown="1">
![BridgeDomain graphical representation](../media/BridgeDomains-BridgeDomain.png)
</figure>

To allow the hosts in a `BridgeDomain` to connect to other IP subnets (routed traffic), an [`IRBInterface`](./irbinterface.md) can connect the `BridgeDomain` to a [`Router`](./router.md). The hosts will use the gateway IP configured on the [`IRBInterface`](./irbinterface.md) as a next-hop for routed traffic. 

## BridgeDomain types

A `BridgeDomain` is a virtual network service, and can be local-only or distributed over multiple nodes. There are 3 types of `BridgeDomains`:

- `Simple`: creates a local-only `BridgeDomain` service, where connectivity is enabled only between physical interfaces on the node where the service is configured.
- `EVPNVXLAN`: creates a distributed `BridgeDomain` service, where connectivity between local and remotely attached interfaces is encapsulated in an **EVPN** service tunnel over a **VxLAN** transport tunnel.
- `EVPNMPLS`: creates a distributed `BridgeDomain` service, where connectivity between local and remotely attached interfaces is encapsulated in an **EVPN** service tunnel over an **MPLS** transport tunnel.

### Service tunnel requirements

If the type of the `BridgeDomain` is either `EVPNVXLAN` or `EVPNMPLS`, EVPN routes must be exchanged via the [underlay](-{{ ref_app_doc('routing', 'index.md') }}-#underlay-routing) for the establishment of the service tunnels.

### Transport tunnel requirements

If the type of the `BridgeDomain` is `EVPNVXLAN`, IP reachability is required to all system IP addresses of the nodes that participate in the service (unless a [`BridgeDomainInterconnect`](./bridgedomaininterconnect.md) is used).

If the type of the `BridgeDomain` is `EVPNMPLS`, label-switched transport tunnels must be established between all nodes that participate in the service (unless a [`BridgeDomainInterconnect`](./bridgedomaininterconnect.md) is used).

## EVIs and VNIs

An Ethernet Virtual Instance or EVI is an EVPN concept, while a VxLAN Network Identifier (VNI) is a VxLAN concept. A thorough explanation of both protocols and related concepts is beyond the scope of this article, but it is worth talking about the assignment of these identifiers. 

Both are integer numbers and are globally significant, meaning that all nodes must use the same values for the same service. To avoid accidentally assigning the same identifier to two different services, it is recommended to use the `eviPool` and `encapOptions.vxlan.vniPool` properties to let EDA take care of ensuring global uniqueness.

/// note

    Technically, the VNIs are only significant within an EVPN domain, and may be reused in different EVPN domains. However, due to the large number of VNIs available, it is recommended to use each VNI only once within your entire network. 
///

If the `BridgeDomain` service is meant to inter-op with (existing) network elements that are not managed by EDA, consider using a static EVI (property `evi`) and VNI (property `encapOptions.vxlan.vni`) instead of a pool.

## Dependencies

The `BridgeDomain` is a purely administrative object, and has no required dependencies. Note that without other resources (such as [`BridgeInterfaces`](./bridgeinterface.md) and [`VLANs`](./vlan.md)) connected to it, the service will not be deployed anywhere.

## Referenced resources

### `IndexAllocationPool`

The EVI and VNI numbers can be allocated by EDA from an index allocation pool, which ensures that every index is only used once. For more information, check the [EVIs and VNIs](#evis-and-vnis) section of this article.

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
