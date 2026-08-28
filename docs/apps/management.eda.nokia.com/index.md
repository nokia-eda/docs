# Management Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [nokia/catalog/management ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

The management application provides resources to configure target nodes as servers for various protocols:

- [FTP](./resources/ftpserver.md) for file access
- [SSH](./resources/sshserver.md) for remote access
- [HTTP](./resources/httpserver.md) for remote management (JSON-RPC)
- [gRPC](./resources/grpcserver.md) for remote management (GRPC)
- [SNMP](./resources/snmpserver.md) for remote management (SNMP)

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`FTPServer`](./resources/ftpserver.md)
* [`GRPCServer`](./resources/grpcserver.md)
* [`HTTPServer`](./resources/httpserver.md)
* [`SSHServer`](./resources/sshserver.md)
* [`SNMPServer`](./resources/snmpserver.md)

</div>
</div>
///

## Server reachability

A server is reachable through a particular routed network instance (IP-VRF). The following options are available:

- The out-of-band [ManagementRouter](-{{ref_app_doc('bootstrap', 'managementrouter')}}-)
- The in-band [DefaultRouter](-{{ref_app_doc('routing', 'defaultrouter')}}-)
- An in-band virtual [Router](-{{ref_app_doc('services', 'router')}}-)

The server is deployed on all nodes that are part of the selected `router`. If the router kind is `DefaultRouter`, multiple routers can be selected through the `routerSelectors` property.
