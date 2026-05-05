# Uploading the assets

/// admonition | Caution
    type: note
These steps are meant to be executed in the air-gapped environment.
///

The [downloaded assets](downloading-the-assets.md#downloading-the-assets-bundles) need to be uploaded to the respective hosting services in the air-gapped environment. As was mentioned in the [Hosting services in air-gapped environment](index.md#hosting-services-in-air-gapped-environment) section, there are two options how the services can be hosted in the air-gapped environment:

1. All services are hosted on a single Asset Host (typically deployed as an Assets VM).
2. Some services are hosted on different hosts.

The procedure for uploading the assets slightly differs depending if all services are uploaded to a single Asset Host or if some are uploaded to different hosts.

## Setting EDA version

Set the `EDA_CORE_VERSION` environment variable (and any `SKIP_...`[^1] environment variables you used when downloading the assets) in your shell. This will ensure that the correct version of the cache and assets is uploaded to the Assets VM.

```bash
export EDA_CORE_VERSION=-{{ eda_version }}-
```

## Uploading all assets to a single Asset Host

When a container registry, a Git server, and a web server are all hosted on a single Asset Host[^2], set the `ASSET_HOST` environment variable to the address of the Asset Host hosting the services and execute the following command to upload all the assets to the Asset Host:

```bash
make -C bundles/ load-all-bundles \
    ASSET_HOST=192.0.2.228 \ #(1)!
    B64_ASSET_HOST_GIT_USERNAME="ZWRh" \ #(2)!
    B64_ASSET_HOST_GIT_PASSWORD="ZWRh" \
    B64_ASSET_HOST_ARTIFACTS_USERNAME="ZWRh" \ #(3)!
    B64_ASSET_HOST_ARTIFACTS_PASSWORD="ZWRh"
```

1. IP address or FQDN of the Asset Host.
2. Base64 encoded (without newline) username and password for the Git server, defaulting to `eda` for both username and password.
3. Base64 encoded (without newline) username and password for the web server, defaulting to `eda` for both username and password.

/// admonition | Notes
    type: subtle-note

1. Make sure to replace the `ASSET_HOST` IP with the IP of your Asset VM.
2. The username and passwords will be configurable in the near future. The `eda` username and password are used by default.

///

## Uploading assets to different hosts

If some of the services are hosted on different hosts, a user needs to use one of the following Make variables:

* `ASSET_HOST_REGISTRY`
: example: `registry.corp.com`  
This **should not** specify a scheme like http / https
If a user needs to force http, then scheme must be specified as: http://registry.com

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
load-eda-bundle-connect-2-0-0 \ #(1)!
load-eda-bundle-core-25-12-3 \
load-eda-bundle-apps-25-12-3 \
load-eda-bundle-tools-2-0-0 \
ASSET_HOST_GIT=https://mygit.net/git/project1337 \
B64_ASSET_HOST_GIT_USERNAME="ZWRh" \
B64_ASSET_HOST_GIT_PASSWORD="ZWRh" \
ASSET_HOST_ARTIFACTS=https://mysrv.net/artifacts-upload \
B64_ASSET_HOST_ARTIFACTS_USERNAME="ZWRh" \
B64_ASSET_HOST_ARTIFACTS_PASSWORD="ZWRh" \
ASSET_HOST_REGISTRY=myregistry.net \
B64_ASSET_HOST_REGISTRY_USERNAME="ZWRh" \
B64_ASSET_HOST_REGISTRY_PASSWORD="ZWRh"
```

1. This example shows how to upload individual bundles to the respective hosts, instead of uploading all bundles.

Once all uploads complete successfully, the Assets Host is ready to support the installation of the Nokia EDA platform in an air-gapped environment.

[:octicons-arrow-right-24: Deploying EDA](../deploying-eda/index.md)

[^1]: If you used `SKIP_...` environment variables when [downloading the assets](downloading-the-assets.md#downloading-the-assets-bundles), make sure to set the same variables when uploading the assets to the Assets VM.
[^2]: Called a *unified mode*.
