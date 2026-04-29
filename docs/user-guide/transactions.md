# Transactions

Transactions form the foundation of Nokia Event-Driven Automation (EDA)'s configuration deployment and revision control. Transactions applying configuration changes atomically, network-wide.

At a very high-level, Nokia EDA transactions perform the following functions:

- Generate configuration from abstractions
- Deploy configuration changes, network-wide
- Commit to Git for revision control

Every action that leads to a network configuration change - modifying a resource, installing a Nokia EDA application, upgrading a network operating system - is processed as a transaction.

Within Nokia EDA, ConfigEngine is the main service behind transactions. Its job is to compute the complete set of resources that must be modified, deleted, or created as part of the transaction; ensure all dependencies and outputs are captured; and then transact the updates.

Changes within a transaction must succeed or fail together. If the change is not deployable on any of the target nodes, the whole transaction is pronounced failed and the changes are reverted from all nodes.

### Commits

When you Commit, the complete transaction, including all of its constituent configuration changes, then succeeds or fails as a unit. If any part of the transaction fails, the whole transaction is rolled back.

Whether the transaction succeeds or fails, you can view the detailed results of the transaction including the node configuration diffs. For a failed transaction, you can review the errors to revise the configuration changes in support of another attempt.

Only successful commits are stored in Git for revision control. This means you cannot commit changes that the network cannot apply, and every commit to Git is a point-in-time of the network's configuration history.

### Dry runs

Nokia EDA allows you to perform a dry run of any transaction. A dry run can reveal anticipated configuration issues if the transaction were to proceed normally, and allow you to troubleshoot any errors before committing the transaction on actual resources.

In a dry run, the system does not send any of the configuration changes to the managed nodes. However, it executes the transaction against Nokia EDA's stored information about each participating resource and validates the results against the managed nodes' YANG schema.

After the dry run is complete, transaction details and diffs are available just as with a normal commit.

### Transaction results

Nokia EDA provides the following summary information for completed transactions:

- **Input Resources** are resources created, updated, or deleted by the user.
- **Intents Run** are configuration intent scripts executed during the transaction.
- **Output Resources** are resources derived from the intents run.
- **Changed Resources** are input and output resources that are changed, compared to the previous committed transaction.
- **Nodes Affected** are nodes which are impacted by this transaction. This includes node configuration changes, node version changes, or changes to the associated `TopoNode` resource in Nokia EDA.

Diffs for changed resources, and node configurations of affected nodes are available in the transaction.

Failed transactions may include the following error types:

- **Intent Errors** - Errors returned by an intent script
- **Node Config Errors** - Error in YANG schema validation or errors returned by the node when pushing configuration
- **General Errors** - Errors related to the Nokia EDA environment

/// admonition | Note
    type: subtle-note
Output Resources often include internal Nokia EDA resource that are not user-facing. For example, a Nokia EDA configuration intent may create a "state" resource that initializes the process for reporting operational status.
///

/// admonition | Note
    type: subtle-note
`NodeConfig` is a special resource in Nokia EDA that is not published to EDB or Kubernetes, but that you will often see in transaction results. `NodeConfig` functions as an internal configlet that intent scripts create to contribute specific sections of node configuration. Nokia EDA combines all the `NodeConfig` resources into a complete node configuration. This is why you will see both 'NodeConfig' and 'Node Configuration' in the transaction diffs.
///

#### Retention period

Whenever you create, update, or delete a resource in Nokia EDA, a number of scripts associated with that resource run. These scripts are called "intents". Any intent that is run with the same set of inputs will always result in the same set of outputs. Therefore, Nokia EDA does not need to persistently store anything that can be derived or computed. Nokia EDA persistently stores intent scripts, input resources, and pool allocations in Git. Other data (e.g. failed transactions, dry-run transactions, output resources, node configuration diffs, etc.) is stored in-memory for a limited time.

There are three named detail levels, which indicate the available data for any given transaction:

- **Detailed** includes full transaction results
- **Standard** does not include the changed resources list, changed resource diffs, and node configuration diffs
- **Basic** includes only data committed to Git

Transactions created from the Nokia EDA GUI include **detailed** results by default. Transactions created with the Nokia EDA API or Kubernetes interfaces include **standard** results by default.

After a certain number of transactions, Nokia EDA reduces older transactions to the **basic** level. Failed and dry-run transactions are purged from this history during this clean-up.

- Details are retained for each user's 25 most recent transactions. Reduce details from any older transactions.
- When more than 10,000 resource diffs are in memory, reduce details from the oldest transactions until there are less than 10,000 resource diffs.

### Revert

