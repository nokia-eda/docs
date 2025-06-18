# NetBox

| <nbsp> {: .hide-th } |                                                                                        |
| -------------------- | -------------------------------------------------------------------------------------- |
| **Description**      | The EDA NetBox app integrates with NetBox to synchronize EDA resources with NetBox     |
| **Supported OS**     | N/A                                                                                    |
| **Catalog**          | [EDA built in apps][manifest]                                                          |
| **Source Code**      | <small>coming soon</small>                                                             |

[manifest]: https://github.com/nokia-eda/catalog/blob/main/vendors/nokia/apps/netbox/manifest.yaml

## Overview

The NetBox app enables users to integrate/synchronize various resources between NetBox and EDA by providing the following resource types:

* **Instance**: Defines the target NetBox instance to interact with.
* **Allocation**: Specifies the type of EDA allocation to create based on the NetBox's `Prefixes`.

/// admonition | Corresponding Instance and Allocation resources **must** be created in the same (non-`eda-system`) namespace.
    type: subtle-note
///

EDA continues to use its own [allocation pools](../user-guide/allocation-pools.md) for IP addresses, indices and subnets, but the NetBox app will dynamically create the allocation pools based on the NetBox's `IPAM > Prefixes` objects and post the allocated objects back to NetBox.

This mode of operation allows the users to leverage NetBox's IPAM features and dynamically create the allocation pools in EDA. Check out the [end-to-end example](#example) for more details.

## Supported objects

In the current version of the NetBox app EDA's allocation pools are created based on the NetBox Prefix objects. Depending on the Prefix's Status mode, the allocation pools of certain type can be created.

| Prefix Status | Suitable EDA Allocation Pools                                                      | Example usage in EDA       |
| ------------- | ---------------------------------------------------------------------------------- | -------------------------- |
| Active        | IP Address (`IPAllocationPool`),<br>IP Address + Mask (`IPInSubnetAllocationPool`) | System IP<br>Management IP |
| Container     | Subnet (`SubnetAllocationPool`)                                                    | ISL subnet                 |

More objects will be supported in the future.

## NetBox Configuration

To enable NetBox to send updates to the EDA app

### Create a Webhook

