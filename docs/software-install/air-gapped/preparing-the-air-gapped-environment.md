# Preparing the Air-gapped environment

After [preparing](preparing-the-assets-vm.md) the Assets VM and [downloading](downloading-the-assets.md) the necessary assets, the fetched data needs to be made available in the Air-gapped environment. Two options are available:

1. Move the system that was used to prepare the Assets VM to the Air-gapped environment. For instance, if it is a laptop or a VM, you can move to the Air-gapped environment by changing its network configuration.
2. Copy the data from the system that was used to prepare the Assets VM to the Air-gapped environment using a USB key or a temporary network connection. The data should include:
    * The playground repository cloned during the ["Preparing for installation"](../preparing-for-installation.md) step.
    * The edaadm repository which includes the `eda-cargo` folder holding the Air-gapped data (bundles, asset VM image and Talos base VM images). The `eda-cargo` folder was populated during the [preparing](preparing-the-assets-vm.md) the Assets VM and [downloading](downloading-the-assets.md) the necessary assets steps.

## Loading the Kpt Setters image

/// admonition | Note
    type: subtle-note
These steps are to be executed in the air-gapped environment.
///

The procedures for setting up the Assets VM and installing EDA use [Kpt](https://kpt.dev) - a package manager for Kubernetes. Kpt relies on the `kpt-apply-setters` container to be present in the local Docker image cache of the air-gapped system to be able to perform its operations.  
The container image is part of the `eda-bundle-tools` bundle in the `edaadm/bundles` list. If you used the `save-all-bundles` option when downloading the assets, you will have that bundle on your air-gapped system. If you do not have it yet, you can download the bundle on the system with Internet and copy over the content of the bundle to the air-gapped environment before executing the steps.

To load the `kpt-apply-setters` image from the `eda-bundle-tools` bundle, follow these steps:

/// html | div.steps

1. Go to the `edaadm` repository directory.

    Change into the `edaadm` repository that you have copied from the Internet-connected system:

    ```bash
    cd path/to/edaadm
    ```

2. Import the image into the local docker image cache

    Note that the version of the bundle might update to a newer version in the future. In that case, replace the `1-0-0` with the appropriate version and the correct `kpt-apply-setters` version as well.

    ```bash
    docker load -i ./bundles/eda-cargo/eda-bundle-tools-1-0-0/images/srl-labs-kpt-apply-setters-0-1-1
    ```
