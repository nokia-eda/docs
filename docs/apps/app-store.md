# EDA Store

## Overview

Almost everything in EDA is considered an Application (App), including all the Apps that were installed during the [Getting Started - Install step](../getting-started/installation-process.md#apps). Apps extend the functionality of EDA by exposing custom resources to the EDA API and MicroPython code that will be executed by EDA whenever such a custom resource is manipulated either by a user or another App.

The EDA Store is used to manage the Applications inside EDA. It can be accessed through the UI which provides 3 different views:

*All Packages List*
: The initial page when opening the EDA Store in the UI will show all the packages known to the EDA Store. Clicking the "All Packages" dropdown at the top allows the selection of "My Packages". Clicking an App from the list will open the App specific page.

*My Packages List*
: This view shows all the installed Apps in the current EDA deployment. Clicking on an App from the list will open the App specific page.

*App Page*
: After clicking on an App in either of the list views, a page will open with specific details from the App. It will show a set of details of the App, and if it has not been installed yet, it will show an install button. If the App has an update available (a new version), an update button will appear. In the future, more details about Apps will become available as the Overview, Documentation and License pages are added to Apps.

## Resources

The EDA Store relies on two different resources in the EDA environment:

*`Catalog`*
: A catalog is a git repository that contains the manifests of Apps. A manifest contains all the details of an App and will be discussed further in the Development section. Using the manifests of all the `Catalogs` registered in EDA, the EDA Store can build a list of all available Apps.

*`Registry`*
: While a manifest of an App contains all the details of an App, the actual code and resources of an App are stored in an OCI compliant image. This image needs to be stored in a container registry. This registry must be known to the EDA deployment so the EDA Store can pull the image and use the data in the image to deploy the App. This information is given to EDA in the form of a `Registry` custom resource.

## Installing an App

To install an App, you can use the EDA Store UI, select the App from the list and click the "Install" button. In the background, this will create a `Workflow` custom resource in the EDA environment. The EDA Store backend takes this resource and takes the appropriate actions to read the information of the App from its manifest, and make sure the appropriate data is available to EDA, which can include the code of the App, custom resource definitions and more.

You can also install an App using `kubectl` and giving it the correct `Workflow` custom resource. Here's an example to install the Cloud Connect App:

=== "YAML Resource"
    ```yaml
    --8<-- "docs/apps/store/install-example.yaml"
    ```

=== "`kubectl apply` command"
    ```bash
    kubectl apply -f - <<EOF
    --8<-- "docs/apps/store/install-example.yaml"
    EOF
    ```

The status of the Workflow shows the progress of the installation. This `Workflow` resource initiates an app installer job. Once installed, a `Manifest` resource will be created and the Workflow is done (and the object may be deleted). To see the installed apps using `kubectl`, you can check their manifests:

```bash
kubectl get manifests -n eda-system
```

## Uninstalling an App

To uninstall an App, you can use the UI. Open the App page, and it will say the currently installed version and to the right, under the general information block, there is a link to "Uninstall package". This will remove the App.

Alternatively, you can use `kubectl` commands to delete an app. Creating a new Workflow with a `delete` operation, will start uninstalling an application.
Here's an example to delete the previously created Cloud Connect App.

/// details | Known Limitations
    type: warning
There is no validation yet when uninstalling apps, so make sure all your config is removed before uninstalling.
///

=== "YAML Resource"
    ```yaml
    --8<-- "docs/apps/store/delete-example.yaml"
    ```

=== "`kubectl apply` command"
    ```bash
    kubectl apply -f - <<EOF
    --8<-- "docs/apps/store/delete-example.yaml"
    EOF
    ```

Note the difference between installing and uninstalling by the `operation` field. Changing an already existing Workflow by updating its operation field from `install` to `delete` will not trigger a new (un)install job. A new Workflow needs to be created instead.

/// details | Uninstalling apps with dependencies

Trying to delete an app that is required by another app will not be permitted to prevent the second app from malfunctioning.
In this case, the EDA store might return an error message saying that the to-be-deleted app is not present. This is a known bug and a more meaningful error message is planned for an upcoming release.

///

## App Requirements

App requirement (or app dependency) management plays an important part to make sure that the whole system after (un)installing apps still functions properly.
In EDA, apps may expect some resources to exist that are provided by other applications. These need to be installed before (or at the same time as) the dependent app. Deletion of apps may also be blocked if it breaks the requirement of another app.
The requirement of an app is defined in its manifest specification, which contains the app and a version constraint (e.g. `v3.0.*`, `>=v3.0.0`).
The EDA Store makes sure that all the app requirements stay valid at all times to prevent invalid app version configurations.

When trying to install an app through the UI, the EDA Store will check if other apps needs to be installed or updated alongside it.
You will then be prompted to approve that the EDA store needs to install or upgrade these additional applications.

/// details | Requirement modes using CLI

Through the CLI, there is currently only one requirement mode that is the default on what the EDA store is allowed to do:

*`strict`*: The app installer only verifies that the resulting installed apps will be satisfied w.r.t. their requirements.
If invalid, the installation will be aborted with an error message denoting what requirement is missing.

Other modes are planned in future releases.

To specify a mode, pass the `autoProcessRequirements` field to the workflow spec. See the app installation example for how this is filled in.

///