The Webhook in NetBox is triggered by the NetBox's Event Rule and allows NetBox to send updates to the EDA app.

   * **Name**: Any meaningful identifier
   * **URL**: `https://${EDA_ADDR}:${EDA_PORT}/core/httpproxy/v1/netbox/webhook/${INSTANCE_NAMESPACE}/${INSTANCE_NAME}`  
      Replace the `${INSTANCE_NAMESPACE}` with the EDA namespace name you will use to create the NetBox Instance custom resource later. The `${INSTANCE_NAME}` should be the name of the NetBox Instance custom resource you will create in the [Instance Customer Resource](#instance-resource) section.

      For example, if you want to create EDA-NetBox integration for the EDA Allocation pools in the `eda` namespace, and you will name your NetBox Instance CR simply `netbox`, then the URL will be:

      ```
      https://youredaaddress.com:9443/core/httpproxy/v1/netbox/webhook/eda/netbox
      ```

   * **Method**: `POST`
   * **Secret**: Choose a signature secret (plaintext string) that will be used to validate the webhook request. The matching Kubernetes secret with the same string will be created later in the [Kubernetes Secrets](#kubernetes-secrets) section.
   * **SSL verification**: Based on your setup either leave SSL verification enabled or disable it.
   * Leave all other settings as default.

### Create an Event Rule

An event rule is used to trigger webhook based on the events happening in NetBox. You will find the Event Rules menu item under the Integrations section in NetBox.

   * **Name**: Choose a relevant name
   * **Objects**: Include **IPAM IPAddresses** and **IPAM Prefixes**
   * **Enabled**: Yes
   * **Event Types**:

     * Object created
     * Object updated
     * Object deleted

   * **Action**:

     * **Type**: Webhook
     * **Webhook**: Select the one created above

### Generate an API Token

Using the Admin → Authentication → API Tokens menu create a NetBox API token for the NetBox user that EDA app will use. Enable write permission for the API token.

### Configure User Permissions

In the Admin → Authentication → Permissions menu, grant the user you created the API token for the permissions to `create`, `update`, and `delete` for the following objects:

* `IPAM > IPAddress`
* `IPAM > Prefix`
* `Extras > Tag` (a.k.a `Customizations.Tags` in earlier versions)
* `Extras > Custom Field` (a.k.a `Customizations.CustomFields` in earlier versions)

### Configure Global VRF Setting

Starting with NetBox 4.2.6, the `ENFORCE_GLOBAL_UNIQUE` setting has been flipped to `true`, this may have negative effect on EDA installations that use multiple topologies using the same IP addressing.

As per the [NetBox documentation](https://netboxlabs.com/docs/netbox/en/stable/models/ipam/vrf/), to relax this enforcement change the configuration setting of the global VRF via environment variable or in the `configuration.py` file.

```bash
ENFORCE_GLOBAL_UNIQUE=false
```

### Tags

In case you plan to have more than one "NetBox Prefix" → "EDA allocation pool" mapping, you will need to create a tag in NetBox for each distinct allocation pool and assign it to the Prefix object in NetBox.

In the [EDA Allocation](#allocation-resource) resource you then reference the tag name in the `tags` field and the allocation pool will be created based on the prefixes with that tag.

## Kubernetes Secrets

The NetBox API Token and the Webhook secret must be created as Kubernetes Secrets in the same namespace where the EDA NetBox app will run (example: `eda`). The data for these secrets must be provided as base64 encoded strings.

Secret for the webhook:

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/webhook-signature-secret.yaml"
```

///
/// tab | `kubectl`

```bash
cat << EOF | kubectl apply -f -
--8<-- "docs/apps/netbox/webhook-signature-secret.yaml"
EOF
```

///

Secret for the API Token:

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/api-token-secret.yaml"
```

///
/// tab | `kubectl`

```bash
cat << EOF | kubectl apply -f -
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

### Instance Resource

Defines connection details to the NetBox instance from the EDA NetBox app:

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

The NetBox Instance resource requires a user to provide names of the two [Kubernetes secrets](#kubernetes-secrets) created in the same namespace where the Instance is deployed:

1. The `apiToken` field references the secret containing the NetBox API Token.
2. The `webhookSignatureSecret` field references the secret containing the Webhook signature secret.

After creation, check the status of the Instance resource to verify successful connection.

### Allocation Resource

With Allocation resource a user specifies which NetBox Prefixes should create which EDA allocation pools.

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

The name of the Allocation resource will drive the name of the EDA allocation pool.

With [tags](#tags) a user selects which tagged Prefixes from NetBox would be "mapped" to this Allocation resource. Since NetBox prefixes don't have a unique name, the tags are used to identify the Prefixes.

A single NetBox prefix object can be mapped to three different allocation pools in EDA depending on the type specified in the Allocation resource.

| Type           | Resource Created                               | Typical Use                              |
| -------------- | ---------------------------------------------- | ---------------------------------------- |
| `ip-address`   | `ipallocationpools.core.eda.nokia.com`         | IP Addresses → **System IPs**            |
| `ip-in-subnet` | `ipinsubnetallocationpools.core.eda.nokia.com` | IP Addresses + Masks → **Management IP** |
| `subnet`       | `subnetallocationpools.core.eda.nokia.com`     | Subnets → **ISL links**                  |

Consult with the [Supported Objects](#supported-objects) section to see what status a NetBox prefix must have to be compatible with the desired allocation pool type.

The status field of the Allocation resource is used to track the matching allocations. For example, consider the following status block in the Allocation resource:

```yaml hl_lines="16-21"
apiVersion: netbox.eda.nokia.com/v1alpha1
kind: Allocation
metadata:
  name: nb-systemip-v4
  namespace: eda
  labels: {}
  annotations: {}
spec:
  enabled: true
  instance: netbox
  tags:
    - eda-systemip-v4
  type: ip-address
  description: ''
  subnetLength: null
status:
  matchedPrefixes:
    - id: 3
      prefix: 192.168.10.0/24
      tags:
        - eda-systemip-v4
  lastEvent: ''
  lastEventStatus: ''
  lastEventTime: null
```

It indicates that the incoming via Webhook NetBox prefix `192.168.10.0/24` tagged with the `eda-systemip-v4` tag was recorded with the ID `3` for this Allocation resource.

## Example

In this example, we will demonstrate how EDA/NetBox integration works by creating two Prefix objects in NetBox for System IPs and inter-switch link subnets that will be synchronized to EDA and result in two Allocation pools in EDA.  
The two pools will then be used to instantiate a Fabric in EDA and through that we will

We will install a demo NetBox instance[^1] in the same cluster that runs EDA using [helm](../user-guide/using-the-clis.md#helm) and the [netbox chart v6.0.33][artifacthub_chart]:

```bash
helm install netbox-server oci://ghcr.io/netbox-community/netbox-chart/netbox \
    --create-namespace \
    --namespace=netbox \
    --set superuser.password=netbox \
    --set enforceGlobalUnique=false \ #(1)!
    --version 6.0.33 #(2)!
```

[artifacthub_chart]: https://artifacthub.io/packages/helm/netbox/netbox?modal=changelog&version=6.0.33

1. `enforceGlobalUnique=false` [allows](https://netboxlabs.com/docs/netbox/models/ipam/vrf/#enforce-unique-space) configures the global VRF of NetBox to allow duplicate IP addresses. The duplicated IP addresses may be created by EDA when distinct topologies use the same IP addressing.
2. We fix the chart version to ensure the reproducibility of the example, but there is no hard dependency on the chart version.

The NetBox instance will take a few minutes to start, you can monitor the pods in the `netbox` namespace[^2] and once all pods are up and running, expose the NetBox instance:

```bash
kubectl -n netbox port-forward svc/netbox-server 45123:80
```

You should now be able to login to the NetBox UI via `http://localhost:45123` using `admin:netbox` credentials.

Then install the NetBox EDA app using one of the [documented methods](#installation).

<h4>NetBox configuration</h4>

<h5>Webhook</h5>

Go to Operations → Integrations → [Webhook](#create-a-webhook) in NetBox UI and create a webhook with the following values:

* Name: `eda`
* URL: `https://${EDA_ADDR}:${EDA_PORT}/core/httpproxy/v1/netbox/webhook/eda/netbox`  
    Replace `${EDA_ADDR}` and `${EDA_PORT}` with the address and port of the EDA instance you use.

* Secret: `eda`
* SSL verification: disabled

<h5>Event Rule</h5>

Go to Operations → Integrations → [Event Rules](#create-an-event-rule) in NetBox UI and create an Event Rule that will trigger the Webhook with the following fields set:

* Name: `eda`
* Object types:
    * `IPAM > IP Address`
    * `IPAM > Prefix`
* Enabled: checked
* Event types: `Object created` `Object deleted` `Object updated`
* Action type: `Webhook`
* Webhook: `eda` (the name of the webhook we created above)

<h5>API Token and Permissions</h5>

Normally you would [generate](#generate-an-api-token) a new API token for the user you want to use for API access, but since the demo instance of NetBox that we installed with the Helm chart already contains an API token for the `admin` user, we will just use it, instead of generating a new one.

<h5>Create secrets</h5>

Now we need to create the Kubernetes secrets for the generated API Token and the Webhook signature secret.

The inputs to the secrets should be in base64 format, therefore the snippets below run the raw inputs through `base64` command to convert them to base64 format.

We install the secrets in the `eda` namespace - the default namespace your EDA installation comes with. If you use another namespace, adjust the namespace name accordingly.

/// tab | Token secret

The NetBox Helm chart used in this example creates a Kubernetes secret `netbox/netbox-server-superuser` which contains the API token for the `admin` user. We will use the existing token value as is:

```bash
NETBOX_API_TOKEN=$(kubectl -n netbox get secret netbox-server-superuser -o jsonpath='{.data.api_token}')
cat << EOF | kubectl apply -f -
--8<-- "docs/apps/netbox/api-token-secret.yaml"
EOF
```

///
/// tab | Webhook signature secret

```bash
NETBOX_WEBHOOK_SIGNATURE_KEY=$(echo -n "eda" | base64)
cat << EOF | kubectl apply -f -
--8<-- "docs/apps/netbox/webhook-signature-secret.yaml"
EOF
```

///
/// tab | Token secret (regular installation)

In case you are repeating this exercise without using NetBox Helm chart, or if you run a non-admin user, you will need to generate the API Token manually.

```bash
NETBOX_API_TOKEN=$(base64 <<< "yourTokenHere")
cat << EOF | kubectl apply -f -
--8<-- "docs/apps/netbox/api-token-secret.yaml"
EOF
```

///

<h5>Prefixes and Tags</h5>

As per the task of this example we need to create two prefixes in NetBox, one for the System IPs and one for the subnets used by our [Fabric](./fabric.md) app to assign addresses on the point-to-point interswitch links.

We will also create a tag for each of the prefixes, such that we can use the tags to identify each prefix in EDA's Allocation resource.

Starting with the System IPs prefix, we first create a Tag using the Customization → Tags NetBox menu, we will name the tag simply `eda-systemip-v4`.  
Then create a prefix in IPAM → Prefixes NetBox menu and specify the `192.168.10.0/24` prefix with the Status=Active and assign the `eda-systemip-v4` tag to it.

Next, we need to create a Prefix for our interswitch links. In EDA, the Fabric app uses the allocation pool of type "subnet" to then assign point-to-point addresses to each end of the interswitch link. This means, that the Prefix in NetBox would need to be created with the `Container` status, as this would indicate that the Prefix is a container for sub-prefixes. Exactly what we need.

We create the `eda-isl-v6` tag first and then the Prefix `2005::/64` with the Status=Container and this tag assigned.

-{{image(url="https://gitlab.com/rdodin/pics/-/wikis/uploads/2aba28211fc4b0a236484719e0f0ebd2/CleanShot_2025-06-15_at_10.14.51.webp", padding=20)}}-

<h4>EDA configuration</h4>

Switching to EDA. Install the NetBox app if you haven't done already and proceed with creation of the NetBox Instance resource as per the [documentation](#instance-resource).

We are using the names of the Kubernetes secrets we created a moment ago for the API Token and the Webhook signature key. And since we deployed the NetBox inside the same cluster, we know the DNS name of the service it uses.

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/example-instance.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/netbox/example-instance.yaml"
EOF
```

///

Shortly after submitting the instance resource, you should see EDA reporting the instance as reachable in the status field of the instance resource. Verify with:

```bash
kubectl get instance netbox -n eda \
-o custom-columns="URL:.spec.url,STATUS:.status.reachable"
```

<div class="embed-result">
```{.bash .no-copy}
URL                                             STATUS
http://netbox-server.netbox.svc.cluster.local   true
```
</div>

<h5>Allocations</h5>

Once the Instance resource is configured and the NetBox is reachable, you can proceed with creating the Allocation resources.

As per our task, we need two Allocation Pools in EDA:

1. `IPAllocationPool` for the IPv4 addresses used as System IPs for our leaf and spines
2. `SubnetAllocationPool` for the subnets used for the interswitch links in our fabric.

Instead of creating these pools manually, we will create two Allocation resources from the EDA NetBox app and let it create these pools for us based on the NetBox prefixes.

Starting with the Allocation resource for the System IPs:

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/example-allocation.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/netbox/example-allocation.yaml"
EOF
```

///

The name of the Allocation resource (`nb-systemip-v4`) will drive the name of the EDA Allocation Pool name once NetBox app will get to create the pool based on the received webhook from the NetBox server.

In the specification block of the Allocation resource we provide

* the name of the NetBox instance resource we just created
* the tags to match the received prefixes from the NetBox server and associate with this Allocation. Recall, that we created this tag in NetBox and added it to the Prefix we intend to use for the System IPs.
* the type of the allocation, which will drive the type of the EDA Allocation Pool. Since System IPs are plain IPv4 addresses, we choose `ip-address` type.

Following the same approach, create the Allocation resource for the subnets used for the interswitch links:

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/example-allocation-subnet.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/netbox/example-allocation-subnet.yaml"
EOF
```

///

The difference between the two Allocation resources is the type of the allocation. Since subnets are CIDR blocks, we choose the `subnet` type and we also specify the `subnetLength` property to define the length of the subnet to allocate from the received prefix.

Once you have the Allocation resources created, you should see the pools with the matching names created in EDA:

/// tab | IP Pool

```bash
kubectl -n eda get ipallocationpool nb-systemip-v4
```

<div class="embed-result">
```
NAME             AGE
nb-systemip-v4   13h
```
</div>
///
/// tab | Subnet Pool
```bash
kubectl -n eda get subnetallocationpool nb-isl-v6
```
<div class="embed-result">
```
NAME        AGE
nb-isl-v6   13h
```
</div>
///

<h5>Fabric</h5>

Next we create a fabric resource using the [EDA Playground](../getting-started/try-eda.md) topology setup in this example. We reference the allocation pools our NetBox app created when it synced the prefixes:

/// tab | YAML

```yaml
--8<-- "docs/apps/netbox/nb-fabric.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/netbox/nb-fabric.yaml"
EOF
```

///

The Fabric app will use the referenced pools and will try to allocated the pool resources in order to instantiate a fabric. In our example the System IP (v4) and Subnets (v6) will be allocated from the pools and the allocated resources will be populated back to the NetBox server to keep track of the allocated resources.

From the Prefix we created for System IPs you will see the three allocated IPs populated back in NetBox server, one per each spine and leaf in our topology:

-{{image(url="https://gitlab.com/rdodin/pics/-/wikis/uploads/e9d7e4c0c7576aa627cae29aa7b3d95e/CleanShot_2025-06-15_at_11.37.00.webp", padding=20)}}-

In the same way, you will see interswitch subnets carved out from the `2005::/64` prefix, one per each link between leafs and spines:

-{{image(url="https://gitlab.com/rdodin/pics/-/wikis/uploads/a7f13496f85de337d8675a139dc870f9/CleanShot_2025-06-15_at_11.32.43.webp", padding=20)}}-

<h5>Custom Fields</h5>

The NetBox app also creates some custom fields in NetBox model to backtrack the allocation of the resources. For example, if you select an allocated sub-prefix from the `2005::/64` prefix, you will see EDA custom fields that show the Allocation resource that created this allocation and the owner object that requested the allocation.

-{{image(url="https://gitlab.com/rdodin/pics/-/wikis/uploads/2a6b0cf2756bb5f261630d6bab42c8b0/CleanShot_2025-06-15_at_11.43.10.webp", padding=20)}}-

The objects allocated by EDA will also have the `EDAManaged` tag assigned to them.

[^1]: Based on NetBox Community v4.3.2-Docker-3.3.0 version and [Helm chart v6.0.33][artifacthub_chart].
[^2]: Or run a wait with:  

    ```bash
    kubectl -n netbox wait --for=condition=available --timeout=300s \
    deployment/netbox-server
    ```
