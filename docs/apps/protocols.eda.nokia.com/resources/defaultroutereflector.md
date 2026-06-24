---
resource_name: DefaultRouteReflector
resource_name_plural: defaultroutereflectors
resource_name_plural_title: Default Route Reflectors
resource_name_acronym: DR
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_defaultroutereflectors.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default Route Reflector

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `DefaultRouteReflector` resource is in many ways similar to the [`RouteReflector`](routereflector.md) resource, but is deployed in the default VRF instead of the overlay. This means that it has support for more routing protocols, which are required to distribute overlay (service) routes.

BGP route reflectors are used to eliminate the need for a full-mesh iBGP peering network, where every router needs to establish an iBGP session with every other router in the network. Route reflectors re-advertise the routes they receive from the [route reflector clients](defaultroutereflectorclient.md), removing the need for iBGP sessions between the clients.

EDA creates a derived [`DefaultBGPPeer`](defaultbgppeer.md) for every [`DefaultRouteReflectorClient`](defaultroutereflectorclient.md) that the `DefaultRouteReflector` targets. This targeting is done by assigning labels to the [`DefaultRouteReflectorClient`](defaultroutereflectorclient.md), and referencing this label in the `DefaultRouteReflector`.

!!! warning "Don't forget to use labels!"

    If no target label is specified in the `ClientSelector` property of the `DefaultRouteReflector` resource, the `DefaultRouteReflector` will create [`DefaultBGPPeer`](defaultbgppeer.md) resources for **every** [`DefaultRouteReflectorClient`](defaultroutereflectorclient.md) and [`RouteReflectorClient`](routereflectorclient.md).

    **Example:**
    
    * `DefaultRouteReflector` RR1 has **no** `ClientSelector` labels
    * `DefaultRouteReflector` RR2 has **one** `ClientSelector` label: `rr-label=client`
    * [`DefaultRouteReflectorClient`](defaultroutereflectorclient.md) Client1 has one label: `rr-label=client`
    * [`DefaultRouteReflectorClient`](defaultroutereflectorclient.md) Client2 has one label: `rr-label=client`
    * [`DefaultRouteReflectorClient`](defaultroutereflectorclient.md) Client3 has one label: `rr-label=somethingelse`

    In this example, `RR1` will create 3 derived [`DefaultBGPPeer`](defaultbgppeer.md) resources: one for each client. `RR2` will create only 2 derived [`DefaultBGPPeer`](defaultbgppeer.md) resources: one towards `client1`, and one towards `client2`. `Client3` does not have label `rr-label=client`, and therefore is not selected as client for `RR2`.

To set up BGP route reflectors in router services, use [`RouteReflector`](routereflector.md) instead.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `DefaultRouteReflector`

- A [`DefaultBGPGroup`](#defaultbgpgroup) that the `DefaultRouteReflector` will inherit settings from, such as local and remote AS numbers
- An interface that the `DefaultRouteReflector` will use to establish the client sessions. This can either be a [`SystemInterface`](#systeminterface) or a [`DefaultInterface`](#defaultinterface)

## Referenced resources

### [`DefaultBGPGroup`](defaultbgpgroup.md)

The [`DefaultBGPPeer`](defaultbgppeer.md) resource that the `DefaultRouteReflector` creates towards each selected [`DefaultRouteReflectorClient`](defaultroutereflectorclient.md) is always linked to a single [`DefaultBGPGroup`](defaultbgpgroup.md). These BGP peers share common parameters, such as BGP import and export policies, local and peer autonomous system numbers, and BGP timers. By specifying these parameters in a [`DefaultBGPGroup`](defaultbgpgroup.md), the operator can change these settings in a single location for all client BGP peers.

### [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md)

To know which IP address is used to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is a [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md) attached directly to the system address of the [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md), a reference to this resource needs to be provided when creating the `DefaultRouteReflector`.

### [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md)

To know which IP address is used to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is an [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) attached to a [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md), a reference to this resource needs to be provided when creating the `DefaultRouteReflector`.

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

The [`DefaultBGPPeer`](defaultbgppeer.md) resources that the `DefaultRouteReflector` creates towards each selected [`DefaultRouteReflectorClient`](defaultroutereflectorclient.md) inherit import/export policies from the assigned [`DefaultBGPGroup`](#dependencies). This behavior can be overridden by specifying policies in the `DefaultRouteReflector`. Click [here](bgppeer.md#policy) for more information on BGP import/export policies.

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
