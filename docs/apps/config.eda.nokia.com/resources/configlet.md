---
resource_name: Configlet
resource_name_plural: configlets
resource_name_plural_title: Configlets
resource_name_acronym: C
crd_path: docs/apps/config.eda.nokia.com/crds/config.eda.nokia.com_configlets.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Configlet

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Sometimes [custom configuration](../index.md#custom-configuration) must be pushed to a node because an existing EDA abstraction does not support it. As the number of supported operating systems increases, abstracting new features into custom resources may take time. Older features that newer protocols have largely replaced may also not have an abstraction.

The `Configlet` resource allows an operator to make quick configuration adjustments on one or more nodes while preserving EDA's declarative design and network-wide transactions.

Although it may be tempting to make `Configlet` resources part of your network design, limit their use to small or temporary workarounds. [Custom applications](../index.md#custom-configuration) avoid the following limitations:

- A `Configlet` does not adapt its paths or configuration payloads to schema changes between operating system versions. Use separate `Configlet` resources for incompatible versions.
- Other resources do not reference `Configlet` resources, so a `Configlet` cannot automatically attach additional configuration to instances of another resource.
- The `Configlet` status reports the selected endpoints, but it does not provide per-path operational health or generate alarms for the configuration it pushes.

## Targeting nodes

The `Configlet` targets nodes listed in the `endpoints` field and nodes whose labels match the `endpointSelectors` field.

The `operatingSystem` and `version` fields can further restrict the nodes matched by `endpointSelectors`. Version matching is exact and does not support wildcard characters.

/// admonition | Use label selectors wherever possible
    type: warning

When selecting targets manually with `endpoints`, every listed node must match the `operatingSystem` and `version` specified in the `Configlet`. Otherwise, the transaction fails.
///

## Priorities

The `priority` of a `Configlet` is an integer between -100 and 100. When configuration values conflict, higher priorities overwrite lower priorities. The default priority is 0.

## Dependencies

### `TopoNode`

A `Configlet` can target one or more `TopoNode` resources. Nodes listed explicitly in `endpoints` must exist and must match the `operatingSystem` and `version` of the `Configlet` when those fields are set.

/// admonition
    type: tip

Use `endpointSelectors` to select nodes by label wherever possible. A `Configlet` can be created even if no nodes currently match its label selectors, allowing it to target hardware onboarded in the future.

The `Configlet` is applied only to nodes that match a label selector and, when specified, its `operatingSystem` and `version`. This supports node upgrades with schema changes, where a single `Configlet` is not valid for both operating system versions.
///

## Referenced resources

The `Configlet` does not reference any other EDA resources.

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

To browse the Custom Resource Definition, go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
