# Services Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/services ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

!!! info "Documentation coming soon!"

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`BridgeDomain`](./resources/bridgedomain.md)
* [`BridgeDomainInterconnect`](./resources/bridgedomaininterconnect.md)
* [`BridgeInterface`](./resources/bridgeinterface.md)
* [`DHCPRelay`](./resources/dhcprelay.md)
* [`IRBInterface`](./resources/irbinterface.md)

</div>
<div markdown>

* [`RoutedInterface`](./resources/routedinterface.md)
* [`Router`](./resources/router.md)
* [`RouterInterconnect`](./resources/routerinterconnect.md)
* [`VirtualNetwork`](./resources/virtualnetwork.md)
* [`VLAN`](./resources/vlan.md)

</div>
</div>
///

/// tab | Workflows
<div class="grid" markdown>
<div markdown>

* [`EdgePing`](./resources/edgeping.md)

</div>
</div>
///
