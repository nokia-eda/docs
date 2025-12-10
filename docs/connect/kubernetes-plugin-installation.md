# Kubernetes Plugin Installation

This guide provides an overview and prerequisites for installing the EDA Connect Kubernetes plugin on OpenShift clusters.

## Installation Methods

The EDA Connect Kubernetes plugin can be installed using two different methods:

* **[Helm-based Installation](kubernetes-plugin-helm-installation.md)**: Traditional installation using Helm charts
* **[OLM-based Installation](kubernetes-plugin-olm-installation.md)**: Installation using Red Hat Operator Lifecycle Manager (OLM)

Make sure to first follow the preparation steps outlined in this guide before proceeding with either installation method.

## Prerequisites

/// details | Other Kubernetes Distributions than OpenShift
type: warning

This guide focuses on installing the EDA Connect Kubernetes plugin on OpenShift clusters. While it may be possible to adapt these instructions for
other Kubernetes distributions, such as vanilla Kubernetes or other managed services, please note that these environments are not officially
supported. Users attempting to deploy the plugin on unsupported Kubernetes distributions do so at their own risk and may encounter issues that are not
covered in this documentation.

Make sure to review the Prerequisites section carefully, as some components mentioned may not be available or may require different installation
steps.
///

Before installing or deploying the Kubernetes plugin components, ensure that:

* The Cloud Connect Core application is properly installed in the EDA cluster (see [Cloud Connect Installation](cloud-connect-installation.md))
* The OpenShift cluster is up and running
* [NMState Operator](https://docs.openshift.com/container-platform/4.16/networking/networking_operators/k8s-nmstate-about-the-k8s-nmstate-operator.html)
  and Multus are installed on the OpenShift cluster
* You have access to the controller container image: `ghcr.io/nokia-eda/eda-connect-k8s-controller:5.0.0`
* NMState Operator is configured to listen for LLDP TLVs on interfaces connected to leaf switches

### Configure NMState for LLDP

Create the following resource in your OpenShift cluster, including all interfaces connected to leaf switches managed by EDA:

```yaml
apiVersion: nmstate.io/v1
kind: NodeNetworkConfigurationPolicy
metadata:
  name: enable-receive-lldp
spec:
  desiredState:
    interfaces:
      - name: <interface-name>
        lldp:
          enabled: true
```

## EDA Kubernetes Preparation

Both installation methods require the same preparation steps on the EDA Kubernetes cluster.

### Create a Service Account

The EDA Connect OpenShift plugin uses a `ServiceAccount` in the EDA Kubernetes cluster to create the necessary resources in the EDA cluster for the
integration to work properly.

To create a service account in the EDA Kubernetes cluster, use the following resource.

/// details | Service Account namespace
    type: warning
This service account must be created in the `eda-system` namespace. Make sure to adapt the namespace when using a customized namespace for EDA.
///

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/openshift-controller-sa-crb.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/openshift-controller-sa-crb.yaml"
EOF
```

///

### Create a Service Account Token

From the above Service Account, you need to create a Service Account Token that can be used by the plugin to connect to the EDA Kubernetes cluster.
This can be done with the below manifest, which should be applied on the EDA Kubernetes cluster.

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/openshift-service-account-token.yaml"
```

///

/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/openshift-service-account-token.yaml"
EOF
```

///

After creating the Service Account Token, retrieve the actual token using the following command from the `eda-system` namespace:

```bash
kubectl get secrets/k8s-controller-plugin -n eda-system --template={{.data.token}} | base64 --decode
```

This token will be needed during plugin deployment.

### Get the Pull Token

The EDA Connect OpenShift Plugin images are hosted on ghcr.io requiring authentication, you will need a pull token.

/// details | Getting the pull token
    type: note

The easiest way to get the token/password for the pull secret is extract it from your EDA deployment and look for the
`appstore-eda-apps-registry-image-pull` secret. By grabbing the content of that secret and using `base64` to decode the `dockerconfigjson`, you can
find the password in the resulting JSON file.

The following command shows how to get the token/password (make sure to have the KUBECONFIG for the EDA cluster loaded, not the OpenShift config):

```bash
kubectl get secret appstore-eda-apps-registry-image-pull -n eda-system -o json | jq -r '.data.".dockerconfigjson"' | base64 -d | jq -r '.auths."ghcr.io".password'
```

///

## Configuration Parameters

Both installation methods require similar configuration parameters. The exact parameter names may vary slightly between methods, but the following
information is needed:

**Plugin Name**
: A unique name for the plugin within your EDA environment.

/// warning | Plugin Name Requirements
The plugin name must comply with the regex check of `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'` and can only contain alphanumerical
characters and `.`, `_` and `-`. It must start with an alphanumerical character, and have a length of 63 characters or fewer.
///

**Heartbeat Interval**
: The interval in seconds at which the plugin should send heartbeats. Values between 10-30 seconds are recommended.

**EDA Namespace**
: The namespace in EDA containing the fabric and resources.

/// details | EDA Namespace
type: warning
The EDA Namespace is the namespace in EDA where the fabric is configured. This is different from the `eda-system` namespace used for EDA system components.
///

**TLS Configuration**
: - **TLS Enabled**: Should always be true to secure communication with the EDA Kubernetes cluster
- **Skip TLS Verify**: Can be enabled to disable server TLS certificate verification (not recommended for production)
- **TLS Certificate Data**: Certificate information of the EDA Kubernetes cluster (only needed if certificate validation is enabled and the
certificate is not signed by a trusted authority)

**EDA Connect Credentials**
: - **Connect Host**: The URL to reach the EDA Kubernetes cluster API
- **Connect Username**: The service account name created in the [Create a Service Account](#create-a-service-account) section
- **Connect Password**: The long-lived token created in the [Create a Service Account Token](#create-a-service-account-token) section

## Post-Installation Verification

After completing either installation method, verify the deployment was successful.

### Verify the Controller is Running in OpenShift

Check if the controller pod is running in the OpenShift cluster:

```bash
kubectl get pods -n eda-connect-k8s-controller
```

/// details | Controller namespace
    type: note
If you used OLM installation, the namespace may be different. Use the namespace where you installed the EDA OpenShift Operator.
///

The expected output:

```
NAME                                            READY   STATUS    RESTARTS   AGE
connect-k8s-controller-manager-c8d4875bc-bpzrx  2/2     Running   0          66m
```

### Verify Plugin Registration in EDA

On the EDA Kubernetes environment, verify the plugin has been registered:

```bash
kubectl get connectplugins -n <plugin-namespace>
```

Expected output:

```
NAME                                   PROVIDED NAME           PLUGIN TYPE   AGE
470e9af1-b85b-439b-b81a-ab71a7166bb0   k8s-controller-plugin   KUBERNETES    2h
```

## Next Steps

After successful installation and verification, proceed to:

* Create Network Attachment Definitions (NADs) in Kubernetes
* Configure Connect Network Definitions (CNDs) if needed
* Review the [Kubernetes Plugin documentation](kubernetes-plugin.md) for usage and operational modes

