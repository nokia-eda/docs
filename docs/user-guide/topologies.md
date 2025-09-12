# Topologies

Topologies in EDA cover a lot of ground. Not only do they define the design of a physical or a virtual network used as a [Digital Twin](../digital-twin/index.md), they also drive the visualization of various overlays in the EDA UI.

Let's start with a familiar role of a topology - the network topology.

## Network topology

A network topology in a broader sense describes the network design. Be it a Clos, a Fat Tree or a Ring design, the topology is what inherently defines the network.

Like every topology is defined by its nodes and links, the EDA topology consists of node ([`TopoNode`][topoNode-crd]) and link ([`TopoLink`][topoLink-crd]) objects. The EDA topology nodes are represented by the devices in your network, and the topology links define the connectivity between them.

[topoNode-crd]: https://crd.eda.dev/toponodes.core.eda.nokia.com/v1
[topoLink-crd]: https://crd.eda.dev/topolinks.core.eda.nokia.com/v1

If you come here after finishing the [Getting Started][gs-guide] guide, you may remember the 3-node topology that we worked on:

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='Physical topology', page=0) }}-

In EDA, this topology is represented by the `TopoNode` and `TopoLink` objects mirroring the physical design:

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='EDA topology', page=1) }}-

Almost no difference with a physical topology, right?

/// admonition | Note
    type: subtle-note
The `TopoNode` and `TopoLink` objects in EDA make up the topology that can be backed by the Digital Twin or a real physical network.
///

If the `TopoNode` and `TopoLink` objects make up a topology, how do we create them?  
A straightforward way is to create these resources by hand, but this is going to be a tedious and likely an error-prone process.

To assist with the topology creation, EDA provides a couple of methods to generate the required topology resources based on an abstracted input:

1. Using a topology file
2. Using a topology generator

### Topology file

Instead of creating the topology resources individually, EDA provides a way to describe the topology nodes and links in a topology file. Based on the contents of this file EDA will create the [`TopoNode`][topoNode-crd], [`TopoLink`][topoLink-crd], [`Interface`][interface-crd] and [`TopoBreakout`][topoBreakout-crd] resources. This approach enables the users to define topologies in a declarative way.

[interface-crd]: https://crd.eda.dev/interfaces.interfaces.eda.nokia.com/v1alpha1
[topoBreakout-crd]: https://crd.eda.dev/topobreakouts.core.eda.nokia.com/v1

Let's have a look at the topology file structure and a snippet matching it.

/// tab | schema

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: eda-topology
data:
  eda.yaml: |
    items:
      - spec:
          nodes:
            - <TopoNode>

          links:
            - <TopoLink>

          breakouts:
            - <TopoBreakout>
```

///
/// tab | snippet

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: eda-topology
data:
  eda.yaml: |
    ---
    items:
      - spec:
          nodes:
            - name: leaf1
              labels:
                eda.nokia.com/role: leaf
                eda.nokia.com/security-profile: managed
              spec:
                operatingSystem: srl
                version: -{{ srl_version }}-
                platform: 7220 IXR-D3L
                nodeProfile: srlinux-ghcr--{{ srl_version }}-
            # remaining nodes omitted for brevity
          links:
            - name: leaf1-spine1-1
              labels:
                eda.nokia.com/role: interSwitch
              spec:
                links:
                  - local:
                      node: leaf1
                      interfaceResource: ""
                      interface: ethernet-1-1
                    remote:
                      node: spine1
                      interfaceResource: ""
                      interface: ethernet-1-1
                    type: interSwitch
            # remaining links omitted for brevity
```

///

As you can see, the topology file is provided as a ConfigMap Kubernetes resource with a predefined name - `eda-topology`. The `eda.yaml` data key is a YAML document that describes the topology and consists of the three lists: `nodes`, `links` and `breakouts`.  
Elements of these lists are modelled after the [`TopoNode`][topoNode-crd], [`TopoLink`][topoLink-crd], and [`TopoBreakout`][topoBreakout-crd] resources, respectively. Let's describe the fields you would typically use in these resources.

/// tab | TopoNode
The list of `TopoNode` elements will be used to create the `TopoNode` resources.

```yaml
name: leaf1 #(1)!
labels: #(2)!
  eda.nokia.com/role: leaf
  eda.nokia.com/security-profile: managed #(7)!
spec:
  operatingSystem: srl #(3)!
  version: -{{ srl_version }}- #(4)!
  platform: 7220 IXR-D3L #(5)!
  nodeProfile: srlinux-ghcr--{{ srl_version }}- #(6)!
```

