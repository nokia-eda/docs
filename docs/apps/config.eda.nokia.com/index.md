# Config Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/config ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

Configuration management is one of the core pillars of the EDA network management system. When it comes to configuration, every EDA resource falls into one of four categories:

1. Resources that do not result in configuration being pushed to a node.
    - Example: an `IPAllocationPool`.
2. Resources that create other derived EDA resources.
    - Example: a [`VirtualNetwork`](-{{ref_app_doc('services', 'virtualnetwork')}}-).
3. Resources that are configured on a node only when another resource references them.
    - Example: a [`PrefixSet`](-{{ref_app_doc('routingpolicies', 'prefixset')}}-).
4. Resources whose creation directly results in configuration being pushed to nodes.
    - Example: an [`Interface`](-{{ref_app_doc('interfaces', 'interface')}}-).

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`Configlet`](./resources/configlet.md)

</div>
</div>
///


## Custom configuration

Not every configuration parameter in every version of each supported operating system is available through an EDA abstraction. To fill this gap while waiting for official EDA support, users are encouraged to write abstraction applications that fulfill their needs.

Although we continuously improve the developer experience, writing an application may seem daunting. It may also be excessive when only one configuration setting needs to change.

This is where the [`Configlet`](./resources/configlet.md) comes in: it allows the operator to specify which configuration options need to be pushed to which nodes, providing a quick and EDA-managed abstraction that encompasses your network's needs.

/// admonition
    type: warning

Do not rely on deviations (manual changes through the CLI) for short- or long-lived workarounds. Instead, convert each deviation into a [`Configlet`](./resources/configlet.md) to track it and ensure that it is retained when a node reboots.
///