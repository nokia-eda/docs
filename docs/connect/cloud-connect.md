# Cloud Connect

## Overview

The EDA Cloud Connect solution (or "Connect") acts as a bridge between EDA and different cloud environments like Red Hat OpenShift, VMware vSphere and
others.

Connect is aware of the different processes and workloads running on the servers that make up the cloud environment, while at the same time being
aware of the fabric as configured on EDA itself.

This dual awareness enables Connect to configure the fabric dynamically based on workloads coming and going on the cloud platform. It does this by
inspecting the cloud itself and learning the compute server, network interface and VLAN on which a specific workload is scheduled. By also learning
the topology based on the LLDP information arriving in the fabric switches, it connects those two information sources.

## Components

The Connect solution is built around a central service, called the Cloud Connect Core, and plugins for each supported cloud environment.

The Connect Core is responsible for managing the plugins and the relation between Connect Interfaces (compute interfaces) and EDA Interfaces (Fabric
Interfaces or Edge-Links). It keeps track of the LLDP information of EDA Interfaces and correlates that back to the Connect Interfaces created by
Plugins to identify the different physical interfaces of the computes of a cloud environment.

Connect Plugins are responsible for tracking the state of compute nodes, their physical interfaces, the virtual networks created in the cloud
environment and their correlation to the physical network interfaces. As applications create networks and virtual machines or containers, the plugins
will inform Connect Core of the changes needed to the fabric. Plugins will also create or manage EDA BridgeDomains to make sure the correct
sub-interfaces are created for the application connectivity.


## Plugins Overview

Connect plugins are specifically made to inspect one type of cloud environment. While these plugins can be developed specifically targeting a custom
cloud environment, Connect comes with three Nokia supported plugins:

* Connect OpenShift plugin
* Connect VMware plugin
* Connect OpenStack ML2 plugin (CBIS only)

## Feature Overview

Connect supports the following features:

* Creating Layer 2 EVPN Overlay Services on EDA.
* Automatically discovering the cloud compute resources and connectivity to the fabric using LLDP.
* Automatically resolving inconsistent states between Connect and the fabric by performing an audit between Connect and EDA.
* Using pre-existing LAGs in the fabric.
* Using the cloud management's standard network management tools to manage the fabric transparently.
* Using EVPN services that are managed by EDA. This is the case in which an operator provisions a service in EDA before making them available in the
  compute environment for use. This allows for more advanced use cases than the compute environment might support natively.

## Installation of Cloud Connect Core

Cloud Connect is an Application in the EDA App ecosystem. It can be easily installed using the EDA Store UI.

### Installation using Kubernetes API

If you prefer installing the Connect Core using the Kubernetes API, you can do so by creating the following Workflow resource:

/// details | Connect Core dependencies

When installing through the UI dependencies are automatically resolved, this is not the case through the API. Make sure all dependencies of the Connect Core app are installed before executing the below kubectl command.

When the dependencies are not satisfied, an error like the following will be added to the status of the AppInstaller object: 

```app requirements validation failed: connect.nokia requires interfaces.nokia, but interfaces.nokia is not present```

///

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/connect-appinstall.yaml"
```

///
/// tab | `kubectl apply` command"

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/connect-appinstall.yaml"
EOF
```

///

### Plugin Configuration Options

When installing Cloud Connect via the EDA UI, users are prompted to configure the application using the following options. These settings control resource limits and behavior of the Connect controllers:

| Configuration Option | Description | Default Value |
|----------------------|-------------|----------------|
| **Interface Controller GraceTimer** (`interfaceControllerGraceTimer`) | The grace period (in seconds) used by the Interface Controller before acting on missing LLDP data. | `10` |
| **Interface Controller Pod CPU Limit** (`interfaceControllerCpuLimit`) | CPU limit for the connect-interface-controller pod. | `1` |
| **Interface Controller Pod Memory Limit** (`interfaceControllerMemoryLimit`) | Memory limit for the connect-interface-controller pod. | `2Gi` |
| **Plugin Controller Pod CPU Limit** (`pluginControllerCpuLimit`) | CPU limit for the connect-plugin-controller pod. | `500m` |
| **Plugin Controller Pod Memory Limit** (`pluginControllerMemoryLimit`) | Memory limit for the connect-plugin-controller pod. | `128Mi` |

These options can be adjusted during installation to meet specific performance or resource requirements.

/// details | Settings are an advanced use case
    type: warning

These settings are intended for advanced users. Misconfiguration can lead to system instability or failure. Proceed with caution and ensure changes are validated in a test environment before applying them to production.
///


## Resources

Connect uses a pluggable architecture. The Cloud Connect core installation is a collection of controllers responsible for bridging the
hypervisor world with the fabric world. It is the plugin that is responsible for introspecting the cloud environment.

The following Custom Resources are involved:

*ConnectPlugin*
: The logical representation of the plugin, created for each plugin automatically when the plugin starts with valid credentials.

*ConnectPluginActionable*
: An actionable is an action to be taken by the `ConnectPlugin`. It is used by the Core to tell the plugin to do something (for example: initiate an
Audit).

*ConnectPluginHeartbeat*
: The `ConnectPlugin` will continuously send heartbeats to the Cloud Connect service to report its status and alarms.

