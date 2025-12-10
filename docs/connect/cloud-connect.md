# Cloud Connect

## Overview

The EDA Cloud Connect solution (or "Connect") acts as a bridge between EDA and different cloud environments like Red Hat OpenShift, VMware vSphere, 
OpenStack and Nutanix.

Connect is aware of the different processes and workloads running on the servers that make up the cloud environment, while at the same time being
aware of the fabric as configured on EDA itself.

This dual awareness enables Connect to configure the fabric dynamically based on workloads coming and going on the cloud platform. It does this by
inspecting the cloud itself and learning the compute server, network interface and VLAN on which a specific workload is scheduled. By also learning
the topology based on the LLDP information arriving in the fabric switches, it connects those two information sources.

## Components

The Connect solution is built around a central service, called the Cloud Connect Core, and plugins for each supported cloud environment.

The Connect Core is responsible for managing the plugins and the relationship between `ConnectInterfaces` (compute interfaces) and EDA `Interfaces` 
(fabric interfaces or edge-links). It keeps track of the LLDP information of EDA `Interfaces` and correlates that back to the `ConnectInterfaces` 
created by plugins to identify the different physical interfaces of the computes of a cloud environment.

Connect plugins are responsible for tracking the state of compute nodes, their physical interfaces, the virtual networks created in the cloud
environment and their correlation to the physical network interfaces. As applications create networks and virtual machines or containers, the plugins
will inform Connect Core of the changes needed to the fabric. Plugins will also create or manage EDA `BridgeDomains` and `VLANs` to make sure the 
correct sub-interfaces are created for the application connectivity.

## Plugins Overview

Connect plugins are the pluggable components that connect the Connect Core service to a specific cloud environment. 
Connect comes with four Nokia supported plugins:

* Connect Nutanix plugin
* Connect OpenShift plugin
* Connect OpenStack plugin
* Connect VMware & NSX plugin

## Feature Overview

Connect supports the following features:

