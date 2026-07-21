---
resource_name: TPIFilter
resource_name_plural: tpifilters
resource_name_plural_title: TPI Filters
resource_name_acronym: TF
crd_path: docs/apps/tpi.eda.nokia.com/crds/tpi.eda.nokia.com_tpifilters.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# TPI Filter

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `TPIFilter` controls what content is included when exporting EDA API objects to a TPI file. There are four filtering mechanisms, each detailed in its own section below:

1. **API object selection** -- restrict the export to specific Kubernetes Kinds. See [Selecting API objects](#selecting-api-objects).
2. **Column inclusion and ordering** -- narrow and reorder the columns kept visible in each sheet. See [Including and ordering columns](#including-and-ordering-columns).
3. **Column exclusion** -- actively strip optional fields from the discovered schema for each Kind. See [Excluding columns](#excluding-columns).
4. **Label-selector filtering** -- export only objects whose labels match a Kubernetes label selector. See [Label selectors](#label-selectors).

Resource status is always included: use `columns` to omit status columns from a sheet.

The `TPIFilter` used during export is recorded in the [`METADATA`](./tpi.md#metadata-sheet) sheet (`tpifilter-name` and `tpifilter-spec`) for traceability.

/// tip | TPIFilter has no effect on import operations

`TPIFilter` is exclusively used during export. Import is governed by Kubernetes and EDA RBAC mechanisms. As of EDA 26.4, this includes GVK (Group/Version/Kind) and namespace rules bound to the authenticated EDA user.
///

## Crafting a filter

A `TPIFilter` is optional for export. When omitted, all resource types from the selected namespace are exported. In practice, defining a filter is strongly recommended to keep exported TPIs focused and manageable.

### Selecting API objects

Each entry in `spec.apiObjects` selects one resource type using its **API group** and **Kind**. These values match the sheet header format `Kind (apigroup)` described in [Sheet Naming](./tpi.md#sheet-naming). For example, to select `VirtualNetwork` from `services.eda.nokia.com`:

```yaml
spec:
  apiObjects:
    - group: services.eda.nokia.com
      kind: VirtualNetwork
```

### Including and ordering columns

`columns` declares which schema columns are kept visible in the exported sheet and, optionally, how they are ordered among their siblings.
The path syntax is the same as the `context` column in a TPI -- dot-separated, with `[]` stripped.
Each entry has a required `path` and an optional `priority`:

- **When `columns` is empty (or omitted), every column from the schema stays visible.**
- **When `columns` is non-empty, only the listed columns (and the columns under a listed parent) are visible.** Other columns are hidden in the sheet. They remain in the workbook so users can unhide them if needed.
- **Parent paths include their whole subtree.** If a parent path remains listed, removing only one descendant entry does not hide that descendant. Remove the ancestor entry (or narrow the parent selection) to actually hide that leaf.
- **Required columns stay visible** even if not listed, unless one of their ancestors is itself hidden (in which case they cascade to hidden too).
- **Status columns can be included and ordered** like any other column.
- **Default order: `.spec` before `.status`.** Even when no priority is supplied, `.spec` columns are placed before `.status` columns. Listing either path with an explicit `priority` overrides this on a per-path basis.
- **`priority` orders siblings.** Entries with a numeric priority are placed before entries without priority within the same sibling group, and lower priority values come first. Listing a parent path applies the priority to the whole block of columns under it.
- **Unlisted siblings keep their default order**, which is determined by the `ui-order-priority` hint in the EDA OpenAPI schema (`x-eda-nokia-com.ui-order-priority`). When no such hint is present, fields are sorted alphabetically.
- **An excluded column cannot also be listed in `columns`**: `excludedColumns` actively strips the column from the discovered schema, so it has no path to include.

**Recommended workflow:** start with `columns` omitted (or empty) to inspect the full sheet, then add only the parent or leaf paths you want to keep visible. Add `priority` values only for siblings you want to reorder.

A path can point to a leaf field or to a parent (applying inclusion / priority to the whole block of columns under it):

```yaml
columns:
  - path: .spec.irbInterfaces
    priority: 1
  - path: .spec.bridgeDomains
    priority: 2
  - path: .spec.routers
    priority: 3
```

This places `irbInterfaces` columns first, then `bridgeDomains`, then `routers` -- and hides every other optional column under `.spec` -- regardless of their schema-defined order.

A single parent entry can be used to include an entire subtree without filtering:

```yaml
columns:
  - path: .spec   # include every column under .spec (no narrower filtering)
```

Another common pattern is to include both configuration and status subtrees:

```yaml
columns:
  - path: .spec
  - path: .status
```

This keeps the full `.spec` subtree visible and also includes all `.status` columns.

The fixed columns (`action`, `name`, `context`) are always at the start of the sheet and are not affected by `columns`. The optional common columns (`labels[]`, `annotations[]`) follow the same include behavior as other optional columns: when `columns` is non-empty, they are visible only if included (for example via `.labels` / `.annotations`). They can still be stripped from the workbook via `excludedColumns` paths `.labels` and `.annotations`. If a `priority` is set on `.labels` or `.annotations`, it has no ordering effect: these columns keep their fixed position in the common-columns block.

### Excluding columns

`excludedColumns` removes optional fields from the exported sheet, reducing noise for operators who do not need those fields. The path syntax is the same as the `context` column in a TPI -- dot-separated, with `[]` stripped:

```yaml
excludedColumns:
  - .spec.bridgeDomains.spec.eviPool   # exclude a specific leaf field
  - .spec.routers                      # exclude an entire subtree
  - .labels                            # hide labels[] column
  - .annotations                       # hide annotations[] column
```

**Rules:**

- **Required fields cannot be excluded.** This constraint is enforced by the [admission webhook](#admission-webhook) at create/update time.
- **Excluding a parent path excludes all its descendants.** For example, excluding `.spec.routers` removes the entire routers subtree, even if some of its children are optional -- as long as the subtree itself is not required.

/// danger | Excluded data is silently lost on update

`excludedColumns` actively strips the listed fields from the discovered schema, so the exported TPI carries no values for them. Imports apply `action=update` as a whole-object replace (see [TPI Import Delta Operations](./tpiimport.md#delta-operations)), not a field-wise merge: any field that is **not** in the workbook is **cleared** on the target object.

As a result, reusing a filtered export as the basis for an update wipes the excluded subtree from every updated cluster object. For example, a filter that drops `.spec.bridgeDomains` from a `VirtualNetwork` export will cause every `update` row to remove the existing `bridgeDomains` entries from that `VirtualNetwork`.

**No runtime warning is emitted** -- the transaction succeeds and the data loss only shows up when the affected objects are inspected.

**Recommendation:** treat filters with `excludedColumns` as read-only or templating filters. Export without `excludedColumns` (or widen it) when preparing TPIs intended to drive updates.

The `columns` include filter does not have this side effect: it only hides columns in the rendered sheet, the values stay in the workbook and survive re-import.
///

### Label selectors

Each entry in `apiObjects` can include `labelSelector` to restrict which objects are exported.

Selectors follow Kubernetes label selector syntax and semantics:

- Multiple entries in `labelSelector` are combined with **OR**
- Multiple requirements in one entry (comma-separated) are combined with **AND**
- Supported operators include `=`, `==`, `!=`, `in`, `notin`, existence (`key`), and does-not-exist (`!key`)

Examples:

```yaml
labelSelector:
  - "eda.nokia.com/role=edge"                                  # OR: objects with role=edge
  - "eda.nokia.com/role=core,eda.nokia.com/site=lon01"         # OR: objects with both role=core AND site=lon01
  - "eda.nokia.com/tpi-exclude!=true"                          # OR: label value is not true, or label is absent
  - "!eda.nokia.com/tpi-exclude"                               # OR: label is absent
  - "eda.nokia.com/role in (edge,core),eda.nokia.com/site"     # OR: role in set AND site label exists
```

For full selector grammar, see the Kubernetes [Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) documentation.

### Filter-wide options

Beyond the four `apiObjects`-level mechanisms above, the `TPIFilter` spec exposes a few filter-wide toggles:

| Field | Default | Effect |
|---|---|---|
| `spec.namespace` | workflow namespace | Overrides the source namespace for data collection. The `TPIExport` workflow itself, the `TPIFilter`, and the `TPIStorage` always live in the workflow namespace; this field lets the filter pull objects from a different namespace. |
| `spec.includeResources` | `true` | When `false`, only a blank TPI template is produced (no object rows). |
| `spec.includeChildResources` | `false` | Include derived/child resources in the export (e.g. a `BridgeDomain` automatically derived from a `VirtualNetwork`). |
| `spec.hideEmptyColumns` | `false` | Post-process the sheet to hide optional columns that are empty across all exported objects. Hidden columns remain in the workbook and can be revealed in a spreadsheet editor. |
| `spec.debug.disableStyling` | `false` | Troubleshooting only -- disable comments, styling, data validation, and conditional formatting in the generated TPI. |

/// admonition | Hide Empty Columns
    type: tip
The *Hide Empty Columns* option comes in handy when exporting a running configuration. Columns for optional fields that have no data across all exported objects are hidden automatically. The resulting TPI is compact and focused on the fields that are actually in use, while still being complete. Hidden columns can be revealed in the spreadsheet editor at any time (select all columns → right-click → *Unhide*).

This is particularly useful as a starting point: export with column hiding, inspect the active fields, then refine your `TPIFilter` to permanently exclude the fields you do not need.

///

## Admission webhook

Creating or updating a `TPIFilter` is validated by an admission webhook that checks each referenced API group and kind against the CRDs currently known to the cluster.

The webhook maintains an in-memory cache of CRDs, kept up to date in real time via a Kubernetes watch on `CustomResourceDefinition` resources. In the unlikely event a `TPIFilter` referencing a newly-registered CRD is rejected with a "CRD not found" error, restarting the manager forces a fresh cache build:


```bash
kubectl rollout restart deployment/tpi-manager -n eda-system  # (1)
```

1. Adapt `eda-system` to your EDA system namespace.

## Dependencies

The `TPIFilter` resource has no dependencies on other EDA resources.

## Referenced resources

A `TPIFilter` does not reference any other EDA resource by name. It selects which Kubernetes Kinds to include in the export via `spec.apiObjects` (group + kind); the referenced CRDs must exist in the cluster and are validated by the [admission webhook](#admission-webhook) at create/update time.

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
