# Cloud Connect Core Installation

This guide provides detailed instructions for installing the EDA Cloud Connect Core application.

## Prerequisites

* EDA cluster is up and running
* Access to the EDA Store UI or Kubernetes API
* All Connect Core dependencies are satisfied (automatically resolved when installing through the UI)

## Installation Using EDA Store UI

Cloud Connect is an application in the EDA app ecosystem. The easiest way to install it is through the EDA Store UI:

1. Navigate to the EDA Store in the EDA UI
2. Locate the Cloud Connect Core application
3. Click Install
4. Configure the installation options (see [Plugin Configuration Options](#plugin-configuration-options))
5. Complete the installation

Dependencies are automatically resolved when installing through the UI.

## Installation Using Kubernetes API

If you prefer installing the Connect Core using the Kubernetes API, you can do so by creating the following Workflow resource:

/// details | Connect Core dependencies

When installing through the UI, dependencies are automatically resolved; this is not the case through the API. Make sure all dependencies of the
Connect Core app are installed before executing the below kubectl command.

When the dependencies are not satisfied, an error like the following will be added to the status of the AppInstaller object:

```app requirements validation failed: connect.eda.nokia.com requires interfaces.eda.nokia.com, but interfaces.eda.nokia.com is not present```

///

/// tab | YAML Resource

```yaml
--8<-- "docs/connect/resources/connect-appinstall.yaml"
```

///
/// tab | `kubectl apply` command"

```bash
kubectl apply -f - <<EOF
--8<-- "docs/connect/resources/connect-appinstall.yaml"
EOF
```

///

## Plugin Configuration Options

When installing Cloud Connect via the EDA UI, users are prompted to configure the application using the following options. These settings control
resource limits and behavior of the Connect controllers:

| Configuration Option                                                         | Description                                                                                        | Default Value |
|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|---------------|
| **Interface Controller GraceTimer** (`interfaceControllerGraceTimer`)        | The grace period (in seconds) used by the Interface Controller before acting on missing LLDP data. | `10`          |
| **Interface Controller Pod CPU Limit** (`interfaceControllerCpuLimit`)       | CPU limit for the connect-interface-controller pod.                                                | `1`           |
| **Interface Controller Pod Memory Limit** (`interfaceControllerMemoryLimit`) | Memory limit for the connect-interface-controller pod.                                             | `2Gi`         |
| **Plugin Controller Pod CPU Limit** (`pluginControllerCpuLimit`)             | CPU limit for the connect-plugin-controller pod.                                                   | `500m`        |
| **Plugin Controller Pod Memory Limit** (`pluginControllerMemoryLimit`)       | Memory limit for the connect-plugin-controller pod.                                                | `128Mi`       |

These options can be adjusted during installation to meet specific performance or resource requirements.

/// details | Settings are an advanced use case
    type: warning

These settings are intended for advanced users. Misconfiguration can lead to system instability or failure. Proceed with caution and ensure changes
are validated in a test environment before applying them to production.
///

## Next Steps

After installing the Cloud Connect Core, you can proceed to install and configure one or more of the cloud platform plugins.
