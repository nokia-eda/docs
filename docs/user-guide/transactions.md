# Transactions

## Introduction

Transactions form the foundation of EDA's powerful revision control system and add sought-after reliability to infrastructure automation by applying the changes atomically, network-wide.  
Every action that leads to a config change in EDA - modifying a resource, installing an EDA application, upgrading a network operating system - is processed as a transaction.  

At a very high-level, EDA transactions have three main steps:

1. Generate config from abstractions
1. Deploy config changes, network-wide
1. Commit to Git for revision control

In EDA, deploy and commit are inseparable. If the change is not deployable on any of the target node, the whole transaction is pronounced failed and the changes are reverted from all nodes. This means users can't commit changes that the network can't apply — every commit to Git is a point-in-time of the network's configuration history.[^1]  
With a single command, you can roll back the entire network from the commit history. Your maintenance window back out just got a whole lot easier!

/// details | Details of the transaction steps
    type: abstract

1. Generate config from abstractions
    * Run all configuration intent scripts which have a dependency on the resources in the transaction.[^2]
    * Compile node configurations pieces from the intent scripts' outputs into full node configurations.
    * Perform YANG schema validation on the full node configurations. If schema is invalid, transaction fails here.
1. Deploy config changes, network-wide
    * Push new configuration to all nodes with commit confirmation.
    * If any node rejects the new config, transaction fails here and EDA performs a network-wide roll-back.
1. Commit to Git for revision control
    * Create a Git commit
    * Push commit to remote Git server(s) for backup
///

### What's in a Transaction Commit?

Whenever you create/update/delete a resource in EDA, a number of scripts associated with this resource run. We call these scripts "intents".

Intents have strict idempotency where every intent run with the same set of inputs will result in the same set of outputs. Always.
Therefore EDA has no need to persistently store anything that can be derived or computed.  
EDA stores intent scripts, input resources, and pool allocations in Git - and that's it![^3]

Yes, that's right, EDA does not backup node configs - we simply don't need them for revision control and omitting those large repetitive files lets us scale the Git repo to very large networks.

### Transaction Basket

Multiple EDA resource changes can be applied together to fate-share a set of changes. The EDA UI uses a basket to represent this. When committing from the basket all resources are applied as a single transaction - if the transaction fails, none of the changes from the basket are committed.

For REST API and Kubernetes users, the basket concept can be used via the [Transaction API](https://rest.wiki/?https://raw.githubusercontent.com/eda-labs/openapi/refs/tags/v-{{eda_version}}-/core/core.json) and [the Transaction CRD](https://crd.eda.dev/transactions.core.eda.nokia.com/v1), respectively.

## Transaction Results

### Summary

EDA stores the result of a transaction for users to review. Here is some of the terminology you'll find in the results:

* Input Resources - Resources created, updated or deleted by the user.
* Intent Runs - Configuration scripts executed during the transaction.
* Output Resources - Resources derived from the intent run.
* Changed Resources - Input and Output resources that are changed, compared to the previous committed transaction.
* Nodes with Changes - Nodes which are impacted by this transaction. This includes node configuration changes, node version changes, or changes to the associated TopoNode resource in EDA.

Error Types:

* Intent Errors - Errors returned by an intent script
* Node Config Errors - Error in YANG schema validation or errors returned by the node when pushing configuration
* General Errors - Errors related to the EDA environment

### Diffs

Diff of all changed resources and changed node configurations in the transaction.

### Transaction Topology

Transaction Topology displays all input and output resources of a transaction and graphs the relationship between derived and parent resources.

Changed resources are colored yellow in the topology, and if an intent error occurred during the transaction the related resource is colored red.

-{{image(
    light_url="https://gitlab.com/-/project/74406595/uploads/89ea69512ee49bb65bad416ad7da065a/image-2.webp",
    dark_url="https://gitlab.com/-/project/74406595/uploads/3c1b5ec13f7573b2b88ba765fc7f893d/image-1.webp",
    padding=20,shadow=true
)
}}-

/// details | Transaction Topology Limitations
    type: info

1. Transaction Topology graphs the createUpdate relationships between resources. Read relationships are not graphed.  
For example: The Fabric intent reads from allocation pool resources. The link between the Fabric resource and the allocation pool resources is not displayed in the topology.

1. Transaction Topology is not currently available for transaction results with more than 1000 resources.
///

### Detail Level

For all transactions committed to Git, EDA can always display the input resources and their diffs.  
Data not in Git (e.g. failed transaction, dry-run transactions, output resources, node configuration diffs, etc.) are stored in-memory for a limited time. EDA uses the following rules for retaining detailed transaction results:

* Keep a guaranteed 25 transactions per user[^4]
* Keep diffs for a maximum 10k resources per user — details from the oldest transactions will be purged if this limit is exceeded

Additionally, transactions from 'machine interfaces' do not contain detailed results. This includes resource changes via the `/apps` REST API endpoint and changes via Kubernetes.

### The NodeConfig Resource

NodeConfig is a special resource in EDA that is not published to EDB or Kubernetes but you will often see in transaction results. These function as an internal configlet which intent scripts create to contribute specific sections of node configuration. EDA combines all the nodeConfig resources into a complete node configuration. This is why you'll see both 'NodeConfig' and 'Node Configuration' in the transaction diffs.

## Dry-Run

What if you want to review the configuration changes before pushing to the network? That's where dry-run comes in.
Any transaction can be executed as a dry run. This performs all config generation and YANG schema validation, but does not push any changes to the network.

## Revert and Restore

EDA exposes 'Revert' and 'Restore' actions for each committed transaction:

* Revert sets all the input resources from a specific transaction back to the previous commit. Note: If changes were made to the resource in a more recent transaction, those changes will also be reverted.
* Restore sets all EDA resources, apps, and allocations to exactly as they were at the specified commit.

Both actions are executed as a new transaction and committed with a new commit hash, i.e., the commit history always moves forward even if the transaction is a roll-back of changes.

[^1]: "But what if I change config outside EDA?"  
Don't worry, EDA detects the deviation and commits it to the transaction log should the deviation be accepted or rejected.
[^2]: Configuration intent scripts use the latest commit and the transaction input to derive resource and pieces of node configuration. The term 'declarative abstraction' is often used to describe this process.
[^3]: Additional data is stored in Git (User settings, user created dashboards, KeyCloak DBs, etc.) but these are not relevant to transactions.
[^4]: If there are outstanding in-progress transactions, a user can temporarily have more than 25 transactions
