---
resource_name: AttachmentLookup
resource_name_plural: attachmentlookups
resource_name_plural_title: Attachment Lookups
resource_name_acronym: AL
crd_path: docs/apps/routing.eda.nokia.com/crds/routing.eda.nokia.com_attachmentlookups.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Attachment Lookup

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `AttachmentLookup` workflow searches all selected nodes for an interface configured with a certain IP address. This is useful for debugging purposes, for example when looking for the node with a particular system IP.

!!! note

    This workflow only looks for interfaces that are configured with the IP address. If you want to look for nodes that have a route toward a particular IP address (for example, both sides of a point-to-point link), use the [RouteLookup](./routelookup.md) workflow instead.

The workflow input must contain the IP address that a lookup is requested for, and an optional list of nodes to perform the lookup on. If neither the `nodeSelectors` nor `nodes` property is specified, the workflow runs on **all** nodes. 

By default, the workflow queries the interfaces of the [`DefaultRouter`](./defaultrouter.md). A different router can be specified by using the `networkInstance` property.

!!! warning

    This workflow does not rely on EDA to do the lookup: it investigates the routing tables on the nodes directly. Currently, only SR Linux nodes are supported. Other operating systems are silently skipped.

## Dependencies

The `AttachmentLookup` workflow has no dependencies.

## Referenced resources

The `AttachmentLookup` workflow has no references to any other EDA resources.

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

    The workflow correctly identified `spine-2` as the owner of IP `11.0.0.4`

    ---

    ```
    apiVersion: routing.eda.nokia.com/v1
    kind: AttachmentLookup
    metadata:
        annotations:
            workflows.core.eda.nokia.com/id: '29'
            workflows.core.eda.nokia.com/root-workflow-group: routing.eda.nokia.com
            workflows.core.eda.nokia.com/root-workflow-kind: AttachmentLookup
            workflows.core.eda.nokia.com/root-workflow-name: attachmentlookup-b9be2e94-0175-425a-bc60-abfd97cc4af1
            workflows.core.eda.nokia.com/root-workflow-namespace: eda
            workflows.core.eda.nokia.com/root-workflow-version: v1
            workflows.core.eda.nokia.com/state: Completed
            workflows.core.eda.nokia.com/username: admin
        name: attachmentlookup-b9be2e94-0175-425a-bc60-abfd97cc4af1
        namespace: eda
    spec:
        address: 11.0.0.4
        nodes:
            - leaf-1
            - leaf-2
            - spine-1
            - spine-2
        status:
            found: true
            results:
                - interface: system0
                  networkInstance: default
                  node: spine-2
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
