# Digital Twin

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

The key ingredient in a recipe for a reliable infrastructure automation is the rigorous testing of the changes before they are applied to the production environment. And when networks are concerned, the testing is better done in a controlled environment that resembles the production as closely as possible. This is where the Digital Twin feature of Nokia EDA comes into play.

The Digital Twin provides scalable and flexible simulation platform for testing the changes in a controlled virtual environment, ensuring that your infrastructure remains stable and reliable.

> The component that implements the Digital Twin feature is called `eda-cx`, therefore, you may see us using the CX term when referring to the Digital Twin feature.

If you completed the [quickstart](../getting-started/try-eda.md), you noticed that the small three-node network topology that the Try EDA cluster comes with is in fact powered by the Digital Twin feature. The `eda-cx` component is responsible for creating a virtual representation of the network, allowing you to test changes without affecting the production environment.

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='', page=0, zoom=1.2) }}-

EDA's Digital Twin packs a powerful set of distinctive and unique features that sets it apart from other network virtualization solutions:

* **Scalability**: The Digital Twin uses the Kubernetes platform to horizontally scale the simulation environment to match the size of your network. This means that you can deploy virtual topologies comprising hundreds of nodes and links, and the Digital Twin will schedule the nodes efficiently.
* **Declarative API**: As everything else in EDA, the Digital Twin operates in a declarative manner. The TopoNode and TopoLink resources that are used to define the physical topology of the network are also used to define the [virtual topology][topologies] in the Digital Twin. This means that you can use the same resources to define both the physical and virtual topologies, and the Digital Twin will automatically create the virtual representation of the network.
* **Multivendor support**: For every vendor device that is supported by EDA, there is a corresponding virtual simulator in the Digital Twin that you can use to create multivendor topologies.[^1].

[topologies]: ../user-guide/topologies.md

> EDA's Digital Twin does not use [Containerlab](https://containerlab.dev) nor [Clabernetes](https://c9s.run). It is a custom, production-grade virtual simulation engine that delivers support for massive scale and a tight integration with the EDA platform to achieve the goals of building the virtual replica of a production network.  
> However, if you want to use EDA with a network topology that is built with Containerlab, you can do so by using the [Containerlab integration](../user-guide/containerlab-integration.md).

## Digital Twin Mode

When [installing EDA software][install-doc], users can choose if they want spin up the EDA cluster for Digital Twin or for the use with the hardware devices. **By default, the cluster is deployed in the "Digital Twin" mode**, where the virtual simulators are created for all the supported vendors based on the TopoNode and TopoLink resources that are defined in the EDA cluster.

To deploy the cluster for production use, set the `SIMULATE=false` in the preferences file during the [installation customization][install-doc].

/// warning
Once the EDA cluster is deployed, you can't change the mode of the cluster without redeploying it.

To check what mode your EDA cluster is deployed in, you can use the command:

```bash
kubectl get -n eda-system engineconfig \
-o custom-columns="SIMULATE MODE:.spec.simulate"
```

///

## Creating Virtual Topologies

One of the key responsibilities of the Digital Twin system is to create and manage the virtual topologies that typically represent a virtual network running network simulators and client endpoints. These networks are then managed by the EDA platform to mimic the behavior of the physical network and allow users to test and model the network changes, validate the designs, develop automation solutions and much more.

In EDA, the network topology (be it physical or virtual) is defined by the `TopoNode` and `TopoLink` resources. As the names suggest, they represent the network devices and the connections between them, respectively. The Digital Twin uses these resources to create the virtual simulators and connect them together in a topology that matches the physical network.

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='Physical topology', page=0) }}-

In EDA, this topology is represented by the `TopoNode` and `TopoLink` objects mirroring the physical design:

-{{ diagram(url='nokia-eda/docs/diagrams/playground-topology.drawio', title='Digital Twin topology', page=1) }}-

> Check the [:material-page-next-outline: Topologies](../user-guide/topologies.md) section for more information on how to create and manage the topologies in EDA.

When a user deploys the topology onto the EDA cluster running in the Digital Twin mode, each TopoNode resource is backed by a virtual simulator instance[^2] and each TopoLink resource is implemented as a datapath connection between the simulators or between a simulator and a testing endpoint.

The Digital Twin uses the Kubernetes platform to create a deployment for each TopoNode resource, which in turn creates a pod that runs the virtual simulator and the datapath wiring component - CXDP. The simulators are scheduled on the EDA's Kubernetes cluster based on the resource requests Kubernetes scheduler. This ensures that the virtual topology can horizontally scale to match the size of the emulated network.

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

But typing in this multiline command is a bit too much for a repetitive process, so here is a little script that you can put in your `$PATH` to quickly SSH to the desired node by its name:

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

With the script in place, you can connect to any node in your Digital Twin by its name:

```bash
node-ssh spine1
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

This will change the default requests for the SR Linux simulator nodes and the Cxdp container.

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
