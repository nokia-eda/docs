# Kubernetes Client Provider

## Overview

The Kubernetes Client Provider publishes metadata about Kubernetes pods into the EDA `networks` client
table.

The provider authenticates to the cluster API, watches Pods, NetworkAttachmentDefinitions, and kubernetes-nmstate
`NodeNetworkState`, and writes `provider-k8s-pod` entries. The Networks Client Provider
then supplies fabric-learned MAC and IP data for the same clients.

/// details | Technical preview
    type: warning

The Kubernetes Client Provider is a technical preview in this release.

///

### Supported Versions

The Kubernetes Client Provider supports the same platforms as the Kubernetes plugin:

* Red Hat OpenShift 4.18
* Red Hat OpenShift 4.20
* Red Hat OpenShift 4.22

The installation of the Kubernetes plugin on the target cluster is mandatory.

## Architecture

The Kubernetes Client Provider is an EDA application. It is separate from the Kubernetes plugin, which runs on the
target cluster instead.

Each `K8sClientProviderInstance` starts one operator pod that connects to one Kubernetes cluster and publishes
client-table rows for the `spec.namespace` namespace.

## Installation

For detailed deployment instructions, see the [Kubernetes Client Provider Installation Guide](installation.md).

## Features

### Inventory

The provider publishes one pod row per network attachment and IP. Each published pod row requires:

* A MAC address
* An IP address
* A `BridgeDomain`

The `BridgeDomain` comes from the Connect Kubernetes plugin after it has synchronized the NetworkAttachmentDefinition.

Pods with more than one attachment will appear as multiple rows.
