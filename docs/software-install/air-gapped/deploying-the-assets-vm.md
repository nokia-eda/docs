# Deploying the Assets VM

## Preparing the VM

The Assets VM will run as a single Virtual Machine inside the air-gapped environment. This VM will hold all of the assets and can be used across multiple deployments and EDA versions, containing the assets for multiple versions.

These steps help create the Assets VM from a base Talos VM image and populate it with the local cache needed to deploy the Assets VM in the air-gapped environment.

/// admonition | Caution
    type: note
These steps are meant to be executed in the public environment with Internet access.
///

### Creating Assets VM Image Cache

Before creating the Assets VM Image for a specific environment, an image cache must be created that will contain the necessary bootstrap images used by the Assets VM.

Change into the cloned `edaadm` repository root directory.

```bash
cd path/to/edaadm
```

And run the following command to create the image cache:

```bash
make -C bundles/ create-assets-host-bootstrap-image-cache
```

### Creating the KVM Assets VM Image

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
    renamed '/home/user/ws/edaadm/public/bundles/eda-cargo/talos-asset-vm-boot-imgs/nocloud-amd64.iso' -> '/home/user/ws/edaadm/public/bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-nocloud-amd64.iso'
    --> INFO: Created /home/user/ws/edaadm/public/bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-nocloud-amd64.iso
    ```

    ////

    The ISO disk image will be saved at the relative path `./bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-nocloud-amd64.iso`.

///

### Creating the VMware Assets VM Image

/// admonition | Note
    type: subtle-note
This is only needed if you plan to deploy the Assets VM on VMware vSphere.
///

/// warning | This command requires Linux kernel version 6 or higher[^1]
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
    renamed '/home/user/ws/edaadm/public/bundles/eda-cargo/talos-asset-vm-boot-imgs/vmware-amd64.ova' -> '/home/user/ws/edaadm/public/bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-vmware-amd64.ova'
    --> INFO: Created /home/user/ws/edaadm/public/bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-vmware-amd64.ova
    ```

    ////

    The OVA disk image will be saved at the relative path `./bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-vmware-amd64.ova`.

///

A single Assets VM can be used for multiple deployments and versions of EDA, as the assets for multiple versions of EDA can be uploaded to the same Assets VM.

## Preparing the air-gapped environment

The downloaded assets need to be made available in the air-gapped environment. Two options are available:

