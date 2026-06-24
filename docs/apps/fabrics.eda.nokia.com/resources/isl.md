---
resource_name: ISL
resource_name_plural: isls
resource_name_plural_title: ISLs
resource_name_acronym: I
crd_path: docs/apps/fabrics.eda.nokia.com/crds/fabrics.eda.nokia.com_isls.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# ISL

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

An inter-switch link, or ISL, is a logical representation of one or more physical links interconnecting two network nodes. ISLs are usually created as derived resources by a [`Fabric`](./fabric.md), as a way to model the physical connectivity of network switches that are part of that [`Fabric`](./fabric.md). 

!!! info "Inter-switch links vs edge links"

    Inter-switch links always connect to network switches, and are never connected to client equipment such as servers. Use `Links` to model a physical connection from an edge interface to a compute.

In addition to modeling physical connectivity between switches, the `ISL` resource is responsible for the configuration of [underlay](../../../routing.eda.nokia.com/docs/index.md#underlay-routing) protocols like [BGP](../../../protocols.eda.nokia.com/docs/resources/defaultbgppeer.md) and [OSPF](../../../protocols.eda.nokia.com/docs/resources/defaultospfinterface.md) for the exchange of [underlay routes](../../../routing.eda.nokia.com/docs/index.md#underlay-routing).

## BFD

BFD parameters can be configured on an `ISL`, which are passed down to the derived [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) that the `ISL` creates. The configured BFD session will monitor the neighboring interface, improving the fault detection time significantly if there is layer-2-only equipment in between the two switches.

??? question "Not seeing BFD sessions being established?"

    BFD requires a protocol to subscribe before a BFD session is created. This could be either a static route, a BGP peer, or OSPF neighbor. For example, a [`DefaultBGPPeer`](../../../protocols.eda.nokia.com/docs/resources/defaultbgppeer.md) with BFD enabled will only establish a session with its peer if the underlying [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) (which is created as a derived resource by the `ISL` resource) has BFD enabled as well, and vice versa.

## Dependencies

### [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md)

`ISL` resources provide [underlay](../../../routing.eda.nokia.com/docs/index.md) connectivity in the [default VRF](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md). Therefore, it is required that [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md) resources are created on each switch that the `ISL` interconnects.

### [`Interface`](../../../interfaces.eda.nokia.com/docs/resources/interface.md)

Both endpoints of an `ISL` are [`Interface`](../../../interfaces.eda.nokia.com/docs/resources/interface.md) resources, which represent a (set of) physical port(s). For each endpoint, the `ISL` will use the [`DefaultRouter`](../../../routing.eda.nokia.com/docs/resources/defaultrouter.md) resource and the [`Interface`](../../../interfaces.eda.nokia.com/docs/resources/interface.md) resource to create a derived [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) resource.

Once the ISL is created, the derived [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) are referenced in the state of the ISL.

!!! info "LAGs vs individual links"

    In a datacenter architecture, it is common practice to avoid LAGs (Link Aggregation Groups) and instead create individual links - each with their own BGP or OSPF session - even if they interconnect the same switches. In some scenarios, this enables more powerful load-balancing behavior compared to bundling physical links.

### `SubnetAllocationPool`

IP addresses are required if the switches are not using IPv6 unnumbered addresses to communicate. These inter-switch IP addresses are taken from a `SubnetAllocationPool`. This allocation pool specifies a bigger subnet (e.g. `172.16.0.0/12`) that can be subdivided into smaller subnets. For the `ISL` resource, the `SubnetAllocationPool` must contain a segment that hands out subnets of size `/31`.

## Referenced resources

### [`IngressPolicy`](../../../qos.eda.nokia.com/docs/resources/ingresspolicy.md)

Quality of Services (QoS) mechanisms can be configured on the `ISL`, ensuring that traffic is properly classified and prioritized. If an [`IngressPolicy`](../../../qos.eda.nokia.com/docs/resources/ingresspolicy.md) is used, these policies must be created before they can be attached to an `ISL`.

!!! warning "Read the QoS documentation"

    The [QoS application documentation](../../../qos.eda.nokia.com/docs/index.md) contains important information about QoS and what is supported by EDA. Specifically, QoS on an inter-switch link is typically referred to as Network QoS, which has different capabilities compared to Access QoS on most hardware platforms.

### [`EgressPolicy`](../../../qos.eda.nokia.com/docs/resources/egresspolicy.md)

Quality of Services (QoS) mechanisms can be configured on the `ISL`, ensuring that traffic is properly prioritized. If an [`EgressPolicy`](../../../qos.eda.nokia.com/docs/resources/egresspolicy.md) is used, these policies must be created before they can be attached to an `ISL`.

### [`DefaultBGPGroup`](../../../protocols.eda.nokia.com/docs/resources/defaultbgpgroup.md)

If BGP is enabled on an `ISL`, the resource will automatically create derived [`DefaultBGPPeer`](../../../protocols.eda.nokia.com/docs/resources/defaultbgppeer.md) resources: one for each endpoint. These peers will exchange (MP-)BGP routes to advertise reachability information throughout the network. In EDA, [`DefaultBGPPeers`](../../../protocols.eda.nokia.com/docs/resources/defaultbgppeer.md) always belong to a [`DefaultBGPGroup`](../../../protocols.eda.nokia.com/docs/resources/defaultbgpgroup.md), which configures common parameters that are re-used across multiple BGP sessions.

Certain BGP session parameters, such as `importPolicies` and `exportPolicies` can be overridden in the `ISL` resource: if they are not specified, the policies of the [`DefaultBGPGroup`](../../../protocols.eda.nokia.com/docs/resources/defaultbgpgroup.md) are used instead. 

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

Routing policies determine which reachability information is advertised to [BGP](../../../protocols.eda.nokia.com/docs/resources/defaultbgppeer.md) and [OSPF](../../../protocols.eda.nokia.com/docs/resources/defaultospfinterface.md) neighbors. In typical datacenter [fabrics](./fabric.md), the `/31` point-to-point subnets are not advertised to peers: the [underlay](../../../routing.eda.nokia.com/docs/index.md) BGP / OSPF sessions are only used for the exchange of system IP addresses. To accomplish this, [routing policies](../../../routingpolicies.eda.nokia.com/docs/index.md) are required. 

### [`DefaultOSPFInstance`](../../../protocols.eda.nokia.com/docs/resources/defaultospfinstance.md)

An OSPF instance is the top-most container in an OSPF hierarchy, and specifies which address families are being exchanged.

!!! info "OSPF hierarchy concepts"
    If OSPF is enabled, a [`DefaultOSPFInterface`](../../../protocols.eda.nokia.com/docs/resources/defaultospfinterface.md) will be created for each derived [`DefaultInterface`](../../../routing.eda.nokia.com/docs/resources/defaultinterface.md) resource, which is then assigned to a [`DefaultOSPFArea`](../../../protocols.eda.nokia.com/docs/resources/defaultospfarea.md) that in turn belongs to a [`DefaultOSPFInstance`](../../../protocols.eda.nokia.com/docs/resources/defaultospfinstance.md).

    Both resources must be created when configuring an `ISL` that uses OSPF to exchange reachability information.

### [`DefaultOSPFArea`](../../../protocols.eda.nokia.com/docs/resources/defaultospfarea.md)

An OSPF area is a logical grouping of routers that share the same area ID, configured within an OSPF instance.

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
