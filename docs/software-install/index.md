# Software Installation Guide

-{{ js_script("/javascripts/viewer-static.min.js") }}-

This document describes the installation procedure in a production environment; to install Nokia Event-Driven Automation (EDA) in a lab, development or test environment, see [Getting Started](../getting-started/try-eda.md).  
It includes procedures for preparing the nodes that host the application, installing the application, upgrading and uninstalling.

/// admonition | Note
    type: subtle-note
This document covers the current release and may also contain some content that will be released in later maintenance loads. See the Nokia EDA Release Notes for information about features supported in each load.
///

//// details | Precautionary and information messages

/// danger
Danger warns that the described activity or situation may result in serious personal injury or death. An electric shock hazard could exist. Before you begin work on this equipment, be aware of hazards involving electrical circuitry, be familiar with networking environments, and implement accident prevention procedures.
///
/// warning
Warning indicates that the described activity or situation may, or will, cause equipment damage, serious performance problems, or loss of data.
///
/// caution
Caution indicates that the described activity or situation may reduce your component or system performance.
///
/// admonition | Note
    type: subtle-note
Note provides additional operational information.
///
/// admonition
    type: tip
Tip provides suggestions for use or best practices.
///
////

## Installation process overview

The installation consists of the following high-level tasks:

### General preparation

These tasks must be completed for both Internet based installations and air-gapped installations.

/// html | div.steps

