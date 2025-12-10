# OpenStack Plugin

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

## Overview

EDA Cloud Connect integrates with OpenStack to provide fabric level application networks for OpenStack virtual machines. The EDA Cloud Connect
integration leverages the OpenStack Neutron architecture to support managing the fabric directly from OpenStack and make the fabric dynamically
respond to the networking needs of the application.

It provides the following advantages and capabilities:

* Direct integration into the network management workflow of OpenStack.
* The use of the common ML2 plugins used by enterprise applications and VNFs like OVS, OVS-DPDK and SR-IOV.
* Support for multiple operational modes, (See also [Operational Modes](#operational-modes).
  * OpenStack-managed: Automatic provisioning of the fabric based on where the virtual machines need the connectivity.
  * EDA-managed: Support advanced workflows directly through EDA, including for VNF use cases with features like QoS, ACLs, and BGP PE-CE.
* Interconnectivity between different cloud environments, allowing for flexible network configurations.

## Supported Versions

* Red Hat OpenStack Platform (RHOSP) 17.1

## Architecture

The OpenStack Plugin deploys some components into the OpenStack environment to allow the management of the SR Linux based fabric through OpenStack.
Below is an overview of these components:

-{{ diagram(url='nokia-eda/docs/diagrams/openstack-architecture.drawio', title='', page=0) }}-

### The Connect ML2 mechanism driver

The Connect ML2 mechanism driver plugin is the heart of the integration between OpenStack and EDA. This plugin integrates with OpenStack Neutron and reacts to the
creation of Networks, Network Segments and VM ports.

Whenever a network segment is created in OpenStack Neutron, a matching `BridgeDomain` and `VLAN` is created in EDA.

When a VM port is created inside a Neutron Subnet and the VM is started on an OpenStack compute node, the OpenStack plugin learns on which compute node the
VM is deployed and through the internal topology ensures the necessary `ConnectInterfaces` are configured in EDA.

The internal topology is learned from the L2 Agent extension which stores the Neutron Network to physical interfaces mapping in the Neutron database.
This is then provided to the Connect service and together with the LLDP information of the fabric, the Connect service knows which downlinks in the
fabrics need to be configured.

### The Connect L2 Agent Extension

The Connect L2 Agent Extensions extend the already existing L2 Agent that is present on every OpenStack compute. These extensions are responsible for
mapping the relation between the physical NICs and the different networking constructs setup for the Neutron networks.

## Installation

For detailed deployment instructions, see the [OpenStack Plugin Installation Guide](openstack-plugin-installation.md).

## Features

### Operational Modes

The plugin supports two operational modes for managing networking, selectable on a per-network basis:

#### OpenStack managed networks

In OpenStack managed mode, all networking is defined in OpenStack. The standard API commands for creating networks and subnets remain valid.

For each VLAN segment created in OpenStack, a corresponding `BridgeDomain` will be created in EDA.

/// details | default network type
    type: info
Neutron defines the default network type for tenant networks. If you want non-administrators to create their own networks that are offloaded to
the EDA fabric, the network type must be set to 'vlan'.
However, if only administrators need this capability, then the network type can be left to its default, since administrators can specify the
network type as part of network creation.

///

In Openstack managed mode only layer 2 `BridgeDomains` are defined in EDA. Layer 3 connectivity such as routing and floating ips 
is however supported through the usual OpenStack routing implementation. These layer 3 capabilities are then not supported by the fabric, but purely
software defined.

#### EDA managed networks

In addition to the OpenStack managed networking model, Connect supports networking managed by EDA itself. In this case, `VNET` or `BridgeDomain`
resources are created first in EDA directly, and then are consumed in OpenStack.

To support EDA managed networking, a proprietary extension has been added to Network: `eda_bridge_domain`. This refers to the `Name` of a
`BridgeDomain` you want to link the network to.

#### Using the EDA Managed operational mode

**Step 1** - Using the EDA rest API, the Kubernetes interface or the UI: Create a VNET with BridgeDomain or a standalone BridgeDomain.

**Step 2** - Obtain the name of the resources.

/// details | EDA managed networking and namespaces
    type: warning
The Connect OpenStack plugin can only see resources in its own namespace, cross namespace referencing is not supported.
///

**Step 3** - Create OpenStack resources.

An example workflow is included below:

* In OpenStack create the consuming network, linking it to the pre-created entity.
  `openstack network create --eda-bridge-domain xyz os-network-1`

/// details | Granularity at the network segment level
    type: note
Since BridgeDomains are actually mapped at the network segment level, you can also specify --eda-bridge-domain when creating a network segment.

```openstack network segment create --network os-network-1 --network-type vlan --eda-bridge-domain xyz os-network-segment-1```
///

* Create a subnet within this network using the standard API syntax. For example:
  `openstack subnet create --network os-network-1 --subnet-range 10.10.1.0/24 os-subnet-1`

* Create a Neutron port and Nova server within this network and subnet also uses standard APIs.

The OpenStack plugin will handle the creation of `VLAN` and `ConnectInterface` resources as in the OpenStack managed use case. However, the
`BridgeDomain` will be fully owned by the operator.

### Virtualization and network types

The EDA Connect OpenStack plugin supports the following segmentation types:

* VLAN: The plugin orchestrates on VLAN neutron networks, programming the EDA Cloud Connect service for fabric-offloaded forwarding.
* VXLAN and GRE: The plugin will not orchestrate on VXLAN or GRE neutron networks, but it is designed to be tolerant to other Neutron ML2 mechanism
  drivers.

/// details | VXLAN and GRE management
    type: note
When utilising another ML2 mechanism driver to provision these networks, make sure to create the relevant `VNET` or `BridgeDomain` and `VLAN`
resources in EDA, as the plugin will not automatically take care of those. Typically, these will utilise the `untagged` VLAN to communicate between
the nodes.

///

The OpenStack plugin also supports the following virtualization types:

* VIRTIO
* SR-IOV
* DPDK


### Bonding

The OpenStack plugin supports the following OpenStack supported bonding models:

* Active/Backup linuxbonds with:
    * VIRTIO
    * SR-IOV

When an Active/Backup bond is used on the compute mode, the corresponding `Interfaces` should not be configured as LAGs in EDA. 
Each physical interface in the bond should be represented as a separate `Interface` in EDA.

* Active/Active LACP OVS bonds with:
    * VIRTIO
    * SR-IOV
    * DPDK

/// details | Active/Active VIRTIO/SR-IOV support
    type: note
Active/Active for VIRTIO and SR-IOV ports is supported by the OpenStack plugin, but might not be in your deployment model.
///


When an Active/Active bond is used on the compute node, a corresponding LAG `Interface` must be configured in EDA. All physical interfaces should be
added to a single `Interface`.

### Trunking

The network trunk service allows multiple networks to be connected to an instance using a single virtual NIC (vNIC). Multiple networks can be
presented to an instance by connecting it to a single port.

For details about the configuration and operation of the network trunk service,
see https://docs.openstack.org/neutron/wallaby/admin/config-trunking.html.

Trunking is supported for VRTIO, DPDK and SR-IOV.

* For vnic_type=normal ports (VIRTIO/DPDK), trunking is supported through an upstream openvswitch trunk driver.
* For vnic_type=direct ports (SR-IOV), trunking is supported by the EDA Connect trunk driver.

/// details | Trunks with SR-IOV ports
    type: warning
Using trunks with SR-IOV has some limitations with regard to the upstream OVS trunk model:

* Both parent ports of the trunk and all subports must be created with vnic_type 'direct'.
* To avoid the need for QinQ on switches, trunks for the SR-IOV instance must be created with parent port belonging to a flat network (untagged).
* If multiple projects within a deployment must be able to use trunks, the Neutron network above must be created as shared (using the --share
  attribute).
* When adding subports to a trunk, their segmentation-type must be specified as VLAN and their segmentation-id must be equal to a segmentation-id of
  the Neutron network that the subport belongs to.
///

### Network VLAN segmentation and VLAN segregation

The OpenStack plugin only acts on VLAN Neutron networks. To use VLAN networking, configure
```provider_network_type = vlan```.

Some OpenStack deployments apply an interconnected bridge model on the OpenStack controller nodes to support multi-physnet host
interfaces and be more economical on the
physical NIC's usage. As a result, when VLAN networks with overlapping segmentation IDs across physnets are applied, care must be taken that no
overlapping segmentation IDs are wired on a host interface. Such a configuration would not be supported by the SR Linux fabric (or any other fabric).

A typical case for this to arise would be if DHCP is enabled on the subnets created on segmentation-ID overlapping networks, as the Neutron DHCP agent
on the OpenStack controller nodes would effectively end up in the described conflicting state. This can be avoided by disabling DHCP on the subnets,
that is, defining the subnet with dhcp_enable = False. Even when DHCP is not effectively consumed by any VNF deployed in the related networks, the
conflict would still occur when DHCP is enabled on the subnets.

If the deployment use cases demand this wiring (for example, some of the deployed VNFs rely on DHCP), the system's VLAN ranges must be segregated per
physical network in the neutron/ML2 configuration.


### Edge Topology Introspection

#### Automated Edge Topology Introspection

When the nic-mapping agent extension is enabled, it will persist the _physnet_ <-> _compute,interface_ relation in the Neutron database so it can wire
Neutron ports properly in the Fabric.

The known interface mappings can be consulted using the CLI command `openstack eda interface mapping list`.

#### LLDP Provisioning

LLDP must be enabled on all data plane interfaces of the controllers and computes for topology discovery. See
the [Installation Guide](openstack-plugin-installation.md) for details on configuring LLDP.

### Audit

On Highly Available (HA) Openstack deployments, if multiple audit requests are created concurrently, they might be processed concurrently by different
Neutron instances. This can lead to a situation when multiple processing instances compete to correct the same discrepancy, yielding unpredictable
results.
It is recommended to ensure no Audit exist in Connect in `InProgress` state prior to creating a new Audit request.
