# Deploying the Assets VM

/// admonition | Caution
    type: note
These steps are meant to be executed in the air-gapped environment.
///

The procedure to deploying the Assets VM is similar to deploying the EDA Talos Kubernetes cluster nodes and uses `edaadm` CLI to manage the deployment process.

## Preparing the Assets VM EDAADM Configuration File

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

Considering you are in the `edaadm` repository root, save the configuration file as `eda-assets-deployment.yaml`.

## Generating the Talos Machine Configuration Files

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

## Deploy the Assets VM

The Assets VM can be deployed on a KVM or VMware vSphere environment. Follow the steps below depending on your hypervisor.

### Creating the Assets VM on KVM

/// admonition | Caution
    type: note
This procedure is executed on the KVM Hypervisor which will host the Assets VM.
///

/// html | div.steps

1. Ensure that the `virt-install` and `genisoimage` tools are installed on the KVM hypervisor.

    If you need to install the tools, use the following command:

    ```bash
    sudo yum install virt-install genisoimage
    ```

    or

    ```bash
    sudo apt --no-install-recommends install virtinst genisoimage
    ```

2. Verify that the Assets VM ISO image is available.

    The Assets VM ISO image was generated in the [Creating the KVM Assets VM Image](preparing-the-assets-vm.md#creating-the-kvm-assets-vm-image) and should be available in the Air-gapped environment when you [copied the assets](preparing-the-air-gapped-environment.md) from the public environment.

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

    Standing in the root of the edaadm repository, copy the machine configuration file generated for the Assets VM to a file called `user-data`. If you have been using the example edaadm configuration file from above, the command would be:

    ```
    cp eda-airgap-assets/eda-assets.yaml user-data
    ```

    Create a file called `meta-data` with the instance-id and local-hostname values:

    ```bash
    cat <<'EOF' > meta-data
    instance-id: eda-assets 
    local-hostname: eda-assets
    EOF
    ```

    And lastly, create a file called `network-config` for the node with the following content:

    ```bash
    cat <<'EOF' > network-config
    version: 2
    EOF
    ```

    Create an ISO file containing the newly created files.
    For ease of use, name the ISO file with the name of the node for which you are creating the ISO.

    ```bash
    mkisofs -o eda-assets-data.iso -V cidata -J -r meta-data network-config user-data 
    ```

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
This procedure is executed in the Air-gapped environment for a VMware vSphere deployment.
///

/// html | div.steps

1. Ensure that the `ovftool` is installed.

    To deploy the Assets VM OVA image on VMware vSphere, the `ovftool` must be installed on the system from which you will create the deployment.

2. Deploy Assets VM OVA image.

    Standing in the root of the edaadm repository, create a base64 encoded string from the Talos machine configuration for the Assets VM. If you have been using the example edaadm configuration file from above, the command would be:

    ```bash
    export NODECONFIG=$(base64 -i eda-airgap-assets/eda-assets.yaml)
    ```

    Deploy the Assets VM OVA image generated in the ["Creating the VMware Assets VM image"](preparing-the-assets-vm.md#creating-the-vmware-assets-vm-image) section using the `ovftool` command:

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

## Uploading the Assets to the Assets VM

Now that the Assets VM and its services are up and running, upload all the assets that you [downloaded previously](downloading-the-assets.md#downloading-the-assets-bundles) to the Assets VM.

Set the `EDA_CORE_VERSION`[^1] environment variable (and any `SKIP_...` environment variables you used when downloading the assets)[^1] in your shell. This will ensure that the correct version of the cache and assets is uploaded to the Assets VM.

```bash
export EDA_CORE_VERSION=-{{ eda_version }}-
```

Then execute the following command to upload all the assets to the Assets VM:

```bash
make -C bundles/ load-all-bundles \
    ASSET_HOST=192.0.2.228 \
    ASSET_HOST_GIT_USERNAME="ZWRh" \
    ASSET_HOST_GIT_PASSWORD="ZWRh" \
    ASSET_HOST_ARTIFACTS_USERNAME="ZWRh" \
    ASSET_HOST_ARTIFACTS_PASSWORD="ZWRh"
```

/// admonition | Notes
    type: subtle-note

1. Make sure to replace the `ASSET_HOST` IP with the IP of your Asset VM.
2. The username and passwords will be configurable in the near future. The `eda` username and password are used by default.

///

Once all uploads have finished successfully, the Assets VM is ready to support the installation of the EDA Talos Kubernetes cluster in the Air-gapped environment.

[^1]: If you used `SKIP_...` environment variables when [downloading the assets](downloading-the-assets.md#downloading-the-assets-bundles), make sure to set the same variables when uploading the assets to the Assets VM.
