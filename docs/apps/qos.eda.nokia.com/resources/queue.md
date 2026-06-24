---
resource_name: Queue
resource_name_plural: queues
resource_name_plural_title: Queues
resource_name_acronym: Q
crd_path: docs/apps/qos.eda.nokia.com/crds/qos.eda.nokia.com_queues.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Queue

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

??? abstract "A brief introduction to QoS"

    Quality of Service (QoS) is a set of technologies and mechanisms used to manage traffic prioritization, often but not exclusively used in scenarios of network congestion. A full explanation of QoS is beyond the scope of this documentation, as the concepts are often as complex as the implementation of them on various network operating systems, along with chip-specific capabilities and limitations.

Queues are intermediary first-in, first-out storage systems for packets as they are processed by a router. Although support depends on the hardware platform, generally there are queues for ingressing packets and for egressing packets.

When a packet arrives on a network element, the packet is **classified** by an [`IngressPolicy`](./ingresspolicy.md) based on packet headers - the classification (priority level) of the packet is called a [forwarding class](./forwardingclass.md). Based on this [forwarding class](./forwardingclass.md), the packet is assigned to a `Queue` with a particular size (which can be static or dynamically growing/shrinking). From there, a scheduler visits all queues to dequeue packets for processing.

After the router decides where the packet should go, it goes through the same process on egress: based on the [forwarding class](./forwardingclass.md) that is attached to the packet, an [`EgressPolicy`](./egresspolicy.md) determines which egress `Queue` for that particular (sub)interface the packet will be added to. Again, a (port-specific) scheduler visits the queues in order of priority and dequeues packets that are then being forwarded out of the interface.

The information above is an abstracted and simplified view. The reality and OS-specific implementations introduce a lot of nuance and sometimes restrictions that need to be taken into account when designing a QoS architecture. For a full understanding of your network behavior, refer to the OS-specific documentation.

!!! note "Dropped packets"

    While schedulers decide which packets are picked up for further processing, they do not decide which packets get dropped in case of congestion: when a queue fills up, any packets that do not fit in a queue are dropped.

Several `Queue` resources are created by default when deploying EDA. They can be used as-is for unicast traffic or overwritten. 

## PFC

Priority-based Flow Control or PFC is a mechanism (IEEE 802.1Qbb) that enables a network element to signal to one of their neighbors to stop sending traffic for a particular priority. When the queue depth (on ingress) exceeds the `pfcOnThresholdPercent` property of a `Queue` of an [`IngressPolicy`](./ingresspolicy.md), the switch will send out a PFC frame out of that interface to stop sending traffic for that particular priority.

## Dependencies

The `Queue` resource does not have any dependencies on other EDA resources.

## Referenced resources

The `Queue` resource does not reference any other EDA resources.

## Examples

/// tab | YAML

```yaml
-{{ include_snippet(resource_name) }}-
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
-{{ include_snippet(resource_name) }}-
EOF
```

///

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
