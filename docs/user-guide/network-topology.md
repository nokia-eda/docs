# Network Topology

A network topology in a broader sense describes the network design on physical and logical levels. Be it a Clos, a Fat Tree or a Ring design, the topology is what inherently defines the network.

Like an arbitrary topology is defined by its nodes and links, the network topology in EDA is modelled with the [`TopoNode`][topoNode-crd] and [`TopoLink`][topoLink-crd] resources. The EDA topology nodes are represented by the devices in your network, and the topology links define the connectivity between them.

[topoNode-crd]: https://crd.eda.dev/toponodes.core.eda.nokia.com/v1
[topoLink-crd]: https://crd.eda.dev/topolinks.core.eda.nokia.com/v1
[topoBreakout-crd]: https://crd.eda.dev/topobreakouts.core.eda.nokia.com/v1

If you come here after finishing the [Getting Started][gs-guide] guide, you may remember the 3-node topology that the "Try EDA" setup comes with:

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='Physical topology', zoom="1.2", page=0) }}-

To represent this network topology in EDA the `TopoNode` and `TopoLink` resources must be created for each node and link in the network topology. Without network topology modelled with the respective topo resources, EDA cannot start managing the network devices.

Here is how the same 3-node topology is modelled with the `TopoNode` and `TopoLink` resources:

- For each device in the topology there is a corresponding [`TopoNode`][topoNode-crd]
- For each link between the nodes there is a corresponding [`TopoLink`][topoLink-crd] representing the inter-switch connections
- For each link from a node to an edge device (not shown in the diagram) there is a corresponding `TopoLink` representing the edge connections.[^1]
- For each interface breakout on the nodes there is a corresponding [`TopoBreakout`][topoBreakout-crd] resource[^2]

The diagram below illustrates how the topology resources represent the same network topology:

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', zoom='1.3', title='EDA topology modelled with TopoNode and TopoLink resources', page=1) }}-

Almost no difference with a physical topology, right? To see the topology diagram in EDA UI select **Topologies** in the left-hand menu and click on the **Physical** row in the table of topologies:

-{{image(url='https://gitlab.com/-/project/7617705/uploads/9164ee1abebbbbc48d5d1c2612de379b/CleanShot_2025-12-01_at_12.08.14.png')}}-

/// note | Digital Twin topology
The Network Topology is used to model both the physical network and its matching Digital Twin. The Digital Twin topology (also known as the simulation topology) is covered in more detail on the [Digital Twin](../digital-twin/index.md) page.
///

## Topology resources

The `TopoNode`, `TopoLink` and `TopoBreakout` resources in EDA make up the network topology that is used both by the real physical network and the [Digital Twin](../digital-twin/index.md). With the 3-node topology created in the EDA cluster you can see these resources in the EDA UI and using `kubectl` or `edactl`:

/// tab | EDA UI

//// tab | TopoNode
TopoNodes are displayed in the EDA UI under **Targets** > **Nodes**:

-{{ image(url='https://gitlab.com/-/project/7617705/uploads/e5ff11d9eaf3ba68d5de001dad67218b/CleanShot_2025-11-28_at_13.32.19.png') }}-
////
//// tab | TopoLink
And to see the TopoLinks go to **Topology** > **Links**:

-{{ image(url='https://gitlab.com/-/project/7617705/uploads/c268a1a73556ec73677b6468450393d0/CleanShot_2025-11-28_at_13.36.12.png') }}-
////
///
/// tab | `kubectl`

TopoNodes:

```bash
kubectl -n eda get toponodes
```

<div class="embed-result">
```{.text .no-select .no-copy}
NAME     PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE     AGE
leaf1    7220 IXR-D3L   25.10.1   srl   true        normal   Connected   Synced   21m
leaf2    7220 IXR-D3L   25.10.1   srl   true        normal   Connected   Synced   21m
spine1   7220 IXR-D5    25.10.1   srl   true        normal   Connected   Synced   21m
```
</div>
TopoLinks:

```bash
kubectl -n eda get topolinks
```

<div class="embed-result">
```{.text .no-select .no-copy}
NAME                 AGE
leaf1-2-e1212        21m
leaf1-e1011          21m
leaf1-ethernet-1-3   21m
leaf1-ethernet-1-4   21m
leaf1-ethernet-1-5   21m
leaf1-ethernet-1-6   21m
leaf1-ethernet-1-7   21m
leaf1-ethernet-1-8   21m
leaf1-ethernet-1-9   21m
leaf1-spine1-1       21m
leaf1-spine1-2       21m
leaf2-e1011          21m
leaf2-ethernet-1-3   21m
leaf2-ethernet-1-4   21m
leaf2-ethernet-1-5   21m
leaf2-ethernet-1-6   21m
leaf2-ethernet-1-7   21m
leaf2-ethernet-1-8   21m
leaf2-ethernet-1-9   21m
leaf2-spine1-1       21m
leaf2-spine1-2       21m
```
</div>
///

