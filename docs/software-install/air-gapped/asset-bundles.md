# Asset bundles

Container images, Git repositories, and file artifacts used by the EDA platform are grouped into *asset bundles*. An asset bundle is a YAML file that defines a group of related assets used by the EDA platform.  
For example, a bundle may define the EDA core components or standard applications for a specific version.

```yaml title="Example air-gap bundle for EDA v25.12.4 core components"
version: 1.0.0
name: core-25.12.4
assets:
  registries:
    - name: ghcr.io
      images:
        - name: nokia-eda/core/api-server
          tags:
            - 25.12.4
        - name: nokia-eda/core/appstore-server
          tags:
            - 25.12.4
        - name: nokia-eda/core/appstore-flow
          tags:
            - 25.12.4
# snipped for brevity
  repos:
    - remote: https://github.com/nokia-eda/playground.git
      name: playground
    - remote: https://github.com/nokia-eda/kpt.git
      name: kpt
    - remote: https://github.com/nokia-eda/catalog.git
      name: catalog
```

Asset bundles play a crucial role in the air-gapped installation process as they allow you to choose which applications, resources and artifacts to include in the air-gapped environment.  
You will find a [set of standard asset bundles](https://github.com/nokia-eda/edaadm/tree/main/bundles) in the `edaadm` repository for EDA's core components, applications and auxiliary tools and resources.

> As explained in the [air-gapped installation overview](index.md), the assets referenced in the asset bundles are downloaded to the Installer host in the public environment first, and then uploaded to the Assets Host[^1] in the air-gapped environment.
>
> You need to select the asset bundles to include in the air-gapped environment before proceeding with the [downloading the assets](downloading-the-assets.md) step.

## Bundle lists

While it is possible to deal with the individual bundles directly, an easier way is to work with the bundle lists that group several bundles together to form a coherent set of assets:

* Default bundle list - Bundles that must be included in the air-gapped environment.
* Sim bundles - bundles containing the container images for simulating network elements (like SR Linux container image).
* Exporter app bundles - bundles that contain EDA applications that export data to external systems (like Prometheus, Kafka, etc.).
* Importer app bundles - bundles that contain EDA applications that import data from external systems (like Kafka, NATS, etc.).
* Notification app bundles - bundles that contain applications that send notifications to external systems (like email, Slack, etc.).
* Connect app bundles - bundles that contain EDA Cloud Connect applications and plugins.
* User bundles - bundles created by the user for custom applications and resources.

/// warning

1. The Default bundle list is mandatory to include in the air-gapped environment. Everything else is optional and can be included or excluded based on the user's needs.
2. Not all bundles are categorized into the lists above. Individual application bundles like `eda-bundle-gitlab-x-y-z`, etc. are not included in any of the bundle lists and should be downloaded individually if these applications are needed in the air-gapped environment.  
    To list all available bundles, use the `make -C bundles ls-all-bundles` command.
///

## Listing the bundle lists

To list the bundles within a list:

/// html | div.steps

1. Ensure you have [cloned the `edaadm`](../preparing-for-installation.md#download-edaadm-tools) repository and changed into its directory.

    ```bash title="changing into edaadm repository directory"
    cd path/to/edaadm
    ```

2. Set the desired Nokia EDA version.

    Set the `EDA_CORE_VERSION` and `EDA_APPS_VERSION` environment variables in your shell to the target Nokia EDA release version. Otherwise, the latest version is assumed.

    ```bash
    export EDA_CORE_VERSION=-{{ eda_version }}-
    export EDA_APPS_VERSION=-{{ eda_version }}-
    ```

3. List the bundles within the list.

    ```bash title="listing the bundles within the 'default' list"
    make -C bundles/ ls-default-bundles
    ```

    <div class="embed-result">
    ```
    --> INFO: List of goals: ls-default-bundles
    --> Default eda core version to load/save: EDA_CORE_VERSION=26.4.1, EDA_APPS_VERSION=26.4.1
    --> Default list:
        eda-bundle-apps-26-4-1
        eda-bundle-core-26-4-1
        eda-bundle-metallb-0-13-7
        eda-bundle-storage-2-0-0
        eda-bundle-talos-1-11-5
        eda-bundle-tools-2-0-0
    ```
    </div>

    As the output shows, the default bundle list contains the EDA core and EDA application bundles, along with the auxiliary bundles for the Talos Kubernetes cluster.

    To list the bundles within the other lists, use the following targets that have the self-explanatory names matching the list names:

    * `ls-exporter-app-bundles`
    * `ls-importer-app-bundles`
    * `ls-notification-app-bundles`
    * `ls-connect-bundles`
    * `ls-sim-bundles`
    * `ls-user-bundles`

4. List all available bundles.

    Not all bundles are categorized into the lists above. Some application bundles like `eda-bundle-gitlab-x-y-z`, etc. are not included in any of the bundle lists and should be downloaded individually if these applications are needed in the air-gapped environment.

    To list all available bundles, use the `ls-all-bundles` target which will list all bundles in the `bundles` directory.

    ```
    make -C bundles ls-all-bundles
    make: Entering directory '/path/to/edaadm/bundles'
    --> INFO: List of goals: ls-all-bundles
    --> List of all bundles:
    eda-assets-image-cache-2-0-0
    ... (snipped for brevity)
    ```

///

## User bundles

The bundles available in the [edaadm repository](https://github.com/nokia-eda/edaadm/tree/main/bundles) are created for Nokia-provided assets. If you need to include additional assets in the air-gapped environment (like custom applications or resources), you need to create a bundle including these assets; we call this type of bundle a *user bundle*.

> A user bundle looks exactly like the standard bundle, but it lists the user-provided assets instead of the Nokia-provided assets.

The following process describes how to create a user bundle for custom applications or resources:

/// html | div.steps

1. Create a new bundle YAML file in the `user-bundles` directory.

    The empty `user-bundles` directory is located in the `bundles` directory of the cloned `edaadm` repository. This directory is used to store the user-provided bundles.

    The following example creates a bundle for the custom [Bottom Toolbar application](https://github.com/eda-labs/catalog/tree/apps/bottom-toolbar.eda.labs/v0.1.0/apps/bottom-toolbar.eda.labs) that is available in the [EDA Labs catalog](https://github.com/eda-labs/catalog/) and is not part of any standard application bundle.

    ```yaml title="user-bundles/bottomtoolbar.yaml"
    version: 1.0.0
    name: bottom-toolbar
    assets:
      registries:
        - name: ghcr.io
          # tlsVerify: false
          # auth:
          #  username: base64-encoded-username
          #  password: base64-encoded-password
          images:
            - name: eda-labs/bottom-toolbar
              tags:
                - v0.1.0
      repos:
        - remote: https://github.com/eda-labs/catalog
          name: eda-labs-catalog
          # tlsVerify: false
          # auth:
          #   username: base64-encoded-username
          #   password: base64-encoded-password
    ```

    As shown in the example above, the bundle file contains a registry asset and a repository asset. The registry asset pulls the public container image from the `ghcr.io` registry. If the container image is not public, configure the bundle to pull it from a private registry by setting the `auth` property.

    The repository asset pulls the Git repository from the `https://github.com/eda-labs/catalog` repository. In case the repository is not public, you can configure the bundle to pull it from a private repository by setting the `auth` property.

    The bundle can also contain arbitrary artifacts that will be served by the web server in the air-gapped environment. To add an artifact, add an `artifacts` section to the bundle file and specify each artifact by name and source URL.

    ```yaml
    assets:
      artifacts:
        - name: custom-artifact.zip
          url: https://github.com/myorg/myrepo/releases/download/myrelease/custom-artifact.zip
          # tlsVerify: true
          # auth:
          #   username: <base64 username>
          #   password: <base64 password/token>
    ```

    The artifact will be served at the URL `https://<ASSET_HOST>/artifacts/<artifact.name>`.

2. Add custom repositories to the setters file. <span id="custom-repositories"></span>

    Custom repositories that were added to the user bundle in step 1 need to be created in the Git server. If the Git server is not part of the Assets Host, create the repositories yourself before loading the user bundle.

    If the Git server is provided as part of the Assets Host, add the repositories to `kpt/config/kpt-setters.yaml` in the cloned `edaadm` repository using the `USER_REPOS_TO_CREATE` variable. The variable is already present with an empty default value.

    ```yaml title="kpt-setters.yaml example"
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: apply-setters-fn-config
    data:
      USER_REPOS_TO_CREATE: "eda-labs-catalog" #(1)!
      # other variables omitted for brevity
    ```

    1. Creates the repository named `eda-labs-catalog` in the Git server

3. List the user bundles.

    User bundles are automatically recognized by the `make` command when using the `ls-user-bundles` target.

    ```
    make -C bundles ls-user-bundles
    make: Entering directory '/path/to/edaadm/bundles'
    --> INFO: List of goals: ls-user-bundles
    --> List of user bundles:
        user-bottomtoolbar
    make: Leaving directory '/path/to/edaadm/bundles'
    ```

    The user bundle name is prefixed with `user-` to distinguish it from the standard bundles.

///

After identifying the bundles to include in the air-gapped environment, the next step is to [download the selected asset bundles](downloading-the-assets.md) that will be used to deploy the EDA platform in the air-gapped environment.

[:octicons-arrow-right-24: Download the assets](downloading-the-assets.md)

[^1]: An Assets Host can be provided by Nokia in the form of the EDA Assets VM, or by the user in the form of an existing service.
