# EDA Resource Model

-{{% import 'icons.html' as icons %}}-

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

EDA is an automation framework that is based on the principles of declarative configuration management with abstractions. An operator's input to the system declares the desired state of the resources and EDA takes care of the deployment process of the resources in a network-wide, consistent and transactional manner.  
In other words, you tell EDA what state you want your infra to be in, and the system carries out the "how" for you in a reliable and most efficient way.

At the core of EDA lies the concept of a Resource - a representation of various managed objects in a declarative and abstracted manner. In this section, we will explore the EDA Resource Model in detail including the founding principles of declarative configuration management and abstractions, that EDA is built upon.

## Declarative Configuration Management

Over the years, the industry has seen a significant shift towards declarative configuration management approach that is based on defining the desired state of system without specifying the exact steps to achieve that state. This paradigm shift has led to increased automation, reduced human error, and improved operational efficiency.

Network configurations have traditionally been managed using imperative methods where network engineers would write commands to configure the network services in a particular sequence to achieve the desired state. For example, a very simple task to configure descriptions on two interfaces would result in the following series of imperative commands:

```srl title="Imperative configuration example"
enter candidate
set / interface ethernet-1/1 description "First interface"
set / interface ethernet-1/2 description "Second interface"
commit now
```

In contrast, a declarative approach would involve defining the desired end state of the interfaces without specifying the exact commands to achieve that state. The state of the system can be expressed in many languages or formats, one common language is YAML where the same configuration could be expressed as follows:

```yaml title="Declarative configuration example"
interfaces:
  - name: ethernet-1-1:
    description: "First interface"
  - name: ethernet-1-2:
    description: "Second interface"
```

While this contrived example may seem trivial, the benefits of declarative configuration management become more apparent as the complexity of the configuration task increases. By defining the desired state of the network in a high-level language, network engineers can focus on what they want to achieve rather than how to achieve it. This shifts the burden of translating the desired state from a network engineer to the automation system that can manage the complexity much more effectively, reducing the likelihood of human error and ensuring consistency across the network.

## Abstractions

The declarative configuration management approach opens the door to building abstracted inputs to the system further simplifying the task of network configuration management. By creating higher-level, customer-specific, and vendor-agnostic abstractions network engineers can define complex configurations using simple, reusable building blocks tailored to their use cases.

Consider one specific example of an abstracted resource in EDA - "Fabric" - a high-level abstraction that represents a data center fabric. The Fabric represents the network-wide IP fabric configuration that includes:

- underlay network configuration such as routing protocol and its parameters, inter-switch link and loopback IP addressing, import/export policies
- overlay network configuration such as overlay routing protocol and its parameters

Here is an example of an input that defines a Fabric resource in EDA:

```yaml title="Fabric input example" linenums="1"
leafs:
  leafNodeSelector:
    - eda.nokia.com/role=leaf
spines:
  spineNodeSelector:
    - eda.nokia.com/role=spine
interSwitchLinks:
  linkSelector:
    - eda.nokia.com/role=interSwitch
  unnumbered: IPV6
systemPoolIPV4: systemipv4-pool
underlayProtocol:
  protocol:
    - EBGP
  bgp:
    asnPool: asn-pool
overlayProtocol:
  protocol: EBGP
```

In under 20 lines of YAML, the network engineer can define a complete data center fabric configuration that would translate to dozens of lines of imperative commands on all target devices to achieve the goal.

> Abstractions do not only simplify the configuration process but also promote vendor-agnostic service description, reusability, and consistency across different deployments.

While the concept of declarative configuration management and abstractions may seem simple in theory, implementing it in production setting can be quite complex. Take a simple task of configuring a Message Of The Day Banner on a set of network devices:

<div class="grid cards" markdown>

- :smiley_cat:

    ---

    :magic_wand: Configure MOTD banner :magic_wand:

- :scream_cat:

    ---

    - Ensure a user is authorized for the task
    - Parse & validate input
    - Identify target network devices for the operation
    - Translate abstracted input to node-specific commands
    - Push configuration to the target nodes in a concurrent and transactional manner
    - Ensure the transaction accepted on all nodes
    - Revert changes on any failure leaving the network in a consistent state
    - Display and monitor the status of the enacted configuration
    - Constantly watch for drift and remediate as necessary

