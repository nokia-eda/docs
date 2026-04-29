# Fabrics Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/fabrics ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

The Fabric application streamlines the construction and deployment of data center fabrics, suitable for environments ranging from small, single-node edge configurations to large, complex multi-tier and multi-pod networks. It automates crucial network configurations such as IP address assignments, VLAN setups, and both underlay and overlay network protocols.

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [Fabric](resources/fabric.md)
* [ISL](resources/isl.md)

</div>
</div>
///

/// tab | Workflows
<div class="grid" markdown>
<div markdown>

* [ISLPing](resources/islping.md)
* [FabricTopology](resources/fabrictopology.md)

</div>
</div>
///

## Fabric topologies

The Fabric application supports highly flexible deployment models, enabling you to tailor the configuration of your data center fabric to suit different architectural needs. You can deploy a single instance of a [`Fabric`](./resources/fabric.md) resource to manage the entire data center, incorporating all network nodes, or you can opt to divide your data center into multiple, smaller [`Fabric`](./resources/fabric.md) instances.


!!! example "Deployment model example"

    For example, you might deploy one Fabric instance to manage the superspine and borderleaf layers while deploying separate Fabric instances for each pod within the data center. This modular approach allows for more granular control. This can be taken to the extreme where each layer of a data center fabric could be its own instance of a Fabric. The choice is yours!

A [`Fabric`](resources/fabric.md) is a collection of network nodes that are interconnected using Inter-Switch Links or [`ISLs`](resources/isl.md). Inter-Switch links are point-to-point links, where each endpoint is a node in the fabric. Edge links that have only one endpoint attached to the [`Fabric`](./resources/fabric.md) are modeled through the `Link` resource.

Clos fabrics are designed to scale with deployment size, ranging from very small to very large networks.

### 2-tier clos Fabric

This topology focuses on small to medium deployments with a couple of racks, where leaf[^1] switches are interconnected through spines[^2]. Leaf switches are often chosen for their port capabilities in terms of speed and connector types, while spine switches are optimized for forwarding capacity.

Typically, computes are attached to [Bridge Domains](../../services.eda.nokia.com/docs/resources/bridgedomain.md) or [Routers](../../services.eda.nokia.com/docs/resources/router.md). To facilitate external connectivity to and from these computes, the reachability information for the IP subnets that are available within the fabric is exchanged with Datacenter Gateway[^3] (DCGW) routers, using one of two methods:

- PE-CE connection type A: exchange **IP-only** routes using a routing protocol like OSPF or BGP
    - Requires strict separation of IP subnets between datacenter fabrics
- PE-CE connection type B: exchange **service** routes using Multi-Protocol BGP
    - Allows for stretched layer 2 services between fabrics

The requirements of your network determine which type should be used.

![Tier 2 Fabric](media/diagrams-Tier2.png)

### 3-tier clos Fabric

The difference between a 2- and a 3-tier fabric is the addition of **borderleafs**. The borderleaf is required in the case where the spines don't support service termination. In this scenario, the spines only support IP routing for the VXLAN transport tunnels, and are not aware of the services that run on the fabric. This is a common occurrence in fabrics with >32 leafs (16 racks). Spines don't scale very well horizontally, since every leaf is supposed to be attached to every spine to limit the number of hops between any two computes.

The borderleafs are functionally the same as leafs, but often differ in port speeds: leafs may have 10 Gbps downlinks towards compute servers, whereas borderleafs provide 100 Gbps connectivity to firewalls, DCGWs[^3], internet gateways, ...

![Tier 3 Fabric](media/diagrams-Tier3.png)

### Clos fabric with superspines

Superspines are introduced in the case where it is no longer feasible to vertically scale the spine nodes, which is typical once the number of leafs exceeds 128 (64 racks). In these hyper-scaled scenarios, an additional hierarchical layer is required.

![Superspine fabric](media/diagrams-TierSuperSpine.png)

This scaling level means there are at most 6 hops in between any two computes instead of 4.

![Superspine hops](media/diagrams-SS-hops.png)

[^1]: Leaf switches connect directly to computes in the rack, and are often called top-of-rack switches. Commonly deployed in pairs for redundancy.
[^2]: Spine switches interconnect leaf switches, and often take on the role of route reflectors for the EVPN routes of the entire fabric. Commonly deployed in pairs for redundancy
[^3]: Datacenter Gateways or DCGWs are a generic name for routers that interconnect datacenters with each other and the WAN network