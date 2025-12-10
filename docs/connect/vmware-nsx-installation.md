# VMware NSX Plugin Installation

This guide provides detailed instructions for installing the EDA Connect VMware NSX plugin.

## Prerequisites

Before installing or deploying the VMware NSX plugin components, ensure that:

* The Cloud Connect Core application is properly installed in the cluster (see [Cloud Connect Installation](cloud-connect-installation.md))
* VMware vSphere Plugin is deployed for each vCenter managed by NSX (see [VMware vSphere Plugin Installation](vmware-plugin-installation.md))
* You have read-only access credentials to the VMware NSX environment

## Installation Steps

To deploy the VMware NSX plugin, complete the following tasks:

1. Deploy the plugin app
2. Deploy the plugin instance

### Step 1: Connect VMware NSX Plugin App Deployment

The VMware NSX plugin app is an application in the EDA app ecosystem. It can be easily installed using the EDA Store UI.

#### Installation Using EDA Store UI

1. Navigate to the EDA Store in the EDA UI
2. Locate the VMware NSX Plugin App
3. Click Install
4. Complete the installation

#### Installation Using Kubernetes API

If you prefer installing the plugin using the Kubernetes API, you can do so by creating the following Workflow resource:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/nsx-appinstall.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/nsx-appinstall.yaml"
EOF
```

///

### Step 2: Connect VMware NSX Plugin Deployment

#### Create a Secret for NSX Credentials

A prerequisite for creating a `NsxPluginInstance` resource is a `Secret` resource with username and password fields that contain the account
information for an account that can connect to the VMware NSX environment and has read-only access to the cluster so that it can monitor the necessary
resources.

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/vmware-secret.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/vmware-secret.yaml"
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
The secrets used by the EDA plugins must have the `eda.nokia.com/backup: "true"` label.
///

#### Create the NSX Plugin Instance

As the VMware NSX plugins are managed through the operator, you can use the EDA UI to create a new `NsxPluginInstance` resource under the **System
Administration > Connect > NSX Plugins** menu item.

As an alternative, you can also create the same `NsxPluginInstance` using the following custom resource example. Make sure to replace the specified
values with their relevant content.

/// details | vCenterFQDN
    type: warning

The vCenterFQDN field has to correspond to the "FQDN or IP Address" field when creating the compute manager in NSX.
![vCenter FQDN or IP](resources/nsx-vcenter-fqdn.png)

///

/// note
A VMware NSX instance can manage multiple VMware vCenter servers. This is reflected by referencing the vCenters and the corresponding Connect VMware
vCenter plugins in the `NsxPluginInstance`.
///

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/nsx-plugin-instance.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/nsx-plugin-instance.yaml"
EOF
```

///

/// warning | Name and External ID constraints
The plugin name and external ID must comply with the regex check of `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'` and can only contain alphanumerical
characters and `.`, `_` and `-`. It must start with an alphanumerical character, and have a length of 63 characters or fewer.
///

## Post-Installation Verification

After deploying the plugin instance, verify that it is running:

```bash
kubectl get pods -n eda-system | grep nsx
```

Check that the plugin has registered with Connect:

```bash
kubectl get connectplugins -n <plugin-namespace>
```

You should see your NSX plugin listed with status information.

## Configuration Parameters

The `NsxPluginInstance` resource supports the following key parameters:

| Parameter           | Description                                                                                              | Required         |
|---------------------|----------------------------------------------------------------------------------------------------------|------------------|
| `name`              | Unique name for the plugin instance                                                                      | Yes              |
| `namespace`         | EDA namespace containing the fabric                                                                      | Yes              |
| `externalID`        | Unique identifier for the NSX environment                                                                | Yes              |
| `nsxManagementIP`   | FQDN or IP address of the NSX Manager (eg. nsx.example.com). Note that no URI scheme should be provided. | Yes              |
| `authSecretRef`     | Reference to the Kubernetes Secret with credentials                                                      | Yes              |
| `heartbeatInterval` | Interval in seconds for heartbeat updates                                                                | No (default: 30) |
| `nsxTlsVerify`      | Whether to verify the TLS certificate of NSX (default: true).                                            | No               |
| `nsxCertificate`    | PEM encoded certificate for NSX if self-signed (default: empty).                                         | No               |
| `nsxPollInterval`   | Interval in seconds for polling NSX for changes (default: 2).                                            | No (default: 60) |
| `vCenters`          | List of vCenter references with FQDN and plugin names                                                    | Yes              |

## Next Steps

After installation, proceed to:

* Configure VLAN or overlay segments in NSX
* Set up NSX tags for EDA-managed mode (if required)
* Review the [VMware NSX Plugin documentation](vmware-nsx.md) for usage and operational modes

