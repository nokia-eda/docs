---
resource_name: DefaultBGPPeer
resource_name_plural: defaultbgppeers
resource_name_plural_title: Default BGP Peers
resource_name_acronym: DB
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_defaultbgppeers.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default BGP Peer

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `DefaultBGPPeer` resource is in many ways similar to the [`BGPPeer`](bgppeer.md) resource, but is deployed in the default VRF instead of the overlay 

This means that it has support for more routing protocols, which are required to distribute overlay (service) routes. This resource is used when setting up a BGP session between two IP addresses in the default VRF. It represents a single participant in the BGP session, so if both sides of the BGP session are managed by EDA, two of these resources will need to be created. 

!!!note "Explicit vs implicit target IP"
    The source IP address of the default BGP peer is always inferred from the [`SystemInterface`](#systeminterface) or [`DefaultInterface`](#defaultinterface) it is linked to. The target IP address can either be explicitely configured, or implicitely inferred from the neighboring [`SystemInterface`](#systeminterface) or [`DefaultInterface`](#defaultinterface). 

    If the BGP neighbor is managed by EDA and also in the default VRF, you should avoid using explicit IPs.

To set up BGP peers in [`Router`](../../../services.eda.nokia.com/docs/resources/router.md) services, use [`BGPPeer`](bgppeer.md) instead.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `BGPPeer`

- A [`DefaultBGPGroup`](#defaultbgpgroup) that the `DefaultBGPPeer` will inherit settings from, such as local and remote AS numbers
- An interface that the `DefaultBGPPeer` will use to establish the session. This can either be a [`SystemInterface`](#systeminterface) or a [`DefaultInterface`](#defaultinterface)
- The target [`SystemInterface`](#systeminterface) or [`DefaultInterface`](#defaultinterface), if the target IP address is not configured explicitely.

## Referenced resources

### [`DefaultBGPGroup`](defaultbgpgroup.md)

A `DefaultBGPPeer` is always linked to a single [`DefaultBGPGroup`](defaultbgpgroup.md). In real-world networks, multiple BGP peers share common parameters, such as BGP import and export policies, local and peer autonomous system numbers, and BGP timers. These parameters can be specified in the group instead, allowing the operator to change these settings in a single location for all linked default BGP peers. All settings in the group can optionally be overridden in the individual peer resources. Configuration inheritance works as follows:

```mermaid
graph LR
    A[DefaultBGPPeer] -->|overrides| B
    B[DefaultBGPGroup] -->|overrides| C
    C[DefaultRouter]

    B[DefaultBGPGroup resource]
    C[DefaultRouter resource]
```

### [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md)

To know which IP address is used to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is a [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md) attached directly to the system address of the [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md), a reference to this resource needs to be provided when creating the `DefaultBGPPeer`.

This resource type can also be configured as the target of a `DefaultBGPPeer`, meaning the BGP session will be reconfigured with the new neighbor IP address if the target [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md) is changed.

### [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md)

To know which IP address is used to send BGP traffic, EDA must have a reference to a virtual interface. If this interface is an [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) attached to a [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md), a reference to this resource needs to be provided when creating the `DefaultBGPPeer`.

This resource type can also be configured as the target of a `DefaultBGPPeer`, meaning the BGP session will be reconfigured with the new neighbor IP address if the target [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) is changed.

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

Routing policies can be specified in various locations of the `DefaultBGPPeer` resource. These policies are used to filter or modify BGP routes sent/received by this `DefaultBGPPeer`. If no policies are configured, the default behavior for the router on which the `DefaultBGPPeer` is configured is followed, which may be different depending on the operating system.

## Examples

/// tab | YAML

```yaml
-{{ include_yaml('docs/snippets/%s.yaml' | format(resource_name | lower)) }}-
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
