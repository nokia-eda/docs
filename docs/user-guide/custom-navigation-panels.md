# Custom navigation panels

The EDA navigation menu provides many links to the tools and resources within the EDA GUI, sorted into categories. These categories and links are organized within separate navigation panels \(for example, the standard navigation panels **Main** and **System Administration**\).

To limit the menu links to the links you use most often, EDA allows you to create navigation panels containing only the categories and navigation links that you select. You can even create multiple custom navigation panels, so that you can switch between the panels and their menus that are optimized for particular tasks.

You can also include custom links to internal pages, and links to saved dashboards as part of your navigation panel.

To further help you manage navigation, you can also show or hide any of the standard or custom EDA navigation panels.

Using the **Manage Panels** option in the EDA main menu, you can:

- Build a custom navigation panel that includes the links to the pages you use most, organized into categories that work for you
- Edit or duplicate a custom panel \(a duplicated navigation panel generally serves as the starting point for creating a modified version of it\)
- Hide or delete a custom panel
- Share your custom panel with other EDA users

/// admonition | Note
    type: subtle-note
Published panels are visible to all EDA users with read permissions for shared user storage.
///

## Custom Panel page <span id="custom-nav-panels-pages"></span>

The Custom Panel page is used, with a minor change in title, whenever you:

- Create a new custom navigation panel
- Edit an existing custom navigation panel
- Open a duplicate of an existing navigation panel, to modify it and save it as a new panel

-{{image(url="graphics/sc0271.png", title="The custom navigation panel creation form", shadow=true, padding=20)}}-

Table: Elements of the Custom Navigation Panel Creation form

|Dashlet|Description|
|-------|-----------|
|Panel name|Enter the name to be displayed in the EDA navigation menu for this panel.|
|Add menu items link|Opens a form on which to define a custom menu item and add it to an existing category within the navigation panel you are designing.|
|Create new category link|Opens a form on which to define a custom menu category with a name and associated icon, and add it to an existing category within the navigation panel you are designing.|
|Available navigation items|A full list of standard EDA menu categories and their available navigation items. Drag whole categories or individual navigation items to any position within the navigation panel you are designing.|
|Selected navigation items|A preview of the navigation panel you are designing.|

## Creating a custom panel <span id="creating-custom-nav-panel"></span>

A custom navigation panel is an EDA navigation panel that you construct yourself, containing menu categories and links to pages within the EDA GUI.

After you construct a custom navigation panel, it appears in the list of selectable navigation panels in the EDA main menu. You can then select the custom navigation panel to display it instead of, or in addition to, the standard EDA main menu.

Optionally, instead of constructing the entire navigation panel from scratch, you can duplicate an existing navigation panel and then add and remove categories and menu items as required.

/// html | div.steps

1. Do either of the following:

    - To build a custom navigation panel from scratch, use the **Main** navigation panel to select **Create Panel**.
    - To start your design from an existing navigation panel, use the **Main** navigation panel to select **Manage Panels**. Select a navigation panel from the resulting list, and click **Duplicate Panel** from the available actions for that selection.
    The Create Panel or Duplicate Panel displays, depending on your selection.

2. Enter a name for your panel in the **Panel Name** field.

