# Kubernetes Plugin

## Overview

EDA Cloud Connect integrates with Kubernetes and in particular the OpenShift flavor to provide fabric-level application networks for 
Kubernetes pods and services. The Connect integration
leverages the Kubernetes Multus CNI solution to support managing the fabric directly from Kubernetes and make the fabric dynamically respond to the
networking needs of the application.

It provides the following advantages and capabilities:

* Direct integration into the network management workflow of Kubernetes
* Use of the common CNIs used by Enterprise applications and CNFs like IPVLAN and SR-IOV
* Automatic provisioning of the fabric based on where the application pods need the connectivity
* Support for advanced workflows
* Different [operational modes](#operational-modes):
    - Kubernetes-managed operational mode
    - EDA-managed operational mode
* Different [association modes](#association-modes)
    - Network Attachment Definition Transparent operational mode (Kubernetes-managed only)
    - Connect Network Definition operational mode (Kubernetes-managed and EDA-managed)
    - Network Attachment Definition Annotation operational mode (EDA-managed only)
* Optimally configure subinterfaces to minimize configuration and security footprint of network services
* LAG/LACP interfaces
* VLAN Trunking
* Audits

### Supported secondary CNI

* MACVLAN
* IPVLAN
* SR-IOV
* Dynamic SR-IOV

/// details | What about the primary CNI?

The traffic of the primary CNI such as flannel or calico is typically vxlan or geneve encapsulated and is not configured as such in EDA or the fabric.
The underlay network used to transport this traffic is typically managed outside of EDA Connect.
///

### Supported Versions

* Red Hat OpenShift 4.16
* Red Hat OpenShift 4.18
* Red Hat OpenShift 4.20

/// details | Other Kubernetes flavors
    type: warning
    
While the Kubernetes plugin is primarily tested on Red Hat OpenShift, it will also work on other Kubernetes flavors, as long as they provide the
required prerequisites.
See the [Installation Guide](./kubernetes-plugin-installation.md) for more details.
///

/// details | Running Kubernetes in VMs
    type: warning

The Kubernetes plugin is designed to work with Kubernetes clusters running on bare-metal nodes. When running the Kubernetes cluster inside VMs,
the fabric can be orchestrated by EDA Connect through the hypervisor plugin (e.g., VMware vSphere, VMware NSX, OpenStack or the Nutanix Prism 
Central plugin).

///
## Architecture

The Kubernetes plugin consists of a controller which will monitor the following resources in Kubernetes:

* The physical NIC configuration and correlation to `NetworkAttachmentDefinitions` through the NMState Operator.
* `NetworkAttachmentDefinitions` and their master interfaces.
* `ConnectNetworkDefinitions` for the configuration of Layer 2 and Layer 3 services configuration.

/// details | Where does the plugin run?

The Kubernetes plugin controller runs as a pod in the Kubernetes cluster, not in the EDA k8s cluster. It connects to the EDA cluster to create and
manage the required EDA resources based on the Kubernetes configuration.
///

### Installation

For detailed deployment instructions, see the [Kubernetes Plugin Installation Guide](./kubernetes-plugin-installation.md). 

## Features

The Kubernetes plugin supports two operational modes for the `NADs`: CMS-managed mode and EDA-managed mode. Next to that it also supports three ways of
associating `NetworkAttachmentDefinitions` to EDA `BridgeDomains`: Transparent association, Annotation based association, and
`ConnectNetworkDefinition` association.

### Operational Modes

*Kubernetes-Managed Mode*
: Also referred to as *Connect Managed*. When using this mode, the plugin will create resources in EDA purely based on the configuration in Kubernetes.
Depending on the association mode used, this can be pure layer 2 or involve routers on the fabric level.

*EDA-Managed Mode*
: In EDA-managed mode, resources are first created in EDA and later on linked in Kubernetes. This allows for more advanced configuration of the
application networks.

### Association Modes

The Kubernetes plugin supports the following association modes between `NetworkAttachmentDefinitions` in Kubernetes and `BridgeDomains` in EDA:

*Transparent association*
: This association does not require any information from EDA in Kubernetes. For every unique master interface defined in `NADs` in the Kubernetes
cluster, the plugin will create a unique `BridgeDomain` resource. This association only supports Kubernetes-managed mode.

*Annotation based association*
: In this association, annotations are added to the `NAD` that reference an existing EDA `BridgeDomain`. This association only supports EDA-managed
mode.

*`ConnectNetworkDefinition` association*
: The `ConnectNetworkDefinition` is a Custom Resource Definition that gets added to the Kubernetes Cluster and is used to describe the relationship
between the different services and `NetworkAttachmentDefinitions`, and how the services relate to each other. This association supports both
Kubernetes-managed and EDA-managed modes. By using this association mode, operators can define more complicated relationships between NADs without
having to configure them on EDA, although EDA-managed mode is also supported. This mode is the most advanced and flexible.

#### Using the Transparent Association Mode

To use the Transparent association mode, create network attachment definitions (NADs) in Kubernetes without any EDA Connect annotations or any
reference to the NAD in a Connect Network Definition (CND).

By doing so, the plugin creates a new EDA `BridgeDomain` for each NAD with a unique master (+VLAN) interface. If a NAD is created for which a NAD with
the same master interface and VLAN already exists, it is associated with the existing `BridgeDomain`.

When you remove the NAD, the EDA bridge domain is also removed.

#### Using the NAD Annotation Association Mode

The NAD Annotation operational mode only works for the EDA-managed operational mode because it relies on an annotation on the NAD that identifies the
pre-existing EDA BridgeDomain resource to which the NAD needs to be associated with.

To use this operational mode, when creating or updating a NAD, add the following annotation to it:

```yaml
connect.eda.nokia.com/bridgedomain: <eda-bridge-domain-name> 
```

In case of VLAN trunking, a more complex annotation needs to be used for each vlan in play, for example:

```yaml
connect.eda.nokia.com/bridgedomain: <eda-bridge-domain-name>:<vlan-id>, <eda-bridge-domain-name-2>:<vlan-id> 
```

#### Using the Connect Network Definition Operational Mode

Connect Network Definition (CND) is a custom resource definition (CRD) that is added to the Kubernetes cluster on deployment of the plugin.

A CND contains a design of all the network services and configuration an application may need. It can be used to define EDA `Routers` and EDA
`BridgeDomain` resources. For each `BridgeDomain`, it is possible to associate one or more NADs with it. By doing so, the plugin knows how to connect
applications into different network services.

In some deployment use cases, `preProvisionHostGroupSelector` can be used to pre-provision connect interface for a NAD interface on a set of selected
hosts, regardless of whether they are consumed by any pod. This will consume more resources on the fabric side, but can be useful
in some scenarios where pods are scheduled dynamically on different nodes and need to have immediate connectivity without waiting for the
fabric to be provisioned.

/// details | Limitations of `preProvisionHostGroupSelector`
    type: warning
Please note that this attribute is only applicable to `IPVLAN` and `MACVLAN` type of `NetworkAttachmentDefinitions`
///

You can use the CMS-managed integration mode, the EDA-managed integration mode, or a combination of both.

Multiple CNDs can exist, for instance one per application.

The below section details a couple of examples of CND usage.

/// details | Example 1: Multiple `NADs` in One `BridgeDomain`
#### Example 1: 

The following is a sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be residing in a single subnet,
when they belong to different master interface. This is an example of Kubernetes Managed Mode.

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example1.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example1.yaml"
EOF
```

///

///

/// details | Example 2: Multiple `NADs` in One `BridgeDomain` with VLAN Trunking

The following is a sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be residing in a single subnet,
and have them use trunk VLAN's:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example2.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example2.yaml"
EOF
```

///

///

/// details |  Example 3: Using EDA-managed mode with CND

The following is a sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be part of a single `BridgeDomain`
that was pre-created in EDA:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example3.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example3.yaml"
EOF
```

///

///

/// details | Example 4: Using preProvisionHostGroupSelector to pre-provision connect interface with the label selector

To be able to consume this attribute in CND, ensure that the Kubernetes nodes are labelled correctly and the same value is used in the CND.

Example of the labelling a node is as following:

```shell

kubectl label nodes node-1 connect.eda.nokia.com/hostGroup=net-group-1
kubectl label nodes node-2 connect.eda.nokia.com/hostGroup=net-group-2
```

The following is a sample configuration of the CND usage to be able to pre-configure connect interface

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example4.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example4.yaml"
EOF
```

///

///

/// details | Example 5: Multiple `NADs` in One `BridgeDomain` associated to a `Router`

The following is a sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be residing in a single subnet,
associated with a router:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example5.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example5.yaml"
EOF
```

///

///
## Troubleshooting

### The controller plugin is not running

Verify the following items:

* Incorrect Service Account Token configuration.
* Check connectivity between controller pod in Kubernetes and EDA cluster.
* Ensure the heartbeat interval is a non-negative integer.
* Plugin name must comply with this regex check `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'`. It may only contain alphanumerical characters
  and '.', '_', '-' (dot, underscore, and, dash) and must start and end with an alphanumerical character.

### Nothing is created in EDA

Verify the following items:

* Check if the plugin controller is able to access the `NMstate` API and `NetworkAttachmentDefinition` API on the Kubernetes cluster.
* Check the plugin can reach EDA cluster correctly.

### The plugin is not configuring the correct state

* Inspect the EDA resources, like `VLAN`, `BridgeDomain` and `ConnectInterface`.
* Check the logs of the plugin pod.
