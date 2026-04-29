---
resource_name: MicroSegmentationPolicy
resource_name_plural: microsegmentationpolicies
resource_name_plural_title: Micro Segmentation Policies
resource_name_acronym: MS
crd_path: docs/apps/microsegmentation.eda.nokia.com/crds/microsegmentation.eda.nokia.com_microsegmentationpolicies.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Micro Segmentation Policies

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural ) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `MicroSegmentationPolicy` is a granular security policy designed to enforce Zero Trust principles within a network. Unlike traditional perimeter-based security that focuses on protecting the border of a network, microsegmentation divides the internal network into distinct, isolated security segments. This allows for precise control over "east-west" traffic (communication between internal resources), significantly reducing the attack surface and preventing lateral movement by unauthorized users or threats.

* Network-Wide Scope: Instead of being applied to individual ports or interfaces one by one, the policy is defined at the network instance level and can be reused across multiple services.

* Inheritance: Once configured, the policy is automatically inherited by all relevant connection points within that network segment, ensuring there are no "blind spots" in security coverage.

* Network Design Agnostic: Because the policy references `GroupTags` rather than specific VLANs or IP addresses, the policy is updated automatically when group memberships or network configuration changes. 


A `MicroSegmentationPolicy` is an ordered list of `policyEntries` that match certain packets and perform an action for those packets, and that are applied to one or more `serviceTargets` 

## Policy Entries

The `policyEntries` are defined in an ordered list.
Each packet is evaluated on ingress against all `policyEntries` in order. If there is no match, the packet is evaluated against the next entry and so on. Once a packet matches a particular entry, evaluation of the chain ends and the action specified in the entry is performed on the packet. This behavior is identical to [`Filters`](../../../filters.eda.nokia.com/docs/resources/filter.md)

### Match Criteria
Packets can be matched by their

* Source [`GroupTag`](../resources/grouptag.md) 
* Destination [`GroupTag`](../resources/grouptag.md) 
* Source port
* Destination port
* Protocol 
* IP version 

### Actions
When a packet matches the `matchCriteria` of a `policyEntry`, the following `actions` can be applied to the packet

* Forwarding - Accept or Drop 
* Logging - Logs the packets to the nodes logging facility
* Collect statistics - See the "Policy Entry Counters" UI dashboard under "Micro Segmentation Policies"

## Service Targets
The `MicroSegmentationPolicy` can be applied to one or more services by setting `serviceTargets`. The following type are supported:

* [`VirtualNetworks`](../../../services.eda.nokia.com/docs/resources/virtualnetwork.md)
* [`BridgeDomains`](../../../services.eda.nokia.com/docs/resources/bridgedomain.md)
* [`Routers`](../../../services.eda.nokia.com/docs/resources/router.md)

!!! info "MicroSegmentationPolicies can not be applied in the underlay"
    `MicroSegmentatioPolicies` are not supported in [`DefaultRouters`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md).

## OS-specific implementation notes

!!! warning "Node reboot required"
    If an SR Linux device is deployed in a role that requires the source tag to be derived from the lookup of the source IP address in the Longest Prefix Match (LPM) table, the device will automatically be configured to operate in LPM source lookup mode ("platform.resource-management.group-based-policy.lpm-source-lookup"). Changing this setting requires a chassis reboot. See the "Node Platform Status" UI dashboard under "Micro Segmentation Policies".

## Dependencies

A `MicroSegmentationPolicy` must be applied to one or more `serviceTargets` of the following types:

* [`VirtualNetworks`](../../../services.eda.nokia.com/docs/resources/virtualnetwork.md)
* [`BridgeDomains`](../../../services.eda.nokia.com/docs/resources/bridgedomain.md)
* [`Routers`](../../../services.eda.nokia.com/docs/resources/router.md)


These resources should be created first, before creating the `MicroSegmentationPolicy`.

## Referenced resources

### Group Tags
A `MicroSegmentationPolicy` typically refers to [`GroupTags`](../resources/grouptag.md) as source or destination `matchCriteria` in the `policyEntries`.

These resources should be created first, before creating the `MicroSegmentationPolicy`.

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
