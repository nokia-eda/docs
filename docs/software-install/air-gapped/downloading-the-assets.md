# Downloading the Assets

/// admonition | Caution
    type: note
This applies to the Public environment, and is executed in the public tools-system.
///

There are two types of assets that need to be downloaded:

* Assets Bundles - The bundles that contain all the resources needed to run Nokia EDA. This includes container images, repositories, tools and more.
* Base Talos VM Image - The base images for the EDA Kubernetes nodes (VMs) that will run the EDA application.

/// details | Make sure the user in the public tools-system is logged in for `docker.io`.
    type: warning
Docker has started to rate limit pulling images from docker.io more aggressively. To avoid the rate limit, ensure that you have a user account on docker.io and that you logged into it on your public tools-system with:

```bash
docker login docker.io
```

///

## Downloading the Assets Bundles

/// html | div.steps

1. Go to the correct directory in the `edaadm` repository.

    In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

2. Download the Assets Bundles.

    The following command will download all Assets Bundles defined in the `bundles` folder and store them in the `eda-cargo` folder.

    ```bash
    make save-all-bundles
    ```

    /// details | Downloading individual bundles
        type: subtle-note
    In case individual bundles need to be downloaded, use the following command to list the available bundles:

    ```bash
    make ls-bundles
    ```

    Using the following command, you can then use the following command to download a specific bundle:

    ```bash
    make save-<bundle-name>
    ```

    ///

///

## Downloading the Base Talos VM Images

To deploy the EDA Kubernetes VMs, the base Talos image is needed for KVM or VMware vSphere. This can also be done using the edaadm bundles folder as described below.

/// html | div.steps

1. Go to the correct directory in the `edaadm` repository.

    In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

2. Download the base Talos images.

    The following command downloads all images for both KVM and VMware vSphere.

    ```bash
    make download-talos-stock-boot-media
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

///
