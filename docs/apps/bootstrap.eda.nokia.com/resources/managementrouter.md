---
resource_name: ManagementRouter
resource_name_plural: managementrouters
resource_name_plural_title: Management Routers
resource_name_acronym: MR
crd_path: docs/apps/bootstrap.eda.nokia.com/crds/bootstrap.eda.nokia.com_managementrouters.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Management Router

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `ManagementRouter` enables a node to communicate with other network nodes through its management port, which may be an out-of-band or an in-band port. It is often connected to a separate physical or virtual (VLAN) network used to manage the nodes.

/// admonition
    type: warning

The `ManagementRouter` is created by the [`Init`](./init.md) resource. It should not be necessary to create this resource manually.
///


## Management network instance name

On each node, EDA configures a single management network instance. The instance name is fixed per operating system and must not be reused as the name of a virtual router service.

- **SR Linux**: `mgmt`
- **SR OS**: `management`
- **Cumulus**: N/A
- **EOS**: N/A
- **Junos**: `mgmt_junos`
- **Nexus**: N/A

## Dependencies

### `TopoNode`

Nodes can be selected with a label selector or listed by name. If neither is provided, the management network instance is configured on all `TopoNode` resources.

## Referenced resources

The `ManagementRouter` does not reference any other EDA resources.

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