1. The name of the `TopoNode` resource.
2. The labels to be applied to the node.
3. The operating system of the node. `srl` for Nokia SR Linux, `sros` for Nokia SR OS, `eos` for Arista EOS.
4. NOS software version.  
    NPP/BootstrapServer validate they see this version when connecting.
5. Platform name.  
    NPP/BootstrapServer validate they see this platform when connecting.
6. Node profile.  
    A reference to a `NodeProfile` resource that defines the profile of the node.
7. A label that is used by the `NodeSecurityProfile` resource to determine the security profile of the node.
///
/// tab | TopoLink
The list of `TopoLink` elements will be used to create the `TopoLink` resources.

TopoLink represents a logical link between two TopoNodes. It may
include more than one physical link to represent a LAG or a multihomed link.  

To create a point to point link with a single interface on both sides use a single link property.  
To create a point to point link with a LAG configured on both sides, use two links with matching nodes.  
A multihomed LAG is created by using two or more links where the local side and/or remote side can be different.  
Creating a link with only local side specified will create an edge interface.

The following examples show common topology link definitions:

//// tab | interSwitch link

```yaml
name: leaf1-spine1-1 #(1)!
labels: #(2)!
  eda.nokia.com/role: interSwitch
spec:
  links:
    - type: interSwitch #(5)!
      local: #(3)!
        node: leaf1
        interface: ethernet-1-1
      remote: #(4)!
        node: spine1
        interface: ethernet-1-1
```

1. The name of the `TopoLink` resource.
2. The labels to be applied to the node.
3. Definition of Local, or "A" endpoint of the link. Can contain the following fields:
    `interface` - Normalized name of the interface/port, e.g. ethernet-1-1.  
    `interfaceResource` - The reference to the existing `Interface` resource. If set to an empty string, the interface will be created.
    `node` - The reference to the `TopoNode` resource that this side of the link is connected to.
4. Definition of Remote, or "B" endpoint of the link. Contains the same fields as the `local` definition.
5. The type of link. One of `edge`, `interSwitch`, `loopback`
////

//// tab | edge link

```yaml
name: leaf1-ethernet-1-10
labels:
  eda.nokia.com/role: edge
encapType: dot1q
spec:
  links:
    - type: edge
      local:
        node: leaf1
        interface: ethernet-1-10
```

////

//// tab | Local LAG

The local LAG is created by specifying multiple local interfaces in the `links` section. Like in the example below, the LAG will consist of ethernet-1-10 and ethernet-1-11 interfaces on the `leaf1` node.

```yaml
name: leaf1-e1011
encapType: dot1q
labels:
  eda.nokia.com/role: edge
spec:
  links:
    - type: edge
      local:
        node: leaf1
        interface: ethernet-1-10
    - type: edge
      local:
        node: leaf1
        interface: ethernet-1-11
```

////

//// tab | Multihomed LAG

The multihomed LAG (ESI LAG in EVPN) is created by specifying multiple interfaces in the `links` section where the nodes are referring to different TopoNodes. Like in the example below, the multihomed LAG will consist of ethernet-1-12 on `leaf1` and `leaf2` nodes.

```yaml
name: leaf1-2-e1212
encapType: dot1q
labels:
  eda.nokia.com/role: edge
spec:
  links:
    - type: edge
      local:
        node: leaf1
        interface: ethernet-1-12
    - type: edge
      local:
        node: leaf2
        interface: ethernet-1-12
```

////
///
/// tab | TopoBreakout
The list of `TopoBreakout` elements will be used to create the Breakout resources that represent the interface breakout.

The example below shows how to define a breakout for ports ethernet-1-10 and ethernet-1-11 on the `leaf1` and `leaf2` nodes. The breakout will create 4 channels of 25G speed.

```yaml
nodes:
  - leaf1
  - leaf2
interface:
  - ethernet-1-10
  - ethernet-1-11
channels: 4
speed: 25G
```

///

#### Simplifying the topology file

Because the topology definition is a YAML-formatted document embedded in a standard ConfigMap resource, we can deal with the topology contents in a separate file and then embed it into the ConfigMap structure. You will see us using this method of defining topologies where a YAML file contains just the `items` list with the nodes, links and breakout elements, without the ConfigMap wrapping:

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='Topology YAML', page=1) }}-

> A topology YAML without the ConfigMap wrapping allows users to enjoy the YAML syntax highlighting and deal with less indentation.  
> This is exactly how the [3-node topology][3-node-topo-file] file is defined that we used in the [Getting Started guide][gs-guide].

