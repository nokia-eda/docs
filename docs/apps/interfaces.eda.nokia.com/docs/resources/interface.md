---
resource_name: Interface
resource_name_plural: interfaces
resource_name_plural_title: Interfaces
resource_name_acronym: I
crd_path: docs/apps/interfaces.eda.nokia.com/crds/interfaces.eda.nokia.com_interfaces.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Interface

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

An `Interface` resource represents an endpoint that terminates physical connectivity. While an `Interface` is always required to enable connectivity between two hosts, it is often not sufficient on its own. It is important to understand the difference between an interface and a sub-interface:

!!! info "Untagged interfaces"

    The term "interface" is ambiguous: it can refer to a physical port, an untagged port, or a VLAN-enabled logical interface (also known as a sub-interface). Throughout the documentation, the following definitions are followed:

    - A **port** is a physical connector that an optical or copper connector can be plugged into
    - An **interface** is an abstract representation of an endpoint (one side of a connection). It can be either:
        - One **port** on a single physical network element
        - Multiple **ports** on a single physical network element (link aggregation)
        - A set of **ports** distributed over multiple physical network elements (multi-homed endpoint)
        - A virtual interface (loopback, see below)
    - A **sub-interface** is a logical host on an **interface** with its own MAC address (and, optionally, IP address)
        - A sub-interface can be untagged in which case only a single **sub-interface** can exist on the **interface**
        - Multiple sub-interfaces can exist on the same **interface** as long as each **sub-interface** has its own (set of) **VLAN(s)**

## Interface types

The `type` of the interface can be set to `Interface`, `Lag`, or `Loopback`. Each type is discussed in detail below.

### Interface

The default type of an `Interface` resource is `Interface`, which is restricted to one member port. 

### Lag

A Link Aggregation Group (LAG) is an interface with one or more member ports, which provides link redundancy and increased bandwidth. LAG interfaces can be configured to use the Link Aggregation Control Protocol (LACP).

Support is provided for both local and ESI-based[^1] LAGs: in the latter, members of the same LAG interface are distributed over multiple network elements. This **does not** enable connectivity between those ports, but rather makes these network elements work together in multi-homing mode, providing node level redundancy for the other end of the link. 

#### LACP

LAG interfaces that use the LACP protocol communicate the status of the individual members to the other end of the link. Based on this status, the other end of the link can decide whether or not to send traffic on that member port.

The `minLinks` parameter can be used to disable an interface entirely if one or more member links are operationally down. This is used in scenarios where physical ports are bundled to provide greater bandwidth throughput, allowing traffic to find a different path through the network towards the end destination in case of link failures.

#### Multi-homing parameters

In cases where LAG interface members are distributed over multiple nodes, multi-homing can be enabled: this configures an ethernet segment over all member ports. Ethernet segments rely on the EVPN protocol to operate, and are beyond the scope of this article.

### Loopback

A loopback interface is not tied to a physical port, but rather belongs to a (virtual) router. A loopback is an interface, meaning it can be configured with multiple sub-interfaces - each with their own IP address. Since these sub-interfaces are not connected to a physical port, a VLAN ID is not used.

Some use cases for loopback interfaces:

- To assign an IP address to a network element for testing purposes
- Overwriting the source IP address for self-generated traffic

!!! warning "Loopback interfaces must not be used as system IP address"

    In EDA, the system interface (also known as the router ID or router IP) is created through a dedicated resource: the [`SystemInterface`](../../../routing.eda.nokia.com/docs/resources/systeminterface.md).

## Interface Naming and Normalization

The Interface application employs a standardized, or normalized, format for interface names within its configurations. This approach ensures consistency when defining interfaces across diverse network operating systems (NOS). The system subsequently translates these normalized names into the specific format required by each target OS.

A key aspect of EDA's interface modeling is the use of normalized interface names. Typically, an OS-native interface name like `ethernet-1/13` is represented as `ethernet-1-13` in EDA configurations by replacing non-alphanumeric characters (like `/`) with a dash (`-`). This normalized name is then used by the system to derive the OS-specific interface identifier.

The following subsections detail how these normalized EDA interface names are translated for various supported operating systems, based on the underlying logic.

/// tab | SR Linux

- Native interface name `ethernet-1/1` is normalized as `ethernet-1-1`.
- Breakout interfaces like `ethernet-1/1/1` become `ethernet-1-1-1`.
- Loopback interfaces such as `lo0` translate to `loopback-0`.
- LAG interfaces like `lag10` translate to `lag-10`.

/// 

/// tab | SR OS

- Native port identifier `1/1/1` translates to `ethernet-1-a-1` name, where "a" is the first MDA on a 1st line card.
- The system supports more complex mappings for different hardware configurations:
    - Port `2/2/1` translates to `ethernet-2-b-1` (representing linecard 2, MDA "b"[^2], port 1).
    - Breakout (implicit MDA 1): `1/1/c1/1` translates to `ethernet-1-1-1`.
    - Breakout (explicit "a" for MDA 1): `1/1/c2/1` translates to `ethernet-1-a-2-1` (where MDA "a" maps to 1, and "2-1" defines the port as `c2/1`).
    - XIOM MDA: `1/x1/1/1` translates to `ethernet-1-1-a-1`.
- Loopback interfaces like `lo0` become `loopback-0`.
- LAG interfaces retain names like `lag-10`.

///

## Encapsulation options

The encapsulation type of the `Interface` determines how many VLAN headers are attached to egressing traffic. Note that the encapsulation type is ignored for Loopback interfaces.

- `encapType Null`: no VLAN headers are attached
- `encapType Dot1q`: one VLAN header

!!! note

    Q-in-Q is currently not supported.

## Storm control

To protect the network, storm control is frequently enabled on customer-facing interfaces. This is done to prevent traffic storms, which happen for example when a customer that has connectivity over two different interfaces accidentally connects these two interfaces in their own network. 

Storm control provides support for separate rate limits for

- Broadcast traffic
- Multicast traffic
- Unknown unicast traffic

/// tab | YAML

```yaml
-{{ include_snippet("interface_stormcontrol") }}-
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
-{{ include_snippet("interface_stormcontrol") }}-
EOF
```

///

## Dependencies

The `Interface` resource has no dependencies.

## Referenced resources

### `TopoNode`

Each `Interface` member is configured on a node. If the interface is distributed over multiple nodes (multi-homing), multiple `members` can be added to the `Interface` resource.

## OS-specific implementation notes

The `Interface` resource is supported on the following operating systems:

- Nokia SR Linux
- Nokia SR OS 
- Cisco NX-OS
- Arista EOS

### SR OS

In SR OS, the parameter `mode` determines the places where an interface can be used:

- `Network`: sub-interfaces can only be used in the default (underlay) router, not in virtual networks
- `Access`: sub-interfaces can only be used in virtual networks, not in the default (underlay) router
- `Hybrid`: sub-interfaces can be used both in the default (underlay) router and in virtual networks

The `mode` of the interface has some implications for which QoS functionality is available. For more information, refer to the SR OS user documentation. When the appropriate mode is unclear, omit this property.

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

[^1]: An EVPN standard-based alternative to proprietary Multi-chassis LAGs.
[^2]: Letter "b" means 2nd MDA.