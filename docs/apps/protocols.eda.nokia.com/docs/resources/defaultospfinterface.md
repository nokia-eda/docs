---
resource_name: DefaultOSPFInterface
resource_name_plural: defaultospfinterfaces
resource_name_plural_title: Default OSPF Interfaces
resource_name_acronym: DO
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_defaultospfinterfaces.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default OSPF Interface

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Open Shortest Path First, or OSPF, is a routing protocol to exchange IP routes. There are two versions of the OSPF protocol:

* Version 2 is configured on IPv4 interfaces and only exchances IPv4 prefixes
* Version 3 is configured on IPv6 interfaces and exchanges both IPv4 and IPv6 prefixes

OSPF sessions in the deafult VRF are always established between `DefaultOSPFInterfaces` in a [`DefaultOSPFArea`](defaultospfarea.md), and never operate inter-area. To connect two OSPF areas to each other, an area border router (ABR) configures both areas in the same [`DefaultOSPFInstance`](defaultospfinstance.md). A [`DefaultOSPFInstance`](defaultospfinstance.md) is an isolated process with its own Link State Database (LSDB).

OSPF interfaces can be configured as "passive", meaning they won't actively try to establish OSPF adjacencies, nor will they respond to incoming OSPF packets. Passive OSPF interfaces are configured to advertise prefixes reachable through this interface, without participating in the OSPF topology.

> To set up an OSPF interface in the overlay, use [`OSPFInterface`](ospfinterface.md) instead.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `DefaultOSPFInterface`

* An interface, options are:
    * The [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) that the OSPF session will be established on 
    * The [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md) that passively participates in the OSPF area
* The [`DefaultOSPFArea`](defaultospfarea.md) this interface is configured in
* The [`DefaultOSPFInstance`](defaultospfinstance.md) this interface is configured in

## Referenced resources

### [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md)

OSPF adjacencies are formed between IP addresses, and therefore require a reference to the [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) that will establish the adjacency. If the `DefaultOSPFInterface` is configured as "passive", no adjacency will be attempted or accepted. This is useful when the prefixes reachable through this interface should be advertised to the OSPF area (for example static routes), without actively taking part in the topology.

### [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md)

In a typical [`Fabric`](../../../fabrics.eda.nokia.com/docs/resources/fabric.md), overlay routes are exchanged via BGP between the [`SystemInterfaces`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md) on each node. To advertise the IP address of the [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md) to the other nodes, it must participate in the OSPF area without actively trying to establish an OSPF session. In this scenario, a `DefaultOSPFInterface` referencing the [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md) is required and must be configured as a passive OSPF interface.

### [`DefaultOSPFInstance`](defaultospfinstance.md)

An OSPF instance is an isolated process that establishes OSPF adjacencies and keeps track of all prefixes that are reachable in the OSPF areas that are part of this instance. For example, if dual-stack OSPFv2 and OSPFv3 topologies are configured, each protocol version runs in its own OSPF instance, with separate Link-State Databases (LSDB).

If the same `DefaultOSPFInterface` is linked to two different [`DefaultOSPFInstances`](defaultospfinstance.md), two `DefaultOSPFInterface` resources need to be created, each referencing a different [`DefaultOSPFInstance`](defaultospfinstance.md).

### [`DefaultOSPFArea`](defaultospfarea.md)

Prefixes can be exchanged between OSPF areas by interconnecting them on an Area Border Router (ABR) which configures both [`DefaultOSPFAreas`](defaultospfarea.md) in the same [`DefaultOSPFInstance`](defaultospfinstance.md). One interface is always part of one [`DefaultOSPFArea`](defaultospfarea.md).


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
