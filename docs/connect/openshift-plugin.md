# OpenShift Plugin

??? Warning "Known Limitations"
    Cloud Connect can be deployed, including plugins. However, without support for real Hardware SR Linux nodes, the plugins can not connect and configure the fabric as the cloud environments need to be deployed as Bare Metal with real SR Linux nodes.

## Overview

EDA Cloud Connect integrates with OpenShift to provide fabric-level application networks for OpenShift pods and services. The Connect integration leverages the OpenShift Multus CNI solution to support managing the fabric directly from OpenShift and make the fabric dynamically respond to the networking needs of the application.

It provides the following advantages and capabilities:

* Direct integration into the network management workflow of OpenShift
* Use of the common CNIs used by Enterprise applications and CNFs like IPVLAN and SR-IOV
* Automatic provisioning of the fabric based on where the application pods need the connectivity
* Support for advanced workflows

### Supported Versions

* Red Hat OpenShift 4.14

## Prerequisites

Before using the Connect OpenShift Plugin, make sure the following prerequisites are met:

* Ensure Openshift cluster is up and running.
* Ensure [NMState-Operator](https://docs.openshift.com/container-platform/4.14/networking/k8s_nmstate/k8s-nmstate-about-the-k8s-nmstate-operator.html) and Multus are installed on openshift cluster.
* Ensure all the nodes which are connected to SRL leaf nodes have LLDP enabled on each node.
* Ensure EDA cluster is up and running.
* Ensure you have access to EDA cluster's kubeconfig  as the values from that file is required for controller installation.
* Ensure you have access to the controller container image named cr.srlinux.dev/eda/containers/connect-k8s-plugin:24.4.0-a1 on harbor registry.

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

<!-- !!! Note "The `ConnectNetworkDefinition` approach is the only one supported in the Alpha release." -->

## Connect OpenShift Plugin Deployment

### Required EDA `kubeconfig` information

For the plugin to connect to the EDA cluster, it requires an account on the EDA Kubernetes environment. Initially, the easiest approach is to gather the following information from your `kubeconfig` used to connect to the Kubernetes environment:

* `CONNECT_HOST`: Server API URL
* `CONNECT_USERNAME`: User `client-certificate-data`
* `CONNECT_PASSWORD`: User `client-key-data`

!!! Note "The `CONNECT_` keys might change in the future"

This information can typically be found in the `.kube/config` file in your home directory, or in the file where you store the `kubeconfig` file. The file looks similar to the following:

```yaml
--8<-- "docs/connect/resources/eda-kubeconfig.yaml"
```

### Creating a Namespace

Create a new namespace for the Connect OpenShift Plugin, in the OpenShift cluster:

```bash
kubectl create namespace connect-k8s-controller
```

### Create a Credentials Secret

Using the `CONNECT_HOST`, `CONNECT_USERNAME` and `CONNECT_PASSWORD` gathered before, create a new secret in the OpenShift cluster and namespace for use by the plugin:

```bash
kubectl create secret generic connect-k8s-controller-env-secret \
 -n connect-k8s-controller \
 --from-literal=CONNECT_HOST=<server value from eda kubeconfig> \
 --from-literal=CONNECT_USERNAME=<client-certificate-data value from eda kubeconfig> \
 --from-literal=CONNECT_PASSWORD=<client-key-data value from eda kubeconfig>
```

### Updating and Deploying the OpenShift Plugin Manifest

[By clicking here](resources/openshift-plugin-manifest.yaml) you can find a manifest with multiple resources that must be created in the OpenShift cluster to deploy the Connect OpenShift Plugin.

!!! Note "Replacing Values"
    Make sure to search the manifest for the text `###CHANGE-ME###`, you must update values in two locations.

??? Note "Full Manifest"
    === "YAML Resource"
        ```yaml
        --8<-- "docs/connect/resources/openshift-plugin-manifest.yaml"
        ```

    === "`kubectl apply` command"
        ```bash
        kubectl apply -f - <<EOF
        --8<-- "docs/connect/resources/openshift-plugin-manifest.yaml"
        EOF
        ```

This will deploy the plugin controller in the OpenShift cluster.

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

=== "YAML Resource"
    ```yaml
    --8<-- "docs/connect/resources/cnd-example1.yaml"
    ```

=== "`kubectl apply` command"
    ```bash
    kubectl apply -f - <<EOF
    --8<-- "docs/connect/resources/cnd-example1.yaml"
    EOF
    ```

#### Example 2: Multiple `NADs` in One `BridgeDomain` with VLAN Trunking

Following is the sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be residing in a single subnet, and have them use trunk VLAN's:

=== "YAML Resource"
    ```yaml
    --8<-- "docs/connect/resources/cnd-example2.yaml"
    ```

=== "`kubectl apply` command"
    ```bash
    kubectl apply -f - <<EOF
    --8<-- "docs/connect/resources/cnd-example2.yaml"
    EOF
    ```

#### Example 3: Using EDA Managed

Following is the sample configuration of the CND usage to be able to have multiple `NetworkAttachmentDefinitions` be part of a single bridgedomain that was pre-created in EDA:

=== "YAML Resource"
    ```yaml
    --8<-- "docs/connect/resources/cnd-example3.yaml"
    ```

=== "`kubectl apply` command"
    ```bash
    kubectl apply -f - <<EOF
    --8<-- "docs/connect/resources/cnd-example3.yaml"
    EOF
    ```

## Troubleshooting

### Controller Plugin Not Running

Verify the following items:

* Incorrect usage of EDA kubeconfig file which is used to provide CONNECT credentials and CONNECT_HOST information.
* Check connectivity between controller pod in Openshift and EDA cluster.
* Ensure the heartbeat interval is a non-negative integer that is set in the Configmap connect-k8s-controller-env-config  in the namespace connect-k8s-controller
* Plugin name must comply with this regex check `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'`. It may only contain alphanumerical characters and '.', '_', '-' (dot, underscore, and, dash) and must start and end whit alphanumerical character.

### Nothing is Created in EDA

Verify the following items:

* Check if the plugin controller is able to access the `NMstate` API and `NetworkAttachmentDefintion` API on the OpenShift cluster.
* Check the plugin can reach EDA cluster correctly.

### The plugin is not configuring the correct state

<!-- !!! Warning "Check the limitations of Connect in the Alpha at the top of this page" -->

* Inspect the EDA resources, like `VLAN`, `BridgeDomain` and `ConnectInterface`.
* Check the logs of the plugin pod.
