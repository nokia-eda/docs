# User groups

A user group associates multiple users with a role, enabling them to access EDA resources. An admin user can create user groups and assign a specific role to each group according to the type of network activities the user group is meant to perform. When a role is assigned to a user group, all users within the group have the same access to resources, as specified by the role.

EDA comes with a default user group called system-administrator. Users who belong to this group can:

- Create, update, and delete local groups
- Assign local users to local groups
- Assign remote users to local groups
- View all users and their group memberships

## Viewing user groups

From the **System Administration** navigation panel, expand **USER MANAGEMENT** and click **User Management**. Select **User Groups** from the drop-down list.

**Note:** LDAP groups are displayed in the **User Groups** page only after they are imported from an LDAP server.

**Parent topic:** [Securing access to EDA](secure-access-eda.md)

## Creating a user group <span id="create-user-group"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand the **USER MANAGEMENT** group, then click **User Management**.

2. Click **User Groups** from the **User Management** drop-down list.

3. Click **Create**.

4. Provide a name for this user group.

5. In the **Assigned Users** section, click **+ Add**.

    Select the users that you want to assign to this user group, then click **Save**.

6. From the **Assigned Roles** drop-down list, select a role to assign to the user group.

    You can only select one role.

7. Click **Save**.

///

## Deleting user groups <span id="delete-user-groups"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand the **USER MANAGEMENT** group, then click **User Management**.

2. Click **User Groups** from the **User Management** drop-down list.

3. Delete one or more user groups.

    - To delete one user group, locate the user group that you want to delete and click **Delete** from the **Table row actions** menu.
    - Alternatively, you can click one or more user groups. Then, click **Delete** from the **Table settings &amp; actions** menu.

4. Click **Save**.

///
