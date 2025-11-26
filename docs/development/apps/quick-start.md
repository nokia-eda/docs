# Quick Start

[An application in EDA](index.md) can contain many things and do way more than just generating node configurations from the abstracted input. But, still, the most common thing you're going to want an app for is to generate some configuration for a target, and potentially publishing some state relating to that configuration and/or target.

To fast track this common case an example demonstrating how to build an app is baked into the `edabuilder` CLI tool. In this quickstart we'll use the baked in example of an app that configures the login banner on a device and walk you through the steps required to build the app from scratch, iterate on it during the development cycle, and then publish it to a custom Catalog so you can share it with others.

Without further ado, let's get started by going into a directory where we want to create our project.

/// html | div.steps

1. **Create a new project**

    We begin with initializing a new project that will contain our demo application that will configure the login banner on a device.

    To create a project, supply the application vendor[^1] and the project name as an argument to the `edabuilder init` command:

    ```shell
    edabuilder init --vendor community example && cd example
    ```

    You find yourself in the `example` directory that we just initialized with some top-level project files and directories scaffolded out for you.

2. **Create a Python virtual environment**

    Now is a good time to create a Python virtual environment that we will use to get autocompletion, code formatting and linting for our application code.

    If you have `uv` installed like was suggested in the [setting the dev environment](setup-env.md) section, you can just run:

    ```shell
    uv sync
    ```

    <small>You are free to use any other means to create a venv.</small>

3. **Create an app**

    From the `./example` project directory, we proceed with creating a directory that will contain our EDA application.

    An important thing to note is that an application in EDA is **a group** that contains one or more of the following resources:

    - config and/or state intents that declaratively describe the desired configuration and state of a target.
    - operational workflows associated with this app
    - dashboards

    Let's call our application - `banners` - since we will scaffold an app that provisions a login banner on the network devices.

    ```shell
    edabuilder create app banners #(1)!
    ```

    1. //// warning
    If your application name is more than one word, the name must be in a kebab-case format.

    In this example, the app name is simply `banners`, but if you wanted to name it "my banners", then you should've named it `my-banners`.
    ////

    This step should generate the `banners` directory where you will find the scaffolded layout of the application with no particular logic implemented yet.

4. **Create a resource**

    At this stage, you would start defining the API of your app, typing code for your configuration and state intents, crafting alarms and creating the workflows and dashboards.  
    But for the sake of this quickstart, we need something quick and easy; you will get to building real apps later once you've got the hang of it.

    We have baked in the example `Banner` resource inside the `edabuilder` CLI tool to demonstrate the app building workflow using a real example, without typing any code.

    //// admonition | custom resources, resources, and intents
        type: subtle-note
    We often use the terms "intent" and "custom resource" or "resource" interchangeably. They all mean the same thing: a declarative definition of the EDA resource which can be, for example, a configuration or state object or a workflow[^2].
    ////

    With the `edabuilder create --app banners resource Banner` command, we will create the Banner resource in the `banners` app directory, and when used with the `-d | --scaffold-demo` flag, we tell edabuilder to output the demo scaffolding for the configuration and state scripts for the Banner resource.

    ```shell
    edabuilder create --app banners resource Banner -d #(1)!
    ```

    1. //// warning
       The resource name must be in a CamelCase format.
      ////

    As a result of this command, you will find

    - the API specification for the Banner and BannerState custom resources created in the `banners/api/v1alpha1` directory[^3]
    - scaffolded configuration and state resources (aka intents) with the corresponding scripts in the `intents/banner` and `intents/bannerstate` directories. Without the demo `-d` flag the resources are created without the scripts, as the developers add them manually.

    We leave the app logic implementation details for a later deep dive. All we need to know for now, that an application that is capable of configuring banner message on the supported Network OSes has been scaffolded and we can deploy it onto the EDA cluster to see it in action.

5. **Deploy the app**

    During the app development you would want to quickly test the changes you made to the app by deploying it to EDA cluster. Edabuilder comes with a one-shot command to do just that:

    ```shell
    edabuilder deploy --app banners
    ```

    The `deploy` command will package app components in an OCI container image, push it to the container registry deployed for you in the EDA cluster and install the app.

    //// admonition | `deploy` command requirements
        type: subtle-note
    The `kubectl` should be using the context that points to the EDA cluster for the operation to succeed.
    ////

6. **Try the app**

    After deploying the development version of the app directly to the EDA cluster, you can try it out by creating an instance of the `Banner` resource via any of the EDA interfaces. Here are two of them:

    //// tab | EDA UI
    In the EDA UI you should see a new group menu named **Banner** appear in the list of the resources:

    ![pic](https://github.com/user-attachments/assets/12db0509-7fd4-4d70-b124-e65f41d7de31)

    Selecting the **Banner** menu will take you to the list of instances of the `Banner` resource, where you can create a new instance of the resource and commit this transaction.
    ////

    //// tab | Kubernetes API/kubectl
    To leverage the Kubernetes API one can create a custom resource in the YAML format like shown below:

    Resource:

    ```yaml
    --8<-- "docs/development/apps/snippets/banner.yml"
    ```

    Apply:

    ```shell
    cat << 'EOF' | kubectl apply -f -
    --8<-- "docs/development/apps/snippets/banner.yml"
    EOF
    ```

    ////

    Regardless of the interface you choose, the result of your actions should be a new instance of the `Banner` resource in the EDA cluster and the appropriate login banner configured on the targets matching your selection.

///

## What just happened?

Quite a lot! Here's a breakdown of what you just did:

1. You initialized a new project.
2. You created a new app.
3. You created a new resource - Banner - with the generated scripts for the Banner and BannerState intents.
4. You generated code-generated artifacts (OpenAPI schemas, CRDs, etc.) for your app.
5. You deployed your app to your EDA cluster.
6. You created an instance of your new resource via Kubernetes API or EDA UI.
7. And observed the results of your app in action by logging into the SR Linux CLI and seeing a new login banner in effect.

## Where to from here?

First, get to know the project layout and the role of each directory and files they contain in the [Project Layout](project-layout.md) section.

Next, dive into the application components to learn what makes up an EDA app in the [Components](components.md) section.

After that, you are ready to learn how the demo Banner app works. How it selects the nodes, generates the config snippets, creates resources in EDA cluster and so on. This is covered in the [Banner script deep dive](scripts/banner-script.md) section.

[^1]: A vendor is the publishing authority of your app. It can be an arbitrary string, but typically it matches your company name, personal name or a community name.
[^2]: The actual runtime used in EDA to run those scripts is MicroPython, but we will dive into these details in a later sections.
[^3]: In the `banner_api_types.go` and `bannerstate_api_types.go` files accordingly. The path is provided from the root of the project's repository.
