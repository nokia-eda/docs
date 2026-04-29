---
resource_name: Breakout
resource_name_plural: breakouts
resource_name_plural_title: Breakouts
resource_name_acronym: B
crd_path: docs/apps/interfaces.eda.nokia.com/crds/interfaces.eda.nokia.com_breakouts.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Breakout

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `Breakout` resource splits a physical port into multiple logical sub-ports, for scenarios where a single fiber on one end is split into multiple fibers (using an "octopus cable"). This is required for the node to understand the right **lane mapping** in the optical module and to provision multiple MAC addresses.

Typically, these breakout cables are used in top-of-rack switches where 100G ports are overkill for compute connectivity: 32x100G ports can be split out into 128x25G ports, optimizing space by only requiring 32 optical cages instead of 128. The signaling is frequently done over DAC (direct-attach copper) cables, but can also be done using fibers.

## Dependencies

The `Breakout` resource does not depend on any other resources. It is required, however, that the underlying physical port supports the breakout configuration.

## Referenced resources

### `TopoNode`

Breakouts can be configured on one or more nodes, using the `nodeSelectors` or `nodes` properties.

## OS-specific implementation notes

Breakouts are supported on the following operating systems:

- SR Linux

### SR OS

In SR OS, breakout ports are specified through connectors in the `TopoNode` resource. `Breakout` resources will ignore any selected SR OS nodes, and no configuration will be pushed to those nodes.

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