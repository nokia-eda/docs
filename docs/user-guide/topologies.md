---
srl_version: 24.10.1
---

# Topologies

Topologies in EDA cover a lot of ground. Not only they define the design of a physical or simulated network but also drive the visualization of various overlays in EDA UI.

Let's start with a familiar role of a topology - the network topology.

## Network topology

A network topology in a broader sense describes the network design. Be it a Clos, a Fat Tree or a Ring design, the topology is what inherently defines the network.

Like every topology is defined by its nodes and links, the EDA topology consists of the nodes (`TopoNode`) and links (`TopoLink`) objects. The EDA topology nodes are represented by the devices in your network, and the topology links define the relationships between them.

If you come here after finishing the [Getting Started][gs-guide] guide, you may remember the 3-node topology that we worked on:

-{{ diagram(url='hellt/tmp/diagrams/playground-topology.drawio', title='Physical topology', page=0) }}-

In EDA, this topology is represented by the `TopoNode` and `TopoLink` objects mirroring the physical design:

-{{ diagram(url='hellt/tmp/diagrams/playground-topology.drawio', title='EDA topology', page=1) }}-

Almost no difference with a physical topology, right?

/// admonition | Note
    type: subtle-note
Bear in mind, that the `TopoNode` and `TopoLink` objects that make up the topology are not specific to your digital twin network, for a physical topology the same objects are used to represent the devices and their links.
///

So if the `TopoNode` and `TopoLink` objects make up a topology, how do we create them?  
The obvious way is to create these Custom Resources manually, but this is going to be a tedious and likely error-prone process when carried out manually.

To assist with this process, EDA provides a couple of methods to generate the required `TopoNode` and `TopoLink` resources based on an abstracted input:

* using topology file
* or using topology generator

### Topology file

Instead of creating the `TopoNode` and `TopoLink` resources individually, EDA provides a way to describes the nodes and links of a topology in a topology file. Based on the contents of this file EDA will drive the creation of the `TopoNode` and `TopoLink` resources making it possible to create a topology in a declarative way from a single file.

Let's have a look at the topology file structure and a corresponding snippet of it that was used in the [quickstart topology][gs-guide-vnet]:

/// tab | schema

```yaml
---
items:
  - metadata:
    spec:
      nodes:
        - <TopoNode>

      links:
        - <TopoLink>
```

///
/// tab | snippet

```yaml
---
items:
  - metadata:
      namespace: default
    spec:
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

The top level of the topology file consists of the two arrays: `nodes` and `links`. Elements of these arrays are modelled after the `TopoNode` and `TopoLink` resources, respectively. Let's take an example of each kind and describe the fields you would typically set in them.

/// tab | TopoNode
The list of `TopoNode` elements will be used to create the `TopoNode` resources. You can use the fields of the `TopoNode` resource in the topology file, the following are the most common ones:

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
3. The operating system of the node. `srl` for Nokia SR Linux and `sros` for Nokia SR OS.
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

//// admonition | TopoLink resource
    type: subtle-note
TopoLink represents a logical link between two TopoNode. It may
include more than one physical link, being used to represent a
LAG or multihomed link.  
To create a point to point link with a
single interface on both sides use a single link property.  
To
create a point to point link with a LAG configured on both side,
use two links with matching nodes. A multihomed LAG is created
by using two or more links where the A side and/or B side can be
different.  
Creating a link with only A specified will create an
edge interface.
////

You can use the fields of the `TopoLink` resource in the topology file, like shown below:

```yaml
name: leaf1-spine1-1 #(1)!
labels: #(2)!
  eda.nokia.com/role: interSwitch
spec:
  links:
    - local: #(3)!
        node: leaf1
        interface: ethernet-1-1
        interfaceResource: ""
      remote: #(4)!
        node: spine1
        interface: ethernet-1-1
        interfaceResource: ""
      type: interSwitch #(5)!
