---
resource_name: DefaultStaticRoute
resource_name_plural: defaultstaticroutes
resource_name_plural_title: Default Static Routes
resource_name_acronym: DS
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_defaultstaticroutes.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default Static Route

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Static routes enable connectivity to remote network elements that do not have a routing protocol enabled to advertise routes. A static route is either configured with one or more next-hop IP addresses, or as a blackhole route. A blackhole route will attract traffic for the entire subnet, but will discard packets if no longer prefix match is available in the routing table. 

Example: if all outbound traffic is meant to pass through a firewall device, a default static route (`0.0.0.0/0`) could be configured with the next-hop IP address of the firewall.

> To set up static routes in the overlay, use [`StaticRoute`](staticroute.md) instead.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `DefaultStaticRoute`

* The [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md) in which the static route will be configured

## Referenced resources

### [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md)

Static route prefixes configured in the `DefaultStaticRoute` resource are only configured in the VRF of the linked [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md) resource. The next-hop of the static routes should be reachable through a local interface (typically a [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md)) configured in the same [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md).

### `TopoNode`

Optionally, a list of nodes can be provided on which the static route is deployed. EDA **does not** determine on which nodes the next-hop IP address is reachable through a local interface, but instead deploys the static route on **ALL** nodes that the [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md) is configured on, if no nodes are specified.

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