3. Add one or more categories for your navigation panel.

    1. <span id="cnp-substep3a"></span> Click **+ Create new category** to open the Create Category form.

    2. Enter a name in the **Category Name** field.

    3. <span id="cnp-substep3c"></span> Select an icon to display next to this category in the custom navigation panel.

    4. Repeat [3.a](custom-navigation-panels.md#cnp-substep3a) to [3.c](custom-navigation-panels.md#cnp-substep3c) until you have added all of the required categories to your navigation panel design.

    5. Click **Save**.

4. Optionally, add one or more custom menu items to your navigation panel and define their target.

    1. <span id="cnp-substep4a"></span> Click **+ Add menu item** to open the Create Custom Menu form.

    2. Select a **Category** from within your custom navigation panel to contain your menu item.

    3. <span id="cnp-substep4c"></span>Enter a **Custom Menu Name** for your menu item.

    4. Specify the target page for the custom link by providing a URL in the **Custom Menu Link** field. Both internal and external links are supported.

        - Internal links for the Topologies page within the EDA GUI are defined by their relative path. For example: `/ui/app/main/topologies.eda.nokia.com/v1alpha1/topologies`.
        - External links can be defined with a URL. For example: [https://docs.eda.dev/](https://docs.eda.dev/).
  
    5. If the required **Custom Menu Link** field is set to /ui/main/queryapi, use the **Optional Navigation Query** field to define an EQL query to load when opening the target page.

        /// admonition | Note
            type: subtle-note
        The **Optional Navigation Query** field only functions if you select the `/ui/main/queryapi` endpoint in the navigation field as described above. No other menu options can incorporate this query into their navigation.
        ///

    6. <span id="cnp-substep4f"></span>Use the **Open link in new tab** check box to indicate whether the target page should replace the current tab, or open a new tab when it opens.

        /// admonition | Note
            type: subtle-note
        External links always open in a new tab.
        ///

    7. Repeat [4.a](custom-navigation-panels.md#cnp-substep4a) through [4.f](custom-navigation-panels.md#cnp-substep4f) until you have added all of the required custom menu items to your navigation panel design.

    8. Click **Save**.

        Your custom menu item is added to the navigation panel design, under the category you selected.

5. Add one or more standard categories or individual menu items from the EDA main menu to your navigation panel design.

    1. <span id="cnpsub5a"></span>Do either of the following to find your intended category or menu item:

        - Expand any of the standard menu categories that are listed under **Available menu items** to reveal the intended menu item.
        - Use the Search field under **Available menu items** to find a particular category or menu item.

    2. <span id="cnpsub5b"></span>Click and drag the category or menu item from the **Available menu items** to the intended position within your navigation panel design.

        /// admonition | Note
            type: subtle-note
        If you drag a menu category from **Available menu items**, all of its menu items are also added to your panel design under that category.
        ///

    3.  Repeat [5.a](custom-navigation-panels.md#cnpsub5a) and [5.b](custom-navigation-panels.md#cnpsub5b) until you have added all of the required categories and menu items to your navigation panel design.

6. To remove a category or menu item from your navigation panel design by clicking the trash icon next to that item in the **Selected menu items** list.

    /// Noate
    This action is most useful if you began by duplicating another, complete menu from which you would like to trim some items.
    ///

7. To edit a category or menu item in your navigation panel design, do the following:

    1. Click the pencil icon next to that item in the **Selected menu items** list.

    2. In the resulting Edit form, do any of the following:

    - For a custom or standard category: edit the category name or change the associated icon.
    - For a custom or standard menu item: change any of the properties of the menu item, including:

        - Category
        - Custom Menu Name
        - Custom menu Link
        - Optional Navigation Query
        - Open link in new tab check box value
        You can also reorder categories and the custom menus inside them, as well as move the custom menus between categories in the panel you are building.

8. Click **Save**.

///

## Managing custom panels <span id="managing-custom-nav-panel"></span>

EDA supports the following actions for custom navigation panels:

- Duplicate an existing standard or custom navigation panel
- Hide an existing standard or custom navigation panel
- Re-display any hidden navigation panel
- Edit an existing custom navigation panel
- Delete an existing custom navigation panel
- Publish a custom panel to share it with other EDA users

    /// admonition | Note
        type: subtle-note
    Sharing a panel automatically makes it available to all users who have access to the shared folder. The ability to see or edit shared panels can be managed through security permissions applied on the ClusterRole URL rule for the path `/core/user-storage/v2/shared/file`.
    ///

/// admonition | Note
    type: subtle-note
You cannot edit or delete the standard Main or System Administration navigation panels.
///

/// html | div.steps

1. Use the **Main** navigation panel to select **Manage Panels** to open the Manage Panels form.

2. Find the navigation panel you want to work with in the resulting list.

3. Select the action that you want from the **Table row action**drop-down list:

    - To duplicate a panel, go to step [4](custom-navigation-panels.md#mcp-4).
    - To hide a navigation panel, click **Hide Panel** and go to step [7](custom-navigation-panels.md#mcp-7).
    - To re-display a hidden navigation panel, click **Unhide Panel** and go to step [7](custom-navigation-panels.md#mcp-7).
    - To edit a navigation panel, go to step [5](custom-navigation-panels.md#mcp-5).
    - To publish \(share\) a navigation panel, click **Publish** and go to step [7](custom-navigation-panels.md#mcp-7).
    - To delete a navigation panel, go to step [6](custom-navigation-panels.md#mcp-6).

4. <span id="mcp-4"></span>To duplicate the navigation panel, do the following:

    1. Click **Duplicate Panel** to open the Duplicate Panel page.

    2. Name and modify the duplicate panel, following the procedure for managing content for a new custom navigation panel.

    3. Click **Save**.

    4. Go to step [7](custom-navigation-panels.md#mcp-7).

5. <span id="mcp-5"></span>To edit the selected custom navigation panel, do the following:

    1. Click **Edit Panel** to open the Edit Panel page.

    2. Modify the panel, following the procedure for managing content for a new custom navigation panel.

        /// admonition | Note
            type: subtle-note
        You cannot edit the name of the custom navigation panel.
        ///

    3. Click **Save**.

    4. Go to step [7](custom-navigation-panels.md#mcp-7).

6. <span id="mcp-6"></span>To delete the selected custom navigation panel, do the following:

    1. Click **Delete Panel**.

    2. Click **OK** in the confirmation message.

7. <span id="mcp-7"></span>Click the **Close** button to close the form and complete this procedure.

///
