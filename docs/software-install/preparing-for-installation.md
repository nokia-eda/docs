# Preparing for installation

## Download the EDA Installation playground

Ensure that your Linux installation[^1] environment meets the requirements described in [Installation platform requirements](eda-installation-overview.md#installation-platform-requirements).

Clone the playground repository to your tools-system.

```bash
git clone https://github.com/nokia-eda/playground && cd playground 
```

### Installing additional tools

Download additional tools that can be used during the installation.

```bash
make download-tools
```

As a result of this command, the `kind`, `kubectl`, `kpt`, and `yq` utilities will be installed in the `./tools` directory.

### Obtaining the EDA packages

EDA is packaged using the [Kubernetes Package Tool](https://kpt.dev) (kpt). EDA uses this package manager tool to install core EDA components. The installer downloads two kpt packages by downloading their relevant git repositories.

To obtain the EDA package, enter the following command:

```
make download-pkgs
```

This command downloads the following git repositories to their respective directories:

* EDA kpt package in the `eda-kpt` directory
* EDA built-in catalog in the `catalog` directory

## Download the EDA EDAADM repository

Ensure that your Linux installation environment meets the requirements described in [Installation platform requirements](eda-installation-overview.md#installation-platform-requirements).

Clone the EDAADM repository to your tools system and change to the directory.

```bash
git clone https://github.com/nokia-eda/edaadm && cd edaadm
```

### Download extra tools

#### Bundle tools

Go to the bundles directory in the `edaadm` repository.  

```bash title="execute from the root of the edaadm repository"
cd bundles
```

And download the tools for the bundles.

```bash title="execute from the bundler directory"
make download-tools
```

This step downloads[^2] the `edaadm` CLI tool for your architecture in the `edaadm/bundles/tools` directory.

The `edaadm` tool is used to generate configuration files for use while deploying the Talos Linux virtual machines and the Kubernetes environment. You can copy or move the `edaadm` tool from the `./tools` directory to a location in your `$PATH` to make it available in your shell for future use.

#### kpt tools

After downloading the tools for bundles, download the tools for kpt. Go to the kpt directory in the `edaadm` repository.

```bash title="relative path assumes you are in the bundles directory"
cd ../kpt
```

And download the tools for the kpt package.

```bash
make download-tools
```

This step downloads the `kpt` and `kubectl` tools in the `edaadm/kpt/tools` directory.

## Download the Talos machine image

The `edaadm` tool provides you with the URL to download the latest Talos machine image for use with VMware or KVM.

To deploy the Talos Kubernetes environment, download the Talos Machine image based on the environment in which you want to deploy the VMs.

### Downloading the KVM image

Use the `edaadm` tool to display the URL from where you can download the latest image for use with KVM for the supported Talos version.

```
edaadm images --mach-type nocloud
```

<div class="embed-result">
```
Schematic ID is :376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba
Asset URLs are:
https://factory.talos.dev/image/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba/v1.9.2/nocloud-amd64.iso
https://factory.talos.dev/image/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba/v1.9.2/nocloud-amd64.raw.xz
```
</div>

Download the `nocloud-amd64.iso` image from the ISO URL, filepath.iso.

You can download using your browser or you can use the curl command.

### Downloading the VMware OVA image

Use the `edaadm` tool to display the URL from where you can download latest image for use with VMware vSphere for the supported Talos version.

```
edaadm images --mach-type vmware
```

<div class="embed-result">
```
Schematic ID is :903b2da78f99adef03cbbd4df6714563823f63218508800751560d3bc3557e40
Asset URLs are:
https://factory.talos.dev/image/903b2da78f99adef03cbbd4df6714563823f63218508800751560d3bc3557e40/v1.9.2/vmware-amd64.iso
https://factory.talos.dev/image/903b2da78f99adef03cbbd4df6714563823f63218508800751560d3bc3557e40/v1.9.2/vmware-amd64.ova
```
</div>

Download the `vmware-amd64.ova` image from the OVA URL, filepath.ova.

You can download using your browser or you can use the curl or wget commands. You can also use the URL directly with the ovftool command to deploy the OVA to your VMware vSphere environment.

[^1]: This system might also be referred to as the "tools-system" further in this documentation.
[^2]: The `edaadm` binary for different platforms can be manually downloaded from https://github.com/nokia-eda/edaadm/releases/.
