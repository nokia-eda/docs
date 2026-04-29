---
resource_name: RouteReflectorClient
resource_name_plural: routereflectorclients
resource_name_plural_title: Route Reflector Clients
resource_name_acronym: RR
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_routereflectorclients.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Route Reflector Client

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

BGP route reflector clients peer with [route reflectors](routereflector.md) to eliminate the need for a full-mesh iBGP peering network, where every router needs to establish an iBGP session with every other router in the network. They assume that all routes in the network are advertised by the [route reflectors](routereflector.md).

EDA creates a derived [`BGPPeer`](bgppeer.md) for every [`RouteReflector`](routereflector.md) that the `RouteReflectorClient` targets. This targeting is done by assigning labels to the [`RouteReflector`](routereflector.md) and referencing this label in the `RouteReflectorClient`.

!!! warning "Don't forget to use labels!"

    If no target label is specified in the `RouteReflectorSelector` property of the `RouteReflectorClient` resource, the `RouteReflectorClient` will create [`BGPPeer`](bgppeer.md) resources for **every** [`DefaultRouteReflector`](defaultroutereflector.md) and [`RouteReflector`](routereflector.md).

    **Example:**
    
    * `RouteReflectorClient` Client1 has **no** `RouteReflectorSelector `labels
    * `RouteReflectorClient` Client2 has **one** `RouteReflectorSelector` label: `my-rr-label=A`
    * [`RouteReflector`](routereflector.md) RR1 has one label: `my-rr-label=A`
    * [`RouteReflector`](routereflector.md) RR2 has one label: `my-rr-label=B`

    In this example, `Client1` will create 2 derived [`BGPPeer`](bgppeer.md) resources: one for each route reflector. `Client2` will create only 1 derived [`BGPPeer`](bgppeer.md) resource towards `RR1`. `RR2` does not have label `my-rr-label=A`, and therefore is not selected as route reflector for `Client2`.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `RouteReflectorClient`

- A [`BGPGroup`](#bgpgroup) that the `RouteReflectorClient` will inherit settings from, such as local and remote AS numbers
- An interface that the `RouteReflectorClient` will use to establish the client sessions. This can either be a [`RoutedInterface`](#routedinterface) or an [`IRBInterface`](#irbinterface)

## Referenced resources

### [`BGPGroup`](bgpgroup.md)

The [`BGPPeer`](bgppeer.md) resource that the `RouteReflectorClient` creates towards each selected [`RouteReflector`](routereflector.md) is always linked to a single [`BGPGroup`](bgpgroup.md). These BGP peers share common parameters, such as BGP import and export policies, local and peer autonomous system numbers, and BGP timers. By specifying these parameters in a [`BGPGroup`](bgpgroup.md), the operator can change these settings in a single location for all BGP peers.

### [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md)

To know which IP address the router uses to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is a [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md) attached directly to an [`Interface`](../../../interfaces.eda.nokia.com/docs/resources/interface.md), a reference to this resource needs to be provided when creating the `RouteReflectorClient`.

### [`IRBInterface`](../../../services.eda.nokia.com/docs/resources/irbinterface.md)

To know which IP address the router uses to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is an [`IRBInterface`](../../../services.eda.nokia.com/docs/resources/irbinterface.md) attached to a [`BridgeDomain`](../../../services.eda.nokia.com/docs/resources/bridgedomain.md), a reference to this resource needs to be provided when creating the `RouteReflectorClient`.

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

The [`BGPPeer`](bgppeer.md) resources that the `RouteReflectorClient` creates towards each selected [`RouteReflector`](routereflector.md) inherit import/export policies from the assigned [`BGPGroup`](#dependencies). This behavior can be overridden by specifying policies in the `RouteReflectorClient`. Click [here](bgppeer.md#policy) for more information on BGP import/export policies.

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