1. Move the system that was used to prepare the Assets VM to the air-gapped environment. For instance, if it is a laptop or a VM, you can move to the air-gapped environment by changing its network configuration.
2. Copy the data from the system that was used to prepare the Assets VM to the air-gapped environment using a USB key or a temporary network connection. The data should include:
    * The playground repository cloned during the ["Preparing for installation"](../preparing-for-installation.md) step.
    * The edaadm repository which includes the `eda-cargo` folder holding the air-gapped data (bundles, asset VM image and Talos base VM images). The `eda-cargo` folder was populated during the [preparing](#preparing-the-vm) the Assets VM and [downloading](downloading-the-assets.md) the necessary assets steps.

### Loading the Kpt Setters image

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

## Deploying the VM

/// admonition | Caution
    type: note
These steps are meant to be executed in the air-gapped environment.
///

The procedure to deploying the Assets VM is similar to deploying the EDA Talos Kubernetes cluster nodes and uses `edaadm` CLI to manage the deployment process.

### Preparing the Assets VM EDAADM Configuration File

The EDAADM configuration file declaratively defines the machine/VM configuration and the Kubernetes cluster parameters and is an abstraction on top of the [Talos machine config](https://docs.siderolabs.com/talos/v1.11/reference/configuration/overview). You will find the edaadm configuration for the Assets VM very similar to the config file used for [EDA Kubernetes nodes](../deploying-eda/setting-up-the-eda-virtual-machine-nodes.md#preparing-the-edaadm-configuration-file) with a few minor differences:

* It is a config file for a single machine.
* The `clusterName` must be unique and different from the EDA Kubernetes cluster.
* The following additions fields must be present in the Assets VM edaadm config:

    ```yaml
    enableImageCache: true
    localPathProvisioner: "/var/local-path-provisioner"
    ```

/// admonition | Notes
    type: subtle-note

1. Consult with the full list of edaadm configuration file options to customize your Assets VM configuration further: **[EDAADM Configuration file fields](../deploying-eda/setting-up-the-eda-virtual-machine-nodes.md#edaadm-configuration-file-fields)**.
2. The Assets VM only needs one network interface, preferably on the OAM network of the EDA Kubernetes cluster. It must be reachable from the OAM network of the EDA Kubernetes cluster.
3. The `edaadm` tool still expects the definition of a storage disk in the machine definition, but this can be a reference to a non-existing disk.
///

Consider an example edaadm configuration for an Assets VM that you can use as a reference when creating your own configuration file:

```yaml title="Example edaadm configuration for the Assets VM - <code>eda-assets-deployment.yaml</code>"
version: -{{ eda_version }}- #(1)!
clusterName: eda-airgap-assets #(2)!
machines:
    - name: eda-assets
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
          mtu: 9000 #(4)!
      disks:
        os: /dev/vda
        storage: /dev/vdb #(3)!
k8s:
    stack: ipv4
    primaryNode: eda-assets
    endpointUrl: https://192.0.2.228:6443
    allowSchedulingOnControlPlanes: true
    control-plane:
        - eda-assets
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

1. EDA version string. Not relevant for the Assets VM, but required by edaadm.
2. The kubernetes cluster name for the Assets VM, must be unique and not the same as the ones specified for the EDA Kubernetes cluster when deploying EDA.
3. The storage disk definition is required by edaadm, but the disk does not need to exist on the Assets VM. Can be set to any value.
4. Pay attention to the set MTU value as the linux bridges, interfaces, and networks between the Assets VM and the EDA Kubernetes cluster nodes must allow for the same MTU size.

Assuming you are in the `edaadm` repository root, save the configuration file as `eda-assets-deployment.yaml`.

### Generating the Talos Machine Configuration Files

After creating the Assets VM EDAADM configuration file, the next step is to generate all the configuration files that are necessary to deploy the Kubernetes environment for the Assets VM.

Use the `edaadm` tool to generate the Talos configuration out of the EDAADM configuration file:

```bash
edaadm generate -c eda-assets-deployment.yaml
```

The output should look similar to the following (a portion has been removed):

```
ConfigFile is eda-assets-deployment.yaml
...
[1/6] Validating Machines
[1/6] Validated Machines
[2/6] Validating Primary Node
[2/6] Validated Primary Node
[3/6] Validating Endpoint URL
[3/6] Validated Endpoint URL
[4/6] Validating Stack
[4/6] Validated Stack
[5/6] Validating Virtual IP
[5/6] Validated Virtual IP
[6/6] Validating Storage
[6/6] Validated Storage
[  OK  ] Spec is validated
[ INFO ] Existing secrets file found - loading:eda-airgap-assets/secrets.yaml
[ INFO ] Loaded secrets bundle eda-airgap-assets/secrets.yaml
generating PKI and tokens
Created eda-airgap-assets/eda-assets.yaml
Created eda-airgap-assets/talosconfig.yaml
Created eda-airgap-assets/rook-ceph-operator-values.yaml
Created eda-airgap-assets/rook-ceph-cluster-values.yaml
```

The generated Talos configuration files will be available in the `eda-airgap-assets` folder which is named after the `clusterName` specified in the EDAADM configuration file.  
The machine config file for the Assets VM is named `eda-assets.yaml` after the `name` field specified in the `machines` section of the EDAADM configuration file.

### Creating the Assets VM on KVM

/// admonition | Caution
    type: note
This procedure is executed on the KVM Hypervisor which will host the Assets VM.
///

/// html | div.steps

1. Ensure that the `virt-install` tool is installed on the KVM hypervisor.

    If you need to install the tools, use the following command:

    ```bash
    sudo yum install virt-install
    ```

    or

    ```bash
    sudo apt --no-install-recommends install virtinst
    ```

2. Verify that the Assets VM ISO image is available.

    The Assets VM ISO image was generated in the [Creating the KVM Assets VM Image](#creating-the-kvm-assets-vm-image) and should be available in the air-gapped environment when you [copied the assets](#preparing-the-air-gapped-environment) from the public environment.

    ```bash title="executing the <code>ls</code> command from the edaadm repository root"
    ls -lh ./bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-nocloud-amd64.iso
    ```

    <div class="embed-result">
    ```{.text .no-select .no-copy}
    -rw-r--r-- 1 root root 684M Nov 12 18:10 eda-cargo/talos-asset-vm-boot-imgs/asset-vm-nocloud-amd64.iso
    ```
    </div>

3. Prepare Assets VM cloud-init files.

    The next step is to create the cloud-init ISO file with the machine configuration file and the necessary metadata.

    Use the `edaadm` tool to generate the cloud-init files for the Assets VM using the edaadm configuration file:

    ```bash
    edaadm make-iso -c eda-assets-deployment.yaml
    ```

    The `eda-assets-data.iso`[^2] file will be created in the `eda-airgap-assets` folder containing the cloud-init information for the Assets VM:

    * `meta-data` file containing the instance-id and local-hostname values set to `.machines[*].name`
    * `network-config` file containing `version: 2` key/value pair. Device types are not specified and will be defined by Talos.
    * `user-data` file containing the Talos machine configuration file for the Assets VM.

4. Create the virtual machine.
    This step uses both the newly created ISO file and the ISO file downloaded from the Talos Machine Factory.

    ```bash
    virt-install -n eda-assets \
    --description "EDA Assets VM for EDA" \
    --noautoconsole --os-variant=generic \ #(1)!
    --memory 16384 --vcpus 4 --cpu host \
    --disk eda-assets-rootdisk.qcow2,format=qcow2,bus=virtio,size=300 \
    --cdrom ./bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-nocloud-amd64.iso \
    --disk eda-assets-data.iso,device=cdrom \
    --network bridge=br0,model=virtio
    ```

    1. Depending on the `virt-install` version, the `--os-variant=generic` option might not be supported. In that case use `--os-type=generic` instead.

    //// warning
    Pay attention to the MTU value set on the Linux bridge, interfaces, and networks between the Assets VM and the EDA Kubernetes cluster nodes must allow for the same MTU size.
    ////

///

### Creating the Assets VM on VMware vSphere

/// admonition | Caution
    type: note
This procedure is executed in the air-gapped environment for a VMware vSphere deployment.
///

/// html | div.steps

1. Ensure that the `ovftool` is installed.

    To deploy the Assets VM OVA image on VMware vSphere, the `ovftool` must be installed on the system from which you will create the deployment.

2. Deploy Assets VM OVA image.

    Standing in the root of the edaadm repository, create a base64 encoded string from the Talos machine configuration for the Assets VM. If you have been using the example edaadm configuration file from above, the command would be:

    ```bash
    export NODECONFIG=$(base64 -i eda-airgap-assets/eda-assets.yaml)
    ```

    Deploy the Assets VM OVA image generated in the ["Creating the VMware Assets VM image"](#creating-the-vmware-assets-vm-image) section using the `ovftool` command:

    ```bash
    ovftool --acceptAllEulas --noSSLVerify \
    -dm=thin \
    -ds=DATASTORE \
    -n=eda-assets \
    --net:"VM Network=OAM" \
    --prop:talos.config="${NODECONFIG}" \
    ./bundles/eda-cargo/talos-asset-vm-boot-imgs/vmware-amd64.ova \
    vi://admin%40vsphere.local@vcenter.tld/My-DC/host/Cluster/Resources/My-Resource-Group
    ```

3. Adjust the Assets VM resources.

    After deploying the VM using the OVA image:

    * Increase the number of vCPUs to 4.
    * Increase the memory to 16G.
    * Increase the main disk size to 300G. On boot, Talos automatically extends the file system.
    * Enable 100% resource reservation for the CPU, memory and disk.
///

## Bootstrap the Assets VM

The Assets VM runs Talos Kubernetes and needs to be bootstrapped using the `edaadm` tool. Use the edaadm configuration file created previously to bootstrap the Assets VM.

```bash
edaadm bootstrap-k8s -c eda-assets-deployment.yaml
```

## Obtaining the Kubernetes Config File

Once the Assets VM Kubernetes cluster is bootstrapped, use the `edaadm` command to fetch the Kubernetes configuration file (kubeconfig) for use with `kubectl`.

/// html | div.steps

1. Obtain the Kubernetes configuration file.

    Execute the following command in the folder with the `eda-assets-deployment.yaml` EDAADM configuration file.

    ```bash
    edaadm get-kubeconfig -c eda-assets-deployment.yaml
    ```

2. Configure the Kubernetes configuration file in your environment.

    You can configure your environment to use the ​kubeconfig​ file for use with the `kubectl` command.

    ```bash
    export KUBECONFIG=eda-airgap-assets/kubeconfig.yaml
    ```

3. Inspect your server and check if all nodes are up and running.

    You can use the typical `kubectl` commands.

    ```bash
    kubectl get nodes
    ```

///

When the node is up and ready, continue with deploying the Assets VM services.

## Deploying the Assets VM Services

<!--
/// details | Defining custom usernames and passwords for the services
    type: note
In case custom usernames and passwords must be provided for the git server and web server, follow these steps:

**Git Server Username and Password**

By default, the git server default username is `eda` and default password is `eda`. To change these defaults, use the following command to generate a base64 hash for the username and a separate one for the password:

```bash
echo -n 'new-username' | base64
```

```bash
echo -n 'new-password' | base64
```

Keep the output of these two commands saved somewhere, as you will need to use them in the next step, as well as when installing the EDA Talos Kubernetes cluster and EDA.

Export these values as environment variables in your shell so they can be used by the kpt platform to configure the services when you execute the commands later in this section:

```bash
export GOGS_ADMIN_USER="base64 encoded value for the username"
export GOGS_ADMIN_PASS="base64 encoded value for the password"
```

**Web Server Username and Password**

By  default, the web server default username is `eda` and default password is `eda`. To change these defaults, use the following command to generate a new htpasswd hash. The command will request you to type a password twice and output a string.

```bash
htpasswd -n new-username
```

Use the string from this command and also do a base64 encoding of it:

```bash
echo -n 'new-username:...' | base64
```

Keep the output of this command saved somewhere, as you will need to use them in the next step, as well as when installing the EDA Talos Kubernetes cluster and EDA.

Export the value as environment variable in your shell so it can be used by the kpt platform to configure the services when you execute the commands later in this section.

```bash
export LIGHTTPD_EDA_HTPASSWD="base64 encoded htpasswd output"
```

///
-->

After deploying and bootstrapping the Assets VM itself, the container registry, git server and web server need to be deployed.

```bash
make -C kpt/ eda-setup-shipyard
```

Once the Assets VM is deployed and bootstrapped, you need to upload the assets to the Assets Host.

[:octicons-arrow-right-24: Upload the assets](uploading-assets.md)

[^1]: See https://github.com/siderolabs/talos/issues/9264#issuecomment-2426756838
[^2]: Where `eda-assets` is the name of the machine defined in the EDAADM configuration file.
