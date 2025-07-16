# Topologies

Topologies in EDA cover a lot of ground. Not only do they define the design of a physical or simulated network, they also drive the visualization of various overlays in the EDA UI.

Let's start with a familiar role of a topology - the network topology.

## Network topology

A network topology in a broader sense describes the network design. Be it a Clos, a Fat Tree or a Ring design, the topology is what inherently defines the network.

Like every topology is defined by its nodes and links, the EDA topology consists of node (`TopoNode`) and link (`TopoLink`) objects. The EDA topology nodes are represented by the devices in your network, and the topology links define the relationships between them.

<!-- [topoNode-crd]: https://doc.crds.dev/github.com/nokia-eda/kpt/core.eda.nokia.com/TopoNode/v1@v-{{ eda_version }}-
[topoLink-crd]: https://doc.crds.dev/github.com/nokia-eda/kpt/core.eda.nokia.com/TopoLink/v1@v-{{ eda_version }}- -->

If you come here after finishing the [Getting Started][gs-guide] guide, you may remember the 3-node topology that we worked on:

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='Physical topology', page=0) }}-

In EDA, this topology is represented by the `TopoNode` and `TopoLink` objects mirroring the physical design:

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='EDA topology', page=1) }}-

Almost no difference with a physical topology, right?

/// admonition | Note
    type: subtle-note
Bear in mind, that the `TopoNode` and `TopoLink` objects that make up the topology are not specific to your digital twin network, for a physical topology the same objects are used to represent the devices and their links.
///

So if the `TopoNode` and `TopoLink` objects make up a topology, how do we create them?  
The obvious way is to create these Custom Resources by hand, but this is going to be a tedious and likely error-prone process when carried out manually.

To assist with this process, EDA provides a couple of methods to generate the required topology resources based on an abstracted input:

* using a topology file
* or using the topology generator

### Topology file

Instead of creating the topology resources individually, EDA provides a way to describe the topology nodes and links in a topology file. Based on the contents of this file EDA will create the `TopoNode`, `TopoLink`, `Interface` and `Breakout` resources. This approach enables the users to define topologies in a declarative way.

Let's have a look at the topology file structure and a snippet matching the structure.

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
Elements of these lists are modelled after the `TopoNode`, `TopoLink`, and `TopoBreakout` resources, respectively. Let's describe the fields you would typically use in these resources.

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

#### Simplifying topology file

Because the topology definition is a YAML-formatted document embedded in a ConfigMap, it is easier to work with the topology content in a separate file and then embed it into the ConfigMap. You will see us using this method to define topologies where a standalone YAML file contain just the `items` list with nodes, links and breakout elements, without the ConfigMap wrapping:

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='Topology YAML', page=1) }}-

> When you have a Topology YAML outside of the ConfigMap wrapping, you can benefit from the YAML syntax highlighting and less indentation to deal with.  
> This is exactly how the [3-node topology][3-node-topo-file] file is defined that we used the [Getting Started guide][gs-guide].

### Deploying Topology

To deploy a topology a user should take the following steps:

1. Create the ConfigMap resource with a predefined `eda-topology` name in a target namespace.
2. Run the `api-server-topo` tool available in the Toolbox pod[^1] to apply the defined topology and make EDA create the `TopoNode`, `TopoLink` and `Interface` resources based on the topology file contents.

/// admonition | Danger
    type: danger
Running the `api-server-topo` tool will remove the `TopoNode`, `TopoLink`, `Interface` and `Breakout` resources that are not part of the new topology.
///

If the topology file is in the simplified format as demonstrated in the [section above](#simplifying-topology-file), you should create a ConfigMap resource with its contents. We have created a few automation scripts to help with this translation, so you don't have to create the ConfigMap manually.

For example, in the [Try EDA][gs-guide] setup the [3-node topology](https://github.com/nokia-eda/playground/blob/main/topology/3-nodes-srl.yaml) is created with [`topology-load` make target][make-load-topo] that takes in the topology defined in the YAML file, adds it to the `eda-topology` ConfigMap in the `eda` namespace, and calls the `api-server-topo` tool to apply the topology:

[make-load-topo]: https://github.com/nokia-eda/playground/blob/c8c6110cf118c88b8b8e7932b30fcda16fb94067/Makefile#L1117

```{.shell .no-select}
make TOPO=topology/3-nodes-srl.yaml topology-load #(1)!
```

1. Using the makefile from the playground repository

If you are working outside of the playground repository where the make targets reside, you can make use of the following shell script that achieves the same result:

/// details | Loading topology YAML with shell script
    type: subtle-note

```bash
#!/bin/bash

# pass the topo yaml file from the root of the repo
# e.g. bash srl-ceos/load-topo.sh srl-ceos/6-node-srl-ceos.yaml
TOPO_YAML=${1}

# namespace to load deploy topology into
# default is eda
TOPO_NS=${2:-eda}

if [ ! -f "${TOPO_YAML}" ]; then
  echo "Topology file ${TOPO_YAML} does not exist"
  exit 1
fi

echo "Loading topology from ${TOPO_YAML}"

cat <<EOF | kubectl apply -n ${TOPO_NS} -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: eda-topology
data:
  eda.yaml: |
$(sed 's/^/    /' "${TOPO_YAML}")
EOF

kubectl -n eda-system exec -it \
  $(kubectl get -n eda-system pods \
  -l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}") \
  -- api-server-topo -n ${TOPO_NS}
```

///

In case your topology definition is already in the ConfigMap format, you can apply it directly using `kubectl`:

```bash
kubectl -n eda apply -f my-topology-cfgmap.yaml
```

The `api-server-topo` tool (available in the Toolbox[^1]) will read the topology file from the `eda-topology` ConfigMap in a specified namespace and generate the following resources in EDA:

* `TopoNode` for each node in the topology ConfigMap.
* `TopoLink` for each link in the topology ConfigMap.
* `Interface` for each interswitch and edge link in the topology ConfigMap.
* `Breakout` for each breakout defined in the topology ConfigMap.

One or more transactions from the Kubernetes API will appear and once they succeed you will see the resources in your cluster.

### Removing Topology

By deploying an empty topology file you can remove the existing topology from EDA. For instance, you can use the following script to remove the topology:

```bash hl_lines="14"
#!/bin/bash

# namespace to load deploy topology into
# default is eda
TOPO_NS=${1:-eda}

cat <<EOF | kubectl apply -n ${TOPO_NS} -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: eda-topology
data:
  eda.yaml: |
    {}
EOF

kubectl -n eda-system exec -it \
  $(kubectl get -n eda-system pods \
  -l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}") \
  -- api-server-topo -n ${TOPO_NS}
```

Deploying an empty topology will remove all `TopoNode`, `TopoLink`, `Interface`, and `Breakout` resources in the specified namespace.

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
