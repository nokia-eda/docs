# Digital Twin

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

The key ingredient in a recipe for a reliable infrastructure automation is the rigorous testing of the changes before they are applied to the production environment. And when networks are concerned, the testing is better done in a controlled environment that resembles the production as closely as possible. This is where the Digital Twin feature of Nokia EDA comes into play.

The Digital Twin provides a scalable and flexible simulation platform for testing the changes in a controlled virtual environment, ensuring that your infrastructure remains stable and reliable.

> The component that implements the Digital Twin feature is called `eda-cx`, therefore, you may see us using the CX term when referring to the Digital Twin feature.

If you completed the [quickstart](../getting-started/try-eda.md), you noticed that the three-node network topology that the Try EDA cluster comes with is in fact powered by the Digital Twin feature. The `eda-cx` component is responsible for creating a virtual representation of the network, allowing you to test changes without affecting the production environment.

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='', page=0, zoom=1.2) }}-

EDA's Digital Twin comes with unique features that set it apart from other network virtualization solutions:

* **Scalability**: The Digital Twin uses the Kubernetes platform to horizontally scale the simulation environment to match the size of your network. This means that you can deploy virtual topologies comprising hundreds of nodes and links, and the Digital Twin will schedule the nodes efficiently.
* **Declarative API**: As everything else in EDA, the Digital Twin operates in a declarative manner. The TopoNode and TopoLink resources that are used to define the physical topology of the network are also used to define the [virtual topology][topologies] in the Digital Twin. This means that you can use the same resources to define both the physical and virtual topologies, and the Digital Twin will automatically create the virtual representation of the network.
* **Multivendor support**: For every vendor device that is supported by EDA, there is a corresponding virtual simulator in the Digital Twin that you can use to create multivendor topologies.[^1].

[topologies]: ../user-guide/network-topology.md

> EDA's Digital Twin does not use [Containerlab](https://containerlab.dev) nor [Clabernetes](https://c9s.run). It is a purpose-built, production-grade virtual simulation engine that delivers support for massive scale and a tight integration with the EDA platform to achieve the goals of building the virtual replica of a production network.  
> However, if you want to use EDA with a network topology that is built with Containerlab, you can do so by using the [Containerlab integration](../user-guide/containerlab-integration.md).

## Digital Twin Mode

When [installing EDA software][install-doc], users can choose whether they want to spin up the EDA cluster for use in the Digital Twin mode or for use with the hardware devices. **By default, the cluster is deployed in the "Digital Twin" mode**, where the [Network Topology](../user-guide/network-topology.md) created by a user results in virtual simulators deployed for the topology nodes and virtual links wired for the topology links.

To deploy the cluster for use with hardware devices, set the `SIMULATE=false` in the preferences file during the [installation customization][install-doc].

/// warning
As of EDA -{{eda_version}}-, once the cluster is deployed, users can't change the mode of the cluster without redeploying it.

To check what mode your EDA cluster is deployed in, you can use the command:

```bash
kubectl get -n eda-system engineconfig \
-o custom-columns="SIMULATE MODE:.spec.simulate"
```

<div class="embed-result">
```{.text .no-copy .no-select}
SIMULATE MODE
true
```
</div>

///

## Simulated Network Topologies

One of the key responsibilities of the Digital Twin system is to create and manage the virtual topologies that typically serve as a virtual replica of the production network allowing users to test and model the network changes, validate the designs, develop automation solutions and much more.

As extensively covered in the [Network Topology](../user-guide/network-topology.md) section, the network topology in EDA is modelled with the `TopoNode`, `TopoLink` and `TopoBreakout` resources. These resources are created by the Network Topology workflow and declaratively define the physical network topology. The three-node fabric we worked on in the [Getting Started](../getting-started/try-eda.md) guide therefore is depicted as follows:

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='', page='7', zoom='2') }}-

