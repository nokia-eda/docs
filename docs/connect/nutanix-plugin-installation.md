# Nutanix Prism Central Plugin Installation

//// warning | Technical Preview

The Nutanix Prism Central Plugin is currently only available as beta version for technical preview purposes. It can be used for demo, POC or lab
purposes.

The following features are **not** included in the technical preview:

* SR-IOV support
* NIC Offloading
* Audit
* Alarms
* Heartbeats

////

This guide provides detailed instructions for installing the EDA Connect Nutanix Prism Central plugin.

## Prerequisites

Before installing or deploying the Nutanix plugin components, ensure that:

* The Cloud Connect Core application is properly installed in the cluster (see [Cloud Connect Installation](cloud-connect-installation.md))
* Nutanix Prism Central is installed and accessible
* You have read-only access credentials to Nutanix Prism Central
* LLDP is enabled on all Nutanix AHV hypervisors
* Downlink Interfaces in EDA are created

## Installation Steps

To deploy the Nutanix Prism Central plugin, complete the following tasks:

1. Deploy the plugin EDA app
2. Deploy the plugin instance

### Step 1: Nutanix Prism Central Plugin App Deployment

The Nutanix plugin app is an application in the EDA app ecosystem. It can be easily installed using the EDA Store UI.

#### Installation Using EDA Store UI

1. Navigate to the EDA Store in the EDA UI
2. Locate the Nutanix Prism Central Plugin App
3. Click Install
4. Complete the installation

#### Installation Using Kubernetes API

If you prefer installing the plugin using the Kubernetes API, you can do so by creating the following Workflow resource:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/nutanix-appinstall.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/nutanix-appinstall.yaml"
EOF
```

///

### Step 2: Nutanix Prism Central Plugin Deployment

#### Create a Secret for Prism Central Credentials

Before creating a `NutanixPluginInstance`, create a Kubernetes `Secret` with the Prism Central credentials:

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/nutanix-secret.yaml"
```

///
/// tab | `kubectl apply` command

```bash
echo -n myUsernameOrPassword | base64
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/nutanix-secret.yaml"
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


#### Create the Nutanix Plugin Instance

As the Nutanix plugins are managed through the operator, you can use the EDA UI to create a new `NutanixPluginInstance` resource under the **System Administration > Connect > Nutanix Plugins** menu item.

As an alternative, you can also create the same `NutanixPluginInstance` using the following custom resource example. Make sure to replace the specified values with their relevant content.

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/nutanix-plugin-instance.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/nutanix-plugin-instance.yaml"
EOF
```


///

## Configuration Parameters

The `NutanixPluginInstance` resource supports the following fields:

| **Field**                 | **Description**                                                                     | **Required** |
|---------------------------|-------------------------------------------------------------------------------------|--------------|
| `name`                    | Name of the plugin instance in EDA.                                                 | Yes          |
| `pluginNamespace`         | The namespace in the EDA deployment holding the fabric associated with this plugin. | Yes          |
| `prismCentralHost`        | URL of the Prism Central instance (e.g `https://prismcentral.mydomain.com:9440`).   | Yes          |
| `authSecretRef`           | Name of the Kubernetes Secret containing Prism Central credentials                  | Yes          |
| `heartbeatInterval`       | Interval in seconds for plugin heartbeat to EDA (default: 30s).                     | No           |
| `prismCentralTlsVerify`   | Whether to verify the TLS certificate of Prism Central (default: true).             | No           |
| `prismCentralCertificate` | PEM encoded certificate for Prism Central if self-signed (default: empty).          | No           |

## Post-Installation Verification

After deploying the plugin instance, verify that it is running:

```bash
kubectl get pods -n eda-system | grep nutanix
```

Check that the plugin has registered with Connect:

```bash
kubectl get connectplugins -n <plugin-namespace>
```

You should see your Nutanix plugin listed with status information.

Verify that the `connect.eda.nokia.com` category has been created in Prism Central with the standard values (`EDA Managed` and `EDA Ignored`).

## Next Steps

After installation, proceed to:

* Configure VLAN subnets in Prism Central
* Set up categories for EDA-managed mode (if required)
* Review the [Nutanix Prism Central Plugin documentation](nutanix-plugin.md) for usage and operational modes

