# Network-wide Transactions

-{{% import 'icons.html' as icons %}}-

Many will find EDA's Atomic Transactions feature one the most exciting ones. And for the good reasons!

How many times have you been staring at a long-running configuration pipeline that goes and applies changes box by box, or pool by pool, only to have it fail at one device because of a minor misconfiguration, incompatibility or a transient resource issue?  
How many hours have been invested in finding the root cause of such failures, coming up with the clean-up steps and rolling back the partially deployed changes?  
How many hours have been invested to create an idempotent configuration pipeline that can perform a guaranteed rollback in case of a failure in a complex service deployment?  
And how much easier would it be if these challenges were handled automatically by the system?

Network-wide Transactions in EDA were designed to solve exactly these challenges faced by every operator on a regular basis.

## Reconciliation vs Transactions

To appreciate the value of EDA's Network-wide Transactions, it is important to understand the difference between reconciliation-based and transaction-based approaches to network automation.  
If you have been following the recent trends in network automation, you have probably noticed the increasing popularity of reconciliation-based approaches boosted by the popularity of Kubernetes, declarative paradigm, and GitOps.

The idea behind the reconciliation pattern is simple: instead of writing imperative steps to configure a service on a set of devices that run from some automation server in one-off fashion, you declare the desired state of the same service and let the "controller" reconcile the actual state of the network with the desired state.  
The process of identifying the delta between the actual and desired states and applying the necessary changes to converge the two states is called reconciliation loop.

A popular implementation of the reconciliation loop is the Operator pattern popularized by Kubernetes. To illustrate the reconciliation loop, consider the following diagram where a user submits the desired state of a resource to the system, and the Operator reconciles (applies necessary changes to) the actual state of the resource to match the desired state.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/b80daae9e1b9a8d40bfc4b985e6cc454/CleanShot_2026-02-01_at_12.37.00.png", title="Reconciliation loop", padding=20, shadow=true)}}-

Imagine, that a user wants to deploy a web server with three replicas across the worker nodes in a Kubernetes cluster. The user would submit a manifest declaring this intent and the Operator in Kubernetes would create the necessary components to realize this intent. And _eventually_ the actual state of the cluster would converge to the desired state.  
The emphasis on "eventually" has been put for a reason. The reconciliation loop may take time to converge the states, and _sometimes it may never converge_ to the desired state if there are persistent issues preventing the deployment.

This case is illustrated above with the `worker1` node not being able to start the web server pod due to, for example, insufficient resources. This would result in the actual state never matching the desired state of three replicas and only two web servers being available.

