# Fabric

The Fabric application streamlines the construction and deployment of data center fabrics, suitable for environments ranging from small, single-node edge configurations to large, complex multi-tier and multi-pod networks. It automates crucial network configurations such as IP address assignments, VLAN setups, and both underlay and overlay network protocols.

Upon deployment, the Fabric application initiates several supporting applications including ISLs (Inter-Switch Links), DefaultRouters, DefaultInterfaces, and DefaultBGPPeers, among others. These applications, in turn, generate node configurations. The operational state of the Fabric is determined by the collective status of these underlying applications.

## Deployment Models

The Fabric application supports highly flexible deployment models, enabling you to tailor the configuration of your data center fabric to suit different architectural needs. You can deploy a single instance of a Fabric resource to manage the entire data center, incorporating all network nodes, or you can opt to divide your data center into multiple, smaller Fabric instances.

For example, you might deploy one Fabric instance to manage the superspine and borderleaf layers while deploying separate Fabric instances for each pod within the data center. This modular approach allows for more granular control.  This can be taken to the extreme where each layer of a datacenter fabric could be its own instance of a Fabric.  The choice is yours!

The Fabric application facilitates interconnecting these Fabric instances through the fabricSelector property. This property enables different Fabric instances to work together seamlessly, ensuring that the network functions as a cohesive whole even when managed by multiple instances of the Fabric resource.

The fabricSelector is a label selector that selects adjacent Fabrics based on their assigned labels and the criteria specified in the selector. The fabricSelector operates in a unidirectional manner, meaning only the upper layer of the fabric needs to select the downstream fabrics. For example, the instance of the Fabric representing the superspine layer would use a label selector to select the pod Fabrics; the pod Fabrics do not need nor should they to select the superspine layer.  Example found below.

## Selecting TopoNodes, TopoLinks and Fabrics

The Fabric application configures network nodes, their interswitch links, and the interconnections between different Fabric instances using a mechanism based on label selectors. These selectors identify specific TopoNodes, TopoLinks, and adjacent Fabric instances that correspond to node roles within a typical Clos network architecture—such as Leaf, Spine, Super-spine, and Border-leaf. The role of a node and the interconnections between Fabric instances significantly influence the configuration parameters applied to them, which are determined by additional inputs from the Fabric application such as the selected underlay or overlay network protocols.

### How Label Selectors Work

Label selectors are used to filter and select the key-value pairs assigned to TopoNodes, TopoLinks, and other Fabric instances based on specific criteria such as their role within the network. Once these elements are labeled, the Fabric application can automatically apply the necessary configurations.

### Configuring Nodes, Links, and Fabrics

1. **Initial Labeling:**  If TopoNodes, TopoLinks, and adjacent Fabric instances are labeled before the creation of the Fabric instance, the application will automatically generate all necessary configurations for these components during the transaction associated with the addition of the Fabric instance.

2. **Post-Deployment Labeling:** If new labels that match the Fabric's selection criteria are added to TopoNodes, TopoLinks, or adjacent Fabric instances after the Fabric instance has been deployed, these components will automatically be configured by the Fabric application during the transaction that handles the addition of the labels. This ensures that changes in network topology, roles, or Fabric interconnections are dynamically incorporated into the Fabric's configuration.

### Example Label Selectors

- **Leaf Node Selector:** `eda.nokia.com/role=leaf`
- **Spine Node Selector:** `eda.nokia.com/role=spine`
- **Fabric Selector:** `eda.nokia.com/pod=pod1`

## Assigning IP Addresses

IP addresses play a critical role in network configuration within the Fabric application. Here's how IP addressing is managed:

### System/Loopback Interfaces

- **IPv4 Assignment:** IPv4 addresses must be assigned to the primary loopback interface (System or Lo0) of each node.
- **IPv6 Assignment:** Optionally, IPv6 addresses can also be configured on these interfaces.

### TopoLink Interfaces

- The Fabric application requires the configuration of either IPv4, IPv6 addresses or the use of IPV6 unnumbered on the interfaces selected by the TopoLink label selector under the `InterSwitchLinks` property . This ensures that all connections within the network are appropriately addressed.

### IP Address Allocation Pools

- IP addresses can be automatically assigned from specified IP Address allocation pools. Separate pools are typically used for System interfaces and ISL (Inter-Switch Link) interfaces.
- **Important:** The allocation pool referenced for either set of interfaces must exist prior to the deployment of the Fabric application instance to ensure successful IP configuration.

The `systemPoolIPV4` property must be provided.

## Optional IP Pools and Autonomous Systems per Role

The Fabric application allows for the optional specification of system IP pools and autonomous systems for different roles within the network fabric. These optional configurations can override the global settings.

For each role (Leaf, Spine, Superspine, Borderleaf) the following properties may be configured:

- **Autonomous System:** The `asnPool` property allows for a specific ASN pool to be used for eBGP sessions, override the pools specified under the underlay protocol section.
- **IP Pools:** The `systemPoolIPV4` and `systemPoolIPV6` properties can be specified to dynamically allocate IP addresses for the System/ lo0 interfaces.

## Selecting an Underlay Protocol

The Fabric application currently supports a single underlay protocol: eBGP. This section details how eBGP is implemented within the network fabric.

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

### Simple Leaf / Spine Fabric

/// tab | `kubectl`

```bash
cat << 'EOF' | tee my-fabric.yaml | kubectl apply -f -
--8<-- "docs/examples/my-fabric.yaml"
EOF
```

///
/// tab | YAML

```yaml
--8<-- "docs/examples/my-fabric.yaml"
```

///

## Verify the Fabric

Verify the fabric operational state:

```shell
kubectl get fabrics

NAME           LAST CHANGE   OPERATIONAL STATE
sunnyvale-dc1   104m          up
```
