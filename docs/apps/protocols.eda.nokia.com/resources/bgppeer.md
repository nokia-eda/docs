---
resource_name: BGPPeer
resource_name_plural: bgppeers
resource_name_plural_title: BGP Peers
resource_name_acronym: BP
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_bgppeers.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# BGP Peer

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `BGPPeer` resource is required when setting up a BGP session between two [`Routers`](../../../services.eda.nokia.com/docs/resources/router.md). It represents a single participant in the BGP session, so if both sides of the BGP session are managed by EDA, two of these resources will need to be created. 

> To set up BGP peers in the default VRF, use [`DefaultBGPPeer`](defaultbgppeer.md) instead.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `BGPPeer`

- A [`BGPGroup`](#bgpgroup) that the `BGPPeer` will inherit settings from, such as local and remote AS numbers
- An interface that the `BGPPeer` will use to establish the session. This can either be a [`RoutedInterface`](#routedinterface) or an [`IRBInterface`](#irbinterface)

## Referenced resources

### [`BGPGroup`](bgpgroup.md)

A `BGPPeer` is always linked to a single [`BGPGroup`](bgpgroup.md). In real-world networks, multiple BGP peers share common parameters, such as BGP import and export policies, local and peer autonomous system numbers, and BGP timers. These parameters can be specified in the group instead, allowing the operator to change these settings in a single location for all linked BGP peers. All settings in the group can optionally be overridden in the individual peer resources. Configuration inheritance works as follows:

```mermaid
graph LR
    A[BGPPeer] -->|overrides| B
    B[BGPGroup] -->|overrides| C
    C[Router]

    B[BGPGroup resource]
    C[Router resource]
```

### [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md)

To know which IP address the router uses to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is a [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md) attached directly to an [`Interface`](../../../interfaces.eda.nokia.com/docs/resources/interface.md), a reference to this resource needs to be provided when creating the `BGPPeer`.

### [`IRBInterface`](../../../services.eda.nokia.com/docs/resources/irbinterface.md)

To know which IP address the router uses to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is an [`IRBInterface`](../../../services.eda.nokia.com/docs/resources/irbinterface.md) attached to a [`BridgeDomain`](../../../services.eda.nokia.com/docs/resources/bridgedomain.md), a reference to this resource needs to be provided when creating the `BGPPeer`.

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

Routing policies can be specified in various locations of the `BGPPeer` resource. These policies are used to filter or modify BGP routes sent/received by this `BGPPeer`. If no policies are configured, the default behavior for the router on which the `BGPPeer` is configured is followed, which may be different depending on the operating system.

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
