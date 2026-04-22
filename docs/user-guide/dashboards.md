# Dashboards

In EDA, you can construct your own dashboard pages to display the data you deem important for your operation.

The Dashboards page allows you to construct a dashboard, which itself can contain one or more layouts. Each layout is a separate dashboard page, selectable using a drop-down in the breadcrumb navigation bar.

Each dashboard layout can consist of a collection of dashlets, each displaying its own source data; or a list layout containing a single data grid.

For dashboard layouts, you can construct each layout by selecting from a set of pre-defined dashlets. Each dashlet can show a particular type of data like counters, lists, and charts. You can then add these dashlets to a page you design, optionally distributing them among a set of rows and columns you have specified within the page. Individual dashlets can be set to span multiple rows or columns.

For each list or dashlet layout in the dashboard, you define source data by constructing a query. You can then specify details about which parts of that data is displayed, and make formatting choices depending on the dashlet type.

Dashboards also supports [filters](#dashboard-filters). Filters use variable substitution to modify dashlet queries based on user input.

## Dashboards list <span id="dashboards-page"></span>

The Dashboards page is the point from which you can access existing dashboards, and begin creating new dashboards.

The Dashboards list displays all of the dashboards available to you. Open the Dashboards list by selecting **Dashboards** from the main navigation panel.

-{{image(url="graphics/sc0218.png", title="The dashboards page", shadow=true, padding=20)}}-

The Dashboard designer displays dashboards that can originate from three sources (as indicated in the **Source** column):

- dashboards that were created by EDA and its installed applications
- dashboards created by the current user
- dashboards that the current or other users have chosen to share.

### Elements of the Dashboard list

Table: Elements of the Dashboard list

|\#|Name|Function|
|:---:|----|--------|
|1|Breadcrumb bar|Displays the current position in the set of Dashboard designer pages.|
|2|Row actions|Clicking the Table row actions icon reveals the actions available for the current row in the dashboards data grid.|
|3|**Create** button|Click to open the Dashboard Designer view for a new dashboard.|
|5|**Import Layout** button|Click to open a file selection dialog. Select the file for a previously exported dashboard and click **Open** to import the selected dashboard. The new dashboard is then displayed in the Dashboards list.|
|6|Information panel|A standard EDA information panel, displaying details about the dashboard that is currently selected in the dashboard list.|

Table: Default Dashboard display columns

|Column|Description|
|------|-----------|
|Name|The display name configured for the dashboard.|
|Source|The source from which the dashboard originated. This can be one of the following values: <ul> <li>An app name \(such as Fabrics or Default Routing\): this is the source application for this dashboard. </li> <li>User Storage: this is a user-created dashboard.</li></ul>|
|Type|<ul><li>Application: a dashboard associated with EDA or one of its installed apps. You cannot edit, delete, or publish these dashboards, as signified by the lock icon beside the dashboard name.</li> <li>Personal: a dashboard created by the current user account.</li> <li>Shared: a user-created dashboard that has been published for sharing. When you share your own dashboards, the Shared version is a different entity than the original Personal dashboard. Both can be edited independently.</li></ul>|
|Last Changed|The time and date that the last modification was saved for this dashboard.|

Table: Non-default Dashboard display columns

|Column|Description|
|------|-----------|
|ID|A unique ID assigned internally by the EDA system.|
|File Name|The name and path for the JSON file that contains this dashboard configuration. For example, services/ui/router-dashboard-v0.2.json.|
|Group|The API group of the EDA app which provides this dashboard.|
|Version|The API version of the EDA app which provides this dashboard|

### Row actions for dashboards

The following row actions are available for dashboards in the list:

Table: Row actions for dashboards

|Action|Description|Application dashboards?|Personal dashboards?|Shared dashboards?|
|------|-----------|:---------------------:|:------------------:|:----------------:|
|Preview|Shows a preview of the dashboard and the data it contains.|Yes|Yes|Yes|
|Duplicate|Make a copy of the current dashboard, which you can save under a different name and then modify as required.|Yes|Yes|Yes|
|Publish|Publish a Personal dashboard for sharing with others. If you publish an already-published dashboard, a confirmation dialog warns you that proceeding will over-write the current published version. |No|Yes|No|
|Edit|Open the current dashboard for editing. Editing a Shared dashboard edits only the shared copy, not the personal copy on which it is based. |No|Yes|Yes|
|Delete|Delete the selected dashboard. Delete is also available as a multi-row action, in which case it deletes all of the dashboards currently selected in the list. |No|Yes|Yes|

## Dashboard designer <span id="dashboard-designer-page"></span>

The dashboard designer page is the space in which to create a dashboard and its constituent layouts, and to configure the data displayed on each.

-{{image(url="graphics/sc0219.png", title="The dashboard designer page", shadow=true, padding=20)}}-

Table: Elements of the Dashboard Designer page

|\#|Name|Function|
|:---:|----|--------|
|1|Definition/Library panel|The Definition tab displays basic parameters about the current dashboard layout, like its name and description.The Library tab displays elements that you can add to the current dashboard layout: flex rows, flex columns, and dashlets.|
|2|Layout panel|This is the area that displays the dashboard layout you are designing. Drag objects from the Libraries tab into this space to add elements to the dashboard layout.<br>Select objects in this panel to view and configure their properties in the Properties tab.|
|3|Properties|The Properties tab displays properties for the current dashboard, and for the row, column, or dashlet currently selected in the layout panel.Use this tab to configure the basic display properties for the dashboard.|
|4|Filter configuration panel|Filters are an optional way to modify the data underlying dashlets contained on the dashboard. <br> <br>Use this panel to configure one or more filters for the current dashboard. <br> <br>When a filter is configured, you can include a corresponding "where" clause in the queries underlying individual dashlets. <br>Enable the **Show filters bar** property to display a widget on the layout panel that allows you display and use specific filters you have configured. <br> <br>See the procedure for creating dashboard filters for the steps to create a filter, add a reference to the queries for dashlets, and use the filters to constrain the data displayed by those dashlets.|
|4|Add|Click to add another dashboard layout to the dashboard.|
|5|Add List Layout|Select this option in the drop-down to add a List page to the dashboard.|
|6|Save|Click to save the current dashboard design.|
|7|Reset|Click to discard all changes since you last saved the layout, after confirmation.|
|8|More icon|Click to view a list of available actions for the current Dashboard:<ul><li>**Preview saved changes**: open a new tab that displays the current dashboard design.</li><li>**Export**: save the dashboard design as a file, which others can import into their copy of EDA.</li></ul>|

### Flex grids <span id="dashboard-flex-grids"></span>

Flex grids are the underlying structure of a dashboard. You must add at least one flex row or flex column to the dashboard before you can then fill the resulting grid with individual dashlets.

To add a flex row or flex column to a dashboard design, drag the flex row or flex column from the Library panel onto the Layout panel.

You can add a series of rows and columns to create a customized grid for your dashboard design. Each cell in the grid can then accept one or more dashlets.

For example, in the illustration below, the dashboard includes multiple flex rows, and a flex column has been added to the first row to divide it into two cells.

-{{image(url="graphics/sc0220.png", title="Flex grid", shadow=true, padding=20)}}-

When you select a specific cell in the Layout panel, the Properties panel displays two properties that you can configure for the selected flex row or column:

- **Vertical Alignment**: the vertical position of any dashlets that are placed in that cell.
- **Horizontal Alignment**: the horizontal position of any dashlets that are placed in that cell.

### Dashlet types <span id="dashlet-types"></span>

Dashlets are the building block from which you can build your dashboard. Several types of dashlets are available in EDA; each can be dragged and dropped on to your dashboard design. If you have added flex columns or rows, you can distribute dashlets within the resulting grid.

#### Counts dashlet <span id="dashlet-counts"></span>

The counts dashlet displays a simple count of qualifying instances of something in EDA. You select a data source, and can then specify criteria to distinguish qualifying instances of the selected data that are counted and highlighted, versus the basic number of all records in the selected data source.

-{{image(url="graphics/sc0221.png", title="A sample counts dashlet", shadow=true, padding=20)}}-

Table: Counter dashlet properties

|Property|Description|
|--------|-----------|
|Common properties|
|Title|The title of the dashlet when displayed in the EDA UI.|
|Subtitle|A subtitle, displayed below the title and in a smaller font.|
|Navigation target|Adds a **View** button to the dashlet that, when clicked, opens a new page. The target page can be:<ul><li>a page within the EDA GUI that you select from the displayed drop-down list (some selections require additional details) <li>an extgrnal page for which you provide a valid URL.|
|Fill available width|Dynamically changes the dashlet width based on the browser window and neighboring dashlets.|
|Dashlet width|The relative width of the dashlet.|
|Dashlet height|The relative height of the dashlet.|
|API Specification|
|Query|Click the More icon to open a page on which to configure the data source for this dashlet.On that page you configure the data source as one of the following:<ol><>li>EQL Query</li><li>Natural Language query</li><li>GVK Definition</li><li> URL Endpoint</li></ol>|
|Counters|These properties configure the highlighting of values that meet criteria on the counts dashlet:<ul><li>**Label**: the label shown beside qualifying values</li><li>**Color**: the color used to highlight qualifying values</li><li>**Field**: the field within the data source to be evaluated for possible highlighting</li><li>**Criteria** \(Equals, Not Equal, Greater Than, Less Than\): the logical operator that qualifies for this highlight \(in combination with Value\)</li><li>**Value**: the comparison value for the logical criterion.|
|Additional dashlet properties|
|Show total|Indicates whether to display a count of all values retrieved in the source data set should be displayed on the chart, in addition to qualifying values.|
|Show total at end|When the total is shown, controls the position of the total display. Changes between the total being the first count, or the last.|
|Show percentage|Indicates whether the counter should display what percentage of all values are represented by qualifying values.|
|Vertical lists|When the total is shown, controls the position of the total count and qualifying count. Changes between the total being above, or below the count of qualifying values.|

#### Line chart dashlet <span id="dashlet-line-chart"></span>

A line chart dashlet places a line chart on the dashboard layout. It supports both stacked line charts \(in which values are successively added to show a series of cumulative totals\) and overlaid \(a standard line chart in which values are displayed independently, not as a sum\).

-{{image(url="graphics/sc0222.png", title="A sample line chart dashlet", shadow=true, padding=20)}}-

Table: Line dashlet properties

|Property|Description|
|--------|-----------|
|Common properties|
|Title|The title of the dashlet when displayed in the EDA UI.|
|Subtitle|A subtitle, displayed below the title and in a smaller font.|
|Navigation target|Adds a **View** button to the dashlet that, when clicked, opens a new page. The target page can be:<ul><li>a page within the EDA GUI that you select from the displayed drop-down list (some selections require additional details) <li>an external page for which you provide a valid URL.|
|Fill available width|Dynamically changes the dashlet width based on the browser window and neighboring dashlets.|
|Dashlet width|The relative width of the dashlet.|
|Dashlet height|The relative height of the dashlet.|
|API Specification|
|Query|Click the More icon to open a page on which to configure the data source for this dashlet.On that page you configure the data source as one of the following: <ol><li>EQL Query </li><li> Natural Language query </li><li>GVK Definition </li><li>URL Endpoint </li></ol>|
|Chart Configuration|These properties control the display of the line chart:<ul><li>Maximum number of data points</li><li>Y-Axis Units</li><li>Scaling Function \(None, Metric Prefix Scaling\)</li></ul>|

#### Donut dashlet <span id="dashlet-donut"></span>

A donut dashlet places a pie chart on the dashboard layout. You must configure a data source, and then set criteria for various pie slices describing qualifying subsets of that data. Many parameters are available to control the way the appearance of the chart and the individual pie slices.

-{{image(url="graphics/sc0223.png", title="A sample donut dashlet", shadow=true, padding=20)}}-

Table: Donut chart properties

|Property|Description|
|--------|-----------|
|Common properties|
|Title|The title of the dashlet when displayed in the EDA UI.|
|Subtitle|A subtitle, displayed below the title and in a smaller font.|
|Navigation target|Adds a **View** button to the dashlet that, when clicked, opens a new page. The target page can be:<ul><li>a page within the EDA GUI that you select from the displayed drop-down list (some selections require additional details) <li>an external page for which you provide a valid URL.|
|Fill available width|Dynamically changes the dashlet width based on the browser window and neighboring dashlets.|
|Dashlet width|The relative width of the dashlet.|
|Dashlet height|The relative height of the dashlet.|
|Charts|
|Charts|A single pie chart dashlet can include multiple pie charts.Use this space to add and configure each pie chart.<br><br>After configuring a pie chart, click the + icon to add and configure an additional pie chart for this dashlet.|
|Donut Chart Details An individual pie chart within the donut dashlet is configured on this page.|
|Query Definition|Specifies the data source on which the pie chart's segments is based. Choose from:<ul><li>EQL Query </li><li>Natural Language query </li><li>GVK Definition </li><li>URL Endpoint </li>|
|Hide title|Indicates whether to show the chart title on the chart, or not. Options: Yes or No.|
|Show total|Indicates whether the sum of all segments should be displayed on the chart, or not.Options: Yes or No|
|Show slice labels|Indicates whether each chart segment should display a label for its data.<br><br>Possible values: All, Percent, None|
|Segments: these properties control the display of each segment in the chart.Configure and add as many segments as your chart requires.|
|Label|Indicates whether this slice should display its own label.|
|Color|The shading color applied to this slice.|
|Field|From the selected data source, the individual field that corresponds to this slide.|
|Criteria|The logical criterion for this slide \(Equals, Not Equal, Greater Than, Less Than\)|
|Value|The fixed value against which the current field value and the Criteria are compared.|
|+|Click this icon to add the slice configuration to the set of slices included in this chart.|

#### Data view dashlet <span id="dashlet-dataview"></span>

A data view dashlet places a data grid on the dashboard. You must specify a data source as part of the dashlet design.

-{{image(url="graphics/sc0262.png", title="A sample dataview dashlet", shadow=true, padding=20)}}-

Table: Dataview properties

|Property|Description|
|--------|-----------|
|Common properties|
|Title|The title of the dashlet when displayed in the EDA UI.|
|Subtitle|A subtitle, displayed below the title and in a smaller font.|
|Navigation target|Adds a **View** button to the dashlet that, when clicked, opens a new page. The target page can be:<ul><li>a page within the EDA GUI that you select from the displayed drop-down list (some selections require additional details) <li>an external page for which you provide a valid URL.|
|Fill available width|Dynamically changes the dashlet width based on the browser window and neighboring dashlets.|
|Dashlet width|The relative width of the dashlet.|
|Dashlet height|The relative height of the dashlet.|
|Charts|
|Query|Click the More icon to open a page on which to configure the data source for this dashlet.On that page you configure the data source as one of the following: <ol> <li>EQL Query </li><li>Natural Language query </li> <li> GVK Definition</li><li> URL Endpoint</li></ol>|
|Show information panel|Indicates whether an information panel should be available on this dashlet.|
|Show status bar|Indicates whether to include a status bar on the dashlet, showing \(for example\) whether any filters are applied, and the total number of rows in the list.|

#### Bar chart dashlet <span id="dashlet-bar-chart"></span>

A bar chart dashlet places a bar chart on the dashboard layout. It supports both horizontal and vertical bar charts.

You can also configure the chart to show stacked bars contributing to a total value, with the elements in the stack indicated as either a raw value or a percentage of the whole.

-{{image(url="graphics/sc0224.png", title="A sample bar chart dashlet", shadow=true, padding=20)}}-

Table: Bar chart properties

|Property|Description|
|--------|-----------|
|Common properties|
|Title|The title of the dashlet when displayed in the EDA UI.|
|Subtitle|A subtitle, displayed below the title and in a smaller font.|
|Navigation target|Adds a **View** button to the dashlet that, when clicked, opens a new page. The target page can be:<ul><li>a page within the EDA GUI that you select from the displayed drop-down list (some selections require additional details) <li>an external page for which you provide a valid URL.|
|Fill available width|Dynamically changes the dashlet width based on the browser window and neighboring dashlets.|
|Dashlet width|The relative width of the dashlet.|
|Dashlet height|The relative height of the dashlet.|
|API Specification|
|Query|Click the More icon to open a page on which to configure the data source for this dashlet.On that page you configure the data source as one of the following:<ol><li>EQL Query</li><li>Natural Language query</li><li>GVK Definition</li><li>URL Endpoint</li>|
|Chart Configuration|These properties control the display of the line chart: <ul> <li>Group By </li><li>Secondary Grouping </li><li>Value Field </li><li>Unit of Measure </li><li>Scaling Function \(None, Metric Prefix Scaling\) </li><li> Use Columns instead of Bars \(yes/no\) </li><li>Show stacked data \(Off/Value/Percent\) </li>|

### Dashboard filters <span id="creating-dashboard-filter"></span>

Filters constrain the data used by the dashlets on a dashboard. For example, a dashboard which displays data for all nodes can be filtered to display only data from a specific node you specify in the filter field.

After you have configured filters, you can modify the underlying query of any dashlet on the dashboard to include a reference to one or more of those filters. When you specify a value within the filter field on the dashboard, those dashlets display only results that satisfy that filter.

At a high level, configuring and using filters involves the following steps:

/// html | div.steps

1. Add one or more filters in the dashboard designer.

2. For each dashlet to which a dashboard filter should apply, edit the dashlet's underlying query to include a "where" expression referring to one or more of the dashboard filters.

3. Enable 'Show filters bar' in the dashboard designer to allow users to enter a filter.

///

The dashboard designer supports three kinds of filters:

- **Name/Namespace filter**: allows you to specify a particular resource name and namespace, to be used in a dashlet query where clause. 

    You can use can use a "where" clause in your dashlet query resembling `where (name = "${NNFilter.name}" and .namespace.name = "${NNFilter.namespace}")`
    
    The available Name/Namespace values will be autocompleted in the filter bar for dashboard users

- **Custom filter**: allows you to specify a particular EQL query and field name, for which the field's value will be used in a dashlet query where clause. 

    The dashboard creator can use the "where" clause in their dashlet query resembling `where (<field> = "${CustomFilter}").`

    The available filter values will be autocompleted in the filter bar for dashboard users

- **String filter**: allows you to specify a free-form string, to be used in a dashlet query where clause.

    The "where" clause for a string filter resembles `where (<field> = "${StringFilter}").`

After you have configured one or more filters, filter fields are displayed in the following places in the EDA GUI:

- on the query configuration page for every dashlet within the dashboard. Here you can add the filter variables to the dashlet's query where clause and test the result by entering filter values to immediately constrain the dashlet's underlying data set.

- on top of the dashboard, if you enable 'Show fitler bar' in the dashboard designer. Entering a filter value here immediately impacts the data displayed in each dashlet whose query uses the filter.

If a filter is configured, but no value is entered in the filter field, the dashlet query filter variables are set to wildcards (*) so that the filter has no effect.

#### Creating dashboard filters <span id="creating-dashboard-filter"></span>

/// html | div.steps

1. Click the + beside the **Filters** label.

2. Select the type of filter you are creating in the **Type** list control:

    - to add a string filter: go to step [3](#df-step-3).
    - to add a Name/Namespace filter: go to step [5](#df-step-5).
    - to add a custom filter: go to step [7](#df-step-7).
  
3. <span id="df-step-3"></span> Configure a String filter for the dashboard by doing the following:

    1. Enter a **Name** for the filter.

    2. Click **Save**.

4. Go to step [8](#df-step-8).

5. <span id="df-step-5"></span> Configure a Name/Namespace filter for the dashboard by doing the following:

    1. Enter a **Name** for the filter.

    2. Use the **Query** field to create a query that generates the data set against which this filter is applied. This query can be in the form of an EQL Query, Natural Language query, GVK Definition, or URL Endpoint.

        /// admonition | Note
            type: subtle-note
        The resulting data set must include the Name and Namespace fields. If those fields are not present in the data set, the filter fails.
        ///

    3. While the focus is still on the **Query** field, press the **Enter** key to signal that you have finished configuring the query.

       /// admonition | Note
            type: subtle-note
       If you do not press the Enter key, the EDA UI does not recognize that the query is complete and you are unable to proceed.
       ///

    4. Click **Save**.

6. Go to step [8](#df-step-8).

7. <span id="df-step-7"></span> Configure a Custom filter for the dashboard by doing the following:

    1. Enter a **Name** for the filter.

    2. Use the **Query** field to create a query that produces the data against which this filter is applied. This query can be in the form of an EQL Query, Natural Language query, GVK Definition, or URL Endpoint.

    3. While the focus is still on the **Query** field, press the **Enter** key to signal that you have finished configuring the query.

        /// admonition | Note
            type: subtle-note
        If you do not press the Enter key, the EDA UI does not recognize that the query is complete and you are unable to proceed.

        You may need to wait a moment for the system to finish resolving the query before selecting a field from the query results in the next step.
        ///

    4. After you have created the query, and the system has had a chance to resolve it and can identify the fields of data returned, use the **Field** list to select one of the fields within the resulting data set. The field you select here is the field against which the filter text you enter later is compared.

    5. Click **Save**.

8. <span id="df-step-8"></span> To apply one or more of the dashboard's filters to one of its dashlets, do the following:

    1. Select the dashlet and open its Details page to configure its underlying query.

        /// admonition | Note
            type: subtle-note
        On the Details page, a field displays for each filter you have configured for the dashboard. Beneath each filter field is a text template for a "where" clause that refers to that filter. Because the syntax for a "where" clause must be precise, these templates are a useful starting point for incorporating the filter in to the dashlet's query.
        ///

    2. Choose a filter and copy its template "where" clause text.

    3. Paste the template text to the appropriate position for a "where" clause within the dashlet query string.

    4. Edit the "where" clause so that it refers to a valid field within the query's data set.

        /// admonition | Note
            type: subtle-note
        Take care to ensure that the resulting "where" clause precisely matches the spacing and syntax of the template provided. Symbols and spaces must all be placed correctly. If there is any error in the formatting of the clause, the query fails.
        ///

    5. Repeat steps b, c, and d to add more filters to the query if required. Be sure to precisely follow the correct syntax for multiple filters in a query.

9. Repeat step [8](#df-step-8) for every dashlet on the dashboard that should be subject to the dashboard's filters.

10. To apply dashboard filters to the dashlets on the dashboard designer page, do the following:

    1. Enable the **Show filters bar** to turn on the dashboard designer page to display the filter fields on the dashboard designer page.

        The filters bar displays at the top of the dashboard's Layouts panel.

    2. Click the filter icon on the filters bar to display a list of available filters, and click a filter in the displayed list.

    3. Repeat step b to display additional filter fields if required.

    4. Enter values into one or more of the displayed filter fields.

        All dashlets on the dashboard whose underlying queries use one of the filter values update to constrain their data to results matching the filter values.

///

### Navigation Targets

Dashlets can be configured with Navigation Targets, allowing users to navigate to additional information about the visualized data. 

Targets can be configured at the dashlet level to add a 'View' link to the dashlet, or at the data segment level to allow users to click-through the chart to a filtered set of results.

If you set a navigation target for your dashlet, additional information may be required depending on your selection:

- For an internal link, select an existing page in the EDA GUI from the **Route** dropdown list. Some internal links require additional configuration:
    - Alarms: Delect a **Screen Name** to identify the specific Alarms page to display. If navigating to the alarm list screen, optionally enter a EQL expression to filter to set of alarms displayed. Click **Validate** to confirm the EQL expression is valid before saving the custom menu item.
    - Dashboard: Use the **Available Dashboards** drop-down list to select an existing dashboard as the link target.
    - Query: Enter and validate an EQL query.
    - Merge Requests: Optionally enter and validate an EQL expression to filter the Merge Requests lists.
    - Role-Based Access Control: Select a **Screen Name** to identify the specific User Management page to display.
    - Resources: Select a Group, Version, and Kind in the **GVK Definition** field to specify the target resource. Select a **Screen Name** to identify the specific Resources page to display; the default screen is the resource list view. Optionally enter and validate an EQL expression to filter the resource list.
- For an external link, select External from the **Route** dropdown list to display the **URL Endpoint** field. In this field, enter our external link as a URL. For example: [https://docs.eda.dev/](https://docs.eda.dev/).

The Data view type dashlet supports the specification of a navigation target template, which will then be used to generate dynamic navigation targets for each row based on the data. To configure the template, use `${raw_column_name}` in your nav target EQL expression. For example, if an alarms navigation target is configured with EQL expression `type = '${type}'` double-clicking an alarm type "InterfaceDown" in the data view will navigate to the alarms list filtered by 'type = 'InterfaceDown'

### Designing a dashboard <span id="designing-dashboard"></span>

This task guides you through the steps of adding and configuring layouts within a single dashboard by:

<ul>
    <li>creating the new dashboard
    <li>adding a single layout: either a list layout, or a dashboard layout consisting of one or more dashlets
    <li>configuring the data source for each list or dashlet, and configuring the appearance and behavior of each.
    <li>optionally adding more list or dashboard layouts to the same dashboard
    <li>saving your layout
</ul>

**Procedure**

/// html | div.steps

1. Use the **Main** navigation panel to select **Dashboards**.

2. Click **Create**.

3. Choose one of the following:
    - To create a dashboard with a list layout, go to step [4](#dd-step-4).
    - To create a dashboard with a set of dashlets, go to step [10](#dd-step-10).

4. <span id="dd-step-4"></span> Use the drop-down control beside **Add** to click **Add List Layout**.

5. In the **Definition** panel, configure basic properties for the dashboard:

    - **Layout name**: an internal name for this layout. This name cannot include spaces or special characters.
    - **Display name**: the name for this layout, as displayed within the EDA GUI. Unlike the layout name, you can include spaces in the Display name.
    - **Description**: an optional description of the layout and its purpose.
    - **Show navigation toolbar?**: governs whether a breadcrumb bar displays above the dashboard.

6. Click the list in the center configuration panel to reveal properties for the list in the Properties panel.

7. Configure display properties for the list:

    - **Show information panel**
    - **Show status bar**
    - **Show column filters**

8. <span id="dd-step-10"></span> Configure the source data for the list:

    1. Click the vertical dots beside the **Query** field to open a window in which to configure data source for the list.

    2. In the Data View Details window, use the first drop-down to select a source type for the dashlet's query:

        - EQL Query
        - Natural Language query
        - GVK Definition
        - URL Endpoint

    3. Use the second field to enter the query expression, or to specify the GVK definition or URL endpoint.

    4. Click **Query** to retrieve data associated with the expression you entered.

    5. Click **Save**.

9.  Go to step [20](#dd-step-20).

10. <span id="dd-step-10"></span>In the **Definition** panel, configure basic properties for the dashboard:

    - **Layout name**: an internal name for this layout. This name cannot include spaces or special characters.
    - **Display name**: the name for this layout, as displayed within the EDA GUI. Unlike the layout name, you can include spaces in the Display name.
    - **Description**: an optional description of the layout and its purpose.
    - **Show navigation toolbar?**:

11. In the **Properties** panel, configure screen properties for the dashboard:Screen Name:

    - **Screen Name**
    - **Screen Type**: This is set to Dashboard and cannot be altered.
    - **Show screen in Navigation Bar?**:
    - **Default screen when layout is loaded?**:

12. Optionally configure one or more filters for this dashboard.

    /// admonition | Note
        type: subtle-note
    See the separate procedure for creating a dashboard filter for the steps to:

    - configure one or more dashboard filters
    - modify the queries underlying one or more dashlets to incorporate those filters
    ///

13. <span id="dd-step-15">Click the **Library** tab to configure the dashboard layout.

14. <span id="dd-step-16"></span>Optionally, add rows and columns to the dashboard:

    /// admonition | Note
        type: subtle-note
    You can arrange dashlets on the dashboard even without creating rows and columns in advance; but configuring a grid gives you more control over dashlet positioning, and allows you to configure dashlets to span multiple cells in the grid arrangement.
    ///

    1. To add rows to the dashboard, drag the **Flex Row** control into the layout panel. Repeat this to add more rows to the dashboard.

    2. To add columns to the dashboard, drag the **Flex Column** control into the layout panel. Repeat this to add more columns to the dashboard.

    3. In the Properties panel, configure the flex row or flex column you added by setting the **Vertical Alignment** and **Horizontal Alignment** properties.

15. <span id="dd-step-17"></span>Add a dashlet to the dashboard by selecting a **Dashlet** control from those displayed, and dragging it into the layout area. If you previously added rows or columns, drop the dashlet into the appropriate position.

16. <span id="dd-step-18"></span>Click the dashlet in the center configuration panel to reveal properties for the dashlet in the Properties panel.

17. Configure the dashlet by setting:

    - Screen properties \(these are common to all dashlets\).
    - Dashlet properties \(some are common to all dashlets; others vary by dashlet type\).
  
    /// admonition | Note
        type: subtle-note
    See the topics for dashlet types for details about the individual parameters available for each type of dashlet.
    ///

18. <span id="dd-step-20"></span> To configure the source data for the dashlet \(among the dashlet properties\):

    1. Click the vertical dots icon beside the **Query** field to open a window in which to configure data source for the dashlet.

    2. In the Details window, use the first drop-down to select a source type for the dashlet's query:

        - EQL Query
        - Natural Language query
        - GVK Definition
        - URL Endpoint

    3. Use the second field to enter the query expression, or to specify the GVK definition or URL endpoint.

    4. Click **Query** to retrieve data associated with the expression you entered.

    5. Click **Save**.

    6. Configure additional properties for the data, if they are available for your dashlet type.

        /// admonition | Note
            type: subtle-note
        For example, a Counter dashlet allows you to specify here whether the counter should display a total, total at end, percentage, or a vertical list of values.
        ///

19. Repeat steps [15](#dd-step-15), [17](#dd-step-17) and [18](#dd-step-18) to add more dashlets to the dashboard if required, until all dashlets are configured.

20. <span id="dd-step-20"></span>Do any of the following:

    - To save your dashboard, click the **Save Layout** icon.
    - To add a new dashboard layout to your dashboard, click **Add**.
    - To add a new list layout to your dashboard, use the drop-down beside the **Add** control to select **Add list Layout**.
    - To preview your dashboard, click the **More** icon and select **Preview Saved Changes** from the list of actions.
    - To save your dashboard layout as a file, suitable for others to import into their EDA system, click the **More** icon and select **Export** from the list of actions.

///

## Sharing dashboards <span id="share-dashboard"></span>

When you create a new dashboard, it is displayed as a new Personal dashboard only in the Dashboards list for your user account. By default only you can see, use, modify, or delete it.

If you would like to share a dashboard for use by others, follow the steps in this procedure.

/// admonition | Note
    type: subtle-note
Once you share a dashboard, it appears as a new, shared entry in the dashboard list. This shared copy can be modified by other users. Changes to the shared dashboard do not alter the original Personal dashboard.

To view shared dashboards, users require URL Rule read permission to path '/core/user-storage/v2/shared/**'

To publish and edit shared dashboards, users require URL Rule readWrite permission to path '/core/user-storage/v2/shared/**'
///

If you later modify a Personal dashboard that you previously published, you can share these changes by Publishing the dashboard again. This overwrites the previous Shared version of that dashboard.

/// html | div.steps

1. Use the **Main** navigation panel to select **Dashboards**.

2. Select a Personal dashboard in the list.

3. Use the **Table row actions** drop-down list to click **Publish**.

    A new copy of the selected dashboard is added to the Dashboards list, with the Type set to Shared.

///
