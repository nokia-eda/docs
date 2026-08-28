---
resource_name: DHCPRelay
resource_name_plural: dhcprelays
resource_name_plural_title: DHCP Relays
resource_name_acronym: DR
crd_path: docs/apps/services.eda.nokia.com/crds/services.eda.nokia.com_dhcprelays.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# DHCP Relay

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The DHCP protocol is used to dynamically assign IP addresses to a host that asks for one. Because a requesting host has no assigned address yet, the initial DHCP Discover is sent from source IP `0.0.0.0` to the limited broadcast `255.255.255.255`, which routers do not forward across subnet boundaries. This is a problem in cases where the DHCP server manages multiple subnets: it would need to be reachable in every broadcast domain, which is often not feasible.

Instead, we use a **DHCP relay** that intercepts the broadcast DHCP message and forwards it as a unicast packet to the DHCP server, recording its own IP address as the gateway address. This intermediary device then *relays* messages in both directions: DHCP client requests are forwarded as unicast packets to the server, and server responses are forwarded back to the client.

The `DHCPRelay` can be configured on two interface types, which are always tied to a virtual [`Router`](./router.md):

- An [`IRBInterface`](./irbinterface.md) that connects to a [`BridgeDomain`](./bridgedomain.md), which can have many sub-interfaces connected to it
- A [`RoutedInterface`](./routedinterface.md) is essentially a broadcast domain on a single physical interface, although there may of course be many devices behind that interface

## Sub-options

DHCP relay options can be defined which add additional information to the DHCP request, such as the sub-interface on which the relay received the DHCP request.

For DHCPv4, the following options are supported:

- `CircuitID`
- `RemoteID`

For DHCPv6, the following options are supported:

- `RemoteID`
- `InterfaceID`
- `ClientLinkLayerAddress`

```text
instance 2 (dhcp-router),
   transmitted DHCP Boot Request to 10.10.10.10 Port 67

   H/W Type: Ethernet(10Mb)  H/W Address Length: 6
   ciaddr: 192.168.0.119     yiaddr: 0.0.0.0
   siaddr: 0.0.0.0           giaddr: 192.168.0.14
   chaddr: aa:13:8c:4d:db:8d    xid: 0x54dea877

   DHCP options:
   [82] Relay agent information: len = 40
      [1] Circuit-id: dc1-leaf4|dhcp-router|irb0|0:0       <-- Added by the DHCP relay
      [2] Remote-id: (hex) aa 13 8c 4d db 8d               <-- Added by the DHCP relay
   [53] Message type: Request
   [57] Max msg size: 576
   [55] Param request list: len = 7
             1  Subnet mask
             3  Router
             6  Domain name server
            12  Host name
            15  Domain name
            28  Broadcast addr
            42  NTP server
   [60] Class id: udhcp 1.36.1
   [61] Client id: (hex) 01 aa 13 8c 4d db 8d
   [255] End
```

## Dependencies

The `DHCPRelay` resource has no dependencies. However, it is only configured on a particular node if at least one [`IRBInterface`](./irbinterface.md) or [`RoutedInterface`](./routedinterface.md) is present on that node.

## Referenced resources

### [`IRBInterface`](./irbinterface.md)

If the DHCP relay is configured on [`IRBInterfaces`](./irbinterface.md) (which connect a [`BridgeDomain`](./bridgedomain.md) to a [`Router`](./router.md)), then those IRB interfaces should exist and be configured with at least one primary IP address. If an [`IRBInterface`](./irbinterface.md) does not have a primary IP on a node, the DHCP relay will not be deployed on that interface.

### [`RoutedInterface`](./routedinterface.md)

If the DHCP relay is configured on [`RoutedInterfaces`](./routedinterface.md) (which connect an [`Interface`](-{{ ref_app_doc('interfaces', 'interface') }}-) to a [`Router`](./router.md)), then those routed interfaces should exist and be configured with at least one primary IP address. If a [`RoutedInterface`](./routedinterface.md) does not have a primary IP on a node, the DHCP relay will not be deployed on that interface.

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
