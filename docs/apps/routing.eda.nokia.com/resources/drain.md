---
resource_name: Drain
resource_name_plural: drains
resource_name_plural_title: Drains
resource_name_acronym: D
crd_path: docs/apps/routing.eda.nokia.com/crds/routing.eda.nokia.com_drains.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Drain

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `Drain` resource is used to divert traffic away from a certain node. It accomplishes this by installing a routing [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md) that artificially extends the AS path of outgoing BGP routes, causing peers to uninstall those routes as they are no longer the most optimal.

!!! warning

    Installing a `Drain` resource on a [`DefaultRouter`](./defaultrouter.md) does not stop the advertisement of any routes, and therefore does not drop traffic: if the **only** route to a particular IP-prefix goes through the drained [`DefaultRouter`](./defaultrouter.md), it will still go through that node!

This resource is usually created as part of a workflow, like the [`DeployImage`](../../../os.eda.nokia.com/docs/resources/deployimage.md) workflow.

## Dependencies

### [`DefaultRouter`](./defaultrouter.md)

The `Drain` resource creates and installs a BGP routing [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md) which is installed in any selected [`DefaultRouter`](./defaultrouter.md). If these [`DefaultRouter`](./defaultrouter.md) resources are selected using the `defaultRouters` property, they must exist before the `Drain` resource is created.

## Referenced resources

The `Drain` has no references to any other EDA resources.

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