* Creating Layer 2 EVPN overlay services on EDA.
* Using pre-existing `Interfaces` including LAGs in the fabric.
* Automatically discovering the cloud compute resources and connectivity to the fabric using LLDP.
* Automatically resolving inconsistent states between Connect and the fabric by performing an audit between Connect and EDA.
* Using the cloud management's standard network management tools to manage the fabric transparently ([CMS Managed](#cms-managed-integration-mode)).
* Using EVPN services that are managed by EDA. This is the case in which an operator provisions a service in EDA before making them available in the
  compute environment for use. This allows for more advanced use cases than the compute environment might support natively ([EDA Managed](#eda-managed-integration-mode)).

## Installation

For detailed installation instructions, see the [Cloud Connect Core Installation Guide](cloud-connect-installation.md).

## Resources

Connect uses a pluggable architecture. The Cloud Connect core installation is a collection of controllers responsible for bridging the
hypervisor world with the fabric world. It is the plugin that is responsible for introspecting the cloud environment.

The following Custom Resources are involved:

*`ConnectPlugin`*
: The logical representation of the plugin, created for each plugin automatically when the plugin starts with valid credentials.

*`ConnectPluginActionable`*
: An actionable is an action to be taken by the `ConnectPlugin`. It is used by the Core to tell the plugin to do something (for example: initiate an
audit).

*`ConnectPluginHeartbeat`*
: The `ConnectPlugin` will continuously send heartbeats to the Cloud Connect service to report its status and alarms.

*`ConnectInterface`*
: The logical representation of a hypervisor NIC and/or LAG. The labels on the `ConnectInterface` are used to label the EDA interface (leaf interface)
correctly so that the correct subinterfaces are created.

### Plugins

Plugins are a core component of the Event Driven Automation (EDA) Connect environment. In the Connect environment, a plugin represents the component
that communicates with the external cloud services. The following plugins are supported by EDA, and are further documented in their respective
sections:

* [Nutanix Connect plugin](./nutanix-plugin.md)
* [OpenStack Connect plugin](./openstack-plugin.md)
* [OpenShift Connect plugin](kubernetes-plugin.md)
* [VMware vSphere plugin](./vmware-plugin.md)
* [VMware NSX plugin](./vmware-nsx.md)

Plugins are automatically registered within the Connect service when they are deployed. Each is stored in the database with the following main
properties:

*`Name`*
: A unique name based on the plugin type and compute environment it is connected to.

*`Plugin Type`*
: The type of plugin, for example, VMware or OpenShift.

*`Heartbeat Interval`*
: The interval, in seconds, between heartbeats that the plugin intends to use.

*`Supported Actions`*
: The different actions a plugin can support. These are actions the Core can request the plugin to do. For example, to trigger an audit.

### Heartbeats

When plugins register with the Connect core service, they can indicate that they support heartbeats. When a plugin supports heartbeats, the plugin is
expected to send a heartbeat to the Connect core service at an interval of the configured value (or more frequently). If the Connect core does not
receive a heartbeat from the plugin after two intervals, it raises an alarm in EDA to indicate that there could be an issue with the plugin.

### Connect Interfaces

`ConnectInterfaces` are managed by the plugins and represent the network interfaces of a compute node. When a plugin notices a new compute or new
network interface on a compute node, it will create a `ConnectInterface` in EDA for Connect Core to monitor.

Connect Core uses the information from the `ConnectInterface` to determine the matching EDA `Interface`. This is the interface on a leaf managed by EDA
to which the interface on the compute node is connected with potentially multiple interfaces, in case of a LAG or bond.

The plugin will label these `ConnectInterfaces` to indicate that Connect Core needs to make sure the matching leaf interfaces have a subinterface
created in the corresponding overlay service or `BridgeDomain`.

This way, only those subinterfaces that are truly necessary are configured in the fabric. This limits configuration bloat and possible security risks.

## Namespace Support

The EDA Connect service supports multiple namespaces. Each plugin is namespaced and can only access resources within its namespace.

This also means that a compute cluster can only belong to a single namespace, and cannot span multiple namespaces. This is to be expected, as compute
clusters belong to a single fabric, and a fabric is part of a single namespace.

## Connect UI

The Connect UI can be found as part of the System Administrator section of the EDA UI, and allows for inspection of the different resources owned and
managed by Connect. This Connect UI follows the same design as the regular EDA UI, where the left menu for Connect opens and displays the different
resources available.

/// details | Do not edit resources manually, as this could interfere with the behavior of the plugins.
    type: warning

If you have made changes manually, an audit will revert them.
Changes should be made through the Cloud orchestration platform. When trying to perform changes through the UI a lock will be displayed, indicating 
that the resource is managed by Connect.
///

## Connect Integration Modes

Integration modes define how plugins create resources in EDA for use by the applications in the compute environments.

Connect supports two integration modes:

*CMS-managed mode*
: Networking concepts of the CMS (Cloud Management System) are used to create new services in EDA.

*EDA-managed mode*
: Network services are created in EDA and the networking concepts in the CMS are linked or associated with these pre-existing services.

Each of these modes can be used by the plugins. For the plugins provided by Nokia, both modes are supported, and you can combine them and switch
between them as needed. For instance, you can use one integration mode for one application, while using the other for another application.

### CMS-Managed Integration Mode

In the Cloud Management mode, Connect creates a `BridgeDomain` resource for each subnet that is created in the Cloud Management System (CMS).
In this mode, the
changes in the CMS are transparently reflected into EDA. The administrator of the CMS does not require any
knowledge about how to use EDA.

### EDA-Managed Integration Mode

For more advanced use cases, a more complex EVPN service (or set of services) may be needed. This can include features of these services that are
supported by EDA, but not natively by the CMS. Examples are configuring complex routing or QoS policies, or using BGP PE/CE for route advertisement
from the application into the network service.

In such cases, Nokia recommends using the EDA-managed integration mode, which instructs Connect to associate the subnets in the CMS with existing
BridgeDomains in EDA, instead of creating new resources in EDA based on the cloud management networking.

In this mode, an administrator, or orchestration engine, with knowledge of EDA first creates the necessary resources in EDA directly. You can create
more complex configurations than the cloud management system itself would be able to do. When creating the networking constructs in the Cloud
Management system, you provide a set of unique identifiers referring to those pre-created `BridgeDomain` constructs. This way, the Connect plugin and
Connect service know not to create their own resources, but to use the pre-created items.

/// details | `VLAN` management
    type: subtle-note

In EDA-managed mode, Connect will still create the necessary `VLAN` resources in EDA as needed, based on the VLANs used in the CMS.
///
## LLDP

To bridge EDA with the cloud environment, Cloud Connect uses LLDP extensively. The LLDP information is collected at the fabric level and streamed to
EDA.
There is also support for reversing that LLDP relationship, by having the computes collect the LLDP information.

* Nutanix Plugin: LLDP collected at fabric level
* OpenStack Plugin: LLDP collected at fabric level
* OpenShift Plugin: LLDP collected at hypervisor level
* VMware plugin: LLDP collected at fabric level

When LLDP is collected at the fabric level, it is advised to disable in-hardware LLDP to prevent those LLDP messages from interfering with the ones
that the host operating system is sending out.[^1][^2]

[^1]: Instructions on how to disable in-hardware LLDP for Mellanox cards can be found
here: https://forums.developer.nvidia.com/t/need-help-disabling-hardware-lldp-c5x-ex/294083

[^2]: Instructions on how to disable in-hardware LLDP in VMware ESXI
environments: https://knowledge.broadcom.com/external/article/344761/enabling-and-disabling-native-drivers-in.html

### LLDP gracetimer

To prevent unnecessary fabric reconfiguration due to temporary LLDP data loss, a grace period is applied when LLDP information is collected at the
fabric level. During this grace period, Connect Core will not reconfigure the fabric, allowing time for LLDP data to recover. The grace period is not
applicable when LLDP data is collected at the hypervisor level.
The gracetimer can be configured when installing Connect using the `interfaceControllerGraceTimer` setting; the default is 10 seconds.

# Support Matrix

In the table below you can find the qualified matrix for the Cloud Connect service.

## 25.12

| Component                 | Release       | Supported Versions (Cloud Type) | EDA Core Version             |
|---------------------------|---------------|---------------------------------|------------------------------|
| **OpenShift**             | 5.0.x         | OpenShift 4.16, 4.18, 4.20      | v4.0.0 (EDA release 25.12.x) |
| **VMware vCenter**        | v5.0.x        | VMware vCenter 8.X              | v4.0.0 (EDA release 25.12.x) |
| **VMware NSX**            | v5.0.x        | VMware NSX 4.2.X                | v4.0.0 (EDA release 25.12.x) |
| **Nutanix Prism Central** | v0.0.x (Beta) | Nutanix Prism Central 7.3.X     | v4.0.0 (EDA release 25.12.x) |
