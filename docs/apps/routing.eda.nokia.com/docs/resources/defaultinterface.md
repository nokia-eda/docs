---
resource_name: DefaultInterface
resource_name_plural: defaultinterfaces
resource_name_plural_title: Default Interfaces
resource_name_acronym: DI
crd_path: docs/apps/routing.eda.nokia.com/crds/routing.eda.nokia.com_defaultinterfaces.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default Interface

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `DefaultInterface` resource links an `Interface` to the [`DefaultRouter`](./defaultrouter.md), with the addition of an optional VLAN tag. It can be configured with an IP-Prefix or IPv6 unnumbered, which configures the IP that will be associated with the interface. 

!!! tip "Best deployed as part of a Fabric"

    When possible, we recommend that you deploy this resource through a [`Fabric`](../../../fabrics.eda.nokia.com/docs/resources/fabric.md) which automatically creates two `DefaultInterfaces` for every [inter-switch link](../../../fabrics.eda.nokia.com/docs/resources/isl.md): one on each side of the `Link`.

## BFD

BFD parameters can be configured on a `DefaultInterface`. The configured BFD session will monitor the neighboring interface, improving the fault detection time significantly if there is layer-2-only equipment in between the two switches.

??? question "Not seeing BFD sessions being established?"

    BFD requires a protocol to subscribe before a BFD session is created. This could be either a static route, a BGP peer, or OSPF neighbor. For example, a [`BGPPeer`](../../../protocols.eda.nokia.com/docs/resources/bgppeer.md) with BFD enabled will only establish a session with its peer if the underlying [`DefaultInterface`](./defaultinterface.md) has BFD enabled as well, and vice versa.

## Dependencies

### [`DefaultRouter`](./defaultrouter.md)

The `DefaultInterface` is always connected to a [`DefaultRouter`](./defaultrouter.md), which is the abstraction for the routing table that will install the IP subnet configured on the interface. The [`DefaultRouter`](./defaultrouter.md) must be created before the `DefaultInterface` can be attached to it.

## Referenced resources

The `DefaultInterface` has no references to any other EDA resources.

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
