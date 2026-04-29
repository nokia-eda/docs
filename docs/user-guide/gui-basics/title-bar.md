# Title bar

The following elements are available at the upper right of every page within the Nokia EDA UI.

## Namespace selector

The namespace drop-down specifies the namespace you are working in. The Nokia EDA UI includes the selected namespace in API server requests.

If you have selected **All Namespaces**, data grids contain data from all namespaces. You must have permissions defined in a cluster role to access data in this view.

**Related information**  

- [Namespaces](../namespaces.md)

## Transaction Basket

Click the **Transaction basket** icon to open the Transactions drop-down panel.

-{{image(url="../graphics/btn-transactions.png", title="Transactions button", shadow=true, padding=20)}}-

The Transactions drop-down panel displays recent transactions from the current user, and a basket area for staging one or more resource changes for a new transaction.

**Related information**  

- [Transactions](../transactions.md)

## Workflows <span id="btn-workflows"></span>

A workflow is a series of steps required to perform a task or process, such as performing a ping or performing a route lookup.

The **Workflows** button allows you to interact with workflows from anywhere in the Nokia EDA UI.

-{{image(url="../graphics/btn-workflow.png", title="Workflows button", shadow=true, padding=20)}}-

When you click the **Workflows** button, the 10 most recent workflows that you executed are displayed, along with any related notifications, such as if a workflow has completed or is waiting for input. From here, you can:

- click one of the workflow executions to take you to its Summary page.
- click the **List** button to take you to the Workflow Executions page.

**Related information**  

- [Workflows](../workflows.md)
- [Workflow Executions page](../workflows.md#workflow-executions-list)
- [Workflow Summary page](../workflows.md#workflow-summary-page)

## Ask EDA

**Ask EDA** is EDA chat interface. You can click the Ask EDA icon from anywhere in the Nokia EDA to open a chat window.

-{{image(url="../graphics/ask-eda-icon.png", title="Ask EDA icon", shadow=true, padding=20)}}-

From the **Ask EDA** chat interface, you can make natural-language queries, enter CLI **show** commands, perform root-cause analysis of alarms and transactions, create charts, and so forth.

**Related information**  

- [Ask EDA](../ask-eda.md)

## User settings <span id="btn_user-settings"></span>

Opening the **User** drop-down panel displays information and available actions for the currently logged-in user.

-{{image(url="../graphics/btn-user.png", title="User settings button", shadow=true, padding=20)}}-

- **User information**: displays the following user and login information:
    - name of the currently logged-in user
    - role of the user
    - date and time of the last successful login
- **Appearance Theme**: click to select a display theme from among the following:
    - Follow system theme: ignore the Nokia EDA theme settings, and instead adopt a light or dark theme based on your system settings.
    - Light: primarily displays dark text on a light background
    - Dark: primarily displays light text on a dark background
    - Enhanced Dark: like Dark, but employs even darker background shading
- **High Contrast Charts**: controls the color selection for chart segments; enabling high-contrast charts makes Nokia EDA charts easier to read for colorblind users.
- **Change Password**: click to change the password for the current user. You must re-authenticate before you can complete the password change.
- **Sign Out**: click to sign out of the Nokia EDA application.

## Help <span id="btn_help"></span>

Click to access the following available information:

- API Documentation: opens the API Documentation page.

/// admonition | Note
    type: subtle-note
From the API Documentation page, you can download the API documentation as a zip file.
///

- Hotkeys: opens a form displaying the keyboard hotkeys available for action.

/// admonition | Note
    type: subtle-note
You can also see the list of hotkeys by pressing "Shift-?" on your keyboard.
///

- Release Information: opens a form displaying the Nokia EDA release number and version.
