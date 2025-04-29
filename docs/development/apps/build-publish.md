# Build and Publish

We take pride in EDA's extensibility through applications, and one of the key aspects of this extensibility is the ease of build, publish, share and install workflows.  
EDA uses standard, well-known and established toolchains for this purpose:

- OCI image as a packaging format for the application
- Container registry as a storage for the application images
- Git for catalog and application discovery and sharing

From the distribution point of view, EDA app consists of two distinct artifacts that are coupled together:

1. An app manifest file that describes the app components, including the URL/tag of the app image
2. An OCI image that contains the app components

This structure can be visualized as:

-{{diagram(url='nokia-eda/docs/diagrams/apps-dev',page=1, title='', zoom=1.5)}}-

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
  image: /banners:v0.0.0
```

As an app owner, you set the image value to an image URI that points to the registry where you want the image to be published in the app manifest file[^1]. As we are using ghcr.io for this example, we could set the image value to e.g.:

```diff
- image: /banners:v0.0.0
+ image: ghcr.io/eda-labs/banners:v2.1.0
```

Now, `edabuilder build-push` has everything it needs - an image URI and the credentials for the container registry the image points to. Simply point the command towards your manifest and its build context[^2], like so:

```shell title="run from the project's directory"
edabuilder build-push --app manifest=banners/manifest.yaml,context=. #(1)!
```

1. Note that the `banners` directory in the `--app manifest=banners/...` argument is the directory containing the application manifest. If you named your app differently you will have to change this value accordingly.

A successful `build-push` action ends by prompting you with "Successfully pushed OCI Image". Your app image should now show up in the registry. If you intend to have your image accessible without authentication, make your image public using the interface of your registry provider.

## Publishing an App

The second pillar of an app is its manifest file[^3], which we still need to publish to a catalog[^4] of our choice.

The first thing you need to ensure is that you have a git repository created that you intend to use as an App Catalog for your EDA applications. In this example, we will be using our [eda-labs/catalog](https://github.com/eda-labs/catalog) repository that we use for our community-oriented applications.

Start off by logging into the Git provider of your choice to make sure you are authorized to push the manifest to the repository:

```shell
edabuilder login git -u hellt -p $(gh auth token) https://github.com/eda-labs/catalog #(1)!
```

1. Change the user, password and repository URL to the appropriate values for your repository.

After a successful login we can publish our application manifest to the repository:

```shell
edabuilder publish https://github.com/eda-labs/catalog \
--app manifest=banners/manifest.yaml
```

A successful publish of the manifest should result in the following output:

```
Publishing to branch 'main'
No app version given, using the manifest image tag as app version: 
Staging `banners` at version `v2.1.0`
Successfully published Apps
```

Now you should see the application manifest published in your Git repository following the `vendors/<vendor-name>/apps/<app-name>` path:

![img](https://gitlab.com/rdodin/pics/-/wikis/uploads/8e2d9d36232338bb3eb18a22065a7671/CleanShot_2025-03-29_at_14.14.59_2x.png)

The app version will be matching the version from the image tag found in the manifest, unless the version is provided inline with the `--app` argument.

To republish an app, i.e. override an existing version, add `--force` flag to the command.

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

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

## Local development

The three sections above describe what you need to do when you're ready to publish an app. It's a bit of manual work, and having to do this over and over again while your app is still under development is cumbersome. That is where `edabuilder deploy` comes in. This command is designed to help you iterate on your app in a frictionless manner during development. Under the hood, it makes use of the concepts described above, but `edabuilder` juggles around some of the URIs in order to use an intermediary development catalog and registry inside of your EDA cluster.

Concretely, when you want to try out a new version of your code, simply travel down to your app directory (the one containing the `manifest.yaml`), and execute

```shell
edabuilder deploy #(1)!
```

1. This command also has support for the `--app` flag, so technically you don't _have_ to travel down to the app directory.

This does the following:

1. create a development catalog repository in the gogs server in your EDA cluster
2. create a secret and Catalog CR for the dev catalog to configure the EDA Store
3. create a simple[^5] development registry (Deployment, Service, and Secret and Registry CR to configure the EDA Store)
4. `edabuilder generate` to keep all of your Python models, CRDs, etc. up-to-date
5. rewrite the manifest AppImage URI (in memory) to point to the development registry, then `edabuilder build-push`
6. `edabuilder publish` to the development catalog
7. apply an app install Workflow to (re)install the app (anew) and wait for the installation result

When you run `edabuilder deploy` for the first time, steps 1 through 3 could take a while if the registry image needs to be pulled.

[^1]: When creating your app development project through `edabuilder init`, you have the option of specifying your production registry. If you do so, the PROJECT file will store the registry and it will automatically be included in the image URI of any newly created apps' manifests.
[^2]: For more information on the `--app` flag, and build context in general, refer to [terminology](terminology.md#application-build-context).
[^3]: For more information on manifests, refer to [terminology](terminology.md#manifest)
[^4]: For more information on catalogs, refer to [terminology](terminology.md#catalog)
[^5]: A basic [CNCF Distribution Registry](https://distribution.github.io/distribution/) image is used here.