The topology file structure may seem verbose with its nodes and links often having the same labels, OS type, version, etc. To reduce the repetition and ensure that the parameters are consistent across the topology resource, you may use YAML anchors and references. This way you can define a set of common parameters once and then reference them in each node or link definition.  
The snippet below shows how YAML anchors and references can be used to set the node and links parameters once and then reference them in the node and link definitions.

/// details | Using YAML anchors and references
    type: code-example

```yaml
# Common node labels
common_node_labels: &common_node_labels
  eda.nokia.com/security-profile: managed

leaf_labels: &leaf_labels
  <<: *common_node_labels
  eda.nokia.com/role: leaf

spine_labels: &spine_labels
  <<: *common_node_labels
  eda.nokia.com/role: spine

# Common srl node specs
srl_spec: &srl_spec
  operatingSystem: srl
  version: 25.3.2
  nodeProfile: srlinux-ghcr-25.3.2

srl_leaf_spec: &srl_leaf_spec
  <<: *srl_spec
  platform: 7220 IXR-D3L

srl_spine_spec: &srl_spine_spec
  <<: *srl_spec
  platform: 7220 IXR-D5

# Link labels
interswitch_labels: &interswitch_labels
  eda.nokia.com/role: interSwitch

edge_labels: &edge_labels
  eda.nokia.com/role: edge

####### TOPOLOGY #######
items:
  - spec:
      nodes:
        - name: leaf1
          labels:
            <<: *leaf_labels
          spec:
            <<: *srl_leaf_spec
        - name: leaf2
          labels:
            <<: *leaf_labels
          spec:
            <<: *srl_leaf_spec
        - name: spine1
          labels:
            <<: *spine_labels
          spec:
            <<: *srl_spine_spec

      links:
        - name: leaf1-spine1-1
          labels:
            <<: *interswitch_labels
          spec:
            links:
              - type: interSwitch
                local:
                  node: leaf1
                  interface: ethernet-1-1
                remote:
                  node: spine1
                  interface: ethernet-1-1
        - name: leaf1-spine1-2
          labels:
            <<: *interswitch_labels
          spec:
            links:
              - type: interSwitch
                local:
                  node: leaf1
                  interface: ethernet-1-2
                remote:
                  node: spine1
                  interface: ethernet-1-2
```

///

### Deploying Topology

To deploy a topology a user should take the following steps:

1. Create the ConfigMap resource named `eda-topology` in a k8s namespace matching the EDA namespace where you want to have the topology created.
2. Run the `api-server-topo` CLI command available in the Toolbox pod[^1] to apply the defined topology and make EDA create the `TopoNode`, `TopoLink`, `Interface` and `Breakout` resources based on the topology file contents.

/// admonition | Danger
    type: danger
Running the `api-server-topo` command will remove the `TopoNode`, `TopoLink`, `Interface` and `Breakout` resources that are not part of the new topology. This will effectively replace any existing node and link objects with the ones defined in the topology file being loaded.
///

To create the `eda-topology` ConfigMap resource with the topology file contents users can use the make target from the playground repository or a simple shell script that can work without cloning the playground repo.

/// tab | deploy with a make target

