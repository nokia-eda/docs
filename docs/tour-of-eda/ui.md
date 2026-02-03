# EDA UI

-{{% import 'icons.html' as icons %}}-

As any modern platform, EDA's UI is an API client of the API server and uses the same endpoints as any automation system would use, which means that technically every exercise in the tour can be solved using either UI or any automation interface.

While we applaud those who will choose to follow the tour using the API interface, for the most part we will use the UI in our examples. Chances are high that this will be your first time seeing and using the EDA UI, so let us give you a quick intro to what it looks like and how to use it.

To access the EDA UI, open your web browser and navigate to https URL displayed at the end of the ["Try EDA" installation process](../getting-started/try-eda.md). Log in using the default administrator credentials - `admin` as username and `admin` as password.

## Main page

When you log in to the EDA UI you land on the **Main** page:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/f91c7a975c7717357376506ce50907e0/CleanShot_2025-12-14_at_20.40.42.png", title="Main page")}}-

-{{icons.circle(letter="1")}}- Applications menu icon. Expands/collapses the left side menu, where all EDA apps and menu items are listed.

-{{icons.circle(letter="2")}}- Panel selector. EDA provides two default panels - "Main" and "System Administration". The panels control what apps are visible in the side menu. Users can create their own panels and switch between them based on the use case.

-{{icons.circle(letter="3")}}- Resource menu item. Clicking on the resource opens up the resource view. Users of EDA UI select a resource from the side menu to manage its lifecycle, for example creating the network interfaces, updating the Fabric configuration or setting up integration apps parameters.

-{{icons.circle(letter="4")}}- Application category toggle. Can be used to hide/show the application category. The resources shipped within an app have the UI category parameter that denotes which category this resource should be put in.

-{{icons.circle(letter="5")}}- The home page features a dashboard that provides some key information about the managed nodes, their interfaces, detected deviations and network-wide traffic rate.

-{{icons.circle(letter="6")}}- The home page has two dashboards to select from. The picker lets you select which dashboard to display. A similar view picker will be available on the resource pages as well.

-{{icons.circle(letter="7")}}- Namespace selector. When you have more than one namespace (`eda` is the default namespace) you will be able to switch between them.

-{{icons.circle(letter="8")}}- User menu. This is where you can change your password, log out, and access the help and about pages.

-{{icons.circle(letter="9")}}- Transaction basket is a staging area where uncommitted transactions will be stored. Users can add multiple resources to a basket and transact them all simultaneously.

-{{icons.circle(letter="10")}}- Workflows. This menu icon lists the recently run workflows in a current namespace.

-{{icons.circle(letter="11")}}- Help menu - displays the release version and the open api swagger specification for the platform and hotkeys.

-{{icons.circle(letter="12")}}- Stream mode selector - allows to select the mode UI uses to get the data from the backend API. "Live" streams the data as it becomes available, while "Pause" stops the streaming until resumed.

## Physical Topology

Every network engineer reaches for the topology view the moment they log in to a network management platform. EDA is no different and offers a physical topology view that displays the managed nodes and links with additional overlays available to visualize various aspects of the network.

To view the graphical topology of the managed network, click on the -{{icons.circle(letter="1")}}- **Topologies** resource under the **Tools** category in the left sidebar. This will open up the list of available topologies where in EDA -{{ eda_version }}- there is only Physical Topology available. Double click on the Physical Topology row to open up the topology view. If you're using try-eda this will show your digital twin topology.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/e15be3a70990106fd7acf50178a648d8/CleanShot_2025-12-18_at_13.41.27.png", title="Physical Topology view")}}-

-{{icons.circle(letter="2")}}- The topology view may be presented in the horizontal or vertical layout as driven by the map icon in the top toolbar.

-{{icons.circle(letter="3")}}- The physical topology consists of nodes and links where nodes can be dynamically arranged based on various grouping parameters available. The default grouping is done by the "Role" parameter, which is set in the node label set[^1].

-{{icons.circle(letter="4")}}- EDA UI supports topology overlays that can be used to overlay various data on top of the physical topology. The overlays can be selected from the overlay dropdown in the top toolbar.  
For example, the "Operational Status" overlay colors the nodes and links based on their operational status, and "CPU" overlay overlays gradient colors on top of the nodes based on their CPU utilization.

-{{icons.circle(letter="5")}}- In addition to the overlays, the topology view supports various badges that can added to the nodes and display additional meta information. For example, if the Overlay is set to "Operational Status", users can add Volume and CPU overlay badges to combine multiple data points in a single view.

The information panel on the right side of the topology view displays the details of the selected node or link in the topology.

## Resources View

When selecting a resource from the left side menu -{{icons.circle(letter="1")}}- a page that lists all instances of this particular resource kind is displayed.

In the example below we selected the -{{icons.circle(letter="I", text="Interfaces")}}- resource kind under the -{{icons.topology()}}- category in the left sidebar and got a list of all Interface resources that EDA manages.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/407f1acf862a2d86f817614bd1843944/CleanShot_2025-12-17_at_18.44.48.png", title="Resources page")}}-

The important elements on the resource view are:

-{{icons.circle(letter="2")}}- View selector. By default users get to see a table grid view listing the existing resources, and the view selector allows to view also dashboards and deleted resources for this resource type.

-{{icons.circle(letter="3")}}- The info panel on the right can be toggled by clicking on the info icon. The information panel displays the details for the currently selected resource in the grid.

-{{icons.circle(letter="4")}}- The Create button that opens up the resource's edit view and allows to create new instances of the resource kind.

-{{icons.circle(letter="5")}}- The context menu button next to the resource allows to select actions targeting this resource.

