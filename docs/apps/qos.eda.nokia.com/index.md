# QoS Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/qos][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

Quality of Service (QoS) is a set of technologies and mechanisms used to manage traffic prioritization, often but not exclusively used in scenarios of network congestion. A full explanation of QoS is beyond the scope of this documentation, as the concepts are often as complex as the implementation of them on various network operating systems, along with chip-specific capabilities and limitations.

When a packet enters through a physical interface, a specific [`IngressPolicy`](./resources/ingresspolicy.md) inspects the headers of the packet and assigns it a [`ForwardingClass`](./resources/forwardingclass.md) and (optionally) a [color or drop probability](./resources/ingresspolicy.md#classification).

Based on the [`ForwardingClass`](./resources/forwardingclass.md) and/or [color](./resources/ingresspolicy.md#classification), the packet may be sent to a [policer](./resources/ingresspolicy.md#policing) for rate-limiting. If the packet is not dropped, the router decides where the packet needs to go and assigns it to a [`Queue`](./resources/queue.md). When a packet enters a [`Queue`](./resources/queue.md), it is either dropped because the [`Queue`](./resources/queue.md) is full, discarded by a [slope policy](./resources/egresspolicy.md#queue-management-and-slope-policies), or accepted.

The [`EgressPolicy`](./resources/egresspolicy.md) then (optionally) converts the [`ForwardingClass`](./resources/forwardingclass.md) to priority bits, after which the scheduler empties the queue and sends the packets out to the next hop in the network.

Policies are applied to (sub)interfaces by creating either a [`PolicyDeployment`](./resources/policydeployment.md) or a [`PolicyAttachment`](./resources/policyattachment.md) resource.

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`ForwardingClass`](./resources/forwardingclass.md)
* [`Queue`](./resources/queue.md)
* [`IngressPolicy`](./resources/ingresspolicy.md)
* [`EgressPolicy`](./resources/egresspolicy.md)
* [`PolicyDeployment`](./resources/policydeployment.md)
* [`PolicyAttachment`](./resources/policyattachment.md)

</div>
</div>
///
