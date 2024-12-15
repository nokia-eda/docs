# Units of automation

EDA is an automation framework that follows declarative principles. An operator's input is the desired state of the resources and EDA takes care of the deployment, provisioning, configuration and reconciliation of the resource.  
In other words, you tell EDA what state you want your infra to be in and EDA carries out the "how" for you in a reliable and most efficient way.

/// admonition | What is a `Resource`?
    type: subtle-question
In EDA, **a resource is a unit of automation** and can represent virtually anything:

- an interface on a network device
- a complete fabric configuration[^1]
- a network service like a VPN or a VRF[^2]
- and even non-network related resources like a user account, a DNS record, or a firewall rule.
///

As a Kubernetes citizen, EDA represents its resources via [Custom Resources (CRs)][CR-k8s-doc] of Kubernetes that can be created using multiple methods including the Kubernetes (K8s) API, the EDA API, or through a User Interface (UI).

You probably wonder what resources are available in EDA and how to interact with them. Great question!  
EDA resources become available as soon as you install an [**EDA Application**](../apps/app-store.md) which is a way to extend EDA with new resources and capabilities on the fly. Applications may be provided by anyone: Nokia, our partners or indie developers - EDA is an open platform!

Nothing beats a hands-on experience, so let's learn more about Resources by following a short but powerful example of configuring a fabric on top of our 3-node topology deployed as part of our [playground](try-eda.md).

## A Fabric resource

You heard it right! We will configure a DC fabric using a single EDA resource in a fully declarative and reliable way. The Fabric resource is a high-level abstraction that allows you to define a fabric configuration suitable for environments ranging from small, single-node edge configurations to large, complex multi-tier and multi-pod networks.

/// admonition | What is a Fabric?
    type: subtle-question
To put it simply, a Fabric resource represents a DC fabric configuration with all its components like:

- a set of leaf and spine devices
- allocation pools for system IPs, ASN numbers
- inter-switch links flavor (numbered, unnumbered, vlans)
- underlay protocol (eBGP, IGP)
- overlay protocol

At the end of the day, a Fabric resource defines and configures everything a DC fabric needs to support overlay networks or L2/L3 services.
///

The [Fabric resource documentation][fabric-app-docs] provides a detailed description of the resource, its attributes and behavior. To not repeat ourselves, we will proceed with creating a Fabric resource and leave the exploration of its attributes to a reader.

Recall, that you can create EDA resources using the Kubernetes API, the EDA API or through a User Interface (UI). Let's start with the Kubernetes API.

## Creating a resource with Kubernetes API

To create a resource via the Kubernetes API, you must first define a Kubernetes Custom Resource (CR) specific to your needs. As we set ourselves to create a Fabric resource, we need to define a Fabric CR using our [Fabric resource documentation][fabric-app-docs].

To create the abstracted declarative definition of our Fabric in EDA we will use `kubectl`[^3] CLI tool. Paste the below command in your terminal to create a Fabric resource named `myfabric-1` in the `eda` namespace.

Have a look at the Fabric CR input below as it highlights the power of abstraction and declarative configuration. In twenty lines of simple YAML, we defined an entire Fabric configuration, selected which leafs and spines, what inter switch links to select, and chose the underlay and overlay protocols.

/// tab | `kubectl`

```bash
cat << 'EOF' | tee my-fabric.yaml | kubectl -n eda apply -f -
--8<-- "docs/examples/my-fabric.yaml"
EOF
```

///
/// tab | YAML

```yaml linenums="1"
--8<-- "docs/examples/my-fabric.yaml"
```

///

Just like that, in a single command we deployed the Fabric resource, as we can verify with:

```bash
kubectl -n eda get fabric myfabric-1 #(1)!
```

