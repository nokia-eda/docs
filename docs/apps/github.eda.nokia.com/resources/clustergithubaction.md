---
resource_name: ClusterGitHubAction
resource_name_plural: clustergithubactions
resource_name_plural_title: Cluster Git Hub Actions
resource_name_acronym: CG
crd_path: docs/apps/github.eda.nokia.com/crds/github.eda.nokia.com_clustergithubactions.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Cluster Git Hub Action

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
