# OpenStack Plugin RHOSO 18 Installation

This guide provides step-by-step instructions for installing the Nokia EDA Connect OpenStack plugin on **Red Hat OpenStack Services on OpenShift (RHOSO)
18.0** using the **OpenStack Operator** on **Red Hat OpenShift Container Platform (RHOCP)**.

/// warning
Before proceeding with this installation method, ensure you have completed all the prerequisites and preparation steps described in the
[OpenStack Plugin Installation](index.md) guide.
///

## Prerequisites

* All prerequisites from the [OpenStack Plugin Installation](index.md) guide must be met
* EDA Kubernetes preparation steps (Service Account and Token) must be completed
* A **RHOCP** cluster that meets RHOSO 18.0 requirements. Red Hat documents validated combinations for each RHOSO release; plan the cluster using
  [Planning your deployment](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/planning_your_deployment/index)
  and
  [Preparing RHOCP for RHOSO](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_preparing-rhocp-for-rhoso)
* **OpenStack Operator** installed in the `openstack-operators` namespace (see
  [Installing and preparing the OpenStack Operator](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_installing-and-preparing-the-openstack-operator))
* Access to **Nokia EDA Connect** container images on `registry.connect.redhat.com/nokia-ni` for the Neutron API and `openstackclient` images used on
  RHOSO 18
* Administrative access to the OpenShift cluster (`oc`) and to the EDA Kubernetes cluster (`kubectl`)

/// details | Getting the container registry credentials
    type: info

Contact your Red Hat representative to obtain credentials for accessing the Nokia container images in the Red Hat Container Catalog. Configure
`registry.connect.redhat.com` in the cluster pull secret (or equivalent image pull authentication for the `openstack` namespace) so worker nodes
can pull the Neutron and `openstackclient` images after you reference them in `OpenStackVersion`.
///

/// details | RHOSP 17.1 vs. RHOSO 18
    type: note

| Aspect                 | RHOSP 17.1 (TripleO)                   | RHOSO 18 (OCP)                                |
|------------------------|----------------------------------------|-----------------------------------------------|
| Neutron deployment     | Podman containers via Heat             | Kubernetes pods via OpenStack Operator        |
| EDA ML2 settings       | TripleO environment file               | Kubernetes `Secret` mounted into Neutron pods |
| Nokia container images | `container-image-prepare` overrides    | `OpenStackVersion.spec.customContainerImages` |
| CA certificate         | `inject-trust-anchor` Heat environment | Kubernetes `Secret` and volume mount          |
| LLDP on computes       | Post-deploy Ansible playbook           | `OpenStackDataPlaneService` on the data plane |

///


## Installation Steps

### Step 1: Prepare EDA specific artifacts

#### EDA CA Certificate Secret (If Required)

