# Add a Custom App Store Registry

## Overview

An App Store Registry is a container registry that contains OCI compliant images of an App. It is where you will upload your full App content and code as a single OCI image.

The `manifest.spec.image` field will point to the specific App image with a specific tag for each version.

## Adding a Registry to the App Store

### Creating a Credentials Secret

Before you can add a Registry to the App Store, you must create a Kubernetes secret that contains the credentials to connect to the Registry git repository over HTTPS. This can be done using the following resource where you replace the data with the correct `base64` encoded values.

=== "YAML Resource"
    ```yaml
    --8<-- "docs/development/resources/authSecretRef.yaml"
    ```

=== "`kubectl apply` command"
    ```bash
    kubectl apply -f - <<EOF
    --8<-- "docs/development/resources/authSecretRef.yaml"
    EOF
    ```

!!! Note "Make sure to give the secret a different name than the Catalog Credentials secret"

### Creating the Registry

You can create your own Registry using the following resource. This uses the above created secret as `authSecretRef`.

=== "YAML Resource"
    ```yaml
    --8<-- "docs/development/resources/registry.yaml"
    ```

=== "`kubectl apply` command"
    ```bash
    kubectl apply -f - <<EOF
    --8<-- "docs/development/resources/registry.yaml"
    EOF
    ```

## Limitations

### Using Artifactory container registry with Apps using embedded container images

Artifactory currently doesn't support OCI compliant images with embedded container images. If you are creating an advanced App that uses its own container image, you can not use Artifactory as a registry. An alternative could be to host your own [Harbor](https://goharbor.io/) registry.

Regular MicroPython Apps do not have this limitation, for these Artifactory will work fine.