If the `TopoNode`, `TopoLink` and `TopoBreakout` objects make up a topology, how do we create them?  
A straightforward way is to create these resources directly, either in UI or using CLI tools or API, but this is going to be a tedious and likely an error-prone process as the number of nodes and especially links may grow quickly.

To assist with the topology creation, EDA provides the Network Topology Workflow - a workflow to define and deploy arbitrary topologies in a transactional manner.

## Network topology workflow

Instead of creating the topology resources individually, EDA provides a way to describe the topology via the Network Topology workflow that can be triggered via UI, REST API, or via CLIs and applied in a single transaction.

> A Workflow in EDA is a resource that defines a job or a set of jobs to be executed in a run-to-completion manner. A typical example of a workflow is the Image Upgrade workflow that performs the upgrade of a network device OS image.

Let's look at the structure of Network Topology Workflow resource and how the Try EDA topology is defined with it:

/// tab | Network Topology workflow structure

```yaml
apiVersion: topologies.eda.nokia.com/v1alpha1
kind: NetworkTopology
metadata:
  name: try-eda-topology
  namespace: eda
spec:
  operation: create  # operation to perform

  nodeTemplates: []     # list of node templates
  nodes: []             # list of nodes 

  linkTemplates: []     # list of link templates
  links: []             # list of links

  breakoutTemplates: [] # list of breakout templates
  breakouts: []         # list of breakouts

  simulation: {}        # digital twin topology settings
  checks: {}            # topology checks and dry runs
```

///
/// tab | Try EDA topology workflow
The three-node topology used in the Try EDA setup is defined with the following Network Topology workflow:

```{.yaml .code-scroll-sm}
--8<-- "docs/user-guide/try-eda-topo.yaml"
```

///

As per the structure, the Network Topology workflow resource spec uses the template-based approach to define nodes, links and breakouts. Corresponding templates are defined in the `nodeTemplates`, `linkTemplates` and `breakoutTemplates` sections, and then referenced in the `nodes`, `links` and `breakouts` sections, respectively.

Using the template-based approach reduces repetition in the topology definition and lets users quickly change the common parameters in one place.

/// note
This document does not dive into the details of the Digital Twin topology (`simulation` section) as this topic is covered on the [Digital Twin](../digital-twin/index.md) page.
///

### Nodes

To define the nodes, create one or more templates and reference them in the `nodes` section. The values specified on the node level override the template values.

```yaml
nodeTemplates:
  - name: leaf #(1)!
    nodeProfile: srlinux-ghcr--{{ srl_version }}- #(5)!
    platform: 7220 IXR-D3L #(4)!
    labels: #(2)!
      eda.nokia.com/security-profile: managed #(6)!
      eda.nokia.com/role: leaf

nodes:
  - name: leaf1 #(7)!
    template: leaf #(3)!
    labels:
      new-node-level-label: new-value #(8)!
```

1. The free-form name of the node template resource.
2. The labels to be applied to the node.
3. The name of the node template that this node is based on.
4. Platform name.  
    NPP and Bootstrap server validate the platform name they see upon connection.
5. Node profile.  
    A reference to a [`NodeProfile`][nodeprofile-crd] resource that defines the profile of the node.
6. A label that is used by the `NodeSecurityProfile` resource to determine the security profile of the node.
7. The name of the node.
8. Parameters specified on the node level override/merge with the template values. In this case, a new label is merged with the template-level labels.

[nodeprofile-crd]: https://crd.eda.dev/nodeprofiles.core.eda.nokia.com/v1

Based on the provided node definition, EDA will create the respective `TopoNode` resource representing the node in the topology.

```yaml title="leaf1 TopoNode"
apiVersion: core.eda.nokia.com/v1
kind: TopoNode
metadata:
  labels:
    eda.nokia.com/role: leaf
    eda.nokia.com/security-profile: managed
    new-node-level-label: new-value
  name: leaf1
  namespace: eda
spec:
  nodeProfile: srlinux-ghcr--{{ srl_version }}-
  npp:
    mode: normal
  onBoarded: true
  operatingSystem: srl
  platform: 7220 IXR-D3L
  productionAddress: {}
  version: -{{ srl_version }}-
status:
  node-details: 10.244.0.224:57400
  node-state: Synced
  npp-details: 10.244.0.75:50057
  npp-pod: eda-npp-1
  npp-state: Connected
  operatingSystem: srl
  platform: 7220 IXR-D3L
  simulate: true
  version: -{{ srl_version }}-
```

