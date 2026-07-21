---
resource_name: TPIImportDryRun
resource_name_plural: tpiimportdryruns
resource_name_plural_title: TPI Import Dry Runs
resource_name_acronym: TD
crd_path: docs/apps/tpi.eda.nokia.com/crds/tpi.eda.nokia.com_tpiimportdryruns.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# TPI Import Dry Run

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Reads a [`TPI`](./tpi.md), validates its content, and submits the resulting changes as a **dry run transaction**. No changes are committed. Use this to preview and verify changes before applying them. See [`TPIImport`](./tpiimport.md) for a detailed walkthrough of the process.

## Dependencies

The `TPIImportDryRun` workflow has no dependencies.

## Referenced resources

The `TPIImportDryRun` workflow references a [`TPI`](./tpi.md) via `spec.tpi` (required) -- the workbook to validate. The referenced `TPI` must live in the same namespace as the `TPIImportDryRun` workflow.

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
