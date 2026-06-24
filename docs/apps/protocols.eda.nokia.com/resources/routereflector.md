---
resource_name: RouteReflector
resource_name_plural: routereflectors
resource_name_plural_title: Route Reflectors
resource_name_acronym: RR
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_routereflectors.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Route Reflector

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-


BGP route reflectors are used to eliminate the need for a full-mesh iBGP peering network, where every router needs to establish an iBGP session with every other router in the network. Route reflectors re-advertise the routes they receive from the [route reflector clients](routereflectorclient.md), removing the need for iBGP sessions between the clients.

EDA creates a derived [`BGPPeer`](bgppeer.md) for every [`RouteReflectorClient`](routereflectorclient.md) that the `RouteReflector` targets. This targeting is done by assigning labels to the [`RouteReflectorClient`](routereflectorclient.md), and referencing this label in the `RouteReflector`.

!!! warning "Don't forget to use labels!"

    If no target label is specified in the `ClientSelector` property of the `RouteReflector` resource, the `RouteReflector` will create [`BGPPeer`](bgppeer.md) resources for **every** [`DefaultRouteReflectorClient`](defaultroutereflectorclient.md) and [`RouteReflectorClient`](routereflectorclient.md).

    **Example:**
    
    * `RouteReflector` RR1 has **no** `ClientSelector` labels
    * `RouteReflector` RR2 has **one** `ClientSelector` label: `my-rrc-label=A`
    * [`RouteReflectorClient`](routereflectorclient.md) Client1 has one label: `my-rrc-label=A`
    * [`RouteReflectorClient`](routereflectorclient.md) Client2 has one label: `my-rrc-label=A`
    * [`RouteReflectorClient`](routereflectorclient.md) Client3 has one label: `my-rrc-label=B`

    In this example, `RR1` will create 3 derived [`BGPPeer`](bgppeer.md) resources: one for each client. `RR2` will create only 2 derived [`BGPPeer`](bgppeer.md) resources: one towards `client1`, and one towards `client2`. `Client3` does not have label `my-rrc-label=A`, and therefore is not selected as client for `RR2`.

To set up BGP route reflectors in the default VRF, use [`DefaultRouteReflector`](defaultroutereflector.md) instead.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `RouteReflector`

- A [`BGPGroup`](#bgpgroup) that the `RouteReflector` will inherit settings from, such as local and remote AS numbers
- An interface that the `RouteReflector` will use to establish the client sessions. This can either be a [`RoutedInterface`](#routedinterface) or an [`IRBInterface`](#irbinterface)

## Referenced resources

### [`BGPGroup`](bgpgroup.md)

The [`BGPPeer`](bgppeer.md) resource that the `RouteReflector` creates towards each selected [`RouteReflectorClient`](routereflectorclient.md) is always linked to a single [`BGPGroup`](bgpgroup.md). These BGP peers share common parameters, such as BGP import and export policies, local and peer autonomous system numbers, and BGP timers. By specifying these parameters in a [`BGPGroup`](bgpgroup.md), the operator can change these settings in a single location for all client BGP peers.

### [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md)

To know which IP address the router uses to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is a [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md) attached directly to an [`Interface`](../../../interfaces.eda.nokia.com/docs/resources/interface.md), a reference to this resource needs to be provided when creating the `RouteReflector`.

### [`IRBInterface`](../../../services.eda.nokia.com/docs/resources/irbinterface.md)

To know which IP address the router uses to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is an [`IRBInterface`](../../../services.eda.nokia.com/docs/resources/irbinterface.md) attached to a [`BridgeDomain`](../../../services.eda.nokia.com/docs/resources/bridgedomain.md), a reference to this resource needs to be provided when creating the `RouteReflector`.

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

The [`BGPPeer`](bgppeer.md) resources that the `RouteReflector` creates towards each selected [`RouteReflectorClient`](routereflectorclient.md) inherit import/export policies from the assigned [`BGPGroup`](#dependencies). This behavior can be overridden by specifying policies in the `RouteReflector`. Click [here](bgppeer.md#policy) for more information on BGP import/export policies.

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
