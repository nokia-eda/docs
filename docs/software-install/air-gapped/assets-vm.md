# Assets VM

-{{ js_script("/javascripts/viewer-static.min.js") }}-

If you chose to use the EDA Assets VM for all or some of the hosting services required to host the downloaded assets in the air-gapped environment, you need to deploy and configure the Assets VM in the air-gapped environment.

The Assets VM runs the container registry, Git server, and web server that host the downloaded assets in the air-gapped environment.

> A single Assets VM can be used for multiple deployments and versions of EDA, as the assets for multiple versions of EDA can be uploaded to the same Assets VM.

## Prerequisites

<!-- --8<-- [start:prerequisites] -->

The downloaded assets are [transferred](downloading-the-assets.md#transferring-the-assets-to-the-air-gapped-environment) to the air-gapped environment.

### Loading the Kpt Setters image

/// admonition | Note
    type: subtle-note
These steps are to be executed in the air-gapped environment.
///

The procedures for setting up the Assets VM and installing EDA use [Kpt](https://kpt.dev) - a package manager for Kubernetes. Kpt relies on the `kpt-apply-setters` container to be present in the local Docker image cache of the air-gapped system to be able to perform its operations.  
The container image is part of the `eda-bundle-tools` bundle. If you downloaded the default bundle list, which includes `eda-bundle-tools`, you will have that bundle on your air-gapped system. If you do not have it yet, download the default bundle list on a system with Internet access using `make -C bundles/ save-default-bundles`.

To load the `kpt-apply-setters` image from the `eda-bundle-tools` bundle, follow these steps:

/// html | div.steps

1. Ensure you have changed into the directory of the [cloned `edaadm` repository](../preparing-for-installation.md#download-edaadm-tools).

    ```bash title="changing into edaadm repository directory"
    cd path/to/edaadm
    ```

2. Import the image into the local Docker image cache.

    The bundle and `kpt-apply-setters` versions may change in future releases. In that case, replace `2-0-0` and `0-1-1` with the appropriate versions.

    ```bash
    docker load -i ./bundles/eda-cargo/eda-bundle-tools-2-0-0/images/srl-labs-kpt-apply-setters-0-1-1
    ```

///

<!-- --8<-- [end:prerequisites] -->

## Deploying the VM

/// admonition | Caution
    type: note
These steps are meant to be executed in the air-gapped environment.
///

The procedure for deploying the Assets VM is similar to deploying the Nokia EDA Talos Kubernetes cluster nodes and uses the `edaadm` CLI to manage the deployment process.

### Preparing the Assets VM EDAADM Configuration File

The EDAADM configuration file declaratively defines the machine/VM configuration and the Kubernetes cluster parameters and is an abstraction on top of the [Talos machine config](https://docs.siderolabs.com/talos/v1.11/reference/configuration/overview). You will find the edaadm configuration for the Assets VM very similar to the config file used for [Nokia EDA Kubernetes nodes](../deploying-eda/setting-up-the-eda-virtual-machine-nodes.md#preparing-the-edaadm-configuration-file) with a few minor differences:

* It is a config file for a single machine.
* The `clusterName` must be unique and different from the Nokia EDA Kubernetes cluster.
* The following additional fields must be present in the Assets VM edaadm config:

    ```yaml
    enableImageCache: true
    localPathProvisioner: "/var/local-path-provisioner"
    ```

/// admonition | Notes
    type: subtle-note

1. Consult the full list of edaadm configuration file options to customize your Assets VM configuration: **[EDAADM Configuration file fields](../deploying-eda/setting-up-the-eda-virtual-machine-nodes.md#edaadm-configuration-file-fields)**.
2. The Assets VM needs only one network interface, preferably on the planned OAM network for the Nokia EDA Kubernetes cluster. It must be reachable from that OAM network during EDA installation.
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

1. Nokia EDA version string. Not relevant for the Assets VM, but required by edaadm.
2. The Kubernetes cluster name for the Assets VM must be unique and different from the names specified for the Nokia EDA Kubernetes cluster.
3. The storage disk definition is required by edaadm, but the disk does not need to exist on the Assets VM. Can be set to any value.
4. Pay attention to the configured MTU, as the Linux bridges, interfaces, and networks between the Assets VM and the Nokia EDA Kubernetes cluster nodes must support the same MTU.

Assuming you are in the `edaadm` repository root, save the configuration file as `eda-assets-deployment.yaml`.

### Generating the Talos machine configuration files

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

    The Assets VM ISO image was generated in the [Downloading the EDA Assets VM components](downloading-the-assets.md#downloading-the-eda-assets-vm-components) procedure (KVM tab) and should be available in the air-gapped environment after you [transfer the assets](downloading-the-assets.md#transferring-the-assets-to-the-air-gapped-environment) from the public environment.

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
    This step uses both the cloud-init ISO created by `edaadm make-iso` (`eda-assets-data.iso`) and the Assets VM boot ISO generated by `create-asset-vm-nocloud-boot-iso` (`asset-vm-nocloud-amd64.iso`).

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
    Pay attention to the MTU value. The Linux bridges, interfaces, and networks between the Assets VM and the Nokia EDA Kubernetes cluster nodes must all allow for the same MTU size.
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

    From the root of the `edaadm` repository, create a base64-encoded string from the Talos machine configuration for the Assets VM. If you used the example configuration file above, run:

    ```bash
    export NODECONFIG=$(base64 -i eda-airgap-assets/eda-assets.yaml)
    ```

    Deploy the Assets VM OVA image generated in the [Downloading the EDA Assets VM components](downloading-the-assets.md#downloading-the-eda-assets-vm-components) procedure (VMware vSphere tab) using the `ovftool` command:

    ```bash
    ovftool --acceptAllEulas --noSSLVerify \
    -dm=thin \
    -ds=DATASTORE \
    -n=eda-assets \
    --net:"VM Network=OAM" \
    --prop:talos.config="${NODECONFIG}" \
    ./bundles/eda-cargo/talos-asset-vm-boot-imgs/asset-vm-vmware-amd64.ova \
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

## Obtaining the Kubernetes config file

Once the Assets VM Kubernetes cluster is bootstrapped, use the `edaadm` command to fetch the Kubernetes configuration file (kubeconfig) for use with `kubectl`.

/// html | div.steps

1. Obtain the Kubernetes configuration file.

    Execute the following command in the folder with the `eda-assets-deployment.yaml` EDAADM configuration file.

    ```bash
    edaadm get-kubeconfig -c eda-assets-deployment.yaml
    ```

2. Configure the Kubernetes configuration file in your environment.

    You can configure your environment to use the `kubeconfig` file with the `kubectl` command.

    ```bash
    export KUBECONFIG=eda-airgap-assets/kubeconfig.yaml
    ```

3. Verify that the Assets VM node is up and running.

    You can use the typical `kubectl` commands.

    ```bash
    kubectl get nodes
    ```

///

When the node is up and ready, continue with deploying the Assets VM services.

## Assets host services

The Assets VM is a single-node Kubernetes cluster used to run the assets host services, such as the container registry, Git server, and web server.
These services are not baked into the Assets VM image, but are deployed as applications on top of the Kubernetes cluster.

-{{ diagram(path='./diagrams/assets-vm-services.drawio', title='Assets host services in Assets VM', page=0, zoom=1.0) }}-

### Customizing the assets host services

The deployed assets host services can be customized by providing custom values for the services in the `kpt/config/kpt-setters.yaml` file of the cloned `edaadm` repository. To list the available custom keys, use the following command:

```bash
make -C kpt/ ls-setters
```

The output will list the available custom keys and their current values.

Populate the `kpt/config/kpt-setters.yaml` file with the desired values and run the following command to apply the configuration:

```bash
make -C kpt/ eda-configure-shipyard
```

### Deploying the assets host services

To deploy the assets host services, run:

```bash
make -C kpt/ eda-setup-shipyard
```

This command deploys the container registry, Git server, and web server on the Kubernetes cluster running on the Assets VM.

Once the Assets VM is deployed and the hosting services are running, you need to upload the assets to the Assets Host.

[:octicons-arrow-right-24: Upload the assets](uploading-assets.md)

[^2]: Where `eda-assets` is the name of the machine defined in the EDAADM configuration file.