-{{icons.circle(letter="6")}}- The table grid header allow to customize the displayed view by selecting the displayed columns, sorting, and filtering.

### Information panel

The information panel on the resource view page displays the resource's details such as its metadata, specification and status.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/948ed9cf4ce8c9bbf106c06ac60f5004/CleanShot_2025-12-17_at_23.31.03.png")}}-

The main goal of the information panel is to provide an easy way to see the details about a selected resource when a user selects them in the table grid.

> Note, that everything in the EDA UI is stream-based is immediately reflected in the UI if the new data is coming. As well as it will be reflected "live" in the information panel should any parameters of the selected resource were to change.

### Details view

Double click on the row in the data grid table or using the "View" item of the row's context menu opens up the resource's detailed view.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/c4372eb603f9185d24569d77d9545bcd/CleanShot_2025-12-18_at_11.57.24.png", title="Opening the resource's details view")}}-

By default the page opens in read-only mode.
Let's break down the different elements of the "Details view":

-{{image(url="https://gitlab.com/-/project/7617705/uploads/29b367bc96ecf3e8ac94a890320c4eec/CleanShot_2025-12-18_at_12.00.06.png", title="Resource details view")}}-

-{{icons.circle(letter="1")}}- The view selector is set to "Details" view. The dropdown allows to switch between different views available for this resource kind, such as Topology view, Resource targets view, and others.

-{{icons.circle(letter="2")}}- The breadcrumb navigation bar allows to navigate back to the resource list page or to the home page and shows the current resource name.

-{{icons.circle(letter="3")}}- Resource transaction information. By default the resource details view shows the latest committed version of the resource. Users can switch to the past versions of the resource by selecting the desired transaction from the dropdown.

The main area of the details view is divided into three panels:

-{{icons.circle(letter="4")}}- Resource outline panel - allows for quick navigation between different sections of the resource structure and searching for specific fields.

-{{icons.circle(letter="5")}}- Resource's schema form - in the view mode the form displays the resource's fields in a read-only mode alongside with the descriptions of the fields.

-{{icons.circle(letter="6")}}- YAML view - displays the resource in YAML format. The YAML view is read-only in the details view mode.

-{{icons.circle(letter="7")}}- YAML view toggle - allows to hide the YAML view panel to provide more space for the schema form panel.

-{{icons.circle(letter="8")}}- YAML/JSON format toggle - allows to switch between YAML and JSON formats in the code view panel.

-{{icons.circle(letter="9")}}- -{{icons.circle(letter="10")}}- A group of buttons to display the transaction details and transaction diff for the selected transaction.

-{{icons.circle(letter="11")}}- Edit button - opens up the resource in the edit mode.

### Edit mode

Naturally, you will spend quite some time creating and editing resources in EDA. To enter in the Resource Edit mode click **Create** button from the [Resource view](#resources-view) or **Edit** from the [Details view](#details-view). The Edit page looks very much like the Details view, with the difference that now you can edit the resource fields.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/2c10dd959ca60cfe9590c86888bdf0b4/CleanShot_2025-12-18_at_13.21.19.png", title="Resource edit view")}}-

When editing or creating a resource, you can use the Schema Form view where every resource field is represented as a form field, or the YAML view where you can edit the resource in the YAML format. You can start with a form view and continue in YAML editor, or vice versa, the changes are always synchronized.

At the bottom of this page you will find buttons that allow you to either add the edited/created resource to the Transaction Basket or to perform one of the immediate actions: Dry Run or Commit.

> We will explore the power of transactions and dry runs in the subsequent sections of the tour.

## Transaction basket

The transaction basket allows you to group resources together and commit them as a single transaction in an all-or-nothing fashion. Transactions are the key ingredient in EDA's mission to drive human error to zero.

By adding resources to the transaction basket you can commit them all together or perform a Dry Run to ensure that the changes pass all sorts of validations before touching the network elements.

The workflow below demonstrates how a Banner resource gets added to the transaction basket, after which a dry run is performed to validate the transaction and then the diffs are browsed to understand the scope of the changes this transaction would result in should we have proceeded with the commit.

-{{video(url="https://gitlab.com/-/project/7617705/uploads/74710de8e90f689ec4ec96d4dec702af/tx-example.mp4")}}-

> Support for atomic transactions for arbitrary large sets of resources is one of the unique features of Nokia EDA platform that makes it stand out from the competition. Throughout the rest of the tour you will see mutiple examples of how transactions can be used to ensure safe and reliable network operations.

## Namespace selector

A namespace is a logical partition within a cluster that provides a mechanism for isolating sets of resources from each other. Such resource segmentation allows multiple teams or applications to share the same cluster without conflict, because each has its own set of resources in its own namespace.

When you first login to EDA as administrator, you have access to all available EDA namespaces and can switch between them using the namespace selector in the top toolbar:

![ns-select](https://gitlab.com/rdodin/pics/-/wikis/uploads/10f8c7779ea629e14214fb88c1280edb/CleanShot_2025-05-14_at_23.27.05_2x.png)

By switching from "All Namespaces" to a particular namespace (e.g. `eda` namespace) the UI will only show the resources from this namespace and new resources will automatically be created in this namespace. This is done by setting the namespace field name for you in the [Resource Edit View](#edit-mode) when you create a new EDA resource.

<div class="grid cards" markdown>

* :fontawesome-solid-route:{ .middle } **Where to next?**

    ---

    EDA takes control of the network devices - nodes - by managing them. Learn the basics of node management in EDA to proceed further in your EDA journey.

    [:octicons-arrow-right-24: **Node Management**](nodes.md)

</div>

[^1]: The node labels contain `eda.nokia.com/role` label that defines the role of the node in the topology. The nodes of the same role are grouped together in the topology view.
