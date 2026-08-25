# OpenStack Client Provider

## Overview

The OpenStack Client Provider publishes metadata about OpenStack virtual machines into the EDA `networks` client
table.

The provider authenticates to Keystone, polls Nova and Neutron, and writes `provider-openstack-vm` entries for each
VM port that it can correlate with a `BridgeDomain`. The Networks Client Provider then supplies fabric-learned MAC and IP
data for the same clients.

/// details | Technical preview
    type: warning

The OpenStack Client Provider is a technical preview in this release.

///

### Supported Versions

The OpenStack Client Provider supports the same OpenStack platforms as the OpenStack plugin:

* Red Hat OpenStack Platform (RHOSP) 17.1
* Red Hat OpenStack Services on OpenShift (RHOSO) 18.0

The installation of the OpenStack plugin on the targeted cloud is mandatory.

## Architecture

The OpenStack Client Provider is an EDA application. It is separate from the OpenStack plugin, which lives on the
target OpenStack cluster instead.

Each `OpenStackClientProviderInstance` starts one operator pod that authenticates to
one OpenStack cloud and publishes client-table rows for the `spec.namespace` namespace.

## Installation

For detailed deployment instructions, see the [OpenStack Client Provider Installation Guide](installation.md).

## Features

### Inventory

The provider publishes VM NICs that are attached to Neutron networks with a **VLAN** or **FLAT** segment.

It does not publish VMs that are only on Geneve or VXLAN overlay networks.

Each published row requires:

* A MAC address
* An IP address
* A `BridgeDomain` or a router value

The provider writes one row for each Neutron fixed IP on the port.

/// details | Neutron segments extension
    type: warning

The provider uses the Neutron segments API to gather information about VLAN and FLAT networks. If that extension is not
available, the inventory is empty even when Nova lists servers.

///

### Bridge domain resolution

The provider publishes a VM row only when it can resolve a `BridgeDomain` for the Neutron network. 
It does this in three ways:

1. For EDA-Managed networks it uses the Neutron network extension `eda_bridge_domain`.
2. For Connect-Managed networks it uses the `BridgeDomain` whose label `connect.eda.nokia.com/external-id` equals the
   Neutron network ID.
3. As a fallback, it selects one `VLAN` resource whose VLAN ID matches the Neutron segment ID.

If none of these match, the provider skips the row.

### IP from other providers

When a port has a MAC and a `BridgeDomain` but no Neutron fixed IP, the provider can reuse an IP from another
provider in the same `networks` client table. The match uses MAC and `BridgeDomain` together. Typical source rows
come from the Networks Client Provider (`provider-networks`).

### Status

After a poll, the instance status reports:

* Phase and a status message
* Last successful sync time
* Server, port, and segment counts from the last poll
