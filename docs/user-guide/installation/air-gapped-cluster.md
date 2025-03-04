# Setting up EDA in an Air-Gapped environment

In situations where the environment in which EDA is deployed does not have any connectivity to the internet, a local mirror with all the resources EDA needs, must be deployed.

This documentation will go over creating and setting up such an environment and use it for installation. It will cover the following items:

<!-- no toc -->
* [Components](#components)
* [Requirements](#requirements)
* [Creating the Assets VM image](#creating-the-assets-vm-image)
* [Downloading the Assets Bundles](#downloading-the-assets-bundles)
* [Downloading the Base Talos VM images](#downloading-the-base-talos-vm-images)
* [Preparing the Air-Gapped Environment](#preparing-the-air-gapped-environment)
* [Deploying the Assets VM](#deploying-the-assets-vm)
* [Uploading the Assets to the Assets VM](#uploading-the-assets-to-the-assets-vm)
* [Updating the EDAADM Configuration File for the EDA Kubernetes Cluster](#updating-the-edaadm-configuration-file-for-the-eda-kubernetes-cluster)

## Overview

### Environments

Two environments will be discussed and used in this environment:

*Public Environment*
: The environment that has internet access, this will be used when creating the Assets VM image and to download all the necessary assets and tools.

*Air-Gapped Environment*
: The environment that does not have internet access and will be used to deploy EDA into.

In each environment, you'll need a system where you can execute the steps from. This could be the same system that you first connect to the internet, follow the steps for the Public network for, and then move the system to the Air-Gapped environment to continue. Or it could be two systems and you copy the data from the Public system to the Air-Gapped system. More details on the requirements for these systems are included further in this document.

For each section, there will be a note in which environment the section applies.

### Components

Several key concepts will be used throughout the documentation, here's an overview of those concepts and components:

*Talos Linux and Kubernetes*
: EDA uses Talos Linux and Kubernetes to host its services in. Talos Linux is a minimalistic, locked-down, read-only and secured Linux environment to run Kubernetes in. This assures a more secure environment with significantly lower security footprint than regular Linux and Kubernetes environments.

*`edaadm`*
: A tool that will be used for several steps in the process:

    * Get the location to download the base Talos image for KVM and VMware environments.
    * Generate Talos machine configuration files for the deployment of both the Assets VM and the EDA Kubernetes cluster VMs.
    * Initiate Talos Kubernetes clusters.

*`edaadm` git repository*
: A [publicly available](https://github.com/nokia-eda/edaadm) git repository that contains details and definitions for:

    * Assets bundles: The EDA Assets are defined in different bundles, based on their purpose. The repository provides the bundles, and has a way to download the content of the bundles from the internet and then upload them to the deployed Assets VM.
    * KPT Package: A KPT package to initiate the Assets VM.

*Assets VM*
: The Assets VM is a Virtual Machine deployed on a KVM or VMware environment. It is a single VM K8s cluster that will run:

    * A container registry to host all the container images used by EDA.
    * A git server to host the App Store Catalog.
    * A web server to host certain artifacts used by EDA.

*Bundles*
: A bundle is a definition of a group of assets that are related. For instance a bundle for the core components of EDA for a specific version, or a bundle of the standard Apps for a specific version. Bundles are downloaded using the `edaadm` tool from the internet, and then uploaded using `edaadm` to the Assets VM. The product comes with a set of standard bundles and custom bundles can be created based on their examples.

*EDA Shipyard*
: A name used to describe the combination of the container registry, git server and web server running on the Assets VM.

*Playground git repository*
: The Playground git repository is [publicly available](https://github.com/nokia-eda/playground) and is used to deploy EDA itself.

### Conceptual Overview

In an Air-Gapped environment, an Assets VM is deployed that will provide the services that will serve the container images, git repositories and artifacts used during installation of the EDA Talos Kubernetes cluster and EDA itself.

The goal of the Air-Gapped solution design, is to allow flexibility in the deployment and content of the Assets VM in the Air-Gapped environment. By providing a standalone Assets VM without any assets automatically included, there is freedom of choice of what assets are uploaded to the Assets VM.

It allows for a single Assets VM to be used for multiple deployments and versions of EDA, as the assets for multiple versions of EDA can be uploaded to the same Assets VM.

Similarly, by splitting up the assets in bundles, it is possible to only upload specific content to the Assets VM. The bundle concept also allows for the creation of custom bundles, for instance for 3rd party Apps, so they can also be hosted on the Assets VM.

## Requirements

### Environment and Tools

/// admonition | This applies to both the Public and Air-Gapped environment
    type: note
///

A Linux system is needed that has the following commands and tools available:

* `docker` - A docker environment needs to be running as it is used to update KPT configuration using the `kpt-apply-setters` image.
* `curl` - Used to download files.
* `git` - Used to check out git repositories.
* `jq` - Used to parse JSON data.
* `sed` - Used to parse and replace content.
* `tar` and `zip` - Used to create and unpack bundles and assets.
* `edaadm` - Used to generate configuration for Talos and other useful commands to initiate the Talos environments. It can be downloaded from the [`edaadm` repository releases](https://github.com/nokia-eda/edaadm/releases/latest) page.
* `htpasswd` - (Optional) Used in case a custom username and password is required for the Assets VM web server.
* `base64` - (Optional) Used in case a custom username and password is required for the Assets VM web server or git server.
* `ovftool` - (Optional) Used to deploy the VMs in a VMware vSphere environment. Can be downloaded from the [Broadcom Developer Portal](https://developer.broadcom.com/tools/open-virtualization-format-ovf-tool/latest)

This system will be referred to as the public or air-gapped tools-system.

/// details | Make sure the user in the public tools-system is logged in for `docker.io`.
    type: warning
Docker has started to rate limit pulling images from docker.io more aggressively. To avoid the rate limit, make sure you have a user on docker.io and you logged into it on your public tools-system with:

```bash
docker login docker.io
```

///

### Repositories

/// admonition | This applies to both the Public and Air-Gapped environment
    type: note
///

Make sure to clone, copy or download (and unpack) the content of the following repositories to both public and air-gapped systems that will be used for the process:

* [`edaadm` repository](https://github.com/nokia-eda/edaadm)
* [Playground repository](https://github.com/nokia-eda/playground)

#### Downloading extra tools and kpt package

/// admonition | This applies to the Public environment, but content should be copied to the Air-Gapped environment.
    type: note
///

**Step 1** - Downloading Playground tools and packages
: In the Playground repository, make sure to run the following commands to download additional tools and the KPT packages needed for the EDA Install.

    ```bash
    make download-tools
    make download-pkgs
    ```

**Step 2** - Go to the bundles directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

**Step 3** - Downloading the tools for the bundles
: The following command will download the right tools

    ```bash
    make download-tools
    ```

**Step 4** - Go to the kpt directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `kpt` folder.

    ```bash
    cd path/to/edaadm-repository/kpt
    ```

**Step 5** - Downloading the tools for the kpt package
: The following command will download the right tools

    ```bash
    make download-tools
    ```

### Assets VM

The Assets VM will run as a single Virtual Machine inside the Air-Gapped environment. This VM will hold all of the assets and can be used across multiple deployments and EDA versions, containing the assets for multiple versions. This VM has the following requirements:

* CPU: 4 vCPUs on a modern x86-64 CPU that supports virtualization
* Memory: 16GB RAM
* Storage: 300GB of storage for the main disk
* Networking:
    * 1GbE interface
    * 1 IPv4 IP and optionally 1 IPv6 IP
    * Preferably in the same OAM network as the EDA Kubernetes VMs, but minimally accessible by the EDA Kubernetes VMs via the OAM network

## Creating the Assets VM Image

/// admonition | This applies to the Public environment, and is executed in the public tools-system
    type: note
///

Creating the Assets VM starts from a base Talos VM image for KVM or VMware, rebuilding it with the local cache needed to deploy the VM, Kubernetes and the Assets VM Services in the Air-Gapped environment.

### Preparing to create the Assets VM image

Before creating the Assets VM Image for a specific environment, the following steps need to be taken:

**Step 1** - Go to the correct directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

**Step 2** - Log in to `ghcr.io` with `docker` so the system can pull private images from `ghcr.io`.
: This needs to be a user with access to images hosted by Nokia EDA. For instance, the `nokia-eda-bot` user.

    ```bash
    docker login ghcr.io -u nokia-eda-bot
    ```

    /// details | Getting the password/token for the `nokia-eda-bot` user
        type: note
The token (password) for the `nokia-eda-bot` user is present in every bundle file in the `edaadm` repository, where it is twice encoded using `base64`.

This token is a read-only token and is not a secret, no sensitive information is accessible using this token.
///

**Step 3** - Prepare the image cache for the Assets VM
: This step will download and prepare an image cache for Assets VM to be build from.

    ```bash
     make create-assets-host-bootstrap-image-cache
    ```

### Creating the KVM Assets VM Image

/// admonition | This is only needed if you plan to deploy the Assets VM on KVM
    type: note
///

Follow these steps to create the Assets VM Image for KVM. This will generate an ISO file based on the Talos VM base image containing a local cache. This image is different from the base Talos image ISO file that you will use for the EDA Kubernetes VMs, but is based on it.

**Step 1** - Go to the correct directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

**Step 2** - Generate the Assets VM ISO for KVM
: Execute the following command to generate the KVM Talos ISO for the Assets VM.

    ```bash
    make create-asset-vm-nocloud-boot-iso
    ```

    The output should look similar to:

    ```
    --> INFO: List of goals: create-asset-vm-nocloud-boot-iso
    docker pull ghcr.io/siderolabs/imager:v1.9.2
    v1.9.2: Pulling from siderolabs/imager
    Digest: sha256:b99d29d04df9eea89d50cb0d13d57e1e035e54cbd9970a26af99b18154e443a9
    Status: Image is up to date for ghcr.io/siderolabs/imager:v1.9.2
    ghcr.io/siderolabs/imager:v1.9.2
    skipped pulling overlay (no overlay)
    profile ready:
    arch: amd64
    platform: nocloud
    secureboot: false
    version: v1.9.2
    input:
      kernel:
        path: /usr/install/amd64/vmlinuz
      initramfs:
        path: /usr/install/amd64/initramfs.xz
      baseInstaller:
        imageRef: ghcr.io/siderolabs/installer:v1.9.2
      imageCache:
        imageRef: ""
        ociPath: /image-cache.oci
    output:
      kind: iso
      imageOptions:
        diskSize: 2147483648
      outFormat: raw
    skipped initramfs rebuild (no system extensions)
    kernel command line: talos.platform=nocloud console=tty1 console=ttyS0 net.ifnames=0 talos.halt_if_installed=1 init_on_alloc=1 slab_nomerge pti=on consoleblank=0 nvme_core.io_timeout=4294967295 printk.devkmsg=on ima_template=ima-ng ima_appraise=fix ima_hash=sha512
    ISO ready
    output asset path: /out/nocloud-amd64.iso
    ```

**Step 3** - Rename the KVM Assets VM image
: Rename the generated image to a convenient name so that you can copy or use it in the future.

    ```bash
    mv eda-cargo/talos-asset-vm-boot-imgs/nocloud-amd64.iso eda-cargo/talos-asset-vm-boot-imgs/eda-asset-vm-nocloud-amd64.iso
    ```

### Creating the VMware Assets VM Image

/// admonition | This is only needed if you plan to deploy the Assets VM on VMware vSphere
    type: note
///

Follow these steps to create the Assets VM Image for VMware vSphere. This will generate an ISO file based on the Talos VM base image containing a local cache. This image is different from the base Talos image ISO file that you will use for the EDA Kubernetes VMs, but is based on it.

**Step 1** - Go to the correct directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

**Step 2** - Generate the Assets VM OVA for VMware vSphere
: Execute the following command to generate the VMware vSphere Talos OVA for the Assets VM.

    ```bash
    make create-asset-vm-vmware-boot-ova
    ```

    The output should look similar to:

    ```
    --> INFO: List of goals: create-asset-vm-vmware-boot-ova
    docker pull ghcr.io/siderolabs/imager:v1.9.2
    v1.9.2: Pulling from siderolabs/imager
    Digest: sha256:b99d29d04df9eea89d50cb0d13d57e1e035e54cbd9970a26af99b18154e443a9
    Status: Image is up to date for ghcr.io/siderolabs/imager:v1.9.2
    ghcr.io/siderolabs/imager:v1.9.2
    skipped pulling overlay (no overlay)
    profile ready:
    arch: amd64
    platform: vmware
    secureboot: false
    version: v1.9.2
    input:
      kernel:
        path: /usr/install/amd64/vmlinuz
      initramfs:
        path: /usr/install/amd64/initramfs.xz
      baseInstaller:
        imageRef: ghcr.io/siderolabs/installer:v1.9.2
      imageCache:
        imageRef: ""
        ociPath: /image-cache.oci
    output:
      kind: image
      imageOptions:
        diskSize: 2147483648
        diskFormat: ova
      outFormat: raw
    skipped initramfs rebuild (no system extensions)
    kernel command line: talos.platform=vmware talos.config=guestinfo console=tty0 console=ttyS0 earlyprintk=ttyS0,115200 net.ifnames=0 init_on_alloc=1 slab_nomerge pti=on consoleblank=0 nvme_core.io_timeout=4294967295 printk.devkmsg=on ima_template=ima-ng ima_appraise=fix ima_hash=sha512
    disk image ready
    output asset path: /out/vmware-amd64.ova    
    ```

**Step 3** - Rename the VMware vSphere Assets VM image
: Rename the generated image to a convenient name so that you can copy or use it in the future.

    ```bash
    mv eda-cargo/talos-asset-vm-boot-imgs/vmware-amd64.ova eda-cargo/talos-asset-vm-boot-imgs/eda-asset-vm-vmware-amd64.ova
    ```

## Downloading the Assets Bundles

**Step 1** - Go to the correct directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

**Step 2** - Download the Assets Bundles
: The following command will download all Assets Bundles defined in the `bundles` folder and store them in the `eda-cargo` folder.

    ```bash
    make save-all-bundles
    ```

    /// details | Downloading individual bundles
        type: note
In case individual bundles need to be downloaded, use the following command to list the available bundles:

```bash
make ls-bundles
```

Using the following command, you can then use the following command to download a specific bundle:

```bash
make save-<bundle-name>
```

///

## Downloading the Base Talos VM Images

/// admonition | This applies to the Public environment, and is executed in the public tools-system
    type: note
///

To deploy the EDA Kubernetes VMs, the base Talos image is needed for KVM or VMware vSphere. This can also be done using the edaadm bundles folder as described below.

**Step 1** - Go to the correct directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

**Step 2** - Downloading the base Talos images
: The following command will download all images, for both KVM and VMware vSphere.

    ```bash
    make download-talos-stock-boot-media
    ```

    The output should look similar to:

    ```
    --> INFO: List of goals: download-talos-stock-boot-media
    --> Downloading boot media for vmware
        From: https://factory.talos.dev/image/903b2da78f99adef03cbbd4df6714563823f63218508800751560d3bc3557e40/v1.9.2/vmware-amd64.iso
        To: /path/to/edaadm-repository/bundles/eda-cargo/talos-stock-boot-media/vmware-amd64.iso
    ############################################################################################################################### 100.0%
        From: https://factory.talos.dev/image/903b2da78f99adef03cbbd4df6714563823f63218508800751560d3bc3557e40/v1.9.2/vmware-amd64.ova
        To: /path/to/edaadm-repository/bundles/eda-cargo/talos-stock-boot-media/vmware-amd64.ova
    ############################################################################################################################### 100.0%
    --> Downloading boot media for nocloud
        From: https://factory.talos.dev/image/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba/v1.9.2/nocloud-amd64.iso
        To: /path/to/edaadm-repository/bundles/eda-cargo/talos-stock-boot-media/nocloud-amd64.iso
    ############################################################################################################################### 100.0%
        From: https://factory.talos.dev/image/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba/v1.9.2/nocloud-amd64.raw.xz
        To: /path/to/edaadm-repository/bundles/eda-cargo/talos-stock-boot-media/nocloud-amd64.raw.xz
    ############################################################################################################################### 100.0%
    --> Downloading boot media for metal
        From: https://factory.talos.dev/image/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba/v1.9.2/metal-amd64.iso
        To: /path/to/edaadm-repository/bundles/eda-cargo/talos-stock-boot-media/metal-amd64.iso
    ############################################################################################################################### 100.0%
        From: https://factory.talos.dev/image/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba/v1.9.2/metal-amd64.raw.zst
        To: /path/to/edaadm-repository/bundles/eda-cargo/talos-stock-boot-media/metal-amd64.raw.zst
    ############################################################################################################################### 100.0%
        From: https://factory.talos.dev/image/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba/v1.9.2/metal-amd64.qcow2
        To: /path/to/edaadm-repository/bundles/eda-cargo/talos-stock-boot-media/metal-amd64.qcow2
    ############################################################################################################################### 100.0%
    ```

## Preparing the Air-Gapped Environment

After downloading all the tools, packages, repositories, bundles and images, the data needs to be made available in the Air-Gapped Enviroment. Two options are available:

1. Move the Public tools-system to the Air-Gapped environment, for instance if it is a laptop or a VM you can easily move to the Air-Gapped environment by changing its network configuration.
2. Copy the following data from the Public tools-system to the Air-Gapped tools-system. For instance using a USB key or a temporary network connection. This should include:
    * The playground repository - This will include the tools and standard installation KPT packages.
    * The edaadm repository - This will include the bundles folder holding the `eda-cargo` folder that has all the Air-Gapped data (bundles, asset VM image and Talos base VM images).

### Loading the KPT Setters image

/// admonition | This applies to the Air-Gapped environment, and is executed in the air-gapped tools-system
    type: note
///

Both setting up the Assets VM and installing EDA uses KPT. For both, it is possible that certain settings need to be configured in the process in the KPT packages. KPT uses a container called `kpt-apply-setters` for this. This image needs to be present in the local docker image cache of the air-gapped tools-system.

The container image is part of the `eda-bundle-tools` bundle in the `edaadm/bundles` list. If you used the `save-all-bundles` option when downloading the bundles, you will have that bundle on your air-gapped tools-system. If you do not have it yet, you can download the bundle on the public tools-system and copy over the content of the bundle to the air-gapped tools-system before executing the steps.

To load the `kpt-apply-setters` image from the `eda-bundle-tools` bundle, follow these steps:

**Step 1** - Go to the correct directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

**Step 2** - Import the image into the local docker image cache
: Note that the version of the bundle might update to a newer version in the future. In that case, replace the `1-0-0` with the appropriate version and the correct `kpt-apply-setters` version as well.

    ```bash
    docker load -i eda-cargo/eda-bundle-tools-1-0-0/images/srl-labs-kpt-apply-setters-0-1-1
    ```

## Deploying the Assets VM

/// admonition | This applies to the Air-Gapped environment, and is executed in the air-gapped tools-system
    type: note
///

Deploying the Assets VM is very similar to deploying an EDA Kubernetes cluster. The high level steps are:

<!-- no toc -->
* [Preparing the Assets VM EDAADM Configuration File](#preparing-the-assets-vm-edaadm-configuration-file)
* [Generating the Talos Machine Configuration Files](#generating-the-talos-machine-configuration-files)
* [Deploy the Assets VM](#deploy-the-assets-vm)
* [Bootstrap the Assets VM](#bootstrap-the-assets-vm)
* [Deploying the Assets VM Services](#deploying-the-assets-vm-services)

### Preparing the Assets VM EDAADM Configuration File

The EDAADM configuration file for the Assets VM is very similar to the EDAADM configuration file of a EDA Kubernetes environment, with a few minor changes:

* It is a config file for a single machine
* The `clusterName` must be unique and different from the EDA Kubernetes cluster
* The following additions are made to the machine definition:

    ```yaml
    enableImageCache: true
    localPathProvisioner: "/var/local-path-provisioner"
    ```

Otherwise, the configuration is very similar to the *Preparing the EDAADM configuration file* section in the official installation guide.

/// admonition | The Assets VM only needs one network interface, this should preferably be on the OAM network of the EDA Kubernetes cluster, but at a minimum reachable from the OAM network of the EDA Kubernetes cluster.
    type: note
///

/// admonition | `edaadm` still expects the definition of a storage disk in the machine definition, but this can be a reference to a non-existing disk.
    type: warning
///

#### Example Assets VM EDAADM Configuration file

The below configuration file is an example for an Assets VM using local DNS and NTP servers.

```yaml
version: 24.12.2
clusterName: eda-airgap-assets
machines:
    - name: eda-assets.domain.tld
      endpoint: 192.0.2.228
      enableImageCache: true
      localPathProvisioner: "/var/local-path-provisioner"
      interfaces:
        - name: eth0
          dhcp: false
          interface: eth0
          addresses:
            - 192.0.2.228/23
          routes:
            - network: 0.0.0.0/0
              gateway: 192.0.2.1
          mtu: 9000
      disks:
        os: /dev/vda
        storage: /dev/vdb
k8s:
    stack: ipv4
    primaryNode: eda-assets.domain.tls
    endpointUrl: https://192.0.2.228:6443
    allowSchedulingOnControlPlanes: true
    control-plane:
        - eda-assets.domain.tld
    time:
        disabled: false
        servers:
            - 192.0.2.253
            - 192.0.2.254
    nameservers:
        servers:
            - 192.0.2.254
            - 192.0.2.253
```

### Generating the Talos Machine Configuration Files

After creating the Assets VM EDAADM configuration file, the next step is to generate all the configuration files that are necessary to deploy the Kubernetes environment using Talos.

This step is very similar to the *Generating the Talos machine configurations* section in the official installation guide.

Use the `edaadm` tool to generate the Talos configuration out of the EDAADM configuration file:

```bash
edaadm generate -c eda-assets-deployment.yaml
```

The output should look similar to the following (a portion has been removed):

```
ConfigFile is eda-assets-deployment.yaml
...
[1/5] Validating Machines
[1/5] Validated Machines
[2/5] Validating Primary Node
[2/5] Validated Primary Node
[3/5] Validating Endpoint URL
[3/5] Validated Endpoint URL
[4/5] Validating Virtual IP
[4/5] Validated Virtual IP
[5/5] Validating Storage
[5/5] Validated Storage
[  OK  ] Spec is validated
Generating secrets for eda-airgap-assets
Created eda-airgap-assets/secrets.yaml
generating PKI and tokens
Created eda-airgap-assets/eda-assets.domain.tld.yaml
Created eda-airgap-assets/talosconfig.yaml
Created eda-airgap-assets/rook-ceph-operator-values.yaml
Created eda-airgap-assets/rook-ceph-cluster-values.yaml
```

### Deploy the Assets VM

The Assets VM can be deployed on a KVM or VMware vSphere environment. This process is very similar to the documented procedures in the *Deploying the Talos virtual machines* section in the official installation guide.

#### Creating the VM on a bridged network on KVM

/// admonition | This procedure is executed on the KVM Hypervisor which will host the Assets VM
    type: note
///

Difference from the procedure in the *Creating the VM on bridged networks on KVM* section in the official installation guide:

* Use the Assets VM ISO image generated by in the [Creating the KVM Assets VM Image](#creating-the-kvm-assets-vm-image) step, instead of the standard Talos KVM image.
* Use the Talos machine config file generated in the [Generating the Talos Machine Configuration Files](#generating-the-talos-machine-configuration-files) step for `user-data`.
* Make sure the root disk is set to 300GB instead of 100GB.
* No need to create a storage disk on the VM.

An example `virt-install` command to deploy the Assets VM in KVM:

```bash
virt-install -n eda-assets \ 
  --description "EDA Assets Vm for EDA" \ 
  --noautoconsole --os-type=generic \ 
  --memory 16384 --vcpus 4 --cpu host \ 
  --disk eda-assets-rootdisk.qcow2,format=qcow2,bus=virtio,size=300 \ 
  --cdrom eda-asset-vm-nocloud-amd64.iso  \ 
  --disk eda-assets-data.iso,device=cdrom \ 
  --network bridge=br0,model=virtio
```

#### Creating the VM on a bridged network on VMware vSphere

/// admonition | This procedure is executed on the Air-Gapped tools-system
    type: note
///

Difference from the procedure in the *Creating the VM on bridged networks on VMware vSphere* section in the official installation guide:

* Use the Assets VM ISO image generated by in the [Creating the VMware Assets VM Image](#creating-the-vmware-assets-vm-image) step, instead of the standard Talos VMware image.
* Use the Talos machine config file generated in the [Generating the Talos Machine Configuration Files](#generating-the-talos-machine-configuration-files) step for `user-data`.
* No need to create a storage disk on the VM.
* After deploying the VM using the OVA image:
    * Increase the number of vCPUs to 4.
    * Increase the memory to 16G.
    * Increase the main disk size to 300G. On boot, Talos automatically extends the file system.
    * Enable 100% resource reservation for the CPU, memory and disk.

Similar to the *Creating the VM on bridged networks on VMware vSphere* section in the official installation guide, create a base64 encoded hash from the Talos machine configuration for the node. For example:

```bash
export NODECONFIG=$(base64 -i eda-assets.domain.tld.yaml)
```

An example `ovftool` command to deploy the Assets VM in VMware vSphere:

```bash
ovftool --acceptAllEulas --noSSLVerify \ 
 -dm=thin \ 
 -ds=DATASTORE \ 
 -n=eda-assets \ 
 --net:"VM Network=OAM" \ 
 --prop:talos.config="${NODECONFIG}" \ 
eda-asset-vm-vmware-amd64.ova \ 
vi://administrator%40vsphere.local@vcenter.domain.tld/My-DC/host/My-Cluster/Resources/My-Resource-Group
```

### Bootstrap the Assets VM

/// admonition | This applies to the Air-Gapped environment, and is executed in the air-gapped tools-system
    type: note
///

Similar to bootstrapping an EDA Kubernetes cluster, the Assets VM can be bootstrapped using the `edaadm` tool.

#### Bootstrapping Kubernetes on the Assets VM

Use the `edaadm` command with the EDAADM configuration file for the Assets VM to bootstrap Kubernetes:

```bash
edaadm boostrap-k8s -c eda-assets-deployment.yaml
```

#### Obtaining the Kubernetes Config File for kubectl

Use the `edaadm` command to obtain the Kubernetes configuration file for use with kubectl. The following parameter is relevant for this procedure:

**Step 1** - Obtain the Kubernetes configuration file.
: Execute the following command in the folder with the `eda-assets-deployment.yaml` EDAADM configuration file.

    ```bash
    edaadm get-kubeconfig -c eda-assets-deployment.yaml
    ```

**Step 2** - Configure the Kubernetes configuration file in your environment.
: You can configure your environment to use the ​kubeconfig​ file for use with the `kubectl` command.

    ```bash
    export KUBECONFIG=eda-airgap-assets/kubeconfig
    ```

**Step 3** - Inspect your server and check if all nodes are up and running.
: You can use the typical `kubectl` commands.

    ```bash
    kubectl get nodes
    ```

When the node is up and ready, continue with deploying the Assets VM services.

### Deploying the Assets VM Services

/// admonition | This applies to the Air-Gapped environment, and is executed in the air-gapped tools-system
    type: note
///

<!--
/// details | Defining custom usernames and passwords for the services
    type: note
In case custom usernames and passwords must be provided for the git server and web server, follow these steps:

**Git Server Username and Password**

By default, the git server default username is `eda` and default password is `eda`. To change this, use the following command to generate a base64 hash for the username, and a separate one for the password:

```bash
echo -n 'new-username' | base64
```

```bash
echo -n 'new-password' | base64
```

Keep the output of these two commands saved somewhere, as you will need to use them in the next step, as well as when installing the EDA Talos Kubernetes cluster and EDA.

Now export these values as environment variables in your shell so they can be used by the kpt platform to configure the services properly when you execute the commands later on in this section.:

```bash
export GOGS_ADMIN_USER="base64 encoded value for the username"
export GOGS_ADMIN_PASS="base64 encoded value for the password"
```

**Web Server Username and Password**

By default, the web server default username is `eda` and default password is `eda`. To change this, use the following command to generate a new htpasswd hash. The command will request to type a password twice and output a string.

```bash
htpasswd -n new-username
```

Use the string from this command and also do a base64 encoding of it:

```bash
echo -n 'new-username:...' | base64
```

Keep the output of this command saved somewhere, as you will need to use them in the next step, as well as when installing the EDA Talos Kubernetes cluster and EDA.

Now export the value as environment variable in your shell so it can be used by the kpt platform to configure the services properly when you execute the commands later on in this section.

```bash
export LIGHTTPD_EDA_HTPASSWD="base64 encoded htpasswd output"
```

///
-->

After deploying and bootstrapping the Assets VM itself, the container registry, git server and web server need to be deployed.

**Step 1** - Go to the correct directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `kpt` folder.

    ```bash
    cd path/to/edaadm-repository/kpt
    ```

**Step 2** - Deploy the Assets VM services
: Make sure your kubeconfig environment variable points to the kubeconfig of the Assets VM as you got it from the [Obtaining the Kubernetes Config File for `kubectl`](#obtaining-the-kubernetes-config-file-for-kubectl) section.

    ```bash
    make eda-setup-shipyard
    ```

## Uploading the Assets to the Assets VM

/// admonition | This applies to the Air-Gapped environment, and is executed in the air-gapped tools-system
    type: note
///

Now that the Assets VM and its services are up and running, all the assets downloaded previously, can be uploaded to the Assets VM.

**Step 1** - Go to the correct directory in the `edaadm` repository
: In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

**Step 2** - Upload the assets
: Make sure your kubeconfig environment variable points to the kubeconfig of the Assets VM as you got it from the [Obtaining the Kubernetes Config File for `kubectl`](#obtaining-the-kubernetes-config-file-for-kubectl) section.

    Make sure to replace the `ASSET_HOST` IP with the IP of your Asset VM.

    ```bash
    make load-all-bundles \
      ASSET_HOST=192.0.2.228 \
      ASSET_HOST_GIT_USERNAME="ZWRh" \
      ASSET_HOST_GIT_PASSWORD="ZWRh" \
      ASSET_HOST_ARTIFACTS_USERNAME="ZWRh" \
      ASSET_HOST_ARTIFACTS_PASSWORD="ZWRh"
    ```

    /// admonition | The username and passwords will be configurable in the near future.
        type: note
    ///

Once all uploads have finished successfully, the Assets VM is ready for use with the installation process of EDA.

## Updating the EDAADM Configuration File for the EDA Kubernetes Cluster

/// admonition | This applies to the Air-Gapped environment, and is executed in the air-gapped tools-system
    type: note
///

To use the Assets VM instead of the Internet for all of the resources needed by the EDA Talos Kubernetes cluster and EDA itself, the EDAADM configuration file used for the EDA Talos Kubernetes cluster needs to be changed in a few ways:

1. Preferably, no proxy configuration should be present, as the Assets VM should be directly reachable
2. A new `mirror` subsection defining the mirror configuration needs to be defined in the `k8s` section. This will look similar to the following:

    ```
        mirror:
          name: 192.0.2.228
          url: https://192.0.2.228
          insecure: true
          overridePath: false
          skipFallback: true
          mirrors:
            - docker.io
            - gcr.io
            - ghcr.io
            - registry.k8s.io
            - quay.io
    ```

Below some more details about the second and third item in the list.

No other changes are needed to run the installation process of the EDA Talos Kubernetes cluster and EDA itself.

### Example EDAADM Configuration File

Using the example configuration file from the *Example EDAADM configuration file* section of the official installation guide, the necessary changes have been made.

/// details | Example EDAADM Configuration File
    type: note

```yaml
version: 24.12.1 
clusterName: eda-compute-cluster 
machines: 
    - name: eda-node01 
      endpoint: "192.0.2.11" 
      interfaces: 
        - name: eth0 
          dhcp: false 
          interface: eth0 
          addresses: 
            - 192.0.2.11/24 
          routes: 
            - network: 0.0.0.0/0 
              gateway: 192.0.2.1 
          mtu: 9000 
        - name: eth1 
          dhcp: false 
          interface: eth1 
          addresses: 
            - 203.0.113.11/24 
          mtu: 9000 
      disks: 
        os: /dev/vda 
        storage: /dev/vdb 
    - name: eda-node02 
      endpoint: "192.0.2.12" 
      interfaces: 
        - name: eth0 
          dhcp: false 
          interface: eth0 
          addresses: 
            - 192.0.2.12/24 
          routes: 
            - network: 0.0.0.0/0 
              gateway: 192.0.2.1 
          mtu: 9000 
        - name: eth1 
          dhcp: false 
          interface: eth1 
          addresses: 
            - 203.0.113.12/24 
          mtu: 9000 
      disks: 
        os: /dev/vda 
        storage: /dev/vdb 
    - name: eda-node03 
      endpoint: "192.0.2.13" 
      interfaces: 
        - name: eth0 
          dhcp: false 
          interface: eth0 
          addresses: 
            - 192.0.2.13/24 
          routes: 
            - network: 0.0.0.0/0 
              gateway: 192.0.2.1 
          mtu: 9000 
        - name: eth1 
          dhcp: false 
          interface: eth1 
          addresses: 
            - 203.0.113.13/24 
          mtu: 9000 
      disks: 
        os: /dev/vda 
        storage: /dev/vdb 
    - name: eda-node04 
      endpoint: "192.0.2.14" 
      interfaces: 
        - name: eth0 
          dhcp: false 
          interface: eth0 
          addresses: 
            - 192.0.2.14/24 
          routes: 
            - network: 0.0.0.0/0 
              gateway: 192.0.2.1 
          mtu: 9000 
        - name: eth1 
          dhcp: false 
          interface: eth1 
          addresses: 
            - 203.0.113.14/24 
          mtu: 9000 
      disks: 
        os: /dev/vda 
    - name: eda-node05 
      endpoint: "192.0.2.15" 
      interfaces: 
        - name: eth0 
          dhcp: false 
          interface: eth0 
          addresses: 
            - 192.0.2.15/24 
          routes: 
            - network: 0.0.0.0/0 
              gateway: 192.0.2.1 
          mtu: 9000 
        - name: eth1 
          dhcp: false 
          interface: eth1 
          addresses: 
            - 203.0.113.15/24 
          mtu: 9000 
      disks: 
        os: /dev/vda 
    - name: eda-node06 
      endpoint: "192.0.2.16" 
      interfaces: 
        - name: eth0 
          dhcp: false 
          interface: eth0 
          addresses: 
            - 192.0.2.16/24 
          routes: 
            - network: 0.0.0.0/0 
              gateway: 192.0.2.1 
          mtu: 9000 
        - name: eth1 
          dhcp: false 
          interface: eth1 
          addresses: 
            - 203.0.113.16/24 
          mtu: 9000 
      disks: 
        os: /dev/vda 
k8s: 
    stack: ipv4 
    primaryNode: eda-node01 
    endpointUrl: https://192.0.2.5:6443 
    allowSchedulingOnControlPlanes : true 
    control-plane: 
        - eda-node01
        - eda-node02
        - eda-node03
    worker:
        - eda-node04
        - eda-node05
        - eda-node06
    vip:
        ipv4: 192.0.2.5
        interface: eth0
    time:
        disabled: false
        servers:
            - 192.0.2.253
            - 192.0.2.254
    nameservers:
        servers:
            - 192.0.2.253
            - 192.0.2.254
    mirror:
      name: 192.0.2.228
      url: https://192.0.2.228
      insecure: true
      overridePath: false
      skipFallback: true
      mirrors:
        - docker.io
        - gcr.io
        - ghcr.io
        - registry.k8s.io
        - quay.io
```

///

## Bootstrapping the EDA Talos Kubernetes Cluster

/// admonition | This applies to the Air-Gapped environment, and is executed in the air-gapped tools-system
    type: note
///

The only change needed in the procedure to bootstrap the EDA Talos Kubernetes cluster, is in the *Setting up the Rook Ceph storage cluster* in the official installation guide.

### Setting up the Rook Ceph Storage Cluster

To deploy Rook Ceph, instead of following the steps in the *Setting up the Rook Ceph storage cluster* section in the install guide, follow these steps.

/// admonition | Make sure to use the correct paths and the correct Assets VM IP in the below commands.
    type: note
///

**Step 1** - Deploy the Rook Ceph operator
: Using the `rook-ceph-operator-values.yaml` file that `edaadm` generated based on the configuration, deploy the Rook Ceph Operator using the Rook Ceph charts present on the Assets VM.

    ```bash
    helm install --create-namespace \
      --namespace rook-ceph \
      --version v1.15.0 \
      -f path/to/rook-ceph-operator-values.yaml \
      rook-ceph \
      http://eda:eda@<ASSETS VM IP>/artifacts/rook-ceph-v1.15.0.tgz
    ```

**Step 2** - Deploy the Rook Ceph cluster
: Using the `rook-ceph-cluster-values.yaml` file that the `edaadm` tool generated, deploy the Rook Ceph Cluster.

    ```bash
    helm install \ 
      --namespace rook-ceph \ 
      --set operatorNamespace=rook-ceph \ 
      -f path/to/rook-ceph-cluster-values.yaml \ 
      rook-ceph-cluster \
      http://eda:eda@<ASSETS VM IP>/artifacts/rook-ceph-cluster-v1.15.0.tgz
    ```

**Step 3** - Wait for the deployment to finish
: This is similar to the **Step 4** in the *Setting up the Rook Ceph storage cluster* section in the install guide

## Installing the EDA Application

/// admonition | This applies to the Air-Gapped environment, and is executed in the air-gapped tools-system
    type: note
///

In the standard installation procedure as described in the *Installing the EDA application* section of the official installation guide, two changes need to be made to the `prefs.mk` file to use the Assets VM instead of the internet:

* Preferably, remove any proxy configuration as the Assets VM should be reachable directly by the EDA Kubernetes cluster
* Add the following settings to the `prefs.mk` file, where the `ASSET_HOST` setting points to the IP of the Assets VM:

    ```
    USE_ASSET_HOST=1
    ASSET_HOST=192.0.2.228
    ASSET_HOST_GIT_USERNAME="eda"
    ASSET_HOST_GIT_PASSWORD="eda"
    ASSET_HOST_ARTIFACTS_USERNAME="eda"
    ASSET_HOST_ARTIFACTS_PASSWORD="eda"
    ```

    /// admonition | The usernames and passwords will be changable in the near future.
        type: note
    ///

### Example `prefs.mk` file

Below is an example `prefs.mk` file, similar to the one present in the *Installing the EDA application* section of the official installation guide:

```
NO_KIND=1
USE_ASSET_HOST=1
ASSET_HOST=192.0.2.228
ASSET_HOST_GIT_USERNAME="eda"
ASSET_HOST_GIT_PASSWORD="eda"
ASSET_HOST_ARTIFACTS_USERNAME="eda"
ASSET_HOST_ARTIFACTS_PASSWORD="eda"
METALLB_VIP=203.0.113.10/32
EXT_DOMAIN_NAME=eda.domain.tld 
EXT_HTTP_PORT=80 
EXT_HTTPS_PORT=443 
EXT_IPV4_ADDR=203.0.113.10
EXT_IPV6_ADDR=""
LLM_API_KEY=...
```

### Installing Nokia EDA

In the *Installing Nokia EDA* section of the official installation guide, **Step 1** and **Step 2** can be skipped as this was done in the preparation of the Air-Gapped tools-system.

The other steps can be executed as documented.
