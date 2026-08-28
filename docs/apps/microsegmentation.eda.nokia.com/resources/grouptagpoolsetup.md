---
resource_name: GroupTagPoolSetup
resource_name_plural: grouptagpoolsetups
resource_name_plural_title: Group Tag Pool Setups
resource_name_acronym: GTPS
crd_path: docs/apps/microsegmentation.eda.nokia.com/crds/microsegmentation.eda.nokia.com_grouptagpoolsetups.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Group Tag Pool Setup

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `GroupTagPoolSetup` workflow resizes the global and local Group Tag `IndexAllocationPool` resources (`group-tag-pool-global` and `group-tag-pool-local`) that allocate Group Tag IDs.

The workflow accepts one or more `groupTagPoolSegments` and supports segment types `Global`, `Local`, and `Reserved`. Segments can be specified with either `end` or `size` (or both when consistent).

During validation and dry-run, the workflow enforces platform limits and rejects invalid layouts:

* D2/D3-capable deployments use an allocatable range of `[1,127]`.
* D4/D5-only deployments use an allocatable range of `[1,16383]`.
* Group Tag ID `0` remains reserved for no-group-tag and is not allocatable.
* Overlapping segments are rejected.
* Changes that would invalidate existing allocations are rejected.

Use this workflow when changing pool boundaries or reserving portions of the Group Tag ID space for future use.

## Dependencies

The `IndexAllocationPool` resources named `group-tag-pool-global` and `group-tag-pool-local` must exist in the target namespace.

## Referenced resources

### [`GroupTag`](./grouptag.md)

The workflow updates the ID allocation pools used by `GroupTag` resources.

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
