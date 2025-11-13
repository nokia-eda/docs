# Setting up the EDA virtual machine nodes

This section describes how to the prepare the configurations file, generate the configuration files, and deploy the Talos virtual machines.

## Preparing the EDAADM configuration file

The `edaadm` tool helps with the creation of the necessary machine configuration files for the Talos VMs that are part of your deployment.

## EDAADM configuration file fields

The EDAADM configuration file is a YAML file that describes your Talos Kubernetes environment. You can use it to configure the different nodes and the general Kubernetes cluster environment.

/// html | table
//// html | th[style='text-align: center;']
Top-level parameter
////
//// html | th[style='text-align: center;']
Description
////

//// html | tr
///// html | td
`version`
/////
///// html | td
The version of the EDA environment to be deployed.  
Example: 25.4.1
/////
////

//// html | tr
///// html | td
`clusterName`
/////
///// html | td
The name of your EDA environment.  
Example: `eda-production-cluster`
/////
////

<!-- machines row start -->
//// html | tr
///// html | td
`machines`
/////
<!-- machines descr cell start -->
///// html | td
A list of Kubernetes nodes. Each Kubernetes node has the following settings:

<!-- machines sub-table start -->
////// html | table

/////// html | tr
//////// html | td
`name`
////////
//////// html | td
The name of a node.  
Example: `eda-node01`
////////
///////

/////// html | tr
//////// html | td
`endpoint`
////////
//////// html | td
The IP address on which the node is reachable for Talos to control. Optional.
////////
///////

/////// html | tr
//////// html | td
`interfaces`
////////
//////// html | td
A list of interfaces present in the node, each with the following settings:

* `name`: the name of the interface.
    Example: `eth0`

* `dhcp`: indicates if DHCP is to be used for the interface.
    Values: `true` or `false`. For production environments, set to `false`.

* `mtu`: the MTU setting for the interface. For an interface used to connect to nodes under management, set to 9000 for best practice. Optional.

* `interface`: the interface name as it appears in Linux. Typically, `eth0`, `eth1`, and so forth. Optional.

* `addresses`: a list of IP addresses; for dual-stack deployments, you can specify both IPv4 and IPv6 addresses. If DHCP is not provided, specify at least one address.

* `routes`: a list of static routes to configure, including the default route. Optional. Routes have the following components:

    * `gateway`: the next-hop or gateway for the route.

    * `metric`: a metric to indicate the priority of the route. Optional.

    * `mtu`: a specific MTU for the route. Optional.

    * `network`: the destination CIDR of the route.

    * `source`: a source interface for the route to apply to. Optional.

* `deviceSelector`: specifies how to select the device associated with this interface.
    * `busPath`: a PCI buspath that can contain wildcards. Optional.

    * `hardwareAddr`: a MAC address that can contain wildcards. Optional.
////////
///////

/////// html | tr
//////// html | td
`disks`
////////
//////// html | td
Identifies the disks available in the node:

* `os`: Specifies which disk to use for the OS. Required setting.

    Typically `/dev/sda` or `/dev/vda`, depending on the hypervisor platform

* `storage`: Optional disk for use with nodes that are to be part of the storage cluster.
////////
///////

//////
<!-- machines sub-table end -->

/////
<!-- machines descr cell end -->
////
<!-- machines row end -->
<!-- k8s row start -->
//// html | tr
///// html | td
`k8s`
/////
<!-- k8s descr cell start -->
///// html | td
The Kubernetes-specific configuration. The following parameters define the Kubernetes cluster:

<!-- k8s sub-table start -->
////// html | table

/////// html | tr
//////// html | td
`stack`
////////
//////// html | td
Indicates the network stack to support. Values: `ipv4`, `ipv6`, or `dual`.

* Set to `ipv6` for IPv6-only deployments. The value of `.k8s.vip.ipv6` will be used to set the Talos Virtual IP (VIP) address.

* For IPv4-only deployments, set to `ipv4`. The value of `.k8s.vip.ipv4` will be used to set the Talos Virtual IP (VIP) address.

