---
resource_name: RouteLookup
resource_name_plural: routelookups
resource_name_plural_title: Route Lookups
resource_name_acronym: RL
crd_path: docs/apps/routing.eda.nokia.com/crds/routing.eda.nokia.com_routelookups.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Route Lookup

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

This workflow looks through the routing table of all selected nodes for a route towards the specified IP address. The result is a list of nodes that were searched, including whether a route was found and if so, what the next-hops are for that route.

By default, the workflow performs a lookup in the [`DefaultRouter`](./defaultrouter.md). A different router can be specified by using the `networkInstance` property.

!!! warning

    This workflow does not rely on EDA to do the lookup: it investigates the routing tables on the nodes directly. Currently, only SR Linux nodes are supported. Other operating systems are silently skipped.

## Resolve property

If `resolve` is set to `true`, the resolved next-hop for that route will be included in the output.

## Dependencies

The `RouteLookup` workflow has no dependencies.

## Referenced resources

The `RouteLookup` workflow has no references to any other EDA resources.

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

    The workflow correctly discovered 3 nodes that have a route towards IP `10.30.1.24` in the `inventory-router` network instance:
        
    - Node `leaf12` has an indirect route and will send these packets to `leaf11`
    - Node `leaf13` has an indirect route and will send these packets to `leaf11`
    - Node `leaf11` has a direct route and will send these packets out over sub-interface `ethernet-1/1.1311`
    
    The two spine nodes do not terminate the `inventory-router` service and do not have a route for this IP.

    ---

    ```
    apiVersion: routing.eda.nokia.com/v1
    kind: RouteLookup
    metadata:
      annotations:
        workflows.core.eda.nokia.com/id: '1'
        workflows.core.eda.nokia.com/root-workflow-group: routing.eda.nokia.com
        workflows.core.eda.nokia.com/root-workflow-kind: RouteLookup
        workflows.core.eda.nokia.com/root-workflow-name: routelookup-2d5801bd-a80e-4f64-8fe9-fca57c3a6a73
        workflows.core.eda.nokia.com/root-workflow-namespace: eda
        workflows.core.eda.nokia.com/root-workflow-version: v1
        workflows.core.eda.nokia.com/state: Completed
        workflows.core.eda.nokia.com/username: admin
      name: routelookup-2d5801bd-a80e-4f64-8fe9-fca57c3a6a73
      namespace: eda
    spec:
      address: 10.30.1.24
      networkInstance: inventory-router
      resolve: false
    status:
      found: true
      nodesWithRoute: 3
      results:
        - found: false
          networkInstance: inventory-router
          node: g99-spine11
        - found: false
          networkInstance: inventory-router
          node: g99-spine12
        - found: true
          networkInstance: inventory-router
          nextHopGroupID: 8605221109
          nextHops:
            - interfaces:
                - localAddress: 10.30.1.1/24
                  name: ethernet-1/1.1311
                  peerNode: g99-leaf11
              ipAddress: 10.30.1.1
              nextHopID: 8605221096
              type: Direct
          node: g99-leaf11
          rawOutput: |-
            /network-instance[name=inventory-router]/route-table:
                10.30.1.0/24
          route: 10.30.1.0/24
        - found: true
          networkInstance: inventory-router
          nextHopGroupID: 8605387614
          nextHops:
            - ipAddress: 10.46.99.31
              nextHopID: 8605387596
              type: Indirect
          node: g99-leaf13
          rawOutput: |-
            /network-instance[name=inventory-router]/route-table:
                10.30.1.0/24
          route: 10.30.1.0/24
        - found: true
          networkInstance: inventory-router
          nextHopGroupID: 8605208653
          nextHops:
            - ipAddress: 10.46.99.31
              nextHopID: 8605208636
              type: Indirect
          node: g99-leaf12
          rawOutput: |-
            /network-instance[name=inventory-router]/route-table:
                10.30.1.0/24
          route: 10.30.1.0/24
    workflowStatus:
      stages:
        - name: Initializing
          state: Completed
        - name: performing-lookup
          state: Completed
      state: Completed
    ```

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
