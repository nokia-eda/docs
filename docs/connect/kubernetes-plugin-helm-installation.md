# Kubernetes Plugin Helm Installation

This guide provides step-by-step instructions for installing the EDA Connect Kubernetes plugin using Helm charts.

/// warning
Before proceeding with this installation method, ensure you have completed all the prerequisites and preparation steps described in the [Kubernetes Plugin Installation](kubernetes-plugin-installation.md) guide.
///

## Prerequisites

* All prerequisites from the [Kubernetes Plugin Installation](kubernetes-plugin-installation.md) guide must be met
* EDA Kubernetes preparation steps (Service Account and Token) must be completed
* Helm 3.x installed on your system

## Installation Steps

### Step 1: Fetch the EDA Connect OpenShift Plugin Helm Charts

There are two ways to get the Helm charts to deploy the EDA Connect OpenShift plugin:

1. Using the EDA Playground (if you used it to install EDA):

    ```bash
    make download-connect-k8s-helm-charts
    ```

2. Downloading the release tarball and unpacking it:

    ```bash
    curl -sLO https://github.com/nokia-eda/connect-k8s-helm-charts/archive/refs/tags/5.0.0.tar.gz
    tar zxf 5.0.0.tar.gz 
    ```

### Step 2: Create a Namespace for the OpenShift Plugin

The OpenShift Plugin uses its own namespace to separate it from other resources in the OpenShift cluster:

```bash
kubectl create namespace eda-connect-k8s-controller
```

### Step 3: Configure a Pull Secret for the Controller Image

If the EDA Connect OpenShift Plugin Controller image is hosted in a registry that requires authentication, create a Kubernetes secret for OpenShift to pull the image:

```bash
export PULL_TOKEN=<PULL_TOKEN>
kubectl create secret docker-registry eda-k8s-image-secret \
  --docker-server=ghcr.io/nokia-eda/eda-connect-k8s-controller \
  --docker-username=nokia-eda-bot \
  --docker-password=${PULL_TOKEN} \
  -n eda-connect-k8s-controller
```

/// details | Getting the pull token
    type: info

The pull token can be retrieved from your EDA deployment. See the [Get the Pull Token](kubernetes-plugin-installation.md#get-the-pull-token) section in the main installation guide for detailed instructions.
///

### Step 4: Set Up the Helm Values

Create a `helm-values.yaml` file with the following content and update the fields as appropriate:

```yaml
--8<-- "docs/connect/resources/openshift-helm-values.yaml"
```

#### Helm Values Reference

The possible Helm Values are:

**`connectpluginname`**
: A name for the plugin. Make sure this is a unique name within your EDA environment.

/// warning | Plugin Name Requirements
The plugin name must comply with the regex check of `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'` and can only contain alphanumerical
characters and `.`, `_` and `-`. It must start with an alphanumerical character, and have a length of 63 characters or fewer.
///

**`heartbeat`**
: The interval in seconds at which the plugin should send heartbeats. Values between 10-30 are recommended.

_**`namespace`**
: A name of a namespace in EDA containing the fabric and resources.

/// details | EDA Namespace
    type: warning
The EDA Namespace is the namespace in EDA where the fabric is configured. This is different from the `eda-system` namespace used for EDA system components.
///

**`skiptlsverify`**
: Can be enabled to disable server TLS certificate verification when connecting to the EDA Kubernetes cluster (not recommended for production).

**`tlscertificatedata`**
: When certificate validation is enabled, this property can contain the certificate information of the EDA Kubernetes cluster, similar to what a kubeconfig would contain. This is only needed if certificate validation is enabled and if the EDA Kubernetes certificate has not been signed by a trusted authority.

**`tlsenabled`**
: Should always be true to make sure TLS is used to secure the communication with the EDA Kubernetes cluster.

**`connectHost`**
: The URL to reach the EDA Kubernetes cluster API.

**`connectPassword`**
: The long-lived token created in the [Create a Service Account Token](kubernetes-plugin-installation.md#create-a-service-account-token) section.

**`connectUsername`**
: The service account name for the account created in the [Create a Service Account](kubernetes-plugin-installation.md#create-a-service-account) section.

### Step 5: Deploy the Plugin

Deploy the EDA Connect OpenShift Plugin using Helm:

```bash
helm install eda-k8s connect-k8s-helm-charts/ \
  -n eda-connect-k8s-controller \
  -f helm-values.yaml \
  --set controller.imagePullSecretName=eda-k8s-image-secret
```

## Post-Installation Verification

After deployment, verify the installation was successful using the steps described in the [Post-Installation Verification](kubernetes-plugin-installation.md#post-installation-verification) section of the main installation guide.

