---
resource_name: RouteTrace
resource_name_plural: routetraces
resource_name_plural_title: Route Traces
resource_name_acronym: RT
crd_path: docs/apps/routing.eda.nokia.com/crds/routing.eda.nokia.com_routetraces.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Route Trace

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `RouteTrace` workflow analyzes the route a packet would take from a source to a destination, by looking at the routing table of the source and all nodes on the (ECMP) path.

The input parameters of the workflow are:

- The **destination IP** address of the packet
- The **node** that the packet starts from
- The **network instance** that the lookups are performed in

The workflow result is a list of possible links that the packet may use to get to the destination.

!!! note "Not a ping"

    The workflow does not send any traffic: it analyzes the routing table directly, and will create one result row per ECMP path segment.

By default, the workflow uses the route table of the [`DefaultRouter`](./defaultrouter.md). A different router can be specified by using the `networkInstance` property.

!!! warning

    This workflow does not rely on EDA to do the lookup: it investigates the routing tables on the nodes directly. Currently, only SR Linux nodes are supported. Other operating systems are silently skipped.

## Dependencies

The `RouteTrace` workflow has no dependencies.

## Referenced resources

The `RouteTrace` workflow has no references to any other EDA resources.

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

??? example "Example execution"

    The workflow correctly discovered 4 links that the packets going from `leaf11` to `leaf13` may encounter:
    
    - Two ECMP paths on `leaf11`
        - One via `spine11`
        - One via `spine12`
    - One path from `spine11` to `leaf13` (the destination)
    - One path from `spine12` to `leaf13` (the destination)

    ---

    ```
    apiVersion: routing.eda.nokia.com/v1
    kind: RouteTrace
    metadata:
      annotations:
        workflows.core.eda.nokia.com/id: '3'
        workflows.core.eda.nokia.com/root-workflow-group: routing.eda.nokia.com
        workflows.core.eda.nokia.com/root-workflow-kind: RouteTrace
        workflows.core.eda.nokia.com/root-workflow-name: routetrace-12670557-e0a3-49d3-ba14-264de513a878
        workflows.core.eda.nokia.com/root-workflow-namespace: eda
        workflows.core.eda.nokia.com/root-workflow-version: v1
        workflows.core.eda.nokia.com/state: Completed
        workflows.core.eda.nokia.com/username: admin
      name: routetrace-12670557-e0a3-49d3-ba14-264de513a878
      namespace: eda
    spec:
      address: 10.46.99.33
      node: leaf11
    status:
      links:
        - fromNode:
            interface: ethernet-1/31
            localAddress: fe80::18cc:10ff:feff:1f
            node: leaf11
          toNode:
            interface: ethernet-1/1
            localAddress: fe80::1892:22ff:feff:1
            node: spine11
        - fromNode:
            interface: ethernet-1/32
            localAddress: fe80::18cc:10ff:feff:20
            node: leaf11
          toNode:
            interface: ethernet-1/1
            localAddress: fe80::1817:23ff:feff:1
            node: spine12
        - fromNode:
            interface: ethernet-1/3
            localAddress: fe80::1892:22ff:feff:3
            node: spine11
          toNode:
            interface: ethernet-1/31
            localAddress: fe80::1814:12ff:feff:1f
            node: leaf13
        - fromNode:
            interface: ethernet-1/3
            localAddress: fe80::1817:23ff:feff:3
            node: spine12
          toNode:
            interface: ethernet-1/32
            localAddress: fe80::1814:12ff:feff:20
            node: leaf13
        - fromNode:
            node: leaf13
          toNode:
            destination: true
    workflowStatus:
      stages:
        - name: Initializing
          state: Completed
        - name: performing-trace
          state: Completed
      state: Completed
    ```

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
