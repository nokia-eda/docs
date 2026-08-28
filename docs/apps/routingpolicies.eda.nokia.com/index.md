# Routing Policies Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/routingpolicies ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

[Routing policies](./resources/policy.md) are ordered lists of rules (known as policy statements) that filter and/or modify routes, and can be applied in two directions:

- An import [Policy](./resources/policy.md) to accept, reject, or modify routes received from a BGP, IS-IS, or OSPF neighbor.
- An export [Policy](./resources/policy.md) to send, block, or modify routes advertised to a BGP, IS-IS, or OSPF neighbor.

In addition, [Policies](./resources/policy.md) can be used to control which routes are [leaked](#route-leaking) across virtual network instances.

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`ASPathSet`](./resources/aspathset.md)
* [`CommunitySet`](./resources/communityset.md)
* [`Policy`](./resources/policy.md)
* [`PrefixSet`](./resources/prefixset.md)
* [`TagSet`](./resources/tagset.md)

</div>
</div>
///

## Policy statements

Every statement, which is one rule of a [Policy](./resources/policy.md), has two components: match criteria to determine which routes the rule applies to, and an action determining what to do with routes that match the rule. The following resources are used in the match criteria and/or action of a policy statement:

- [PrefixSets](./resources/prefixset.md) are used exclusively in match criteria, and allow matching based on the subnet of a route.
- [ASPathSets](./resources/aspathset.md) are used exclusively in match criteria, and allow matching based on the AS path of a BGP route.
- [CommunitySets](./resources/communityset.md) are used in match criteria to allow matching based on the (extended) communities of a BGP route, as well as in actions to add, remove, or replace the route's (extended) communities.
- [TagSets](./resources/tagset.md) are used in match criteria to allow matching based on the internal tag assigned to a route, as well as in actions to set a route's internal tag.

/// details | The difference between tags and communities
    type: note

Communities are BGP path attributes that can be propagated to peers, subject to policy. In contrast, internal route tags are locally significant metadata attached to routes and are not sent on the wire.

/// details | Examples of BGP communities
    type: example

- `65500:100` - BGP standard (32-bit) community whose semantics are defined by the operator of AS 65500
- `target:65510:100` - BGP Route Target extended community using AS 65510 and locally assigned value 100
- `origin:65500:1` - BGP Route Origin extended community using AS 65500 and locally assigned value 1

Well-known communities and extended-community types have standardized meanings. Operators define the semantics of other administratively assigned values.

///

Route tags are vendor-specific and locally significant to the device. While they are not transmitted to neighbors or peers, they can influence which routes are advertised to other peers. For example, an operator may assign a temporary isolation tag to all routes received from one or more BGP peers, and then prevent routes with this tag from being advertised to an external peer.

/// details | Examples of route tags
    type: example

- 20 - assigned to routes that **are** to be advertised to an external internet gateway
- 30 - assigned to routes that **are not** to be advertised to an external internet gateway
- 99 - routes that are not (yet) classified as internal or external

Note that there are no hard rules for the numbering of route tags.

///

///

## Route leaking

Virtualized networking services are used to isolate traffic, ensuring that there is no connectivity between isolated sets of hosts. For example, virtual [Routers](-{{ ref_app_doc('services', 'router') }}-) may be used to separate a lab network and a production network. 

Sometimes, however, exceptions must be made. For example, system administrators may require connectivity to the servers in both the lab and production networks. In this example, routes to the system administrators' VPN subnet must be leaked into both the lab and production routers. In the opposite direction, routes to the compute hosts' management subnets must be leaked into the management network.

[Routing policies](./resources/policy.md) may be used to control which routes are leaked into and out of virtualized [Router](-{{ ref_app_doc('services', 'router') }}-) services.
