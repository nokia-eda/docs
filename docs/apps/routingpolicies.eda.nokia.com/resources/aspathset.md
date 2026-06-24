---
resource_name: ASPathSet
resource_name_plural: aspathsets
resource_name_plural_title: AS Path Sets
resource_name_acronym: AP
crd_path: docs/apps/routingpolicies.eda.nokia.com/crds/routingpolicies.eda.nokia.com_aspathsets.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# AS Path Set

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
