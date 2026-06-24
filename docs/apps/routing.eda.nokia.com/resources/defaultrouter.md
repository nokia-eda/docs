---
resource_name: DefaultRouter
resource_name_plural: defaultrouters
resource_name_plural_title: Default Routers
resource_name_acronym: DR
crd_path: docs/apps/routing.eda.nokia.com/crds/routing.eda.nokia.com_defaultrouters.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default Router

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `DefaultRouter` resource is an abstraction for the main network instance of a router. On most network operating systems this special router has a number of additional features compared to virtual router services: 

- Enables routing protocols like OSPF, IS-IS to operate on (sub)interfaces that are attached to the default router
- Establishes transport tunnels like VxLAN and MPLS tunnels
- Originates and advertises MP-BGP service routes like EVPN and BGP-IPVPN routes

!!! tip "Best deployed as part of a Fabric"

    When possible, we recommend that you deploy this resource through a [`Fabric`](../../../fabrics.eda.nokia.com/docs/resources/fabric.md) which automatically creates a `DefaultRouter` for every node in the [`Fabric`](../../../fabrics.eda.nokia.com/docs/resources/fabric.md).

The `DefaultRouter` resource is the representation of a routing table, which receives IPv4 and IPv6 routes from attached [`DefaultInterfaces`](./defaultinterface.md), [`SystemInterfaces`](./systeminterface.md), and BGP neighbors. In addition, it contains the service routes originating from bridged and routed interfaces connected to virtual network services.

## Deployment

One `DefaultRouter` resource is linked to a single `TopoNode` resource, which represents a physical network switch. The `DefaultRouter` specifies certain global parameters such as:

- The router ID
- [BGP parameters](#bgp)
- [Route leaking](#route-leaking) policies
- Import and export policies that determine which routes are accepted from neighbors and which routes are exported to neighbors

## BGP

If BGP is used as a protocol to exchange routes from the default router to its neighbors, the BGP section of the `DefaultRouter` must be enabled and configured. 

Most of the properties of the BGP container can be overridden by BGP peers and BGP groups (set of BGP peers that share common parameters). Nevertheless, it is useful to have default values specified in the `DefaultRouter` resource and to enable all BGP address families that will be exchanged in your network, even if not every BGP peer will be used to exchange all of these families. 

!!! important "Autonomous system number"

    On Nokia SR OS, the autonomous system number must be present in the `DefaultRouter`, even if it is overridden in the BGP peer. Without it, BGP sessions will appear as down and no routes will be exchanged.

## Route leaking

Route leaking is performed when reachability information from a virtual router service needs to be exposed to the default routing table. A use case for route leaking is an in-band management network that needs to be reachable from the default routing table. The inverse is also possible: for example, a default static route towards the internet that is configured in the default router of your network may be exposed to services that have access to the internet.

Often, route leaking is done in both ways simultaneously: public IP addresses are isolated from internal IP addresses through a virtual router service. To enable internet access for those publicly routable IP addresses, a default route towards the internet is leaked from the default router to the virtual router, and the public IP subnet is exposed to the internet by leaking from the virtual router to the default router.

![Route leaking in action](../media/routing-route_leaking.svg){ width="100%" }

## Dependencies
 
### `TopoNode`

A `DefaultRouter` is always linked to exactly one node. The `TopoNode` resource must be created before the `DefaultRouter` can be deployed.

## Referenced resources

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

Import and export [routing policies](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md) can be configured for [route leaking](#route-leaking) purposes or as global parameters for [BGP](#bgp) peering sessions. 

### [`Keychain`](../../../security.eda.nokia.com/docs/resources/keychain.md)

BGP keychains contain authentication parameters to secure communication between two BGP peers. If a [`Keychain`](../../../security.eda.nokia.com/docs/resources/keychain.md) is configured in the `DefaultRouter`, every BGP peer established on a [`DefaultInterface`](./defaultinterface.md) will use it to authenticate the neighbor unless it is overridden at the group or peer level.

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
