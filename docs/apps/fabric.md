# Fabric

The Fabric application streamlines the construction and deployment of data center fabrics, suitable for environments ranging from small, single-node edge configurations to large, complex multi-tier and multi-pod networks. It automates crucial network configurations such as IP address assignments, VLAN setups, and both underlay and overlay network protocols, ensuring enhanced performance and reliability.

Upon deployment, the Fabric application initiates several supporting applications including ISLs (Inter-Switch Links), DefaultRouters, DefaultInterfaces, and DefaultBGPPeers, among others. These applications, in turn, generate node configurations. The operational state of the Fabric is determined by the collective status of these underlying applications.

## Selecting TopoNodes and TopoLinks

The Fabric application configures network nodes and their interswitch links using a mechanism based on label selectors. These selectors identify specific TopoNodes and TopoLinks that correspond to node roles within a Clos network architecture—such as Leaf, Spine, Super-spine, and Border-leaf. The role of a node significantly influences the configuration parameters applied to it, which are determined by additional inputs from the Fabric application such as the selected underlay or overlay network protocols.

### How Label Selectors Work

Label selectors are used to filter and select the key-value pairs assigned to TopoNodes and TopoLinks based on specific criteria such as their role within the network. Once these elements are labeled, the Fabric application can automatically apply the necessary configurations.

### Configuring Nodes and Links

1. **Initial Labeling:** If TopoNodes and TopoLinks are labeled before the creation of the Fabric instance, the application will automatically generate all necessary configurations for these components during the transaction associated with the addition of the Fabric instance.

2. **Post-Deployment Labeling:** If new labels that match the Fabric's selection criteria are added to TopoNodes and TopoLinks after the Fabric instance has been deployed, these components will automatically be configured by the Fabric application during the transaction that handles the addition of the labels. This ensures that changes in network topology or roles are dynamically incorporated into the Fabric's configuration.

### Example Label Selectors

- **Leaf Node Selector:** `eda.nokia.com/role=leaf`
- **Spine Node Selector:** `eda.nokia.com/role=spine`

## Assigning IP Addresses

IP addresses play a critical role in network configuration within the Fabric application. Here's how IP addressing is managed:

### System/Loopback Interfaces

- **IPv4 Assignment:** IPv4 addresses must be assigned to the primary loopback interface (System or Lo0) of each node.
- **IPv6 Assignment:** Optionally, IPv6 addresses can also be configured on these interfaces.

### TopoLink Interfaces

- The Fabric application requires the configuration of either IPv4 or IPv6 addresses on the interfaces selected by the TopoLink label selector. This ensures that all connections within the network are appropriately addressed.

### IP Address Allocation Pools

- IP addresses are automatically assigned from specified IP Address allocation pools. Separate pools are typically used for System interfaces and ISL (Inter-Switch Link) interfaces.
- **Important:** The allocation pool referenced for either set of interfaces must exist prior to the deployment of the Fabric application instance to ensure successful IP configuration.

The `systemPoolIPV4` property and `islPoolIPV4` or `islPoolIPV6 ` propertie must be provided.

## Selecting an Underlay Protocol

The Fabric application supports a single underlay protocol: eBGP. This section details how eBGP is implemented within the network fabric.

### eBGP Configuration

- **ISL Application:** The Fabric app will emit instances of the ISL application to configure both the IP addressing and the BGP peering between nodes on each of the TopoLinks.
- **Autonomous Systems:** Like IP addresses, the autonomous systems used by the eBGP sessions are automatically allocated from the specified ASN pool (`asnPool`).

### Routing Policies

- **Automatic Generation:** If not explicitly specified, the Fabric will automatically generate the required `RoutingPolicies`. These policies are used in the eBGP peering sessions to ensure IP reachability across the fabric.  However, if RoutingPolicies are defined independently of the Fabric they can be used by specifying the `importPolicy` and `exportPolicy` properties.

## Selecting an Overlay Protocol

The application supports the use of either eBGP or iBGP for transporting the EVPN AFI/SAFI, which are used for overlay services.

### eBGP Configuration

When eBGP is selected as the overlay protocol, it leverages existing eBGP sessions established by the underlay protocol. These sessions are extended to advertise the EVPN address family, in addition to the existing ipv4-unicast and ipv6-unicast families.  It should be noted that the import and export policies specified in the Underlay configuration will be used, any import or export policies specified in the overlay protocol will be ignored.