```

1. The name of the `TopoLink` resource.
2. The labels to be applied to the node.
3. Definition of Local, or "A" endpoint of the link. Can contain the following fields:
    `interface` - Normalized name of the interface/port, e.g. ethernet-1-1.  
    `interfaceResource` - The reference to the existing `Interface` resource. If set to an empty string, the interface will be created.
    `node` - The reference to the `TopoNode` resource that this side of the link is connected to.
4. Definition of Remote, or "B" endpoint of the link. Contains the same fields as the `local` definition.
5. The type of link. One of `edge`, `interSwitch`, `loopback`

///

By adding node and link elements to the topology file you define your topology. This is exactly how the [3-node topology][3-node-topo-file] used in the Getting Started guide was created.

The topology file is now complete and we can apply it to drive the creation of the `TopoNode` and `TopoLink` resources. But before we get to the topology deployment, let's take a look at another way to generate a topology file.

### Topology generation

Using a topology file instead of creating the `TopoNode` and `TopoLink` resources manually is a step forward, but wouldn't it be nice to have a tool that could generate the topology file based on a more abstracted definition? This is exactly what the topology generator is for.

EDA Topology Generator allows users to define an abstracted input for a topology that can further simplify working with topologies. The topology generator expects user to provide a JSON file that consists of "layers". Each layer represents a set of nodes of the same type and role, and maps nicely to the tiers or stages of a Clos topology.  
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
    "SlotCount": 1, //(8)!
    "PodId": "1", //(9)!
    "GenerateEdge": true, //(10)!
    "NodeProfile": "srlinux-ghcr--{{ srl_version }}-", //(11)!
    "Version": "-{{ srl_version }}-", //(12)!
    "OperatingSystem": "srl", //(13)!
    "EdgeEncapType": "dot1q", //(14)!
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
4. The layer role. An arbitrary string value, but often named after a topology stage, like `leaf`, `spine`, etc.
5. The role of the next layer that this layer connects to.  
    In this example the `leaf` role has the `spine` role as the next layer, and hence the uplinks of the `leaf` layer will connect to the `spine` layer.
6. The number of uplinks each node in this layer has.
7. The number of downlinks each node in this layer has.
8. Used with chassis platforms, and will result in uplinks/downlinks being evenly distributed over line cards.
9. Pod ID is translated to a TopoNode label that is leveraged by the Fabric app when dealing with multi-pod topologies.
10. Indicating whether to generate Interface resources for links not used for either uplinks or downlinks.
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
alias toolbox='kubectl -n eda-system exec -it \
  $(kubectl get -n eda-system pods \
  -l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}") \
  -- env "TERM=xterm-256color" bash'
```

And then run `toolbox` to get a shell in the toolbox pod.

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

Now we need to run the `edatopogen` binary to generate the topology file. We will use the `-y` flag to tell the generator to output the topology file in the ConfigMap format. It will be clear why we ask for the ConfigMap format in the next section:

```bash
edatopogen -y -f topo.json
```

By default this will generate the ConfigMap file in a file named `generated_topo_pod_1.yaml` where `pod_1` is the pod ID used in the input file.

/// admonition | Remove the namespace
    type: subtle-note
Currently, the generated config map contains the `default` namespace in the resource metadata which is a remnant of the previous release. Until this is fixed in the `edatopogen` we shall remove the namespace from the generated file so that we can set the namespace ourselves when applying this resource later.

```bash
yq eval -i 'del(.metadata.namespace)' generated_topo_pod_1.yaml #(1)!
```

1. `yq` tool is included in the toolbox pod.

///

If you take a look at the generated file you will see that it has the familiar topology file structure, just packed into the ConfigMap resource. This knowledge will be useful in the next chapter when we will deploy the generated topology.

### Topology deployment

We have learned how to craft topologies using two different ways:

* by [composing the topology file](#topology-file) and specifying each TopoNode and TopoLink in a YAML file
* by using the [topology generator](#topology-generation) to generate the topology file by parsing the layered input file

Both methods in the end provided the same result: a topology file that defines the TopoNode and TopoLink of the topology. In order to drive the creation of these resources we need to perform the following steps:

1. Create a namespaced `ConfigMap` resource with a name `topo-config` in the cluster containing a JSON object describing the topology.
2. Call the `api-server-topo -n <namespace>` tool available in the `eda-toolbox` pod that will read the topology file from the namespaced `topo-config` ConfigMap and generate the required resources.

If you created your topology file in the YAML format as we did in the [topology file](#topology-file) section, you can use the available make target that will create the ConfigMap and call the `api-server-topo` tool to apply the topology in single step.

```{.shell .no-select}
make TOPO=/path/to/topo.yml topology-load #(1)!
```

1. Using the makefile from the playground repository

If you used the topology generator, then you have a ConfigMap already created, all you need to do is to apply it to the cluster:

```{.shell .no-select}
kubectl -n eda apply -f generated_topo_pod_1.yaml #(1)!
```

1. We create the ConfigMap with the topology file in the `eda` namespace. The `eda` namespace is a "user" namespace where user's resources are created.

and run the `api-server-topo` tool:

```{.shell .no-select}
api-server-topo -n eda
```

/// admonition | Danger
    type: danger
Running the `api-server-topo` tool will remove all `TopoNode`, `TopoLink` and `Interfaces` resources that are not part of the topology.
///

The `api-server-topo` tool will read the topology file from the `topo-config` ConfigMap and generate the following resources in EDA:

* `TopoNode` resources matching the topology.
* `TopoLink` resources matching the topology.
* `Interface` resources for every interface in the topology.
* Loopback `Interface` resource for every `TopoNode`.

[gs-guide]: ../getting-started/try-eda.md
[gs-guide-vnet]: ../getting-started/virtual-network.md
[3-node-topo-file]: https://github.com/nokia-eda/playground/blob/main/topology/3-nodes-srl.yaml

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>
