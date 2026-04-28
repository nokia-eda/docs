# Users

Users are individuals with access to the EDA system. Users gain access to application and network resources through the user groups to which they are assigned. A user can be assigned to more than one user groups, either locally or through an external directory.

Individual users can also be assigned roles directly, without membership to a user group.

## Types of users

The following types of users interact with EDA components:

- Local users are created locally on the EDA system and authenticated using Keycloak.
- Remote users are configured on a remote directory, such as a Lightweight Directory Access Protocol (LDAP) server, that the system queries to authenticate remote users when they try to log in. For more information, see [Remote directories](remote-directories.md).
- Node users are configured with access to a set of TopoNodes. A NodeUser resource configures a node user's password, SSH keys, and group bindings.

## Default admin user

EDA comes with a default local user called admin. The admin user is assigned to the system-administrator group and can perform the following functions:

- create, update, and delete users (except for the admin user)
- manually set a password for users during creation
- modify the password of the admin user and perform other functions other than modifying its group
- disable or enable non-admin users without deleting the user

## Users page

The **Users** page in the UI lists all local and remote EDA users and a provides a summary of user details. You can sort and filter for users using the typical mechanisms described in [Working with data grids](gui-basics/data-grids.md).

|Column|Description|
|------|-----------|
|Username|The login name for the user.|
|First Name|The first name of the user.|
|Last Name|The last name of the user.|
|Enabled|Indicates whether the user account is active or disabled.|
|Last Successful Login|The timestamp for the user's last successful login.|
|Federated User|The federation provider, if the user is a federation user.|
|Failed Logins Since Successful Login|The number of failed log in attempts after a user successfully logs in. This counter resets to 0 after the user successfully logs in again.|
|Last Failed Login|The timestamp for the user's last login failure.|
|Temporarily Disabled|Indicates if a user is temporarily disabled because of exceeding the allowed number of failed log in attempts.|

**Parent topic:** [Securing access to EDA](secure-access-eda.md)

## Creating a new local user <span id="create-new-user"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT** and select **User Management**.

2. From the **User Management** drop-down list, click **Users**.

3. Click **Create**.

4. In the **User Information** section, enter the required information for the new user.

    - a username
    - the user's first and last name
    - the user's email address
  
5. Click **Set Password**.

    In the form that opens, provide a password and confirm it. By default, the password is temporary and a user must log in and provide a new password for the newly created account.

6. Assign this user to one or more user groups.

    From the **Assigned User Groups** drop-down list, select an existing user group. Optionally, you can create a user without assigning the user to a user group. Later, you can add the user to a user group.

7. Click **Save**.

///

## Managing user accounts <span id="manage-user-accounts"></span>

**Note:** A user with system-administrator privileges cannot delete the built-in admin user or modify its groups or roles.
/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT** and click **User Management**.

2. Click **Users** from the **User Management** drop-down list.

3. You can act on a single user or many users.

    - To manage a single user, locate the user and click the action that you want to take from the **Table row actions** menu.
        - Click **Edit** to update details for a user such as user first name and last name, and assigned user groups. You can also enable or disable a user.
        - Click **Set Password** to set a new password.
    - Alternatively, you can select more than one user, then click the **Table settings &amp; actions button** icon. You can perform one of the following multi-row actions:
        - Delete the selected users.
        - Set passwords for the selected users.
        - Disable or enable the selected users.
4. Click **Save**.

///

## Changing your password <span id="changing-your-password"></span>

Perform this task from any page on EDA UI.

/// html | div.steps

1. Click the user icon at the upper right of the screen and select **Change Password**.

2. When prompted, log in again with your credentials.

3. Enter your new password and confirm it.

4. Click **Save**.

///

## Restoring a user's default persistent settings <span id="restore-default-persistent-settings-for-users"></span>

The `edactl aaa user settings clear` command restores a user's persistent settings in EDA to the default settings. This command is useful in scenarios where a user inadvertently writes an incompatible or errored change to their persistent settings, resulting in the browser going into a perpetual error loop.

The command does not impact dashboards and other user-generated content, but does impact settings for grid layouts, dark mode settings, and so forth.