### iBGP Configuration

If iBGP is the preferred method for exchanging EVPN routes, additional properties must be configured within the Fabric application:

- **Autonomous System (`autonomousSystem`):** Specifies the AS used for the establishment of the iBGP session.

- **Route Reflector (RR) Configuration:**
  - **RR Client Node Selector (`rrClientNodeSelector`):** This label selector identifies TopoNodes to be configured as iBGP RR clients. It also drives the configuration of the selected iBGP RR neighbors if being configured by the Fabric.  Typically, this would select leaf and border leaf nodes.
    - Example: `eda.nokia.com/role=leaf`
  - **RR IP Addresses (`rrIPAddresses`):** If the Route Reflectors are not configured by the Fabric application, these IP addresses are used to configure the iBGP neighbors on the selected RR clients.
  - **RR Node Selector (`rrNodeSelector`):** This label selector identifies TopoNodes to be configured as iBGP Route Reflectors. It also drives the configuration of the selected iBGP RR client neighbors, typically involving spines or border leafs.
    - Example: `eda.nokia.com/role=borderleaf`

## Example fabric K8S CRs

### eBGP Underlay and Overlay dual stack IPv4/IPv6

```yaml
apiVersion: fabrics.eda.nokia.com/v1alpha1
kind: Fabric
metadata:
  name: ebgp-fabric1
spec:
  borderLeafNodeSelector: 
    - eda.nokia.com/role=borderleaf
  islPoolIPV4: ipv4-pool
  islPoolIPV6: ipv6-pool
  leafNodeSelector: 
    - eda.nokia.com/role=leaf
  linkSelector: 
    - eda.nokia.com/role=interSwitch
  spineNodeSelector: 
    - eda.nokia.com/role=spine
  superSpineNodeSelector: 
    - eda.nokia.com/role=superspine
  systemPoolIPV4: systemipv4-pool
  systemPoolIPV6: systemipv6-pool
  underlayProtocol:
    asnPool: asn-pool
    bfd:
      desiredMinTransmitInt: 10000
      detectionMultiplier: 3
      enabled: true
      requiredMinReceive: 30000
    exportPolicy: 
    importPolicy: 
    protocol:
      - ebgp
  overlayProtocol:
    protocol: ebgp
    bfd:
      desiredMinTransmitInt: 10000
      detectionMultiplier: 3
      enabled: true
      requiredMinReceive: 30000
```

### eBGP Underlay and iBGP Overlay dual stack IPv4/IPv6

```yaml
apiVersion: fabrics.eda.nokia.com/v1alpha1
kind: Fabric
metadata:
  name: ebgp-ibgp-fabric2
spec:
  islPoolIPV4: ipv4-pool
  islPoolIPV6: ipv6-pool
  systemPoolIPV4: systemipv4-pool
  systemPoolIPV6: systemipv6-pool
  borderLeafNodeSelector: 
    - eda.nokia.com/role=borderleaf
  leafNodeSelector: 
    - eda.nokia.com/role=leaf
  linkSelector: 
    - eda.nokia.com/role=interSwitch
  spineNodeSelector: 
    - eda.nokia.com/role=spine
  superSpineNodeSelector: 
    - eda.nokia.com/role=superspine
  underlayProtocol:
    asnPool: asn-pool
    bfd:
      desiredMinTransmitInt: 10000
      detectionMultiplier: 3
      enabled: true
      requiredMinReceive: 30000
    exportPolicy: 
    importPolicy: 
    protocol:
      - ebgp
  overlayProtocol:
    protocol: ibgp
    autonomousSystem: 500
    clusterID: 2.2.2.2
    rrClientNodeSelector:
      - eda.nokia.com/role in (leaf, borderleaf)
    rrNodeSelector:
      - eda.nokia.com/role in (spine)
    bfd:
      desiredMinTransmitInt: 10000
      detectionMultiplier: 3
      enabled: true
      requiredMinReceive: 30000
```

## Deploy the Fabric

Apply the fabric CR to your K8s cluster:

```shell
kubectl apply -f <path-to-yaml>
```

Verify the fabric operational state:

```shell
kubectl get fabrics

NAME           LAST CHANGE   OPERATIONAL STATE
ebgp-fabric1   104m          up
```