1. [Downloading the Nokia EDA Installation playground](preparing-for-installation.md#download-the-nokia-eda-installation-playground)  
    This task describes how to access the NokiaEDA installation playground for use during the installation. It also covers how to configure the playground.

2. [Downloading the edaadm tools](preparing-for-installation.md#download-edaadm-tools)  
    This task describes how to download the EDAADM repository and the `edaadm` tool, used for several steps in the installation process.

3. [Download the Talos machine image](preparing-for-installation.md#download-the-talos-machine-image)  
    This task describes how to download the Talos base image from the official Talos image factory for your environment.

///

### Air-gapped setup

In case the installation will be air-gapped, this section provides steps on how to set up the Assets VM and load it with the necessary assets for deploying EDA in an air-gapped environment.

/// html | div.steps

1. [Downloading the assets](air-gapped/downloading-the-assets.md)  
    This task describes how to download all the necessary assets using a system with Internet access, so they can be used to deploy EDA in the air-gapped environment.

2. [Deploying the Assets VM](air-gapped/assets-vm.md) <small>optional</small>  
    Deploys the Assets VM in the air-gapped environment, bootstraps it and uploads all the assets to it.

3. [Uploading the assets](air-gapped/uploading-assets.md)  
    Uploads all the assets to the Assets VM.

///

### Deploying Nokia EDA

/// html | div.steps

1. [Preparing the EDAADM configuration file](deploying-eda/setting-up-the-eda-virtual-machine-nodes.md#preparing-the-edaadm-configuration-file)  
    This task describes the details of the EDAADM configuration file and how to set it up.

2. [Generating the Talos machine configurations](deploying-eda/setting-up-the-eda-virtual-machine-nodes.md#generating-the-talos-machine-configurations)  
    Using the `edaadm` tool and the configuration file, this task generates specific Talos machine configuration files for each Talos VM.

3. [Deploying the Talos virtual machines](deploying-eda/setting-up-the-eda-virtual-machine-nodes.md#deploying-the-talos-virtual-machines)  
    This task describes how to use the Talos base image and machine configuration files to deploy the Talos VMs in your KVM or VMware vSphere environment.

4. [Bootstrap the Talos Kubernetes cluster](deploying-eda/bootstrap-the-talos-kubernetes-cluster.md)  
    This task bootstraps the Talos Kubernetes environment using the VMs you have created.

5. [Installing the Nokia EDA application](deploying-eda/installing-the-eda-application.md)  
    Using the Nokia EDA Installation playground, this step installs Nokia EDA on the Kubernetes environment in the Nokia EDA nodes.

///

## Components

Several key concepts are used throughout the documentation; following is an overview of these concepts and components:

*Talos Linux and Kubernetes*
: Nokia EDA uses Talos Linux and Kubernetes to host its services. Talos Linux is a minimalistic, locked-down, read-only and secured Linux environment purposely built to run Kubernetes. This ensures a more secure environment with significantly lower security footprint than regular Linux and Kubernetes environments.

*Playground git repository*
: The Playground git repository is [publicly available](https://github.com/nokia-eda/playground) and is used to deploy Nokia EDA itself.

*[`edaadm`](preparing-for-installation.md#download-edaadm-tools)*
: A CLI tool that will be used for several steps in the process:

    * Get the location to download the base Talos image for KVM and VMware environments.
    * Generate Talos machine configuration files for the deployment of both the Assets VM and the Nokia EDA Kubernetes cluster VMs.
    * Initiate Talos Kubernetes clusters.

*`edaadm` git repository*
: A [publicly available](https://github.com/nokia-eda/edaadm) git repository that contains details and definitions for:

    * Assets bundles for air-gapped installations: Nokia EDA assets are defined in different bundles, based on their purpose. The repository provides the bundles and the means to download the content of the bundles from the Internet and then upload them to the deployed Assets VM.
    * A KPT package to initiate the Assets VM.

*Air-gapped Assets VM*
: Used in an air-gapped environment, the Assets VM is a Virtual Machine deployed on a KVM or VMware environment. It is a single VM K8s cluster that will run:

    * A container registry to host all the container images used by Nokia EDA.
    * A git server to host the App Store Catalog.
    * A web server to host certain artifacts used by Nokia EDA.

*Air-gapped Bundles*
: Used in air-gapped installations, a bundle is a definition of a group of assets that are related. For instance a bundle for the core components of Nokia EDA for a specific version, or a bundle of the standard Apps for a specific version. Bundles are downloaded using the `edaadm` tool from the internet, and then uploaded using `edaadm` to the Assets VM. The product comes with a set of standard bundles and custom bundles can be created based on their examples.

*Air-gapped Nokia EDA Shipyard*
: A name used to describe the combination of the container registry, git server and web server running on the Assets VM.

## Version information

### Release numbering

Nokia EDA software uses the following release numbering scheme:

* **Major release number**: The last two digits of the year in which the release is made. For example, releases made in -{{ eda_year }}- use the major release number `-{{ eda_major_version }}-`, as in `-{{ eda_major_version }}-.x`.
* **Minor release number**: The number of the month in which the feature release first becomes available. For example, a feature release made available in April of -{{ eda_year }}- has the release number `-{{ eda_major_version }}-.4`, where `4` indicates the fourth month. The minor release number remains fixed even if the release is delayed past the end of the intended month.
* **Maintenance release number**: The final number appended to the release number. The first iteration of a release is appended with `.1`, as in `-{{ eda_major_version }}-.4.1`; the second with `.2`, as in `-{{ eda_major_version }}-.4.2`; and so on.

The following diagram shows how these components combine into a complete release number:

-{{ diagram(path='./diagrams/release-numbering.drawio', title='Release numbering scheme', page=0, zoom=1.2) }}-

/// admonition | Long-term release
    type: subtle-note
The last minor release of the year happens in December (e.g., `-{{ eda_major_version }}-.12`) and is the **long-term release**. It receives security and bug fixes for longer than the other minor releases in the same major release.
///

### Core and applications

EDA software consists of the EDA core and the pluggable applications. The core is versioned using the semantic versioning scheme and the following table lists the matching EDA core versions for each release:

| EDA release version | EDA core version |
|-------------|------------------|
| 26.8 | v6.0.0 |
| 26.4 | v5.0.0 |
| 25.12 | v4.0.0 |
| 25.8 | v3.0.0 |
| 25.4 | v2.0.0 |
| 24.12 | v2.0.0 |

EDA applications declare the supported EDA core versions in their manifest file using the `.spec.supportedCoreVersions` field.

The applications themselves are versioned individually using the semantic versioning scheme and do not have a direct relationship to the EDA core version. Individual application versions can be viewed in the EDA Store UI or as git tags in the application's catalog.

### Talos Kubernetes

The Talos Kubernetes version Nokia EDA is deployed on is set by the [`edaadm`](preparing-for-installation.md#download-edaadm-tools) CLI tool. Edaadm downloads the respective Talos images and generates the machine configurations and bootstraps the Kubernetes cluster.

The following table lists the default Talos and the corresponding Kubernetes versions for each `edaadm` version:

| edaadm version | Talos version | Kubernetes version |
|----------------|---------------|--------------------|
| [4.0.0][edaadm-gh-4.0.0] | [1.13.6][talos-rel-1.13.6] | [1.36.2][kubernetes-rel-1.36] |
| [3.3.0][edaadm-gh-3.3.0] | [1.11.5][talos-rel-1.11.5] | [1.34.1][kubernetes-rel-1.34] |
| [3.2.0][edaadm-gh-3.2.0] | [1.11.5][talos-rel-1.11.5] | [1.34.1][kubernetes-rel-1.34] |
| [3.1.0][edaadm-gh-3.1.0] | [1.11.5][talos-rel-1.11.5] | [1.34.1][kubernetes-rel-1.34] |
| [3.0.0][edaadm-gh-3.0.0] | [1.11.5][talos-rel-1.11.5] | [1.34.1][kubernetes-rel-1.34] |
| [2.0.0][edaadm-gh-2.0.0] | [1.9.2][talos-rel-1.9.2] | 1.32.1 |
| [1.0.0][edaadm-gh-1.0.0] | [1.8.3][talos-rel-1.8.3] | 1.31.2 |

The Kubernetes version denotes the default Kubernetes version that is used by the `edaadm` tool of the given release. The user can choose a different Kubernetes version by specifying setting it in the [`edaadm` configuration file](deploying-eda/setting-up-the-eda-virtual-machine-nodes.md#edaadm-configuration-file-fields).

[edaadm-gh-4.0.0]: https://github.com/nokia-eda/edaadm/releases/tag/v4.0.0
[talos-rel-1.13.6]: https://github.com/siderolabs/talos/releases/tag/v1.13.6
[kubernetes-rel-1.36]: https://kubernetes.io/releases/1.36/

[edaadm-gh-3.3.0]: https://github.com/nokia-eda/edaadm/releases/tag/v3.3.0
[edaadm-gh-3.2.0]: https://github.com/nokia-eda/edaadm/releases/tag/v3.2.0
[edaadm-gh-3.1.0]: https://github.com/nokia-eda/edaadm/releases/tag/v3.1.0
[kubernetes-rel-1.34]: https://kubernetes.io/releases/1.34/

[edaadm-gh-3.0.0]: https://github.com/nokia-eda/edaadm/releases/tag/v3.0.0
[talos-rel-1.11.5]: https://github.com/siderolabs/talos/releases/tag/v1.11.5

[edaadm-gh-2.0.0]: https://github.com/nokia-eda/edaadm/releases/tag/v2.0.0
[talos-rel-1.9.2]: https://github.com/siderolabs/talos/releases/tag/v1.9.2

[edaadm-gh-1.0.0]: https://github.com/nokia-eda/edaadm/releases/tag/v1.0.0
[talos-rel-1.8.3]: https://github.com/siderolabs/talos/releases/tag/v1.8.3

## Deployment models

Nokia EDA is deployed as an application on a compatible Kubernetes cluster comprised of one, three, or more nodes (validated for up to six nodes). The nodes (VMs) run a Kubernetes cluster with the following composition:

* One or three Kubernetes master nodes that also function as worker nodes: one, in case a single-VM deployment is used; otherwise three Kubernetes master nodes.
* Any remaining nodes (in a four or more node deployment) function as worker nodes.
* One, two or more nodes must also be designated as storage nodes. For redundancy, two is the minimum in a three or more node deployment. These nodes still function as worker (and potentially master) nodes as well. Rook-Ceph is used to create a storage cluster across the nodes indicated as storage nodes.
* (Optional) An Assets VM which will hold all the resources and files needed in case of an [air-gapped environment](air-gapped/index.md).

## Networking for Nokia EDA nodes

This guide describes the deployment of EDA on a Kubernetes cluster with a single network, where access from both users and orchestrators to the UI and API, and access from EDA to the fabric (for example, SR Linux devices) go over the same interface.

It is possible to use two separate networks for the EDA nodes:

* OAM network  
    This interface is used to access the UI and the API of Nokia EDA. It is also through this network that the deployment tool reaches the nodes.

* Fabric management network  
    This interface is used to communicate with the management interfaces of the fabric (for example, SR Linux devices) and is where Nokia EDA exposes its DHCP and ZTP services.

## EDA nodes

The Nokia EDA nodes are the VMware vSphere-based or KVM-based virtual machines (VMs) that host the Kubernetes environment on which the Nokia EDA application and Digital Sandbox are run.

These nodes run a hardened Talos Kubernetes environment. Talos is a secure, up-to-date and hardened platform for running Kubernetes.

EDA supports the following deployment models:

* an environment with one node, which hosts only the Nokia EDA application for small scale deployments
* an environment with three or more nodes, which hosts only the Nokia EDA application

## Requirements for deployment

This section describes the platform requirements, node requirements, and virtual IP requirements for deploying EDA.

### Installation platform requirements

To execute the installation process, you need access to a Linux environment[^1] with the following components installed:

/// html | table
//// html | th[style='text-align: center;']
Component
////
//// html | th[style='text-align: center;']
Requirement
////

//// html | tr
///// html | td
**Linux environment**
/////
///// html | td
Any Linux distribution. The procedures provided in this document are validated on Ubuntu.
/////
////

//// html | tr
///// html | td
**Container runtime**
/////
///// html | td
Docker must be running and you should be able to run containers
/////
////

//// html | tr
///// html | td
**Tools**
/////
///// html | td

* `make` - Used to execute several installation steps.
* `git` - Used to check out git repositories.
* `curl` - Used to download files.
* `jq` and `yq` - Used to parse JSON and YAML files.
* `sed` - Used to parse and replace content.
* `tar` and `zip` - Used to create and unpack bundles and assets for the air-gapped installation process.
* `edaadm` - Used to generate configuration for Talos and other useful commands to initiate the Talos environments. It can be downloaded from the [`edaadm` repository releases](https://github.com/nokia-eda/edaadm/releases/latest) page.
* `htpasswd` - (Optional) Used in case a custom username and password is required for the Assets VM web server.
* `base64` - (Optional) Used in case a custom username and password is required for the Assets VM web server or git server.
* `ovftool` - (Optional) Used to deploy the VMs in a VMware vSphere environment. Can be downloaded from the [Broadcom Developer Portal](https://developer.broadcom.com/tools/open-virtualization-format-ovf-tool/latest)

The following tools are also helpful. If they are not present, the installation tool downloads them later:

* `kubectl`
* `helm`
* `k9s`
* `kpt`

/////
////

//// html | tr
///// html | td
**Internet access**
/////
///// html | td
Required for Internet-based installations. For air-gapped installations, at least one system needs internet access.

Either directly or through a proxy.
/////
////

///

/// admonition | Note
    type: subtle-note
In case of an air-gapped installation, the guide will refer to two tools-systems, one with public internet access and one in the air-gapped environment. These can be the same system that is moved from the public side to the air-gapped side after downloading all the resources; or it can be two different systems.
///

### Nokia EDA node requirements

The Nokia EDA nodes are deployed as virtual machine servers. Node requirements summarizes the requirements of Nokia EDA nodes in KVM and VMware hypervisor.

/// html | table
//// html | th[style='text-align: center;']
Component
////
//// html | th[style='text-align: center;']
Requirement
////

//// html | tr
///// html | td
**CPU**
/////
///// html | td
32 vCPU on a modern x86-64 CPU that supports virtualization
/////
////

//// html | tr
///// html | td
**Memory**
/////
///// html | td
64 GB
/////
////

//// html | tr
///// html | td
**Storage**
/////
///// html | td

* Operating system: 100GB of available SSD-based storage
* Storage nodes: 300GB of available SSD-based storage on a separate virtual disk
/////
////

//// html | tr
///// html | td
**Networking**
/////
///// html | td

* at least one 10 Gbps NIC
* the configured DNS servers must be reachable, functional, and able to resolve the hostnames used for the Nokia EDA nodes
* for internet-based installations: Internet access directly or through a proxy
* system time synced using NTP

/////
////

//// html | tr
///// html | td
**Virtualization platform**
/////
///// html | td
You can run the Nokia EDA nodes as virtual machines using the following virtualization platforms:

* operating system: VMware vSphere 7.0 or 8.0 or RHEL/Rocky
* hypervisor: ESXi 7.0 or 8.0 or KVM
* resource reservation for CPU, memory, and disks must be set to 100% for the Nokia EDA node virtual machines
/////
////
///

### Nokia EDA Assets VM requirements

/// admonition | Note
    type: subtle-note
This only applies if you plan to use the air-gapped installation process.
///

The Assets VM runs as a single VM inside the air-gapped environment. This VM holds all of the assets and can be used across multiple deployments and Nokia EDA versions, containing the assets for multiple versions. This VM has the following requirements:

/// html | table
//// html | th[style='text-align: center;']
Component
////
//// html | th[style='text-align: center;']
Requirement
////

//// html | tr
///// html | td
**CPU**
/////
///// html | td
4 vCPU on a modern x86-64 CPU that supports virtualization
/////
////

//// html | tr
///// html | td
**Memory**
/////
///// html | td
16 GB
/////
////

//// html | tr
///// html | td
**Storage**
/////
///// html | td

* Operating system: 300GB
/////
////

//// html | tr
///// html | td
**Networking**
/////
///// html | td

* 1 Gbps NIC
* 1 IPv4 IP and optionally 1 IPv6 IP
* Preferably in the same OAM network as the Nokia EDA Kubernetes VMs, but minimally accessible by the Nokia EDA Kubernetes VMs via the OAM network
* system time synced using NTP

/////
////

//// html | tr
///// html | td
**Virtualization platform**
/////
///// html | td
You can run the Nokia EDA Assets VM as a virtual machine using the following virtualization platforms:

* operating system: VMware vSphere 7.0 or 8.0 or RHEL/Rocky
* hypervisor: ESXi 7.0 or 8.0 or KVM
/////
////
///

### Virtual IP requirements

The deployment of Nokia EDA requires two virtual IP addresses in the management network:

* Kubernetes VIP: the virtual IP address used by all the control plane nodes in the Kubernetes cluster.
* Nokia EDA API/UI VIP: the virtual IP address used by the Nokia EDA API and UI.

[^1]: This system might also be referred to as the "tools-system" further in this documentation.