* For dual-stack deployments, set to `dual`. Only one value can be specified for the VIP (`.k8s.vip.ipv4` or `.k8s.vip.ipv6`) address and the set value will be used to set the Talos Virtual IP (VIP) address.

IPv6 and dual-stack are supported from EDA 25.8.2 onwards.
////////
///////

/////// html | tr
//////// html | td
`vip`
////////
//////// html | td
The [Virtual IP (VIP) address](https://www.talos.dev/v1.9/talos-guides/network/vip/) used for Kubernetes API access and the interfaces to which they should be attached in the control plane nodes. Choose the value depending on the IP stack in use:

* `interface`: the interface to which the VIP is attached on the nodes.

    Example: `eth0`

* `ipv4`: the IPv4 VIP address.

    Example: `192.0.2.10`

* `ipv6`: the IPv6 VIP address.

> Since VIP functionality relies on etcd for elections, the shared IP will not come alive until after you have bootstrapped Kubernetes.

////////
///////

/////// html | tr
//////// html | td
`primaryNode`
////////
//////// html | td
The first control plane node in the cluster to be used for bootstrapping the Kubernetes cluster.

Specify the name of a machine.
////////
///////

/////// html | tr
//////// html | td
`endpointUrl`
////////
//////// html | td
The URL on which to reach the Kubernetes control plane. This setting uses the Kubernetes VIP address. Example: `https://192.0.2.10:6443`
////////
///////

/////// html | tr
//////// html | td
`allowSchedulingOnControlPlanes`
////////
//////// html | td
Specifies if workloads can be deployed on the control plane node.
Values: `true` or `false`. For best practice, set to `true`.
////////
///////

/////// html | tr
//////// html | td
`control-plane`
////////
//////// html | td
A list of control plane nodes. Specify a machine name.
////////
///////

/////// html | tr
//////// html | td
`worker`
////////
//////// html | td
A list of worker nodes. Specify a machine name.
////////
///////

/////// html | tr
//////// html | td
`nodeIP`
////////
//////// html | td
Network settings for the nodes:

* `validSubnets`: the list of IPv4 and/or IPv6 subnets used by the k8s nodes.
    Can be used to force the node convergence in a multi-nic environment to a single or a set of subnets.  
    Also sets the subnet over which etcd should converge, perform heartbeats and leader election.  
    This property in the adm configuration sets the following talos [machine config properties](https://www.talos.dev/v1.9/introduction/prodnotes/#multihoming-and-etcd):  
      - `cluster.k8s.etcd.advertisedSubnets`
      - `machine.kubelet.nodeIP.validSubnets`

    Must be within the configured addresses on one of the interfaces in the `machine.interface[*]` otherwise the node won't be able to join the cluster.

    Example:  
        ```
        - 192.168.123.101/24
        - 2001:0db8:0ca2:0006:0000:0000:0000:1001/64
        ```

////////
///////

/////// html | tr
//////// html | td
`network`
////////
//////// html | td
Kubernetes pods and services network settings.

* `podSubnets`: Talos by default only configures an IPv4 pod subnet.
    If you want to change the default IPv4 pod subnet or add an IPv6 pod subnet, provide the subnet(s) here as a list.
    This property sets the `cluster.network.podsSubnets` Talos machine config property.

    Example:  
        ```
        - 10.244.0.0/16
        - fd31:e17c:f07f:8b6d::/64
        ```

* `serviceSubnets`: Talos by default only configures an IPv4 service subnet.
    If you want to change the default IPv4 service subnet or add an IPv6 service subnet, provide the subnet(s) here as a list.
    This property sets the `cluster.network.serviceSubnets` Talos machine config property.

    Example:  
        ```
        - 10.96.0.0/12
        - fd31:e17c:f07f:2dc0:4e2b:2ebc:cbc0:0/108
        ```

* `node-cidr-mask-size-ipv4`: Defines the subnet mask size for IPv4 network as defined by the `podSubnets` that each node will use.  
    Default: `24`

    Sets the `cluster.controllerManager.extrArgs.node-cidr-mask-size-ipv4` Talos machine config property.

    Example value: `28`

* `node-cidr-mask-size-ipv6`: Defines the subnet mask size for IPv6 network as defined by the `podSubnets` that each node will use.  
    Default: `64`

    Sets the `cluster.controllerManager.extrArgs.node-cidr-mask-size-ipv6` Talos machine config property.

    Example value: `80`
////////
///////

/////// html | tr
//////// html | td
`flannelArgs`
////////
//////// html | td
[Flannel CNI CLI arguments](https://github.com/flannel-io/flannel/blob/master/Documentation/configuration.md#key-command-line-options) allow a user to customize the flannel configuration. Provided as a list of `key=value` pairs.

Example:  
    ```
    - --iface=eth0
    ```

A common use case is to specify the interface used by flannel when the default route is not set up or the CNI needs to bound to a specific interface due to security or operational reasons.
////////
///////

/////// html | tr
//////// html | td
`env`
////////
//////// html | td
Section that includes the optional proxy settings for the Kubernetes nodes:

* `http_proxy`: The HTTP proxy URL to use.

    Example: `http://192.0.2.254:808`

* `https_proxy`: the HTTPS proxy URL to use.

    Example: `http://192.0.2.254:808`

* `no_proxy`: the no proxy setting for IP addresses, IP ranges, and hostnames
////////
///////

/////// html | tr
//////// html | td
`time`
////////
//////// html | td
Defines NTP settings.

* `disabled`: Specifies whether NTP is enabled. For production environments, set to false to enable NTP.
* `servers`: A list of NTP servers; required for production environments.
////////
///////

/////// html | tr
//////// html | td
`nameservers`
////////
//////// html | td
A list of DNS servers specified under the following sub-element:

* `servers`: the list of DNS servers
////////
///////

/////// html | tr
//////// html | td
`certBundle`
////////
//////// html | td
An optional set of PEM-formatted certificates that need to be trusted; this setting is used for trust external services.
////////
///////

/////// html | tr
//////// html | td
`mirror`
////////
//////// html | td
Only needed for Air-gapped environment, following settings can be set:

* `name`: The name of the mirror
* `url`: The URL of the mirror
* `insecure`: should be `true`
* `overridePath`: should be `false`
* `skipFallback`: should be `true`
* `mirrors`: A list of online registry domain names for which the mirror is used. This should look like:

    ```
    - docker.io
    - gcr.io
    - ghcr.io
    - registry.k8s.io
    - quay.io
    ```

////////
///////

//////
<!-- k8s sub-table end -->

/////

<!-- k8s descr cell end -->
////
<!-- k8s row end -->
///

### Example EDAADM configuration file

The following examples show an EDAADM configuration file for a 6-node Kubernetes cluster. For a standard Internet based installation, as well as for an Air-gapped installation. These are the same two files, with only the `mirror` addition on the second tab/file.

/// tab | Internet based installation

```{.yaml .code-scroll-lg}
--8<-- "docs/software-install/resources/edaadm-config-example.yaml"
```

///

/// tab | Air-gapped installation

```{.yaml .code-scroll-lg}
--8<-- "docs/software-install/resources/edaadm-config-example.yaml"
  mirror:
    name: 192.0.2.228
    url: https://192.0.2.228
    insecure: true
    overridePath: false
    skipFallback: true
    mirrors:
      - docker.io
      - gcr.io
      - ghcr.io
      - registry.k8s.io
      - quay.io
```

///

## Generating the Talos machine configurations

After creating the EDAADM configuration file, the next step is to generate all the configuration files that are necessary to deploy the Kubernetes environment using Talos.

Use the `edaadm` tool to generate the deployment files.

```bash
edaadm generate -c eda-input-6-node.yaml
```

<div class="embed-result">
```
$ edaadm generate -c eda-input-6-node.yaml
ConfigFile is eda-input-6-node.yaml
...
[1/4] Validating Machines
[1/4] Validated Machines
[2/4] Validating PrimaryNode
[2/4] Validated PrimaryNode
[3/4] Validating Endpoint URL
[3/4] Validated Endpoint URL
[4/4] Validating Virtual IP
[4/4] Validated Virtual IP
[  OK  ] Spec is validated
Generating secrets for eda-compute-cluster
Created eda-compute-cluster/secrets.yaml
generating PKI and tokens
Created eda-compute-cluster/eda-node01.yaml
Created eda-compute-cluster/talosconfig.yaml
generating PKI and tokens
Created eda-compute-cluster/eda-node02.yaml
generating PKI and tokens
Created eda-compute-cluster/eda-node03.yaml
generating PKI and tokens
Created eda-compute-cluster/eda-node04.yaml
generating PKI and tokens
Created eda-compute-cluster/eda-node05.yaml
generating PKI and tokens
Created eda-compute-cluster/eda-node06.yaml
```
</div>

The configuration files created by the `edaadm` tool are used in the next steps when you deploy the virtual machines.

/// admonition | Note
    type: subtle-note
Nokia strongly recommends that you store these files securely and keep a backup.
///

## Deploying the Talos virtual machines

This section provides the procedures for deploying an EDA node as a virtual machine on KVM or VMware vSphere.

### Creating the VM on bridged networks on KVM

Complete the following steps to deploy an EDA node as a virtual machine on KVM. These steps are executed on the RedHat Enterprise Linux or Rocky Linux hypervisor directly. The steps below assume the deployment of the eda-node01 virtual machine as per the above configuration file. Ensure that you use the correct machine configuration file generated by the `edaadm` tool.

/// admonition | Note
    type: subtle-note
This procedure expects two networks to be available on the KVM hypervisors. The OAM network is referred to as br0 and the fabric management network is referred to as br1. Both of these networks are standard Linux bridge networks. If you use only one interface, adapt Step `7` to only use the br0 network only.
///

/// html | div.steps

1. Ensure that the virt-install tool is installed on the KVM hypervisor.  
    If you need to install the tool, use the following command:

    ```
    yum install virt-install
    ```

2. Verify that the ISO image downloaded in [Downloading the KVM image](../preparing-for-installation.md#downloading-the-kvm-image) is available on the hypervisor.
3. Copy the machine configuration file generated for this specific node to a file called user-data.

    ```
    cp eda-node01-control-plane.yaml user-data 
    ```

4. Create a file called meta-data for the node.
    Use the appropriate instance-id and local-hostname values.

    ```
    instance-id: eda-node01 
    local-hostname: eda-node01 
    ```

5. Create a file called `network-config` for the node.

    The file should have the following content:

    ```
    version: 2
    ```

6. Create an ISO file containing the newly created files.
    For ease of use, name the ISO file with the name of the node for which you are creating the ISO.

    ```
    mkisofs -o eda-node01-data.iso -V cidata -J -r meta-data network-config user-data 
    ```

7. Create the virtual machine.
    This step uses both the newly created ISO file and the ISO file downloaded from the Talos Machine Factory.

    ```
    virt-install -n eda-node01 \ 
    --description "Talos 1.9.2 vm for node eda-node01" \ 
    --noautoconsole --os-type=generic \ 
    --memory 65536 --vcpus 32 --cpu host \ 
    --disk eda-node01-rootdisk.qcow2,format=qcow2,bus=virtio,size=100 \ 
    --disk eda-node01-storagedisk.qcow2,format=qcow2,bus=virtio,size=300 \ 
    --cdrom nocloud-amd64.iso \ 
    --disk eda-node01-data.iso,device=cdrom \ 
    --network bridge=br0,model=virtio \ 
    --network bridge=br1,model=virtio
    ```

    /// admonition | Note
        type: subtle-note
    If the node is not a storage node, you can remove the second --disk line.
    ///

///

### Creating the VM on bridged networks on VMware vSphere

Complete the following steps to deploy an EDA node as a virtual machine on VMware vSphere. The steps below assume the deployment of the eda-node01 virtual machine as per the above configuration file. Ensure that you are using the correct machine configuration file generated by the `edaadm` tool.

You can use one of the following methods to deploy the VM on VMware vSphere:

* the VMware vSphere vCenter or ESXi UI

    For instructions, see *Deploy an OVF or OVA Template* in the VMware vSphere documentation.

* the VMware Open Virtualization Format Tool CLI (VMware OVF Tool CLI)

    This procedure provides an example of how to use the VMware OVF Tool CLI.

/// admonition | Note
    type: subtle-note
This procedure uses two networks (portgroups) to be available on the ESXi hypervisors. The OAM network is referred to as OAM and the fabric management network is referred to as FABRIC. Both of these networks can be standard PortGroups or distributed PortGroups. If you only use one network, you do not need to create a second interface on the VM.
///

/// html | div.steps

1. Download and install the latest version of the VMware OVF Tool from the VMware Developer website.
2. Display details about the OVA image.

    ```
    ovftool vmware-amd64.ova 
    ```

    <div class="embed-result">
    ```
    OVF version:   1.0
    VirtualApp:    false
    Name:          talos

    Download Size:  103.44 MB

    Deployment Sizes:
      Flat disks:   8.00 GB
      Sparse disks: Unknown

    Networks:
      Name:        VM Network
      Description: The VM Network network

    Virtual Machines:
      Name:               talos
      Operating System:   other3xlinux64guest
      Virtual Hardware:
        Families:         vmx-15
        Number of CPUs:   2
        Cores per socket: automatic
        Memory:           2.00 GB

        Disks:
          Index:          0
          Instance ID:    4
          Capacity:       8.00 GB
          Disk Types:     SCSI-VirtualSCSI

        NICs:
          Adapter Type:   VmxNet3
          Connection:     VM Network

    Properties:
      Key:         talos.config
      Label:       Talos config data
      Type:        string
      Description: Inline Talos config

    References:
      File:  disk.vmdk

    ```
    </div>

3. Create a base64 encoded hash from the Talos machine configuration for the node.

    In this example, the output is stored as an environment variable to make it easy to use in the command to deploy the image using the OVF Tool.

    ```
    export NODECONFIG=$(base64 -i eda-node01-control-plane.yaml)
    ```

4. Deploy the OVA image using the OVF Tool.
    For details about command line arguments, see the OVF Tool documentation from the VMware website.

    /// admonition | Note
        type: subtle-note
    If you prefer using the VMware vCenter UI to create the virtual machines, use the regular method of deploying an OVA/OVF template. In this process, in the Customize template step, when you are prompted to provide the Inline Talos config, you must provide the base64 encoded data from the Talos machine configuration for the node. This very long string that is returned when you execute the base64 -i eda-node01.yaml command. Copy that long string and paste it into the field in the UI, then continue.
    ///

    ```
    ovftool --acceptAllEulas --noSSLVerify \
    -dm=thick \
    -ds=DATASTORE \
    -n=eda-node01 \
    --net:"VM Network=OAM" \
    --prop:talos.config="${NODECONFIG}" \
    vmware-amd64.ova \
    vi://administrator%40vsphere.local@vcenter.domain.tld/My-DC/host/My-Cluster/Resources/My-Resource-Group
    ```

    <div class="embed-result">
    ```
    Opening OVA source: vmware-amd64.ova
    The manifest validates
    Enter login information for target vi://vcenter.domain.tld/
    Username: administrator%40vsphere.local
    Password: ***********
    Opening VI target: vi://administrator%40vsphere.local@vcenter.domain.tld:443/My-DC/host/My-Cluster/Resources/My-Resource-Group
    Deploying to VI: vi://administrator%40vsphere.local@ vcenter.domain.tld:443/My-DC/host/My-Cluster/Resources/My-Resource-Group  
    Transfer Completed
    Completed successfully
    ```
    </div>

    This step deploys the VM with the CPU, memory, disk, and NIC configuration of the default OVA image. The next step updates these settings.

5. In vCenter, edit the VM settings.

    Make the following changes:

    * Increase the number of vCPU to 32.
    * Increase the memory to 64G.
    * Increase the main disk size to 100G. On boot, Talos automatically extends the file system.
    * Optionally, if this VM is a storage node, add a new disk with a size of 300G.
    * Optionally, add a second network interface and connect it to the FABRIC PortGroup.
    * Enable 100% resource reservation for the CPU, memory and disk.

6. Power on the virtual machine.

///
