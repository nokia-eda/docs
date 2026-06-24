# Micro Segmentation Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Supported HW**     | **Nokia 7220 IXR-D2/D3**  |
| **Catalog**          | [Nokia/catalog/microsegmentation ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

!!! info "Micro segmentation is introduced as BETA in EDA 26.4.1"


!!! info "Micro segmentation is currently only available on select hardware platforms"
    Micro segmenation leverages the Group Based Policy functionality which was introduced in SRL 26.3.1

    It is only supported on IXR 7220-D2/D3 platforms and on IXR 7220-D4 (for L2 only).



Micro segmentation is a network security capability intended to prevent lateral movement of security threats. It divides networks into smaller, isolated zones (known as micro segments) and establishes rules to restrict traffic between them. An example of a micro segment defined within an enterprise network is a set of homogeneous devices such as DNS servers, printers, client applications, or server applications.

The use of micro segmentation policies offers various benefits over traditional ACLs or IP filters:

* Abstraction of micro segments independent of networking concepts (IP addressing, VLANs etc).
* Flexible network designs and IP addressing schemes.
* Update the micro segment a host belongs to, without changing the security policy.

To start using micro segmentation policies:

1. create [`GroupTags`](./resources/grouptag.md) to define the micro segments
2. create a [`GroupTagAssociationPolicy`](./resources/associationpolicy.md) to associate the group tags with interfaces or routes. 
3. create a [`MicroSegmentationPolicy`](./resources/microsegmentationpolicy.md) referencing the group tags as source and/or destination


The application provides the following components:

/// tab | Resource Types

<div class="grid" markdown>
<div markdown>

* [`GroupTags`](./resources/grouptag.md)
* [`GroupTagAssociationPolicies`](./resources/associationpolicy.md)
* [`MicroSegmentationPolicies`](./resources/microsegmentationpolicy.md)


</div>
</div>
///
/// tab | Dashboards

<div class="grid" markdown>
<div markdown>
Summary dashboards for the following resource types:

* Group Tags
* Microsegmentation Policies - Policy Entry Coutners
* Microsegmenation Policies - Node Platform Status

</div>
</div>
///
/// tab | Bootstrap Resources

<div class="grid" markdown>
<div markdown>
The app installs the following resources:

* `IndexAllocationPool`: [group-tag-pool-global](./resources/grouptag.md#scopes)
* `IndexAllocationPool`: [group-tag-pool-local](./resources/grouptag.md#scopes)

</div>
</div>
///