### Links

A link represents a connection between two nodes in the topology. In EDA, you will find two link types used in the context of a network topology:

1. **interSwitch** - a link between two topology nodes, typically representing a connection between two network devices.
2. **edge** - a link connecting a topology node to an edge device that is not part of the topology. Most often the access links from the leaf switches to the end devices (servers, workstations, etc.) are modelled as edge links.

To define the links, create one or more link templates and reference them in the `links` section. The values specified on the link level override the template values.

The following examples show common topology link definitions that you will find in the Network Topology workflow spec:

//// tab | Inter switch link

An inter switch link (ISL) is a point-to-point link that connects two network devices in the topology. In the example below, the ISL connects `leaf1` and `spine1` nodes using their `ethernet-1-1` interfaces.

////// admonition | Diagram
    attrs: {class: inline end subtle-note}
-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='Click to zoom in', page='2', zoom='2') }}-
//////

```yaml
linkTemplates:
  - name: isl #(6)!
    type: interSwitch #(5)!
    speed: 25G #(7)!
    encapType: "null"
    labels: #(2)!
      eda.nokia.com/role: interSwitch

links:
  - name: leaf1-spine1-1 #(1)!
    template: isl #(9)!
    endpoints: #(8)!
      - local: #(3)!
          node: leaf1
          interface: ethernet-1-1
        remote: #(4)!
          node: spine1
          interface: ethernet-1-1

```

1. The name of the `TopoLink` resource.
2. The labels to be applied to the node.
3. Definition of Local, or "A" endpoint of the link. Can contain the following fields:  
   `interface` - Normalized name of the interface/port, e.g. `ethernet-1-1`.  
   `node` - The reference to the `TopoNode` resource that this side of a link is connected to.
4. Definition of Remote, or "B" endpoint of the link. Contains the same fields as the `local` definition.
5. The type of link. One of `edge`, `interSwitch`, `loopback`
6. Name of the link template.
7. Default link speed. Optional.
8. Endpoints is a list of endpoint definitions, where each endpoint object contains the `local` and optionally the `remote` sides.  
    For a typical inter-switch link both `local` and `remote` sides are defined, where the `local` side refers to one topology node and the `remote` side refers to another.  
    You will see how edge links don't have a `remote` side defined in the next example.
9. Reference to the link template that this link is based on.

As a result of this link definition, EDA will create two resources - a `TopoLink` resource representing the link itself, and two `Interface` resources representing the interfaces on both ends of the link. The `Interface` resources will be responsible for configuring the respective interfaces on the devices.

/// tab | TopoLink

```yaml
apiVersion: core.eda.nokia.com/v1
kind: TopoLink
metadata:
  labels:
    eda.nokia.com/role: interSwitch
    eda.nokia.com/source-link: leaf1-spine1-1
  name: leaf1-spine1-1
  namespace: eda
spec:
  links:
    - local:
        interface: ethernet-1-1
        interfaceResource: leaf1-ethernet-1-1
        node: leaf1
      remote:
        interface: ethernet-1-1
        interfaceResource: spine1-ethernet-1-1
        node: spine1
      speed: 25G
      type: interSwitch
status:
  members:
    - interface: ethernet-1-1
      node: leaf1
      operationalState: up
    - interface: ethernet-1-1
      node: spine1
      operationalState: up
  operationalState: up
```

///
/// tab | Interface
//// tab | Leaf1 ethernet-1-1

```yaml
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Interface
metadata:
  labels:
    eda.nokia.com/role: interSwitch
    eda.nokia.com/source-link: leaf1-spine1-1
  name: leaf1-ethernet-1-1
  namespace: eda
spec:
  enabled: true
  encapType: 'null'
  ethernet:
    stormControl: {}
  lldp: true
  members:
    - enabled: true
      interface: ethernet-1-1
      lacpPortPriority: 32768
      node: leaf1
  type: interface
status:
  enabled: true
  lastChange: '2025-11-28T12:08:22.671Z'
  members:
    - enabled: true
      interface: ethernet-1-1
      lastChange: '2025-11-28T12:08:22.671Z'
      neighbors:
        - interface: ethernet-1/1
          node: spine1
      node: leaf1
      nodeInterface: ethernet-1/1
      operationalState: up
      speed: 100G
  operationalState: up
  speed: 100G
```

