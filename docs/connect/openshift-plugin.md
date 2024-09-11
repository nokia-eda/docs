# OpenShift Plugin

## Overview

EDA Cloud Connect integrates with OpenShift to provide fabric-level application networks for OpenShift pods and services. The Connect integration leverages the OpenShift Multus CNI solution to support managing the fabric directly from OpenShift and make the fabric dynamically respond to the networking needs of the application.

It provides the following advantages and capabilities:

* Direct integration into the network management workflow of OpenShift
* Use of the common CNIs used by Enterprise applications and CNFs like IPVLAN and SR-IOV
* Automatic provisioning of the fabric based on where the application pods need the connectivity
* Support for advanced workflows

### Supported Versions

* Red Hat OpenShift 4.14
* Red Hat OpenShift 4.16

## Prerequisites

Before using the Connect OpenShift Plugin, make sure the following prerequisites are met:

* Ensure Openshift cluster is up and running.
* Ensure [NMState-Operator](https://docs.openshift.com/container-platform/4.14/networking/k8s_nmstate/k8s-nmstate-about-the-k8s-nmstate-operator.html) and Multus are installed on openshift cluster.
* Ensure all the nodes which are connected to SRL leaf nodes have LLDP enabled on each node.
* Ensure EDA cluster is up and running.
* Ensure EDA Cloud Connect App is installed.
* Ensure you have access to the controller container image named `ghcr.io/nokia-eda/eda-connect-k8s-controller:v1.0.0`.

/// details | Known Limitations
    type: warning
The OpenShift Plugin currently requires LLDP to be enabled on the OpenShift hypervisors. This limitation will be lifted in a future release of EDA.
///

/// details | Using a Daemonset to enable LLDP
    type: note
When using RHCOS as the OS for the OpenShift nodes, it is not possible to install services inside the node to enable LLDP. Instead it is advised to deploy an LLDP Daemonset.

The following set of manifests can be used to deploy such an LLDP Daemonset:

```yaml
--8<-- "docs/connect/resources/openshift-lldp-daemonset.yaml"
```

///

## Architecture

The OpenShift Plugin consists of a controller which will monitor the following resources in OpenShift:

* The physical NIC configuration and correlation to `NetworkAttachmentDefinitions` through the NMState Operator.
* `NetworkAttachmentDefinitions` and their master interfaces.
* `ConnectNetworkDefinitions` for the configuration of Layer 2 and Layer 3 services configuration.

The OpenShift Plugin will support three ways of associating `NetworkAttachmentDefinitions` to EDA `BridgeDomains`:

*Transparent association*
: This association does not require any information from EDA in OpenShift. For every unique master interface defined in `NADs` in the OpenShift Cluster, the plugin will create a unique `BridgeDomain`. This association only supports OpenShift Managed Mode.

*Annotation based association*
: In this association, annotations are added to the `NAD` that reference an existing EDA `BridgeDomain`. This association only supports EDA Managed Mode.

*`ConnectNetworkDefinition` association*
: The `ConnectNetworkDefinition` is a Custom Resource Definition that gets added to the OpenShift Cluster and is used to describe the relationship between the different services and `NetworkAttachmentDefinitions`, and how the services relate to each other. This association supports both OpenShift Managed and EDA Managed Modes.

## EDA Connect OpenShift Plugin Deployment

### EDA Kubernetes Preparation

#### Create a Service Account

The EDA Connect OpenShift Plugin uses a `ServiceAccount` in the EDA Kubernetes cluster to create the necessary resources in the EDA cluster for the integration to properly work.

To create a service account in the EDA Kubernetes cluster, the following resource can be used.

//// details | Service Account and Cluster Role Binding manifest
    type: note

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
////

#### Create a Service Account Token

From the above Service Account, we need to create a Service Account Token which can be used by the plugin to connect to the EDA Kubernetes cluster. This can be done with the below manifest, which should be applied on the EDA Kubernetes cluster.

//// details | Service Account Token Manifest
    type: note

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
////

After creating the Service Account Token, you can retrieve the actual token itself using the following command. This token is what will need to be provided to the plugin during deployment.

```bash
kubectl get secrets/k8s-controller-plugin --template={{.data.token}} | base64 --decode
```

### Fetching the EDA Connect OpenShift plugin Helm charts

There are two ways to get the Helm charts to deploy the EDA Connect OpenShift plugin:

1. Clone the github repository:

    ```bash
    git clone --depth 1 --branch v1.0.0 https://github.com/nokia-eda/connect-k8s-helm-charts
    ```

2. Downloading the release tarball and unpacking it:

    ```bash
    curl -sLO https://github.com/nokia-eda/connect-k8s-helm-charts/archive/refs/tags/v1.0.0.tar.gz
    tar zxf v1.0.0.tar.gz 
    ```

### Deploying the Plugin in OpenShift

#### Configuring a Pull Secret for the Controller Image

If the EDA Connect OpenShift Plugin Controller image is hosted in a registry that requires authentication, a Kubernetes Secret needs to be created for OpenShift to be able to pull the image. 

The following command does so for the officially hosted image with a secure read-only token to the registry.

```bash
kubectl create secret docker-registry eda-k8s-image-secret --docker-server=ghcr.io/nokia-eda/eda-connect-k8s-controller --docker-username=nokia-eda-bot --docker-password=<TOKEN> -n eda-connect-k8s-controller
```

#### Setting up the local Helm values

Create a `helm-values.yaml` file with the following content and update the fields as appropriate:

```yaml
--8<-- "docs/connect/resources/openshift-helm-values.yaml"
```

##### Helm Values

The possible Helm Values are:

**`connectpluginname`**
: A name for the plugin. Make sure this is a unique name within your EDA environment.

**`heartbeat`**
: The interval in seconds at which the plugin should send heartbeats. 10-30 are good values, lower can cause extra unnecessary load on the system.

**`namespace`**
: A name of a namespace, where EDA Connect service is deployed

**`skiptlsverify`**
: Can be enabled to disable server TLS certificate verification when connecting to the EDA Kubernetes cluster

**`tlscertificatedata`**
: When certificate validation is enabled, this property can contain the certificate information of the EDA Kubernetes cluster, similar to what a kubeconfig would contain. This is only needed if certificate validation is enabled and if the EDA Kubernetes certificate has not been signed by a trusted authority.

**`tlsenabled`**
: Should always be true to make sure TLS is used to secure the communication with the EDA Kubernetes cluster.

**`connectHost`**
: The URL to reach the EDA Kubernetes cluster API.

**`connectPassword`**
: The long lived token created in the [Create a Service Account Token](#create-a-service-account-token) section.

**`connectUsername`**
: The service account name for the account created in the [Create a Service Account](#create-a-service-account) section.

### Deploying the Plugin

You can now deploy the EDA Connect OpenShift Plugin using its Helm charts with the following command:

```bash
helm install eda-k8s connect-k8s-helm-charts/ \
  -n eda-connect-k8s-controller \
  -f helm-values.yaml \
  --set controller.imagePullSecretName=eda-k8s-image-secret
```

### Deployment Verification

You can verify if the plugin was deployed by checking if the controller is running in the OpenShift Cluster.

```bash
$ kubectl get pods -n connect-k8s-controller
NAME                                            READY   STATUS  RESTARTS AGE
connect-k8s-controller-manager-c8d4875bc-bpzrx  2/2     Running 0        66m
```

On the EDA Kubernetes environment you can verify the plugin has been registered.

```bash
$ kubectl get connectplugins
NAME                                   PROVIDED NAME           PLUGIN TYPE   AGE
470e9af1-b85b-439b-b81a-ab71a7166bb0   k8s-controller-plugin   KUBERNETES    2h
```

## Functionality

### Using the `ConnectNetworkDefinition`

The `ConnectNetworkDefinition` (`CND`) identifies how `NADs` are associated to different `BridgeDomains`. Multiple `NADs` can be associated to the same `BridgeDomain`. A few examples are shown below.

#### Example 1: Multiple `NADs` in One `BridgeDomain`

Following is the sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be residing in a single subnet, when they belong to different master interface. This is an example of OpenShift Managed Mode.

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example1.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example1.yaml"
EOF
```

///

#### Example 2: Multiple `NADs` in One `BridgeDomain` with VLAN Trunking

Following is the sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be residing in a single subnet, and have them use trunk VLAN's:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example2.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example2.yaml"
EOF
```

///

#### Example 3: Using EDA Managed

Following is the sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be part of a single bridgedomain that was pre-created in EDA:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example3.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example3.yaml"
EOF
```

///

## Troubleshooting

### Controller Plugin Not Running

Verify the following items:

* Incorrect Service Account Token configuration.
* Check connectivity between controller pod in Openshift and EDA cluster.
* Ensure the heartbeat interval is a non-negative integer.
* Plugin name must comply with this regex check `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'`. It may only contain alphanumerical characters and '.', '_', '-' (dot, underscore, and, dash) and must start and end with an alphanumerical character.

### Nothing is Created in EDA

Verify the following items:

* Check if the plugin controller is able to access the `NMstate` API and `NetworkAttachmentDefinition` API on the OpenShift cluster.
* Check the plugin can reach EDA cluster correctly.

### The plugin is not configuring the correct state

* Inspect the EDA resources, like `VLAN`, `BridgeDomain` and `ConnectInterface`.
* Check the logs of the plugin pod.
