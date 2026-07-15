# Preparing for installation

## Download the Nokia EDA installation playground

Ensure that your Linux installation[^1] environment meets the requirements described in [Installation platform requirements](index.md#installation-platform-requirements).

Clone the playground repository to your tools-system.

```bash
git clone https://github.com/nokia-eda/playground && cd playground 
```

### Installing tools

Download the CLI tools that the installation process relies on.

```bash
make download-tools
```

As a result of this command, the `kind`, `edactl`, `kubectl`, `k9s`, `kpt`, `helm` and `yq` utilities will be installed in the `./tools` directory.

### Obtaining the Nokia EDA packages

Nokia EDA is packaged using the [Kubernetes Package Tool](https://kpt.dev) (kpt). Nokia EDA uses this package manager tool to install core Nokia EDA components. The installer downloads two kpt packages by downloading their relevant git repositories.

To obtain the Nokia EDA package, enter the following command:

```
make download-pkgs
```

This command downloads the following git repositories to their respective directories:

* Nokia EDA kpt package in the `eda-kpt` directory
* Nokia EDA built-in catalog in the `catalog` directory

## Download edaadm tools

Ensure that your Linux installation environment meets the requirements described in [Installation platform requirements](index.md#installation-platform-requirements).

Clone the EDAADM repository:

```bash
git clone https://github.com/nokia-eda/edaadm && cd edaadm
```

The CLI tool that orchestrates the configuration and installation of the Nokia EDA platform in a production environment is called `edaadm`. To download `edaadm` and the tools it relies on, run the following commands from the root of the `edaadm` repository:

```bash
make -C bundles/ download-tools
make -C kpt/ download-tools
```

This step downloads[^2] the `edaadm` CLI tool for your architecture in the `./bundles/tools` directory. You can copy the `edaadm` binary from the `./bundles/tools` directory to a location in your `$PATH` to make it available in your shell for future use, for example:

```bash title="copying edaadm to /usr/local/bin"
sudo cp bundles/tools/edaadm* /usr/local/bin/edaadm
```

/// note | Upgrading <code>edaadm</code> tool
Running the latest version of the `edaadm` tool is recommended. To upgrade the `edaadm` tool, perform `git pull` in the `edaadm` repository to update the local repository to the latest version and execute the `make -C bundles/ download-tools` command to download the latest available `edaadm` binary.

This will download the latest `edaadm-<version>` binary to the `./bundles/tools` directory.  Copy it to the `/usr/local/bin` directory to replace the older version of the `edaadm` binary:

```bash title="copying edaadm to /usr/local/bin"
sudo cp bundles/tools/edaadm* /usr/local/bin/edaadm

```

///

## Download the Talos machine image

The `edaadm` tool provides you with the URL to download the latest Talos machine image for use with VMware or KVM.

To deploy the Talos Kubernetes environment, download the Talos Machine image based on the environment in which you want to deploy the VMs.

### Downloading the KVM image

Use the `edaadm` tool to display the URL from where you can download the latest image for use with KVM for the supported Talos version.

```
edaadm images --mach-type nocloud
```

<div class="embed-result">
```{.text .no-copy .no-select}
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
```{.text .no-copy .no-select}
Schematic ID is :903b2da78f99adef03cbbd4df6714563823f63218508800751560d3bc3557e40
Asset URLs are:
https://factory.talos.dev/image/903b2da78f99adef03cbbd4df6714563823f63218508800751560d3bc3557e40/v1.9.2/vmware-amd64.iso
https://factory.talos.dev/image/903b2da78f99adef03cbbd4df6714563823f63218508800751560d3bc3557e40/v1.9.2/vmware-amd64.ova
```
</div>

Download the `vmware-amd64.ova` image from the OVA URL, filepath.ova.

You can download using your browser or you can use the curl or wget commands. You can also use the URL directly with the `ovftool` command to deploy the OVA to your VMware vSphere environment.

[^1]: This system might also be referred to as the "tools-system" further in this documentation.
[^2]: The `edaadm` binaries for different platforms can be found at https://github.com/nokia-eda/edaadm/releases/.
