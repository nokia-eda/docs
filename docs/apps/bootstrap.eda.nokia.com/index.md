# Bootstrap Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/bootstrap ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

The bootstrap application contains resources that enable an operator to onboard nodes under EDA.

Before a node is onboarded, some configuration needs to be pushed so that EDA can perform the initial connection. That configuration is produced by the [`Init`](./resources/init.md) resource (shown as **Bootstrap** in the UI), which also allows limited options such as the MTU of the management port.

This initial configuration is pushed by the ZTP process. After that, EDA can [rotate the node TLS certificate](./resources/rotatecertificate.md) used for the gNMI connection. When EDA has a secured connection to the node, it starts pushing configuration produced by other EDA resources.

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`Init`](./resources/init.md) (Bootstrap in the UI)
* [`ManagementRouter`](./resources/managementrouter.md)
* [`Satellite`](./resources/satellite.md)

</div>
</div>
///

/// tab | Workflows
<div class="grid" markdown>
<div markdown>

* [`RotateCertificate`](./resources/rotatecertificate.md)

</div>
</div>
///
