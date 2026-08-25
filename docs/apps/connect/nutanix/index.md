# Nutanix Prism Central Plugin

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
* Advanced use cases managed through EDA ([EDA Managed Mode](#operational-modes))
* Interconnectivity between different cloud environments through EDA

Currently not supported:

* SR-IOV
* NIC Offloading

### Supported Versions

* Nutanix Prism Central 7.3
* Nutanix Prism Central 7.5


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

For detailed deployment instructions, see the [Nutanix Prism Central Plugin Installation Guide](installation.md).

## Features

### Limitations

* VM NICs in Trunked mode are not supported
* SR-IOV and NIC offloading are not supported

### Operational Modes

The plugin supports two operational modes for managing VLAN subnets, selectable on a per-subnet basis:

*__Prism Central-Managed Mode__*
: This is the default mode. Each VLAN subnet in Prism Central results in a unique `BridgeDomain` in EDA. The VLAN in Prism Central determines the `VLANs`
managed for the `BridgeDomain`. If multiple subnets use the same VLAN on the same virtual switch, only a single `BridgeDomain` will be provisioned.
The `BridgeDomain` is not routable through the fabric in this mode. 
If routing is required, EDA managed mode can be used, or external routing can be provisioned in the subnet.

*__EDA-Managed Mode__*
: Subnets can be associated with an existing EDA `BridgeDomain` from Prism Central or from EDA. In Prism Central, attach the
`connect.eda.nokia.com` category with key `EDA Managed` to the subnet. The name of the subnet must match the name of the EDA `BridgeDomain`.
In EDA, create a `NutanixEDAManagedBridgeDomain` custom resource.

Alternatively, subnets can be excluded from EDA management by attaching the `connect.eda.nokia.com` category with key `EDA Ignored`. An example use
case for this is the initial infrastructure network hosting the CVM and Prism Central VMs.

#### Using EDA-Managed Mode

EDA-Managed mode can be configured through two different methods:

1. Using a Prism Central category
2. Using the `NutanixEDAManagedBridgeDomain` custom resource

#### Using a Prism Central category

The plugin automatically creates the `connect.eda.nokia.com` category in Prism Central on startup if it does not exist. It also ensures that the two
standard values, `EDA Managed` and `EDA Ignored`, are present for this category.

To use EDA-managed mode through a category:

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

If multiple values for the `connect.eda.nokia.com` category are associated with a single subnet, `EDA Ignored` will get precedence.

///

/// details | Category configuration in Prism Central
    type: subtle-note

Categories can be assigned to subnets in Prism Central via the UI or API. An example configuration using the UI is shown below:
-{{image(url="../resources/nutanix-category-example.webp", title="Category configuration in Prism Central")}}-
///


/// details | Switching between EDA-managed and Prism-managed mode
    type: subtle-note
You can switch between EDA-managed and Prism-managed mode at any time.
When switching between the two available modes, connectivity will be temporarily disrupted while the plugin reconfigures the resources in EDA.
///

#### Using the NutanixEDAManagedBridgeDomain custom resource

To use the EDA-managed mode through the `NutanixEDAManagedBridgeDomain` custom resource follow these steps:

1. Create a `BridgeDomain` in EDA with the desired settings
2. Create the virtual switch and/or VLAN subnet in Prism Central
3. Create a `NutanixEDAManagedBridgeDomain` custom resource in EDA referring to the `BridgeDomain`, virtual switch, and
   subnet.

In the Nokia EDA UI, autocomplete functionality allows you to select the Prism Central subnet automatically with a
dropdown menu.

/// note | Subnet ID
Set the Subnet ID to the Nutanix `externalId` field. The autocomplete functionality will help you
in mapping Subnet ID to human-readable values as well.
///

/// tab | Autocomplete

-{{image(
    light_url="../resources/nutanix-eda-mgd-from-eda-light.webp",
    dark_url="../resources/nutanix-eda-mgd-from-eda-dark.webp",
    padding=20,shadow=true,
    title="In the Nokia EDA UI, autocomplete functionality allows you to select the Prism Central subnet automatically with a dropdown menu."
)}}-

///
/// tab | Select Subnet ID

-{{image(
    light_url="../resources/nutanix-select-subnet-id-light.webp",
    dark_url="../resources/nutanix-select-subnet-id-dark.webp",
    padding=20,shadow=true,
    title="Use the table icon on the right to select the Subnet ID from a table with the human-readable name."
)}}-

///


When both a Prism Central category and a `NutanixEDAManagedBridgeDomain` are defined for the same subnet, the `NutanixEDAManagedBridgeDomain` takes precedence.

#### Restricting Operational Modes

The plugin configuration allows you to restrict the operational modes that are allowed. By default, both modes are allowed (`Unrestricted`). You can restrict the modes to only allow Prism Central-managed mode by setting the `OperationalMode` to `ConnectManagedOnly`. You can restrict the modes to only allow EDA-managed mode by setting the `OperationalMode` to `EDAManagedOnly`.

/// details | Restricting Operational Modes during operation
    type: info

If you restrict the operational modes, an audit runs. The audit removes resources that the new mode does not allow, and it adds resources that the new mode allows.
///

#### VPC Overlay Subnets

Subnets created in a VPC are overlay (Geneve-based) and are not visible to the EDA fabric. Only breakout subnets (VLAN-based) can be managed by EDA.
EDA will correctly manage the connectivity for the transport subnets, used to carry the overlay subnet traffic between the hypervisors.


### Virtual Switch Modes

A Nutanix virtual switch can operate in several modes:

* __Active-Backup__: Each uplink is represented as a separate `ConnectInterface`.
* __Active-Active with MAC pinning__: This bonding type is not supported by the EDA plugin.
* __Active-Active with LACP__: A single `ConnectInterface` is created for all uplinks, mapped to an LACP interface in EDA.

The plugin provisions the correct `ConnectInterface` objects based on the virtual switch mode. The corresponding Interface objects in EDA must be
created before installing the plugin.

### Event Monitoring

The plugin subscribes to events in Prism Central and configures EDA resources accordingly:

| **Event Trigger**                     | Custom Resource    | Purpose                                                                  |
|---------------------------------------|--------------------|--------------------------------------------------------------------------|
| VLAN Subnet events                    | `BridgeDomain`     | Each VLAN subnet results in a unique `BridgeDomain` (Prism Central mode) |
| VLAN Subnet events                    | `VLAN`             | Each VLAN subnet creates a `VLAN` resource for attachment to the BD      |
| Host NIC virtual switch uplink events | `ConnectInterface` | Each host NIC uplink creates a `ConnectInterface`                        |

### Audit

The plugin performs an audit on startup and when requested by the operator to ensure synchronization between Prism Central and EDA. Any discrepancies are resolved automatically. See also the [audit documentation](../audit.md).

#### Operator Initiated Audit

In addition to the startup audit, users can initiate an [audit](../audit.md) manually. The audit object contains the status and results, including any discrepancies found between Nutanix and Connect.


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
