---
resource_name: SystemPing
resource_name_plural: systempings
resource_name_plural_title: System Pings
resource_name_acronym: SP
crd_path: docs/apps/routing.eda.nokia.com/crds/routing.eda.nokia.com_systempings.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# System Ping

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `SystemPing` workflow is used to verify reachability between the nodes via the [`DefaultRouter`](./defaultrouter.md). It works by selecting either nodes or [`SystemInterface`](./systeminterface.md) resources directly, and pinging between each pair of system IP addresses.

!!! info

    If the `nodes` or `nodeSelectors` properties are used, the workflow will look for [`SystemInterface`](./systeminterface.md) resources configured on those nodes. If no [`SystemInterfaces`](./systeminterface.md) were detected, the node will be ignored.
    
    Pings are done intelligently, meaning that if the workflow already pinged `leaf2` from `leaf1`, there will not be a ping to `leaf1` from `leaf2`. 

The workflow result contains an entry for each unique pair of system IP addresses, and the result of the ping between the two including minimum, maximum, and average latency.

## Dependencies

The `SystemPing` workflow has no dependencies.

## Referenced resources

### [`SystemInterface`](./systeminterface.md)

If the workflow is created for a set of manually selected [system interfaces](./systeminterface.md), these resources must be created first.

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
    apiVersion: routing.eda.nokia.com/v1
    kind: SystemPing
    metadata:
      annotations:
        workflows.core.eda.nokia.com/id: '26'
        workflows.core.eda.nokia.com/root-workflow-group: routing.eda.nokia.com
        workflows.core.eda.nokia.com/root-workflow-kind: SystemPing
        workflows.core.eda.nokia.com/root-workflow-name: systemping-81b6fdef-a885-43b8-9e1a-33f4f5e2e186
        workflows.core.eda.nokia.com/root-workflow-namespace: eda
        workflows.core.eda.nokia.com/root-workflow-version: v1
        workflows.core.eda.nokia.com/state: Completed
        workflows.core.eda.nokia.com/username: admin
      name: systemping-81b6fdef-a885-43b8-9e1a-33f4f5e2e186
      namespace: eda
    spec:
      addressFamily: DualStack
      count: 3
      timeoutSeconds: 5
    status:
      details:
        - details:
            averageTimeNanoseconds: 12356720
            maxTimeNanoseconds: 13588366
            minTimeNanoseconds: 10809367
            received: 3
            sent: 3
            stdDevNanoseconds: 1416143
            totalTimeNanoseconds: 38341978
          name: ping-system-spine11-10.46.99.35
          success: true
        - details:
            averageTimeNanoseconds: 7503323
            maxTimeNanoseconds: 9691685
            minTimeNanoseconds: 6345616
            received: 3
            sent: 3
            stdDevNanoseconds: 1896240
            totalTimeNanoseconds: 23948084
          name: ping-system-spine12-10.46.99.31
          success: true
        - details:
            averageTimeNanoseconds: 5878512
            maxTimeNanoseconds: 9310029
            minTimeNanoseconds: 3702043
            received: 3
            sent: 3
            stdDevNanoseconds: 3007280
            totalTimeNanoseconds: 18607960
          name: ping-system-leaf13-10.46.99.35
          success: true
        - details:
            averageTimeNanoseconds: 5399288
            maxTimeNanoseconds: 5771370
            minTimeNanoseconds: 5116235
            received: 3
            sent: 3
            stdDevNanoseconds: 336518
            totalTimeNanoseconds: 17323897
          name: ping-system-leaf12-10.46.99.34
          success: true
        - details:
            averageTimeNanoseconds: 5203379
            maxTimeNanoseconds: 6467957
            minTimeNanoseconds: 3466243
            received: 3
            sent: 3
            stdDevNanoseconds: 1555652
            totalTimeNanoseconds: 17347780
          name: ping-system-leaf11-10.46.99.34
          success: true
        - details:
            averageTimeNanoseconds: 4889455
            maxTimeNanoseconds: 5200816
            minTimeNanoseconds: 4650883
            received: 3
            sent: 3
            stdDevNanoseconds: 282099
            totalTimeNanoseconds: 15415420
          name: ping-system-leaf13-10.46.99.34
          success: true
        - details:
            averageTimeNanoseconds: 7636149
            maxTimeNanoseconds: 8961390
            minTimeNanoseconds: 6473607
            received: 3
            sent: 3
            stdDevNanoseconds: 1251846
            totalTimeNanoseconds: 23869686
          name: ping-system-leaf11-10.46.99.32
          success: true
        - details:
            averageTimeNanoseconds: 7048913
            maxTimeNanoseconds: 9226398
            minTimeNanoseconds: 5607136
            received: 3
            sent: 3
            stdDevNanoseconds: 1918518
            totalTimeNanoseconds: 22189162
          name: ping-system-leaf12-10.46.99.35
          success: true
        - details:
            averageTimeNanoseconds: 6271170
            maxTimeNanoseconds: 7487181
            minTimeNanoseconds: 5559837
            received: 3
            sent: 3
            stdDevNanoseconds: 1058152
            totalTimeNanoseconds: 19935917
          name: ping-system-leaf11-10.46.99.33
          success: true
        - details:
            averageTimeNanoseconds: 6461501
            maxTimeNanoseconds: 7667273
            minTimeNanoseconds: 5654733
            received: 3
            sent: 3
            stdDevNanoseconds: 1063946
            totalTimeNanoseconds: 20295980
          name: ping-system-leaf12-10.46.99.33
          success: true
        - details:
            averageTimeNanoseconds: 8145697
            maxTimeNanoseconds: 9013546
            minTimeNanoseconds: 6576511
            received: 3
            sent: 3
            stdDevNanoseconds: 1361503
            totalTimeNanoseconds: 25217676
          name: ping-system-leaf11-fd00:fde8::99:32
          success: true
        - details:
            averageTimeNanoseconds: 5771167
            maxTimeNanoseconds: 6710480
            minTimeNanoseconds: 4601224
            received: 3
            sent: 3
            stdDevNanoseconds: 1073374
            totalTimeNanoseconds: 19479179
          name: ping-system-spine12-fd00:fde8::99:31
          success: true
        - details:
            averageTimeNanoseconds: 7168727
            maxTimeNanoseconds: 7937682
            minTimeNanoseconds: 6170828
            received: 3
            sent: 3
            stdDevNanoseconds: 905403
            totalTimeNanoseconds: 22177755
          name: ping-system-leaf12-fd00:fde8::99:33
          success: true
        - details:
            averageTimeNanoseconds: 5522008
            maxTimeNanoseconds: 5937602
            minTimeNanoseconds: 5264407
            received: 3
            sent: 3
            stdDevNanoseconds: 363344
            totalTimeNanoseconds: 17433108
          name: ping-system-leaf13-fd00:fde8::99:34
          success: true
        - details:
            averageTimeNanoseconds: 14531547
            maxTimeNanoseconds: 25759695
            minTimeNanoseconds: 6592502
            received: 3
            sent: 3
            stdDevNanoseconds: 9997947
            totalTimeNanoseconds: 44409977
          name: ping-system-spine11-fd00:fde8::99:35
          success: true
        - details:
            averageTimeNanoseconds: 5714881
            maxTimeNanoseconds: 6661003
            minTimeNanoseconds: 5105480
            received: 3
            sent: 3
            stdDevNanoseconds: 830631
            totalTimeNanoseconds: 17722611
          name: ping-system-leaf11-fd00:fde8::99:34
          success: true
        - details:
            averageTimeNanoseconds: 5253029
            maxTimeNanoseconds: 6230132
            minTimeNanoseconds: 4754764
            received: 3
            sent: 3
            stdDevNanoseconds: 846251
            totalTimeNanoseconds: 16246248
          name: ping-system-leaf12-fd00:fde8::99:35
          success: true
        - details:
            averageTimeNanoseconds: 6080806
            maxTimeNanoseconds: 7543035
            minTimeNanoseconds: 3879698
            received: 3
            sent: 3
            stdDevNanoseconds: 1940223
            totalTimeNanoseconds: 19022060
          name: ping-system-leaf13-fd00:fde8::99:35
          success: true
        - details:
            averageTimeNanoseconds: 5785009
            maxTimeNanoseconds: 6669773
            minTimeNanoseconds: 4821829
            received: 3
            sent: 3
            stdDevNanoseconds: 926464
            totalTimeNanoseconds: 17969893
          name: ping-system-leaf12-fd00:fde8::99:34
          success: true
        - details:
            averageTimeNanoseconds: 6664910
            maxTimeNanoseconds: 8562166
            minTimeNanoseconds: 4566891
            received: 3
            sent: 3
            stdDevNanoseconds: 2005189
            totalTimeNanoseconds: 21903241
          name: ping-system-leaf11-fd00:fde8::99:33
          success: true
    workflowStatus:
      stages:
        - name: Initializing
          state: Completed
        - name: collecting SystemInterface info
          state: Completed
        - name: building ping map
          state: Completed
        - name: pinging Ipv4
          state: Completed
          subflows:
            - group: oam.eda.nokia.com
              id: 27
              kind: Ping
              name: ping-system-leaf11-10.46.99.32-27
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 28
              kind: Ping
              name: ping-system-leaf12-10.46.99.35-28
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 29
              kind: Ping
              name: ping-system-leaf13-10.46.99.34-29
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 30
              kind: Ping
              name: ping-system-spine12-10.46.99.31-30
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 31
              kind: Ping
              name: ping-system-leaf12-10.46.99.34-31
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 36
              kind: Ping
              name: ping-system-spine11-10.46.99.35-36
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 34
              kind: Ping
              name: ping-system-leaf13-10.46.99.35-34
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 33
              kind: Ping
              name: ping-system-leaf11-10.46.99.34-33
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 32
              kind: Ping
              name: ping-system-leaf12-10.46.99.33-32
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 35
              kind: Ping
              name: ping-system-leaf11-10.46.99.33-35
              namespace: eda
              version: v1
        - name: pinging Ipv6
          state: Completed
          subflows:
            - group: oam.eda.nokia.com
              id: 37
              kind: Ping
              name: ping-system-spine12-fd00:fde8::99:31-37
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 38
              kind: Ping
              name: ping-system-leaf11-fd00:fde8::99:32-38
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 39
              kind: Ping
              name: ping-system-leaf12-fd00:fde8::99:33-39
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 40
              kind: Ping
              name: ping-system-leaf11-fd00:fde8::99:34-40
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 41
              kind: Ping
              name: ping-system-leaf11-fd00:fde8::99:33-41
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 42
              kind: Ping
              name: ping-system-leaf13-fd00:fde8::99:35-42
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 46
              kind: Ping
              name: ping-system-spine11-fd00:fde8::99:35-46
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 44
              kind: Ping
              name: ping-system-leaf12-fd00:fde8::99:35-44
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 45
              kind: Ping
              name: ping-system-leaf12-fd00:fde8::99:34-45
              namespace: eda
              version: v1
            - group: oam.eda.nokia.com
              id: 43
              kind: Ping
              name: ping-system-leaf13-fd00:fde8::99:34-43
              namespace: eda
              version: v1
      state: Completed
    ```

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
