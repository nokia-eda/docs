# OpenStack Plugin RHOSP 17.1 Installation

This guide provides step-by-step instructions for installing the EDA Connect OpenStack plugin on Red Hat OpenStack Platform (RHOSP) 17.1 using the
OpenStack Director (TripleO).

/// warning
Before proceeding with this installation method, ensure you have completed all the prerequisites and preparation steps described in
the [OpenStack Plugin Installation](openstack-plugin-installation.md) guide.
///

## Prerequisites

* All prerequisites from the [OpenStack Plugin Installation](openstack-plugin-installation.md) guide must be met
* EDA Kubernetes preparation steps (Service Account and Token) must be completed
* Red Hat OpenStack Platform Director (undercloud) is installed and operational
* Refer to
  the [Red Hat OpenStack Platform Director Installation Guide](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1)
  for details on setting up the undercloud and overcloud

## Overview

The installation process involves the following main steps:

1. Prepare custom container images that include the Nokia EDA Connect plugin
2. Configure Neutron with the EDA Connect mechanism driver
3. Deploy or update the overcloud with the EDA Connect integration
4. Configure LLDP on all compute and controller nodes for topology discovery

## Installation Steps

### Step 1: Get Container Registry Credentials

The EDA Connect OpenStack Plugin images are hosted on `registry.connect.redhat.com/nokia-ni` requiring authentication. You will need credentials to
pull the Nokia-published container images for:

* `neutron-server`
* `neutron-openvswitch-agent`

/// details | Getting the container registry credentials
    type: info

Contact your Red Hat representative to obtain the credentials for accessing the Nokia container images in the Red Hat Container Catalog.

The credentials will be in the format of a username (or service key) and password that need to be configured in the
`ContainerImageRegistryCredentials` section during OpenStack deployment.
///

### Step 2: Prepare Container Images

The Nokia EDA Connect OpenStack plugin provides customized container images for `neutron-server` and `neutron-openvswitch-agent` that include the ML2
mechanism driver.

Create a container preparation parameters file to use the Nokia-published images:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/openstack-container-prepare-params.yaml"
```

///

/// tab | Example file

Create the file at `/home/stack/templates/container-prepare-parameters.yaml` and update the credentials section with your Nokia-provided credentials:

```bash
cat > /home/stack/templates/container-prepare-parameters.yaml <<'EOF'
--8<-- "docs/connect/resources/openstack-container-prepare-params.yaml"
EOF
```

///

/// warning | Default values of the container preparation parameters file

The values provided here are only examples. The example is based on the default RHOSP 17.1 template. If you have a customized deployment, ensure to
adjust the values accordingly. 
///

/// details | Container Registry Credentials
    type: note

Replace `<USERNAME>|<SERVICE_KEY>` and `<PASSWORD>` with the credentials provided by Red Hat for accessing the container registry. See
the [Get Container Registry Credentials](openstack-plugin-installation.md#create-a-service-account-token) section for more information.
///

Run the container image prepare command to generate the image list:

```bash
openstack tripleo container image prepare \
    -e /home/stack/templates/container-prepare-parameters.yaml \
    --output-env-file /home/stack/templates/overcloud-images.yaml
```

### Step 3: Configure EDA CA Certificate (If required)

If your EDA Kubernetes cluster uses a self-signed certificate, you must inject the certificate authority into the overcloud image.

Create a file at `/home/stack/templates/inject-trust-anchor.yaml`:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/openstack-inject-trust-anchor.yaml"
```

///

/// tab | Example file

```bash
cat > /home/stack/templates/inject-trust-anchor.yaml <<EOF
--8<-- "docs/connect/resources/openstack-inject-trust-anchor.yaml"
EOF
```

///

Replace `<EDA_CA_CERTIFICATE_CONTENT>` with the CA certificate content obtained earlier using:

```bash
kubectl get secrets/openstack-plugin -n eda-system -o 'template={{index .data "ca.crt"}}' | base64 --decode
```

/// details | Official CA certificates
    type: info

If the EDA Kubernetes cluster uses certificates signed by a well-known certificate authority that is already trusted by the overcloud nodes, you can
skip this step and omit the `ca_cert_path` parameter from the Neutron configuration.
///

