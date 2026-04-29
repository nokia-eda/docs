---
resource_name: IslPing
resource_name_plural: islpings
resource_name_plural_title: Isl Pings
resource_name_acronym: IP
crd_path: docs/apps/fabrics.eda.nokia.com/crds/fabrics.eda.nokia.com_islpings.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Isl Ping

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

This `IslPing` workflow can be used to test whether all [`ISL`](./isl.md) links created by the [`Fabric`](./fabric.md) are functioning properly. The workflow loops over all [`ISL`](./isl.md) resources and pings the remote end from the local side.

In addition to reporting how many ping replies were received, this workflow also reports the minimum, maximum, and average round-trip-time of the pings done on each [`ISL`](./isl.md).

## Dependencies

The `IslPing` workflow does not have any dependencies. 

## Referenced resources

The `IslPing` workflow does not reference any other EDA resources.

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

    ```
    apiVersion: fabrics.eda.nokia.com/v1
    kind: IslPing
    metadata:
    annotations:
        workflows.core.eda.nokia.com/id: '17'
        workflows.core.eda.nokia.com/root-workflow-group: fabrics.eda.nokia.com
        workflows.core.eda.nokia.com/root-workflow-kind: IslPing
        workflows.core.eda.nokia.com/root-workflow-name: islping-2066d7ed-7caa-434d-a1b3-35f8a5f2dc24
        workflows.core.eda.nokia.com/root-workflow-namespace: eda
        workflows.core.eda.nokia.com/root-workflow-version: v1
        workflows.core.eda.nokia.com/state: Completed
        workflows.core.eda.nokia.com/username: admin
    name: islping-2066d7ed-7caa-434d-a1b3-35f8a5f2dc24
    namespace: eda
    spec:
    addressFamily: IPv4
    count: 5
    islSelectors:
        - fabric = my-fabric
    timeoutSeconds: 5
    status:
    details:
        - details:
            averageTimeNanoseconds: 2032000
            maxTimeNanoseconds: 3107000
            minTimeNanoseconds: 1293000
            received: 5
            sent: 5
            stdDevNanoseconds: 692000
            totalTimeNanoseconds: 4215530920
        name: isl-leaf-2-spine-2-0
        success: true
        - details:
            averageTimeNanoseconds: 2022000
            maxTimeNanoseconds: 3826000
            minTimeNanoseconds: 1223000
            received: 5
            sent: 5
            stdDevNanoseconds: 939000
            totalTimeNanoseconds: 4221295371
        name: isl-leaf-2-spine-2-1
        success: true
        - details:
            averageTimeNanoseconds: 2115312
            maxTimeNanoseconds: 2823286
            minTimeNanoseconds: 1892261
            received: 5
            sent: 5
            stdDevNanoseconds: 396844
            totalTimeNanoseconds: 10946287
        name: isl-leaf-1-spine-1-0
        success: true
        - details:
            averageTimeNanoseconds: 2157322
            maxTimeNanoseconds: 2906570
            minTimeNanoseconds: 1947374
            received: 5
            sent: 5
            stdDevNanoseconds: 419571
            totalTimeNanoseconds: 11066996
        name: isl-leaf-1-spine-1-1
        success: true
        - details:
            averageTimeNanoseconds: 2547236
            maxTimeNanoseconds: 3017186
            minTimeNanoseconds: 1888286
            received: 5
            sent: 5
            stdDevNanoseconds: 586873
            totalTimeNanoseconds: 13082031
        name: isl-leaf-1-spine-2-0
        success: true
        - details:
            averageTimeNanoseconds: 3237203
            maxTimeNanoseconds: 4776602
            minTimeNanoseconds: 1910719
            received: 5
            sent: 5
            stdDevNanoseconds: 1052750
            totalTimeNanoseconds: 16725643
        name: isl-leaf-1-spine-2-1
        success: true
        - details:
            averageTimeNanoseconds: 1077000
            maxTimeNanoseconds: 1362000
            minTimeNanoseconds: 800000
            received: 5
            sent: 5
            stdDevNanoseconds: 196000
            totalTimeNanoseconds: 4213035784
        name: isl-leaf-2-spine-1-0
        success: true
        - details:
            averageTimeNanoseconds: 1262000
            maxTimeNanoseconds: 1537000
            minTimeNanoseconds: 1031000
            received: 5
            sent: 5
            stdDevNanoseconds: 183000
            totalTimeNanoseconds: 4215465378
        name: isl-leaf-2-spine-1-1
        success: true
    workflowStatus:
    stages:
        - name: Initializing
        state: Completed
        - name: collecting ISL info
        state: Completed
        - name: pinging
        state: Completed
        subflows:
            - group: oam.eda.nokia.com
            id: 18
            kind: Ping
            name: ping-isl-isl-leaf-2-spine-2-0-18
            namespace: eda
            version: v1
            - group: oam.eda.nokia.com
            id: 19
            kind: Ping
            name: ping-isl-isl-leaf-2-spine-2-1-19
            namespace: eda
            version: v1
            - group: oam.eda.nokia.com
            id: 20
            kind: Ping
            name: ping-isl-isl-leaf-1-spine-1-0-20
            namespace: eda
            version: v1
            - group: oam.eda.nokia.com
            id: 21
            kind: Ping
            name: ping-isl-isl-leaf-1-spine-1-1-21
            namespace: eda
            version: v1
            - group: oam.eda.nokia.com
            id: 22
            kind: Ping
            name: ping-isl-isl-leaf-1-spine-2-0-22
            namespace: eda
            version: v1
            - group: oam.eda.nokia.com
            id: 23
            kind: Ping
            name: ping-isl-isl-leaf-1-spine-2-1-23
            namespace: eda
            version: v1
            - group: oam.eda.nokia.com
            id: 24
            kind: Ping
            name: ping-isl-isl-leaf-2-spine-1-0-24
            namespace: eda
            version: v1
            - group: oam.eda.nokia.com
            id: 25
            kind: Ping
            name: ping-isl-isl-leaf-2-spine-1-1-25
            namespace: eda
            version: v1
    state: Completed
    ```

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
