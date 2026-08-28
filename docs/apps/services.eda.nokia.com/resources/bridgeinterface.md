---
resource_name: BridgeInterface
resource_name_plural: bridgeinterfaces
resource_name_plural_title: Bridge Interfaces
resource_name_acronym: BI
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_bridgeinterfaces.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Bridge Interface

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `BridgeInterface` combines a single [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) with a VLAN tag to create a sub-interface, which is then connected to a [`BridgeDomain`](./bridgedomain.md). This way, the host(s) that are connected to this sub-interface can communicate with other hosts in the [`BridgeDomain`](./bridgedomain.md).

/// note | BridgeInterface vs VLAN

The `BridgeInterface` connects a single [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) to the [`BridgeDomain`](./bridgedomain.md), while a [`VLAN`](./vlan.md) uses labels to select which [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-) are connected to the [`BridgeDomain`](./bridgedomain.md). The latter should be preferred wherever possible.
///

Traffic is switched via the [`BridgeDomain`](./bridgedomain.md) that matches the VLAN tag that the packets are tagged with, which allows a physical device to communicate with multiple services over the same physical interface.

A common use case is a server that hosts virtual machines: the physical device (hypervisor) hosts multiple VMs, all of which are assigned a unique VLAN ID to be able to connect to the network over the same physical interface.

![BridgeInterface graphical representation](../media/BridgeDomains-BridgeInterface.png)

## Uplinks

An uplink in the context of the `BridgeInterface` is a connection between a breakout switch and a service-aware switch. The breakout switch usually has fewer capabilities, both in terms of port speeds and control plane functionality.

These switches are typically not VxLAN or MPLS capable, and the distributed [`BridgeDomain`](./bridgedomain.md) can therefore not be extended onto the access switch. Instead, a separate non-distributed bridge domain service is created on the breakout switch which is attached to the distributed [`BridgeDomain`](./bridgedomain.md) through the uplink.

The `uplinkSelectors` label selector property is used to identify which links are connected to breakout switches. The VLAN that is used on this breakout uplink is determined by the `uplinkVLANID` or `uplinkVLANPool` property. 

/// note

On the breakout switch, only the interface selected by the `BridgeInterface` will be attached to the bridge domain service.
///

## Dependencies

### [`BridgeDomain`](./bridgedomain.md)

The `BridgeInterface` connects an [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) to a [`BridgeDomain`](./bridgedomain.md), allowing the hosts that are behind the [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) to communicate with other hosts in the [`BridgeDomain`](./bridgedomain.md).

The [`BridgeDomain`](./bridgedomain.md) must exist before the `BridgeInterface` can be configured.

### [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-)

A `BridgeInterface` is mapped to a single [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-), although the same [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) can be referenced by many `BridgeInterfaces`. A VLAN tag is used to determine which service the traffic will be forwarded to.

The [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) must exist before the `BridgeInterface` can be configured.

## Referenced resources

### `TopoLink`

If an uplink is configured which connects an [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) on a breakout switch to the distributed [`BridgeDomain`](./bridgedomain.md) service, the uplink label selector selects `TopoLink` resources that are used to connect the breakout switch to the rest of the network.

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
