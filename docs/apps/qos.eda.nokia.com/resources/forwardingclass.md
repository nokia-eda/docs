---
resource_name: ForwardingClass
resource_name_plural: forwardingclasss
resource_name_plural_title: Forwarding Classes
resource_name_acronym: FC
crd_path: docs/apps/qos.eda.nokia.com/crds/qos.eda.nokia.com_forwardingclasss.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Forwarding Class

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

??? abstract "A brief introduction to QoS"

    Quality of Service (QoS) is a set of technologies and mechanisms used to manage traffic prioritization, often but not exclusively used in scenarios of network congestion. A full explanation of QoS is beyond the scope of this documentation, as the concepts are often as complex as the implementation of them on various network operating systems, along with chip-specific capabilities and limitations.

To prioritize one traffic stream over another, the router must assign a priority to each packet as it ingresses on an interface. Several options are available:

- Based on the IP header: source IP, destination IP, source port, destination port, ...
- Based on the Dot1p priority bits of the ethernet frame
- Based on the DSCP priority bits of an IP header

These are called **classifiers**: based on the classifier criteria, the router attaches an internal 'tag' to the packet that determines how the packet is treated while it propagates through the box. This 'tag' is called a **forwarding class**.

!!! note "Forwarding classes"

    Forwarding classes are only locally significant, meaning they are not added to the packet headers. Ingressing traffic is classified based on the `classifiers` in an [`IngressPolicy`](./ingresspolicy.md). 
    
    To influence the packet's priority at the next hop, a rewrite policy must be defined in an [`EgressPolicy`](./egresspolicy.md), which translates the internal forwarding class to the priority bits of the IP / MAC header of the egressing packet.

The creation of a `ForwardingClass` resource does not result in configuration being pushed to the nodes. It is configured on the nodes by creating a [`PolicyAttachment`](./policyattachment.md) or [`PolicyDeployment`](./policydeployment.md) that specifies an [`IngressPolicy`](./ingresspolicy.md) or [`EgressPolicy`](./egresspolicy.md) that references the `ForwardingClass`.

!!! warning "Forwarding class naming conventions"

    The naming convention of a forwarding class matters. See section "OS-specific implementation notes" for more information.

## OS-specific implementation notes

EDA comes pre-packaged with a number of `ForwardingClass` resources. Not all resources can be deployed on every operating system, though.

### Nokia SR Linux

The name of a forwarding class can be chosen freely, although there are reserved names (`fc0`, `fc1`, ... ) already provisioned in EDA. By default, these are linked to their respective (`unicast-0`, `unicast-1`, ...) [`Queues`](./queue.md), which can be overwritten. For more information, refer to the SR Linux documentation.

### Nokia SR OS

The following forwarding classes are supported on SR OS:

```
be - Best effort
l2 - Low 2 (best effort)
af - Assured forwarding (assured)
l1 - Low 1 (assured)
h2 - High 2 (high priority)
ef - Expedited forwarding (high priority)
h1 - High 1 (high priority)
nc - Network control (high priority)
```

## Dependencies

The `ForwardingClass` resource has no dependencies on other EDA resources.

## Referenced resources

The `ForwardingClass` resource does not reference any other EDA resources.

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
