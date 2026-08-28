# Logging Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [nokia/catalog/logging ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

The logging application retrieves, filters, and stores messages. A [`Log`](./resources/log.md) resource sends messages captured by one or more [`Source`](./resources/source.md) resources to one or more [`Destination`](./resources/destination.md) resources.

A [`Source`](./resources/source.md) acts as a filter that selects only the messages relevant to the [`Log`](./resources/log.md). The messages are stored in memory or in a file on the node's file system, or sent to a syslog server.

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`Log`](./resources/log.md)
* [`Source`](./resources/source.md)
* [`Destination`](./resources/destination.md)

</div>
</div>
///