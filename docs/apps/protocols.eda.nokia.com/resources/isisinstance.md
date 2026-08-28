---
resource_name: ISISInstance
resource_name_plural: isisinstances
resource_name_plural_title: ISIS Instances
resource_name_acronym: II
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_isisinstances.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# ISIS Instance

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

/// admonition | Documentation coming soon!
    type: info

///
<!-- ## Dependencies

..

## Referenced resources

..

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

/// -->

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
