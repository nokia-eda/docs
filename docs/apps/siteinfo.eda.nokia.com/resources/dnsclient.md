---
resource_name: DNSClient
resource_name_plural: dnsclients
resource_name_plural_title: DNS Clients
resource_name_acronym: DC
crd_path: docs/apps/siteinfo.eda.nokia.com/crds/siteinfo.eda.nokia.com_dnsclients.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# DNS Client

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
