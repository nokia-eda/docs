# OpenShift Plugin

## Overview

EDA Cloud Connect integrates with OpenShift to provide fabric-level application networks for OpenShift pods and services. The Connect integration leverages the OpenShift Multus CNI solution to support managing the fabric directly from OpenShift and make the fabric dynamically respond to the networking needs of the application.

It provides the following advantages and capabilities:

* Direct integration into the network management workflow of OpenShift
* Use of the common CNIs used by Enterprise applications and CNFs like IPVLAN and SR-IOV
* Automatic provisioning of the fabric based on where the application pods need the connectivity
* Support for advanced workflows

### Supported Versions

* Red Hat OpenShift 4.16
* Red Hat OpenShift 4.18

## Prerequisites

Before using the Connect OpenShift Plugin, make sure the following prerequisites are met:

* Ensure Openshift cluster is up and running.
* Ensure [NMState-Operator](https://docs.openshift.com/container-platform/4.16/networking/networking_operators/k8s-nmstate-about-the-k8s-nmstate-operator.html) and Multus are installed on openshift cluster.
* Ensure all the nodes which are connected to SRL leaf nodes have LLDP enabled on each node.
* Ensure EDA cluster is up and running.
* Ensure EDA Cloud Connect App is installed.
* Ensure you have access to the controller container image named `ghcr.io/nokia-eda/eda-connect-k8s-controller:3.0.0`.
* NMState Operator is configured to listen for LLDP TLVs. Create the following resource in your OpenShift cluster and make sure to include all interfaces in the list that are connected to leaf switches managed by EDA:

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

## Architecture

The OpenShift Plugin consists of a controller which will monitor the following resources in OpenShift:

* The physical NIC configuration and correlation to `NetworkAttachmentDefinitions` through the NMState Operator.
* `NetworkAttachmentDefinitions` and their master interfaces.
* `ConnectNetworkDefinitions` for the configuration of Layer 2 and Layer 3 services configuration.

### Operational Modes

The OpenShift Plugin supports three ways of associating `NetworkAttachmentDefinitions` to EDA `BridgeDomains`, called Operational modes:

*Transparent association*
: This association does not require any information from EDA in OpenShift. For every unique master interface defined in `NADs` in the OpenShift Cluster, the plugin will create a unique `BridgeDomain`. This association only supports OpenShift Managed Mode.

*Annotation based association*
: In this association, annotations are added to the `NAD` that reference an existing EDA `BridgeDomain`. This association only supports EDA Managed Mode.

*`ConnectNetworkDefinition` association*
: The `ConnectNetworkDefinition` is a Custom Resource Definition that gets added to the OpenShift Cluster and is used to describe the relationship between the different services and `NetworkAttachmentDefinitions`, and how the services relate to each other. This association supports both OpenShift Managed and EDA Managed Modes.

### Supported Features

The following are some of the supported OpenShift features:

* CMS-managed integration mode
* EDA-managed integration mode
* Network Attachment Definition Transparent operational mode (CMS-managed only)
* Connect Network Definition operational mode (CMS-managed and EDA Managed)
* Network Attachment Definition Annotation operational mode (EDA-managed only)
* Optimally configure subinterfaces to minimize configuration and security footprint of network services
* LAG/LACP interfaces
* VLAN Trunking
* Audits

The following are supported CNIs:

* MACVLAN
* IPVLAN
* SRIOV
* Dynamic SRIOV

## EDA Connect OpenShift Plugin Deployment

### EDA Kubernetes Preparation

#### Create a Service Account

The EDA Connect OpenShift Plugin uses a `ServiceAccount` in the EDA Kubernetes cluster to create the necessary resources in the EDA cluster for the integration to properly work.

To create a service account in the EDA Kubernetes cluster, the following resource can be used.

//// details | Service Account and Cluster Role Binding manifest
    type: note
This service account must be created in the `eda-system` namespace.

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

After creating the Service Account Token, you can retrieve the actual token itself using the following command from `eda-system` namespace as defined in the above created service account.
This token is what will need to be provided to the plugin during deployment.

```bash
kubectl get secrets/k8s-controller-plugin -n eda-system --template={{.data.token}} | base64 --decode
```

### Fetching the EDA Connect OpenShift plugin Helm charts

There are two ways to get the Helm charts to deploy the EDA Connect OpenShift plugin:

1. Using the EDA Playground, which you used to install EDA, you can clone the github repository:

    ```bash
    make download-connect-k8s-helm-charts
    ```

2. Downloading the release tarball and unpacking it:

    ```bash
    curl -sLO https://github.com/nokia-eda/connect-k8s-helm-charts/archive/refs/tags/3.0.0.tar.gz
    tar zxf 3.0.0.tar.gz 
    ```

### Deploying the Plugin in OpenShift

#### Create a Namespace for the OpenShift Plugin

The OpenShift Plugin uses its own namespace to separate it from other resources in the OpenShift cluster. You can create the correct namespace using the following command:

```bash
kubectl create namespace eda-connect-k8s-controller
```

#### Configuring a Pull Secret for the Controller Image

If the EDA Connect OpenShift Plugin Controller image is hosted in a registry that requires authentication, a Kubernetes Secret needs to be created for OpenShift to be able to pull the image.

The following command does so for the officially hosted image with a secure read-only token to the registry.

```bash
export PULL_TOKEN=<PULL_TOKEN>
kubectl create secret docker-registry eda-k8s-image-secret \
  --docker-server=ghcr.io/nokia-eda/eda-connect-k8s-controller \
  --docker-username=nokia-eda-bot \
  --docker-password=${PULL_TOKEN} \
  -n eda-connect-k8s-controller
```

/// details | Getting the pull token
    type: note
The easiest way to get the token/password for the pull secret, is to look at your EDA deployment and look for the `appstore-eda-apps-registry-image-pull` secret. By grabbing the content of that secret and using `base64` to decode the `dockerconfigjson`, you can find the password in the resulting json.

Example to do so in one line (make sure to have the KUBECONFIG for the EDA cluster loaded, not the OpenShift config):

```bash
kubectl get secret appstore-eda-apps-registry-image-pull -n eda-system -o json | jq -r '.data.".dockerconfigjson"' | base64 -d | jq -r '.auths."ghcr.io".password'
```

///

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
: A name of a namespace. This will be a namespace in EDA containing the fabric and resources, this will different from the eda-system namespace.

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

On the EDA Kubernetes environment you can verify the plugin has been registered on EDA in the namespace referred in `openshift-helm-values.yaml`.
The following command assumes that namespace value set to be `eda`

```bash
$ kubectl get connectplugins -n eda
NAME                                   PROVIDED NAME           PLUGIN TYPE   AGE
470e9af1-b85b-439b-b81a-ab71a7166bb0   k8s-controller-plugin   KUBERNETES    2h
```

## Using Operational Modes

The OpenShift Connect plugin operates in the following operational modes:

* Transparent operational mode
* Connect Network Definition operational mode
* NAD annotation operational mode

### Using the Transparent Operational Mode

To use the Transparent operational mode, create network attachment definitions (NADs) in OpenShift without any EDA Connect annotations or any reference to the NAD in a Connect Network Definition (CND).

By doing so, the plugin creates a new EDA `BridgeDomain` for each NAD with a unique master (+VLAN) interface. If a NAD is created for which a NAD with the same master interface and VLAN already exists, it is associated with the existing `BridgeDomain`.

When you remove the NAD, the EDA bridge domain is also removed.

### Using the Connect Network Definition Operational Mode

Connect Network Definition (CND) is a custom resource definition (CRD) that is added to the OpenShift cluster on deployment of the plugin.

A CND contains a design of all the network services and configuration an application may need. It can be used to define EDA Routers and EDA BridgeDomain resources. For each BridgeDomain, it is possible to associate one or more NADs with it. By doing so, the plugin knows how to connect applications into different network services.

In some deployment use cases `preProvisionHostGroupSelector` can be used to pre-provision connect interface for a NAD interface on a set of selected hosts, regardless of whether they are consumed by any pod.

/// details | Limitations of `preProvisionHostGroupSelector`
    type: warning
Please note that this attribute is only applicable to `IPVLAN` and `MACVLAN` type of `NetworkAttachmentDefinitions`
///

You can use the CMS-managed integration mode, the EDA-managed integration mode, or a combination of both.

Multiple CNDs can exist, for instance one per application.

#### Example 1: Multiple `NADs` in One `BridgeDomain`

The following is a sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be residing in a single subnet, when they belong to different master interface. This is an example of OpenShift Managed Mode.

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

The following is a sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be residing in a single subnet, and have them use trunk VLAN's:

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

#### Example 3: Using EDA-Managed

The following is a sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be part of a single `BridgeDomain` that was pre-created in EDA:

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

#### Example 4: Using preProvisionHostGroupSelector to pre-provision connect interface with the label selector

To be able to consume this attribute in CND, ensure that the openshift/k8s nodes are labelled correctly and the same value is used in the CND.

Example of the labelling a node is as following:

```shell

kubectl label nodes node-1 connect.eda.nokia.com/hostGroup=net-group-1
kubectl label nodes node-2 connect.eda.nokia.com/hostGroup=net-group-2
```

The following is a sample configuration of the CND usage to be able to pre-configure connect interface

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example4.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example4.yaml"
EOF
```

///

#### Example 5: Multiple `NADs` in One `BridgeDomain` associated to a `Router`

The following is a sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be residing in a single subnet, associated with a router:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/cnd-example5.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/cnd-example5.yaml"
EOF
```

///

### Using the NAD Annotation Operational Mode

The NAD Annotation operational mode only works for the EDA-managed integration mode because it relies on an annotation on the NAD that identifies the pre-existing EDA BridgeDomain resource to which the NAD needs to be associated with.

To use this operational mode, when creating or updating a NAD, add the following annotation to it:

```yaml
connect.eda.nokia.com/bridgedomain: <eda-bridge-domain-name> 
```

In case of VLAN trunking, a more complex annotation can be used, for example:

```yaml
connect.eda.nokia.com/bridgedomain: <eda-bridge-domain-name>:<vlan-id>, <eda-bridge-domain-name-2>:<vlan-id> 
```

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
