# Terraform

<small>[:octicons-link-external-16: Nokia EDA Providers Reference][tf-registry-namespace] · ==**Beta release**==</small>

[Terraform](https://www.terraform.io/) is open-source infrastructure as code software that allows users to define resources in human-readable configuration files, which can be versioned, reused, and shared.

Terraform can manage low-level components such as compute, storage, and networking resources, as well as high-level components like DNS entries and SaaS features. In the context of Nokia EDA, Terraform is used to declaratively manage EDA Resources[^1] by defining them in Terraform files and applying them to the EDA cluster using providers from Nokia.

## Terraform Providers for EDA

Terraform creates and manages resources on cloud platforms and other services through their application programming interfaces (APIs). Providers enable Terraform to interact with virtually any platform or service that exposes an API.

-{{image(url='https://gitlab.com/rdodin/pics/-/wikis/uploads/c203c48300d0c69a9a515a1b40401c6a/image.png',padding=20, shadow=True)}}-

In the diagram above, the Nokia EDA API server represents the _Target API_, and the [Terraform providers published by Nokia][tf-registry-namespace] are used by Terraform to interface with it.

[tf-registry-namespace]: https://registry.terraform.io/namespaces/nokia-eda

Nokia EDA offers unprecedented extensibility, allowing users to install EDA applications at any time. As a result, its API surface is highly dynamic and extensible. Rather than a single Terraform provider for EDA, each EDA application has its own standalone provider.  
Terraform users install providers for each EDA application they wish to manage, specifying the desired API version.

> The Terraform providers for EDA are open sourced and published under the [nokia-eda][tf-registry-namespace] namespace in the Terraform registry.

### Versions

Providers include two types of versioning information:

<h4> API Version </h4>

This refers to the specific application API version for which the provider is built. In EDA, applications may have several API versions (e.g., `v1alpha1`, `v1`, `v2`, and so on). The provider's name will include the API version; for example, the **interfaces-v1alpha1** provider is designed to be used with the **Interfaces v1alpha1** API version.

This means automation users should focus on the API version supported, rather than the installed application version.

<h4> Provider Version </h4>

This is the version of the Terraform provider itself, which is independent of the Application API version. It follows [Semantic Versioning](https://semver.org/) principles and indicates changes to the provider's functionality, compatibility, documentation, and more. The provider version is visible in the registry UI and in the Git repository where the provider's code is stored.

> In summary, for the provider with the name `interfaces-v1alpha1` and version `0.1.0`:
>
> * the application this provider is built for is `Interfaces`
> * the Interfaces API version is `v1alpha1`
> * and the provider version is `0.1.0`.

## Installation

To install the Terraform providers for Nokia EDA, add the required provider block to your Terraform file[^2]:

```hcl title="providers.tf"
terraform {
  required_providers {
    interfaces-v1alpha1 = {
      source  = "nokia-eda/interfaces-v1alpha1"
      version = "0.0.5"
    }
  }
}
```

> The `version` can be omitted; Terraform will default to the latest version.

When you have the `required_providers` block in place, the Terraform CLI will download the required provider binary when [initializing](https://developer.hashicorp.com/terraform/cli/init) a working directory. It can automatically download providers from a Terraform registry:

/// tab | Terraform init

```
terraform init
```

///

/// tab | Output

```
Initializing the backend...
Initializing provider plugins...
- Finding nokia-eda/interfaces-v1alpha1 versions matching "0.0.5"...
- Installing nokia-eda/interfaces-v1alpha1 v0.0.5...
- Installed nokia-eda/interfaces-v1alpha1 v0.0.5 (self-signed, key ID 6F5BC22CD9F83F19)
Partner and community providers are signed by their developers.
If you'd like to know more about provider signing, you can read about it here:
https://developer.hashicorp.com/terraform/cli/plugins/signing
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.


Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

///

## Configuration

The provider needs to be configured with the proper credential information before it can be used. Provider configuration is typically defined in the same file as your provider specifications. For example, if you defined your provider in the `providers.tf` file above, you can add the provider configuration block there as well:

```hcl title="providers.tf" hl_lines="10-12"
terraform {
  required_providers {
    interfaces-v1alpha1 = {
      source  = "nokia-eda/interfaces-v1alpha1"
      version = "0.1.0"
    }
  }
}

provider "interfaces-v1alpha1" {
  # Configuration options
}
```

### Options

At a minimum, provider configuration[^3] specifies the API server address and authentication parameters.

<h4> Base URL </h4>

With `base_url` provider configuration, users set the address of the EDA API server. This is the same address you use to access the EDA UI and includes the schema and port. For example: `https://eda-demo.test.io:9443`.

<h4> Authentication options </h4>

Terraform, like other non-browser-based API clients, uses the [Resource Owner Password Credentials Grant][oauth-rfc-ropc] OAuth flow for authentication. This flow requires the API client to provide the following parameters:

<h5> EDA Client ID </h5>

The `eda_client_id` is an identifier for your API client. It is used to authenticate your requests to the EDA API. By default EDA comes with a pre-created client id of `eda`. Administrators can create other clients.

Default value: `eda`.

<h5> EDA Client Secret </h5>

The secret that is associated with the `eda_client_id`. Stored in Keycloak and can be retrieved by administrators and provided to the users of the API. Refer to the API documentation to see how to fetch the `eda_client_secret` using [Keycloak UI](../api/index.md#getting-the-client_secret).

/// warning
If you omit the `eda_client_secret` parameter, the provider will try to fetch the secret by authenticating with the Keycloak service using `kc_*` variables that are set to their default values. While this might be tempting to use, this method is not recommended and should not be used in production.
///

<h5> EDA Username and Password </h5>

The API client - Terraform - should have credentials of the EDA user it authenticates as. This is done by providing the `eda_username` and `eda_password` parameters in the provider configuration.

Default value for both is `admin` if not set.

[oauth-rfc-ropc]: https://datatracker.ietf.org/doc/html/rfc6749#autoid-45

<h5> TLS Verification </h5>

With `tls_skip_verify` boolean flag a user can select whether to verify the TLS certificate presented by EDA's API server or not.

Default value: `false` (means validate certificate)

With the mandatory options set, the provider configuration takes the following form:

```hcl title="snippet from providers.tf"
provider "interfaces-v1alpha1" {
  base_url          = "https://eda-demo.test.io:9443"
  eda_client_id     = "eda" # default value, can be omitted if not changed
  eda_client_secret = "your_client_secret"
  eda_username      = "your_username"
  eda_password      = "your_password"
}
```

### Environment variables

All configuration variables that can be provided to the EDA providers have a matching environment variable. The below table summarizes all available options:

| TF variable         | OS env variable     | Default     | Description         |
| ------------------- | ------------------- | ----------- | ------------------- |
| base_url            | EDA_BASE_URL        |             | Base URL            |
| kc_username         | KC_USERNAME         | "admin"     | Keycloak Username   |
| kc_password         | KC_PASSWORD         | "admin"     | Keycloak Password   |
| kc_realm            | KC_REALM            | "master"    | Keycloak Realm      |
| kc_client_id        | KC_CLIENT_ID        | "admin-cli" | Keycloak Client ID  |
| eda_username        | EDA_USERNAME        | "admin"     | EDA Username        |
| eda_password        | EDA_PASSWORD        | "admin"     | EDA Password        |
| eda_realm           | EDA_REALM           | "eda"       | EDA Realm           |
| eda_client_id       | EDA_CLIENT_ID       | "eda"       | EDA Client ID       |
| eda_client_secret   | EDA_CLIENT_SECRET   |             | EDA Client Secret   |
| tls_skip_verify     | TLS_SKIP_VERIFY     | false       | TLS skip verify     |
| rest_debug          | REST_DEBUG          | false       | REST Debug          |
| rest_timeout        | REST_TIMEOUT        | "15s"       | REST Timeout        |
| rest_retries        | REST_RETRIES        | 3           | REST Retries        |
| rest_retry_interval | REST_RETRY_INTERVAL | "5s"        | REST Retry Interval |

## Bulk Installation

If selecting and configuring providers in an a-la-carte manner feels like a cumbersome approach given they share the same config values, here is an all-you-can-eat buffet approach that lists a bunch of providers you can put in your `providers.tf` file and configure them all using variables:

/// details | Bulk install and configure example
    type: code-example

```hcl
--8<-- "docs/development/terraform/providers-all.tf"
```

///

## Using the Providers

With the providers configured a user can start managing their infrastructure in EDA using Terraform by defining the [resources][resource-doc] and [data-sources][datasource-doc] that the providers expose.

[datasource-doc]: https://developer.hashicorp.com/terraform/language/data-sources
[resource-doc]: https://developer.hashicorp.com/terraform/language/resources

### Resources

Resources are the most important element in the Terraform language. Each resource block describes one or more infrastructure objects in general, and in EDA's case, these are the resources you create in EDA, such as an Interface, a Virtual Network, a Fabric, a User, etc.

Each provider exposes its own set of resources and they are documented in the provider's documentation on Terraform [registry][tf-registry-namespace], for example, here is a link to the list of resources provided by the [Interfaces][interfaces-tf-doc] provider.

[interfaces-tf-doc]: https://registry.terraform.io/providers/nokia-eda/interfaces-v1alpha1/latest/docs

The most obvious resource in the Interfaces app is the [interface][interface-resource-tf-doc] itself which, as the name suggests, allows users to manage Interface resources in EDA. The Terraform resources are modelled after the EDA resources, therefore it is very easy to map between the two, they are essentially the same.

[interface-resource-tf-doc]: https://registry.terraform.io/providers/nokia-eda/interfaces-v1alpha1/latest/docs/resources/interface

For example, let's compare what it takes to define an interface `ethernet-1/14` on `leaf1` using the [Try EDA Playground](../../getting-started/try-eda.md) from the Getting Started guide using EDA UI and Terraform:

/// tab | EDA UI
Navigating to the **Topology → Interfaces** in the left sidebar and creating a new interface with the following parameters:

* name: leaf1-ethernet-1-14
* namespace: eda
* enabled: true
* description: "set via UI"
* LLDP: enabled
* encap type: 'null'
* members:
    * interface: ethernet-1-14
    * node: leaf1

Would be represented like this:

-{{image(url='https://gitlab.com/rdodin/pics/-/wikis/uploads/625371d2534fed2d50ee0b3266845181/CleanShot_2025-08-20_at_19.55.36.webp', padding=10)}}-

Now look what would be the equivalent Terraform configuration in the next tab.

///
/// tab | Terraform
With terraform, the resources contain the same fields and take in the same values as in the UI. Some may say "obviously", because at the end they use the same EDA API to create manage the resources.

Here is the definition of the same interface in the Hashicorp Configuration Language that Terraform uses:

```hcl
resource "interfaces-v1alpha1_interface" "leaf1-ethernet-1-14" {
  metadata = {
    name      = "leaf1-ethernet-1-14"
    namespace = "eda"
  }
  spec = {
    enabled     = true
    encap_type  = "null"
    type        = "interface"
    lldp        = true
    description = "set via Terraform"
    members = [{
      enabled   = true
      node      = "leaf1"
      interface = "ethernet-1-14"
    }]
  }
}
```

/// note
Fields that have the same name in a resource spec must be uniquely identifiable, which result in the same-named fields being disambiguated using `_1`, `_2` suffix. For example, if the `bgp` field is present in the fabric provider at different levels of the hierarchy, it will be referenced as `bgp_1`, `bgp_2`, etc. The provider reference will show the accurate names as expected to be provided by the user.
///

///

As shown in the Terraform tab above, the resources for the EDA applications are almost indistinguishable from the YAML representation you see in the EDA UI. One thing to note is that the Terraform resource omits the `apiVersion` and `kind` fields, because they are set by the provider already.

### Data-sources

Data sources allow Terraform to use information defined outside of Terraform, defined by another separate Terraform configuration. Each provider exposes its own set of data-sources and they are documented in the provider's documentation on Terraform [registry][tf-registry-namespace], for example, here is a link to the list of resources provided by the [Interfaces][interfaces-tf-doc] provider.

You will notice that the data-sources follow a particular pattern: a data-source ending with `_list` fetches multiple instances of a resource, while a data-source without it fetches a single instance. Here are some examples of how data sources can be used in different scenarios:

```hcl
# Get all interfaces.
data "interfaces-v1alpha1_interface_list" "all" {
  namespace = "eda"
}

# Get all interfaces with label selector
data "interfaces-v1alpha1_interface_list" "interswitch" {
  namespace     = "eda"
  labelselector = "eda.nokia.com/role=interSwitch"
}

# Get a single interface by name
data "interfaces-v1alpha1_interface" "leaf1_ethernet_1_1" {
  namespace = "eda"
  name      = "leaf1-ethernet-1-1"
}
```

### Import

Terraform supports importing existing resources into your Terraform state. This is useful for managing resources that were created before you started to use Terraform or were created outside of Terraform. This is known as a brownfield deployment scenario.

The [import documentation](https://developer.hashicorp.com/terraform/language/import) covers various ways to import resources, including the [generate configuration](https://developer.hashicorp.com/terraform/language/import/generating-configuration) method that we show below to import a couple of existing interfaces into the `interfaces.tf` file[^4]:

```hcl
import {
  to = interfaces-v1alpha1_interface.leaf1-ethernet-1-1
  id = "eda/leaf1-ethernet-1-1"
}

import {
  to = interfaces-v1alpha1_interface.leaf2-ethernet-1-1
  id = "eda/leaf2-ethernet-1-1"
}
```

By adding these import statements to your module and running `terraform plan -generate-config-out=interfaces.tf`, Terraform will:

1. Check the state file for the imported resources and proceed with fetching them if the state does not contain them.
2. Reach out to the EDA API fetching the resources using the `.import.id` value defined.
3. Create the `interfaces.tf` file where the imported resources will be written.

After the successful import, you can remove the `import` blocks.

> The [import ID](https://developer.hashicorp.com/terraform/language/import#import-id) is a unique identifier for the resource being imported. In EDA, this will typically be the resource's namespace and name, formatted as `namespace/name`.

## Issues and Limitations

1. Workflows cannot be triggered via Terraform.
2. Transaction-based operations are not supported yet. These operations, where resources are jointly committed via the Transaction API, are instead managed via REST API calls to the respective application endpoints, not through the Transaction API.
3. Direct calls to application endpoints in the current release do not store node/resource diffs. Node diffs are only stored when using the Transaction API.
4. Fields that have the same name in a resource spec must be uniquely identifiable, which result in the same-named fields being disambiguated using `_1`, `_2` suffix. For example, if the `bgp` field is present in the fabric provider at different levels of the hierarchy, it will be referenced as `bgp_1`, `bgp_2`, etc. The provider reference will show the accurate names as expected to be provided by the user.

[^1]: Such as interfaces, fabrics, virtual networks and so on.
[^2]: Often the providers configuration goes into the `providers.tf` file as per the [style guide](https://developer.hashicorp.com/terraform/language/style#file-names).
[^3]: Full list of options you can find in the providers documentation hosted on Terraform registry.
[^4]: The file must not exist before the `terraform plan` command is run.
