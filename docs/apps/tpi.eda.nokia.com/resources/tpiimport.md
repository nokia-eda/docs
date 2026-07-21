---
resource_name: TPIImport
resource_name_plural: tpiimports
resource_name_plural_title: TPI Imports
resource_name_acronym: TI
crd_path: docs/apps/tpi.eda.nokia.com/crds/tpi.eda.nokia.com_tpiimports.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# TPI Import

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Reads a [`TPI`](./tpi.md), validates its content, and submits the resulting changes as an EDA transaction. By default, the transaction is committed; set `spec.dryRun: true` to validate without applying any changes. Optionally chains a [`TPIExport`](./tpiexport.md) afterward (only on a successful non-dry-run import) to produce an updated master TPI.

## TPI processing

To help understand what can and cannot be done when populating a TPI, this section describes the processing steps used during an import.

### Column resolution

When processing a TPI, the column-to-schema mapping is built by walking the header hierarchy:

1. Start at row 4 for each column
2. Follow merged cells downward, concatenating field names with dots
3. Map the resulting path to the corresponding schema property

This allows columns to be reordered without breaking imports.

### Row processing

For each data row:

1. Read the `context` value to determine the target JSON path
2. Classify each cell as either:

    - **Content**: Schema path (without `[]`) starts with the context → value to insert
    - **Primary Key**: Schema path does not start with context → used for navigation
    - **Content in wrong context**: The cell column is not included in its context → report an error.

3. Navigate the object tree using primary keys to find the insertion point
4. Insert the content at the target location

### Cell content handling

- Whitespace around the sheet title (row 1) and the `action` value is trimmed before parsing; all other cell content is taken verbatim from the workbook.
- Empty cells are ignored.

### Type coercion

Cell values are coerced based on schema type:

| Schema Type | Coercion Rule |
|-------------|---------------|
| `string` | Used as-is (after trimming) |
| `integer` | Parsed as 64-bit integer |
| `number` | Parsed as 64-bit float |
| `boolean` | Case-insensitive `true` or `false` |

If parsing fails, the original string is preserved and schema validation will report the error.

### Delta operations

The `action` column on the top-level row (context = `.`) specifies the operation:

| Action | Behavior |
|--------|----------|
| `add` | Create new resource. This will fail if the object already exists in EDA to avoid accidental hijack. |
| `update` | Replace the existing resource with the spec assembled from the TPI rows. This will fail if the object does not exist in EDA. |
| `delete` | Remove resource. |
| (empty) | Skip this object during import. |

Nested rows (non-root context) have an empty action. Actions are applied on the object as a whole, not per property.

/// danger | update is a whole-object replace, not a field-wise merge

Any field that is **absent** from the rows of an `update` object is **cleared** on the target object during import. This matters whenever the source TPI is missing columns that exist on the live object -- most commonly when the workbook was produced with a [`TPIFilter`](./tpifilter.md) whose `excludedColumns` strips part of the schema (e.g. `.spec.bridgeDomains` on `VirtualNetwork`). Re-importing such a workbook with `action=update` removes those excluded fields from every matching cluster object, even though the operator never wrote anything there. **No runtime warning is emitted.** When a filtered export is reused as the basis for an update, either widen the filter to include every field that must be preserved, or restrict the workbook to the rows that genuinely need to change. The include-style `columns` filter does not exhibit this problem: hidden columns remain in the workbook with their original values, so re-import preserves them.
///

### Validation

Validation occurs at multiple stages; the checks performed by the `TPIImport` workflow itself are:

1. **Primary key validation**: Errors if required primary keys are missing from a row.
2. **Context validation**: Errors if there are cells that are neither primary keys for the context nor values of the context itself.
3. **Schema validation**: Assembled objects are validated against the Kubernetes CRD OpenAPI schema, which covers required fields, type and format constraints, enums, and length/range bounds. Type coercion (see [Type coercion](#type-coercion)) fails silently into the raw string and surfaces here.
4. **Existence validation**: For `add` rows, errors if the target object already exists in the cluster (to avoid accidental hijack); for `update` rows, errors if it does not exist. `delete` rows are not pre-checked here; missing targets surface at transaction time.

All validation errors are collected and returned together where possible (for example, if a row is missing primary keys, schema validation cannot be performed without risking false positives or negatives).

EDA will then proceed with further validations when processing the intents, generating the `NodeConfig` and validating them with the NPP, and eventually sending the `NodeConfig` to the devices. If any error occurs at this stage, it will be captured in the transaction result.

## Transactions

Every import workflow (`TPIImport` and `TPIImportDryRun`) creates an EDA transaction. The transaction description follows the pattern:

```
TPI import for <tpi-name>
```

where `<tpi-name>` is the name of the referenced [`TPI`](./tpi.md) object.

### Validation failures

If validation fails (TPI-level validation or EDA transaction validation), **no changes are committed** to the cluster. Errors are reported in the workflow status under the `errors` field, with structured information including:

- The affected sheet
- The object name
- The field path
- The error message
- A cell reference back to the TPI

For details on the validation stages and the types of checks performed, see [Validation](#validation).

### Warnings

When no row on a sheet sets the `action` column, no object from that sheet would have been part of the transaction even on a successful parse — every row maps to [`action = (empty)`](#delta-operations), i.e., skipped. Blocking the whole import on parse errors from such a sheet would penalise users for unrelated mistakes on sheets they did not intend to touch. To prevent this, parsing errors collected from those sheets are demoted: they are **not** added to `status.errors`, the workflow does **not** fail because of them, and they are listed under `status.warnings` instead:

```yaml
status:
  warnings:
    - sheet: virtualnetworks
      field: .name
      error: missing object name
      ref: B17
```

A WARN-level message is also written to the workflow log for every affected sheet.

Errors keep their original blocking behaviour (land on `status.errors` and fail the workflow) when any of the following is true:

- At least one row on the sheet has a non-empty `action` value (the user intended to touch this sheet).
- The error is not attributable to a single sheet (for example, namespace validation against the `METADATA` sheet, or transaction-level failures returned by EDA).
- The sheet's schema could not be resolved (`no schema found for sheet ...`).

### Dry run transactions

A [`TPIImportDryRun`](./tpiimportdryrun.md) always creates a dry run transaction with detailed output. This lets you inspect exactly what changes would be applied -- including intent processing, `NodeConfig` generation, and NPP validation -- without any risk of modifying cluster state.

## Dependencies

The `TPIImport` workflow has no dependencies.

## Referenced resources

The `TPIImport` workflow references:

- [`TPI`](./tpi.md) via `spec.tpi` (required) -- the workbook to import.
- When `spec.exportMaster` is set (only valid with `dryRun: false`), the embedded export configuration also references:
    - [`TPIFilter`](./tpifilter.md) via `spec.exportMaster.tpifilter` (**required** in this mode; the master export refuses to run without it, since the filter owns namespace selection and would otherwise silently diverge from the imported TPI's metadata namespace).
    - [`TPIStorage`](./tpistorage.md) via `spec.exportMaster.tpiStorage` (optional; when unset the chained export only produces a workflow artifact).

All referenced resources must live in the same namespace as the `TPIImport` workflow.

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
