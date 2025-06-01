# NetBox

| <nbsp> {: .hide-th } |                                                                                        |
| -------------------- | -------------------------------------------------------------------------------------- |
| **Description**      | The EDA NetBox app integrates with NetBox to automate IP allocations using custom CRs. |
| **Supported OS**     | SR Linux, SR OS                                                                        |
| **Catalog**          | [nokia-eda/catalog][catalog] / [manifest][manifest]                                                          |
| **Source Code**      | <small>coming soon</small>                                                             |

[catalog]: https://github.com/nokia-eda/catalog
[manifest]: https://github.com/nokia-eda/catalog/blob/main/vendors/nokia/apps/netbox/manifest.yaml

## Overview

The NetBox app enables users to integrate/synchronize various resources between NetBox and EDA by providing the following resource types:

* **Instance**: Defines the target NetBox instance to interact with.
* **Allocation**: Specifies the type of EDA allocation to create based on Netbox `Prefixes`.

> **Note**: Both CRs **must** be created in the same namespace (excluding `eda-system`).

## NetBox Configuration

To enable NetBox to send updates to the EDA app:

### Create a Webhook in NetBox

* **Name**: Any meaningful identifier
* **URL**:
  `https://${EDA_ADDR}:${EDA_PORT}/core/httpproxy/v1/netbox/webhook/${INSTANCE_NAMESPACE}/${INSTANCE_NAME}`
* **Method**: `POST`
* **Secret**: Choose a signature secret string. This will be configured in the `Instance` CR later on.

Leave all other settings as default.

### Create an Event Rule

* **Name**: Choose a relevant name
* **Objects**: Include **IPAM IPAddresses** and **IPAM Prefixes**
* **Enabled**: Yes
* **Event Types**:

    * Object Created
    * Object Updated
    * Object Deleted

* **Action**:

    * **Type**: Webhook
    * **Webhook**: Select the one created above

### Generate a NetBox API Token

The token should have at a minimum the permissions to `create`, `update`, and `delete` the following resources:

* `IPAM.IPAddresses`
* `IPAM.Prefixes`
* `Customizations.Tags`
* `Customizations.CustomFields`

### Configure Global VRF Setting

Set the following environment variable in NetBox to allow duplicate prefixes across VRFs:

```bash
ENFORCE_GLOBAL_UNIQUE=false
```

As per [NetBox documentation](https://netboxlabs.com/docs/netbox/en/stable/models/ipam/vrf/), this is required if you're working with overlapping prefixes.

## EDA Configuration

### Installation

Netbox app can be installed using [EDA Store](app-store.md) or by running the app-installer workflow with `kubectl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/netbox/install.yml"
EOF
```

///

### Instance Custom Resource

Defines connection details to the NetBox instance:

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/instance.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/netbox/instance.yml"
EOF
```

///

After creation, check the status of the Instance CR to verify successful connection.

---

### Allocation Custom Resource

Defines what allocation to create, based on NetBox tags:

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/allocation.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/netbox/allocation.yml"
EOF
```

///

| `type`         | Resource Created                               |
| -------------- | ---------------------------------------------- |
| `ip-address`   | `ipallocationpools.core.eda.nokia.com`         |
| `ip-in-subnet` | `ipinsubnetallocationpools.core.eda.nokia.com` |
| `subnet`       | `subnetallocationpools.core.eda.nokia.com`     |
