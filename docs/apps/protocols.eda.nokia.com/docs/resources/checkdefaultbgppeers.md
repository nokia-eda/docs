---
resource_name: CheckDefaultBgpPeers
resource_name_plural: checkdefaultbgppeerss
resource_name_plural_title: Check Default Bgp Peers
resource_name_acronym: CD
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_checkdefaultbgppeerss.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Check Default Bgp Peers

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `CheckDefaultBGPPeers` workflow can be used to query the status of all BGP sessions in the default VRF, across a selection of nodes. More specifically, for a list of nodes, it loops over all [`DefaultBGPPeers`](defaultbgppeer.md) configured on those nodes and looks up whether the session is established on the relevant node.

## Workflow definition

The selection of the nodes can be done in one of two ways:

1. via the node selector, by selecting individual nodes
2. via the label selector, which selects all nodes that have the label assigned to them

If both the node selector and the label selector are left empty, no nodes will be selected. 

??? info "The Waitfor parameter"

    The `Waitfor` parameter of this workflow waits for the nodes on which the workflow is run to be ready, not for the sessions to be ready!

## Workflow execution

The result of the workflow, upon completion, is the number of BGP sessions that were operational compared to the number of BGP sessions that have an associated [`DefaultBGPPeer`](defaultbgppeer.md) resource. For example:

```
...
status:
  result: default BGP peer check successful, 8/8 up
...
```

## Dependencies

This workflow has no dependencies. If no nodes were selected by the node selector or no nodes matched the label selector, the workflow will complete successfully.

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
