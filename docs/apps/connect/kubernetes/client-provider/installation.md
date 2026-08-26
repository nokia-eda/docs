# Kubernetes Client Provider Installation

This guide provides detailed instructions for installing the Kubernetes Client Provider.

## Prerequisites

Before you deploy the Kubernetes Client Provider, ensure that:

* The Services application is installed
* The [Cloud Connect Core](../../cloud-connect-installation.md) and [Kubernetes plugin](../installation/index.md) are
  installed on the target cluster
* kubernetes-nmstate is installed on the target cluster
* You have a token that can read pods, nodes, NetworkAttachmentDefinitions, and NMState `NodeNetworkState`

## Installation Steps

To deploy the Kubernetes Client Provider, complete the following tasks:

1. Deploy the Kubernetes Client Provider app
2. Create a Secret for the cluster token
3. Create a `K8sClientProviderInstance`

### Step 1: Kubernetes Client Provider App Deployment

The Kubernetes Client Provider is an application in the EDA app ecosystem. You can install it from the EDA Store UI.

#### Installation Using EDA Store UI

1. Navigate to the EDA Store in the EDA UI
2. Locate the K8s Client Provider app
3. Click Install
4. Complete the installation

#### Installation Using Kubernetes API

If you prefer installing the app using the Kubernetes API, you can do so by creating the following Workflow resource:

/// tab | YAML Resource

```yaml
--8<-- "docs/apps/connect/resources/k8s-client-provider-appinstall.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/apps/connect/resources/k8s-client-provider-appinstall.yaml"
EOF
```

///

### Step 2: Create a Secret for the Cluster Token

Create a Kubernetes `Secret` in the `eda-system` namespace.

/// tab | YAML Resource

```yaml
--8<-- "docs/apps/connect/resources/k8s-client-provider-secret.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/apps/connect/resources/k8s-client-provider-secret.yaml"
EOF
```

///

/// warning | mandatory label
The secrets used by EDA must have the `eda.nokia.com/backup: "true"` label.
///

### Step 3: Create the Kubernetes Client Provider Instance

Create the `K8sClientProviderInstance` in the EDA UI under
**System Administration > Client Providers > K8s Client Providers**.

You can also create the same resource using the Kubernetes API. Replace the example values with values for your
deployment.

/// tab | YAML Resource

```yaml
--8<-- "docs/apps/connect/resources/k8s-client-provider-instance.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/apps/connect/resources/k8s-client-provider-instance.yaml"
EOF
```

///

/// details | Namespaces
    type: note

Create the `K8sClientProviderInstance` in `eda-system`. Set `spec.namespace` to the namespace that holds the fabric
where the Kubernetes resources are created.

///

/// details | TLS certificate
    type: note

When TLS is enabled and skip verify is `false`, you can set `spec.k8sClusterTLSCertificate` to the CA certificate of the
target API server if it is self-signed.

///

## Configuration Parameters

The `K8sClientProviderInstance` resource supports the following fields:

| **Field**                   | **Description**                                                                 | **Required** |
|-----------------------------|---------------------------------------------------------------------------------|--------------|
| `name`                      | Name of the instance in EDA.                                                    | Yes          |
| `k8sClusterURI`             | Kubernetes API URL, including the scheme and optional port.                     | Yes          |
| `authSecretRef`             | Name of the Kubernetes Secret in `eda-system` that contains the `usertoken`.    | Yes          |
| `k8sClusterTLSEnabled`      | Enables TLS to the cluster API. Default is `true`.                              | Yes          |
| `k8sClusterSkipTLSVerify`   | Skips verification of the API server certificate. Default is `false`.           | Yes          |
| `namespace`                 | Namespace that holds the fabric where Kubernetes resources are scheduled.       | Yes          |
| `k8sClusterTLSCertificate`  | CA certificate used to verify the API server.                                   | No           |

## Post-Installation Verification

After you create the instance, verify that the operator pod is running:

```bash
kubectl get pods -n eda-system | grep k8s-client-provider
```

Check the instance status:

```bash
kubectl get k8sclientproviderinstances -n eda-system
```

## Next Steps

After installation, proceed to:

* Check the `.namespace.clienttables.networks` client table for Kubernetes entries.
