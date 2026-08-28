---
resource_name: IRBInterface
resource_name_plural: irbinterfaces
resource_name_plural_title: IRB Interfaces
resource_name_acronym: II
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_irbinterfaces.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# IRB Interface

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `IRBInterface` is used to connect a [`BridgeDomain`](./bridgedomain.md) to a [`Router`](./router.md). This is required to allow hosts within a [`BridgeDomain`](./bridgedomain.md) to communicate with the outside world. 

Example: if the host has IP address `192.168.100.123/24`, it may use a gateway to reach the internet: it is configured with a default static route, for example, to reach anything not in the `192.168.100.0/24` subnet. 

On Linux, the default static route usually looks like this: `0.0.0.0/0 via 192.168.100.1`. The gateway IP, `192.168.100.1` in this case, is configured as an anycast gateway IP on the `IRBInterface`.

## Secondary IP addresses

A typical `IRBInterface` may have one anycast IP address on all nodes, and a secondary IP address for each node individually. Some use cases:

- BGP sessions may be established from either the primary IP or the secondary IP (see [below](#bgp-and-bfd))
- A [DHCP relay](./dhcprelay.md) requires a secondary IP to be configured on each node that will be acting as a DHCP relay
- For debugging purposes, it may be useful to configure a secondary IP address on at least one node, to confirm routed connectivity to a particular IP

### BGP and BFD

BFD settings may be configured for every BGP session established by this `IRBInterface`. There are many designs where routers initiate BGP sessions with hosts connected to the datacenter. The most common scenarios are discussed below.

#### Single-homed PE-CE sessions (no BGP session redundancy)

When a host is connected to a [`BridgeDomain`](./bridgedomain.md), it may establish a BGP session with the IRB on the top-of-rack (leaf) to exchange routes with the datacenter. No secondary IP address is required, and the session may be initiated by either the node or the host.

This design is not well-suited for VMs that move freely between racks.

- **When the active leaf fails:** the BGP session goes down and does not recover.

#### Multi-homed PE-CE sessions (no BGP session redundancy)

When a host is connected to multiple network elements (for example, for redundancy purposes) and establishes a BGP session with the `IRBInterface`, the network elements should not actively try to establish the BGP session. 

Instead, the [`BGPPeer`](-{{ ref_app_doc('protocols', 'bgppeer') }}-) should dynamically accept BGP sessions from the host IP subnet, because the host will only establish a single BGP session, with one of the switches it is connected to.

This design is well-suited for VMs that move freely between racks, but does not provide redundant BGP sessions.

/// warning | Using secondary IP addresses to establish PE-CE sessions

Establishing redundant BGP sessions from the secondary IP addresses instead of the primary anycast gateway IP may look like a good idea, but may not actually provide redundancy: the host may choose the same leaf to reach both secondary IP addresses, which will both fail when that leaf fails.
///

- **When the active leaf fails:** the BGP session is re-established with the other leaf. During the switchover, routes are withdrawn by both the datacenter and the peer.

#### Multi-homed PE-CE sessions (redundant BGP sessions)

If the host creates 2 BGP sessions for redundancy, the centralized routing model should be preferred where the `IRBInterface` lives on the spine switches or borderleafs rather than on the top-of-rack (leaf) switches. This way, true redundancy is achieved for BGP sessions.

- **When a leaf fails:** both peer IP addresses are still reachable through the other leaf
- **When a spine/borderleaf fails:** the other peer IP addresses are still reachable through either/all leafs

### EVPN route advertisement

**EVPN route advertisement** refers to the concept of advertising EVPN route-type 2 MAC-IP bindings to other nodes that participate in the [`BridgeDomain`](./bridgedomain.md). It ensures that every participating node has a full view of all MAC-IP bindings.

#### No EVPN route advertisement

If no MAC-IP routes are advertised, routing may not work at all: see [asymmetric vs symmetric routing](../index.md#symmetric-and-asymmetric-routing) for more details. 

/// details | Example: why routing may not work without EVPN route advertisement
    type: example

Imagine a scenario where [`BridgeDomain`](./bridgedomain.md) `A` is deployed only on leaf 1, and [`BridgeDomain`](./bridgedomain.md) `B` is deployed only on leaf 7 and 8. Both [`BridgeDomain`](./bridgedomain.md) services are connected to the same [`Router`](./router.md). Leaf 1 sends the packet to the subnet of `B`, and the [`Router`](./router.md) chooses leaf 7 to send the packet to, as one of the two next-hops for that subnet.

Leaf 7 receives the packet, but does not know the MAC address that the destination IP is associated with. It therefore holds the packet and sends out an ARP request for the destination IP, to all locally connected sub-interfaces and to leaf 8. 

Leaf 8 receives the broadcast ARP request, and replicates it towards all locally connected sub-interfaces.

The destination host, which is multi-homed to leafs 7 and 8, receives the ARP request and responds with its MAC address. It sends the ARP response as a unicast packet, with the destination IP set to the anycast gateway (configured on leaf 7, which originated the ARP request, and leaf 8).

Leaf 8 (by chance) receives the ARP response and sees that the destination IP is set to its own destination gateway IP, and processes the ARP response. It installs the MAC-IP binding, but since EVPN route advertisement is turned off, it does not broadcast this information to leaf 7. Hence, leaf 7 will never know where to send the packet to and will eventually drop it.

///

#### Dynamic EVPN route advertisement

When enabled for ARP and/or ND, locally learnt MAC-IP bindings are advertised to other nodes that participate in the same [`BridgeDomain`](./bridgedomain.md). 

#### Static EVPN route advertisement

When enabled for ARP and/or ND, locally configured static MAC-IP bindings are advertised to other nodes that participate in the same [`BridgeDomain`](./bridgedomain.md). 

/// details | Example of a statically configured MAC-IP binding for Nokia SR Linux
    type: example

```text
network-instance MAC-VRF-1 {
    bridge-table {
        proxy-arp {
            admin-state enable
            static-entries {
                neighbor 101.1.1.1 {
                    link-layer-address 00:00:64:01:01:01
                }
            }
        }
    }
}
```

///

### Host route population

**Host route population** refers to the concept of installing host (`/32`) IP addresses in the routing table of the [`Router`](./router.md). It ensures that the most efficient route is taken, even if the destination bridge domain is not configured on the ingress node.

#### No host route population

If no host routes are installed in the routing table, routing may not be optimal: see [asymmetric vs symmetric routing](../index.md#symmetric-and-asymmetric-routing) for more details. 

#### Dynamic host route population

When enabled, the `IRBInterface` creates host (`/32`) routes in the routing table of the virtualized [`Router`](./router.md) service for dynamically learnt MAC-IP bindings. A dynamic host entry in this context is a host that is connected to one of the local bridge interfaces.

#### EVPN host route population

When enabled, the `IRBInterface` creates host (`/32`) routes in the routing table of the virtualized [`Router`](./router.md) service for MAC-IP bindings learnt through EVPN. An EVPN host entry in this context is a host that is remotely connected to one of the other nodes participating in the bridge domain.

#### Static host route population

When enabled, the `IRBInterface` creates host (`/32`) routes in the routing table of the virtualized [`Router`](./router.md) service for statically configured MAC-IP bindings.

/// details | Example of a statically configured MAC-IP binding for Nokia SR Linux
    type: example

```text
network-instance MAC-VRF-1 {
    bridge-table {
        proxy-arp {
            admin-state enable
            static-entries {
                neighbor 101.1.1.1 {
                    link-layer-address 00:00:64:01:01:01
                }
            }
        }
    }
}
```

///

### Proxy ARP / ND

Proxy-ARP / proxy-ND are IPv4 / IPv6 anti-flooding mechanisms, and allow a leaf node that receives an ARP request (IPv4) or neighbor solicitation (IPv6) to answer on behalf of the destination host. This prevents the request from being flooded to all possible destination endpoints.

For proxy-ARP / proxy-ND to work, the leaf node needs to know the MAC-IP binding of the destination host. Therefore, [EVPN advertisement](#evpn-route-advertisement) must be enabled.

### IRB index allocation

On some network operating systems, IRB (sub-)interfaces are numbered. For example, on Nokia SR Linux, the subinterface index is a number between 0 and 9999. The `IRBInterface` has three modes to assign this number:

- `GlobalPool`: allocates a single index per `IRBInterface` from the `IndexAllocationPool` with name `irb-subif-pool`, which is a pool that is by default configured in EDA.
- `PerNodePool`: allocates a single index per `IRBInterface` on that particular node, from the pool specified in the `indexAllocation.indexPool` property. This is useful if the number of `IRBInterfaces` in your network is very large, but the number of `IRBInterfaces` configured on any particular node is significantly less.
- `Manual`: allows manual specification of the IRB sub-interface index.

/// warning | Default size of the 'irb-subif-pool'

    The size of the default `IndexAllocationPool` with name `irb-subif-pool` is limited to 4000 by default. Consider using the `PerNodePool` mode if the number of `IRBInterface` resources in your network exceeds this number. 
///

## Dependencies

### [`BridgeDomain`](./bridgedomain.md)

An `IRBInterface` is always connected to a [`BridgeDomain`](./bridgedomain.md). When configured with an anycast IP address, it can act as a gateway for routed traffic from hosts connected to the [`BridgeDomain`](./bridgedomain.md).

### [`Router`](./router.md)

An `IRBInterface` is always connected to a [`Router`](./router.md) where it allows bridged traffic to be routed to other subnets.

## Referenced resources

### [`Filter`](-{{ ref_app_doc('filters', 'filter') }}-)

Traffic that is received by or sent from the `IRBInterface` can optionally be filtered by specifying one or more [`Filter`](-{{ ref_app_doc('filters', 'filter') }}-) resources in the `ingress` (respectively `egress`) container.

### [`IngressPolicy`](-{{ ref_app_doc('qos', 'ingresspolicy') }}-)

Traffic that is received by the `IRBInterface` can optionally be processed by one or more QoS [`IngressPolicies`](-{{ ref_app_doc('qos', 'ingresspolicy') }}-) by specifying them in the `ingress` container.

### [`EgressPolicy`](-{{ ref_app_doc('qos', 'egresspolicy') }}-)

Traffic that is sent by the `IRBInterface` can optionally be processed by one or more QoS [`EgressPolicies`](-{{ ref_app_doc('qos', 'egresspolicy') }}-) by specifying them in the `egress` container.

### `IndexAllocationPool`

Optionally, an `IndexAllocationPool` may be specified for the assignment of the IRB sub-interface on some operating systems. For more information, see [IRB index allocation](#irb-index-allocation).

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
