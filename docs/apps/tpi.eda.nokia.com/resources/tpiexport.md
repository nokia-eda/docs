---
resource_name: TPIExport
resource_name_plural: tpiexports
resource_name_plural_title: TPI Exports
resource_name_acronym: TE
crd_path: docs/apps/tpi.eda.nokia.com/crds/tpi.eda.nokia.com_tpiexports.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# TPI Export

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Exports EDA objects into a TPI workbook file. The generated file is always available as a workflow artifact. When `tpiStorage` is set and the referenced [`TPIStorage`](./tpistorage.md) CR exists in the workflow namespace, the file is also uploaded there and -- when the path can be sanitized into a valid Kubernetes DNS-1123 name -- a [`TPI`](./tpi.md) object is created in the workflow namespace, named `<storage-name>-<sanitized-path>` (path lowercased; any character outside `[a-z0-9.-]` replaced with `-`; leading and trailing `-` and `.` trimmed). If the [`TPIStorage`](./tpistorage.md) CR is missing, the workbook is still written to the workflow artifact, then the export **fails**, so the run is visibly unsuccessful; no upload occurs.

## Filter refinement

The typical export cycle is iterative: export, review, refine the filter, and re-export until the TPI content matches expectations.

1. **Create a `TPIFilter`** selecting the desired API groups, kinds, and optionally label selectors and column exclusions.
2. **Trigger a `TPIExport`** referencing that filter, a target path, and optionally a `TPIStorage`.
3. **Download and review the exported TPI** -- either from the `TPIStorage` server or directly from the workflow artifact.
4. **Adjust the `TPIFilter`** (add/remove kinds, exclude columns, reorder columns, narrow label selectors) and **re-export** until the result is satisfactory.

## Child resources

By default, `TPIExport` **does not** include **child resources** -- objects EDA manages under a parent resource. Enable **Include child resources** on the `TPIFilter` (set `includeChildResources: true` on the `TPIFilter` spec) when you need those rows in the workbook.

If the `TPIFilter` selects only kinds where **every** matching instance in the cluster is a **child resource**, the export can end up **empty** for those resource types: by default, each matching instance is omitted, so there are no data rows. An example is exporting **only** `BridgeDomain` when each bridge domain is part of a parent `VirtualNetwork`. To change that, enable `includeChildResources` on the filter, or widen the filter to include the parent kind (for example `VirtualNetwork`) so matching parent objects appear as normal rows in the workbook.

## Dependencies

The `TPIExport` workflow has no dependencies.

## Referenced resources

The `TPIExport` workflow optionally references:

- [`TPIFilter`](./tpifilter.md) via `spec.tpifilter`. When unset, all API resources visible to the workflow's service account are exported.
- [`TPIStorage`](./tpistorage.md) via `spec.tpiStorage`. When unset, the workbook is only available as a workflow artifact (no upload, no `TPI` CR created).

Both must live in the same namespace as the `TPIExport` workflow.

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