////
//// tab | Spine1 ethernet-1-1

```yaml
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Interface
metadata:
  labels:
    eda.nokia.com/role: interSwitch
    eda.nokia.com/source-link: leaf1-spine1-1
  name: spine1-ethernet-1-1
  namespace: eda
spec:
  enabled: true
  encapType: 'null'
  ethernet:
    stormControl: {}
  lldp: true
  members:
    - enabled: true
      interface: ethernet-1-1
      lacpPortPriority: 32768
      node: spine1
  type: interface
status:
  enabled: true
  lastChange: '2025-11-28T12:08:22.667Z'
  members:
    - enabled: true
      interface: ethernet-1-1
      lastChange: '2025-11-28T12:08:22.667Z'
      neighbors:
        - interface: ethernet-1/1
          node: leaf1
      node: spine1
      nodeInterface: ethernet-1/1
      operationalState: up
      speed: 400G
  operationalState: up
  speed: 400G
```

////
///

////

//// tab | Edge link

The edge link is a link that connects a topology node (typically a leaf switch) to an edge device that is not part of the topology. The edge device may be a server, a GPU, or a generic device that is not managed by EDA. As this link has only one side connected to a topology node, only the `local` side is defined in the link definition:

////// admonition | Diagram
    attrs: {class: inline end subtle-note}
-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='Click to zoom in', page='3', zoom='2') }}-
//////

```yaml
linkTemplates:
  - name: edge
    type: edge #(1)!
    encapType: dot1q
    labels:
      eda.nokia.com/role: edge #(2)!

links:
  - name: leaf1-ethernet-1-3
    template: edge
    endpoints:
      - local:
          node: leaf1
          interface: ethernet-1-3
```

1. Edge links have their own special type - `edge`.
2. The label is optional, but since the edge links are targeted by the overlay services like Virtual Network, it's a good practice to label them accordingly so that these applications can easily select the edge links.

As a result of this link definition, EDA will create two resources - a `TopoLink` resource representing the link itself, and the `Interface` resource representing the interfaces on the leaf side. The `Interface` resources will be responsible for configuring the respective interface on the leaf device.

/// tab | TopoLink

```yaml
apiVersion: core.eda.nokia.com/v1
kind: TopoLink
metadata:
  labels:
    eda.nokia.com/role: edge
    eda.nokia.com/source-link: leaf2-ethernet-1-3
  name: leaf2-ethernet-1-3
  namespace: eda
spec:
  links:
    - local:
        interface: ethernet-1-3
        interfaceResource: leaf2-ethernet-1-3
        node: leaf2
      remote:
        interfaceResource: ''
        node: ''
      type: edge
status:
  members:
    - interface: ethernet-1-3
      node: leaf2
      operationalState: up
  operationalState: up
```

///
/// tab | Interface

```yaml
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Interface
metadata:
  labels:
    eda.nokia.com/role: edge
    eda.nokia.com/source-link: leaf1-ethernet-1-3
  name: leaf1-ethernet-1-3
  namespace: eda
spec:
  enabled: true
  encapType: dot1q
  ethernet:
    stormControl: {}
  lldp: true
  members:
    - enabled: true
      interface: ethernet-1-3
      lacpPortPriority: 32768
      node: leaf1
  type: interface
status:
  enabled: true
  lastChange: '2025-11-28T12:08:22.795Z'
  members:
    - enabled: true
      interface: ethernet-1-3
      lastChange: '2025-11-28T12:08:22.795Z'
      neighbors: []
      node: leaf1
      nodeInterface: ethernet-1/3
      operationalState: up
      speed: 100G
  operationalState: up
  speed: 100G
```

///

////

//// tab | Local LAG

The Link Aggregation Group (LAG) link combines multiple physical interfaces into a single logical link. In EDA, two types of LAG exist: local LAG and multihomed LAG.

The "local" LAG aggregates ports **between a single pair** of nodes and is created by specifying multiple endpoints each having only **local** sides defined on the **same node**. In the example below, the LAG will consist of `ethernet-1-10` and `ethernet-1-11` interfaces on the `leaf1` node reaching out to an edge device that is expected to have a matching LAG configuration.

////// admonition | Diagram
    attrs: {class: inline end subtle-note}
-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='Click to zoom in', page='4', zoom='2') }}-
//////

