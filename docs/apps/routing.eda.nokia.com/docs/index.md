# Routing Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/routing ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

The Routing app is one of the cornerstones of EDA, and of any datacenter network. It contains resources that configure the [underlay](#underlay-routing) connectivity of the network that are used to exchange [service routes](#overlay-and-underlay-concepts), as well as workflows that provide verification and debugging capabilities.

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [`DefaultRouter`](./resources/defaultrouter.md)
* [`DefaultInterface`](./resources/defaultinterface.md)
* [`SystemInterface`](./resources/systeminterface.md)

* [`Drain`](./resources/drain.md)

</div>
</div>
///

/// tab | Workflows
<div class="grid" markdown>
<div markdown>

* [`AttachmentLookup`](./resources/attachmentlookup.md)
* [`RouteLookup`](./resources/routelookup.md)
* [`RouteTrace`](./resources/routetrace.md)
* [`SystemPing`](./resources/systemping.md)

</div>
</div>
///

Reachability information in a typical datacenter can be divided into two categories

- **Underlay:** reachability information for the network elements in the datacenter
- **Overlay:** EVPN routes with reachability information on the hosts that are connected to virtual networking services

This is a very generalizing definition, and is frequently too conservative. For example, one can have an in-band virtual management network for the switches and/or computes, which is subsequently leaked into the [default router](./resources/defaultrouter.md).


## Overlay and Underlay concepts

The documentation frequently refers to "underlay routing" and "overlay routing". To explain the difference between the two, we focus on one of the cornerstones of datacenter networks — virtualized services — and explain how underlay and overlay networking works together to enable connectivity between two hosts.

??? example "An introduction to virtualized services"

    !!! note "Generalization galore"

        This section contains a lot of generalizations and simplifications, to the point where some of it may be inaccurate in certain scenarios. This section is meant as a very basic introduction into service routing, and should be read as such.

    Datacenter networking (and any networking for that matter) is all about providing connectivity for clients. For the sake of this discussion, clients are computers. In reality, clients can be anything from mobile subscribers to firewalls, mainframes, badge readers, barcode scanners, security cameras, and so much more.

    In its simplest form, two computers can talk to each other by connecting them with a cable:

    ![Back-to-back connectivity](./media/routing-connectivity_1.svg){ width="100%" }

    This is technically a network with two hosts, but isn't very flexible: what if a third PC is connected? We could connect computer B to computer C, but that too has big limitations: if computer B shuts down, computer A can no longer communicate with computer C:

    ![Ring connectivity](./media/routing-connectivity_2.svg){ width="100%" }

    We need a device that provides point-to-multipoint connectivity: either by replicating every packet to all other clients (hub) or by intelligently passing the packets to the right computer (switch).

    ![Hub or switch connectivity](./media/routing-connectivity_3.svg){ width="100%" }

    We're getting somewhere now! A collection of networking equipment and physical links that enable computers to talk to each other without restrictions is called a **broadcast domain** or **bridged domain**, and operates entirely on layer 2 traffic. As our network grows though, we will need to up our security and isolate different groups of clients. 
    
    For example, we may want to add a bunch of security cameras that we want to separate from our main computer network. That is where VLANs come into play: VLAN tags are numbers that are added to the ethernet header of a packet, and isolate traffic that is tagged with different VLANs.

    !!! note

        There are many more reasons why you want to isolate traffic other than security, for example to limit the amount of broadcast traffic that each connected client receives.

    ![VLAN isolation](./media/routing-connectivity_4.svg){ width="100%" }

    But we have a problem: now that the two broadcast domains are isolated from each other, our computers can't connect to the cameras anymore. To fix this, we need a router that routes connectivity from one IP subnet to another. This is the first time that our networking equipment needs to become aware of the IP addresses that the hosts will use to communicate: previously, the network acted as a mailbox, whereas from now on the network behaves more like a postman. 

    ![Routed connectivity](./media/routing-connectivity_5.svg){ width="100%" }

    The network has now grown so much that the clients can no longer all connect to the same network device. The network turns into a proper datacenter.

    ![Distributed networking](./media/routing-connectivity_6.svg){ width="100%" }

    For reasons beyond the scope of this explanation, exchanging IP reachability information using BGP as a route exchange protocol in this way will not work. We need a protocol that allows broadcast domains to stretch over multiple networking switches. 
    
    In the datacenter world, EVPN is most frequently used for the exchange of service routes: it is a very flexible routing protocol that uses transport tunnels as a next hop instead of IP addresses. These transport tunnels are set up between two routers and support traffic from multiple different services, ensuring traffic remains isolated at the remote end of the tunnel.

    !!! note "Transport tunnels"

        The two most common transport protocols are Multiprotocol Label Switching (MPLS) and Virtual Extensible LAN (VxLAN): MPLS uses labels to establish a tunnel, while VxLAN encapsulates traffic in an IP datagram with the source and destination IP address of network switches. VxLAN is often preferred in the datacenter, among other reasons because it can operate over existing (non-service aware) networks. 

    ![Distributed networking with EVPN](./media/routing-connectivity_7.svg){ width="100%" }

### Overlay routing

When the documentation refers to overlay routing, it is synonymous with data plane traffic within a service: it enables client traffic to go from one point in the datacenter to another, ensuring that the traffic remains isolated to the virtual bridge domain or virtual router. If EVPN is used, these service tunnels are identified by their EVPN Instance ID (EVI) and underlying transport tunnel. 

EVPN routes act as traffic rules and are created by networking equipment. They are communicated through the [underlay](#underlay-routing) MP-BGP sessions in the [`DefaultRouter`](./resources/defaultrouter.md). 

### Underlay routing

When the documentation refers to underlay routing, it is synonymous with control plane traffic in the [`DefaultRouter`](./resources/defaultrouter.md) of the switches: it enables the network elements to communicate with each other using the BGP, OSPF, or IS-IS routing protocol to find the optimal path through the network. These protocols exchange [system IP addresses](./resources/systeminterface.md) that will be used to establish the MP-BGP sessions that exchange [overlay](#overlay-routing) routes.

Think of the underlay as highways that interconnect cities, and overlay routing as the traffic rules that everyone must follow: these rules determine which packets can take which exits and which lane they must follow once they exit the highway.