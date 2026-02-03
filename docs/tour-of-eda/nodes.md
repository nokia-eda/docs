# Node Management

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

-{{% import 'icons.html' as icons %}}-

In contrast to some automation frameworks that either only generate configuration snippets or push configurations in a one-off manner, EDA maintains continuous control over the network devices, referred to as topology nodes. The closed-loop management of these nodes is a fundamental aspect of EDA and is essential to achieving reliable and consistent infrastructure automation.

When a node is successfully onboarded into EDA the platform starts to act as the single source of truth for the configuration of that node and continuously monitors its state. From the operations perspective this means that any changes to the configuration of the managed nodes should be done through EDA, as any out-of-band changes will be classified as deviations and the platform will offer to remediate them to the desired state.

The simplified device onboarding flow is illustrated below:

-{{ diagram(url='nokia-eda/docs/diagrams/tour-of-eda.drawio', title='Simplified device onboarding flow', page=2, zoom=1.5) }}-

> Device onboarding procedure is covered in the user guide and is not part of this tour.

You don't need to have the real hardware network devices to experience EDA capabilities thanks to the Digital Twin component that is part of the EDA platform. EDA Digital Twin allows users to run virtualized network topologies of arbitrary complexity and size and interact with them as if they were real devices.

The Try EDA environment that you set up earlier, comes with a Kubernetes cluster powered by KinD that hosts the EDA platform and the three node Digital Twin topology pre-installed and ready to use:

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='', page=0, zoom=1.2) }}-

> To learn more about EDA's Digital Twin and how to define virtualized topologies, refer to the [Digital Twin documentation](../digital-twin/index.md).

Regardless of whether you are using web UI or any of the automation/CLI tools, the interaction with the EDA system is carried out over the REST API exposed by the EDA API server or Kubernetes API server respectively. Users, however, don't need to interact with the nodes directly, as all node management operations are powered by EDA. This connectivity diagram in its simplified form presented below:

-{{ diagram(url='nokia-eda/docs/diagrams/tour-of-eda.drawio', title='', page=4, zoom=1.5) }}-

The topology that Try EDA provides consists of three Nokia SR Linux virtual routers connected in a leaf-spine architecture with distinct hardware types emulated for each layer. The topology also describes the links between the devices as well as from the leaf nodes to emulated hosts. The node names in the physical topology and their corresponding emulated hardware types that Try EDA comes with is illustrated below:

-{{ diagram(url='nokia-eda/docs/diagrams/tour-of-eda.drawio', title='Physical topology', page=3, zoom=1.8) }}-

## Node List

The simulator nodes are onboarded by EDA during the initial platform setup, so you should have them already managed by EDA. In the EDA UI you can navigate to the **Nodes** section under the **Targets** category to see the list of nodes entered in the EDA system and their status:

-{{ image(url='https://gitlab.com/-/project/7617705/uploads/8153d19669331376f18206f8e0681c2d/CleanShot_2026-01-03_at_17.15.37.png', title='Nodes list in EDA UI') }}-

The table lists the three nodes along with their current configuration and state values. Selecting a node -{{icons.circle(letter="1")}}- from the list and opening the information panel on the right side of the screen makes it easy to see the node details:

-{{ image(url='https://gitlab.com/-/project/7617705/uploads/0bf5972d4de3f7854bcb0b3b06dd8e99/CleanShot_2026-01-03_at_17.22.56.png', title='Node details', shadow="True", padding=20) }}-

such as:

-{{icons.circle(letter="2")}}- NPP connection state - shows whether the EDA control node is connected to the managed node via gNMI[^1].

-{{icons.circle(letter="3")}}- Node synchronization state. `Synced` status indicates that EDA has successfully applied the intended configuration to the node and its current state matches the desired state.

-{{icons.circle(letter="4")}}- Node management address that EDA uses to connect to the node.

-{{icons.circle(letter="5")}}- Node platform and OS details.

In the table view you can also see the `Simulate = True` value reported for all three nodes, indicating that these are virtualized nodes running in Digital Twin mode and not physical devices.

For CLI enthusiasts, the list of nodes can also be retrieved using the `edactl` or `kubectl`:

```bash
edactl -n eda get toponode
```

<div class="embed-result">
```{.text .no-copy .no-select}
NAME     PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE
leaf1    7220 IXR-D3L   25.10.1   srl   true        normal   Connected   Synced
leaf2    7220 IXR-D3L   25.10.1   srl   true        normal   Connected   Synced
spine1   7220 IXR-D5    25.10.1   srl   true        normal   Connected   Synced
```
</div>

## Node Labels

