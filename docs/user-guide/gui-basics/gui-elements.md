# GUI elements

The following elements are available at the upper right or right edge of every page within the EDA GUI. This section also contains recurring elements that appear on multiple pages within the EDA GUI.

## Transactions

A transaction defines a set of changes that need to occur synchronously in EDA.

Click the **Transactions** basket icon to open the Transactions drop-down panel.

-{{image(url="../graphics/btn-transactions.png", title="Transactions button", shadow=true, padding=20)}}-

The Transactions drop-down panel displays information and options for the current transaction. From here you can edit the configuration changes contained within the transaction, discard the transaction, or commit the transaction.

**Related information**  

- [Transactions](../transactions.md)

## Workflows <span id="btn-workflows"></span>

A workflow is a series of steps required to perform a task or process, such as performing a ping or performing a route lookup.

The **Workflows** button allows you to interact with workflows from anywhere in the EDA UI.

-{{image(url="../graphics/btn-workflow.png", title="Workflows button", shadow=true, padding=20)}}-

When you click the **Workflows** button, the 10 most recent workflows that you executed are displayed, along with any related notifications, such as if a workflow has completed or is waiting for input. From here, you can:

- click one of the workflow executions to take you to its Summary page.
- click the **List** button to take you to the Workflow Executions page.

**Related information**  

- [Workflows](../workflows.md)
- [Workflow Executions page](../workflows.md#workflow-executions-page)
- [Workflow Summary page](../workflows.md#workflow-summary-page)

## User settings <span id="btn_user-settings"></span>

Opening the **User** drop-down panel displays information and available actions for the currently logged-in user.

-{{image(url="../graphics/btn-user.png", title="User settings button", shadow=true, padding=20)}}-

- **User information**: displays the following user and login information:
    - name of the currently logged-in user
    - role of the user
    - date and time of the last successful login
- **Appearance Theme**: click to select a display theme from among the following:
    - Follow system theme: ignore the EDA theme settings, and instead adopt a light or dark theme based on your system settings.
    - Light: primarily displays dark text on a light background
    - Dark: primarily displays light text on a dark background
    - Enhanced Dark: like Dark, but employs even darker background shading
- **High Contrast Charts**: controls the color selection for chart segments; enabling high-contrast charts makes EDA charts easier to read for colorblind users.
- **Change Password**: click to change the password for the current user. You must re-authenticate before you can complete the password change.
- **Sign Out**: click to sign out of the EDA application.

## Help <span id="btn_help"></span>

Click to access the following available information:

- API Documentation: opens the API Documentation page.

/// admonition | Note
    type: subtle-note
From the API Documentation page, you can download the API documentation as a zip file.
///

- Hotkeys: opens a form displaying the keyboard hotkeys available for EDA actions.

/// admonition | Note
    type: subtle-note
You can also see the list of hotkeys by pressing "Shift-?" on your keyboard.
///

- Release Information: opens a form displaying the EDA release number and version.

## Information panel <span id="btn_information"></span>

Most pages in the EDA GUI include an **Information** panel. You can open this panel by clicking the **Expand/Contract** control at the middle right of any page.

The Information panel displays information about any selected object on the corresponding main page.

To enhance readability, fields that would contain no information are excluded from the information panel.

-{{image(url="../graphics/sc0206.png", title="An example of an expanded information panel, showing the collapse control", shadow=true, padding=20)}}-

## Split view panel <span id="btn-yaml-and-json"></span>

When viewing the details of an element in the EDA GUI, such as a node or a workflow, the **Details** page opens and displays outline, status, and configuration information for the element. The **Split view** panel displays configuration information that can be viewed in either YAML or JSON format.

You can switch between YAML and JSON format by clicking the drop-down menu and selecting the format.

-{{image(url="../graphics/sc0304.png", title="Split view panel", shadow=true, padding=20)}}-

## Related targets <span id="btn-related-targets"></span>

When viewing a resource in the EDA UI, the **Related targets** view allows you to view a list of targets where the selected resource's intent generated a part of the target's configuration.

/// admonition | Note
    type: subtle-note
The **Related targets** view does not account for read relationships between resources. For example, BGP group resources do not have any related targets because the BGP configuration of the target is generated by a different resource intent which reads the BGP group resource as an input.
///

You can switch to the **Related targets** view by selecting **Related targets** from the drop-down list at the upper right of the page.

-{{image(url="../graphics/sc0305.png", title="Related targets view", shadow=true, padding=20)}}-