```yaml
linkTemplates:
  - name: edge
    type: edge
    encapType: dot1q
    labels:
      eda.nokia.com/role: edge

links:
  - name: leaf1-e1011
    template: edge
    endpoints:
      - local:
          node: leaf1 #(1)!
          interface: ethernet-1-10
      - local:
          node: leaf1
          interface: ethernet-1-11
```

1. Both endpoints in this example refer to the same node - `leaf1`, indicating that this is a local LAG link, where both interfaces are belonging to the same node.

As a result of this link definition, EDA will create two resources - a `TopoLink` resource representing the link itself, and **only one** `Interface` resource with two members in it representing the local LAG.

Also note, that the `Interface` resource also features LAG-specific configuration under the `lag` section in its spec.

/// tab | TopoLink

```{.yaml .code-scroll-lg}
apiVersion: core.eda.nokia.com/v1
kind: TopoLink
metadata:
  labels:
    eda.nokia.com/role: edge
    eda.nokia.com/source-link: leaf1-e1011
  name: leaf1-e1011
  namespace: eda
spec:
  links:
    - local:
        interface: ethernet-1-10
        interfaceResource: lag-leaf1-e1011-local
        node: leaf1
      remote:
        interfaceResource: ''
        node: ''
      type: edge
    - local:
        interface: ethernet-1-11
        interfaceResource: lag-leaf1-e1011-local
        node: leaf1
      remote:
        interfaceResource: ''
        node: ''
      type: edge
status:
  members:
    - interface: ethernet-1-10
      node: leaf1
      operationalState: up
    - interface: ethernet-1-11
      node: leaf1
      operationalState: up
  operationalState: up
```

///
/// tab | Interface

```{.yaml .code-scroll-lg}
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Interface
metadata:
  labels:
    eda.nokia.com/role: edge
    eda.nokia.com/source-link: leaf1-e1011
  name: lag-leaf1-e1011-local
  namespace: eda
spec:
  enabled: true
  encapType: dot1q
  ethernet:
    stormControl: {}
  lag:
    lacp:
      interval: fast
      lacpFallback:
        mode: static
        timeout: 60
      mode: active
      systemPriority: 32768
    minLinks: 1
    multihoming:
      esi: auto
      mode: all-active
      reloadDelayTimer: 100
      revertive: false
    type: lacp
  lldp: true
  members:
    - enabled: true
      interface: ethernet-1-10
      lacpPortPriority: 32768
      node: leaf1
    - enabled: true
      interface: ethernet-1-11
      lacpPortPriority: 32768
      node: leaf1
  type: lag
status:
  enabled: true
  lag:
    adminKey: 2
    systemIdMac: FE:2F:AA:00:00:02
  lastChange: '2025-11-28T12:08:25.692Z'
  members:
    - enabled: true
      interface: ethernet-1-10
      lastChange: '2025-11-28T12:08:25.674Z'
      neighbors: []
      node: leaf1
      nodeInterface: ethernet-1/10
      operationalState: up
      speed: 100G
    - enabled: true
      interface: ethernet-1-11
      lastChange: '2025-11-28T12:08:25.692Z'
      neighbors: []
      node: leaf1
      nodeInterface: ethernet-1/11
      operationalState: up
      speed: 100G
    - enabled: true
      interface: lag-2
      lastChange: '2025-11-28T12:08:25.675Z'
      neighbors: []
      node: leaf1
      nodeInterface: lag2
      operationalState: up
      speed: 200G
  operationalState: up
  speed: 200G

```

///

////

//// tab | Multihome LAG

In contrast to the local LAG, the multihome LAG aggregates ports from a single node **towards two and more** nodes. A typical application of a multihome LAG is the ESI LAG in EVPN deployments where up to four switches connect to the same downstream device (e.g. server or a router) using a LAG.

The multihome LAG is created by specifying multiple endpoints each having only **local** sides defined for **different nodes**. Like in the example below, the multihome LAG will consist of `ethernet-1-12` on the `leaf1` and same `ethernet-1-12` on the `leaf2` node.

////// admonition | Diagram
    attrs: {class: inline end subtle-note}
-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='Click to zoom in', page='5', zoom='2') }}-
//////

```yaml
linkTemplates:
  - name: edge
    type: edge
    encapType: dot1q
    labels:
      eda.nokia.com/role: edge

links:
  - name: leaf1-2-e1212
    template: edge
    endpoints:
      - local:
          node: leaf1 #(1)!
          interface: ethernet-1-12
      - local:
          node: leaf2
          interface: ethernet-1-12
```