EDA allows its users to label[^3] any resource under its management to facilitate resource organization, filtering, and selection. Nodes are not an exception and you will find the labels assigned to each node in the Try EDA topology:

-{{ image(url='https://gitlab.com/-/project/7617705/uploads/f63977dba6a95b883e90cb3d324f0214/CleanShot_2026-01-06_at_12.06.25.png', title='Node labels in EDA UI', shadow="True", padding=20) }}-

> Labels are free-form key-value pairs that can be assigned to any resource in EDA.

Evidently, each node has a couple of labels assigned to it:

* `eda.nokia.com/role=leaf | spine` - denotes the role of the node in the topology. Since our Try EDA topology uses a leaf-spine architecture, the leaf nodes are labeled with `role=leaf` and the spine node with `role=spine`. Note, that `eda.nokia.com/` is a just a prefix that by convention uses a domain-like format to denote the ownership of the label. When you create your own labels, you can use any prefix you like or none at all.
* `eda.nokia.com/security-profile=managed` - indicates that the TLS certificates for these nodes are managed by EDA.

During the tour, you will see how `role` label is used in resource definitions to target specific nodes based on their role in the topology.

## Physical Topology

-{{image(url="https://gitlab.com/-/project/7617705/uploads/e15be3a70990106fd7acf50178a648d8/CleanShot_2025-12-18_at_13.41.27.png", title="Physical Topology view")}}-

Refer to the [Physical Topology](ui.md#physical-topology) section in the EDA UI page to read more about the topology view and how to interact with it.

## Node Configuration

As was discussed earlier, EDA is the authoritative source of truth for the configuration of the managed nodes. And while EDA does something smarter than just config templating and "replace at root" on each transaction, it still can display the full acting configuration on any managed node:

-{{video(url="https://gitlab.com/-/project/7617705/uploads/a7a005b4d85bcea1d56c1f57f07b18fd/node-config.mp4", title="Displaying node configuration from the Node List view")}}-

The configuration view has a toggle -{{icons.circle(letter="1")}}- that allows to switch from a simple configuration view to a "blame" mode where each configuration region is annotated with the resource name that resulted in that configuration being generated.

-{{image(url='https://gitlab.com/-/project/7617705/uploads/6b9d768ae31cd3efec1ed80db7626b86/CleanShot_2026-01-03_at_19.12.53.png', title='Node configuration with resource annotations', shadow="True", padding=20) }}-

The Interface resource[^2] named `leaf1-ethernet-1-1` and highlighted with -{{icons.circle(letter="2")}}- icon above is responsible for generating the configuration snippet shown next to it. This makes it easy to trace back any part of the node configuration to the resource that created it.

The node configuration can also be displayed from the terminal using [`edactl`](index.md#packing-the-tools) CLI tool:

```bash
edactl -n eda node get-config leaf1
```

## Node CLI

While EDA UI/API is the primary interface for all interactions with the managed nodes, there are scenarios where direct CLI access to the nodes is required for troubleshooting or verification purposes. Users can access the CLI of any managed node using the [`node-ssh` script](../digital-twin/index.md#connecting-to-the-digital-twin-nodes) that opens the SSH session from one of the EDA pods to the target node.

Setup the `node-ssh` script as described in the referenced section and then you can connect to any of the nodes in the topology. For example, to connect to the `leaf1` node, run:

```bash
node-ssh leaf1
```

<div class="embed-result">
```{.bash .no-copy .no-select}
Warning: Permanently added '10.254.32.151' (ED25519) to the list of known hosts.
(admin@10.254.32.151) Password:
Last login: Sun Jan  4 15:00:55 2026 from 10.254.12.87
Loading environment configuration file(s): ['/etc/opt/srlinux/srlinux.rc']
Welcome to the Nokia SR Linux CLI.

--{ + running }--[  ]--
A:admin@leaf1#

```
</div>

Username is set to `admin` and the password is `NokiaSrl1!`.

<div class="grid cards" markdown>

* :fontawesome-solid-route:{ .middle } **Where to next?**

    ---

    Now that we know how EDA manages network nodes, let's learn how EDA leverages declarative abstractions to ensure reliable and consistent network operations. Because imperative configuration management is a thing of the past!

    [:octicons-arrow-right-24: **EDA Resource Model**](resource-model.md)

</div>

[^1]: gNMI is currently the only supported protocol for device management in EDA, with support for other management protocols planned for future releases.
[^2]: Resources are the declarative units of automation and core building blocks of EDA. They represent the desired state that should be enacted on a target device. Refer to the [next section](resource-model.md) of the tour to learn more about resources in EDA.
[^3]: Kubernetes-style labels are used in EDA.
