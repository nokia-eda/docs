# Downloading the assets

/// admonition | Caution
    type: note
Run these steps in the public environment, which has Internet access.
///

The assets download operation fetches container images, Git repositories, and other artifacts needed to run Nokia EDA and its applications, and stores them on the local machine's disk.

## Downloading the Nokia EDA Assets Bundles

Nokia EDA asset bundles contain the resources needed to run Nokia EDA and its applications. These resources include container images, repositories, tools, and more.

The user is free to choose which bundles to download based on the needs of the air-gapped environment, with the default bundle list being the only mandatory one. The procedure for downloading the bundles is as follows:

/// html | div.steps

1. Ensure you have changed into the directory of the [cloned `edaadm` repository](../preparing-for-installation.md#download-edaadm-tools).

    ```bash title="changing into edaadm repository directory"
    cd path/to/edaadm
    ```

2. Select Nokia EDA version.

    Set the `EDA_CORE_VERSION` and `EDA_APPS_VERSION` environment variables in your shell to the target Nokia EDA release version. Otherwise, the latest version is assumed. This ensures that the assets are downloaded for the correct version of Nokia EDA.

    ```bash
    export EDA_CORE_VERSION=-{{ eda_version }}-
    export EDA_APPS_VERSION=-{{ eda_version }}-
    ```

3. Download the default assets bundle list.  

    The [default assets bundle list](../air-gapped/asset-bundles.md#bundle-lists) contains the core components and applications for Nokia EDA and must be available in the air-gapped environment.

    ```bash
    make -C bundles/ save-default-bundles
    ```

    The command will download the bundles from the default bundle list and store the downloaded assets in the `eda-cargo` folder.

4. Download optional asset bundles.  

    In case additional application or simulator bundles are needed, they can be downloaded with respective make targets:

    ```bash
    make -C bundles/ save-<bundle-list-or-bundle>
    ```

    Replace `<bundle-list-or-bundle>` with one of the following:

    * any of the available [bundle lists](../air-gapped/asset-bundles.md#bundle-lists)
    * individual bundle names from the `make -C bundles/ ls-all-bundles` output.
    * user bundles from the `make -C bundles/ ls-user-bundles` output.

5. Note the bundle names.

    The bundle names will be used in the upload step to upload the assets to the Assets Host or individual services capable of serving the downloaded assets in the air-gapped environment. Therefore, make sure to note the bundle names you used in the download step.
///

## Downloading the Base Talos VM images

If Nokia EDA is deployed on its own Talos Kubernetes cluster, download the base Talos OS boot media. The command below fetches images for KVM (`nocloud`), VMware vSphere, and bare metal.

/// html | div.steps

1. Ensure you are in the `edaadm` repository.

    In case you have changed directories, ensure that you are in the `edaadm` repository.

    ```bash title="changing into edaadm repository directory"
    cd path/to/edaadm
    ```

2. Download the base Talos images.

    The following command downloads boot media for KVM (`nocloud`), VMware vSphere, and bare metal.

    ```bash
    make -C bundles/ download-talos-stock-boot-media
    ```

    The output should look similar to the following:

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

    The downloaded images are stored in `./bundles/eda-cargo/talos-stock-boot-media/` and provide the base Talos boot media for the Nokia EDA Kubernetes cluster nodes.

///

## Downloading the EDA Assets VM components

If you choose to use the EDA Assets VM for all or some of the hosting services required to host the downloaded assets in the air-gapped environment, you need to download the EDA Assets VM components.

> Read more on different [assets hosting models](../air-gapped/hosting-assets.md) available.

/// html | div.steps

1. Ensure you are in the `edaadm` repository.

    In case you have changed directories, ensure that you are in the `edaadm` repository.

    ```bash title="changing into edaadm repository directory"
    cd path/to/edaadm
    ```

2. Download the EDA Assets VM cache.

    ```bash
    make -C bundles/ create-assets-host-bootstrap-image-cache
    ```

3. Create the EDA Assets VM boot media.

    Based on the target hypervisor, run the appropriate command to create the EDA Assets VM boot media:

    /// tab | KVM

    ```bash
    make -C bundles/ create-asset-vm-nocloud-boot-iso
    ```

    The ISO disk image will be saved at the relative path `./bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-nocloud-amd64.iso`.
    ///

    /// tab | VMware vSphere

    > This command requires Linux kernel version 6 or higher[^1]

    ```bash
    make -C bundles/ create-asset-vm-vmware-boot-ova
    ```

    The OVA disk image will be saved at the relative path `./bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-vmware-amd64.ova`.
    ///

///

## Transferring the assets to the air-gapped environment

The following components need to be transferred to the air-gapped environment:

* The `playground` repository cloned during the ["Preparing for installation"](../preparing-for-installation.md#download-the-nokia-eda-installation-playground) step with the downloaded tools.
* The `edaadm` repository, which includes the downloaded assets.

The assets can be transferred to the air-gapped environment in several ways:

* By archiving the downloaded assets and transferring the archive to the air-gapped environment using the USB drive, network transfer, cloud storage service, etc.
* By moving the Installer host with the downloaded assets to the air-gapped environment.
* By cloning the Installer host disk image and creating a new VM from the cloned image in the air-gapped environment.

If you transfer the assets using archives, each archive must contain the complete repository, not only the downloaded asset files.

/// html | div.steps

1. Archiving the `edaadm` repository

    The `edaadm` repository archive can be created using the `tar` command executed from the root of the `edaadm` repository:

    ```bash
    tar -cf ../edaadm.tar -C .. edaadm
    ```

    This creates an archive file named `edaadm.tar` in the parent directory of the `edaadm` repository. Transfer the archive to the air-gapped environment using your chosen method.

2. Archiving the `playground` repository  

    The `playground` repository archive can be created using the `tar` command executed from the root of the `playground` repository:

    ```bash
    tar -cf ../playground.tar -C .. playground
    ```

    This creates an archive file named `playground.tar` in the parent directory of the `playground` repository. Transfer the archive to the air-gapped environment using your chosen method.
///

In the air-gapped environment, extract the archive using the `tar` command:

```bash title="extracting the archive in the air-gapped environment"
tar -xf edaadm.tar
```

Downloading the assets only stores them on the local machine's disk. Once the assets are downloaded, the next step is to [choose the hosting model](hosting-assets.md) for the assets in the air-gapped environment.

[:octicons-arrow-right-24: Hosting the assets](hosting-assets.md)

[^1]: See https://github.com/siderolabs/talos/issues/9264#issuecomment-2426756838