1. In contrast to the local LAG example, here the `local` sides of the endpoint object refer to different nodes - `leaf1` and `leaf2`. This denotes the "multihome" nature of this LAG link.

As a result of this link definition, EDA will create two resources - a `TopoLink` resource representing the link itself, and **only one** `Interface` resource with two members where each member belongs to a different node.

Also note, that the `Interface` resource also features LAG-specific configuration under the `lag` section in its spec.

/// tab | TopoLink

```{.yaml .code-scroll-lg}
apiVersion: core.eda.nokia.com/v1
kind: TopoLink
metadata:
  labels:
    eda.nokia.com/role: edge
    eda.nokia.com/source-link: leaf1-2-e1212
  name: leaf1-2-e1212
  namespace: eda
spec:
  links:
    - local:
        interface: ethernet-1-12
        interfaceResource: lag-leaf1-2-e1212-local
        node: leaf1
      remote:
        interfaceResource: ''
        node: ''
      type: edge
    - local:
        interface: ethernet-1-12
        interfaceResource: lag-leaf1-2-e1212-local
        node: leaf2
      remote:
        interfaceResource: ''
        node: ''
      type: edge
status:
  members:
    - interface: ethernet-1-12
      node: leaf1
      operationalState: up
    - interface: ethernet-1-12
      node: leaf2
      operationalState: up
  operationalState: up

```

///
/// tab | Interface

```{.yaml .code-scroll-lg}
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Interface
metadata:
  labels:
    eda.nokia.com/role: edge
    eda.nokia.com/source-link: leaf1-2-e1212
  name: lag-leaf1-2-e1212-local
  namespace: eda
spec:
  enabled: true
  encapType: dot1q
  ethernet:
    stormControl: {}
  lag:
    lacp:
      interval: fast
      lacpFallback:
        mode: static
        timeout: 60
      mode: active
      systemPriority: 32768
    minLinks: 1
    multihoming:
      esi: auto
      mode: all-active
      reloadDelayTimer: 100
      revertive: false
    type: lacp
  lldp: true
  members:
    - enabled: true
      interface: ethernet-1-12
      lacpPortPriority: 32768
      node: leaf1
    - enabled: true
      interface: ethernet-1-12
      lacpPortPriority: 32768
      node: leaf2
  type: lag
status:
  enabled: true
  lag:
    adminKey: 3
    systemIdMac: FE:2F:AA:00:00:03
  lastChange: '2025-11-28T12:08:27.578Z'
  members:
    - enabled: true
      interface: ethernet-1-12
      lastChange: '2025-11-28T12:08:25.697Z'
      neighbors: []
      node: leaf1
      nodeInterface: ethernet-1/12
      operationalState: up
      speed: 100G
    - enabled: true
      interface: lag-1
      lastChange: '2025-11-28T12:08:25.697Z'
      neighbors: []
      node: leaf1
      nodeInterface: lag1
      operationalState: up
      speed: 100G
    - enabled: true
      interface: ethernet-1-12
      lastChange: '2025-11-28T12:08:27.577Z'
      neighbors: []
      node: leaf2
      nodeInterface: ethernet-1/12
      operationalState: up
      speed: 100G
    - enabled: true
      interface: lag-2
      lastChange: '2025-11-28T12:08:27.578Z'
      neighbors: []
      node: leaf2
      nodeInterface: lag2
      operationalState: up
      speed: 100G
  operationalState: up
  speed: 100G

```

///

////

### Breakouts

Breakouts allow splitting a high-speed interface into multiple lower-speed channels, like a 400G port on Nokia SR Linux 7220 IXR-H4 can be broken out into multiple lower speed interfaces, e.g. 4 by 100G. To model port breakouts in EDA, the [`TopoBreakout`][topoBreakout-crd] resource is used. And to define the port breakouts, the familiar template-based approach is implemented in the Network Topology workflow.

While the "Try EDA 3-node topology" does not feature breakout ports, the example below will take a similar topology with two leafs and one spine, where the `ethernet-1-1` interface on `spine1` is broken down to four 100G interfaces to which the leafs connect.

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='', page='6', zoom='1.8') }}-

The breakout template sets the number of channels and speed per channel, and the breakout definition references the template and specifies the nodes and interfaces where the breakout should be applied. In the example below only `spine1/ethernet-1-1` is broken out, but you can define nodes and interfaces on them as needed.

