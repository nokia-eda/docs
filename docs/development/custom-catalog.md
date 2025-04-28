# Add a Custom App Store Catalog

## Overview

An App Catalog is a structured git repository that contains all the necessary information app store needs to install an app. The `Manifest`  is the most important one. But the app can also contain other app metadata information for the UI, like a README, or a license (see the manifest `appInfo`  specification field). The catalog of built-in apps that is delivered along with EDA can be found here.

## Catalog Structure

The structure of a catalog is as follows:

```
vendors/
    <vendor-1-name>
        apps/
            <app-1-name>/
                manifest.yaml
                README.md
                LICENSE
                ... # Other useful files, which can be referenced in the manifest and used in the UI.
            <app-2-name>/
                ...
    <vendor-2-name>/
        apps/
            ...
    ...
```

/// admonition | The manifest of an App must be called `manifest.yaml` and be placed in `vendors/<vendor-name>/apps/<app-name>/manifest.yaml` in the git repository.
    type: note
///

### App Versioning

Apps will have multiple versions. To version the Apps in the Catalog, git tags are used. A structured git tag will be seen as an installable App (with a certain version) for the App Store, which can then be installed from the UI.

Any tag in the form of `vendors/<vendor-name>/apps/<app-name>/<version>` will be registered as an installable App by the App Store.

The version field should conform to [Semantic Versioning 2.0](https://semver.org/), prefixed with a "v". For example: v0.1, v0.1.0-alpha.

## Adding a Catalog to the App Store

### Creating a Credentials Secret

If the Catalog-hosting Git repository requires authentication, you must create a Kubernetes secret that contains the credentials to connect to the Catalog git repository over HTTPS. This can be done using the following resource where you replace the data with the correct `base64` encoded values.

/// tab | YAML Resource

```yaml
--8<-- "docs/development/resources/authSecretRef.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/development/resources/authSecretRef.yaml"
EOF
```

///

### Creating the Catalog

You can create your own Catalog using the following resource. This uses the above created secret as `authSecretRef`.

/// tab | YAML Resource

```yaml
--8<-- "docs/development/resources/catalog.yaml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<EOF
--8<-- "docs/development/resources/catalog.yaml"
EOF
```

///