If the EDA K8S API uses a self-signed certificate, store the CA in a `Secret` in the `openstack` namespace. The file should contain the PEM CA Certificate
you retrieved earlier (see also [OpenStack Plugin Installation](index.md#create-a-service-account-token)).

/// details | Trusted public CA
type: info

If EDA uses certificates signed by a well-known certificate authority, skip creating `eda-ca-secret`, omit the CA volume from `extraMounts`, and remove
the `ca_cert_path` setting from the ML2 fragment in Step 5.
///

```bash
oc create secret generic eda-ca-secret \
  --from-file=eda.crt=/path/to/eda-ca.crt \
  -n openstack
```

Replace `/path/to/eda.crt` with the path to the saved CA certificate.


#### Neutron ML2 EDA Connect Secret

Create a `Secret` that holds the `[ml2_eda_connect]` configuration consumed by Neutron. Use a temporary file, then create the secret:

/// tab | INI fragment

```ini
--8<-- "docs/apps/connect/resources/openstack-rhoso-eda-ml2.ini"
```

///

/// tab | Example commands

```bash
cat > /tmp/eda-ml2.conf <<'EOF'
--8<-- "docs/apps/connect/resources/openstack-rhoso-eda-ml2.ini"
EOF

oc create secret generic nokia-eda-ml2-config \
  --from-file=eda.conf=/tmp/eda-ml2.conf \
  -n openstack
rm /tmp/eda-ml2.conf
```

///

Update the placeholders in the fragment before creating the secret:

**`plugin_name`**
: A unique name for this OpenStack deployment in EDA (for example `rhoso-prod`)

/// warning | Plugin name requirements
The plugin name must comply with the regex `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'`, contain only alphanumerics and `.`, `_`, `-`, start with an
alphanumeric, and be at most 63 characters.
///

**`api_host`**
: EDA Kubernetes API hostname (for example `api.eda.example.com`); the URI in the file must include `https://` and port `:6443` as shown

**`api_namespace`**
: Namespace where the fabric is configured in EDA

**`api_token`**
: Bearer token from the [Create a Service Account Token](index.md#create-a-service-account-token) section

**`ca_cert_path`**
: Use `/etc/pki/ca-trust/source/anchors/eda.crt` when using `eda-ca-secret`; omit the line entirely if EDA uses a public CA

**`heartbeat_interval`**
: Optional; shown as `10` seconds in the example


### Step 2: OpenStack Operator and Namespaces

On the **OpenShift** cluster, create the operator and workload namespaces and install the OpenStack Operator following Red Hat's guide:

* [Installing and preparing the OpenStack Operator](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_installing-and-preparing-the-openstack-operator)

Use the YAML from the
current RHOSO documentation for your release rather than copying abbreviated examples here.
Follow chapters 1, 2 and 3 in the guide, continue here once you get to Chapter 4: "Creating the control plane". 



### Step 3: OpenStack Control Plane — Neutron and EDA Mounts

During chapter 4 of the Red Hat guide, you will have to adjust some steps as detailed below.

Build your **`OpenStackControlPlane`** custom resource from
[Creating the control plane](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_creating-the-control-plane).
Merge Red Hat’s full control plane `spec` (DNS, Keystone, Nova, Cinder, Glance, storage class, secrets, and so on) with the adjusted Neutron settings below.

For EDA Connect, we will heavily modify the neutron section of the `OpenStackControlPlane` custom resource, as touched upon in the Red Hat [Configuring network services](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html-single/configuring_networking_services/index) and [Integrating partner content](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html-single/integrating_partner_content/index#set-custom-configuration-for-the-networking-driver_integrating-rhoso-networking-services)]guide:

/// warning | Configuration example

The below configuration is an example of the neutron section of the `OpenStackControlPlane` custom resource. Adapt it to your environment. Important elements of the configuration have been annotated with (+) to explain their purpose.

///
```yaml
apiVersion: core.openstack.org/v1beta1
kind: OpenStackControlPlane
metadata:
  name: openstack
  namespace: openstack
spec:
  secret: osp-secret
  storageClass: <STORAGE_CLASS>       # e.g. ocs-storagecluster-ceph-rbd

  # ... (DNS, Keystone, Nova, Cinder, Glance, etc. — see upstream guide)
  # https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_creating-the-control-plane

  neutron:
    enabled: true
    apiOverride:
      route: {}
    template:
      databaseInstance: openstack
      secret: neutron-secret
      networkAttachments:
        - internalapi
      replicas: 3

      customServiceConfig: | #(2)!
        [DEFAULT]
        debug = True
        service_plugins = ovn-router,segments,trunk,qos,port_forwarding,placement,nic_mapping

        [ml2]
        type_drivers = flat,vlan,vxlan
        tenant_network_types = vlan,vxlan
        mechanism_drivers = ovn,eda_connect,sriovnicswitch
        extension_drivers = eda_network,port_security,qos,uplink_status_propagation,dns_domain_keywords

        [ml2_type_vlan]
        network_vlan_ranges = datacentre:1:4094

      # Mount the EDA ML2 config secret and CA cert into the Neutron pod
      extraMounts: 
        - extraVol:
            - mounts:
                - name: nokia-eda-config #(3)!
                  mountPath: /etc/neutron/neutron.conf.d/ml2_eda_connect.conf
                  subPath: ml2_eda_connect.conf
                  readOnly: true
                - name: eda-ca-cert #(4)!
                  mountPath: /etc/pki/ca-trust/source/anchors/eda.crt
                  subPath: eda.crt
                  readOnly: true
              volumes:
                - name: nokia-eda-config #(3)!
                  secret:
                    secretName: nokia-eda-ml2-config
                - name: eda-ca-cert #(4)!
                  secret:
                    secretName: eda-ca-secret
```

1. Custom Neutron image from registry.connect.redhat.com/nokia-ni that includes the eda_connect ML2 driver, adjust the image tag to the appropriate one for your environment.
2. We override the configuration of the Neutron service to include the eda_connect mechanism driver and the eda_network extension driver.
   Note that all other configuration should be adapted to your environment, you can omit any entries to use the default values.
3. We mount the nokia-eda-ml2-config from Step 1 to provide the EDA Connect OpenStack ML2 plugin with its configuration.
4. If the EDA K8S API uses a self-signed CA, we mount that CA in the pod to validate communication with the EDA K8S API. Leave this block out if the EDA K8S API is signed by an official CA.


Do **not** set a custom Neutron `containerImage` on the control plane for the Nokia image. Image overrides are applied in Step 8 via
`OpenStackVersion` so they persist across operator reconciliation.

Apply your control plane manifest with the configuration for all other services as normal and continue with step 4.

### Step 4: Nokia Container Images Override

To adapt the deployment with the correct images for the EDA Connect OpenStack driver, adapt the `OpenStackVersion` CR. The `OpenStackVersion` object is created when the OpenStack Operator reconciles the control plane. Wait until it exists, then patch
**`spec.customContainerImages`** so Neutron API and the `openstackclient` deployment use Nokia images that include the EDA mechanism driver and the
`python-eda-openstackclient` extension.

```bash
oc wait openstackversion openstack -n openstack \
  --for=condition=Initialized \
  --timeout=120s
```

/// tab | Example `oc patch`

```bash
oc patch openstackversion openstack -n openstack \
  --type merge -p '{
    "spec": {
      "customContainerImages": {
        "neutronAPIImage": "registry.connect.redhat.com/nokia-ni/rhoso18-openstack-neutron-server-nokia-eda:<TAG>",
        "openstackClientImage": "registry.connect.redhat.com/nokia-ni/rhoso18-openstack-openstackclient-nokia-eda:<TAG>"
      }
    }
  }'
```

///

Replace `<TAG>` with the image tags supplied by Nokia or Red Hat. Ensure the cluster can authenticate to `registry.connect.redhat.com` (for example
via the global pull secret), as described under **Getting the container registry credentials** in the prerequisites.

Verify the patch of the `OpenStackVersion` CR:

```bash
oc get openstackversion openstack -n openstack \
  -o jsonpath='{.spec.customContainerImages}' | jq .
```

Wait for the control plane to become ready after the patch:

```bash
oc wait openstackcontrolplane openstack \
  --for=condition=Ready \
  --timeout=1200s \
  -n openstack
```

Verify the EDA Connect ML2 driver was loaded:

```bash
# Get the neutron-server pod name
NEUTRON_POD=$(oc get pods -n openstack -l service=neutron -o jsonpath='{.items[0].metadata.name}')

# Check logs for EDA Connect initialization
oc logs ${NEUTRON_POD} -n openstack | grep -i "eda_connect"
```
Expected output should include lines indicating the plugin initialized and registered with EDA.



### Step 5: Data Plane

Continue with chapter 5 [Creating the data plane](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_creating-the-data-plane) in the Red Hat guide.

EDA Connect requires **LLDP** on data plane interfaces of compute nodes. On RHOSO 18, model that with an `OpenStackDataPlaneService` before proceeding beyond step 5.3 "Creating the data plane secrets":

/// tab | YAML Resource

```yaml
--8<-- "docs/apps/connect/resources/openstack-rhoso-edpm-lldp-service.yaml"
```

///

/// tab | `oc apply`

```bash
oc apply -f - <<'EOF'
--8<-- "docs/apps/connect/resources/openstack-rhoso-edpm-lldp-service.yaml"
EOF
```

///

/// details | Interface pattern
    type: info

The default pattern `em*,en*,p*,!en*v*,!p*v*` matches most physical interfaces while excluding common virtual patterns. Override the playbook content
if your NIC naming differs.
///



### Step 6: Creating the OpenStackDataPlaneNodeSet

Define your `OpenStackDataPlaneNodeSet` following
[Creating the data plane](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_creating-the-data-plane)
and, if applicable,
[Deploying an NFV environment with SR-IOV and DPDK](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_a_network_functions_virtualization_environment/assembly_create-data-plane-sriov-dpdk_rhoso-nfv).

Include the previously created `edpm-lldp-service* in `spec.services` after the standard services that should run before LLDP (for example after `ovn` and Neutron
metadata services). Exact ordering should follow your validated service list from Red Hat; a typical pattern is to add `edpm-lldp-service` alongside
other post-network services.


/// details | Example OpenStackDataPlaneNodeSet YAML
    type: info

/// warning | Example only
Node network templates, SR-IOV mappings, repositories, and node addresses are environment-specific. Do not copy values from examples without aligning
them to your hardware and RHOSO network design.
///


```yaml
--8<-- "docs/apps/connect/resources/openstack-rhoso-dataplanenodeset.yaml"
```
///

Apply the nodeset as normal and wait for it to complete.


### Step 7: Deploy the Data Plane

After the nodeset is deployed, continue deploying the data plane following the steps in [Deploying the data plane](https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_creating-the-data-plane#proc_deploying-the-data-plane_dataplane) in the Red Hat guide.


## Post-Installation Configuration

### Verify the EDA mechanism driver in Neutron

```bash
NEUTRON_POD=$(oc get pods -n openstack -l service=neutron -o jsonpath='{.items[0].metadata.name}')
oc logs ${NEUTRON_POD} -n openstack | grep -iE "eda_connect|eda connect"
```

You should see log lines indicating the EDA Connect mechanism driver initialized and registered with EDA.

### Verify the EDA CLI extension (`openstackclient`)

```bash
oc rsh -n openstack "$(oc get pod -n openstack -l app=openstackclient -o jsonpath='{.items[0].metadata.name}')" \
  openstack eda interface mapping --help
```


### Verify LLDP on EDPM nodes

On a compute node (SSH as your EDPM user, for example `cloud-admin`):

```bash
sudo systemctl status lldpd
sudo lldpcli show neighbors
```

### Verify topology discovery

From a host or pod where the OpenStack CLI is configured with credentials for the RHOSO cloud (including the `openstackclient` pod if you use the Nokia
client image there):

```bash
openstack eda interface mapping list
```

### Verify registration in EDA

On the EDA cluster:

```bash
kubectl get connectplugins -n <eda-namespace>
```


## Troubleshooting

### Neutron pods fail or restart

```bash
oc describe pod -n openstack -l service=neutron
oc logs -n openstack -l service=neutron --tail=200 --previous
```

Common causes:

* **Invalid or expired API token**: Recreate the `nokia-eda-ml2-config` secret with an updated ML2 fragment, then restart Neutron API pods so they load
  the new secret (for example `oc delete pod -n openstack -l service=neutron`, or `oc rollout restart` on the Neutron API workload if your RHOSO
  revision exposes it as a `Deployment`).
* **Unreachable EDA API**: Confirm routes and DNS from OpenShift worker nodes to the host in `api_host`.
* **TLS errors**: Confirm `eda-ca-secret` matches `ca_cert_path` and the mount path in `extraMounts`.

### LLDP does not show fabric neighbors

1. Confirm `lldpd` is running on the EDPM node.
2. Inspect `/etc/lldpd.d/eda-connect.conf` and adjust the interface pattern if NIC names do not match.
3. Confirm LLDP is enabled on the fabric ports toward the servers.

### VLAN networks do not create `BridgeDomain` objects in EDA

* Networks must use **`provider-network-type vlan`** for EDA orchestration.
* Check Neutron logs for EDA-related errors.
* In EDA: `kubectl get connectplugins -n <eda-namespace> -o yaml` and verify status.

### SR-IOV kernel arguments not active

If IOMMU flags are not present in `/proc/cmdline` after deployment, run a data plane deployment that includes the `reboot-os` service (see Red Hat
EDPM documentation) so nodes reboot into the configured kernel.


## Reference

| Resource                                   | URL                                                                                                                                                                                                   |
|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RHOSO 18 Deployment Guide                  | https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/                                                         |
| RHOSO 18 Preparing RHOCP for RHOSO         | https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_preparing-rhocp-for-rhoso                       |
| RHOSO 18 Installing the OpenStack Operator | https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_installing-and-preparing-the-openstack-operator |
| RHOSO 18 Data Plane                        | https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_red_hat_openstack_services_on_openshift/assembly_creating-the-data-plane                         |
| RHOSO 18 NFV — SR-IOV and DPDK Data Plane  | https://docs.redhat.com/en/documentation/red_hat_openstack_services_on_openshift/18.0/html/deploying_a_network_functions_virtualization_environment/assembly_create-data-plane-sriov-dpdk_rhoso-nfv   |
| EDPM Ansible Variables                     | https://openstack-k8s-operators.github.io/edpm-ansible/                                                                                                                                               |
