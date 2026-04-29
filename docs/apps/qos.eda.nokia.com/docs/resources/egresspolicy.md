---
resource_name: EgressPolicy
resource_name_plural: egresspolicys
resource_name_plural_title: Egress Policies
resource_name_acronym: EP
crd_path: docs/apps/qos.eda.nokia.com/crds/qos.eda.nokia.com_egresspolicys.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Egress Policy

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

??? abstract "A brief introduction to QoS"

    Quality of Service (QoS) is a set of technologies and mechanisms used to manage traffic prioritization, often but not exclusively used in scenarios of network congestion. A full explanation of QoS is beyond the scope of this documentation, as the concepts are often as complex as the implementation of them on various network operating systems, along with chip-specific capabilities and limitations.

An `EgressPolicy` applies to packets that are egressing through a physical interface, and converts the internal [`ForwardingClass`](./forwardingclass.md) tag attached to the packet to the priority bits in the packet headers so packet prioritization is maintained end-to-end.

## Forwarding class mapping

The `EgressPolicy` allows you to override the default mapping between a [`ForwardingClass`](./forwardingclass.md) and a [`Queue`](./queue.md). By separating traffic based on priority classes, proper packet prioritization is ensured in case of congestion. 

## Queue management and slope policies

Every queue has a certain maximum size and associated parameters like Committed Burst Size (CBS), Maximum Burst Size (MBS) and PFC priorities. In addition, the scheduler - the mechanism that dequeues packets and sends them out of the egress interface - takes the priority levels and weights of the queue into account.

By default packets are dropped if there is no more room in the queue. This is fine if all packets in the queue are equally important, but colored packets (see [`IngressPolicy`](./ingresspolicy.md#classification)) may still be dropped regardless of their priority. To mitigate that, **slope policies** can be configured per drop probability.

**Slope policies** are evaluated for every packet with a particular drop probability that enters the [`Queue`](./queue.md). Based on the occupancy of the [`Queue`](./queue.md), one of three actions is taken:

- If the occupancy of the queue is below the minimum threshold, the packet is allowed in the queue.
- If the occupancy of the queue is above the maximum threshold, the packet is dropped.
- If the occupancy of the queue is above the minimum, but below the maximum threshold, the packet has a chance to be dropped that increases as the queue becomes more occupied.

??? example "Quick maths"

    The effective drop probability is calculated in accordance with the following formula:

    ```
    ((maxThreshold - minThreshold) / queueOccupancy) * (maxProbability - 0%)
    ```

## Rewrite policies

**Rewrite policies** do the opposite of a [classifier](./ingresspolicy.md#classification): instead of reading the priority bits from the packet headers and assigning an internal [`ForwardingClass`](./forwardingclass.md) to the packet, **rewrite policies** transform the [`ForwardingClass`](./forwardingclass.md) into priority bits that are written to the packet headers.

By using [classifiers](./ingresspolicy.md#classification) and **rewrite policies**, traffic can be classified when it ingresses the network, and this priority is maintained while the packet traverses the network.

## Deadlock avoidance

A PFC[^1] deadlock may occur in specific scenarios: router `A` is sending PFC frames to router `B`, which in turn sends PFC frames downstream. If that PFC frame ever reached router `A` again, a loop is established where all routers will wait on each other.

The deadlock detection timer and recovery timer may be used to recover from this state.

## Dependencies

### [`ForwardingClass`](./forwardingclass.md)

Most QoS mechanisms either assign a [`ForwardingClass`](./forwardingclass.md) to a packet, or take an action based on the assigned [`ForwardingClass`](./forwardingclass.md). These must exist as a resource if the `EgressPolicy` refers to them.

### [`Queue`](./queue.md)

The `EgressPolicy` decides which [`Queue`](./queue.md) the packet is put in, based on the [`ForwardingClass`](./forwardingclass.md) of that packet, in addition to configuring the [`Queues`](./queue.md) themselves. The [`Queue`](./queue.md) resources referenced by the policy must exist as resources before the `EgressPolicy` can be configured.

## Referenced resources

The `EgressPolicy` has no references to any EDA resources other than the ones specified in [Dependencies](#dependencies).

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