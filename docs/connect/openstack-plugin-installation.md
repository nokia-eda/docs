# OpenStack Plugin Installation

This guide provides an overview and prerequisites for installing the EDA Connect OpenStack plugin on Red Hat OpenStack Platform (RHOSP) clusters.

## Installation Methods

The EDA Connect OpenStack plugin can be installed using the below method:

* **[RHOSP 17.1 Director Installation](openstack-plugin-rhosp-installation.md)**: Automated installation using Red Hat OpenStack Platform Director (
  TripleO)

[//]: # (* **Manual Installation**: Manual installation on existing OpenStack deployments &#40;documentation to be provided&#41;)

/// details | Non-RHOSP OpenStack Distributions
    type: warning
This guide focuses on installing the EDA Connect OpenStack plugin on Red Hat OpenStack Platform 17.1. While it may be possible to adapt these
instructions for other OpenStack distributions, such as vanilla OpenStack or other managed services, these environments are not officially supported.
Users attempting to deploy the plugin on unsupported OpenStack distributions do so at their own risk and may encounter issues that are not covered in
this documentation.
///

Make sure to first follow the preparation steps outlined in this guide before proceeding with either installation method.

## Prerequisites

Before installing or deploying the OpenStack plugin components, ensure that:

* The Cloud Connect Core application is properly installed in the EDA cluster (see [Cloud Connect Installation](cloud-connect-installation.md))
* You have administrative access to both the EDA Kubernetes cluster and the OpenStack environment
* The fabric is provisioned and operational in EDA
* You have access to the Nokia EDA Connect OpenStack plugin container images from `registry.connect.redhat.com/nokia-ni`

## EDA Kubernetes Preparation

All installation methods require the same preparation steps on the EDA Kubernetes cluster.

### Create a Service Account

The EDA Connect OpenStack plugin uses a `ServiceAccount` in the EDA Kubernetes cluster to create the necessary resources in the EDA cluster for the
integration to work properly.

To create a service account in the EDA Kubernetes cluster, use the following resource.

/// details | Service Account namespace
    type: warning
This service account must be created in the `eda-system` namespace. Make sure to adapt the namespace when using a customized namespace for EDA.
///

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/openstack-controller-sa-crb.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/openstack-controller-sa-crb.yaml"
EOF
```

///

### Create a Service Account Token

From the above Service Account, you need to create a Service Account Token that can be used by the plugin to connect to the EDA Kubernetes cluster.
This can be done with the below manifest, which should be applied on the EDA Kubernetes cluster.

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/openstack-service-account-token.yaml"
```

///

/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/openstack-service-account-token.yaml"
EOF
```

///

After creating the Service Account Token, retrieve the actual token and CA certificate using the following commands from the `eda-system` namespace:

**Retrieve the bearer token:**

```bash
kubectl get secrets/openstack-plugin -n eda-system --template={{.data.token}} | base64 --decode
```

**Retrieve the CA certificate (if EDA uses a self-signed certificate):**

```bash
kubectl get secrets/openstack-plugin -n eda-system -o 'template={{index .data "ca.crt"}}' | base64 --decode
```

These values will be needed during plugin deployment.

/// details | Service Account naming
    type: note
When using the OpenStack plugin in production, it is advised to create a service account per plugin instance. This way tokens can be revoked on a
per-plugin basis. If deploying multiple OpenStack clouds, create separate service accounts for each deployment.
///


## Post-Installation Verification

After completing either installation method, verify the deployment was successful.

### Verify Plugin Registration in EDA

On the EDA Kubernetes cluster, verify the plugin has been registered:

```bash
kubectl get connectplugins -n <eda-namespace>
```

The expected output should show your OpenStack plugin with status `Ready`:

```
NAME               STATUS   AGE
openstack-plugin   Ready    5m
```

### Verify the OpenStack Plugin is Active in OpenStack

From the OpenStack undercloud or a system with access to the overcloud controllers, check the Neutron server logs to verify the EDA Connect OpenStack plugin
loaded successfully:

```bash
sudo podman exec -it neutron_api grep -i "eda_connect" /var/log/neutron/server.log
```

You should see log entries indicating the OpenStack plugin initialized successfully and established communication with the EDA cluster.

### Verify Topology Discovery

Ensure LLDP is functioning properly and the OpenStack plugin can discover the network topology:

```bash
openstack eda interface mapping list
```

This command should display the discovered mappings between physical networks (physnets) and compute node interfaces.
