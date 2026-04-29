# Filters Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/filters ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: fill in the hyperlink to the published manifest in the public catalog)
[manifest]: https://docs.eda.dev/

The `filters` application adds functionality for packet filtering.

A properly hardened communication network has traffic filters in place to protect the network from malicious or malfunctioning client devices. 

Usually, a combination of hardware and software filters are used: **hardware filters** operate on the linecard, and are able to drop packets that match certain criteria, often at line rate. **Software filters** provide an additional layer of security for packets that are destined for the CPU (control plane traffic).

Use [`Filters`](resources/filter.md) for:

- Dropping traffic from a certain IP subnet into a [`Router`](../../services.eda.nokia.com/docs/resources/router.md) service
- Rate-limiting packets with the broadcast MAC address `ff:ff:ff:ff:ff:ff` as destination

Use [`ControlPlaneFilters`](resources/controlplanefilter.md) for:

- Only allowing SSH / BGP connections from a particular IP-subnet
- Rate-limiting the number of ICMP Echo requests processed by the node

The `filters` application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`Filter`](resources/filter.md)
* [`PrefixSet`](resources/prefixset.md)
* [`ControlPlaneFilter`](resources/controlplanefilter.md)

</div>
</div>
///

/// tab | Workflows
<div class="grid" markdown>

The `filters` app has no workflows

</div>
///
