---
resource_name: RoutedInterface
resource_name_plural: routedinterfaces
resource_name_plural_title: Routed Interfaces
resource_name_acronym: RI
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_routedinterfaces.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Routed Interface

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `RoutedInterface` associates an [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) with a [`Router`](./router.md), usually with an IP address that is used as the source IP of originated traffic.

It is very similar to the [`IRBInterface`](./irbinterface.md), which connects a [`Router`](./router.md) to a [`BridgeDomain`](./bridgedomain.md). The `RoutedInterface` does not have to be associated with a physical interface: it can also be used with loopback[^1] interfaces.

The most common use cases of routed interfaces are:

- Setting up a BGP connection to a locally connected device (a firewall, a datacenter gateway)
- Establishing an OSPF neighborship between a host and the virtualized [`Router`](./router.md)
- Providing a next-hop for static routes toward an internet gateway router

## Dependencies

### [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-)

A `RoutedInterface` is always associated with a particular [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-). This interface can be virtual (a loopback[^1]), or linked to a (set of) physical port(s).

The same physical interface can be connected to multiple virtualized [`Router`](./router.md) services. A VLAN tag is used to determine which service will be used to process the packet.

### [`Router`](./router.md)

The `RoutedInterface` enables reachability towards a particular subnet. This route may be a host route (`/32`) for a loopback[^1] interface, a point-to-point route (`/31` or `/30`), or a bigger subnet route.

This route is installed in the routing table of the [`Router`](./router.md) that the `RoutedInterface` is connected to. If the [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) should be connected to the default VRF, check out the [`DefaultInterface`](-{{ ref_app_doc('routing', 'defaultinterface') }}-) instead.

## Referenced resources

### `IndexAllocationPool`

If the `RoutedInterface` is connected to a physical interface, a VLAN tag should be specified to determine which packets will be processed by the [`Router`](#router) associated with this `RoutedInterface`.

The VLAN tag can be manually specified (including special values `null` and `any`), or can automatically be drawn from an index allocation pool.

### [`Filter`](-{{ ref_app_doc('filters', 'filter') }}-)

Traffic that is received by or sent from the `RoutedInterface` can optionally be filtered by specifying one or more [`Filter`](-{{ ref_app_doc('filters', 'filter') }}-) resources in the `ingress` (respectively `egress`) container.

### [`IngressPolicy`](-{{ ref_app_doc('qos', 'ingresspolicy') }}-)

Traffic that is received by the `RoutedInterface` can optionally be processed by one or more QoS [`IngressPolicies`](-{{ ref_app_doc('qos', 'ingresspolicy') }}-) by specifying them in the `ingress` container.

### [`EgressPolicy`](-{{ ref_app_doc('qos', 'egresspolicy') }}-)

Traffic that is sent by the `RoutedInterface` can optionally be processed by one or more QoS [`EgressPolicies`](-{{ ref_app_doc('qos', 'egresspolicy') }}-) by specifying them in the `egress` container.

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

[^1]: Loopback interfaces are logical interfaces used to enable a switch to send or receive traffic. The system interface is an example of a loopback interface.