The **Revert** action exists to reverse the changes in a specific transaction. On revert, Nokia EDA creates a new additive commit that sets the input resources from a specific transaction back to their previously committed value.

However, if there have been subsequent changes to resources being reverted, this can produce unexpected results. To avoid this, Nokia EDA always causes such a revert action to fail. To revert such a transaction, first revert any subsequent transactions that affected the same resources.

/// admonition | Note
    type: subtle-note
Executing a Revert operation requires Read-Write permission for all input resources in the transaction.
///

### Restore

The **Restore** action selects a specific past commit and sets all Nokia EDA resources, apps, and allocations to exactly as they were at the specified commit.

/// admonition | Note
    type: subtle-note
Executing a Restore operation requires readWrite permission for the transaction restore API endpoint.
///

## Transactions in the Nokia EDA GUI

Several elements within the Nokia EDA GUI support the creation and management of transactions.

- When you make any change to a resource, Nokia EDA offers choices to:

    - **Commit**: immediately commit the configuration change (performing a transaction with just this change)

    - Perform a **Dry Run** of the change

    - **Add to Basket**: add the resource change to a set of resources stored in the **Transactions Basket**. These can be included together in a transaction that you commit later.

- The **Basket** icon at the top of the Nokia EDA GUI indicates how many resource changes are pending. Clicking the icon opens the **Transactions** basket.

- Any resource that is in the Basket will display a basket icon beside its name in a corresponding resource list.  If a resource has been un-selected in the basket in order to exclude it from the transaction, this icon is not displayed beside the resource.

    -{{image(url="graphics/sc0465.png", title="A resource list showing the basket icon", shadow=true, padding=20, scale=0.4)}}-

- The **Transaction Log** displays a record of past transactions.

- The **Transaction Summary** page displays details about one, selected transaction

- The **Transaction status bar** displays at the top of any configured resource page, and allows you to view past states for the same resource that were associated with past commits.

### The Transactions basket

When one or more resource configuration changes have been added to the **Transactions** basket to be part of a transaction, and that transaction has not yet been committed, the **Basket** icon is highlighted and displays a count of the resources selected for inclusion in the transaction.

-{{image(url="graphics/sc0476.png", title="The basket showing one pending resource change", shadow=true, padding=20, scale=0.6)}}-

/// admonition | Note
    type: subtle-note
Adding a change to the basket does not mean it must be committed at the same time as all of the other changes already in the Basket.  You can decide before committing the transaction to include, or exclude, individual resources in the Basket from the transaction.  Any resources in the basket that are not committed now can be committed later as part of a different transaction.
///

You can open the **Transactions** basket by clicking the **Basket** icon.

From the **Transactions** basket you can:

- review the changes in the basket
- add a commit message to the transaction
- perform a dry run transaction
- commit the transaction
- create a merge request
- discard the changes in the basket
- view a list of recently completed transactions

You can also manage the individual resources within the **Transactions** basket. You can:

- from the actions menu, edit a resource
- from the actions menu, delete a resource (removing it from the basket)
- select or un-select any resource, so that it will be included in, or excluded from, the transaction

You also use the **Transactions** basket to view the **Transaction Log**.

-{{image(url="graphics/sc0466.png", title="The Transactions basket", shadow=true, padding=20, scale=0.5)}}-

<!-- Missing Add to merge request in table below.  For that:
"Merge Request - generate a merge request from the transaction.
This empties the users basket and redirects the UI to the merge request that was created as a result." -->

Table: Elements of the Transactions basket

|#|Description|
|---|-----------|
|1|**Clear Basket** button: click to clear all resource configuration changes from the Basket.|
|2|**Log** button: click to open the **Transactions Log**.|
|3|**Actions** menu for the Basket.  Click and select either of the following: <ul><li>**Import Basket Items** to import a set of resources and their configurations from a JSON file you have prepared beforehand.</li><li>**Export basket items** to export the contents of the basket to a JSON file.</li>|
|4|**Select/un-select all resources**: Click this to toggle between select and un-selecting all of the resources in the basket.|
|5|**Resource selectors**: Check or un-check the box beside a resource to include that resource in, or exclude it from, the transaction.|
|6|**More** button for a resource: click <ul><li>**Edit** to modify the set of changes you are requesting for this resource as part of the transaction</li><li>click **Delete** to remove this resource and the planned changes from the basket</li>|
|7|**Delete Items** button: click to remove only the selected resources from the basket.|
|8|Transaction options:<ul><li>**Dry Run**: perform a dry run to evaluate the effects of the transaction before committing.</li><li>**Commit**: proceed with updating the selected resources as part of transaction.</li><li>**Create merge request**: create a merge request consisting of the selected resource configuration changes, and empty the basket. The merge request can be performed as a transaction later on the **Merge Requests** page.</li></ul>|

