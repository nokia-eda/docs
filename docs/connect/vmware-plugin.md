
# VMware vSphere Plugin

## Overview

The VMware vSphere Plugin leverages the VMware vSphere distributed vSwitch architecture to support managing the fabric directly from VMware vCenter and make the fabric respond to the networking needs of the environment.

It provides the following advantages and capabilities:

* Direct integration into the network management workflow of VMware vCenter.
* The use of the common distributed vSwitches and Port Groups for both regular Virtual Machine NICs as well as SR-IOV use cases.
* VMware plugin supports the following VLAN types for Port Groups.
    * None: Vlan 0
    * VLAN: <vlan-id> (1-4094)
* Automatic provisioning of the fabric based on where the Virtual Machines need the connectivity.
* Support advanced workflows through the Fabric Service System Managed solution, including for VNF use cases with features like QoS, ACLs, and BGP PE-CE.
* Interconnectivity between different cloud environments, allowing for flexible network configurations.

### Supported Versions

* VMware vSphere 7
* VMware vSphere 8

## Prerequisites

Before installing or deploying the VMware vSphere Plugin components, make sure that the Cloud Connect Core application is properly installed in the cluster.

## Architecture

The VMware vSphere Plugin consists of two components:

*VMware vSphere Plugin App*
: This app runs in EDA and manages the lifecycle of the VMware vSphere Plugins. It does so in the standard app model where a custom resource is used to manage the VMware vSphere Plugins.

*VMware vSphere Plugin*
: The Plugin itself which is responsible for connecting and monitoring the VMware vCenter environment for changes. The Plugin will listen to the events of the following objects:

    * Distributed vSwitch (dvS)
    * Distributed Port Groups (dvPG)
    * Host to dvS associations
    * Custom Attributes

### Supported Features

The following are some of the supported VMware vSphere features:

* CMS-managed integration mode
* EDA-managed integration mode
* Optimally configure subinterfaces to minimize configuration and security footprint of network services
* LAG/LACP interfaces
* SRIOV interfaces
* Audits

## Deployment

To deploy the VMware vSphere plugin, complete the following tasks:

* Deploy the plugin app.
* Deploy the plugin.

### Connect VMware vSphere Plugin App Deployment

The VMware vSphere Plugin App is an Application in the EDA App eco-system. It can be easily installed using the App Store UI.

#### Installation using Kubernetes API

If you prefer installing the Connect Core using the Kubernetes API, you can do so by creating the following Workflow resource:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/vmware-appinstall.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/vmware-appinstall.yaml"
EOF
```

///

### Connect VMware vSphere Plugin Deployment

A prerequisite for creating a `vmwarePluginInstance` resource is a `Secret with username and password fields that contain the account information for an account that can connect to the VMware vCenter environment and has read-only access to the cluster so that it can monitor the necessary resources.

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/vmware-secret.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/vmware-secret.yaml"
EOF
```

///

As the VMware vSphere Plugins are managed through the operator, you can use the EDA UI to create a new `VmwarePluginInstance` resource under the **System Administration > Connect > VMware Plugins** menu item.

As an alternative, you can also create the same `VmwarePluginInstance` using the following custom resource example. Make sure to replace the specified values with their relevant content.

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/vmware-plugin-instance.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/vmware-plugin-instance.yaml"
EOF
```

///

The plugin name and external ID must comply with the regex check of `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'` and can only contain alpha-numerical characters and `.`, `_` and `-`. It must start with an alpha-numerical character.

## Functionality

This section describes VMware vSphere plugin operations including startup, event monitoring, and the plugin's operational modes.

### Startup

When the plugin is started, the following actions are taken by the plugin:

* The plugin registers itself with Connect, based on the provided `externalID`. If a matching `ConnectPlugin` pre-exists, it is reused.
* The plugin performs an audit: Any Connect-related state that was programmed in vCenter while the plugin was not running is synchronized with Connect.

### Event Monitoring

A plugin will connect to a VMware vCenter environment and subscribe to VMware events. The plugin will configure Connect and EDA based on the events it receives:

| **Event Trigger**                         | Custom Resource    | Purpose                                                                                                                                                     |
| ----------------------------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VLAN-tagged distributed PortGroup events  | `BridgeDomain`     | In VMware Managed mode, each dvPG will result in its own unique `BridgeDomain`                                                                              |
| VLAN-tagged distributed PortGroup events  | `VLAN`             | Each dvPG with a specific VLAN tag will have an EDA `VLAN` resource so it can be attached to the `BridgeDomain`                                             |
| Host NIC distributed Switch Uplink events | `ConnectInterface` | Each Host NIC that gets added as an Uplink to a dvS, will trigger the creation of a `ConnectInterface` which is mapped by Connect Core to a EDA `Interface` |

!!! Note "Naming limitations"
    The uplink names must comply with the regex check of `^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]$`. It can only contain alpha-numerical characters and ` `(space), `.`, `_`, and `-`. It must also have a length of 64 characters or less.

### Operational Modes

The plugin supports the following Operational Modes, these modes can be used simultaneously.

*VMware Managed Mode*
: Also referred to as *Connect Managed*. When using this mode, the plugin will create a unique `BridgeDomain` for each VLAN tagged dvPG in the VMware vCenter environment.

*EDA Managed Mode*
: In EDA Managed Mode, a dvPG is given a special custom attribute that refers to an existing EDA `BridgeDomain`. When the plugin detects this custom attribute, and it refers to an existing `BridgeDomain` in EDA, it will not create a new `BridgeDomain` but instead will associate the dvPG with the existing one. This allows for more advanced configuration of the application networks.

#### Using EDA Managed Mode

To use the EDA Managed Mode follow these steps:

1. Create a `BridgeDomain` in EDA with the desired settings
2. When creating a distributed PortGroup in vCenter, configure a Custom Attribute called `ConnectBridgeDomain` and set its value to the key of the EDA `BridgeDomain`.

!!! Note "Both the key of the Custom Attribute and the value are case sensitive"

You can configure multiple dvPGs with the same `BridgeDomain`.

It is also supported to switch between EDA Managed and VMware Managed at any time. You can switch back to VMware Managed by setting the `ConnectBridgeDomain` Custom Attribute to `none`, or by deleting the Custom Attribute entirely.

## Troubleshooting

### The plugin is not running

If an incorrect vCenter hostname or IP is configured in the `VmwarePluginInstance` resource, the plugin will try to connect for 3 minutes and crash/restart if it fails to connect. In case the credentials are incorrect, the plugin will crash/restart immediately.

* Check the raised plugin alarms.
* Check the connectivity from the EDA cluster to vCenter.
* Verify the credentials for vCenter.
* Ensure the heartbeat interval is a positive integer.
* Check the logs of the plugin pod.

### The plugin is not creating any resources in EDA

* Check the raised plugin alarms.
* Check the connectivity from the EDA cluster to vCenter.
* Check the logs of the plugin pod.
* Check the Plugin staleness state field and verify heartbeats are being updated.

### The plugin is not configuring the correct state

* Check the raised plugin alarms.
* Verify the Uplinks for the dvPG in vCenter are configured as active or standby. If there are no active or standby Uplinks configured, the plugin will not associate any `ConnectInterface` with the `VLAN`.
* Uplink names can only contain alpha-numerical characters and `.`, `_`, `-` and must have a length of 64 characters or less.
* VLAN Ranges are not supported on dvPGs.
* Inspect the EDA resources, like `VLAN`, `BridgeDomain` and `ConnectInterface`.
* Check the logs of the plugin pod.
