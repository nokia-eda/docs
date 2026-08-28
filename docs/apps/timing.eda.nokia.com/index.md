# Timing Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/timing ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

The timing application provides abstractions for maintaining an accurate time reference on devices.

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`NTPClient`](./resources/ntpclient.md)
* [`TimeZone`](./resources/timezone.md)

</div>
</div>
///

A network element keeps accurate time when it is a [client](./resources/ntpclient.md) of an NTP server and is configured with the appropriate [time zone](./resources/timezone.md). The primary reason to add a time zone is to influence the timestamps of [log messages](-{{ref_app_doc('logging', 'index.md')}}-).