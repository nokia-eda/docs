# Build and Publish

-{{ js_script("/javascripts/viewer-static.min.js") }}-

We take pride in EDA's extensibility through applications, and one of the key aspects of this extensibility is the ease of build, publish, share and install workflows.  
EDA uses standard, well-known and established toolchains for this purpose:

- OCI image as a packaging format for the application
- Container registry as a storage for the application images
- Git for catalog and application discovery and sharing

From the distribution point of view, EDA app consists of two distinct artifacts that are coupled together:

1. An app manifest file that describes the app components, including the URL/tag of the app image
2. An OCI image that contains the app components

This structure can be visualized as:

-{{diagram(path='./diagrams/apps-dev.drawio',page=1, title='', zoom=1.5)}}-

In this chapter we will cover the process of building and publishing an application.

## Building an OCI App Image

We refer to the process of packaging the application artifacts into an [OCI](https://opencontainers.org/) image format as "building" the image. But building the image alone won't make the app installable, as the image needs to be hosted in an OCI container registry that is reachable from your EDA cluster.
As these two steps are tightly coupled, we have a single command in the `edabuilder` CLI that takes care of both operations at once - `edabuilder build-push`.

Since most container registries require authentication, we first need to login to the registry. The `edabuilder` has a `login registry` subcommand that takes in two arguments - username and password.  
For example, to login to a free ghcr.io registry, you would use the following command:

```shell
edabuilder login registry -u <username> -p <password> ghcr.io #(1)!
```

1. If you're using GitHub CLI, then instead of providing the token as a password, you can make use of the `gh` CLI tool and perform the following:

    Add `write:packages` scope to your token:

    ```shell
    gh auth login -s 'write:packages'
    ```

    And then use the token as:

    ```shell
    edabuilder login registry -u hellt -p $(gh auth token) ghcr.io
    ```

With the authentication step out of the way, we need to make sure that the application manifest has the correct container image URL and tag set. When `edabuilder` scaffolds an application it sets the image name in the app's manifest. If you have followed the [quickstart guide](quick-start.md), your `banners` app manifest file will contain the following:

```yaml title="banners/manifest.yaml"
apiVersion: core.eda.nokia.com/v1
kind: Manifest
metadata:
  name: banners
spec:
  # omitted for brevity
  group: banners.eda.local
  image: change.me/banners:v0.0.0
```

As an app owner, you set the image value to an image URI that points to the registry where you want the image to be published in the app manifest file[^1]. As we are using ghcr.io for this example, we could set the image value to e.g.:

```diff
- image: change.me/banners:v0.0.0
+ image: ghcr.io/eda-labs/banners:v2.1.0
```

Now, `edabuilder build-push` has everything it needs - an image URI and the credentials for the container registry the image points to. Simply point the command towards your app directory, like so:

```shell title="run from the project's directory"
edabuilder build-push --app banners #(1)!
```

1. `banners` is the directory that holds the app's `manifest.yaml`. If your app has a different name, use its directory instead.

A successful `build-push` action ends by prompting you with "Successfully pushed OCI Image". Your app image should now show up in the registry. If you intend to have your image accessible without authentication, make your image public using the interface of your registry provider.

## Publishing an App

The second pillar of an app is its manifest file, which we still need to publish to a catalog of our choice.

The first thing you need to ensure is that you have a git repository created that you intend to use as an App Catalog for your EDA applications. In this example, we will be using our [eda-labs/catalog](https://github.com/eda-labs/catalog) repository that we use for our community-oriented applications.

Start off by logging into the Git provider of your choice to make sure you are authorized to push the manifest to the repository:

```shell
edabuilder login git -u hellt -p $(gh auth token) https://github.com/eda-labs/catalog #(1)!
```

1. Change the user, password and repository URL to the appropriate values for your repository.

After a successful login we can publish our application manifest to the repository:

```shell
edabuilder publish https://github.com/eda-labs/catalog --app banners
```

A successful publish of the manifest should result in the following output:

```
Publishing to branch 'main'
No app version given, using the manifest image tag as app version: 
Staging `banners` at version `v2.1.0`
Successfully published Apps
```

Now you should see the application manifest published in your Git repository following the `vendors/<vendor-name>/apps/<app-name>` path:

-{{image(url="graphics/CleanShot_2025-03-29_at_14.14.59_2x.webp", shadow=true, padding=20, title="Application manifest published in Git repository")}}-

The app version will be matching the version from the image tag found in the manifest, unless the version is provided inline with the `--app` argument, for example `--app manifest=banners/manifest.yaml,version=v2.1.1`.

To republish an app, i.e. override an existing version, add `--force` flag to the command.

## Signing an App

Before installing an app, EDA verifies the signature of its OCI image against the public keys the cluster trusts. If the image is unsigned, or signed with a key the cluster doesn't know, the install fails, unless an administrator turns off signature verification for the registry hosting the image. Signing your app images means nobody has to lower that guard, and gives your users a guarantee that the image they install is the one you built.

### Generating a key pair

`edabuilder` can create the key pair for you:

```shell
export SIGNING_KEY_PASSWORD=<passphrase> #(1)!
edabuilder sign generate-key-pair
```

1. The private key is encrypted with this passphrase. `edabuilder` reads the same environment variable when it signs an image, so keep it set, or set it again, before signing.

This writes the private key to `~/.config/edabuilder/keys/default.key` and the public key to `~/.config/edabuilder/keys/default.pub`. Use `--private-key` and `--public-key` to write them elsewhere, and `--type ed25519` if you prefer an Ed25519 key over the default ECDSA P-256 one. If the key files already exist, `edabuilder` asks before overwriting them; `--force` skips the question.

The public key is what you hand over to the administrators of the EDA clusters that will install your app. The private key is a different story.

/// warning | Handle the private key with care
Anyone holding your private key can sign images in your name, and every cluster that trusts your public key will install them. Store it somewhere safe, back it up, and never commit it to a repository.

If the key leaks, ask the administrators to remove your public key from their `SigningKey` resources right away. If you lose it, you can't sign with it anymore. Either way, you'll have to generate a new key pair, get the new public key trusted, and rebuild and republish your apps with `--sign`.
///

### Signing at build time

Signing happens when the image is pushed. Add the `--sign` flag to the `build-push` command:

```shell
edabuilder build-push --app banners --sign #(1)!
```

1. The default private key is used. Point to another one with `--sign-key <path>`.

`edabuilder` signs the image by its digest, pushes the signature to the registry next to the image, and writes a signature bundle to the `.sign` directory at the root of your project (or next to the manifest, for apps that are not part of a project). For our `banners` app that is `.sign/banners.eda.local.sigstore.json`, named after the app's group.

Then publish as usual. `edabuilder publish` picks up the bundle from the `.sign` directory, stores it as `sigstore.json` next to the manifest in the catalog and records the image digest in the published manifest. At install time, EDA pulls the image by that digest and verifies the signature stored in the registry. If you want to keep the bundles somewhere else, pass the same `--sign-data-dir <dir>` to both `edabuilder build-push` and `edabuilder publish app`.

/// note | Publish from the same place you build
Even without `--sign`, `build-push` writes a bundle to `.sign` containing the image digest. `publish` needs it: without a bundle, the app is published without a digest, and EDA refuses to install it from a registry that has digest verification enabled. `publish` only warns you about a missing bundle when the `.sign` directory exists or `--sign-data-dir` is given, so run `build-push` and `publish` from the same project.
///

### Trusting the key in EDA

The EDA cluster only accepts your signature once an administrator adds your public key to a `SigningKey` resource. How that works is described in [App image signing](../../apps/index.md#app-image-signing).

/// tip
You don't need to sign anything while iterating with [`edabuilder deploy`](#local-development). The development registry it creates is configured to skip signature and digest verification.
///

## Releasing an App

Once you are familiar with the building and publishing processes, you can use the `edabuilder release` command to do them in a single step. The `edabuilder release` command builds and pushes the app image and publishes the manifest to the catalog in a single operation.

```shell
edabuilder release https://github.com/eda-labs/catalog --app banners --sign
```

If you passed `--catalog` to `edabuilder init`, `release` falls back to the catalog in your PROJECT file when you don't pass a URL, so from within your project this is enough:

```shell
edabuilder release --app banners --sign
```

The signature bundle, signed or not, goes straight into the catalog, there's no need for the `.sign` directory in between. Use `--force` to override an existing version, the same way as with `publish`. There is a `--dry-run` flag too, which stages the catalog commit and tag without pushing them, but since it doesn't build the image either, the staged commit won't contain the new image digest or signature.

## Configuring EDA Store with your publishing authority

Just uploading the OCI image and the manifest to a catalog won't make your application available in the EDA Store. You need to make the store aware of any new OCI registries and/or catalogs. The procedure for adding a registry to the EDA store can be found [here](../custom-registry.md#adding-a-registry-to-the-eda-store), the procedure for catalogs can be found [here](../custom-catalog.md#adding-a-catalog-to-the-eda-store).

In our example we are using ghcr.io. If you've deployed EDA through the [Playground](https://github.com/nokia-eda/playground), this registry is already registered with the EDA store, so nothing needs to be done.  

We do need to apply a catalog CR, though. Here is the Catalog CR that adds a catalog named "eda-labs" and references the Git repo we pushed our manifest to in the previous step:

/// tab | Catalog CR

```yaml
--8<-- "docs/development/apps/snippets/catalog.yml"
```

///

/// tab | Apply command

```shell
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/development/apps/snippets/catalog.yml"
EOF
```

///

Once added, the EDA Store will start parsing the referenced Git repo and display them as available applications in the EDA Store.

Since our repo is public, we did not utilize the `authSecretRef` reference; if your Git repo is private, you would need to create a Secret and reference it.

## Local development

The steps outlined above describe the process required to publish an app. This process is repetitive and cumbersome, especially during the development phase. Designed to streamline app iteration, the `edabuilder deploy` command enables a more seamless and efficient development experience. Behind the scenes, `edabuilder` leverages the previously mentioned concepts, dynamically adjusting some of the URIs to use an intermediary development catalog and registry within your EDA cluster.

Concretely, when you want to try out a new version of your code, simply travel down to your app directory (the one containing the `manifest.yaml`), and execute

```shell
edabuilder deploy #(1)!
```

1. This command also has support for the `--app` flag, so technically you don't _have_ to travel down to the app directory.

This does the following:

1. create a development catalog repository in the git server in your EDA cluster
2. create a secret and Catalog CR for the dev catalog to configure the EDA Store
3. create a simple[^2] development registry (Deployment, Service, and Secret and Registry CR to configure the EDA Store)
4. `edabuilder generate` to keep all of your Python models, CRDs, etc. up-to-date
5. rewrite the manifest AppImage URI (in memory) to point to the development registry, then `edabuilder build-push`
6. `edabuilder publish` to the development catalog
7. apply an app install Workflow to (re)install the app and wait for the installation result

When you run `edabuilder deploy` for the first time, step 3 could take a while if the registry image needs to be pulled.

### Bring your own catalog/registry

The `edabuilder deploy` command is customisable through a configuration file, located at `~/.config/edabuilder/config.yaml`[^3]. It allows you to provide multiple custom OCI registries and/or application catalogs (Git repositories) by specifying the URL of the corresponding component and to select the current one to use for the `edabuilder deploy` command.

Consult with the [:material-page-next-outline: deploy targets](edabuilder.md#configuring-deploy-targets) section of the `edabuilder` CLI documentation for more information on how to use this configuration file.

[^1]: When creating your app development project through `edabuilder init`, you can use the `-r | --registry` option to specify your production registry. If you do so, the PROJECT file will store the registry and it will automatically be included in the image URI of any newly created apps' manifests.
[^2]: A basic [CNCF Distribution Registry](https://distribution.github.io/distribution/) image is used here.
[^3]: You can provide a custom location for this file by setting the `EDABUILDER_CONFIG` environment variable.
