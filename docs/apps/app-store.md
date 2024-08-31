# App Store

## Overview

Almost everything in EDA is considered an Application (App), including all the Apps that were installed during the [Getting Started - Install step](../getting-started/install.md#deploying-apps). Apps extend the functionality of EDA by exposing custom resources to the EDA API and MicroPython code that will be executed by EDA whenever such a custom resource is manipulated either by a user or another App.

The EDA App Store is used to manage the Applications inside EDA. It can be accessed through the UI which provides 3 different views:

*All Packages List*
: The initial page when opening the App Store in the UI will show all the packages known to the App Store. Clicking the "All Packages" dropdown at the top allows the selection of "My Packages". Clicking an App from the list will open the App specific page.

*My Packages List*
: This view shows all the installed Apps in the current EDA deployment. Clicking on an App from the list will open the App specific page.

*App Page*
: After clicking on an App in either of the list views, a page will open with specific details from the App. It will show a set of details of the App, and if it has not been installed yet, it will show an install button. If the App has an update available (a new version), an update button will appear. In the future, more details about Apps will become available as the Overview, Documentation and License pages are added to Apps.

## Resources

The App Store relies on three different resources in the EDA environment:

*`Catalog`*
: A catalog is a git repository that contains the manifests of Apps. A manifest contains all the details of an App and will be discussed further in the Development section. Using the manifests of all the `Catalogs` registered in EDA, the App Store can build a list of all available Apps.

*`Registry`*
: While a manifest of an App contains all the details of an App, the actual code and resources of an App are stored in an OCI compliant image. This image needs to be stored in a container registry. This registry must be known to the EDA deployment so the App Store can pull the image and use the data in the image to deploy the App. This information is given to EDA in the form of a `Registry` custom resource.

*`AppInstall`*
: An `AppInstall` is a custom resource that informs the App Store it must install an App in the EDA environment.

## Installing an App

To install an App, you can use the App Store UI, select the App from the list and click the "Install" button. In the background, this will create a `AppInstall` custom resources in the EDA environment. The App Store backend takes this resource and takes the appropriate actions to read the information of the App from its manifest, and make sure the appropriate data is available to EDA, which can include the code of the App, custom resource definitions and more.

You can also install an App using `kubectl` and giving it the correct `AppInstall` custom resource. Here's an example to install the Cloud Connect App:

=== "YAML Resource"
    ```yaml
    --8<-- "docs/connect/resources/connect-appinstall.yaml"
    ```

=== "`kubectl apply` command"
    ```bash
    kubectl apply -f - <<EOF
    --8<-- "docs/connect/resources/connect-appinstall.yaml"
    EOF
    ```

## Uninstalling an App

To uninstall an App, you can use the UI. Open the App page and it will say the currently installed version and to the right, under the general information block, there is a link to "Uninstall package". This will remove the App.

Alternatively, you can use `kubectl` commands to delete the resource. Here's an example to delete the previously created Cloud Connect `AppInstall`.

/// details | Known Limitations
    type: warning
There is no validation yet when uninstalling apps, so make sure all your config is removed before uninstalling.
///

```bash
kubectl delete appinstall connect
```
