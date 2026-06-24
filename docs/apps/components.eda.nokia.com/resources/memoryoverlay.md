---
resource_name: MemoryOverlay
resource_name_plural: memoryoverlays
resource_name_plural_title: Memory Overlays
resource_name_acronym: MO
crd_path: docs/apps/components.eda.nokia.com/crds/components.eda.nokia.com_memoryoverlays.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Memory Overlay

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

!!! info "Documentation coming soon!"

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