Running two web servers instead of three may sound acceptable in some scenarios, if there is ample time to fix the underlying issue and let the reconciliation loop converge the states. However, {==every network operator knows they can't afford partially applied changes==}.  
In the network world, partially applied changes may lead to service outages, security vulnerabilities, and compliance violations. Therefore, network operators need stronger guarantees that either all changes are applied successfully, or none of them are applied at all. This is where EDA's Network-wide Transactions come into play.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/e7db2b14c83850de170bc323e7e5be5b/CleanShot_2026-02-01_at_19.47.08.png", title="Network-wide Transactions", padding=20, shadow=true)}}-

In EDA, the declarative network management principles meet the strong consistency guarantees of atomic transactions. Whenever a user submits a resource manifest to EDA, the platform creates a transaction with the calculated changes required to converge the actual state of the network with the desired state declared in the manifest. The transaction is then executed across all affected devices in the network in an atomic, all-or-nothing fashion.  
No guesswork and no unnecessary tokens thrown at a problem that can be solved with some good old engineering to guarantee the safety and reliability of operations.

> In EDA, every action that results in the node config change benefits from the atomic transaction guarantees provided by the platform.

Let's work through an example of how Network-wide Transactions work in EDA. Imagine, that an operator needs to add a new customer in a data center network spanning multiple switches along with the necessary ACL entries to enforce security policies. The operator would add a set of resources reflecting the desired state of the network to the transaction basket in EDA and submit the transaction for execution.

Before the first network request is made, EDA will perform a set of validations.

* It ensures that the provided input intents match the schema and no fat fingering happened to the input data.  
* It checks dependencies between the resources, e.g. the referenced IP pool is not depleted, the selected target node exists, etc.  
* Then it will calculate the necessary node-level changes to be applied on each target device and these changes will undergo the semantic and syntactic validation based on the targeted platforms and their YANG model.

If all these validation pass, the transaction will transition to the deploy phase.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/a69bccadf0214e9cbf49e2f9c25b9fd2/CleanShot_2026-02-01_at_21.09.45.png", title="Creating a transaction", padding=20, shadow=true)}}-

In the deploy phase, the transaction will target all affected devices in the network . EDA will concurrently apply the changes across all devices in the transaction, ensuring that the changes will be attempted on all devices at the same time. Even though the extensive set of validations performed before the deploy phase significantly reduces the chances of failure during the configuration push, failures may still happen due to nature of model-based checks and hardware resource constraints, transient network issues, or self-inflicted communication path failures.

This is where EDA's Network-wide Transactions shine. When EDA applies the changes on each device, it uses gNMI Commit Confirmed extension so that each successful commit requires an explicit confirmation from EDA within a specified confirmation timeout window. Continuing with our example, let's imagine that first device successfully applied the changes and transitioned to the "waiting for confirmation" state. The third device hasn't yet processed its commit set, while the second device failed to apply the changes due exhausted TCAM resources:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/d8fbbc0ee08726d7190b856eec1a7b4e/CleanShot_2026-02-01_at_21.10.26.png", title="Transaction failure during deploy phase", padding=20, shadow=true)}}-

Because one of the devices failed to apply the transaction change set, EDA is immediately notified of the failure and initiates the rollback phase of the transaction. The rollback in this case is as simple as sending the gNMI Commit Cancel message to all devices that either successfully applied the changes or are still in the process of applying them. Once the devices receive the Commit Cancel message, they will automatically revert to the previous configuration state, ensuring that no partial changes are left in the network.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/616cc193c914158cc1627dddf9e0c4b0/CleanShot_2026-02-01_at_21.10.42.png", title="Transaction rollback phase", padding=20, shadow=true)}}-

The network remains in a consistent state, with no partial changes applied, and the operator can investigate the root cause of the failure without worrying about cleaning up after a partially applied configuration.

> Did you know that Nokia EDA team contributed[^1] the gNMI Commit Confirmed extension to the OpenConfig?

In summary, each operation in EDA is put through a rigorous validation and check process with multiple safety barriers to ensure the the malicious or accidental misconfigurations are minimized to the greatest extent possible. As all transactions share fate, no matter how big or small the change set is, how big or small the target set of devices is, EDA will ensure the atomicity of the changes and record the successful transaction in its persistent Git repository for future audits and rollbacks.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/0eb4fe8eadef4768bcca6d6634d2e568/CleanShot_2026-02-01_at_23.46.54.png", padding=20, shadow=true)}}-

## Working With Transactions

With the good theoretical primer behind us, it is time to see the transactions in action. We will work through a simple task of enabling the `ethernet-1/20` interface on both `leaf1` and `leaf2` switches in our data center fabric.  
If you recall from the [Nodes chapter](./nodes.md), both `leaf1` and `leaf2` switches have ports from 1 to 12 enabled and acting either as uplink or server-facing ports, while the rest of the ports are not even configured[^2].

```srl title="Interface ethernet-1/20 has not been configured"
--{ + running }--[  ]--
A:admin@leaf1# info /interface ethernet-1/20

--{ + running }--[  ]--
A:admin@leaf1#
```

### Transaction basket

To add an interface go to the -{{icons.circle(letter="I", text="Interfaces")}}- resource page in the left side menu and click on "Create" to fill in the details for the new interface resource for `leaf1`:

-{{video(url="https://gitlab.com/-/project/7617705/uploads/9bff4143b21745f10199c2f109c6cc52/select-interface.mp4", title="Creating a new interface")}}-

In the editing mode, we will fill in the necessary information to define the new interface resource. To keep things simple, we will paste the following YAML snippet in the editor:

```yaml
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Interface
metadata:
  namespace: eda
  name: leaf1-ethernet-1-20 #(3)!
spec:
  enabled: true
  type: interface
  encapType: dot1q
  lldp: true
  members:
    - enabled: true
      lacpPortPriority: 32768
      interface: ethernet-1-20 #(1)!
      node: leaf1 #(2)!
```

1. We set the `interface` field to `ethernet-1-20` which is the normalized, vendor-agnostic interface name that is transformed to the vendor-specific interface name by EDA during the configuration push.
2. We set the `node` field to `leaf1` to target the first leaf switch in our fabric.
3. We set the resource `name` to `leaf1-ethernet-1-20` to uniquely identify this interface resource in EDA.

> When editing resources in EDA, the resource definition is matched against its API schema. This is the first validation step that ensures the resource definition adheres to its schema before it is added to the transaction basket.

After pasting the YAML snippet or filling the schema form, click on "Add" button to add the new interface resource to the transaction basket.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/7f4ece52ca56379a9dd31e68285a0f5d/CleanShot_2026-02-02_at_11.11.33.png", title="Adding to basket", padding=20, shadow=true)}}-

By adding a resource to the transaction basket you are staging the resource for inclusion in the next transaction. No configuration changes are being pushed yet. Continue with adding the second interface resource for `leaf2` switch by repeating the same steps as above, but changing the `name` and `node` fields accordingly.

After adding both interfaces to the transaction basket, you should see the counter next to the basket icon in the top right corner of the EDA UI indicating that there are two staged resources waiting to be committed. Clicking on the basket icon will open the transaction basket popup where you can review the staged resources, perform operations on them (edit, delete), or proceed with transaction operations.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/e190a96b0c2d3a5b3894661cea357555/CleanShot_2026-02-02_at_11.19.43.png", title="Transaction basket with two staged resources", padding=20, shadow=true)}}-

> [EDA REST API](../development/api/index.md) and [EDA Ansible collections](../development/ansible/index.md) has full support for managing transactions.

### Dry run

When you have the resources in your transaction basket workspace you could straight away commit them and let the platform do its magic. But among the things that operators don't want to have is magic and surprises when provisioning their networks.

Acknowledging this fact, EDA provides a "Dry run" feature that allows operators to preview the changes that would be applied to the network without actually applying them. This is a great way to validate the intended changes before committing them to the network.

To initiate a dry run, click on the dropdown selector next to the "Commit" button and choose "Dry run" option:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/90b15669ec1a2d380efd2a7a990f2ea1/CleanShot_2026-02-02_at_14.54.27.png", title="Initiating a dry run", padding=20, shadow=true)}}-

EDA will start processing the resources in the basket's workspace and run another validation as part of the dry run. This validation includes schema validation using node's YANG models that EDA is aware of. Things like data types, ranges, mandatory fields and other constraints defined in the YANG models of the target devices are checked during this validation step.

In a few moments, EDA will present the dry run results in the same popup window, from where a user can either proceed with committing the transaction upon a successful dry run, or look at the transaction details and diffs to understand the scope of the changes in the basket workspace.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/5ee9d096cc5bf45b1c4154247f943260/CleanShot_2026-02-02_at_15.10.31.png", title="Dry run results", padding=20, shadow=true)}}-

Let's start with the diff view, and leave transaction details for when we submit the actual transaction.

### Diff

Clicking on the "Diffs" icon will pop up a new window with the calculated diffs that would look like this:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/6ae6e8251c624e8e821935c58239ad63/CleanShot_2026-02-02_at_15.43.27.png", title="Transaction diffs", padding=20, shadow=true)}}-

The diff view is split in two panes, on the left side we have the list of resources affected or created by the transaction and on the right side we have the familiar text diff view showing the exact changes in the "before/after" format for each resource.

The "Node Configuration" diffs are always at the top of the list as they represent the actual configuration changes that will be applied to the target devices. In our case, we have two new interfaces being created on `leaf1` and `leaf2` nodes respectively, and the diff shows the exact configuration snippets that will be added (in this case) to the running configuration of each device.

> Being able to see the detailed diff as a result of a dry run removes another layer of uncertainty from the network operations process, showing the proposed changes in a familiar format.

Besides the Node Configuration diffs, we also have diffs for the resources being created or modified in this transaction. Like the Interface resources that we added to the transaction can be found in the list of resources in the left pane.

### Committing the transaction

Based on the dry run diff review an operator may want to edit the resources in the basket workspace to adjust the parameters and re-run the dry run until satisfied with the proposed changes. Once ready, the operator can proceed with committing the transaction by clicking on the "Commit" button in the transaction basket popup.

Pulling up the transaction basket will now show the "Commit" without the dropdown selector as we have already performed the dry run and haven't changed anything in the basket workspace since then.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/9c821579778c2086692a4f9cc90f324e/CleanShot_2026-02-02_at_16.09.52.png", title="Committing the transaction", padding=20, shadow=true)}}-

The commit process will look similar to the dry run, however, this time EDA will proceed with pushing the changes to the target devices using the Network-wide Transactions mechanism described earlier.  
After clicking on the "Commit" button, EDA will show the transaction progress in the same popup window and display the final transaction result once the transaction is confirmed by all target devices.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/2a0a104a50fee511723e8a200c2e9d01/CleanShot_2026-02-02_at_16.18.08.png", title="Transaction commit", padding=20, shadow=true)}}-

After the transaction is successfully committed, you can click "Done" to close the transaction basket popup and return to the main EDA UI.

If you were to go and check the configuration on both `leaf1` and `leaf2` switches, you would see that the `ethernet-1/20` interfaces are now present and enabled:

```srl
--{ + running }--[  ]--
A:admin@leaf1# info /interface ethernet-1/20
    admin-state enable
    vlan-tagging true
```

### Transaction list

The Git repository that backs up EDA transactions deserves its own chapter which we will leave for later. For now, all that is important to know is that every committed transaction is persisted in the replicated EDA's Git repository.

You will find the transaction list right at the top section of the left side menu in the EDA UI, clicking on it will pull up the transaction list[^3]:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/fb23e941fbd0cd474ef429b30d9294e9/CleanShot_2026-02-02_at_19.44.23.png", title="Transaction list", padding=20, shadow=true)}}-

Attentive readers will notice that the transaction list contains both the transactions that were run in the dry run mode as well as the committed ones. Also both successful and failed transactions are listed here for audit and troubleshooting purposes.  
With every transaction having the incremental identifier it is easy to track the sequence of changes applied to the network over time.

Double-clicking on a transaction entry will pull up the transaction details view where all the information about the transaction can be found:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/78040bb22f256adb3358bb027bbe6851/CleanShot_2026-02-02_at_19.48.14.png", title="Transaction details", padding=20, shadow=true)}}-

The detailed transaction view covers a lot of ground. First, on the panel with the big checkmark status you see the transaction ID and its commit status. The panel to the right shows transaction KPI-s, like

-{{icons.circle(letter="1")}}- Number of input resources provided to the transaction. The transaction we are looking was recorded as a result of us adding two Interface resources a moment ago, hence the value of 2 here.

-{{icons.circle(letter="2")}}- Number of EDA application runs that were involved in processing this transaction.

-{{icons.circle(letter="3")}}- Number of emitted resources that were created as a result of EDA applications working on the input resources.

-{{icons.circle(letter="4")}}- Number of resources that have been changed as part of this transaction. This includes both created and modified resources.

-{{icons.circle(letter="5")}}- How many topology nodes were affected by this transaction. Read it as "on how many devices changes were applied".

-{{icons.circle(letter="6")}}- In the Transaction Details tab you will find the actual resources for which the KPIs were calculated.

-{{icons.circle(letter="7")}}- With the top bar toggle you can change the view from transaction details to diffs or transaction topology graph.

-{{icons.circle(letter="8")}}- The "advanced" toggle will show additional internal resources participating in this transaction if available.

It is always a good idea to start with the transaction list when experiencing unexpected issues in the platform, since some transactions may be triggered automatically by the system and not directly by the user.

### Restores and reverts

We mentioned earlier that EDA persists every committed transaction in its Git repository. And many of you will immediately guess where we are going with this.

Git is perfect for maintaining the change history and being able to revert to any previous state when needed. EDA leverages this capability of Git to provide operators with the ability to rollback or revert transactions as needed.  
No matter how far back in time you need to go, how many resources were created since, or how many nodes were added - EDA can effectively go back in time to any point in time and bring the network to state recorded at that time.

EDA exposes `Revert` and `Restore` actions for each committed transaction:

* `Revert` sets all the input resources from a specific transaction back to the previous commit[^4]
* `Restore` sets all EDA resources, apps, and allocations to exactly as they were at the specified commit

Both actions are executed as a new transaction and committed with a new commit hash, i.e., the commit history always moves forward even if the transaction is a roll-back of changes.

The easiest way to access these actions is from the transaction details view where the `Revert` and `Restore` actions are available in the context menu of each committed transaction:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/b3c5f102d13f90d2d656a0f268d8688f/CleanShot_2026-02-02_at_20.34.50.png", title="Revert and Restore actions", padding=20, shadow=true)}}-

In the screenshot above, the selected transaction is the one where we created the two interfaces on `leaf1` and `leaf2` switches. Let's say we realized that we made a mistake and these interfaces are not needed after all. We could've gone to the interface list and deleted them, but in case your transaction involved multiple resources or changes were made to some existing resources, then reverting the transaction is a much easier and safer option.

If we were to click on the "Revert" we would see the dialog asking us to choose between a dry run or an actual revert operation.

> Even rollback and revert operations can be first tried out to add that extra safety layer.

Click on "Revert" and EDA will create a new transaction that "reverts" the changes and you could check the config on the nodes to ensure that the `ethernet-1/20` interfaces are no longer present.

As explained above, the Revert operation reverts a single transaction, while Restore brings the entire EDA platform back to the state recorded at the specified transaction.

## Network-wide Transaction Example

What about our promise to manage transactions in the all-or-nothing fashion with strong consistency guarantees and automatic rollback in case of failures? To see this in action we would need to simulate a sudden communication loss from EDA to one of the target devices during the transaction commit phase, or fabricate a wrong configuration input that the node would reject during the commit. The latter is easier to simulate, so let's do that.

Let's populate our transaction basket workspace with three Interface resources this time. If you rolled back the `ethernet-1/20` interfaces on leaf1 and leaf2 switches, you can re-add them to the basket, and add a third Interface resource for `spine1` that would look like this:

```yaml
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Interface
metadata:
  namespace: eda
  name: spine1-ethernet-1-99
spec:
  enabled: true
  type: interface
  encapType: dot1q
  lldp: true
  members:
    - enabled: true
      lacpPortPriority: 32768
      interface: ethernet-1-99
      node: spine1
```

Do you see the induced mistake? There is no `ethernet-1/99` interface on the 7220 IXR D5 platform that `spine1` switch is running, and this "error" won't be intercepted by the dry run or schema validation, since the port range constraints are not part of the YANG model of the device.

With three interfaces in our basket, let's first run a dry run to see the diffs:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/0a22d2b2acf5d13f8b750e6da314dc74/CleanShot_2026-02-02_at_21.53.40.png", title="Dry run with an invalid interface", padding=20, shadow=true)}}-

The dry run completes successfully, and the diffs shows that the node configuration change targeting the `spine1` switch will attempt to add the `ethernet-1/99` interface. Let's see what happens if we were to proceed with the change:

-{{video(url="https://gitlab.com/-/project/7617705/uploads/220844599b0c9ddf76c95543b7af5337/network-wide.mp4", title="Committing transaction with an invalid interface")}}-

As you can see, the whole transaction has been pronounced as failed as all the resources in the transaction share the same fate, and a failure on one target caused the entire transaction to fail. The failed transaction also did not let any partial changes to be applied to the network, that can be validated by checking the list of the interface in the EDA as well as on the nodes themselves.

<div class="grid cards" markdown>

* :fontawesome-solid-route:{ .middle } **Where to next?**

    ---

    The Tour of EDA is far from over, but we are busy working on the next chapters. In the meantime, feel free to explore other parts of the documentation, connect with the EDA PLM team and our lovely community [in Discord](https://eda.dev/discord) or [check out YouTube](https://www.youtube.com/results?search_query=nokia%20eda) for video tutorials and webinars.

</div>

[^1]: https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-commit-confirmed.md
[^2]: You can ensure this by [checking the node configuration](./nodes.md#node-configuration) from the EDA UI.
[^3]: Check the [Transactions](../user-guide/transactions.md) documentation for more details on which transactions are listed and the details shown there.
[^4]: If a more recent transaction made changes to any of the input resources, revert will fail. This prevents 'undoing' changes that are not part of the selected transaction.
