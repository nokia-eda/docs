# Nutanix Prism Central Plugin

//// warning | Technical Preview

The Nutanix Prism Central Plugin is currently only available as beta version for technical preview purposes. It can be used for demo, POC or lab
purposes.

The following features are **not** included in the technical preview:

* SR-IOV support
* NIC Offloading
* Audit
* Alarms
* Heartbeats

////

## Overview

The Nutanix Prism Central plugin integrates Nokia EDA with Nutanix Prism Central, enabling automated network provisioning and management for Nutanix
environments. It supports both VLAN Basic and Advanced Networking subnets, and provides seamless connectivity between Nutanix-managed workloads and
the EDA fabric.

Key capabilities include:

* Direct integration with Nutanix Prism Central through its v4 rest API
* Automatic provisioning of the fabric based on Nutanix virtual switch and subnet configuration
* Support for VLAN Basic and Advanced Networking subnets
* Support for VPC breakout subnets (VLAN-based)
* Basic workflows managed completely through Prism Central ([Prism Managed Mode](#operational-modes))
* Advanced workflows managed through EDA ([EDA Managed Mode](#operational-modes))
* Interconnectivity between different cloud environments through EDA

### Supported Versions

* Nutanix Prism Central 7.3


## Architecture

The Nutanix Prism Central plugin consists of two components:

*__Nutanix Prism Central Plugin App__*
: Manages the lifecycle of Nutanix plugin instances in EDA using a custom resource definition (CRD).

*__Nutanix Prism Central Plugin__*
: Connects to Prism Central, monitors configuration changes, and synchronizes state with EDA. The plugin listens for events on:

    * Virtual switches
    * Subnets (VLAN Basic and VLAN Advanced)
    * Host NIC to virtual switch associations
    * Categories (for EDA-managed mode)

## Installation

For detailed deployment instructions, see the [Nutanix Prism Central Plugin Installation Guide](nutanix-plugin-installation.md).

## Features

### Limitations

* VM NICs in Trunked mode are not supported
* Audit functionality is not supported in the technical preview
* Heartbeats are not supported in the technical preview
* SR-IOV and NIC offloading are not supported in the technical preview

### Operational Modes

The plugin supports two operational modes for managing VLAN subnets, selectable on a per-subnet basis:

*__Prism Central-Managed Mode__*
: This is the default mode. Each VLAN subnet in Prism Central results in a unique `BridgeDomain` in EDA. The VLAN in Prism Central determines the `VLANs`
managed for the `BridgeDomain`. If multiple subnets use the same VLAN on the same virtual switch, only a single `BridgeDomain` will be provisioned.
The `BridgeDomain` is not routable through the fabric in this mode. 
If routing is required, EDA managed mode can be used, or external routing can be provisioned in the subnet.

*__EDA-Managed Mode__*
: Subnets can be associated with an existing EDA `BridgeDomain` by attaching the `connect.eda.nokia.com` category with key `EDA Managed` to the subnet
in Prism Central. The name of the subnet must match the name of the EDA `BridgeDomain`.

Alternatively, subnets can be excluded from EDA management by attaching the `connect.eda.nokia.com` category with key `EDA Ignored`. An example use
case for this is the initial infrastructure network hosting the CVM and Prism Central VMs.

#### Using EDA-Managed Mode

The plugin automatically creates the `connect.eda.nokia.com` category in Prism Central on startup if it does not exist. It also ensures that the two
standard values, `EDA Managed` and `EDA Ignored`, are present for this category.

To use EDA-managed mode:

1. Create a `BridgeDomain` in EDA with the desired settings. This can be a `BridgeDomain` in a `VirtualNetwork` as well as a standalone `BridgeDomain`.
2. In Prism Central, attach the `connect.eda.nokia.com` category to the subnet and set its value to `EDA Managed`. The name of the subnet must match
   the name of the EDA `BridgeDomain`.

/// details | BridgeDomain not found
    type: warning

If the referenced `BridgeDomain` does not exist in EDA, the plugin raises an alarm and no connectivity can be provided for the subnet. If the
BridgeDomain is created later, the plugin will automatically reconcile and establish connectivity.
///

/// details | Multiple values for connect.eda.nokia.com Category
    type: subtle-note

If multiple values for the `connect.eda.nokia.com` category are associated with a single subnet, EDA-Ignored will get precedence.

///

/// details | Category configuration in Prism Central
    type: subtle-note

Categories can be assigned to subnets in Prism Central via the UI or API. An example configuration using the UI is shown below:
![Category configuration in Prism Central](resources/nutanix-category-example.png)
///

You can switch between EDA-managed and Prism-managed mode at any time.

/// details | Switching between EDA-managed and Prism-managed mode
    type: subtle-note

When switching between the two available modes, connectivity will be temporarily disrupted while the plugin reconfigures the resources in EDA.
///

#### VPC Overlay Subnets

Subnets created in a VPC are overlay (Geneve-based) and are not visible to the EDA fabric. Only breakout subnets (VLAN-based) can be managed by EDA.

### Virtual Switch Modes

A Nutanix virtual switch can operate in several modes:

* __Active-Backup__: Each uplink is represented as a separate `ConnectInterface`.
* __Active-Active with MAC pinning__: A single `ConnectInterface` is created for all uplinks, mapped to a static LAG interface in EDA.
* __Active-Active with LACP__: A single `ConnectInterface` is created for all uplinks, mapped to an LACP interface in EDA.

The plugin provisions the correct `ConnectInterface` objects based on the virtual switch mode. The corresponding Interface objects in EDA must be
created before installing the plugin.

/// details | Unsupported virtual switch modes in the technical preview
    type: warning

In the technical preview, only the Active-Backup mode is supported. Active-Active modes with MAC pinning or LACP are not supported.
///

### Event Monitoring

The plugin subscribes to events in Prism Central and configures EDA resources accordingly:

| **Event Trigger**                     | Custom Resource    | Purpose                                                                  |
|---------------------------------------|--------------------|--------------------------------------------------------------------------|
| VLAN Subnet events                    | `BridgeDomain`     | Each VLAN subnet results in a unique `BridgeDomain` (Prism Central mode) |
| VLAN Subnet events                    | `VLAN`             | Each VLAN subnet creates a `VLAN` resource for attachment to the BD      |
| Host NIC virtual switch uplink events | `ConnectInterface` | Each host NIC uplink creates a `ConnectInterface`                        |

### Audit

The plugin performs an audit on startup and when requested by the operator to ensure synchronization between Prism Central and EDA. Any discrepancies are resolved automatically. See also the [audit documentation](./audit.md).

[//]: # (### Operator Initiated Audit)

[//]: # ()
[//]: # (In addition to the startup audit, users can initiate an [audit]&#40;./audit.md&#41; manually. The audit object contains the status and results, including any discrepancies found between Nutanix and Connect.)

### Startup

* The plugin instance has registered itself with Connect using the provided `metadata.name` as the `ConnectPlugin` `metadata.name`.
* The plugin checks connectivity with Prism Central and validates the provided credentials.
* The plugin performs an audit to synchronize initial state between Prism Central and EDA.
* The plugin creates the `connect.eda.nokia.com` category in Prism Central if it does not exist.

//// details | Wrong credentials
    type: warning

If the provided credentials are invalid, the plugin raises an alarm and will not retry any calls to Prism Central.
In the technical preview, the authSecretRef has to be corrected and the Deployment has to be restarted manually.

////

## Troubleshooting

### The plugin is not running

* Check plugin alarms in EDA.
* Verify connectivity from the EDA cluster to Prism Central.
* Check credentials in the Kubernetes Secret.
* Check the plugin pod logs in the `eda-system` namespace in Kubernetes.

### The plugin is not creating resources in EDA

* Check plugin alarms in EDA.
* Verify connectivity from the EDA cluster to Prism Central.
* Check the plugin pod logs in the `eda-system` namespace in Kubernetes.
* Check the staleness state of the plugin object in EDA.

### The plugin is not configuring the correct state

* Check plugin alarms in EDA.
* Verify uplink configuration for vswitches in Prism Central.
* VLAN ranges are not supported on subnets.
* Inspect EDA resources (`VLAN`, `BridgeDomain`, `ConnectInterface`).
* Check the plugin pod logs.
