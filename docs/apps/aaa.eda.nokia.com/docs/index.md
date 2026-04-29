# AAA Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                        |
| -------------------- |----------------------------------------|
| **Group/Version**     | -{{app_group}}-/-{{app_api_version}}-  |
| **Supported OS**     | -{{supported_os_versions(app_group)}}- |
| **Catalog**          | [nokia-eda/catalog/aaa][manifest]      |
| **Source Code**      | <small>coming soon</small>             |

[manifest]: https://github.com/nokia-eda/catalog/blob/main/vendors/nokia/apps/aaa/manifest.yaml

AAA stands for "Authentication, Authorization, and Accounting". As the name implies, it covers the following three topics:

- Determining **who** someone/something is
- Defining **what** someone/something can do
- **Logging** what someone/something does

In network operating systems, authentication is usually done through an account consisting of a **username** and a **password** and/or **private key**. 

The AAA application provides the following components:

/// tab | Resource Types

<div class="grid" markdown>
<div markdown>

* [Node Groups](resources/nodegroup.md)
* [Server Groups](resources/servergroup.md)
* [Authentication Policies](resources/authenticationpolicy.md)

</div>
</div>
///

## Users and Groups

Users are identified by their username and a password or private key (authentication). A user is configured on a set of nodes, and is linked to a [group](resources/nodegroup.md). The group defines what the user can or cannot do (authorization).

!!! info 
    Node users are a core feature of EDA, and are not discussed in this article.