1. You can see the Fabric with the name `myfabric-1` in the EDA UI as well under the Fabrics section.

    ![f1](https://gitlab.com/rdodin/pics/-/wikis/uploads/52dc36bedf67aab0078e9b7ebd29f9a7/image.png)

<div class="embed-result highlight">
```{.text .no-select .no-copy}
NAME         LAST CHANGE   OPERATIONAL STATE
myfabric-1   1m            up
```
</div>

Ok, we see that the Fabric resource named `myfabric-1` has been created in our cluster, but what exactly has happened? Let's find out.

Without getting you overwhelmed with the details, let's just say that EDA immediately recognized the presence of the Fabric resource and turned an abstracted declarative Fabric definition to dozens of important fabric-related sub-resources.  
The sub-resources in their turn have been translated to the node-specific configuration blobs and were pushed in an all-or-nothing, transactional manner to all of the nodes in our virtual topology; all of this in a split second.

You see the power of abstraction and automation in action, where the complex configuration task is reduced to a single declarative statement that is reliably transacted to the nodes, just as it should be.

/// admonition | "I don't think that the Fabric should be abstracted like that"
    type: subtle-note
It is absolutely fine if your view how the Fabric abstraction should look like is different from ours. EDA doesn't tell you how to do your infrastructure automation, EDA is here to help you do it.

Leveraging the power of [pluggable applications](../apps/app-store.md), you can create your own Fabric abstraction and use them to configure your fabric in a way that is most convenient for you.
///

Now, when the abstracted and declarative input has been processed by EDA, a fully functional Fabric configuration has been deployed on the nodes of our virtual topology.  
Don't take our word for it, let's connect to the nodes and check what config they have now. Do you remember that all the nodes in our fabric [had no configuration](virtual-network.md#initial-configuration) at all? Let's see what changed after we applied the fabric resource:

//// details | Checking the running configuration on `leaf1`
    type: code-example
We can connect to the nodes with a single command like `make leaf1-ssh` and check the running configuration with `info` command:

```{.srl .code-scroll-sm }
--8<-- "docs/getting-started/leaf1-config-post-fabric-create.cfg"
```

The result of the deployed Fabric app is a fully configured BGP EVPN fabric that is configured on all of the nodes in our topology.

We can list the BGP neighbors on `leaf1` to see that it has established BGP sessions with `leaf2` and `spine1`.

```srl
--{ + running }--[  ]--
A:leaf1# show network-instance default protocols bgp neighbor *
--------------------------------------------------------------------------------------------------------------------------------------------
BGP neighbor summary for network-instance "default"
Flags: S static, D dynamic, L discovered by LLDP, B BFD enabled, - disabled, * slow
+----------------+-----------------------+----------------+------+---------+-------------+-------------+-----------+-----------------------+
|    Net-Inst    |         Peer          |     Group      | Flag | Peer-AS |    State    |   Uptime    | AFI/SAFI  |    [Rx/Active/Tx]     |
|                |                       |                |  s   |         |             |             |           |                       |
+================+=======================+================+======+=========+=============+=============+===========+=======================+
| default        | fe80::53:beff:feff:1% | bgpgroup-ebgp- | D    | 101     | established | 0d:0h:16m:2 | evpn      | [0/0/0]               |
|                | ethernet-1/1.0        | myfabric-1     |      |         |             | 2s          | ipv4-     | [2/2/1]               |
|                |                       |                |      |         |             |             | unicast   | [0/0/0]               |
|                |                       |                |      |         |             |             | ipv6-     |                       |
|                |                       |                |      |         |             |             | unicast   |                       |
| default        | fe80::53:beff:feff:2% | bgpgroup-ebgp- | D    | 101     | established | 0d:0h:16m:2 | evpn      | [0/0/0]               |
|                | ethernet-1/2.0        | myfabric-1     |      |         |             | 2s          | ipv4-     | [3/2/3]               |
|                |                       |                |      |         |             |             | unicast   | [0/0/0]               |
|                |                       |                |      |         |             |             | ipv6-     |                       |
|                |                       |                |      |         |             |             | unicast   |                       |
+----------------+-----------------------+----------------+------+---------+-------------+-------------+-----------+-----------------------+
Summary:
0 configured neighbors, 0 configured sessions are established, 0 disabled peers
2 dynamic peers
```

////

Everything a fabric needs has been provisioned and configured on the nodes in a declarative way, taking the inputs from the abstracted, sweet and short Fabric CR that everyone can understand.

## State of a resource

Too often, the automation platforms are built solely around the configuration problem, leaving state handling to a different set of applications. In EDA we believe that the state of a resource is as important as the configuration, and state-triggered automation is a key part of the EDA's philosophy.

Be it a higher-level abstracted resource such as Fabric or a lower-level Interface, you will find the state reported for every EDA-managed resource. The relationship between the resource's specification and its state allows us to work with the abstracted configuration **and** the abstracted state.

Take the recently deployed Fabric resource which spans multiple nodes, and consists of multiple sub-resources. How do we know that the Fabric is healthy? Checking the operational status of every BGP peer and every inter-switch link is not a practical approach.

In EDA, the application developer can define the rules to calculate the state of a resource and populate the resource with this information. By looking at the Fabric's state field an operator can confidently determine the health of the Fabric, without having to inspect the configuration of every single node.

Users can access the status of a resource using `edactl`, `kubectl`, or UI.

/// admonition | `edactl`
    type: subtle-info
Not all resources are published into K8s and therefore it is recommended to use `edactl` to view the status of resources. EDActl is a CLI tool that runs in the [toolbox pod](../user-guide/using-the-clis.md#accessing-the-clis) in a cluster and provides a way to interact with the EDA API.
///

To leverage `edactl`, paste the following command into your terminal to install a shell alias that would execute `edactl` in the toolbox pod each time you call it.

```{.shell .no-select title="Install <code>edactl</code> alias"}
alias edactl='kubectl -n eda-system exec -it $(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}") \
-- edactl'
```

Now we can inspect the created Fabric resource using both `edactl` and `kubectl`.

/// tab | `edactl`

```{.shell .no-select}
edactl -n eda get fabrics myfabric-1 -o yaml
```

<div class="embed-result highlight">
```{.yaml .no-select .no-copy hl_lines="9 24"}
kind: Fabric
metadata:
  annotations: {}
  name: myfabric-1
  namespace: eda
spec:
# -- snipped --
status:
  health: 100
  healthScoreReason: |
    Breakdown:
    Metric "ISL Health", weight: 1, score: 100, calculation method: divide
    Metric "DefaultRouter Health", weight: 1, score: 100, calculation method: divide
  lastChange: "2024-12-15T17:24:50.000Z"
  leafNodes:
  - node: leaf1
    operatingSystem: srl
    operatingSystemVersion: 24.10.1
    underlayAutonomousSystem: 102
  - node: leaf2
    operatingSystem: srl
    operatingSystemVersion: 24.10.1
    underlayAutonomousSystem: 100
  operationalState: up
  spineNodes:
  - node: spine1
    operatingSystem: srl
    operatingSystemVersion: 24.10.1
    underlayAutonomousSystem: 101

```
</div>


///
/// tab | `kubectl`

```bash
kubectl -n eda get fabrics myfabric-1 -o yaml
```

The output will be the same as with `edactl`, but this is because the Fabric resource was "the input" resource, and EDA publishes those resources into K8s.

///

Note, how the `health` and `operationalState` of the whole Fabric resource is reported in the `status` field. Having the abstracted state is as important as the configuration, since it allows operators to focus on the important information, without having to inspect the configuration of every single node or component of a composite resource.

The operational state can have different values that would help an operator to determine the health of the Fabric. It is totally up to the application developer to define what status is reported for a given resource based on what is relevant for the application.

And, of course, the same information can be layed out nicely in the UI using resources dashboards (you guessed it, they are also customizable by the application developer).

![f2](https://gitlab.com/rdodin/pics/-/wikis/uploads/9059831c586c27cd6a1f7914c7ce66e8/image.png)

With a glance at the Fabric's dashboard an operator can determine the state of the whole fabric, without having to inspect a dozen of dashboards in a separate system.

## Transactions

The Kubernetes reconciliation loop mechanism offers a way to enable the declarative approach for the infrastructure management. Define the desired state of the infrastructure stack, in the Kubernetes Resource Model, apply it, and the corresponding controllers start to reconcile the actual state of the infrastructure with the desired state.  

Sounds great, but what if the desired state is not achievable? What if you deploy a workload with three replicas, but your infrastructure at the moment can only host two of them? The reconciliation loop will keep trying to reconcile the desired state with the actual state, and while it reconciles, you end up living with just two replicas running.

Doesn't sound like a big deal? Yes, maybe if you deploy three web servers and have two only two of them running for some time it is not the end of the world. But in the networking world, having a partially deployed service is a big, big problem.

- What if your CPM filter is partially deployed?
- What if your routing policy has been deployed on a subset of edge nodes?
- What if your service has been added to 100 out of 110 leafs?

In EDA every configuration change is done in an **all-or-nothing** fashion and transacted in Git. Always.  
If the desired state is not achievable even on a single target node, the whole transaction is pronounced failed and the changes are reverted immediately from all of the nodes.  
The transactions are network-wide.

When you create any resource, EDA automatically initiates a transaction and publishes its result. To view the list of existing transactions, use `edactl`:

```{.bash .no-select}
edactl transaction
```

<div class="embed-result highlight">
```{.text .no-copy}
 ID  Result  Age     Detail   DryRun  Username    Description
 27  OK      56h37m  SUMMARY          workflow    [workflow 10] Installing App: services.nokia: v2.0.0+24.12.1 (catalog=eda-catalog-builtin-apps)
 28  OK      56h37m  DEBUG            workflow    [workflow 9] Installing App: protocols.nokia: v2.0.0+24.12.1 (catalog=eda-catalog-builtin-apps)
 29  OK      56h37m  DEBUG            kubernetes
 30  OK      56h37m  DEBUG            kubernetes
 31  OK      56h37m  DEBUG            kubernetes
 32  OK      56h36m  DEBUG            kubernetes
 33  OK      56h36m  DEBUG            kubernetes
 34  OK      56h35m  DEBUG            kubernetes
 35  OK      56h35m  DEBUG            kubernetes
 36  OK      1h22m   DEBUG            kubernetes
```
</div>

The transaction list shows the transaction ID, the status and the user who initiated the transaction. The transaction ID can be used to view the details of the transaction, including the changes made to the resources.
Transactions are sequential and can be viewed in the order they were initiated.

What did we do last in this quickstart? Created a Fabric resource!  
Let's see what the latest transaction has to say about it:

```{.bash .no-select .code-scroll-sm}
edactl transaction 36
```

<div class="embed-result highlight">
```{.yaml .no-copy}
input-crs:
    gvk: fabrics.eda.nokia.com/v1alpha1, kind=Fabric name: myfabric-1 action: CreateUpdate
intents-run:
  - fabrics.eda.nokia.com/v1alpha1, kind=Fabric, myfabric-1
    output-crs:
    - fabrics.eda.nokia.com/v1alpha1, kind=FabricState, myfabric-1
    - fabrics.eda.nokia.com/v1alpha1, kind=ISL, isl-leaf1-spine1-1
# clipped
    pool-allocs:
    - template: Index:asn-pool name: global key: myfabric-1-spine value: 101
    script:
    - execution-time: 18.688ms
  - fabrics.eda.nokia.com/v1alpha1, kind=ISL, isl-leaf1-spine1-1
# clipped
  - routingpolicies.eda.nokia.com/v1alpha1, kind=PolicyDeployment, policy-ebgp-isl-import-policy-myfabric-1-node-spine1
      output-crs:
      - core.eda.nokia.com/v1, kind=NodeConfig, policy-cfg-ebgp-isl-import-policy-myfabric-1-spine1
      script:
      - execution-time: 26.559ms
nodes-with-config-changes:
  - name: leaf1
  - name: leaf2
  - name: spine1
general-errors:
commit-hash: 0b0e155356a3b451e05b5aafacb92188729fecf4
execution-summary: intents-run: 43, nodes-changed: 3, engine-time=135.150566ms, push-to-node=2.045243438s, publish-cr=27.772µs, git-save=543.984017ms
timestamp: 2024-12-15 17:24:41 +0000 UTC [2024-12-15T17:24:41Z] - 1h23m ago
result: OK
dry-run: false
```
</div>

You will see a lot of details, some of them we clipped from the output to keep it short, but essentially the transaction logged the input resource (kind=Fabric name: myfabric-1) and the output products of this resource being created (output-crs). Each of these outputs constitute a Fabric resource.

At the very end of the transaction output you will see the identified nodes that are affected by this change and the result of the transaction. Since the result is OK, we are rightfully see the resulting configs applied to the nodes in our virtual network.

## Creating a resource in UI

You've seen how to create a resource using the k8s API, and were introduced to the concept of transactions. Now, let's see how we can change an existing resource, perform a dry-run and finally commit the changes.

Usually quickstarts show some simple operations to keep the flow clean and simple, like adding a VLAN to a switch. We won't bother you with these basics, instead lets swap the overlay protocol for every node in our Fabric from eBGP to iBGP with a single operation.

<div class="iframe-container">
<iframe width="853" height="480" src="https://www.youtube.com/embed/ls0mQKKxfXM" title="EDA UI Resource change workflow" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

Here is what happened in these 60 seconds:

1. We've found the `myfabric-1` Fabric resource created earlier with `kubectl` in the UI under the <kbd>Fabrics</kbd> section.
2. We opened the resource and navigated its configuration schema all the way to the <kbd>Overlay Protocol</kbd> section.
3. We changed the overlay protocol from eBGP to iBGP and provided the required iBGP bits such as ASN number, Router ID.
4. We also provided the labels for the nodes that should be used as RR (route reflector) and RR clients; Our topology has been labeled with `role: spine` and `role: leaf` when we deployed it.
5. Instead of applying the change right away, we added it to the transaction basket. We could've added more changes to it, but for now we were ok with a single change.
6. Before applying the change we ran the Dry-Run, which started the process of unwrapping the abstracted high-level Fabric resource into the sub-resources and dependent resources.
7. The dry-run provided us with the extensive diff view of the **planned changes** to the nodes and all sub-resources touched by our single protocol change.
8. We've reviewed the diff and decided that it is good to commit the change.
9. Once we committed the change, we ensured that the change was immediately applied to the nodes by looking at `leaf1` show output and seeing how iBGP appeared in the output of peer neighbors.

/// admonition | Have a look at the Fabric dashboard
    type: subtle-note
Once the change is committed, BGP will take some time to converge. During this period you can see the [resource's state](#state-of-a-resource) in action by opening a Fabric dashboard and observing how the Fabric status transitions from "Degraded" to "Healthy".
///

Transactions made by a user in the UI[^5] are also visible in the Transactions UI[^4]:

![tr-ui](https://gitlab.com/rdodin/pics/-/wikis/uploads/aeb1dfb9ae61f6e43de48ed276175384/image.png)

Congratulations, your fabric is now using iBGP as its overlay protocol :partying_face:  
From a tiny change in the Fabric' declarative abstraction through the transformation to sub-resources and eventually to the node-level configurations, that are reliably transacted and pushed to the constituent nodes. How cool is that?

[CR-k8s-doc]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
[fabric-app-docs]: ../apps/fabric.md
[vnet-app-docs]: ../apps/virtualnetwork.md

[^1]: Like the [Fabric resource][fabric-app-docs] documented in the Apps section.
[^2]: Like the [Virtual Network resource][vnet-app-docs] documented in the Apps section.

[^3]: You can find the `kubectl` CLI tool in the `tools` folder of your playground repository.  
    You can copy it to the `/usr/local/bin` dir to make it globally available.
[^4]: Soon you will be able to see the transactions made via the k8s API as well, when the relevant permissions are granted.
[^5]: Transactions made via kubectl will be visible in the UI in a later release.
