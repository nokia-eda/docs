# Preparing the Assets VM

The Assets VM will run as a single Virtual Machine inside the Air-Gapped environment. This VM will hold all of the assets and can be used across multiple deployments and EDA versions, containing the assets for multiple versions.

These steps help create the Assets VM from a base Talos VM image and populate it with the local cache needed to deploy the Assets VM in the Air-Gapped environment.

/// admonition | Caution
    type: note
These steps are meant to be executed in the public environment with Internet access.
///

## Creating Assets VM Image Cache

Before creating the Assets VM Image for a specific environment, an image cache must be created that will contain the necessary bootstrap images used by the Assets VM.

Change into the cloned `edaadm` repository root directory.

```bash
cd path/to/edaadm
```

And run the following command to create the image cache:

```bash
make -C bundles/ create-assets-host-bootstrap-image-cache
```

## Creating the KVM Assets VM Image

/// admonition | Note
    type: subtle-note
This is only needed if you plan to deploy the Assets VM on KVM.
///

Follow these steps to create the Assets VM Image for KVM. This will generate an ISO file based on the Talos VM base image containing a local cache. This image is different from the base Talos image ISO file that you will use for the EDA Kubernetes VMs, but is based on it.

/// html | div.steps

1. Change into the `edaadm` repository.

    In case you have changed directories, ensure that you are in the `edaadm` repository.

    ```bash title="changing into edaadm repository directory"
    cd path/to/edaadm
    ```

2. Generate the Assets VM ISO for KVM.

    Execute the following command to generate the KVM Talos ISO for the Assets VM.

    ```bash
    make -C bundles/ create-asset-vm-nocloud-boot-iso
    ```

    //// details | Output example
        type: subtle-note
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

    ////

    The ISO disk image will be saved at the relative path `./bundles/eda-cargo/talos-asset-vm-boot-imgs/nocloud-amd64.iso`.

///

## Creating the VMware Assets VM Image

/// admonition | Note
    type: subtle-note
This is only needed if you plan to deploy the Assets VM on VMware vSphere.
///

Follow these steps to create the Assets VM Image for VMware vSphere. This will generate an ISO file based on the Talos VM base image containing a local cache. This image is different from the base Talos image ISO file that you will use for the EDA Kubernetes VMs, but is based on it.

/// html | div.steps

1. Change into the `edaadm` repository.

    In case you have changed directories, ensure that you are in the `edaadm` repository.

    ```bash title="changing into edaadm repository directory"
    cd path/to/edaadm
    ```

2. Generate the Assets VM OVA for VMware vSphere.

    Execute the following command to generate the VMware vSphere Talos OVA for the Assets VM.

    ```bash
    make -C bundles/ create-asset-vm-vmware-boot-ova
    ```

    //// details | Output example
        type: subtle-note

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

    ////

    The OVA disk image will be saved at the relative path `./bundles/eda-cargo/talos-asset-vm-boot-imgs/vmware-amd64.ova`.

///
