# OpenStack Client Provider Installation

This guide provides detailed instructions for installing the OpenStack Client Provider.

## Prerequisites

Before you deploy the OpenStack Client Provider, ensure that:

* The Services application is installed
* The [Cloud Connect Core](../../cloud-connect-installation.md) and [OpenStack plugin](../installation/index.md) are
  installed when you want the provider to correlate Connect-managed networks
* You have OpenStack credentials with the Nova and Neutron visibility that you need

## Installation Steps

To deploy the OpenStack Client Provider, complete the following tasks:

1. Deploy the OpenStack Client Provider app
2. Create a Secret for OpenStack credentials
3. Create an `OpenStackClientProviderInstance`

### Step 1: OpenStack Client Provider App Deployment

The OpenStack Client Provider is an application in the EDA app ecosystem. You can install it from the EDA Store UI.

#### Installation Using EDA Store UI

1. Navigate to the EDA Store in the EDA UI
2. Locate the OpenStack Client Provider app
3. Click Install
4. Complete the installation

#### Installation Using Kubernetes API

If you prefer installing the app using the Kubernetes API, you can do so by creating the following Workflow resource:

/// tab | YAML Resource

```yaml
--8<-- "docs/apps/connect/resources/openstack-client-provider-appinstall.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/apps/connect/resources/openstack-client-provider-appinstall.yaml"
EOF
```

///

### Step 2: Create a Secret for OpenStack Credentials

Create a Kubernetes `Secret` in the `eda-system` namespace.

/// tab | YAML Resource

```yaml
--8<-- "docs/apps/connect/resources/openstack-client-provider-secret.yaml"
```

///
/// tab | `kubectl apply` command

```bash
echo -n myUsernameOrPassword | base64
kubectl apply -f - <<EOF
--8<-- "docs/apps/connect/resources/openstack-client-provider-secret.yaml"
EOF
```

///

/// details | Base64 encoding

Use the following command to base64 encode your username and password:

```bash
echo -n myUsernameOrPassword | base64
```

///

/// warning | mandatory label
The secrets used by EDA must have the `eda.nokia.com/backup: "true"` label.
///

The Secret can use `username` / `password` keys, or the OpenStack `OS_USERNAME` / `OS_PASSWORD` keys. Alternatively,
application credentials use `OS_APPLICATION_CREDENTIAL_*` keys, or the equivalent lowercase names. Additionally, domain
and project scope can come from the Secret or from fields on the instance. For more information about OpenStack
authentication see
the [upstream documentation](https://docs.openstack.org/python-openstackclient/latest/cli/authentication.html).

### Step 3: Create the OpenStack Client Provider Instance

Create the `OpenStackClientProviderInstance` in the EDA UI under
**System Administration > Client Providers > OpenStack Client Providers**.

You can also create the same resource using the Kubernetes API. Replace the example values with values for your
deployment.

/// tab | YAML Resource

```yaml
--8<-- "docs/apps/connect/resources/openstack-client-provider-instance.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/apps/connect/resources/openstack-client-provider-instance.yaml"
EOF
```

///

/// details | Namespaces
    type: note

Create the `OpenStackClientProviderInstance` in `eda-system`. Set `spec.namespace` to the namespace that holds the
fabric where the OpenStack resources are created on.

///


## Configuration Parameters

The `OpenStackClientProviderInstance` resource supports the following fields:

| **Field**                              | **Description**                                                                                               | **Required** |
|----------------------------------------|---------------------------------------------------------------------------------------------------------------|--------------|
| `name`                                 | Name of the instance in EDA.                                                                                  | Yes          |
| `namespace`                            | Namespace that holds the fabric where OpenStack resources are scheduled on.                                   | Yes          |
| `authURL`                              | Keystone authentication URL.                                                                                  | Yes          |
| `authSecretRef`                        | Name of the Kubernetes Secret in `spec.namespace` that contains OpenStack credentials.                        | Yes          |
| `regionName`                           | OpenStack region name.                                                                                        | Yes          |
| `sync.mode`                            | Sync mode. The current release supports `Polling` only.                                                       | Yes          |
| `sync.polling.fullSyncIntervalSeconds` | Interval in seconds for a full inventory poll.                                                                | Yes          |
| `identityInterface`                    | Keystone catalog interface: `public` (default), `internal`, or `admin`.                                       | No           |
| `domainName`                           | Domain name that contains the user.                                                                           | No           |
| `domainID`                             | Domain ID that contains the user.                                                                             | No           |
| `projectName`                          | Project-level authentication scope (name).                                                                    | No           |
| `projectID`                            | Project-level authentication scope (ID).                                                                      | No           |

## Post-Installation Verification

After you create the instance, verify that the operator pod is running:

```bash
kubectl get pods -n eda-system | grep oscp
```

Check the instance status:

```bash
kubectl get openstackclientproviderinstances -n eda-system
```

The status phase and message show whether the last poll reached Keystone, Nova, and Neutron.

## Next Steps

After installation, proceed to:

* Check the `.namespace.clienttables.networks` client table for OpenStack entries.
