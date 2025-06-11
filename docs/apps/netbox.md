# NetBox

| <nbsp> {: .hide-th } |                                                                                        |
| -------------------- | -------------------------------------------------------------------------------------- |
| **Description**      | The EDA NetBox app integrates with NetBox to automate IP allocations using custom CRs. |
| **Supported OS**     | SR Linux, SR OS                                                                        |
| **Catalog**          | [nokia-eda/catalog][catalog] / [manifest][manifest]                                    |
| **Source Code**      | <small>coming soon</small>                                                             |

[catalog]: https://github.com/nokia-eda/catalog
[manifest]: https://github.com/nokia-eda/catalog/blob/main/vendors/nokia/apps/netbox/manifest.yaml

## Overview

The NetBox app enables users to integrate/synchronize various resources between NetBox and EDA by providing the following resource types:

* **Instance**: Defines the target NetBox instance to interact with.
* **Allocation**: Specifies the type of EDA allocation to create based on NetBox `Prefixes`.

> **Note**: Both CRs **must** be created in the same namespace (excluding `eda-system`).

---

## Prerequisites

### NetBox Version Compatibility

This release supports **NetBox v4.2.5**. Version 4.2.6 introduced a change that prevents overlapping IP addresses, which the EDA app currently relies on when the same IP exists in more than one topology/fabric.

### NetBox Configuration

To enable NetBox to send updates to the EDA app:

1. **Create a Webhook in NetBox**

   * **Name**: Any meaningful identifier
   * **URL**: `https://${EDA_ADDR}:${EDA_PORT}/core/httpproxy/v1/netbox/webhook/${INSTANCE_NAMESPACE}/${INSTANCE_NAME}`
   * **Method**: `POST`
   * **Secret**: A signature secret string (store it later in a Kubernetes Secret)
   * Leave all other settings as default.

2. **Create an Event Rule**

   * **Name**: Choose a relevant name
   * **Objects**: Include **IPAM IPAddresses** and **IPAM Prefixes**
   * **Enabled**: Yes
   * **Event Types**:

     * Object Created
     * Object Updated
     * Object Deleted
   * **Action**:

     * **Type**: Webhook
     * **Webhook**: Select the one created above

3. **Generate an API Token**

   Create a NetBox API token for the user that the app will use. The token **must** have permission to `create`, `update`, and `delete` **IPAddresses** and **Prefixes** (and optionally Tags/CustomFields if you use them).

4. **Configure Global VRF Setting**

   ```bash
   ENFORCE_GLOBAL_UNIQUE=false
   ```

   As per the [NetBox documentation](https://netboxlabs.com/docs/netbox/en/stable/models/ipam/vrf/), this is required when working with overlapping prefixes across VRFs.

### Create Kubernetes Secrets

After you have the webhook secret string **and** the API token, create the following Secrets in the same namespace where the EDA NetBox app will run (example: `eda`). Replace the base64‑encoded values with your own data:

Secret for the webhook:

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/webhook-signature-secret.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/netbox/webhook-signature-secret.yaml"
EOF
```

///

Secret for the api-token:


/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/api-token-secret.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/netbox/api-token-secret.yaml"
EOF
```

///


---

## EDA Configuration

### Installation

Install the NetBox app from the [EDA Store](app-store.md) or with `kubectl`:

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

### Instance Custom Resource

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

> The `apiToken` field references the **netbox-api-token** Secret created above.

After creation, check the status of the Instance CR to verify successful connection.

### Allocation Custom Resource

Specifies which allocations to create based on NetBox tags:

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

| Type           | Resource Created                               | Typical Use                     |
| -------------- | ---------------------------------------------- | ------------------------------- |
| `ip-address`   | `ipallocationpools.core.eda.nokia.com`         | IP Addresses → **system IPs**   |
| `ip-in-subnet` | `ipinsubnetallocationpools.core.eda.nokia.com` | IP Addresses + Masks → **mgmt** |
| `subnet`       | `subnetallocationpools.core.eda.nokia.com`     | Subnets → **ISL links**         |
