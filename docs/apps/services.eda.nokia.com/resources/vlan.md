---
resource_name: VLAN
resource_name_plural: vlans
resource_name_plural_title: VLANs
resource_name_acronym: V
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_vlans.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# VLAN

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `VLAN` combines a set of [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-) with a VLAN tag to create sub-interfaces, which are then connected to a [`BridgeDomain`](./bridgedomain.md). This way, the hosts that are connected to these sub-interfaces can communicate amongst themselves and with other hosts in the [`BridgeDomain`](./bridgedomain.md).

/// note | VLAN vs BridgeInterface

A `VLAN` uses labels to select which [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-) are connected to the [`BridgeDomain`](./bridgedomain.md), while a [`BridgeInterface`](./bridgeinterface.md) connects a single [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) to the [`BridgeDomain`](./bridgedomain.md). The former should be preferred wherever possible.
///

Traffic is switched via the [`BridgeDomain`](./bridgedomain.md) that matches the VLAN tag that the packets are tagged with, which allows a physical device to communicate with multiple services over the same physical interface.

A common use case is a server that hosts virtual machines: the physical device (hypervisor) hosts multiple VMs, all of which are assigned a unique VLAN ID to be able to connect to the network over the same physical interface.

![VLAN graphical representation](../media/BridgeDomains-VLAN.png)

## Split-horizon groups

Split-horizon groups are used for loop avoidance, grouping all interfaces selected by this `VLAN`. BUM traffic received through one of these [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-) is not forwarded to any other VLAN sub-interface **local to that physical switch**. Note that sub-interfaces on a different switch may still receive the packets.

Split-horizon groups are typically used in scenarios where a set of interfaces may be inter-connected through a backdoor link, and in certain multihomed scenarios.

/// note | Split-horizon groups for multi-homing

Rather than creating a split-horizon group for interfaces that are used for all-active multi-homing, prefer using an EVPN Ethernet Segment wherever possible. Dedicated loop-avoidance features are built into the EVPN protocol that are superior to split-horizon groups. 

Ethernet segments also provide loop avoidance when the links are connected to different physical switches, which is not possible with split-horizon groups.
///

## Uplinks

An uplink in the context of the `VLAN` is a connection between a breakout switch and a service-aware switch. The breakout switch usually has fewer capabilities, both in terms of port speeds as well as control plane functionality.

These switches are typically not VxLAN or MPLS capable, and the distributed [`BridgeDomain`](./bridgedomain.md) can therefore not be extended onto the access switch. Instead, a separate non-distributed bridge domain service is created on the breakout switch which is attached to the distributed [`BridgeDomain`](./bridgedomain.md) through the uplink.

The `uplinkSelectors` label selector property is used to identify which links are connected to breakout switches. The VLAN that is used on this breakout uplink is determined by the `uplinkVLANID` or `uplinkVLANPool` property. 

/// note

On the breakout switch, only the interfaces selected by the `VLAN` will be attached to the bridge domain service.
///

## Dependencies

### [`BridgeDomain`](./bridgedomain.md)

The `VLAN` connects a set of [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-) to a [`BridgeDomain`](./bridgedomain.md), allowing the hosts that are behind the [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-) to communicate with each other and to other hosts in the [`BridgeDomain`](./bridgedomain.md).

The [`BridgeDomain`](./bridgedomain.md) must exist before the `VLAN` can be configured.

## Referenced resources

### [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-)

A `VLAN` is mapped to multiple [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-), and those [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-) can be referenced by many `VLANs`. A VLAN tag is used to determine which service the traffic will be forwarded to.

Although the label selector that selects [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) resources for this `VLAN` must be specified, there is no requirement that the label is actually applied to any [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-). If the `VLAN` selects no [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-), it will not be deployed.

### `TopoLink`

If an uplink is configured which connects a set of [`Interfaces`](-{{ ref_app_doc('interfaces', 'interface') }}-) on one or more breakout switches to the distributed [`BridgeDomain`](./bridgedomain.md) service, the uplink label selector selects `TopoLink` resources that are used to connect the breakout switch(es) to the rest of the network.

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
