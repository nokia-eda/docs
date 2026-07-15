# Uploading the assets

/// admonition | Caution
    type: note
These steps are meant to be executed in the air-gapped environment.
///

As described in [Hosting assets](hosting-assets.md), there are two ways the services can be hosted in the air-gapped environment:

1. All services are hosted on a single Assets Host (typically deployed as an Assets VM).
2. Some services are hosted on different hosts.

The procedure differs depending on whether assets are uploaded through a single Assets Host or to services running on different hosts.

## Prerequisites

> Skip this step if you have already completed it as part of the [Assets VM](assets-vm.md#prerequisites) deployment.

--8<-- "docs/software-install/air-gapped/assets-vm.md:prerequisites"

/// note
In case you used the archive-based [transfer method](downloading-the-assets.md#transferring-the-assets-to-the-air-gapped-environment) to get the assets in the air-gapped environment, you need to unpack the archive:

```bash title="assuming the archive is named edaadm.tar"
tar -xf edaadm.tar
```

///

## Setting EDA version

Set the `EDA_CORE_VERSION` and `EDA_APPS_VERSION` environment variables in your shell to the target Nokia EDA release version. Otherwise, the latest version is assumed.

```bash
export EDA_CORE_VERSION=-{{ eda_version }}-
export EDA_APPS_VERSION=-{{ eda_version }}-
```

## Preparing the Git repositories for user bundles

/// warning
Execute this step if all of the following conditions are met, otherwise skip it:

1. You are using EDA-provided Git servers.
2. You have user bundles that contain Git repositories.
///

Before loading the bundles, ensure that the custom repositories are configured in the setters file as described in [Step 2 of User bundles](asset-bundles.md#custom-repositories). Then run the following command from the root of the `edaadm` repository:

```bash
make -C kpt/ eda-configure-shipyard eda-shipyard
```

## Uploading assets to a single Assets Host

When a container registry, Git server, and web server are all hosted on a single Assets Host[^1], specify the Assets Host address by using the `ASSET_HOST` Make variable in the following command:

```bash linenums="1"
make -C bundles/ load-default-bundles \
    load-<bundle-name> \ #(4)!
    ASSET_HOST=192.0.2.228 \ #(1)!
    B64_ASSET_HOST_GIT_USERNAME="ZWRh" \ #(2)!
    B64_ASSET_HOST_GIT_PASSWORD="ZWRh" \
    B64_ASSET_HOST_ARTIFACTS_USERNAME="ZWRh" \ #(3)!
    B64_ASSET_HOST_ARTIFACTS_PASSWORD="ZWRh"
```

1. IP address or FQDN of the Assets Host.
2. Base64 encoded (without newline) username and password for the Git server, defaulting to `eda` for both username and password.
3. Base64 encoded (without newline) username and password for the web server, defaulting to `eda` for both username and password.
4. In case you downloaded bundles other than the default bundle list, you need to specify the bundle names you used in the [downloading the assets](downloading-the-assets.md#downloading-the-nokia-eda-assets-bundles) step to upload the assets to the Assets Host.

/// admonition | Notes
    type: subtle-note

1. Note that besides the mandatory `load-default-bundles` target, you need to specify any additional bundle names you used in the [Downloading the assets](downloading-the-assets.md#downloading-the-nokia-eda-assets-bundles) step, as shown on line 2 of the example above.
2. Replace the `ASSET_HOST` IP address with the IP address of your Assets VM.
3. The usernames and passwords will be configurable in a future release. The default username and password are both `eda`.

///

## Uploading assets to different hosts

If some of the services are hosted on different hosts, you need to use one or more of the following Make variables:

* `ASSET_HOST_REGISTRY`
: example: `registry.corp.com`  
This **should not** specify a scheme such as HTTP or HTTPS.
If you need to force HTTP, the scheme must be specified as `http://registry.com`.

* `ASSET_HOST_GIT`
: example: `https://git.corp.com`

* `ASSET_HOST_ARTIFACTS`
: example: `https://artifacts.corp.com`

Specify the authentication credentials in base64 encoding for the used services by providing the following Make variables:

* `B64_ASSET_HOST_GIT_USERNAME`
* `B64_ASSET_HOST_GIT_PASSWORD`
* `B64_ASSET_HOST_ARTIFACTS_USERNAME`
* `B64_ASSET_HOST_ARTIFACTS_PASSWORD`
* `B64_ASSET_HOST_REGISTRY_USERNAME`
* `B64_ASSET_HOST_REGISTRY_PASSWORD`

```bash title="Example"
make -C bundles/ \
    load-default-bundles \
    load-<bundle-name> \ #(2)!
    ASSET_HOST_GIT=https://mygit.net/git/project1337 \ #(1)!
    B64_ASSET_HOST_GIT_USERNAME="ZWRh" \
    B64_ASSET_HOST_GIT_PASSWORD="ZWRh" \
    ASSET_HOST_ARTIFACTS=https://mysrv.net/artifacts-upload \
    B64_ASSET_HOST_ARTIFACTS_USERNAME="ZWRh" \
    B64_ASSET_HOST_ARTIFACTS_PASSWORD="ZWRh" \
    ASSET_HOST_REGISTRY=myregistry.net \
    B64_ASSET_HOST_REGISTRY_USERNAME="ZWRh" \
    B64_ASSET_HOST_REGISTRY_PASSWORD="ZWRh"
```

1. Example of the Git server address.
2. In case you downloaded bundles other than the default bundle list, you need to specify the bundle names you used in the [downloading the assets](downloading-the-assets.md#downloading-the-nokia-eda-assets-bundles) step to upload the assets to the respective hosts.

Once all uploads have completed successfully, the asset-hosting services are ready to support installation of the Nokia EDA platform in the air-gapped environment.

[:octicons-arrow-right-24: Deploying EDA](../deploying-eda/index.md)

[^1]: Called a *unified mode*.