/// admonition | Note
    type: subtle-note
When your transaction is in progress, a blue dot pulses beside the Basket icon. If the transaction is successful, the dot disappears. If the in progress transaction fails while the basket is closed, the blue dot becomes a red dot to notify the user.
///

#### Adding resource changes to the Basket

/// html | div.steps

1. Create, edit, or delete any resource in the Nokia EDA GUI.

2. Select the **Add to Basket** action on the configuration form or delete prompt.

The configuration change for this resource is added as an item in the basket. The change is not applied until you run commit the basket.

#### Commit changes

Clicking **Commit** commits all of the currently selected resources in the basket as a single transaction.

Whether the transaction succeeds or fails, you can view the details for the transaction, and the diffs that resulted from it. For a failed transaction, you can edit each row within the transaction to revise the configuration changes in support of another attempt.

Closing the transaction basket dismisses the basket, but retains information about the most recent commit. If changes occur to the basket contents, any commit information is cleared and it is restored to the normal list view.

#### Dry-run changes

Clicking **Dry Run** performs a [dry run transaction](#dry-runs) of all the currently selected resources in the basket.

After the dry run is complete, transaction details and diffs are available just as with a normal commit.

Closing the Transaction basket dismisses the form, but retains information about the most recent dry run. If changes occur to the basket contents, any dry run information is cleared and the form is restored to the normal list view.

<!-- Updated this image for 26.4; minor cosmetic changes -->

-{{image(url="graphics/sc0469.png", title="A sample result of a dry run", shadow=true, padding=20, scale=0.5)}}-

Table: Elements of the dry run results display

|#|Description|
|---|-----------|
|1|**Details** button: click to open the Details view for this transaction.|
|2|**Diffs** button: click to open the Diffs view for this transaction.|
|3|**Commit** button: as before the Dry Run, use this to proceed with the validated transaction.|

#### Recent transactions

Click on the **Recent** tab to view a list of the most recent transactions from the current user. A more complete list of transactions is available from the [Transactions log](#transactions-log).

### Transactions Log

The **Transactions Log** displays a list of past transactions and is visible to all authenticated users.

The following information displayed in the transactions log:

|Column|Description|
|------|-----------|
|Transaction ID |A unique ID for the transaction assigned internally.|
|Transaction type|Whether the transaction was a dry run or commit. In a dry run, the system does not send any of the configuration changes to the managed nodes. However, it executes the transaction against Nokia EDA's stored information about each participating node, and validates the transaction against that data.|
|Status|Whether the transaction was successful, or failed.|
|Description|An optional description provided at the time the transaction is committed.|
|Created by|The originator of the transaction. This could be a specific user, or a Nokia EDA component such as "workflow" or "admin" or "kubernetes".|
|Completion Timestamp|The date and time the transaction was completed.|
|State|The state of the completed transaction.|
|Commit Hash|A unique string that identifies this transaction in the Nokia EDA repository.|

/// admonition | Note
    type: subtle-note
The Transactions log retains the complete details of past transactions only for the most recent 25 transaction for each user. All successfully committed transactions are still retained in the list beyond that limit, but display only "Basic" details. Dry-run and failed transactions are not retained after the 25 limit. See [Transaction results](#retention-period) for more information.
///

#### Transaction row actions

For each row in the Transaction log, a set of actions available from the **table row actions** menu:

- **Details**, which opens the [Transaction Summary](#transaction-summary) page showing detailed information for one transaction.
- **Diffs**, which opens the changed resource and node configuration diffs for this transaction.
- **Revert**, [reverts](#revert) the changes in this transaction. A confirmation dialog displays before the Revert operation proceeds.
- **Restore**: [restores](#restore) all configurations to a specific transaction commit. A confirmation dialog displays before the Restore operation proceeds.
- **Add to Basket**: adds the transaction's input resources to the [Transaction Basket](#the-transactions-basket). This allows you re-try the transaction (or a modified version of a previous transaction).
- **Export Basket Items**: exports the transaction's input resources to a JSON file. The Basket includes an option to import the contents of such a file.

### Transaction Summary

While the **Transaction log** is a list of past transactions, the **Transaction summary** page shows detailed information about a single transaction.

-{{image(url="graphics/sc0474.png", title="The Transactions summary page", shadow=true, padding=20)}}-

This includes:

- The completion status, the name of the transaction, any description provided, and a timestamp for its completion.

- If there were errors, an Error Summary panel showing the number of:
    - General errors: errors related to the EDA environment
    - Intent errors: errors returned by an intent script
    - Node configuration errors: Errors in YANG schema validation, or errors returned by the node when pushing configuration

- A Resource Summary panel, showing the number of:
    - Input Resources: resources created, updated or deleted by the user
    - Intents Run: configuration scripts executed during the transaction
    - Output Resources: resources derived from the intent run
    - Changed Resources: input and output resources that are changed, compared to the previous committed transaction

You can enable the **Advanced** toggle at the top of the page to hide internal Nokia EDA resources from the results.

The advanced toggle is applicable to the **Diffs**, **Transaction Topology**, and resource lists in the **Details** view. It does not filter the counters in the **Resource Summary** of the **Details** view.

#### Details

The errors and resources that are summarized at the top of the Summary page can be viewed in detail in the Transaction Details panel. Different tabs display lists of input resources, changed resources, intents run, nodes affected, and errors.

The information displayed can be [Detailed, Standard, or Basic](#retention-period). When only Basic or Standard results are available, a banner at the top of the Transaction Details page explains that this limitation is in effect.

#### Diffs

From the breadcrumb at the top of the Transactions summary page you can select **Diffs** to view the **Transaction diffs** view.  This view shows details of the specific configurations changes that were part of this transaction.

-{{image(url="graphics/sc0472.png", title="The Transaction Diffs view", shadow=true, padding=20)}}-

Each changed CR and resulting node configuration change as part of this transaction is displayed, along with a diff view representing the new or changed lines in the respective configuration data.  Lines shaded red were removed or changed; lines shaded green were added.

<!-- 3502 Inline diffs view -->

A pair of buttons at the top right of the **Transaction diffs** page allows you to switch between a side-by-side and inline view of the changes.

/// admonition | Note
    type: subtle-note
Output Resource diffs are only visible to users if they have read access to all Input CRs for the transaction.
///

/// admonition | Note
    type: subtle-note
Node Configuration diffs are only visible to users if they have read access to the transaction nodeconfig diff API endpoint.
///

#### Topology

From the breadcrumb at the top of the **Transactions Summary** page you can select **Topology** to view the set of resources affected by the transaction and their relationships.

Resources are displayed as nodes within the topology.

Links in the **Transaction Topology** page represents resource relationships established by the intent runs where:

- endpoint A represents the resource which triggered the intent script
- endpoint B represents the resource that was updated or created by the intent script

Changed resources are shaded yellow in the topology.

If an intent error occurred during the transaction, the resource that triggered the intent script is shaded red.

-{{image(
    light_url="graphics/transaction-topology-light.webp",
    dark_url="graphics/transaction-topology-dark.webp",
    padding=20,shadow=true
)
}}-

/// admonition | Note
    type: subtle-note
The **Transaction Topology** page only graphs createUpdate relationships. For example, when a fabric intent creates ISL resources, this is represented as links between the fabric resource and those ISL resources.

The **Transaction Topology** page does not graph Read relationships. For example, when a fabric intent reads information from allocation pool resources, the links between the fabric resource and allocation pool resources are not illustrated in the **Transaction Topology** page.
///

Some elements in the illustration represent a group of resources. Click the **+** at the upper right of such elements to expand the group and see the complete set of individual resources.

Additional information about any selected element or connection within the transaction topology is available from the **Information** panel.

### The Transaction status bar

Every committed resource configuration is associated with a particular transaction. As you alter the resource over time, it accumulates a permanent commit history representing all the versions of itself that were ever committed as part of the current and past transactions.

By default, viewing a resource in Nokia EDA shows the latest version of that resource. But you can view past versions of the same resource using the transaction status bar at the top of the page to view the resource's states in past commits.

-{{image(url="graphics/sc0473.png", title="Transaction status bar", shadow=true, padding=20, scale=0.8)}}-

Table: Elements of the Transaction status bar

|#|Name|Function|
|:---:|----|--------|
|1|Version indicator|Shows whether the currently displayed configuration is the latest version, or some previous version.|
|2|Transaction selector|Displays a list of every transaction that includes a change to this resource's configuration. Select a past transaction to see a previous version of this resource.**Note:** When you select a past transaction, the option to Revert is displayed as a button at the bottom of the page. Clicking **Revert** opens an editing window showing the modifications that reversion would make to the current version of the resource. You can then proceed with those changes, or alter them further. When the changes are correct, you can Dry Run, Commit, or Add the changes to the current transaction, just like any other change to a resource.|
|3|Navigate to Transaction button|Click to view details about the transaction currently show in the **Transaction selector** drop-down.|
|4|Diffs view button|Click to see a before-and-after comparison showing the specific changes that were applied by the resource as part of the selected transaction.|
