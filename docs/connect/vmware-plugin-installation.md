# VMware vSphere Plugin Installation

This guide provides detailed instructions for installing the EDA Connect VMware vSphere plugin.

## Prerequisites

Before installing or deploying the VMware vSphere plugin components, ensure that:

* The Cloud Connect Core application is properly installed in the cluster (see [Cloud Connect Installation](cloud-connect-installation.md))
* You have read-only access credentials to the VMware vCenter environment

## Installation Steps

To deploy the VMware vSphere plugin, complete the following tasks:

1. Deploy the plugin EDA app
2. Deploy the plugin instance

### Step 1: Connect VMware vSphere Plugin App Deployment

The VMware vSphere plugin app is an application in the EDA app ecosystem. It can be easily installed using the EDA Store UI.

#### Installation Using EDA Store UI

1. Navigate to the EDA Store in the EDA UI
2. Locate the VMware vSphere Plugin App
3. Click Install
4. Complete the installation

#### Installation Using Kubernetes API

If you prefer installing the plugin using the Kubernetes API, you can do so by creating the following Workflow resource:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/vmware-appinstall.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/vmware-appinstall.yaml"
EOF
```

///

### Step 2: Connect VMware vSphere Plugin Deployment

#### Create a Secret for VMware Credentials

A prerequisite for creating a `vmwarePluginInstance` resource is a `Secret` resource with username and password fields that contain the account
information for an account that can connect to the VMware vCenter environment and has read-only access to the cluster so that it can monitor the
necessary resources.

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

#### Create the VMware Plugin Instance

As the VMware vSphere plugins are managed through the operator, you can use the EDA UI to create a new `VmwarePluginInstance` resource under the *
*System Administration > Connect > VMware Plugins** menu item.

As an alternative, you can also create the same `VmwarePluginInstance` using the following custom resource example. Make sure to replace the specified
values with their relevant content.

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/vmware-plugin-instance.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/vmware-plugin-instance.yaml"
EOF
```

///

/// warning | Name and External ID constraints
The plugin name and external ID must comply with the regex check of `'([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]'` and can only contain alphanumerical
characters and `.`, `_` and `-`. It must start with an alphanumerical character, and have a length of 63 characters or fewer.
///

## Configuration Parameters

The `VmwarePluginInstance` resource supports the following key parameters:

| **Field**           | **Description**                                                                           | **Required** |
|---------------------|-------------------------------------------------------------------------------------------|--------------|
| `name`              | Name of the plugin instance in EDA.                                                       | Yes          |
| `externalID`        | Unique identifier of the Plugin.                                                          | Yes          |
| `pluginNamespace`   | The namespace in the EDA deployment holding the fabric associated with this plugin.       | Yes          |
| `vcsaHost`          | URL of the VCSA (e.g `vcenter.mydomain.com`). Note that no URI scheme should be provided. | Yes          |
| `authSecretRef`     | Name of the Kubernetes Secret containing VCSA credentials                                 | Yes          |
| `heartbeatInterval` | Interval in seconds for plugin heartbeat to EDA (default: 30s).                           | No           |
| `vcsaTlsVerify`     | Whether to verify the TLS certificate of VCSA (default: true).                            | No           |
| `VCSACertificate`   | PEM encoded certificate for VCSA if self-signed (default: empty).                         | No           |

## Post-Installation Verification

After deploying the plugin, verify that it is running:

```bash
kubectl get pods -n eda-system | grep vmware
```

Check that the plugin has registered with Connect:

```bash
kubectl get connectplugins -n <plugin-namespace>
```

You should see your VMware plugin listed with status information.

## Next Steps

After installation, proceed to:

* Configure distributed Port Groups in vCenter
* Set up Custom Attributes for EDA-managed mode (if required)
* Make sure LLDP is enabled on the distributed vSwitch (at least advertise in Discovery protocol settings)
* Review the [VMware vSphere Plugin documentation](vmware-plugin.md) for usage and operational modes
