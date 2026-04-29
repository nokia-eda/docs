---
resource_name: Fabric
resource_name_plural: fabrics
resource_name_plural_title: Fabrics
resource_name_acronym: F
crd_path: docs/apps/fabrics.eda.nokia.com/crds/fabrics.eda.nokia.com_fabrics.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Fabric

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `Fabric` is an abstracted representation of a datacenter that is using the Clos architecture. It manages the nodes in their different roles (leafs, spines, borderleafs, ...), the links that interconnect them, and the protocols that facilitate the exchange of routing information. 

Upon deployment, the `Fabric` resource initiates several supporting resources including [`ISLs`](./isl.md) (Inter-Switch Links), [`DefaultRouters`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md), [`DefaultInterfaces`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md), and [`DefaultBGPPeers`](../../../protocols.eda.nokia.com/docs/resources/defaultbgppeer.md), among others. These resources, in turn, generate node configurations. The operational state of the `Fabric` is determined by the collective status of these underlying resources.

## Fabric nodes

The [`Fabric application`](../index.md) home page gives an overview of some common fabric topologies. Within an EDA namespace, multiple fabrics may exist, which can be standalone or [interconnected](#fabric-of-fabrics). Each `Fabric` manages the set of nodes that make up the datacenter network, and creates [`ISL`](./isl.md) resources for all `Links` that interconnect these nodes.

!!! info "LAGs in Fabrics"

    Typically, datacenters don't use LAGs. If there are multiple links between a pair of nodes (whether for redundancy or for increased bandwidth), a BGP or OSPF session is set up for each of them to exchange routes, relying on ECMP rather than link hashing. 
    
    The `Fabric` resource does not enforce this: an [`ISL`](./isl.md) is created for every `Link`, which in turn connects two `Interfaces`. The `Interface` resource references one or more physical ports.

## Labels

Nodes and node roles are identified using labels: this ensures that a `Fabric` can easily grow over time when new racks are added, simply by onboarding new nodes in EDA and assigning them the label that corresponds with their role. If multiple `Fabrics` are used, a secondary label should be added to the nodes that identifies the `Fabric` that the switch belongs to.

!!! note "Label selectors"

    Most `Fabric` resources support multiple labels to be defined. Use a comma (`,`) to indicate that **both** labels need to be present on a node before it is selected. For example, the following label selector indicates that a node must have both the `leaf` role **and** belong to the `London` region:

    ```
    leafNodeSelectors:
        - eda.nokia.com/role = leaf, datacenter=London
    ```

**Initial Labeling:**  If `TopoNodes`, `TopoLinks`, and adjacent `Fabric` instances are labeled before the creation of the `Fabric` instance, the application will automatically generate all necessary configurations for these components during the transaction associated with the addition of the Fabric instance.

**Post-Deployment Labeling:** If new labels that match the `Fabric`'s selection criteria are added to `TopoNodes`, `TopoLinks`, or adjacent `Fabric` instances after the `Fabric` instance has been deployed, these components will automatically be configured by the Fabric application during the transaction that handles the addition of the labels. This ensures that changes in network topology, roles, or Fabric interconnections are dynamically incorporated into the `Fabric`'s configuration.

## `Fabric` nodes

Different network switches fulfill different roles in the network, with different requirements in terms of port speed capabilities, forwarding throughput, and control plane capabilities. The roles that the `Fabric` resource supports are listed below.

### Leaf nodes

Leaf nodes are also referred to as top-of-rack switches, or ToR for short, and facilitate connectivity between computes in the same rack. As the name implies, these are typically installed in every rack, and duplicated for redundancy. They interconnect **physical computes** such as servers and firewalls to the datacenter `Fabric`, which will facilitate inter- and intra-rack connectivity, as well as connectivity to the WAN. 

Each leaf node gets its own system IP address from the [system IP](#allocation-pools) allocation pool, and its own autonomous system (AS) number. 

!!! question "Why one ASN per leaf switch?"

    When the `Fabric` is configured to use eBGP for the exchange of IP addresses in the [underlay](#underlay-protocols), to ensure that these routes are not rejected, each leaf requires its own Autonomous System Number.

### Spine nodes

Spine nodes interconnect [leaf](#leaf-nodes) nodes and are used to establish inter-rack connectivity. For redundancy, there are two or more spines per [pod](#superspine-nodes), and all leaf nodes in the [pod](#superspine-nodes) are connected to all spines. When iBGP is used for the [overlay](#overlay-protocols), the spine nodes are typically used as route reflectors for the EVPN routes.

Each spine node (within a pod) uses the same autonomous system (AS) number.

!!! question "Why one ASN for all spine switches?"

    In typical datacenters, there is no crosslink between the spines. Inter-rack traffic may use either spine, and in case of a link failure the affected spine should stop advertising reachability information for the affected leaf. This way, traffic latency is minimized and tromboning is avoided. 

    As a consequence of spines sharing the same autonomous system number, the spines are not aware of each other, and you won't be able to ping between spines!

### Superspine nodes

Superspines are used in highly scaled datacenters, where it is no longer feasible to connect all leafs to every spine. The `Fabric` is subdivided into pods, where the spines of each pod are connected to every superspine. This trades off higher scale for increased latency (more hops for inter-pod traffic).

### Borderleaf nodes

Borderleaf nodes are very similar in definition to [leaf nodes](#leaf-nodes), but often differ in port capabilities: while the focus for leaf switches is typically on supporting as many different port speeds as possible, the borderleaf is chosen for its high-bandwidth ports and control plane capabilities. It is used to advertise the `Fabric` to the WAN network (via a DCGW[^1] or an internet gateway), enabling connectivity between the `Fabric` and the network elements outside of the datacenter. 

In smaller networks, the role of the spine and the borderleaf is often collapsed: spines already have high-throughput ports to interconnect leaf switches, and if the switch can terminate EVPN services (becoming aware of the IP routes used in virtual networking services), it can establish the (MP-)BGP session to the WAN network. 

In larger networks, higher throughput requirements mean EVPN capabilities are reduced: if the [spine](#spine-nodes) switches are no longer capable of terminating EVPN services, borderleaf nodes are required to connect to the WAN and/or internet. 

## Inter-switch links

Once [nodes](#fabric-nodes) are configured in the `Fabric`, they need to be interconnected using inter-switch links ([`ISLs`](./isl.md)). These [`ISL`](./isl.md) resources configure routing protocols such as `eBGP` and `OSPF` for the exchange of system IP addresses. 

The `linkSelectors` property of the `interSwitchLinks` context of the `Fabric` resource selects all `Link` resources that are used for inter-switch ([underlay](#underlay-protocols)) connectivity. If both ends of the `Link` correspond with a node of the `Fabric`, an [`ISL`](./isl.md) is created for that `Link`.

!!! warning "Don't forget this property!"

    If the `linkSelector` property is omitted, or does not select the right `Links`, there will be no connectivity between the nodes of your `Fabric`! 

## Allocation pools

Several allocation pools are required to distribute IP addresses to the resources that the `Fabric` creates:

- System IP addresses for the [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md) resource on each node in the `Fabric`, drawn from an `IPAllocationPool`
- Point-to-point IP subnets for the [`ISL`](#inter-switch-links), drawn from a `SubnetAllocationPool`
- Autonomous System Numbers (ASNs) for the [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md) resource on each node in the `Fabric`, drawn from an `IndexAllocationPool`

System IP address pools can be configured globally and/or per role. The system IP address pool configured under the [node role](#fabric-nodes) context overrides the globally configured pools.

!!! warning

    An IPv4 pool is mandatory: it must always be configured, even if the routes are exchanged exclusively through IPv6

Autonomous system pools can be specified under the [underlay](#underlay-protocols) protocol and/or per role. The autonomous system pool configured under the [node role](#fabric-nodes) context overrides the one specified in the [underlay](#underlay-protocols) section.

## Underlay protocols

The **underlay** of a datacenter refers to the exchange of reachability information that enables the [overlay](../../../routing.eda.nokia.com/docs/index.md#overlay-routing) routes to be exchanged. The `Fabric` resource uses the **underlay** protocol for the exchange of system IP addresses, which will be used to establish the MP-BGP session for the exchange of EVPN routes. Currently the following protocols are supported for the exchange of system IP addresses:

- eBGP (iBGP not supported)
- OSPFv2
- OSPFv3

!!! question "Is exchange of EVPN routes via the underlay supported?"

    Yes, exchange of EVPN routes is supported over eBGP. Note however that exchanging EVPN routes via OSPF is not possible. There are scale considerations that favor the separation of underlay and overlay (using iBGP), however these discussions are beyond the scope of this article.

!!! warning "MTU considerations for OSPF interoperability"

    Different network operating systems have different default port MTUs. OSPF is notoriously specific when it comes to MTU, and will not establish a session if the signaled MTU is mismatched. 
    
    If the MTU is not set using the [`DefaultMTU`](../../../siteinfo.eda.nokia.com/docs/resources/defaultmtu.md) resource, it is important to set the `ipMTU` property of the `interSwitchLinks` container in the `Fabric` resource. An MTU value of `8922` works for most interop scenarios.

## Overlay protocols

The **overlay** of a datacenter refers to the exchange of **service routes**. In a datacenter context, EVPN is most commonly used as a way of ensuring traffic isolation between (virtual) distributed networks belonging to different tenants. The inner workings of EVPN are beyond the scope of this article. 

Both eBGP and iBGP are supported: in case eBGP is used, service routes are exchanged between the IP addresses of the individual links between the nodes. If iBGP is used, service routes are exchanged between the system IP addresses of the nodes. 

!!! question "Which protocol to choose?"

    eBGP is easiest to set up, but there are scale implications that should be investigated before choosing this route, which are beyond the scope of this article. 
    
From a technical point of view, iBGP requires the addition of route reflectors. These are typically configured on the [spines](#spine-nodes) or [superspines](#superspine-nodes), but can also exist outside of the datacenter. The following elements are required when using iBGP for the exchange of service routes:

- Specify the autonomous system number that all switches will use to communicate with the route reflectors.
- If the route reflectors are configured on nodes in the `Fabric`, the `rrNodeSelectors` and `clusterId` properties are required.
- If the route reflectors are **not** configured on nodes in the `Fabric`, their IP addresses must be listed in the `rrIpAddresses` property.
- Select the nodes that will peer with the route reflectors by populating the `rrClientNodeSelectors` label selector.

!!! warning "Don't forget!"

    When using iBGP, don't forget to select route reflector clients using the `rrClientNodeSelectors` label selector! Without it, no overlay BGP sessions will be established.

## Routing Policies

If not explicitly specified, the Fabric will **automatically generate** the required [Policy](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md) resources. These policies are used in the BGP peering sessions to ensure IP reachability across the fabric. 

If [`routing policies`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md) are defined independently of the `Fabric` through the `importPolicies` or `exportPolicies` properties, they will be used instead.

## Route leaking

Route leaking is used to establish connectivity between the [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md) and virtual networking services. For example, it may be done on the [borderleaf nodes](#borderleaf-nodes) to expose an isolated in-band management network to the WAN.

Route leaking relies on [`routing policies`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md) and can be specified globally in the `Fabric` resource or overridden under each [node role](#fabric-nodes) container.

## Fabric of Fabrics

To establish connectivity between multiple datacenters, several options may be considered. Each has its own use case:

- Connect each `Fabric` to DCGW[^1] routers using (MP-)BGP
- Interconnect each fabric using [superspines](#superspine-nodes)
- Create a "`Fabric` of fabrics" resource

A fabric of fabrics is a separate `Fabric` resource that interconnects other `Fabric` resources. It is configured and works largely the same as a regular `Fabric` resource, with the addition of the `fabricSelectors` property, which is a label selector that identifies the `Fabrics` that this resource will interconnect. [`ISL`](./isl.md) resources will be created for each `Link` that is connected to:

- A node in the fabric of fabrics
- A node in a `Fabric` selected by the `fabricSelectors` label selector

!!! warning "A note on inter-fabric Links"

    The `Link` resources that the `linkSelectors` property selects must be configured with the `remote` side pointing to the child `Fabrics`.

## Dependencies

### `IPAllocationPool`

IP allocation pools are resource pools that hand out single IP addresses from a pool. The `Fabric` resource uses them to provision system IP addresses for the nodes in the `Fabric`.

### `SubnetAllocationPool`

Subnet allocation pools are resource pools that hand out IP subnets with a specific length from a pool. The `Fabric` resource uses them to provision point-to-point IP addresses for derived [`ISL`](./isl.md) resources.

### `IndexAllocationPool`

Index allocation pools are resource pools that hand out indices (whole numbers) from a pool. The `Fabric` resource uses them to assign autonomous system (AS) numbers to the nodes in the `Fabric`.

## Referenced resources

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

Routing policies determine which IP prefixes are advertised to neighbors. In the `Fabric` resource, they can optionally be specified:

- In the [underlay protocol](#underlay-protocols) if BGP is selected
- In the [route leaking](#route-leaking) context

### [`IngressPolicy`](../../../qos.eda.nokia.com/docs/resources/ingresspolicy.md)

Quality of Service policies can optionally be specified in the `interSwitchLinks` container of the `Fabric` resource. An [`IngressPolicy`](../../../qos.eda.nokia.com/docs/resources/ingresspolicy.md) is used to assign priorities to incoming traffic, and optionally to rate-limit traffic with a particular priority.

### [`EgressPolicy`](../../../qos.eda.nokia.com/docs/resources/egresspolicy.md)

Quality of Service policies can optionally be specified in the `interSwitchLinks` container of the `Fabric` resource. An [`EgressPolicy`](../../../qos.eda.nokia.com/docs/resources/egresspolicy.md) is used to assign packets to [`Queues`](../../../qos.eda.nokia.com/docs/resources/queue.md) depending on their priority and to modify the priority bits in the headers of outgoing traffic.

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

[^1]: Datacenter Gateways or DCGWs are a generic name for routers that interconnect datacenters with each other and the WAN network