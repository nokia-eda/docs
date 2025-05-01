# Virtual Network (VNET)

The Virtual Network (`VNET`) application is a resource designed to group and manage network services together, typically deployed as overlay services. The VNET simplifies management by serving as a single input for a set of resources that support a common set of applications.

## Core Components of VNET

The primary components that make up the VNET include:

- **BridgeDomain**: Represents a Layer 2 broadcast domain. It is used in conjunction with VLAN and BridgeInterface resources, which attach sub-interfaces to this L2 broadcast domain.

- **VLAN**: Groups sub-interfaces together under a common VLAN ID. VLAN IDs can be automatically assigned from a pool or manually set by the user.  The VLAN uses a label selector to select the interfaces on which to provisioning the sub-interfaces.

- **BridgeInterface**: Allows operators to manually attach a sub-interface to a specific BridgeDomain.

- **Router**: Acts as a Layer 3 domain manager. It can connect multiple BridgeDomains through an `IRBInterface` or link directly to `RoutedInterfaces`.

- **IRBInterface** (Integrated Routing and Bridging Interface): Connects a BridgeDomain to a Router, facilitating communication between Layer 2 and Layer 3 networks.

- **RoutedInterface**: Represents a directly connected Layer 3 interface on a device that is attached to a Router.

- **DHCPRelay**: Enables DHCP relay functionality on sub-interfaces within the VNET, facilitating dynamic IP address allocation.

## Additional Capabilities

- **PE-CE BGP**: The VNET also supports Provider Edge to Customer Edge (PE-CE) BGP.
- **IP Filters**: IPv4, IPv6 and MAC filters can also be used within the `VirtualNetwork`.
- **DSCP and Dot1p classifiers**: Attachment of DSCP and Dot1p classifiers are also supported.

## Example VNETs

### Layer 2 VNET

/// tab | `kubectl`

```bash
cat << 'EOF' | tee l2-vnet.yaml | kubectl apply -f -
--8<-- "docs/examples/l2-vnet.yaml"
EOF
```

///
/// tab | YAML

```yaml
--8<-- "docs/examples/l2-vnet.yaml"
```

///

### Layer 3 VNET

/// tab | `kubectl`

```bash
cat << 'EOF' | tee l3-vnet.yaml | kubectl apply -f -
--8<-- "docs/examples/l3-vnet.yaml"
EOF
```

///
/// tab | YAML

```yaml
--8<-- "docs/examples/l3-vnet.yaml"
```

///

## Verify the status of the `VirtualNetwork`

Verify the fabric operational state:

```shell
kubectl -n eda get virtualnetwork

NAME    OPERATIONALSTATE   LASTCHANGE
vnet1   down               2024-04-30T21:26:36.000Z
vnet2   degraded           2024-04-30T22:47:38.000Z
```
