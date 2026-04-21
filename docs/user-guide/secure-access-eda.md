# Securing access to EDA

EDA uses Keycloak, a well-known and secure solution, for its identity and access management. Authentication is required to interact with EDA.

EDA implements authorization through role-based access control (RBAC) for the following elements:

Users
:   Individuals with access to the system. Each user has a user information profile to store information about them. System administrators can assign users to user groups.

User groups
:   A collection of users organized according to the type of activities they are meant to perform. You assign resource access rights to user groups through user roles. When you assign a role to a user group, all access rights defined in the role are inherited by the users of the group.

Roles
:   Specifies which resources users or associated user group members can access. You assign network resource access to roles through resource groups. Each member of a group can perform the roles specified for that group.

    A role that exists in a namespace is referred to as a *role*. A role that exists cluster wide \(that is, it is not in a namespace\) is referred to as a *cluster role*.

A user can belong to more than one group, and a group can be assigned multiple roles.

## Subtopics

- **[Roles](roles.md)**  

- **[User groups](user-groups.md)**  

- **[Users](users.md)**  

- **[Password policies](password-policies.md)**  

- **[Remote directories](remote-directories.md)**  

**Parent topic:** [Security](security.md)
