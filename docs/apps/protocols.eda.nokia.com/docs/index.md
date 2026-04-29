# Protocols Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**     | -{{app_group}}-/-{{app_api_version}}-   |
| **Supported OS**     | -{{supported_os_versions(app_group)}}-  |
| **Catalog**          | [nokia-eda/catalog/protocols][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[manifest]: https://github.com/nokia-eda/catalog/blob/main/vendors/nokia/apps/protocols/manifest.yaml

To facilitate distributed [routing and switching services](../../services.eda.nokia.com/docs/index.md), network elements need to exchange forwarding and routing information. The Protocols application enables users to create and manage various routing protocols and contains resources that are split between the [Overlay Routing](../../routing.eda.nokia.com/docs/index.md#overlay-routing) and [Default Routing](../../routing.eda.nokia.com/docs/index.md#underlay-routing) categories.

Resources from the Default Routing category will have the _Default_ prefix in their name[^1] and are used in the network element's default VRF[^2], also known as Global Routing Table (GRT).  

On the other hand, the resources listed under the Overlay Routing category[^3] are designed to be associated with a custom, non-default VRF.

The application provides the following components:

/// tab | Resource Types

<div class="grid" markdown>
<div markdown>
-{{icons.default_routing()}}-

* [Default BGP Groups](./resources/defaultbgpgroup.md)
* [Default BGP Peers](./resources/defaultbgppeer.md)
* [Default Static Routes](./resources/defaultstaticroute.md)
* [Default Aggregate Routes](./resources/defaultaggregateroute.md)
* [Default Route Reflectors](./resources/defaultroutereflector.md)
* [Default Route Reflector Clients](./resources/defaultroutereflectorclient.md)

</div>
<div markdown>
-{{icons.overlay_routing()}}-

* [BGP Groups](./resources/bgpgroup.md)
* [BGP Peers](./resources/bgppeer.md)
* [Static Routes](./resources/staticroute.md)
* [Aggregate Routes](./resources/aggregateroute.md)
* [Route Reflectors](./resources/routereflector.md)
* [Route Reflector Clients](./resources/routereflectorclient.md)

</div>
</div>
///

/// tab | Dashboards
Summary dashboards for the following resource types:

* Default BGP Peers
* Default BGP Groups
* Default Route Reflectors
* Default Route Reflector Clients
///

Several routing protocols are available, both for usage in the Default VRF (Global Routing Table) and the Overlay VRF:

* Static routing
* Border Gateway Protocol (BGP)
* Open Shortest Path First (OSPF)

## Static Routing

For populating the routing table without a dynamic routing protocol, users can make use of the Static Routes resources, which are available in both the Default and Overlay routing variations.

If it is required to combine multiple routes (from a contiguous subnet) into one single route to advertise to the other elements in the network, use an [Aggregate Route](resources/aggregateroute.md) resource. An example could be an internet gateway router that has the entire internet routing table, which may not be desirable to distribute in its entirety to the rest of the network. Instead, an aggregated route (for example, `0.0.0.0/0`) is advertised to the other network elements.

For Static Routing configuration, the application provides the following resource based on the target deployment scenario:

* **For configuration in the Default VRF:**
    * [Default Static Route](resources/defaultstaticroute.md) for creating the static routes in the default VRF
    * [Default Aggregate Route](resources/defaultaggregateroute.md) for creating the aggregate routes in the default VRF
* **For configuration in the Overlay VRF**:
    * [Static Route](resources/staticroute.md) for creating the static routes in the overlay VRF
    * [Aggregate Route](resources/aggregateroute.md) for creating the aggregate routes in the overlay VRF

## Border Gateway Protocol (BGP)

BGP configuration in the Protocols application supports both the Default VRF and Overlay VRF deployments, with comprehensive features for peer management, route reflection, and policy control. EDA provides configuration options to facilitate both explicit and dynamic peer establishment.

Two routers that exchange routes using the BGP protocol are called **BGP Peers**, and they inherit settings from the **BGP Group** they belong to. To avoid a full-mesh BGP topology (where every router peers with every other router), designated **Route Reflectors** can be configured that all other routers peer with as Route **Reflector Clients**.

For BGP configuration, the application provides the following resource based on the target deployment scenario:

* **For configuration in the Default VRF**
    * [`DefaultBGPPeer`](resources/defaultbgppeer.md) and [`DefaultBGPGroup`](resources/defaultbgpgroup.md) for configuration of BGP peering sessions
    * [`DefaultRouteReflector`](resources/defaultroutereflector.md) and [`DefaultRouteReflectorClient`](resources/defaultroutereflectorclient.md) for route reflector configuration

* **For configuration in the Overlay VRF**
    * [`BGPPeer`](resources/bgppeer.md) and [`BGPGroup`](resources/bgpgroup.md) for configuration of BGP peering sessions.
    * [`RouteReflector`](resources/routereflector.md) and [`RouteReflectorClient`](resources/routereflectorclient.md) for route reflector configuration

## Open Shortest Path First (OSPF)

OSPF configuration in the Protocols application supports both Default VRF and Overlay VRF deployment models.

An alternative for the exchange of IPv4 and IPv6 routes is OSPF. Just like BGP, two OSPF neighbors establish an OSPF adjacency to advertise and receive the routes into and out of the default routing table or custom IP-VRF. OSPF needs to be enabled on two adjacent **OSPF Interfaces**, within a particular **OSPF Instance**, which is in turn created in a particular **OSPF area**.

The application provides support for OSPF in the two target deployment scenarios:

* **For configuration in the Default VRF**
    * [`DefaultOSPFArea`](resources/defaultospfarea.md), [`DefaultOSPFInstance`](resources/defaultospfinstance.md), and [`DefaultOSPFInterface`](resources/defaultospfinterface.md) for configuration of OSPF adjacencies
* **For configuration in the Overlay VRF**
    * [`OSPFArea`](resources/ospfarea.md), [`OSPFInstance`](resources/ospfinstance.md), and [`OSPFInterface`](resources/ospfinterface.md) for configuration of OSPF adjacencies

[^1]: For example, `Default BGP Peer`.
[^2]: The term VRF - Virtual Routing and Forwarding - is often called a network instance.
[^3]: The overlay resources do not carry any specific prefix, for example, the `BGP Peer` resource is used to define the BGP peer in the overlay VRF.
