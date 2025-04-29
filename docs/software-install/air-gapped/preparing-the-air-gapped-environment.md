# Preparing the Air-gapped environment

After downloading all the tools, packages, repositories, bundles and images, the data needs to be made available in the Air-Gapped Enviroment. Two options are available:

1. Move the Public tools-system to the Air-Gapped environment. For instance, if it is a laptop or a VM, you can easily move to the Air-Gapped environment by changing its network configuration.
2. Copy the data from the Public tools-system to the Air-Gapped tools-system using a USB key or a temporary network connection. The data should include:
    * The playground repository which includes the tools and standard installation KPT packages.
    * The edaadm repository which includes the bundles folder holding the `eda-cargo` folder that has all the Air-Gapped data (bundles, asset VM image and Talos base VM images).

## Loading the KPT Setters image

/// admonition | Note
    type: subtle-note
This applies to the Air-Gapped environment, and is executed in the air-gapped tools-system
///

The procedures for setting up the Assets VM and installing EDA use KPT. For both tasks, you may need to configure some setting in the KPT packages; KPT uses a container called kpt-apply-setters for this purpose. This image must be present in the local Docker image cache of the air-gapped tools-system.

The container image is part of the `eda-bundle-tools` bundle in the `edaadm/bundles` list. If you used the `save-all-bundles` option when downloading the bundles, you will have that bundle on your air-gapped tools-system. If you do not have it yet, you can download the bundle on the public tools-system and copy over the content of the bundle to the air-gapped tools-system before executing the steps.

To load the `kpt-apply-setters` image from the `eda-bundle-tools` bundle, follow these steps:

/// html | div.steps

1. Go to the correct directory in the `edaadm` repository

    In the `edaadm` repository that you have cloned or downloaded, go to the `bundles` folder.

    ```bash
    cd path/to/edaadm-repository/bundles
    ```

2. Import the image into the local docker image cache

    Note that the version of the bundle might update to a newer version in the future. In that case, replace the `1-0-0` with the appropriate version and the correct `kpt-apply-setters` version as well.

    ```bash
    docker load -i eda-cargo/eda-bundle-tools-1-0-0/images/srl-labs-kpt-apply-setters-0-1-1
    ```
