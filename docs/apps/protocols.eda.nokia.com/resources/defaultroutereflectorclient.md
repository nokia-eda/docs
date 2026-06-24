---
resource_name: DefaultRouteReflectorClient
resource_name_plural: defaultroutereflectorclients
resource_name_plural_title: Default Route Reflector Clients
resource_name_acronym: DR
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_defaultroutereflectorclients.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default Route Reflector Client

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `DefaultRouteReflectorClient` resource is in many ways similar to the [`RouteReflectorClient`](routereflectorclient.md) resource, but is deployed in the default VRF instead of the overlay. This means that it has support for more routing protocols, which are required to distribute overlay (service) routes.

BGP route reflector clients peer with [route reflectors](defaultroutereflector.md) to eliminate the need for a full-mesh iBGP peering network, where every router needs to establish an iBGP session with every other router in the network. They assume that all routes in the network are advertised by the [route reflectors](defaultroutereflector.md).

EDA creates a derived [`DefaultBGPPeer`](defaultbgppeer.md) for every [`DefaultRouteReflector`](defaultroutereflector.md) that the `DefaultRouteReflectorClient` targets. This targeting is done by assigning labels to the [`DefaultRouteReflector`](defaultroutereflector.md) and referencing this label in the `DefaultRouteReflectorClient`.

!!! warning "Don't forget to use labels!"
    If no target label is specified in the `RouteReflectorSelector` property of the `DefaultRouteReflectorClient` resource, it will create [`DefaultBGPPeer`](defaultbgppeer.md) resources for **every** [`DefaultRouteReflector`](defaultroutereflector.md) and [`RouteReflector`](routereflector.md).

    **Example:**
    
    * `DefaultRouteReflectorClient` Client1 has **no** `RouteReflectorSelector `labels
    * `DefaultRouteReflectorClient` Client2 has **one** `RouteReflectorSelector` label: `my-rr-label=A`
    * [`DefaultRouteReflector`](defaultroutereflector.md) RR1 has one label: `my-rr-label=A`
    * [`DefaultRouteReflector`](defaultroutereflector.md) RR2 has one label: `my-rr-label=B`

    In this example, `Client1` will create 2 derived [`DefaultBGPPeer`](defaultbgppeer.md) resources: one for each route reflector. `Client2` will create only 1 derived [`DefaultBGPPeer`](defaultbgppeer.md) resource towards `RR1`. `RR2` does not have label `my-rr-label=A`, and therefore is not selected as route reflector for `Client2`.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `RouteReflectorClient`

- A [`DefaultBGPGroup`](#defaultbgpgroup) that the `DefaultRouteReflectorClient` will inherit settings from, such as local and remote AS numbers
- An interface that the `DefaultRouteReflectorClient` will use to establish the client sessions. This can either be a [`SystemInterface`](#systeminterface) or a [`DefaultInterface`](#defaultinterface)

## Referenced resources

### [`DefaultBGPGroup`](defaultbgpgroup.md)

The [`DefaultBGPPeer`](defaultbgppeer.md) resource that the `DefaultRouteReflectorClient` creates towards each selected [`DefaultRouteReflector`](defaultroutereflector.md) is always linked to a single [`DefaultBGPGroup`](defaultbgpgroup.md). These BGP peers share common parameters, such as BGP import and export policies, local and peer autonomous system numbers, and BGP timers. By specifying these parameters in a [`DefaultBGPGroup`](defaultbgpgroup.md), the operator can change these settings in a single location for all BGP peers.

### [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md)

To know which IP address is used to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is a [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md) attached directly to the system address of the [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md), a reference to this resource needs to be provided when creating the `DefaultRouteReflectorClient`.

### [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md)

To know which IP address is used to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is an [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) attached to a [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md), a reference to this resource needs to be provided when creating the `DefaultRouteReflectorClient`.

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

The [`DefaultBGPPeer`](defaultbgppeer.md) resources that the `DefaultRouteReflectorClient` creates towards each selected [`DefaultRouteReflector`](defaultroutereflector.md) inherit import/export policies from the assigned [`DefaultBGPGroup`](#dependencies). This behavior can be overridden by specifying policies in the `DefaultRouteReflectorClient`. Click [here](bgppeer.md#policy) for more information on BGP import/export policies.

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