When a user creates the topology resources in an EDA cluster running in the Digital Twin mode, the `eda-cx` component that is responsible for the simulation network will create the virtual counterparts for the `TopoNode` and `TopoLink` resources, namely the **`SimNode`**/**`SimLink`** resources.  
To illustrate this process, let's create a dummy topology with two nodes and one link between them in the `net-topo-test` namespace that we used in the [Network Topology](../user-guide/network-topology.md#topology-operations) section:

/// tab | Topology diagram
-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='', page='2', zoom='1.4') }}-
///
/// tab | Workflow YAML

Note, that the workflow spec has nothing specific to the Digital Twin here, it is the same topology input as you would use for the physical topology as well:

```yaml
--8<-- "docs/user-guide/network-topology/snippets/two-nodes-1.yaml"
```

///
/// tab | `kubectl`
Copy paste this command in your terminal to create the topology in the `net-topo-test` namespace:

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/two-nodes-1.yaml"
EOF
```

///

As shown in the diagram above, the `TopoNode` and `TopoLink` resources represent the network devices and the connections between them. The Digital Twin component in EDA uses these resources to create the virtual simulators and connect them together in a topology that mirrors the physical design. For each `TopoNode` resource, a corresponding `SimNode` resource is created, and for each `TopoLink` resource, a corresponding `SimLink` resource is created:

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='', page='3', zoom='1.4') }}-

> Check the [:material-page-next-outline: Topologies](../user-guide/network-topology.md) section for more information on how to create and manage the topologies in EDA.

### Sim topology resources

When a user deploys the topology onto the EDA cluster running in the Digital Twin mode, each TopoNode resource is backed by a virtual simulator instance[^2] and each TopoLink resource is implemented as a datapath connection established in the cluster between the sim node containers. Therefore, for the topology we created above, the Digital Twin will create two simulator instances and connect them with a virtual link:

/// tab | Sim Node resources

```bash
kubectl get -n net-topo-test simnode
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME    AGE
node1   15h
node2   15h
```
</div>
///
/// tab | Sim Link resources
```bash
kubectl get -n net-topo-test simlink
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME          AGE
node1-node2   15h
```
</div>
///

The Digital Twin uses the Kubernetes platform to create a deployment for each TopoNode resource, which in turn creates a pod that runs two containers - the virtual simulator and the datapath wiring component (cxdp). The simulators are scheduled on the EDA's Kubernetes cluster based on resource requests by the Kubernetes scheduler. This ensures that the virtual topology can horizontally scale to match the size of the emulated network.  
All Digital Twin simulator nodes run in the `eda-system` namespace, and can be listed with the following command:

```bash title="Digital Twin simulator deployments in <code>eda</code> and <code>net-topo-test</code> namespaces"
kubectl get -n eda-system deploy -l 'eda.nokia.com/app-group=cx-cluster'

```

<div class="embed-result">
```{.bash .no-copy .no-select}
NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE
cx-eda--leaf1-sim                       1/1     1            1           22h
cx-eda--leaf2-sim                       1/1     1            1           22h
cx-eda--spine1-sim                      1/1     1            1           22h
cx-eda--testman-default-sim             1/1     1            1           22h
cx-net-topo-test--node1-sim             1/1     1            1           15h
cx-net-topo-test--node2-sim             1/1     1            1           15h
```

</div>

The deployment name embeds the namespace the virtual simulator runs in and the TopoNode name, so you can easily identify which virtual simulator corresponds to which TopoNode resource.

### Edge links

The Digital Twin automatically created the simulation resources for the TopoNodes representing the `node1` and `node2` devices, as well as the SimLink resource representing the link between them. However, you may have noticed that our simple topology had no edge links, just the inter-switch link.

Let's see what happens if we add an edge link to `node2` and redeploy the topology:

/// tab | Topology diagram
-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='', page='4', zoom='1.4') }}-
///
/// tab | Workflow YAML

We add a new link template of type `edge` and create a new TopoLink resource that uses this template to connect to `node2`:

```yaml linenums="1" hl_lines="24-25 36-41"
--8<-- "docs/user-guide/network-topology/snippets/two-nodes-2.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/two-nodes-2.yaml"
EOF
```

///

A couple of interesting observations can be made after this new topology with an added edge link to the `node2` device is deployed:

1. There are no new SimLink resources created for the added edge TopoLink, only the original SimLink representing the inter-switch link is present:

    /// tab | TopoLinks

    ```
    kubectl get -n net-topo-test topolink
    ```

    <div class="embed-result">
    ```{.text .no-copy .no-select}
    NAME                  AGE
    node1-node2           159m
    node2-ethernet-1-10   159m
    ```
    </div>
    ///
    /// tab | SimLinks

    ```
    kubectl get -n net-topo-test simlink
    ```

    <div class="embed-result">
    ```{.text .no-copy .no-select}
    NAME          AGE
    node1-node2   68s
    ```
    </div>
    ///

2. There is a new Interface resource created for the edge link attached to the `node2` device, but it is operationally down:

    ```
    kubectl get -n net-topo-test interface
    ```

    <div class="embed-result">
    ```{.text .no-copy .no-select}
    NAME                  ENABLED   OPERATIONAL STATE   SPEED   LAST CHANGE   AGE
    node1-ethernet-1-1    true      up                  100G    10m           11m
    node2-ethernet-1-1    true      up                  100G    10m           11m
    node2-ethernet-1-10   true      down                100G    11m           11m
    ```
    </div>

The reason for this behavior is that the edge link defined in our topology is a stub, it has no other node to connect to, therefore no SimLink resource is created for it, and the Interface resource remains down. Edge links are typically used to connect to external systems (servers, storage, GPUs, etc) or testing endpoints, and in our case, since there is no such endpoint defined, the edge link remains unconnected.  
To bring the edge link up, a user would need to define a Sim Node that will represent the external system and connect the SimLink to it. This is the topic of the next section.

### Sim nodes

As we have identified earlier in this section, the Digital Twin in EDA automatically creates SimNode resources for each TopoNode and SimLink resource for each TopoLink that has both endpoints (local and remote) defined. The Digital Twin won't create a SimLink resource for edge TopoLinks, as they by default only have a local endpoint defined and as such don't have a remote endpoint to connect to.

However, the Network Topology workflow allows users to define custom Sim Nodes that can be used as a remote endpoint for edge TopoLinks. This way, users can connect edge links to a simulated external system in the Digital Twin.

Building on top of our previous example, let's enhance our topology spec by defining a Sim Node that will be represented as a container image running off of `ghcr.io/srl-labs/network-multitool:latest` image and connect the edge link on `node2` to it:

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='', page='5', zoom='1.4') }}-

/// tab | Workflow YAML

The changes to the workflow spec include populating the `.spec.simulation` container and defining the simulation node template and its instance, the same way as we defined templates and instances for the nodes and links of the topology.

In the `.spec.simulation.simNodeTemplates` section we define a new sim node template of type `Linux` which represents a generic Linux container with the specified container image. In the `.spec.simulation.simNodes` section we create an instance of the sim node template we just defined under the name `server2`.  
Finally, we update the edge link definition to feature the `sim` block in its endpoints list that references the newly created sim node and the interface name inside it.

```yaml linenums="1" hl_lines="42-52"
--8<-- "docs/user-guide/network-topology/snippets/two-nodes-3.yaml"
```

1. The `.spec.simulation.simNodeTemplates[].type` field defines the type of the Sim Node. Two types are currently supported: `Linux` and `TestMan`. The `Linux` type represents a generic Linux container that can run any container image specified in the `image` field.

    The `TestMan` type represents a special container image that is purpose-built to assist in testing and validation in the EDA Digital Twin environment. See the [TestMan](#testman) section below for more details.

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl create -f -
--8<-- "docs/user-guide/network-topology/snippets/two-nodes-3.yaml"
EOF
```

///

Applying this topology will result in the Digital Twin creating a new SimNode resource, the associated k8s deployment for it and the SimLink object for the edge link that now has both local and sim (remote) endpoints defined:

/// tab | Sim Nodes and deployments

The newly created SimNode resource is now present in the namespace:

```bash
kubectl get -n net-topo-test simnode
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME      AGE
node1     19m
node2     19m
server2   19m
```
</div>

And the corresponding simulator deployments are created in the `eda-system` namespace:

```bash
kubectl get -n eda-system deploy -l 'eda.nokia.com/app-group=cx-cluster' \
  -l 'cx-node-namespace=net-topo-test'
```

<div class="embed-result">
```{.bash .no-copy .no-select}
NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
cx-net-topo-test--node1-sim     1/1     1            1           20m
cx-net-topo-test--node2-sim     1/1     1            1           20m
cx-net-topo-test--server2-sim   1/1     1            1           20m
```
</div>
///

/// tab | SimLinks and TopoLinks

The same number of TopoLink resources are present as before:

```
kubectl get -n net-topo-test topolink
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME                  AGE
node1-node2           159m
node2-ethernet-1-10   159m
```
</div>

But now there is a new SimLink resource connecting `node2` and `server2` that was not present before until we added a SimNode to connect to:

```bash
kubectl get -n net-topo-test simlink
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME                  AGE
node1-node2           23m
node2-ethernet-1-10   23m
```
</div>
///

Everything looks great, but the Interface resource `node2-ethernet-1-10` still shows as operationally down:

```bash
kubectl get -n net-topo-test interface
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME                  ENABLED   OPERATIONAL STATE   SPEED   LAST CHANGE   AGE
node1-ethernet-1-1    true      up                  100G    22m           24m
node2-ethernet-1-1    true      up                  100G    22m           24m
node2-ethernet-1-10   true      down                100G    23m           24m
```
</div>

Why? Because for SimNode of type `Linux`, EDA's Digital Twin does not automatically bring up the interfaces that we specified in the topology input.  
If we connect to the shell of the `server2` container image we will see that the `eth1` interface that we specified in the links section of our topology is operationally down. We can bring it up manually with the standard Linux commands:

```bash title="connecting to the shell of the server2 SimNode"
kubectl -n eda-system exec -it \
$(kubectl get -n eda-system pods -l 'cx-node-namespace=net-topo-test' \
-l 'cx-pod-name=server2' \
-o jsonpath='{.items[].metadata.name}') \
-- bash
```

<div class="embed-result">
```{.text .no-copy .no-select}
[*]─[cx-net-topo-test--server2-sim-58cb56dd56-sgh6r]─[/]
└──> ip link show eth1
3: eth1@eth1-cx: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 5e:80:14:5e:bf:6f brd ff:ff:ff:ff:ff:ff
```
</div>

Let's bring up the interface with the `ip link set` command:

```bash
[*]─[cx-net-topo-test--server2-sim-58cb56dd56-sgh6r]─[/]
└──> ip link set eth1 up
```

Immediately after that we can see that the Interface resource for the `ethernet-1-10` port on `node2` is now operationally up:

```bash
kubectl get -n net-topo-test interface
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME                  ENABLED   OPERATIONAL STATE   SPEED   LAST CHANGE   AGE
node1-ethernet-1-1    true      up                  100G    37m           38m
node2-ethernet-1-1    true      up                  100G    37m           38m
node2-ethernet-1-10   true      up                  100G    7s            38m
```
</div>

Now you know how to define SimNodes in the Network Topology workflow and connect edge links to them.

### Connections topology

In the [Sim Nodes](#sim-nodes) section we described how users can define custom Sim Nodes in the `.spec.simulation.simNodes` section of the Network Topology workflow spec and connect edge links to them by providing the `sim` block in the link endpoints. This way, users can selectively attach edge links to the simulated nodes, however, this approach may become tedious when there are many edge links to be connected in the same way.  
For example, when you want to connect ports `ethernet-1-1` on all nodes to a single Sim Node that represents a testing agent or a traffic generator. This is the case when the [TestMan](#testman) is used as a Sim Node to which multiple edge links can be connected simultaneously. To simplify the process of connecting multiple edge links to a single Sim Node, the Digital Twin supports the concept of a connection topology.

The connection topology is defined in the `.spec.simulation.topology` section of the Network Topology workflow spec. Here, users can define the rules that specify which nodes and interfaces should be connected to which Sim Node and which Sim Node interface. The rules support wildcard patterns to match multiple nodes and interfaces, allowing for a concise definition of the connections.

Let's work through a set of connection topologies examples that showcase the capabilities and use cases of this feature.

The previous example in the [Sim Nodes](#sim-nodes) section showed how to connect the edge link `ethernet-1-10` on `node2` to a Sim Node named `server2`. The same connection can be defined with the connection topology as follows (and then no `sim` block is needed in the link definition):

```yaml
spec:
  simulation:
    topology:
      - node: "node2"
        interface: "ethernet-1-10"
        simNode: server2
        simNodeInterface: "eth1"
```

The `.spec.simulation.topology` section defines a list of connection pairs that specify which node and interface should be connected to which Sim Node and Sim Node interface. For example, here is how several node/interface pairs can be defined:

```yaml
spec:
  simulation:
    topology:
      - node: "node1"
        interface: "ethernet-1-10"
        simNode: server1
        simNodeInterface: "eth1"
      - node: "node2"
        interface: "ethernet-1-10"
        simNode: server2
        simNodeInterface: "eth1"
```

A more interesting use case where connection topology shines is when wildcards are used in the node and/or interface fields. For example, to connect all edge interfaces on `node1` to a single Sim Node named `server1`, the following connection topology can be defined:

```yaml
spec:
  simulation:
    topology:
      - node: "node1"
        interface: "*"
        simNode: server1
```

Note, how `*` is used in the `interface` field to match all interfaces on `node1`. The `simNodeInterface` field is omitted here, so the Digital Twin will automatically assign the interfaces on the Sim Node in the order they are connected using the `eth0`, `eth1`, `eth2`, ... naming convention.

Another popular use case is to connect the same interface on all nodes to a single Sim Node. For example, to connect the `ethernet-1-10` interface on all nodes to a Sim Node named `testman-default`, the following connection topology can be defined:

```yaml
spec:
  simulation:
    topology:
      - node: "*"
        interface: "ethernet-1-10"
        simNode: testman-default
```

Here, the wildcard `*` is used in the `node` field to match all nodes in the topology while the interface field specifies the `ethernet-1-10` value. This results in all `ethernet-1-10` interfaces on all nodes being connected to the `testman-default` Sim Node. As before, since the Sim Node interface is not specified, the Digital Twin will automatically assign the interfaces on the Sim Node in the order they are connected.

And lastly, a fully wildcarded connection topology can be defined to connect all edge interfaces on all nodes to a single Sim Node. We use this connection mode with the [Try EDA](../getting-started/try-eda.md) topology for example, where we need to connect all edge interfaces on all nodes to the `testman-default` Sim Node to make all links up and running:

```yaml
spec:
  simulation:
    topology:
      - node: "*"
        interface: "*"
        simNode: testman-default
```

## TestMan

In a lot of cases, the simulated topology benefits from having emulated client devices that can be used to test the connectivity and functionality of the network. Containers running iperf, ICMP pings, HTTP clients, and other tools dear to network engineers are typically found in these emulated clients.

While we [showed above](#sim-nodes) how users can define a Sim Node of type `Linux` and use any container image to run the testing tools, it might not be very convenient to run a standalone container for each access port in the topology. And while it is possible to use one generic Linux container and create VRFs and namespaces inside it, the burden of managing this configuration falls on the user.  
Another tension point is the API. The iPerfs, ICMPs and curls of the world don't have a native support for REST or gRPC API to allow a system to programmatically control the test execution and retrieve the results.

These challenges and limitations served as a motivation to create the TestMan - a container image that is purpose-built to assist in testing and validation in the EDA Digital Twin environment.  
Having ownership of the TestMan allows us to tightly integrate it with the EDA Digital Twin and provide a seamless experience for users.

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='A single TestMan container emulates many clients', page='6', zoom='2') }}-

In fact, the "Try EDA" topology that is featured in the [Getting Started](../getting-started/try-eda.md) guide leverages the TestMan as the emulated clients for all edge links in the topology.

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='TestMan container in Try EDA topology', page='7', zoom='1.2') }}-

To define the TestMan SimNode in the Network Topology users need to set the type of the Sim Node template to `TestMan` as follows:

```yaml title="Defining TestMan SimNode in Network Topology workflow (snippet)"
spec:
  simulation:
    topology:
      - node: "*"
        interface: "*"
        simNode: testman-default
    simNodeTemplates:
      - name: default
        type: TestMan #(2)!
    simNodes:
      - name: testman-default #(1)!
        template: default
```

1. Currently `edactl` tool expects the TestMan node to be named `testman-default`.
2. The `.spec.simulation.simNodeTemplates[].type` field is set to `TestMan` to indicate that this Sim Node template represents a TestMan container and not just a generic Linux container.

### TestMan interfaces

When the TestMan node is defined in the topology, the Digital Twin automatically creates and manages the interfaces inside the TestMan container to match the number of connections made to it. This will cause every TopoLink to be in the operational up state:

```bash
kubectl -n eda get topolink \
-o custom-columns="NAME:.metadata.name,NAMESPACE:.metadata.namespace,STATE:.status.operationalState"
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME                 NAMESPACE   STATE
leaf1-2-e1212        eda         up
leaf1-e1011          eda         up
leaf1-ethernet-1-3   eda         up
leaf1-ethernet-1-4   eda         up
leaf1-ethernet-1-5   eda         up
leaf1-ethernet-1-6   eda         up
leaf1-ethernet-1-7   eda         up
leaf1-ethernet-1-8   eda         up
leaf1-ethernet-1-9   eda         up
leaf1-spine1-1       eda         up
leaf1-spine1-2       eda         up
leaf2-e1011          eda         up
leaf2-ethernet-1-3   eda         up
leaf2-ethernet-1-4   eda         up
leaf2-ethernet-1-5   eda         up
leaf2-ethernet-1-6   eda         up
leaf2-ethernet-1-7   eda         up
leaf2-ethernet-1-8   eda         up
leaf2-ethernet-1-9   eda         up
leaf2-spine1-1       eda         up
leaf2-spine1-2       eda         up
```
</div>

However, without any services deployed in EDA, the edge interfaces inside the TestMan container will not be configured with any IP/MAC addresses:

```bash
edactl -n eda testman get-edge-if all
```

<div class="embed-result">
```{.text .no-copy .no-select}
No EdgeInterfaces found
```
</div>

> `edactl -n <namespace> testman` is the command line interface to interact with the TestMan features.

If you were to create a Fabric and a Virtual Network in EDA that would target the edge interfaces connected to the TestMan, the Digital Twin would automatically configure the interfaces inside the TestMan container with the appropriate addressing.

/// details | Creating a Fabric and a Virtual Network
    type: code-example
If you don't have a Fabric and a Virtual Network created in EDA yet, paste this snippet in your terminal to create them in the `eda` namespace:

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/examples/my-fabric.yaml"
---
--8<-- "docs/user-guide/network-topology/snippets/vnet-vlan-10.yaml"
EOF
```

///

The above snippet creates an EVPN VXLAN fabric and a Layer 2 Virtual Network that uses VLAN 10 on all interfaces labelled with `eda.nokia.com/role=edge`. Based on this configuration, the Digital Twin will automatically configure the corresponding edge interfaces on the TestMan side to be part of VLAN 10 and assign IP and MAC addresses to them:

```bash
edactl -n eda testman get-edge-if all
```

<div class="embed-result">
```{.text .no-copy .no-select}
--------------------------------------------------------------------------------
        Number of EdgeInterfaces found: 17
--------------------------------------------------------------------------------
Namespace           : eda
Name                : eif-lag-leaf1-2-e1212-local-vlan-10
IfResName           : lag-leaf1-2-e1212-local
IfName              : b2
VlanID              : 10
Router              :
BridgeDomain        : vnet-demo-bd
MAC                 : FE:3F:BB:00:00:0B
IPs                 : 10.0.0.12
                    : fd12:3456:789a:1::c
--------------------------------------------------------------------------------
Namespace           : eda
Name                : eif-lag-leaf1-e1011-local-vlan-10
IfResName           : lag-leaf1-e1011-local
IfName              : b3
VlanID              : 10
Router              :
BridgeDomain        : vnet-demo-bd
MAC                 : FE:3F:BB:00:00:08
IPs                 : 10.0.0.9
                    : fd12:3456:789a:1::9
--------------------------------------------------------------------------------
# snipped for brevity
--------------------------------------------------------------------------------
Namespace           : eda
Name                : eif-leaf1-ethernet-1-3-vlan-10
IfResName           : leaf1-ethernet-1-3
IfName              : eth1
VlanID              : 10
Router              :
BridgeDomain        : vnet-demo-bd
MAC                 : FE:3F:BB:00:00:0C
IPs                 : 10.0.0.13
                    : fd12:3456:789a:1::d
--------------------------------------------------------------------------------
```
</div>

> The Digital Twin controller knows how to configure LAG interfaces as well, so for the local and multi-node ESI LAGs defined in the topology, TestMan will create the corresponding LAG interfaces and assign them the appropriate addressing as well.

### Ping

As of -{{eda_version}}-, TestMan supports ICMP ping tests that can be executed against the edge interfaces. This allows users to quickly validate the connectivity of the simulated network from the client perspective.

To execute a ping test from TestMan, users need to run the `edactl -n <ns> testman ping` command, that supports the following parameters:

```
ping dst-ip using edge-interface

Usage:
  edactl testman ping [command]

Available Commands:
  eif-name    ping dst-ip using specified edge-interface
  interface   ping dst-ip using edge-interface identified by interface-resource and qtag
  vrf-name    ping dst-ip using one of the edge-interface from specified vrf
```

Using the Try EDA topology as an example and the simple Layer 2 Virtual Network we created above, we can execute a ping test from TestMan from one of the edge interfaces to an IP address assigned to another edge interface. For a concrete example, let's validate that the client connected to `leaf1:ethernet-1-3` interface can reach the client connected to `leaf2:ethernet-1-3` interface. We start by identifying the edge interface name inside TestMan that corresponds to the `leaf1-ethernet-1-3` interface resource:

```bash
edactl -n eda testman get-edge-if interface leaf1-ethernet-1-3
```

<div class="embed-result">
```{.text .no-copy .no-select}
--------------------------------------------------------------------------------
        Number of EdgeInterfaces found: 1
--------------------------------------------------------------------------------
Namespace           : eda
Name                : eif-leaf1-ethernet-1-3-vlan-10
IfResName           : leaf1-ethernet-1-3
IfName              : eth1
VlanID              : 10
Router              :
BridgeDomain        : vnet-demo-bd
MAC                 : FE:3F:BB:00:00:0C
IPs                 : 10.0.0.13
                    : fd12:3456:789a:1::d
--------------------------------------------------------------------------------
```
</div>

Next, let's identify the IP address assigned to the edge interface connected to `leaf2-ethernet-1-3` interface resource:

```bash
edactl -n eda testman get-edge-if interface leaf2-ethernet-1-3
```

<div class="embed-result">
```{.text .no-copy .no-select}
--------------------------------------------------------------------------------
        Number of EdgeInterfaces found: 1
--------------------------------------------------------------------------------
Namespace           : eda
Name                : eif-leaf2-ethernet-1-3-vlan-10
IfResName           : leaf2-ethernet-1-3
IfName              : eth5
VlanID              : 10
Router              :
BridgeDomain        : vnet-demo-bd
MAC                 : FE:3F:BB:00:00:0A
IPs                 : 10.0.0.11
                    : fd12:3456:789a:1::b
--------------------------------------------------------------------------------
```
</div>

Great, we have everything we need to run the ping test now:

* the source edge interface name inside TestMan: `eif-leaf1-ethernet-1-3-vlan-10`
* the destination IP address to ping: `10.0.0.11`

Let's run the ping test:

```bash
edactl -n eda testman ping eif-name eif-leaf1-ethernet-1-3-vlan-10 10.0.0.11
```

<div class="embed-result">
```{.text .no-copy .no-select}
--- timeout: 16.00 sec, interval: 1000000 µsec ---
PING 10.0.0.11 10.0.0.13 &{eda eif-leaf1-ethernet-1-3-vlan-10}: 56(84) bytes of data.
84 bytes from 10.0.0.11: icmp_seq=0 ttl=128 time=2.886ms
--- 10.0.0.11 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 104ms
rtt min/avg/max/mdev = 2.886/2.886/2.886/0.000ms
```
</div>

> More TestMan capabilities are coming soon, stay tuned!

## Connecting to the Digital Twin Nodes

By the virtue of being Kubernetes-native, each simulator node in the Digital Twin is represented by a pod that runs the network OS and the datapath component. Therefore, you can connect and expose the simulator nodes using the standard Kubernetes tooling and methods.

For long-term access to the simulated nodes an administrator might create a service and an ingress or loadbalancer resource. This typically requires some additional configuration and infrastructure setup, but achieves persistent access to the selected ports and protocols.

Typically, though, users would want to connect with SSH to the simulator nodes to inspect the configuration, logs or run ad-hoc commands. Start with listing the TopoNodes in your namespace using `kubectl`. If you are running the [Try EDA](../getting-started/try-eda.md) cluster, you can expect to see the three nodes in the output:

```bash
kubectl -n eda get toponodes 
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME     PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE     AGE
leaf1    7220 IXR-D3L   25.3.2    srl   true        normal   Connected   Synced   99m
leaf2    7220 IXR-D3L   25.3.2    srl   true        normal   Connected   Synced   99m
spine1   7220 IXR-H2    25.3.2    srl   true        normal   Connected   Synced   99m
```
</div>

As we explained earlier, each TopoNode is backed by a Kubernetes deployment that runs the simulator. These deployments are spawned in the EDA core namespace (`eda-system` by default) and have the `eda.nokia.com/app-group=cx-cluster` label set:

```bash
kubectl -n eda-system get deploy -l eda.nokia.com/app-group=cx-cluster
```

<div class="embed-result">
```{.bash .no-copy .no-select}
NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
cx-eda--leaf1-sim             1/1     1            1           3h32m
cx-eda--leaf2-sim             1/1     1            1           3h32m
cx-eda--spine1-sim            1/1     1            1           3h32m
cx-eda--testman-default-sim   1/1     1            1           3h32m
```

<small>If you are running the Try EDA cluster, you will see the <code>testman</code> deployment as well. This is a special testing agent that we will cover in a later section.</small>

</div>

As per the virtual topology that comes with the [Try EDA](../getting-started/try-eda.md) cluster, we got three simulator deployments for leaf1, leaf2 and spine1 nodes. Using `kubectl` we can connect to the node's shell and execute the CLI process to get the CLI access:

```bash
kubectl --namespace eda-system exec -it \
$(kubectl --namespace eda-system get pods -l cx-pod-name=leaf1 \
-o=jsonpath='{.items[*].metadata.name}') \
-- bash -l -c 'sudo sr_cli'
```

<div class="embed-result">
```{.text .no-copy .no-select}
Defaulted container "leaf1" out of: leaf1, cxdp
Loading environment configuration file(s): ['/etc/opt/srlinux/srlinux.rc']
Welcome to the Nokia SR Linux CLI.

--{ + running }--[  ]--
A:root@leaf1#

```
</div>

But typing in this multiline command is a bit too much for a repetitive process, so here is a little script that you can put in your `$PATH` to quickly SSH to the desired node by its name. This script will work for physical nodes as well as simulator nodes.

/// details | `node-ssh` script to connect to a simulator node
    type: example
/// tab | script
```bash
--8<-- "docs/digital-twin/node-ssh"
```

///
/// tab | adding to `$PATH`

You can paste this command in your terminal to add the script to `/usr/local/bin` directory, and make it executable:

```bash
cat << 'EOF' | sudo tee /usr/local/bin/node-ssh
--8<-- "docs/digital-twin/node-ssh"
EOF
sudo chmod +x /usr/local/bin/node-ssh
```

///
///

With the `node-ssh` script in place, you can connect with ssh to any node in your Digital Twin by its name:

```bash
# Usage: ./node-ssh <node-name> [<user-namespace>:-eda] [<core-namespace>:-eda-system]
node-ssh spine1
```

For SimNodes that don't have SSH access (like SimNodes running generic Linux containers), use the `node-shell` script that opens up a shell in the simulator pod:

/// details | `node-shell` script to open a shell to a simulator node
    type: example
/// tab | script

```bash
--8<-- "docs/digital-twin/node-shell"
```

///
/// tab | adding to `$PATH`

You can paste this command in your terminal to add the script to `/usr/local/bin` directory, and make it executable:

```bash
cat << 'EOF' | sudo tee /usr/local/bin/node-shell
--8<-- "docs/digital-twin/node-shell"
EOF
sudo chmod +x /usr/local/bin/node-shell
```

///
///

With the script in place, you can connect to any node in your Digital Twin by its name:

```bash
# Usage: ./node-ssh <node-name> [<user-namespace>:-eda] [<core-namespace>:-eda-system]
node-ssh spine1
```

With the `node-shell` script in place, you can open the shell to any node in your Digital Twin by its name:

```bash
# Usage: ./node-shell <node-name> [<user-namespace>:-eda] [<core-namespace>:-eda-system]
node-shell testman-default
```

## Configuring Simulator Resource Requests

When EDA CX component creates the virtual simulators in the Digital Twin, it creates a Kubernetes deployment for each simulator node in the topology. To guarantee that the simulators have enough resources to run under potentially high load, the deployments are configured with the resource requests for CPU and memory.

For example, if you have the Try EDA cluster deployed, you can check the resource requests for the **leaf1** simulator node with the command:

```bash
kubectl get pods -n eda-system -l cx-pod-name=leaf1 \
-o custom-columns="POD:.metadata.labels.cx-pod-name,\
CPU_REQUEST:.spec.containers[*].resources.requests.cpu,\
MEM_REQUEST:.spec.containers[*].resources.requests.memory"
```

<div class="embed-result">
```
POD     CPU_REQUEST   MEM_REQUEST
leaf1   200m,200m     1Gi,250Mi
```
</div>

You will see at least two values reported for the CPU and memory requests. The first value is the resources requested for the simulator node itself, and the second value is the resources requested for the topology wiring service that EDA's Digital Twin uses to connect the simulator nodes in the topology.  
In the example above, the leaf1 simulator node requests 200m of CPU and 1Gi of memory for itself, and 200m of CPU and 250Mi of memory for the topology wiring service, resulting in a total of 400m of CPU and 1.25Gi of memory requested per the simulator node of the SR Linux type.

The default values for the resource requests are chosen to ensure that the simulators can run under medium load. However, you may want to adjust the resource requests based on your specific use case and either increase or decrease them. Often, you may want to decrease the default values to save resources in the cluster and fit more simulator nodes, especially if you run development clusters with a limited amount of hardware resources.

EDA allows you to configure CPU and memory requests and limits for the supported simulator types via the Config Engine setting. For example, to change the CPU and memory requests for the SR Linux simulator nodes and the CXDP (topology wiring service), start by entering the edit mode for the Config Engine:

```bash
kubectl edit -n eda-system engineconfig
```

Add the following block to the `spec` section:

```yaml
customSettings:
- applicationName: cx
  settings:
  - name: SrlCpuRequest
    value: 100m
  - name: SrlMemoryRequest
    value: 500Mi
  - name: CxdpCpuRequest
    value: 50m
  - name: CxdpMemoryRequest
    value: 200Mi
```

This will change the default requests for the SR Linux simulator nodes and the CXDP container.

> After editing the Config Engine resource, you need to redeploy the topology for the changes to take effect.

/// details | Full list of setting names for the CX application

| Setting Name         | Default Value | Description             |
| -------------------- | ------------- | ----------------------- |
| **Nokia SR Linux**        |           |     |
| `SrlCpuRequest`        | 200m          | SR Linux CPU request    |
| `SrlMemoryRequest`     | 1Gi           | SR Linux Memory request |
| `SrlCpuLimit`          |               | SR Linux CPU limit      |
| `SrlMemoryLimit`       |               | SR Linux Memory limit   |
| **Nokia SR OS**        |           |     |
| `SrosCpuRequest`       | 200m          | SR OS CPU request       |
| `SrosMemoryRequest`    | 1Gi           | SR OS Memory request    |
| `SrosCpuLimit`         |               | SR OS CPU limit         |
| `SrosMemoryLimit`      |               | SR OS Memory limit      |
| **Cisco NX OS**        |           |     |
| `NxosCpuRequest`       | 200m          | NX-OS CPU request       |
| `NxosMemoryRequest`    | 1Gi           | NX-OS Memory request    |
| `NxosCpuLimit`         |               | NX-OS CPU limit         |
| `NxosMemoryLimit`      |               | NX-OS Memory limit      |
| **Arista EOS**        |           |     |
| `EosCpuRequest`        | 200m          | EOS CPU request         |
| `EosMemoryRequest`     | 1Gi           | EOS Memory request      |
| `EosCpuLimit`          |               | EOS CPU limit           |
| `EosMemoryLimit`       |               | EOS Memory limit        |
| **Nokia EDA Edge Sim**        |           |     |
| `EdgeSimCpuRequest`    | 200m          | EdgeSim CPU request     |
| `EdgeSimMemoryRequest` | 500Mi         | EdgeSim Memory request  |
| `EdgeSimCpuLimit`      |               | EdgeSim CPU limit       |
| `EdgeSimMemoryLimit`   |               | EdgeSim Memory limit    |
| **Nokia EDA CXDP**        |           |     |
| `CxdpCpuRequest`       | 200m          | CXDP CPU request        |
| `CxdpMemoryRequest`    | 250Mi         | CXDP Memory request     |
| `CxdpCpuLimit`         |               | CXDP CPU limit          |
| `CxdpMemoryLimit`      |               | CXDP Memory limit       |

///

After editing the Config Engine resource and redeploying the topology, you can check that the new values have been applied:

```bash
kubectl get pods -n eda-system -l cx-pod-name=leaf1 \
-o custom-columns="POD:.metadata.labels.cx-pod-name,\
CPU_REQUEST:.spec.containers[*].resources.requests.cpu,\
MEM_REQUEST:.spec.containers[*].resources.requests.memory"
```

<div class="embed-result">
```
POD     CPU_REQUEST   MEM_REQUEST
leaf1   100m,50m      500Mi,100Mi
```
</div>

[install-doc]: ../software-install/deploying-eda/installing-the-eda-application.md#customizing-the-installation

[^1]: EDA does not bundle the virtual simulators for the 3rd-party vendors. Users should obtain the simulators themselves and made them available to the Digital Twin.
[^2]: Like [Nokia SR Linux](https://github.com/nokia/srlinux-container-image), Nokia SR OS (SR-SIM) or third-party vendor simulator, e.g. Arista EOS.