</div>

The simple "intent" of configuring a banner translates to a complex series of steps that need to be orchestrated reliably across multiple network devices. This is where EDA excels by providing first-class support for vendor-agnostic, declarative configuration management and handling the complexity associated with these tasks.

## Resource Definition

Inspired by the [Kubernetes Resource Model](https://github.com/kubernetes/design-proposals-archive/blob/main/architecture/resource-management.md), EDA uses the concept of Resources to represent various managed objects in a declarative and abstracted manner.  
These abstractions allow network engineers to define the desired state of the network in a implementation-agnostic language, which is then translated into the necessary commands by the EDA platform.

/// admonition | What is a `Resource`?
    type: subtle-question
In EDA, a resource is an intent in a declarative format that can represent virtually anything:

- an interface on a network device
- a complete fabric configuration
- a network service like an L2 VPN
- and even non-network related resources like a user account, a DNS record, or a firewall rule.
///

Continuing with the banner example, to configure the MOTD banner on a set of network devices using EDA, a user would submit the following resource definition to the EDA API server:

-{{ diagram(url='nokia-eda/docs/diagrams/tour-of-eda.drawio', title='Banner resource', page=0) }}-

A resource definition in EDA has the following sections:

- **apiVersion**: Specifies the version of the API that the resource `kind` is coming from. The version consists of a group in form of a domain-like string and a version identifier.
- **kind**: Indicates the kind of resource being defined in this manifest. In this case, it is a "Banner" resource that resides in the API group `siteinfo.eda.nokia.com` of `v1alpha1` version. The combination of `apiVersion` and `kind` uniquely identifies the type of resource being defined.
- **metadata**: Contains information about the resource such as its name, namespace, labels, and annotations. This metadata is used to uniquely identify the resource instance within the EDA platform.
- **spec**: Defines the desired state of the resource. In this case, it includes the banner message and selects the target network devices to create the banner on.
- **status**: Represents the current state of the resource. This section is populated by the EDA platform (not the user) after the resource is created and constantly provides the feedback to the user as to the status of the resource. In the case of the Banner resource, the status section simply lists the nodes where the banner has been successfully created, but more sophisticated resources may have more complex status sections such as operational state, statistics, health indicators, etc.

## Resource Groups

Resource kinds in EDA are organized into versioned API groups based on their functionality and purpose. For example, the Banner kind resides in the `siteinfo.eda.nokia.com` group. Other API groups that you will find installed in the "Try EDA" instance include `fabrics.eda.nokia.com` for DC fabric-related resources, `protocols.eda.nokia.com` for routing protocols, `services.eda.nokia.com` for higher-level service abstractions, and many more.

These resource groups and the kinds they contain are distributed as **EDA Applications** that can be installed and managed via [EDA Store](../apps/app-store.md).

-{{ diagram(url='nokia-eda/docs/diagrams/tour-of-eda.drawio', title='EDA applications and resource kinds', page=1) }}-

By installing EDA apps the new resource kinds are added which extend the capabilities of the EDA instance and is a key enabler for EDA's extensibility. Extensibility through the pluggable apps ensures a mode of continuous innovation where new features and capabilities can be added to EDA without the need to upgrade the core platform.

## Resource Operations

EDA provides multiple ways to perform operations on resources ranging from Web UI and command line tools to various API clients. For new users, the Web UI is the most user-friendly way to explore and interact with EDA resources, however, we will also provide equivalent CLI commands for each operation for those who are more fluent with terminal tools.

As expected, EDA supports the full lifecycle of resource operations including: list, read, create, modify, and delete. Let's explore each of these operations in more detail.

### List

For instance, to [view](ui.md#resources-view) all Interface resources in the system find the -{{icons.circle(letter="I", text="Interfaces")}}- menu item in the side panel under the -{{icons.topology()}}- category:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/407f1acf862a2d86f817614bd1843944/CleanShot_2025-12-17_at_18.44.48.png", title="Resources page")}}-

The table lists all resources of the "Interface" kind in the system along with their key attributes such as name, labels, interface type/speed, and so on. You can click on any resource row to view its [details](ui.md#details-view) including the full YAML definition of the resource.

The same resources can be viewed using the `edactl` or `kubectl` command line tool:

```{.shell .no-select}
edactl -n eda get interfaces
```

<div class="embed-result highlight">
```{.text .no-select .no-copy}
NAME                      ENABLED   OPERATIONAL STATE   SPEED   LAST CHANGE
lag-leaf1-2-e1212-local   true      up                  100G    2025-12-12T20:11:44.932Z
lag-leaf1-e1011-local     true      up                  200G    2025-12-12T20:11:44.745Z
lag-leaf2-e1011-local     true      up                  200G    2025-12-12T20:11:42.504Z
leaf1-ethernet-1-1        true      up                  100G    2025-12-12T20:11:41.906Z
leaf1-ethernet-1-2        true      up                  100G    2025-12-12T20:11:41.958Z
leaf1-ethernet-1-3        true      up                  100G    2025-12-12T20:11:42.014Z
leaf1-ethernet-1-4        true      up                  100G    2025-12-12T20:11:42.098Z
leaf1-ethernet-1-5        true      up                  100G    2025-12-12T20:11:42.158Z
leaf1-ethernet-1-6        true      up                  100G    2025-12-12T20:11:42.210Z
leaf1-ethernet-1-7        true      up                  100G    2025-12-12T20:11:42.254Z
leaf1-ethernet-1-8        true      up                  100G    2025-12-12T20:11:42.318Z
leaf1-ethernet-1-9        true      up                  100G    2025-12-12T20:11:42.374Z
leaf2-ethernet-1-1        true      up                  100G    2025-12-12T20:11:39.673Z
leaf2-ethernet-1-2        true      up                  100G    2025-12-12T20:11:39.725Z
leaf2-ethernet-1-3        true      up                  100G    2025-12-12T20:11:39.777Z
leaf2-ethernet-1-4        true      up                  100G    2025-12-12T20:11:39.833Z
leaf2-ethernet-1-5        true      up                  100G    2025-12-12T20:11:39.905Z
leaf2-ethernet-1-6        true      up                  100G    2025-12-12T20:11:39.965Z
leaf2-ethernet-1-7        true      up                  100G    2025-12-12T20:11:40.033Z
leaf2-ethernet-1-8        true      up                  100G    2025-12-12T20:11:40.081Z
leaf2-ethernet-1-9        true      up                  100G    2025-12-12T20:11:40.149Z
spine1-ethernet-1-1       true      up                  400G    2025-12-12T20:11:41.865Z
spine1-ethernet-1-2       true      up                  400G    2025-12-12T20:11:41.925Z
spine1-ethernet-1-3       true      up                  400G    2025-12-12T20:11:39.629Z
spine1-ethernet-1-4       true      up                  400G    2025-12-12T20:11:39.689Z
```
</div>

### Read

To get the contents of a specific resource, click on its name in the Web UI to open the [details view](ui.md#details-view) where you can see the full definition of the resource (in schema and YAML/JSON formats) along with its status and other metadata.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/29b367bc96ecf3e8ac94a890320c4eec/CleanShot_2025-12-18_at_12.00.06.png", title="Resource details view")}}-

To read a specific resource in YAML format using the command line, use `kubectl` or `edactl` as follows:

```{.shell .no-select}
edactl -n eda get interfaces leaf1-ethernet-1-1 -o yaml
```

<div class="embed-result highlight">
```{.yaml .no-select .no-copy}
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Interface
metadata:
  labels:
    eda.nokia.com/role: interSwitch
  name: leaf1-ethernet-1-1
  namespace: eda
spec:
  enabled: true
  encapType: "null"
  ethernet:
    stormControl: {}
  lldp: true
# omitted for brevity
```
</div>

### Create

To create a new resource in EDA in the Web UI, select the desired resource kind in the left side panel and click on the **Create** button to open the resource creation form. In the form, you can either fill out the fields manually or edit the YAML directly. Both workflows can be mixed as the form fields and the YAML editor are synchronized in real-time.

Let's create a new Banner resource to configure the Message Of The Day banner on all leaf nodes in the network:

-{{video(url="https://gitlab.com/-/project/7617705/uploads/c53a06b905439a703393ccaf3b265750/create-banner.mp4", title="Creating a Banner resource")}}-

> To target only the leaf nodes, we used a label selector in the resource spec that matches all nodes with the label `eda.nokia.com/role=leaf`. The [nodes are labeled](nodes.md#node-labels) with leaf and spine roles in the Try EDA topology definition and you will have them available in your own EDA instance.

As the demonstration shows, we are directly committing the resource instead of adding the resource to the transaction basket. This means that the resource will be immediately transacted by EDA and if no errors are found during the deployment process you will see the new resource in the list of resources. We do not use dry-run mode or transaction basket in this example, as the transaction operations will be covered in more detail in the next chapter.

A CLI approach to create the same Banner resource can be performed using EDA's Kubernetes API using the `kubectl` command:

```bash
cat <<EOF | kubectl apply -n eda -f -
apiVersion: siteinfo.eda.nokia.com/v1alpha1
kind: Banner
metadata:
  name: my-banner
  namespace: eda
spec:
  motd: here is my message of the day!
  nodeSelector:
    - eda.nokia.com/role = leaf
EOF
```

This will create the Banner resource in the Kubernetes API server and synced to the EDA platform automatically. EDA then performs the necessary steps by validating and deploying the resource to the target nodes in the same way as in the Web UI example.

/// details | Checking the MOTD banner on the leaf nodes
Naturally, we want to verify that the MOTD banner has been actually configured on the leaf devices. There are several ways how users can interrogate the state of the managed devices in EDA, here are two simple methods:

//// tab | Using Web UI
As shown in the [Nodes chapter](nodes.md#node-configuration), EDA UI provides a web view of the running configuration of each managed node. For example, if we open the configuration viewer for `leaf1` node and search for `motd`, we can see that the banner has been successfully created on the device:

-{{video(url="https://gitlab.com/-/project/7617705/uploads/2fa5a5e816b918703b6c9e82fcfed650/view-conf.mp4", title="Ensuring the MOTD banner on leaf1 node")}}-
////
//// tab | Using Node CLI
Alternatively, using the [`node-ssh` script](nodes.md#node-cli) we can connect to the `leaf2` and verify the same:

```bash
node-ssh leaf2 eda
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy hl_lines="4"}
Warning: Permanently added '10.254.40.49' (ED25519) to the list of known hosts.
(admin@10.254.40.49) Password:
Last login: Fri Dec 19 15:15:54 2025 from 10.254.12.87
here is my message of the day!
Loading environment configuration file(s): ['/etc/opt/srlinux/srlinux.rc']
Welcome to the Nokia SR Linux CLI.
--{ + running }--[  ]--
A:admin@leaf2#
```
</div>

////
///

### Edit

To edit an existing resource in EDA using the Web UI, navigate to the resource details view and click on the **Edit** button to open the resource editing form. Similar to the creation form, you can either modify the fields manually or edit the YAML directly.

-{{video(url="https://gitlab.com/-/project/7617705/uploads/03dfd00518cff6e90e91cd95040a73d7/edit-banner.mp4", title="Editing a Banner resource")}}-

In the CLI-land, you can use the `kubectl apply` command to modify in-place an existing resource. For example, to update the MOTD message of the previously created Banner resource:

```bash
cat <<EOF | kubectl apply -n eda -f -
apiVersion: siteinfo.eda.nokia.com/v1alpha1
kind: Banner
metadata:
  name: my-banner
  namespace: eda
spec:
  motd: This message has been updated via kubectl!
  nodeSelector:
    - eda.nokia.com/role = leaf
EOF
```

### Delete

And finally, to delete a resource in EDA using the Web UI, navigate to the resource details view and click on the **Delete** button in the row menu. You will be prompted to select the delete operation mode - immediate commit

-{{video(url="https://gitlab.com/-/project/7617705/uploads/03651be686534afee972b5be4df74c22/delete-banner.mp4", title="Deleting a Banner resource")}}-

In the command line, you can delete the same Banner resource using the `kubectl delete` command and referencing the banner resource by its name and namespace:

```bash
kubectl -n eda delete banner my-banner
```

## Resource Composition

By now you probably saw a lot of different categories in the left side panel of the EDA UI with resource kinds representing various network and platform-related objects.

<figure markdown>
  [Nodes](#resource-composition){ .md-button } [NTP Clients](#resource-composition){ .md-button } [BGP Groups](#resource-composition){ .md-button } [Virtual Networks](#resource-composition){ .md-button }

  [DHCP Relays](#resource-composition){ .md-button } [Fabrics](#resource-composition){ .md-button } [Default Interfaces](#resource-composition){ .md-button } [Banners](#resource-composition){ .md-button } [Filters](#resource-composition){ .md-button }
  
  [Egress Policies](#resource-composition){ .md-button } [User-created resource](#resource-composition){ .md-button } [And so on...](#resource-composition){ .md-button }
  <figcaption>Example EDA Resources</figcaption>
</figure>

Some of these resources represent low-level building blocks such as interfaces, BGP groups, Policies, and so on, while others are higher-level abstractions such as Fabrics, Virtual Networks, and Bridge Domains that are composed of multiple lower-level resources. These resource composition is front and center in EDA's design and allows to reuse automation primitives to build more complex and sophisticated abstractions that can be tailored to specific use cases.

### Low-level resources

A simple low-level resource like a Banner that we used in the previous examples does not need to leverage any other resources to achieve its goal; it simply configures the banner on the target nodes as specified in its definition. However, even the Banner resource uses a particular utility resource - **NodeConfig** - that EDA engine uses to perform the configuration push to the target devices.

To help visualize the resource composition and dependencies, EDA UI provides a Resource Topology view that can be accessed from the resource details view:

-{{video(url="https://gitlab.com/-/project/7617705/uploads/c1398900509dc75d5ef4ccb2bd59397e/resource-topo1.mp4", title="Banner Resource Topology")}}-

The video shows how to display the resource topology for the Banner resource we have created earlier. Reading the topology diagram from bottom to top, we can see that the Banner resource that we created in the system generated a group of NodeConfig resources - one per each leaf switch - that contains the actual JSON configuration snippet to be pushed to the target devices.

> 1. The NodeConfig resources are not kept in the EDA DB for scale and performance reasons. You can only see their content in the transaction diffs.  
> 2. If you are curious to see how the Banner application works under the hood - have a look at the [Banner intent walkthrough](../development/apps/scripts/banner-script.md).

The low-level resources that result in concrete configuration changes on the target devices are used by higher-level resources to build more complex abstractions.

### Higher-level resources

A popular example of resource composition in EDA is the [Fabric resource](../apps/fabric.md) that we mentioned earlier. The Fabric is a high-level abstraction that represents a Clos-based EVPN VXLAN fabric of an arbitrary size. When a user creates a Fabric resource, EDA configures on the target devices multiple entities, such as:

- the IP underlay network including routing protocols, addressing, and policies
- the overlay protocol

In other words, it builds the L3 fabric that is ready to be configured with the overlay EVPN services such as L2/L3 VPNs.

The [Fabric resource documentation][fabric-app-docs] provides a detailed description of the resource, its attributes and behavior. To not repeat ourselves, proceed with creating a Fabric resource and leave the exploration of its attributes to a reader.

[fabric-app-docs]: ../apps/fabric.md

Recall, that you can create EDA resources using the Kubernetes API, the EDA API or through a Web User Interface (UI). This time let's use the Kubernetes API. Paste the below command in your terminal to create a Fabric resource named `myfabric-1` in the `eda` namespace.

Have a look at the Fabric resource input as it highlights the power of abstraction and declarative configuration. In twenty lines of YAML, we defined the entire fabric configuration, selected leafs/spine nodes and inter-switch links, chose the underlay and overlay protocols with their parameters.

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/examples/my-fabric.yaml"
EOF
```

///
/// tab | YAML

```yaml linenums="1"
--8<-- "docs/examples/my-fabric.yaml"
```

///

After a few moments, the Fabric resource should be created and transacted by EDA. You can verify that by listing the `my-fabric1` resources in the system using `kubectl`:

```bash
kubectl -n eda get fabric myfabric-1
```

<div class="embed-result highlight">
```{.text .no-select .no-copy}
NAME         LAST CHANGE   OPERATIONAL STATE
myfabric-1   1m            up
```
</div>

In EDA UI you will find the newly created Fabric resource with the name `myfabric-1` under the Fabrics category:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/3d29f9102195ca647144c682dac5bc37/CleanShot_2026-01-06_at_23.07.44.png",title="Fabric resource in EDA UI", padding=20, shadow="true")}}-

If you open the Fabric resource details view and navigate to the Resource Topology tab, you will see a complex graph of resources that were created as part of the Fabric resource deployment:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/a9d274f62dbda655847cfb0a6d2abb9e/CleanShot_2026-01-06_at_23.22.23.png",title="Fabric resource topology", padding=20, shadow="true")}}-

The entrypoint of the topology is the Fabric resource itself on the left side of the diagram. From there, you can see how the Fabric resource created multiple lower-level resources[^1] such as DefaultRouter, ISL, PrefixSet and other resources that in their turn emitted their sub-resources to build the complete fabric configuration on the target devices.

By leveraging resource composition, developers can build powerful abstractions while reusing existing building blocks, promoting consistency, and reducing complexity in the system.

## Resource State

We have discussed how to declaratively define and create resources in EDA by providing their metadata and desired specification of the resource. However, defining the desired specification is only part of the story, and often not even the most important one.

In addition to the desired configuration of a resource, EDA also maintain a representation of its current state reflected in the `status` field. This state information is crucial for operators to gain insights into the actual observed state and make informed decisions about the resource's health and performance.

You will often find the `status` field in resource definition to contain information such as:

- operational state (up/down)
- last change timestamp
- health indicators
- references to the related nodes where the resource is deployed

To illustrate the state fields and their significance, let's open the Fabrics view and select the `myfabric-1` resource that we created earlier. Open up the information panel on the right side of the table form to view the resource details, including its status:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/7383ae8de88a71d786c57a6fa5df870c/CleanShot_2026-02-01_at_10.36.50.png", title="Resource status")}}-

At first glance, the status information may seem trivial; who haven't seen an operational state field before on an interface, or BGP session, what's the big deal? The key is that the status field in this case is provided for the high-level Fabric resource that abstracts away multiple underlying resources and their states. The Fabric resource status aggregates the state information from all its sub-resources and presents a unified view of the overall health and operational state of the entire fabric.

Just by looking at the Fabric resource status, an operator can quickly assess whether the fabric is operational or if there are any issues that need attention. This abstraction simplifies the monitoring and management of complex network configurations by providing an operational insight at a higher level, the level that matters the most to the operator.

> However big or small your fabric is, EDA will provide its health and operational state in a single place, freeing the operational team from the burden of tracking and aggregating multiple low-level resources and their states.  

The state information is {==continuously updated==} by EDA as it monitors[^2] all resources and their deployment on the target devices. This dynamic, event-driven nature of the resource state fetching allows operators to have real-time visibility into the health and performance of their network configurations, enabling proactive management and troubleshooting.  
You will notice, that the real-time nature of handling resource data, be it configuration or state, is one of the core tenets of EDA. You can even see the real time updates happening in your browser as you look at the resource details view in EDA UI.  
The importance of being able to see the live state of the resources you used in the configuration cannot be overstated. Especially in the medium and large scale networks where the deployed services can include thousands of interfaces and sessions.

The live state received and processed by EDA can also be streamed out to external monitoring and analytics systems, because in EDA we eliminate the black boxes, not create new ones. The whole power of EDA's State Engine that continuously monitors and processes the resource state can be harnessed by external systems to build custom dashboards, alerts, and reports based on the live data.  
Check out the open source [EDA Telemetry Lab](https://github.com/eda-labs/eda-telemetry-lab/) that demonstrates how to export the live resource state from EDA to a Prometheus/Grafana stack for visualization and alerting.

-{{video(url="https://gitlab.com/-/project/7617705/uploads/14ebb6c0ea041736063f4d698494fc4c/422951112-38efb03a-c4aa-4a52-820a-b96d8a7005ea.mp4", title="EDA Telemetry Lab demo")}}-

The short video demonstrates the Grafana panel that is backed by the live data exported from EDA showing the health and operational state of various resources in the system.

<div class="grid cards" markdown>

- :fontawesome-solid-route:{ .middle } **Where to next?**

    ---

    The EDA Resource Model is a foundational concept hence we spent a good amount of time exploring its various aspects. Now we are ready to move on to another important topic - Transactions in EDA.

    [:octicons-arrow-right-24: **Transactions**](transactions.md)

</div>

[^1]: Also known as sub-resources or child-resources.
[^2]: Using Streaming Telemetry