*ConnectInterface*
: The logical representation of a hypervisor NIC and/or LAG. The labels on the `ConnectInterface` are used to label the EDA interface (leaf interface)
correctly so that the correct subinterfaces are created.

### Plugins

Plugins are a core component of the Event Driven Automation (EDA) Connect environment. In the Connect environment, a plugin represents the component
that communicates with the external cloud services. The following plugins are supported by EDA, and are further documented in their respective
sections:

* [OpenShift Connect plugin](./openshift-plugin.md)
* [VMware vSphere plugin](./vmware-plugin.md)
* [OpenStack ML2 plugin](./openstack-plugin.md)

Plugins are automatically registered within the Connect service when they are deployed. Each is stored in the database with the following main
properties:

*Name*
: A unique name based on the plugin type and compute environment it is connected to.

*Plugin Type*
: The type of plugin, for example, VMware or OpenShift.

*Heartbeat Interval*
: The interval, in seconds, between heartbeats that the plugin intends to use.

*Supported Actions*
: The different actions a plugin can support. These are actions the Core can request the plugin to do. For example, to trigger an Audit.

### Heartbeats

When plugins register with the Connect core service, they can indicate that they support heartbeats. When a plugin supports heartbeats, the plugin is
expected to send a heartbeat to the Connect core service at an interval of the configured value (or more frequently). If the Connect core does not
receive a heartbeat from the plugin after two intervals, it raises an alarm in EDA to indicate that there could be an issue with the plugin.

### Connect Interfaces

Connect interfaces are managed by the plugins and represent the network interfaces of a compute node. When a plugin notices a new compute or new
network interface on a compute node, it will create a Connect interface in EDA for Connect Core to monitor.

Connect Core uses the information from the Connect interface to determine the matching EDA interface. This is the interface on a leaf managed by EDA
to which the interface on the compute is connected to, or potentially multiple interfaces in case of a LAG or Bond.

The plugin will label these Connect interfaces to indicate that Connect Core needs to make sure the matching leaf interfaces have a subinterface
created in the corresponding overlay service (BridgeDomain).

This way, only those subinterfaces that are truly necessary are configured in the fabric. This limits configuration bloat and possible security risks.

## Namespace support

The EDA Connect service supports multiple namespaces. Each plugin is namespaced and can only access resources within its namespace.

This also means that a compute cluster can only belong to a single namespace, and cannot span multiple namespaces. This is to be expected as compute
clusters belong to a single fabric, and a fabric is part of a single namespace.

## Connect UI

The Connect UI can be found as part of the System Administrator section of the EDA UI, and allows for inspection of the different resources owned and
managed by Connect. This Connect UI follows the same design as the regular EDA UI, where the left menu for Connect opens and displays the different
resources available.

/// details | Do not create new resources manually, as this could interfere with the behavior of the plugins.
    type: warning

If you have made changes manually, an audit will revert them.
Changes should be made through the Cloud orchestration platform.
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

In the Cloud Management mode, Connect creates an EDA BridgeDomain for each subnet that is created in the Cloud Management system. In this mode, the
changes in the Cloud Management system are transparently reflected into EDA. The administrator of the Cloud Management system does not require any
knowledge about how to use EDA.

### EDA-Managed Integration Mode

For more advanced use cases, a more complex EVPN Service (or set of services) may be needed. This can include features of these services that are
supported by EDA, but not natively by the CMS. Examples are configuring complex routing or QoS policies, or using BGP PE/CE for route advertisement
from the application into the network service.

In such cases, Nokia recommends using the EDA-managed integration mode, which instructs Connect to associate the subnets in the CMS with existing
BridgeDomains in EDA, instead of creating new resources in EDA based on the cloud management networking.

In this mode, an administrator (or orchestration engine) with knowledge of EDA first creates the necessary resources in EDA directly. You can create
more complex configurations than the cloud management system itself would be able to do. When creating the networking constructs in the Cloud
Management system, you provide a set of unique identifiers referring to those pre-created networking constructs. This way, the Connect plugin and
Connect service know not to create their own resources, but to use the pre-created items.

## LLDP

To bridge EDA with the cloud environment, Cloud Connect uses LLDP extensively. The LLDP information is collected at the fabric level and streamed to
EDA.
There is also support for reversing that LLDP relationship, by having the computes collect the LLDP information.

- OpenShift Plugin: LLDP collected at hypervisor level
- OpenStack Plugin: LLDP collected at fabric level
- VMware plugin: LLDP collected at fabric level

When LLDP is collected at the fabric level, it is advised to disable in-hardware LLDP to prevent those LLDP messages from interfering with the ones
that the host operating system is sending out.[^1]

[^1]: Instructions on how to disable in-hardware LLDP for Mellanox cards can be found here: https://forums.developer.nvidia.com/t/need-help-disabling-hardware-lldp-c5x-ex/294083

### LLDP gracetimer


To prevent unnecessary fabric reconfiguration due to temporary LLDP data loss, a gracetimer is applied when LLDP information is collected at the fabric level. During this grace period, Connect Core will not reconfigure the fabric, allowing time for LLDP data to recover. The gracetimer is not applicable when LLDP data is collected at hypervisor level.
The gracetimer can be configured when installing Connect using the _interfaceControllerGraceTimer_ setting, the default is 10 seconds.

