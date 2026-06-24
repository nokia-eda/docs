---
resource_name: SystemLoadBalancer
resource_name_plural: systemloadbalancers
resource_name_plural_title: System Load Balancers
resource_name_acronym: SL
crd_path: docs/apps/siteinfo.eda.nokia.com/crds/siteinfo.eda.nokia.com_systemloadbalancers.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# System Load Balancer

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
