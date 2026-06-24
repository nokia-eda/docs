---
resource_name: IngressPolicy
resource_name_plural: ingresspolicys
resource_name_plural_title: Ingress Policies
resource_name_acronym: IP
crd_path: docs/apps/qos.eda.nokia.com/crds/qos.eda.nokia.com_ingresspolicys.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Ingress Policy

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

??? abstract "A brief introduction to QoS"

    Quality of Service (QoS) is a set of technologies and mechanisms used to manage traffic prioritization, often but not exclusively used in scenarios of network congestion. A full explanation of QoS is beyond the scope of this documentation, as the concepts are often as complex as the implementation of them on various network operating systems, along with chip-specific capabilities and limitations.

An `IngressPolicy` is used to **map** an incoming packet to a particular [Queue](./queue.md). It operates in 3 stages, each of which is explained in more detail below:

1. Inspect the packet headers and **classify** it: classification means that the packet is assigned an internal-only [`ForwardingClass`](./forwardingclass.md) tag
2. Police the incoming traffic: limit the bandwidth of certain traffic classes
3. Based on the [`ForwardingClass`](./forwardingclass.md), map the packet to a particular [`Queue`](./queue.md)

In addition, the `IngressPolicy` also determines the parameters of the `Queue`, such as Committed Burst Size (CBS), Maximum Burst Size (MBS), and PFC[^1] parameters.

!!! warning "Mapping a forwarding class to a queue"

    Currently, EDA does not support mapping a forwarding class to a [`Queue`](./queue.md) on ingress, even though it can be configured through the `forwardingClassToQueueMapping` property: this property is ignored.

    ??? question "Why?"
    
        While advanced routers like the Nokia 7750 SR have dedicated queues for ingressing and egressing traffic, in the datacenter there is often only one queue being used. This queue is either a Virtual Output Queue (VOQ) before the packet crosses the forwarding fabric, or an Egress Queue (EGQ) after the packet has crossed the forwarding fabric. The technical reason for this, as well as their benefits and drawbacks, are beyond the scope of this article.

## Classification

Traffic streams can be prioritized by looking at certain packet headers. Currently supported headers include:

- IP header
    * based on source / destination prefix, source / destination port, ...
    * based on the DSCP priority bits
- MAC header
    * based on the dot1p priority bits

Each classifier will map a packet to a [`ForwardingClass`](./forwardingclass.md) and drop probability or **"color"**. The lower the drop probability, the less likely a packet is to be dropped while in the queue. When the queue is full, all new incoming packets are discarded regardless of drop probability. This mechanism is known as color marking and requires policers (on ingress) or slope policies (on egress) to be active on the node to be effective.

### IP entry

When using the `ipEntry` classifier, you can optionally rewrite the DSCP value. This can be useful to re-assess priorities, or it can be used to ignore priority bits altogether when packets ingress the network.

### Dot1p entry

The `dot1pPolicyEntry` creates a classifier that inspects the Priority Code Point (PCP) bits of a VLAN tag in an ethernet header. Based on the PCP bits, the packet is assigned a particular [`ForwardingClass`](./forwardingclass.md). The PCP field is 3 bits long, and therefore has values ranging from 0 to 7 (inclusive).

### DSCP entry

The `dscpPolicyEntry` creates a classifier that inspects the Differentiated Services Code Point (DSCP) bits in an IP header. The DSCP field is 6 bits long, and therefore has values ranging from 0 to 63 (inclusive).

## Policing

Policers count bits per second, and can recolor packets (re-assign drop probabilities) if the packets that are counted by this policer exceed a certain bandwidth. That's a lot to unpack: let's break it down:

- An [`IngressPolicy`](./ingresspolicy.md) determines which combination of [`ForwardingClass`](./forwardingclass.md) and traffic types (unicast, multicast, ...) are policed by a certain policer.
- The policer counts the packets that pass through it, and takes one of three actions.
    * A packet that comes in while the policer is in a normal (non-exceeding) state, is not recolored.
    * A packet that comes in while the policer exceeds the committed rate (CIR), but below the peak rate (PIR), is recolored in accordance with `exceedAction`.
    * A packet that comes in while the policer exceeds the peak rate (PIR) is recolored in accordance with `violateAction`.

!!! question "What about pre-coloring?"

    Policers rely on a two-rate token-based system, where each packet drains a number of tokens from one, two, or zero buckets (depending on pre-coloring done by the classifiers) that are continuously being refilled. There are a lot of nuances to this mechanism and there are subtle implementation differences between operating systems and even hardware platforms. For an in-depth overview of policers, refer to the OS-specific user documentation.

## Queueing

When a packet has been classified (assigned a forwarding class) and colored (assigned a drop probability or 'color') and has not been dropped by the `violate-action` of the policer, the router performs a forwarding lookup that determines the egress port for the packet. Depending on the hardware platform, the packet is enqueued in a VOQ (Virtual Output [`Queue`](./queue.md)) or EGQ (Egress [`Queue`](./queue.md)). 

If there is room in the [`Queue`](./queue.md), the packet is added to the queue. If there is no room left in the [`Queue`](./queue.md), the packet is dropped.

## Slope policies

Slope policies drop a certain percentage of incoming packets when a packet enters the queue. The percentage is based on the occupancy of the [`Queue`](./queue.md) and the configuration of the slope policy of the [`EgressPolicy`](./egresspolicy.md), and is discussed in more detail in the [`EgressPolicy`](./egresspolicy.md) documentation article.

## Dependencies

### [`ForwardingClass`](./forwardingclass.md)

Most QoS mechanisms either assign a [`ForwardingClass`](./forwardingclass.md) to a packet, or take an action based on the assigned [`ForwardingClass`](./forwardingclass.md). These must exist as a resource if the `IngressPolicy` refers to them.

!!! warning "Deployment of a ForwardingClass"

    Both the `IngressPolicy` and [`EgressPolicy`](./egresspolicy.md) resources refer to a [`ForwardingClass`](./forwardingclass.md) by name, and therefore this name must exist on the node. Only the [`EgressPolicy`](./egresspolicy.md) configures these, which means that a (default) [`EgressPolicy`](./egresspolicy.md) must always be configured that maps all referenced [`ForwardingClasses`](./forwardingclass.md) to a queue, even if it is not used.

### [`Queue`](./queue.md)

The `IngressPolicy` defines the classification of packets, and assigns them to a particular [`Queue`](./queue.md) for further processing, in addition to configuring the [`Queues`](./queue.md) themselves. The [`Queue`](./queue.md) resources referenced by the policy must exist as resources before the `IngressPolicy` can be configured.

## References

The `IngressPolicy` has no references to any EDA resources other than the ones specified in [Dependencies](#dependencies).

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

[^1]: Priority-based Flow Control or **PFC** is a mechanism (IEEE 802.1Qbb) that enables a network element to signal to one of their neighbors to stop sending traffic for a particular priority.