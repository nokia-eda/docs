---
resource_name: RouterInterconnect
resource_name_plural: routerinterconnects
resource_name_plural_title: Router Interconnects
resource_name_acronym: RI
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_routerinterconnects.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Router Interconnect

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Virtualized services like [`BridgeDomains`](./bridgedomain.md) for layer-2 connectivity and [`Routers`](./router.md) for layer-3 connectivity can be distributed using EVPN, allowing hosts connected to different (sets of) network switches to communicate with each other as if they were in the same location.

For scaling reasons, it may be required to divide the network into multiple EVPN domains, which are "stitched" together at the edges, via a datacenter interconnect domain. That's where the [`RouterInterconnect`](./routerinterconnect.md) resource comes in, which makes the [`Router`](./router.md) available to multiple EVPN domains.

These domains may even use different transport tunnel protocols: for example, VxLAN in the first datacenter, MPLS in the WAN, and then VxLAN again in the second datacenter.

/// admonition
    type: note

The `RouterInterconnect` is connected to a single [`Router`](./router.md) resource. Multiple [`Routers`](./router.md) cannot be stitched together with the `RouterInterconnect` resource.
///

<figure markdown="1">
![Router interconnect diagram](../media/services-RouterInterconnect.png)
</figure>

## VxLAN to VxLAN stitching

When stitching an EVPN VxLAN domain to another - different - EVPN VxLAN domain, it is important that the interconnect [`Router`](./router.md) uses a different VNI than the service that is being stretched over multiple datacenters, as choosing the same VNI could potentially lead to routing loops.

## VxLAN to MPLS stitching

Service traffic transported over VxLAN tunnels is encapsulated in an IP packet, which makes IP connectivity between the service endpoints the only requirement (alongside the ability to encapsulate and decapsulate the packets). 

For MPLS transport tunnels, labels need to be exchanged between service endpoints (and all switches in between) as packets are label-switched instead of IP-routed. Check out the [MPLS app](-{{ ref_app_doc('mpls', 'index.md') }}-) for more details.

## Dependencies

### `TopoNode`

To identify which nodes in the network will serve as stitching points (usually the datacenter gateways), the `RouterInterconnect` resource must select a set of nodes. 

Nodes can be selected explicitly via the `nodes` property, or through label assignment via the `nodeSelectors` property.

### [`Router`](./router.md)

The `RouterInterconnect` resource allows a [`Router`](./router.md) to be distributed across multiple EVPN domains. The [`Router`](./router.md) resource must exist before the `RouterInterconnect` resource can be created.

## Referenced resources

### [`Policy`](-{{ ref_app_doc('routingpolicies', 'policy') }}-)

As an alternative to import and export route targets, dedicated routing policies may be used to determine which routes are exchanged to and from the datacenter interconnect domain. 

### `IndexAllocationPool`

On some operating systems, the VxLAN tunnel interface is configured as a subinterface of a VxLAN interface. This subinterface requires an ID that is unique on the node (locally significant only). 

If the interconnect BGP instance is using VxLAN transport tunnels, the `vxlan.tunnelIndexPool` property must be specified. 

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
