---
resource_name: SystemInterface
resource_name_plural: systeminterfaces
resource_name_plural_title: System Interfaces
resource_name_acronym: SI
crd_path: docs/apps/routing.eda.nokia.com/crds/routing.eda.nokia.com_systeminterfaces.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# System Interface

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The system interface is also known as the router ID, and is a special loopback address in the [`DefaultRouter`](./defaultrouter.md) used as a unique identifier for the node in the network. The `SystemInterface` resource is also typically used as the source IP address for setting up MP-BGP sessions that exchange [overlay](../index.md#overlay-routing) routes.

!!! tip "Best deployed as part of a Fabric"

    When possible, we recommend that you deploy this resource through a [`Fabric`](../../../fabrics.eda.nokia.com/docs/resources/fabric.md) which automatically creates a `SystemInterface` for every node in the `Fabric`.

## BFD

BFD parameters can be configured on a `SystemInterface`. The configured BFD session will monitor a remote IP address, improving the fault detection time significantly. 

??? question "Not seeing BFD sessions being established?"

    BFD requires a protocol to subscribe before a BFD session is created. This could be either a static route or a BGP peer. For example, a [`BGPPeer`](../../../protocols.eda.nokia.com/docs/resources/bgppeer.md) with BFD enabled will only establish a BFD session with its peer if the underlying [`SystemInterface`](./systeminterface.md) has BFD enabled as well, and vice versa.

## Dependencies

### [`DefaultRouter`](./defaultrouter.md)

The `SystemInterface` is always connected to a [`DefaultRouter`](./defaultrouter.md), which is the abstraction for the routing table that will install the IP subnet configured on the interface. The [`DefaultRouter`](./defaultrouter.md) must be created before the `SystemInterface` can be attached to it.

## Referenced resources

The `SystemInterface` has no references to any other EDA resources.

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