In the [Try EDA][gs-guide] setup the [3-node topology](https://github.com/nokia-eda/playground/blob/main/topology/3-nodes-srl.yaml) is created with calling the [`topology-load` make target][make-load-topo] that takes in the topology defined in the YAML file, adds it to the `eda-topology` ConfigMap in the `eda` namespace, and calls the `api-server-topo` CLI tool to apply the topology:

[make-load-topo]: https://github.com/nokia-eda/playground/blob/c8c6110cf118c88b8b8e7932b30fcda16fb94067/Makefile#L1117

```{.shell .no-select}
make TOPO=topology/3-nodes-srl.yaml topology-load
```

///
//// tab | deploy with a shell script
Some times the playground repository is not available on the same machine where the topology file is. In this case, users can add the script below to their environment and use it to load the topology file.  
It performs the same operations as the make target from the playground repository:

1. Wrap the topology file in the ConfigMap structure.
2. Create the `eda-topology` ConfigMap resource.
3. Run the `api-server-topo` CLI tool to apply the topology.

/// details | Loading topology YAML with shell script
    type: subtle-note

```bash title="load-topo.sh"
--8<-- "docs/user-guide/topo.sh"
```

///

With the script added to your current directory or `$PATH` you can run it to load a topology file:

```bash
bash topo.sh load my-topology.yaml
```

////

Both methods of deploying a topology rely on the `api-server-topo` tool available in the Toolbox[^1] pod. It reads the topology file from the `eda-topology` ConfigMap in a specified namespace and generates the following resources in EDA:

* `TopoNode` for each node in the topology.
* `TopoLink` for each link in the topology.
* `Interface` for each interSwitch and edge link in the topology.
* `Breakout` for each breakout defined in the topology.

One or more transactions will appear and once they succeed you will see the resources in your cluster and the topology diagram in the EDA UI.

### Removing Topology

By deploying an empty topology file you can remove the existing topology from EDA.

/// tab | remove with a make target
A handy make target is available in the playground repository to remove the existing topology:

```
make teardown-topology
```

The topology will be removed from the namespace set with the `EDA_USER_NAMESPACE` variable, or from the `eda` namespace if the variable is not set.
///
/// tab | remove with a script

The same script that is used to load the topology can be used to remove it. To remove a topology:

```bash
bash topo.sh remove
```

Path to the topology is not required as the empty topology is assumed for the `remove` operation.

///

Deploying an empty topology will remove all `TopoNode`, `TopoLink`, `Interface`, and `Breakout` resources in the specified namespace.

### Topology generation

Topology file provides a flexible way of defining `TopoNode` and `TopoLink` resources in a single document, but its flexibility in managing individual nodes and links leads to verbosity when defining larger topologies. For cookie-cutter topologies like Clos, a simpler abstraction can be used to define the topology in a more compact way and scalable way.

EDA Topology Generator allows users to define such an abstracted input in format of a JSON file that consists of layers. Each layer represents a set of nodes of the same role, and maps nicely to the tiers/stages of a Clos topology.  
The layers are then connected to each other based on the `NextLayerRole` field defined in each layer. This way, the uplinks of one layer connect to the downlinks of the next layer.

The example below should help clarify the layered structure and the definition of each field inside a layer.

```{.json .no-select .code-scroll-lg}
{
  "leaf": { //(1)!
    "NodeCount": 2, //(2)!
    "NodeLabels": {
      "eda.nokia.com/security-profile": "managed" //(18)!
    },
    "Platform": "7220 IXR-D3L", //(3)!
    "LayerRole": "leaf", //(4)!
    "NextLayerRole": "spine", //(5)!
    "Uplinks": 2, //(6)!
    "Downlinks": 2, //(7)!
    "GenerateEdge": true, //(10)!
    "EdgeEncapType": "dot1q", //(14)!
    "SlotCount": 1, //(8)!
    "PodId": "1", //(9)!
    "NodeProfile": "srlinux-ghcr--{{ srl_version }}-", //(11)!
    "Version": "-{{ srl_version }}-", //(12)!
    "OperatingSystem": "srl", //(13)!
    "RedundancyLabelsOdd": { //(15)!
      "eda.nokia.com/redundancy-group": "a"
    },
    "RedundancyLabelsEven": { //(16)!
      "eda.nokia.com/redundancy-group": "b"
    },
    "CanaryLabels": { //(17)!
      "eda.nokia.com/canary": "true"
    }
  },
  "spine": {
    "NodeCount": 1,
    "NodeLabels": {
      "eda.nokia.com/security-profile": "managed"
    },
    "Platform": "7220 IXR-H2",
    "LayerRole": "spine",
    "NextLayerRole": "superspine",
    "Uplinks": 2,
    "Downlinks": 4,
    "SlotCount": 1,
    "PodId": "1",
    "NodeProfile": "srlinux-ghcr--{{ srl_version }}-",
    "Version": "-{{ srl_version }}-",
    "OperatingSystem": "srl"
  }
}
```

1. A layer name. It is an arbitrary name of a layer, but it must be unique across the entire topology.
2. The number of nodes in the layer.
3. The platform of the node.
4. The layer role. An arbitrary string value, but often named after a topology stage, like `leaf`, `spine`, etc. The layer role is used in the `NextLayerRole` field to tie layers together.
5. The role of the next layer that this layer connects to.  
    In this example the `leaf` role has the `spine` role as the next layer, and hence the uplinks of the `leaf` layer will connect to the `spine` layer.
6. The number of uplinks each node in this layer has.
7. The number of downlinks each node in this layer has.
8. Used with chassis platforms, and will result in uplinks/downlinks being evenly distributed over line cards.
9. Pod ID groups layers into pods. Layers of the same pod make up a fabric and the pod ID becomes a TopoNode label that is leveraged by the Fabric app when dealing with multi-pod topologies.  
    Each pod is therefore a separate fabric and the topology generator input would be composed of multiple layer combinations with different pod IDs.
10. Indicating whether to generate Interface resources for the downlinks of the layer. This is typically the leaf layer that has no layer beneath it, and hence its downlinks are edge links.
11. The profile of the node.
12. The software version of the node.
13. The operating system of the node.
14. Sets the encapType value for any Interface resources generated as edge interfaces.
15. Labels on odd TopoNode generated within the layer.
16. Labels on even TopoNode generated within the layer.
17. Labels on the first TopoNode generated within the layer.
18. Security profile label that is used by the `NodeSecurityProfile` CR as a selector. The managed profile means the certificates for the nodes are managed by EDA.

This input defines a three node topology with one spine and two leaves. The nodes are automatically tagged with the respected labels and edge links are created for the leaf nodes.

EDA topology generator is implemented in the `edatopogen` binary that you can find in the `eda-toolbox` pod. Feel free to use the makefile in the playground repository to quickly connect to the `eda-toolbox` pod or create a handy alias for the toolbox to use it from anywhere.
/// tab | `toolbox` alias

```bash
alias edatoolbox='kubectl -n eda-system exec -it \
  $(kubectl get -n eda-system pods \
  -l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}") \
  -- env "TERM=xterm-256color" bash -l'
```

And then run `edatoolbox` to get a shell in the toolbox pod.

///
/// tab | make target from the playground repository
--8<-- "docs/user-guide/using-the-clis.md:open-toolbox"
///

Create a topology generator input file and name it something like `topo.json`. We will just copy the example used before:

```{.bash .code-scroll-sm}
cat <<EOF > topo.json
{
  "leaf": {
    "NodeCount": 2,
    "NodeLabels": {
      "eda.nokia.com/security-profile": "managed"
    },
    "Platform": "7220 IXR-D3L",
    "LayerRole": "leaf",
    "NextLayerRole": "spine",
    "Uplinks": 2,
    "Downlinks": 2,
    "SlotCount": 1,
    "PodId": "1",
    "GenerateEdge": true,
    "NodeProfile": "srlinux-ghcr--{{ srl_version }}-",
    "Version": "-{{ srl_version }}-",
    "OperatingSystem": "srl",
    "EdgeEncapType": "dot1q",
    "RedundancyLabelsOdd": {
      "eda.nokia.com/redundancy-group": "a"
    },
    "RedundancyLabelsEven": {
      "eda.nokia.com/redundancy-group": "b"
    },
    "CanaryLabels": {
      "eda.nokia.com/canary": "true"
    }
  },
  "spine": {
    "NodeCount": 1,
    "NodeLabels": {
      "eda.nokia.com/security-profile": "managed"
    },
    "Platform": "7220 IXR-H2",
    "LayerRole": "spine",
    "NextLayerRole": "superspine",
    "Uplinks": 2,
    "Downlinks": 4,
    "SlotCount": 1,
    "PodId": "1",
    "NodeProfile": "srlinux-ghcr--{{ srl_version }}-",
    "Version": "-{{ srl_version }}-",
    "OperatingSystem": "srl"
  }
}
EOF
```

Now, run the `edatopogen` binary to generate the topology file. Use the `-y` flag to instruct the generator to output the topology file directly in the ConfigMap format.

```bash
edatopogen -y -f topo.json
```

By default, this command generates a ConfigMap file named `generated_topo_pod_1.yaml`, where `pod_1` is the pod ID specified in the input file.

If you examine the generated file, you'll see that it contains the familiar topology file structure embedded within a ConfigMap resource.

Because `edatopogen` produces the ConfigMap resource directly, you can apply it to the cluster using `kubectl`:

```{.shell .no-select}
kubectl -n eda apply -f generated_topo_pod_1.yaml #(1)!
```

1. This command creates the ConfigMap with the topology file in the `eda` namespace. The `eda` namespace is a namespace where user resources are created.

Next, run the `api-server-topo` tool in the Toolbox pod[^1] to parse the topology ConfigMap and create the resources:

```{.shell .no-select}
api-server-topo -n eda
```

[gs-guide]: ../getting-started/try-eda.md
[3-node-topo-file]: https://github.com/nokia-eda/playground/blob/main/topology/3-nodes-srl.yaml

[^1]:
    The `api-server-topo` CLI tool is available in the `eda-toolbox` pod.

    --8<-- "docs/user-guide/using-the-clis.md:open-toolbox"

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>
