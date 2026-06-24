---
resource_name: SFlow
resource_name_plural: sflows
resource_name_plural_title: S Flows
resource_name_acronym: SF
crd_path: docs/apps/flowsampling.eda.nokia.com/crds/flowsampling.eda.nokia.com_sflows.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# SFlow

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
