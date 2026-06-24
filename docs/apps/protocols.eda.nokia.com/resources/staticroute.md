---
resource_name: StaticRoute
resource_name_plural: staticroutes
resource_name_plural_title: Static Routes
resource_name_acronym: SR
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_staticroutes.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Static Route

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Static routes enable connectivity to remote network elements that do not have a routing protocol enabled to advertise routes. A static route is either configured with one or more next-hop IP addresses, or as a blackhole route. A blackhole route will attract traffic for the entire subnet, but will discard packets if no longer prefix match is available in the routing table. 

Example: if all outbound traffic is meant to pass through a firewall device, a default static route (`0.0.0.0/0`) could be configured with the next-hop IP address of the firewall.

!!! note "Deployment of the static route"

    The `StaticRoute` resource can optionally configured with a list of `TopoNodes` on which the static route is configured. If no nodes are referenced, EDA will configure the static route on all nodes that the [`Router`](../../../services.eda.nokia.com/docs/resources/router.md) is configured on. Although static routes are not installed in the routing table if the next-hop is not a locally reachable IP address, configuring a static route with a non-local next-hop should be avoided.

> To set up static routes in the default VRF, use [`DefaultStaticRoute`](defaultstaticroute.md) instead.

## Dependencies

To configure this resource, the following resources must exist or be created alongside the `StaticRoute`

* The [`Router`](../../../services.eda.nokia.com/docs/resources/router.md) in which the static route will be configured

## Referenced resources

### [`Router`](../../../services.eda.nokia.com/docs/resources/router.md)

Static route prefixes configured in the `StaticRoute` resource are only configured in the VRF of the linked [`Router`](../../../services.eda.nokia.com/docs/resources/router.md) resource. The next-hop of the static routes should be reachable through a local interface (typically a [`RoutedInterface`](../../../services.eda.nokia.com/docs/resources/routedinterface.md) or [`IRBInterface`](../../../services.eda.nokia.com/docs/resources/irbinterface.md)) configured in the same [`Router`](../../../services.eda.nokia.com/docs/resources/router.md).

### `TopoNode`

Optionally, a list of nodes can be provided on which the static route is deployed. EDA **does not** determine on which nodes the next-hop IP address is reachable through a local interface, but instead deploys the static route on **ALL** nodes that the [`Router`](../../../services.eda.nokia.com/docs/resources/router.md) is configured on, if no nodes are specified.

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
