# VMware NSX Plugin

## Overview

The NSX plugin enables automated fabric configuration for VMware NSX environments, supporting both **Overlay** and **VLAN segments**. It integrates with EDA Connect to dynamically manage bridge domains and VLANs based on NSX segment definitions.

NSX provides advanced networking capabilities such as:

* L2/L3 overlays using VXLAN or Geneve
* VLAN-based connectivity
* Tier-0 routers for overlay-to-underlay breakout
* Micro-segmentation, load balancing, and VPN services

This plugin focuses on automating fabric configuration for overlay and VLAN segments:

* Automatic provisioning of the fabric based on the configured NSX VLAN segments.
* Automatic provisioning of the fabric based on NSX Host Transport Node and Host Switch Profile. The plugin will facilitate the communication between the hypervisors on these overlay segments. EDA will not be involved in the actual overlay traffic in this case.
* Automatic provisioning of the fabric based on NSX Edge Node Transport VLANs.
* CMS-managed and EDA-managed integration modes (See also [Operational Modes](#operational-modes))

### Supported Versions

* VMware NSX 4.2

## Architecture

The VMware NSX plugin consists of two components:

*VMware NSX Plugin App*
: This app runs in EDA and manages the lifecycle of the VMware NSX plugins. It does so in the standard app model where a custom resource is used
to manage the VMware NSX plugins.

*VMware NSX Plugin*
: The plugin itself, which is responsible for connecting and monitoring the VMware NSX environment for changes.

## Installation

For detailed deployment instructions, see the [VMware NSX Plugin Installation Guide](vmware-nsx-installation.md).

## Features

### vCenter Support

While NSX is used for defining overlay networking, vCenter is still used to configure the compute hosts and VMs. The NSX plugin has a dependency on one or more VMware vCenter plugins for the creation of the ConnectInterface objects in EDA.

### Supported network scenarios

#### Host Transport Nodes and Overlay Segments

Overlay segments in NSX are L2 networks encapsulated in L3 using VXLAN or Geneve. The encapsulated traffic is VLAN-tagged and transported via uplinks defined in NSX configurations.

The NSX plugin will create a `BridgeDomain` and a `VLAN` resource based on the *Transport VLAN* defined on the *Host Transport Node* in NSX. EDA and the Fabric will not be involved in the overlay traffic itself; the plugin will only facilitate communication between the hypervisors on these overlay segments.

#### VLAN Segments

In NSX, it is also still possible to create VLAN segments. When a VLAN segment is linked in a Host Transport Node, the NSX plugin will create the appropriate `BridgeDomain` and `VLAN` resources in EDA.

/// details | Constraints when using VLAN Segments
    type: danger

When linked to Edge nodes, VLAN segments are not configured by the NSX plugin. VLAN segments can only be linked to Host Transport Nodes.

///

#### Edge Node

In NSX Edge Nodes provide services at the edge of the network, such as routing between NSX logical networks and external physical networks. The plugin automatically provisions the transport network for the Edge Nodes when it is defined in NSX.

The uplinks of the Edge nodes are virtual rather than physical. To map these to the physical uplinks of the host, the plugin copies the uplink mapping from the Host Transport Node to the Edge Transport Node.

The NSX plugin will create a `BridgeDomain` and a `VLAN` resource based on the *Transport VLAN* defined on the uplink profile and transport zone of the *Edge Node* in NSX. The VLAN is allocated only when a transport zone of type "overlay" is also set, since any overlay network requires a transport zone.

/// details | Constraints when using Edge Nodes
    type: danger

The following constraints are imposed on Edge Node transport networks:

* The Edge Node can only have a transport network on a switch that has a default uplink teaming for its parent host.
* The Edge Node cannot have its transport network traffic go through a different NIC/Uplink than its parent host.
* The Edge Node cannot exclude itself from a Host Switch that its host is participating on. In the example above, this means it is not possible to create the VLAN for one of the switches and not the other.

///

/// details | Host Transport Node to Edge Node connectivity
    type: info

Most scenarios require connectivity between Host Transport Nodes and Edge Nodes. The easiest way to achieve this is by using [EDA-managed `BridgeDomains`](#operational-modes). Either with a single `BridgeDomain` for both Host Transport Nodes and Edge Nodes or by using multiple `BridgeDomains` interconnected through a `VirtualNetwork`. When using a single `BridgeDomain` make sure the IPAM configuration places both Host Transport Nodes and Edge Nodes in the same subnet.
///

### Operational Modes

The plugin supports the following operational modes:

*NSX Managed Mode*
: Also referred to as *Connect Managed*. When using this mode, the plugin will create a unique `BridgeDomain` for each VLAN segment and to facilitate overlay segment communication between the hypervisors.

*EDA Managed Mode*

: EDA managed BridgeDomains are supported for both VLAN and overlay networks. To specify an EDA managed BridgeDomain, use an NSX tag with:



    >   **Scope (key)**: `ConnectBridgeDomain`
    > 
    >   **Tag (value)**: The BridgeDomain name

: 
- For VLAN networks: Place the tag on the VLAN segment.
- For overlay networks: Place the tag on the overlay transport zone.
- For Edge Node transport VLANs: Place the tag on the Edge Node **overlay** transport zone.

: A VLAN is uniquely defined by its hostSwitchID, vlanTag, and edaBridgeDomain (the tag value). Two segments with the same VLAN tag but different BridgeDomain tags will result in two Connect VLANs.


[//]: # ( TODO&#40;Tom&#41; Add a screenshot of a tag here.)


### Heartbeat

The plugin implements a heartbeat mechanism, polling Connect at a regular interval (configured by `heartbeatInterval`). This ensures the plugin's health and timely processing of actionable events from Connect.

### Operator Initiated Audit

In addition to the startup audit, users can initiate an [audit](./audit.md) manually. The audit object contains the status and results, including any discrepancies found between NSX and Connect.

### Startup

When the plugin is started, the following actions are taken by the plugin:

* The plugin registers itself with Connect, based on the provided `externalID`. If a matching `ConnectPlugin` pre-exists, it is reused.
* The plugin performs an audit: Any Connect-related state that was programmed in NSX while the plugin was not running is synchronized with
  Connect.

### Alarms

Alarms will notify users of issues such as:

- Incorrect NSX credentials
- Bad certificate
- No connectivity to NSX
- EDA BridgeDomain missing for EDA managed resources
- Misconfigured resources (e.g., invalid uplink name)

[//]: # (- Required plugin or vCenter missing)

/// details | Required plugin or vCenter missing
    type: warning

When the NSX plugin detects that a required vCenter plugin is missing, it will not raise an alarm in the current release. 
Make sure that for all vCenters configured in NSX a corresponding vCenter plugin is installed and running in EDA.
///

## Troubleshooting

### The plugin is not running

If an incorrect NSX hostname or IP is configured in the `NsxPluginInstance` resource, the plugin will raise an alarm and retry the connection
indefinitely. In case the credentials are incorrect, the plugin will also raise an alarm and retry indefinitely.

* Check the raised NSX plugin alarms as well as any connect VMware plugin alarms.
* Check that the 'NSXPluginInstance' matches the compute manager's server IP or FQDN field and the corresponding VMware plugin name field.
* Check the connectivity from the EDA cluster to NSX.
* Verify the credentials for NSX. Make sure to check the base64 encoding of the Secret.
* Check the logs of the plugin pod.

### The plugin is not creating any resources in EDA

* Check the raised plugin alarms.
* Check the connectivity from the EDA cluster to NSX.
* Check the logs of the plugin pod.
* Check the plugin staleness state field and verify that heartbeats are being updated.
* Check the `NSXPluginInstance` resource and verify that it has valid values.
* Make sure the LLDP settings are correctly configured on all distributed vSwitches.
* Try to sync state by launching an Audit (see [Operator Initiated Audit](#operator-initiated-audit)).


### The plugin is configuring an incorrect state in EDA

* Check the raised NSX and VMware plugin alarms.
* Check the logs of the plugin pod.
* Make sure the LLDP settings are correctly configured on all distributed vSwitches.
* Try to sync state by launching an Audit (see [Operator Initiated Audit](#operator-initiated-audit)).
* Inspect the EDA resources, like `VLANs` and `BridgeDomains`.
* Verify the required vCenter plugins are configured correctly.