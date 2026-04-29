---
resource_name: NTPClient
resource_name_plural: ntpclients
resource_name_plural_title: NTP Clients
resource_name_acronym: NC
crd_path: docs/apps/timing.eda.nokia.com/crds/timing.eda.nokia.com_ntpclients.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# NTP Client

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