```{.yaml .code-scroll-lg}
breakoutTemplates:
  - name: 4x100
    channels: 4
    speed: 100G
breakouts:
  - name: breakouts
    template: 4x100
    node:
      - spine1
    interface:
      - ethernet-1-1

links:
  - name: leaf1-spine1-1
    template: isl
    endpoints:
      - local:
          node: leaf1
          interface: ethernet-1-1
        remote:
          node: spine1
          interface: ethernet-1-1-1 #(1)!
  - name: leaf1-spine1-2
    template: isl
    endpoints:
      - local:
          node: leaf1
          interface: ethernet-1-2
        remote:
          node: spine1
          interface: ethernet-1-1-2
  - name: leaf2-spine1-1
    template: isl
    endpoints:
      - local:
          node: leaf2
          interface: ethernet-1-1
        remote:
          node: spine1
          interface: ethernet-1-1-3
  - name: leaf2-spine1-2
    template: isl
    endpoints:
      - local:
          node: leaf2
          interface: ethernet-1-2
        remote:
          node: spine1
          interface: ethernet-1-1-4
```

1. Note, how the interface name of a port that is broken out is represented in a normalized way with its channel suffix - `ethernet-1-1-1`, `ethernet-1-1-2`, etc.

The above breakout definition will result in creation of the two identical resources - `TopoBreakout` and `Breakout`. The `TopoBreakout` won't be visible in the EDA UI while the `Breakout` resource can be seen in the **Topology** > **Breakouts** section.

```yaml
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Breakout
metadata:
  name: breakouts
  namespace: breakout-test
spec:
  channels: 4
  interface:
    - ethernet-1-1
  node:
    - spine1
  speed: 100G
```

## Topology operations

Now that you are familiar with how nodes, links, and breakouts are defined in the Network Topology workflow, let's see how to create, modify, and remove Network Topologies in EDA.

Since Network Topology is a resource backed by the workflow it can be triggered via UI, REST API, CLIs and anything that can create a resource in EDA.

-{{video(url="https://gitlab.com/-/project/7617705/uploads/b17e9b8eda20991e79a2d0c79afda301/eda-nt-ui.mp4", title="Network Topology Workflow in EDA UI")}}-

Regardless of the method used to create the Network Topology resource, a user would need to fill in the network topology resources as explained in the previous sections and select the desired operation - `create`, `replace`, or `delete`. Let's see what each operation does.

To demonstrate the effects of each operation, let's create an empty namespace `net-topo-test` where we will deploy and modify the topology in the examples below.

```bash
edactl namespace bootstrap create --from-namespace eda net-topo-test #(1)!
```

1. Don't have `edactl` installed? [It is one command away](using-the-clis.md#edactl).

/// admonition | Workflow names
    type: subtle-note
Workflow resources should have unique names within a namespace. When creating a new workflow in EDA UI the name is auto-generated, and when using `kubectl` users can leverage Kubernetes' `generateName` feature to create unique names. In the examples below we will use `generateName` field with `kubectl` snippets instead of providing a fixed name.
///

### Create

To create a Network Topology select the `create` operation in the Network Topology workflow spec. Create operation will error if any of the topology resources already exist in the target namespace, therefore it is suitable for either creating a new topology in an empty namespace, or adding new nodes and links to an existing topology without modifying the existing resources.

Since our brand new `net-topo-test` namespace is empty, we can safely create the topology there, using the following workflow:

/// tab | Topology

```yaml hl_lines="7"
--8<-- "docs/user-guide/network-topology/snippets/create.yaml"
```