### Step 4: Configure Neutron for EDA Connect

Create an environment file at `/home/stack/templates/neutron-eda-connect-config.yaml` with the EDA Connect plugin configuration:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/openstack-neutron-eda-config.yaml"
```

///

/// tab | Example file

```bash
cat > /home/stack/templates/neutron-eda-connect-config.yaml <<'EOF'
--8<-- "docs/connect/resources/openstack-neutron-eda-config.yaml"
EOF
```

///

Update the following parameters in the file:

**`ml2_eda_connect/plugin_name`**
: A unique name for this OpenStack deployment within EDA (e.g., `openstack-plugin` or `rhosp-prod`)

/// warning | Plugin Name Requirements
The plugin name must comply with the regex check of `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'` and can only contain alphanumerical characters and
`.`, `_` and `-`. It must start with an alphanumerical character, and have a length of 63 characters or fewer.
///

**`ml2_eda_connect/api_host`**
: The API endpoint of the EDA Kubernetes cluster (e.g., `https://api.eda.example.com:6443`)

**`ml2_eda_connect/api_namespace`**
: The namespace in EDA where the fabric is configured (e.g., `default` or your custom namespace)

**`ml2_eda_connect/api_token`**
: The bearer token obtained from the service account token secret in
the [Create a Service Account Token](openstack-plugin-installation.md#create-a-service-account-token) section

**`ml2_eda_connect/ca_cert_path`**
: Path to the CA certificate file (use `/etc/pki/ca-trust/source/anchors/eda.crt.pem` if injecting the certificate, or omit if using a trusted CA)

/// details | Additional Configuration Parameters explained
    type: note

- **NIC Mapping Provisioning**: Enables the automatic discovery of the physical NIC to Neutron network topology
- **Mechanism Drivers**: The `eda_connect` driver must be listed to enable fabric orchestration
- **Service Plugins**: The `nic_mapping` plugin is required for topology discovery
- **Plugin Extensions**: The `eda_network` extension enables EDA-managed networking features

/// warning | Example values

The values provided here are only examples. The example is based on the default RHOSP 17.1 template. If you have a customized deployment, ensure to
adjust the values accordingly.
///
///


### Step 5: Configure NIC Bonding (Optional)

If your deployment uses bonded interfaces for high availability or increased bandwidth, configure the appropriate bond type in your NIC configuration
templates.

#### Linux Bonds (for VIRTIO and SR-IOV)

For active-backup mode Linux bonds an example configuration is as follows:

```yaml
--8<-- "docs/connect/resources/openstack-linux-bond-example.yaml"
```

Supported bonding modes:

- `mode=active-backup`: Active/standby failover
- `mode=802.3ad`: LACP-based link aggregation

/// note
For active-backup mode, no LAG configuration is required in EDA. For 802.3ad mode, configure a LAG with LACP settings in the EDA `Interfaces`.
///

#### OVS DPDK Bonds

For balance-tcp mode with LACP an example is as follows:

```yaml
--8<-- "docs/connect/resources/openstack-ovs-dpdk-bond-example.yaml"
```

Supported bonding modes:

- `bond_mode=active-backup`: Active/standby failover
- `bond_mode=balance-tcp` with `lacp=active`: LACP-based load balancing

/// note
For balance-tcp mode with LACP, configure a LAG with LACP settings in the EDA `Interfaces`.
///

/// warning | Example Bond Configuration

Make sure to adapt the above examples to your specific deployment and bonding requirements.
///

### Step 6: Deploy or Update the Overcloud

Add the environment files created above to your `openstack overcloud deploy` command:

```bash
openstack overcloud deploy \
    --log-file overcloud_deployment.log \
    --templates /usr/share/openstack-tripleo-heat-templates/ \
    --stack overcloud \
    -n /home/stack/templates/network_data.yaml \
    -r /home/stack/templates/roles_data.yaml \
    -e /home/stack/templates/overcloud-baremetal-deployed.yaml \
    -e /home/stack/templates/overcloud-networks-deployed.yaml \
    -e /home/stack/templates/overcloud-vip-deployed.yaml \
    -e /home/stack/templates/overcloud-images.yaml \
    -e /home/stack/templates/neutron-eda-connect-config.yaml \
    -e /home/stack/templates/inject-trust-anchor.yaml
```

/// details | Environment file order
    type: warning

The order of environment files matters. Ensure that:

1. `overcloud-images.yaml` is included to use the Nokia container images
2. `neutron-eda-connect-config.yaml` comes after any base Neutron configuration
3. `inject-trust-anchor.yaml` is included if using self-signed certificates
///

/// details | Updating an existing deployment
    type: note

If updating an existing overcloud deployment, you can use the `openstack overcloud update` command instead. Make sure to include all the environment
files from the original deployment plus the new EDA Connect configuration files.
///

### Step 7: Configure LLDP on Overcloud Nodes

After the overcloud deployment completes, LLDP must be enabled on all data plane interfaces of the controllers and computes for topology discovery.

Create an Ansible playbook file at `/home/stack/post-overcloud-lldp.yaml`:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/openstack-lldp-playbook.yaml"
```

///

/// tab | Example file

```bash
cat > /home/stack/post-overcloud-lldp.yaml <<'EOF'
--8<-- "docs/connect/resources/openstack-lldp-playbook.yaml"
EOF
```

///

Run the playbook against the overcloud inventory:

```bash
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -v \
    -i ~/overcloud-deploy/overcloud/config-download/overcloud/tripleo-ansible-inventory.yaml \
    /home/stack/post-overcloud-lldp.yaml
```

/// details | LLDP package requirements
    type: warning

The playbook depends on the availability of the `lldpd` package on overcloud nodes. Overcloud nodes must be registered to Red Hat Subscription
Manager (RHSM) to install the package. Alternatively, you can modify the overcloud image to include the `lldpd` package before deployment.
///

/// details | Customizing interface patterns
    type: note

The default interface pattern `em*,en*,p*,!en*v*,!p*v*` matches most physical interfaces while excluding virtual interfaces. You can override this by
passing the `nic_pattern` variable to the playbook:

```bash
ansible-playbook -v -i <inventory> post-overcloud-lldp.yaml -e "nic_pattern='ens*,eno*'"
```

///

## Post-Installation Configuration

### Verify LLDP is Functioning

On one of the overcloud compute or controller nodes, verify LLDP is transmitting and receiving:

```bash
sudo lldpcli show neighbors
```

You should see the connected fabric switches listed as neighbors.

### Verify Topology Discovery

From the undercloud or a system with OpenStack client access, verify the NIC mapping has been discovered:

```bash
openstack eda interface mapping list
```

This should display the discovered mappings between physical networks and compute node interfaces.


## Troubleshooting

### Neutron Server Fails to Start

If the Neutron server container fails to start, check the logs:

```bash
sudo podman logs neutron_api
```

Common issues:

- Invalid API token: Verify the token is correct and not expired
- Cannot reach EDA API: Check network connectivity and the API host URL
- Certificate validation errors: Ensure the CA certificate is correctly injected

### LLDP Not Discovering Topology

If topology discovery is not working:

1. Verify LLDP is running on overcloud nodes:
   ```bash
   sudo systemctl status lldpd
   ```

2. Check LLDP is configured with the correct interface pattern:
   ```bash
   sudo lldpcli show configuration
   ```

3. Verify the fabric switches have LLDP enabled on the interfaces connected to OpenStack nodes

### Networks Not Creating BridgeDomains in EDA

If OpenStack networks are not creating corresponding BridgeDomains in EDA:

1. Check the Neutron controller logs for errors:

2. Verify the ConnectPlugin is registered and healthy in EDA:
   ```bash
   kubectl get connectplugins -n <eda-namespace> -o yaml
   ```

3. Ensure the network is created with `provider-network-type vlan` (the plugin only manages VLAN networks)

### Updating the Bearer Token After Installation

If you need to update the bearer token after installation:

1. Update the configuration file on all controller nodes at `/var/lib/config-data/puppet-generated/neutron/etc/neutron/plugins/ml2/ml2_conf.ini`:

   ```ini
   [ml2_eda_connect]
   api_token = <new_api_token>
   ```

2. Restart the Neutron server container on all controllers


