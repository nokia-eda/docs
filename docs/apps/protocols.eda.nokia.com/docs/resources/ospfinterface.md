---
resource_name: OSPFInterface
resource_name_plural: ospfinterfaces
resource_name_plural_title: OSPF Interfaces
resource_name_acronym: OI
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_ospfinterfaces.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# OSPF Interface

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Open Shortest Path First, or OSPF, is a routing protocol to exchange IP routes. There are two versions of the OSPF protocol:

* Version 2 is configured on IPv4 interfaces and only exchances IPv4 prefixes
* Version 3 is configured on IPv6 interfaces and exchanges both IPv4 and IPv6 prefixes

OSPF sessions are always established between `OSPFInterfaces` in an [`OSPFArea`](ospfarea.md), and never operate inter-area. To connect two OSPF areas to each other, an area border router (ABR) configures both areas in the same [`OSPFInstance`](ospfinstance.md). An [`OSPFInstance`](ospfinstance.md) is an isolated process with its own Link State Database (LSDB).

OSPF interfaces can be configured as "passive", meaning they won't actively try to establish OSPF adjacencies, nor will they respond to incoming OSPF packets. Passive OSPF interfaces are configured to advertise prefixes reachable through this interface, without participating in the OSPF topology.

> To set up an OSPF interface in the default VRF, use [`DefaultOSPFInterface`](defaultospfinterface.md) instead.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `OSPFInterface`

* The [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md) that the OSPF session will be established on
* The [`OSPFArea`](ospfarea.md) this interface is configured in
* The [`OSPFInstance`](ospfinstance.md) this interface is configured in

## Referenced resources

### [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md)

OSPF adjacencies are formed between IP addresses, and therefore require a reference to the [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md) that will establish the adjacency. If the `OSPFInterface` is configured as "passive", no adjacency will be attempted or accepted. This is useful when the prefixes reachable through this interface should be advertised to the OSPF area (for example loopback IP addresses, static routes, ...), without actively taking part in the topology.

### [`OSPFInstance`](ospfinstance.md)

An OSPF instance is an isolated process that establishes OSPF adjacencies and keeps track of all prefixes that are reachable in the OSPF areas that are part of this instance. For example, if dual-stack OSPFv2 and OSPFv3 topologies are configured, each protocol version runs in its own OSPF instance, with separate Link-State Databases (LSDB).

If the same `OSPFInterface` is linked to two different [`OSPFInstances`](ospfinstance.md), two `OSPFInterface` resources need to be created, each referencing a different [`OSPFInstance`](ospfinstance.md).

### [`OSPFArea`](ospfarea.md)

Prefixes can be exchanged between OSPF areas by interconnecting them on an Area Border Router (ABR) which configures both [`OSPFAreas`](ospfarea.md) in the same [`OSPFInstance`](ospfinstance.md). One interface is always part of one [`OSPFArea`](ospfarea.md).


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
