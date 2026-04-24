# Kubernetes Plugin Helm Installation

This guide provides step-by-step instructions for installing the EDA Connect Kubernetes plugin using Helm charts.

/// warning
Before proceeding with this installation method, ensure you have completed all the prerequisites and preparation steps
described in the [Kubernetes Plugin Installation](index.md) guide.
///

## Prerequisites

* All prerequisites from the [Kubernetes Plugin Installation](index.md) guide must be met
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
    curl -sLO https://github.com/nokia-eda/connect-k8s-helm-charts/archive/refs/tags/5.0.0-1.tar.gz
    tar zxf 5.0.0-1.tar.gz 
    ```

/// details | Updating helm charts
    type: info

To update the Helm charts to a newer version, simply execute
```make update-connect-k8s-helm-charts``` or download and unpack the newer release tarball as shown above. Make sure to
update the version number in the command accordingly.

///

### Step 2: Create a Namespace for the OpenShift Plugin

The OpenShift Plugin uses its own namespace to separate it from other resources in the OpenShift cluster:

```bash
kubectl create namespace eda-connect-k8s-controller
```

### Step 3: Configure the Controller Image

When the EDA Connect OpenShift Plugin Controller is being installed in an internet-enabled cluster, no further configuration is needed.


/// details | Airgapped Environments
    type: warning
If your OpenShift cluster does not have access to the public registry where the controller image is hosted, you
can use the mirror set up by the airgapped installation method. You'll need to update
the `controller.image` field in the Helm values to point to the mirrored image in your registry.

See [Step 5](#step-5-deploy-the-plugin) for detailed instructions on how to update the Helm values for this scenario.
An example helm install command with the updated image field would look like this:

```bash

helm install eda-k8s connect-k8s-helm-charts/ \
  -n eda-connect-k8s-controller \
  -f helm-values.yaml \
  --set controller.image=your-registry/eda-connect-k8s-controller:5.0.0 \
  --set controller.imagePullSecretName="" # No pull secret needed when using mirrored image in airgapped environment
```

/// details | Update the saved bundle in edaadm
    type: warning
Make sure to run 
```bash 
make save-eda-bundle-connect-k8s-plugin-5-0-0
```
to update the saved bundle with the latest image reference in the eda adm deployment.
///

///

### Step 4: Set Up the Helm Values

Create a `helm-values.yaml` file with the following content and update the fields as appropriate:

```yaml
--8<-- "docs/apps/connect/resources/openshift-helm-values.yaml"
```

#### Helm Values Reference

The possible Helm Values are:

**`connectpluginname`**
: A name for the plugin. Make sure this is a unique name within your EDA environment.

/// details | Plugin Name Requirements
    type: warning
The plugin name must comply with the regex check of `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'` and can only contain
alphanumerical
characters and `.`, `_` and `-`. It must start with an alphanumerical character, and have a length of 63 characters or
fewer.
///

**`heartbeat`**
: The interval in seconds at which the plugin should send heartbeats. Values between 10-30 are recommended.

**`namespace`**
: A name of a namespace in EDA containing the fabric and resources.

/// details | EDA Namespace
    type: warning
The EDA Namespace is the namespace in EDA where the fabric is configured. This is different from the `eda-system` namespace used for EDA system components.
///

**`skiptlsverify`**
: Can be enabled to disable server TLS certificate verification when connecting to the EDA Kubernetes cluster (not
recommended for production).

**`tlscertificatedata`**
: When certificate validation is enabled, this property can contain the certificate information of the EDA Kubernetes
cluster, similar to what a kubeconfig would contain. This is only needed if certificate validation is enabled and if the
EDA Kubernetes certificate has not been signed by a trusted authority.

**`tlsenabled`**
: Should always be true to make sure TLS is used to secure the communication with the EDA Kubernetes cluster.

**`connectHost`**
: The URL to reach the EDA Kubernetes cluster API.

**`connectPassword`**
: The long-lived token created in
the [Create a Service Account Token](index.md#create-a-service-account-token) section.
Make sure to base64 decode the token:

```bash
echo "$TOKEN" | base64 --decode
```

**`connectUsername`**
: The service account name for the account created in
the [Create a Service Account](index.md#create-a-service-account) section.

### Step 5: Deploy the Plugin

Deploy the EDA Connect OpenShift Plugin using Helm:

```bash
helm install eda-k8s connect-k8s-helm-charts/ \
  -n eda-connect-k8s-controller \
  -f helm-values.yaml
```

## Post-Installation Verification

After deployment, verify the installation was successful using the steps described in
the [Post-Installation Verification](index.md#post-installation-verification) section of the
main installation guide.