1. The `generateName` field is used to let Kubernetes generate a unique name for the workflow resource and is only applicable for cases when the workflow resource is created with `kubectl`. If you were to paste this snippet in the EDA UI, you would need to replace this field with the `name: some-unique-name` field.

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/create.yaml"
EOF
```

///
You should expect the workflow created for this topology to complete and two nodes and one link to be created in the `net-topo-test` namespace.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/0389b3291f78e76a0fa37eee26a68adc/CleanShot_2025-11-30_at_23.27.29.png")}}-

Because the `create` operation adds new topology resources without modifying the existing ones, it is possible to use it to incrementally add new nodes and links to an existing topology. For example, if we wanted to add a new node `node3` and connect it to `node1`, we could create a new workflow with the `create` operation and provide the new node and its links in the spec.

/// tab | Topology

```yaml hl_lines="7"
--8<-- "docs/user-guide/network-topology/snippets/add.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/add.yaml"
EOF
```

///

The result of running this workflow will be that `node3` is added to the existing topology along with its link to `node1`, while `node1` and `node2` remain unchanged.

### Replace

Replace operation is used to replace the existing topology with a new one and it comes in two variants - `replace` and `replaceAll`.

When using `replace` operation, the workflow will **only** replace the existing topology resources whose names match the ones defined in the workflow spec. Topology resources that exist in the target namespace but are not part of the new topology definition will be left unmodified. The example below demonstrates changing `node2` definition by adding the node-level platform value, overriding the template. The result of this replace operation will be that `node1` will remain unchanged, but `node2` will have its platform set to `7220 IXR-D2L`.

/// tab | Topology

```yaml hl_lines="7 20"
--8<-- "docs/user-guide/network-topology/snippets/replace-1.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/replace-1.yaml"
EOF
```

///
> Changing node-specific parameters like platform, operating system, version, etc. triggers re-onboarding of the node.

When using `replaceAll` operation, the workflow will first **remove all** topology resources from the targeted namespace and then add the resources defined in the workflow spec. This operation is useful when you want to completely replace the existing topology with a new one.

/// admonition | Danger
    type: danger
Running the workflow with the `replaceAll` operation will effectively delete all topology resources in the target namespace and create the new node and link objects as defined in the workflow spec. Use with caution to avoid unintentional topology changes.
///

The below example demonstrates how the previous topology with `node1` and `node2` is replaced with a new topology that consists of the three nodes - `switch1`, `switch2`, and `switch3`, and two links connecting them. As you can see, the names of the nodes are different, but this is not a problem, because the `replaceAll` operation removes all previous nodes and links and replaces them with the new ones.

/// tab | Topology

```yaml hl_lines="7"
--8<-- "docs/user-guide/network-topology/snippets/replaceAll-1.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/replaceAll-1.yaml"
EOF
```

///

### Delete

Use `delete` operation to remove named topology resources from the target namespace or `deleteAll` operation to remove all topology resources from the target namespace.

Continuing from the previous step where we had three nodes - `switch1`, `switch2`, and `switch3` - we can delete the `switch3` node by providing a workflow with the `delete` operation and specifying the name of the node and its link to be deleted.

/// tab | Topology

```yaml hl_lines="7"
--8<-- "docs/user-guide/network-topology/snippets/delete-1.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/delete-1.yaml"
EOF
```

///

To remove **all** topology resources from the target namespace, use the `deleteAll` with an empty spec:

/// tab | Topology

```yaml hl_lines="7"
--8<-- "docs/user-guide/network-topology/snippets/deleteAll-1.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/deleteAll-1.yaml"
EOF
```

///

Running this workflow will remove all topology resources from the `net-topo-test` namespace. No nodes will remain.

## Topology checks

Performing operations on the topology is a high-touch activity as removing or changing the nodes and links accidentally clearly impacts the network services running on top of the network. To reduce the risk of making accidental changes to the topology, the Network Topology workflow allows a user to run it in the Dry Run mode by setting the `.spec.checks.dryRun: true` field in the workflow spec.

With Dry Run enabled, the workflow will pause and ask for the user's confirmation before adding/removing or changing any of the topology resources.

To demonstrate how Dry Run works, we will create a workflow that uses the `replaceAll` operation to remove any existing topology and create a new one with just one `node1` node. The workflow definition is as follows:

/// tab | Topology

```yaml hl_lines="18-19"
--8<-- "docs/user-guide/network-topology/snippets/replaceAll-check.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/replaceAll-check.yaml"
EOF
```

///

Because the `replaceAll` operation translates to two actions:

1. Deleting all existing topology resources
2. Creating new topology resources

The workflow will pause two times, first asking to confirm the transaction that removes all existing topology elements and resources that were created for the nodes by EDA. After confirming this action, the workflow will proceed to the second pause where it will ask to confirm the creation of the new topology resources as a second transaction.  
The topology checks are implemented as a transaction in the Dry Run mode, hence you will be able to inspect the transaction details like for any other transaction in EDA.

The below video demonstrates how the Dry Run mode works in practice.

-{{video(url='https://gitlab.com/-/project/7617705/uploads/2d6af323ca96d821286e5badf37acf2a/checks.mp4')}}-

[gs-guide]: ../getting-started/try-eda.md

[^1]: Edge devices are not shown in the diagram because they are not (currently) managed by EDA and hence are not part of the topology. However, the links from the nodes to the edge devices must be modelled with `TopoLink` resources of type `edge` to allow EDA to manage these interfaces.

[^2]: Interface breakouts are not shown in the diagram because there are no breakouts defined in the "Try EDA" three-node topology. However, if there were any port breakouts on the nodes, they would be modelled with the `TopoBreakout` resources.

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>
