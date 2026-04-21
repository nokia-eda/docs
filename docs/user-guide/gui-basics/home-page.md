# The Home page

The EDA Home page is the first landing page for the EDA GUI. While some elements of the Home page are unique, it also includes a set of standard controls that are available from all pages within the EDA GUI.

The EDA Home page includes a drop-down that allows you to choose between two views:

- the Summary page (default), that displays status summaries for nodes, interfaces, and traffic as well as active alarms
- the Platform Status page, that displays summary information for the status of key EDA component

## The Summary page

-{{image(url="../graphics/sc0204.png", title="The EDA Summary page", shadow=true, padding=20)}}-

Table: Common elements on the Home page

|#|Name|Function|
|:---:|----|--------|
|1|Menu pin/un-pin|Use this button to expand and pin, or collapse and hide, the main menu in the left column of the EDA GUI.|
|2|Menu controls|Use these tools to:<br><ul><li>Change between:<ul><li>the **Main** EDA menu, providing access to network management functions</li><li>the **System Administration** menu, providing access to functions that manage EDA itself</li><li>**All**, which displays all menu selections for the Main and System Administration menus</li></ul><li>Enable **Auto Expand** for the navigation menu, which causes a collapsed menu to expand horizontally when you hover over any menu icon</li><li>Search the full menu items for items that match specific text</li><li>Expand or collapse all menu categories</li></ul><br>**Note**: Because EDA allows you to create your own custom navigation panels, additional panels may be available for selection here. These could be panels you have created yourself, or created by others and then published for sharing with other users.|
|3|Menu category|Click to expand or collapse a category to reveal or hide the individual links that are grouped within it.|
|4|Event Driven Automation Home button|Click here on any page of the EDA GUI to navigate to, or re-load, the EDA Home page.|
|5|Namespace selector|Use this drop-down selector to choose a working namespace: either all namespaces, or one specific namespace. This selection affects the namespace from which to display data, and either create or manage resources.**Note:** The namespaces listed in the selector are limited to those namespaces that you have permission to access.|
|6|Common buttons|<ul><li>The **Transaction** basket: indicates the number of pending resource changes for the current user. Click to open the **Transactions** form.</li><li>The **Workflows** button opens the Workflow Executions form, which displays recent workflows and their status.</li><li>The **Help** button: click to open a menu to access API documentation, hotkey configuration, and Release information.</li><li>The **User settings** button: click to open the **User Settings** menu.</li></ul>|
|7|Dashlets|Each dashlet displays important information about the status of the EDA application and the network it is managing.Clicking the View link in any dashlet opens the EDA GUI page specific to that dashlet's information.|
|8|Live/Pause selector|Use this drop-down selector to start or pause streaming updates on all resource pages, including the following:<br><ul><li>datagrids</li><li>dashboards</li><li>schema forms</li><li>topologies</li></ul><br>Clicking **Pause** pauses the stream of data which can be helpful for pages with high rates of change.<br><br>Clicking **Live** resumes the streaming of data.|

The following default dashlets display on the Summary page:

- **Nodes**: displays the synchronization state of the nodes known to EDA (total nodes: synced nodes and unsynced nodes).

    Clicking the **View** link from this dashlet takes you to the Nodes list.

- **Deviations**: displays the number of nodes that are configured in a way that differs from the last intent known to EDA. Separate counts are displays for those deviations that have been accepted (incorporated into the stored intent) and those that have been detected but have not been accepted.

    Clicking the **View** link from this dashlet takes you to the Deviations list.

- **Interfaces**: displays the operational state of the interfaces known to EDA (Up interfaces, Down interfaces, Degraded interfaces).

    Clicking the **View** link from this dashlet takes you to the Interfaces list.

- **Traffic**: displays total inbound and outbound traffic for the network as a whole.

    Clicking the **View** link from this dashlet takes you to the EDA Query Builder, displaying the sum of in and out traffic rates for all nodes: `.namespace.node.srl.interface.traffic-rate fields [sum(in-bps), sum(out-bps)]`.

- **Alarms**: displays the number of current app alarms and platform alarms, and their percentage distribution by alarm type.

    Clicking the **View** link from this dashlet takes you to the Alarms Summary.

**Related information**  

- [Transactions](gui-elements.md#transactions)
- [User settings](gui-elements.md#user-settings)
- [Information panel](gui-elements.md#information-panel)
