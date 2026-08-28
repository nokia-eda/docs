---
resource_name: EdgePing
resource_name_plural: edgepings
resource_name_plural_title: Edge Pings
resource_name_acronym: EP
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_edgepings.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Edge Ping

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `EdgePing` workflow is used to test service connectivity in a fully virtualized setup with testman `SimNode` containers. 

/// admonition | Warning
    type: warning

This workflow **cannot** be used in a hardware setup, nor is it capable of sending a ping from a network switch to a host. It can **only** be used to ping an IP from a testman `SimNode` container.

///


## Ping test types

This workflow supports three connectivity tests:

- `Edge` to ping from a single testman host to a single destination
- `Gateway` to ping from multiple testman hosts to the gateway IP address
- `EdgeMesh` to ping between multiple testman hosts

### Edge

This sends ping packets to a single destination, from a single source host. 

The number of ping messages being sent is `count * 1`. The following parameters must be specified:

- `interfaceResource`
- `vlanID`
- `destination`

/// details | Example
    type: example

```yaml
apiVersion: services.eda.nokia.com/v2
kind: EdgePing
metadata:
    name: edgeping-72d9e649-1758-4224-a073-e519f5265433
    namespace: eda
spec:
    count: 3
    pingType: Edge
    interfaceResource: leaf-2-ethernet-1-2-1
    vlanID: 100
    destination: 10.0.0.8
```

///

### Gateway

This sends ping packets from all hosts associated with a [`VLAN`](./vlan.md) or [`RoutedInterface`](./routedinterface.md) in a particular [`VirtualNetwork`](./virtualnetwork.md). The destination IP of the packets is the [`IRBInterface`](./irbinterface.md) gateway IP of the [`BridgeDomain`](./bridgedomain.md) associated with the [`VLAN`](./vlan.md), or the [`RoutedInterface`](./routedinterface.md) IP address. 

The number of ping messages is `count * num_hosts`, where `num_hosts` is the number of sub-interfaces created by the [`VirtualNetwork`](./virtualnetwork.md). The following parameters must be specified:

- `virtualNetwork`

/// details | Example
    type: example

```yaml
apiVersion: services.eda.nokia.com/v2
kind: EdgePing
metadata:
    name: edgeping-f63dc46a-2b02-4fea-a9ba-e712bb0992e9
    namespace: eda
spec:
    count: 3
    pingType: Gateway
    virtualNetwork: my-vnet
```

///

### EdgeMesh

This sends ping packets between all hosts associated with a [`VLAN`](./vlan.md) or [`RoutedInterface`](./routedinterface.md) in a particular [`VirtualNetwork`](./virtualnetwork.md).

The number of ping messages is `count * num_hosts * (num_hosts - 1) / 2`, where `num_hosts` is the number of sub-interfaces created by the [`VirtualNetwork`](./virtualnetwork.md). The following parameters must be specified:

- `virtualNetwork`

/// details | Example
    type: example

```yaml
apiVersion: services.eda.nokia.com/v2
kind: EdgePing
metadata:
    name: edgeping-147762ba-798d-4ef5-8c6a-8aace9cada04
    namespace: eda
spec:
    count: 3
    pingType: EdgeMesh
    virtualNetwork: my-vnet
```

///

## IP address assignment

When a [`VLAN`](./vlan.md) or [`RoutedInterface`](./routedinterface.md) is created, an `EdgeInterface` is created for every sub-interface. If the interface is connected to a testman `SimNode`, an IP address is configured with the relevant VLAN ID on that simulated node. This IP address is taken from a pool that matches the [`IRBInterface`](./irbinterface.md) or [`RoutedInterface`](./routedinterface.md).

If no [`IRBInterface`](./irbinterface.md) was found for the [`BridgeDomain`](./bridgedomain.md) that the [`VLAN`](./vlan.md) is connected to, the following default pools are used to assign IP addresses:

- IPv4: 10.0.0.0/16
- IPv6: fd12:3456:789a:0001:0000::/112

## Dependencies

### [`VirtualNetwork`](./virtualnetwork.md)

If the type of this ping is `EdgeMesh` or `Gateway`, the `virtualNetwork` property selects the [`VirtualNetwork`](./virtualnetwork.md) resource to find sub-interfaces attached to testman hosts. 

### [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-)

If the type of this ping is `Edge`, the `interfaceResource` property in combination with the `vlanID` selects the sub-interface attached to a testman host. 

## Referenced resources

No other resources are referenced by the `EdgePing` workflow.

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


/// details | Example execution
    type: example

```
apiVersion: services.eda.nokia.com/v2
kind: EdgePing
metadata:
  annotations:
    workflows.core.eda.nokia.com/id: '422'
    workflows.core.eda.nokia.com/root-workflow-group: services.eda.nokia.com
    workflows.core.eda.nokia.com/root-workflow-kind: EdgePing
    workflows.core.eda.nokia.com/root-workflow-name: edgeping-2607fb76-1b1b-4773-bf30-0305d5f4902d
    workflows.core.eda.nokia.com/root-workflow-namespace: eda
    workflows.core.eda.nokia.com/root-workflow-version: v2
    workflows.core.eda.nokia.com/state: Completed
    workflows.core.eda.nokia.com/username: admin
  name: edgeping-2607fb76-1b1b-4773-bf30-0305d5f4902d
  namespace: eda
spec:
  count: 9
  destination: 10.0.0.21
  interfaceResource: leaf-2-ethernet-1-2-1
  pingType: Edge
  vlanID: 100
status:
  result: >-
    Ping successful, 9 packets transmitted, 9 received:
    leaf-2-ethernet-1-2-1:100 -> 10.0.0.21
workflowStatus:
  stages:
    - name: Initializing
      state: Completed
    - name: pinging from testman
      state: Completed
  state: Completed
```
///

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
