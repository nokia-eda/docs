# Application Components

As was covered in the [Project Layout](project-layout.md) section, each app has its own directory in the EDA project. Taking the [quickstart app](quick-start.md) as a starting point, your project directory will contain the `banners` directory that has the following structure.

```title="contents of the banners app directory"
.
├── api
├── crds
├── docs
├── examples
├── intents
├── openapiv3
├── test
├── ui
├── workflows
├── go.mod
├── go.sum
└── manifest.yaml
```

## Application API

To define application APIs, edabuilder uses the same pattern as kubebuilder, i.e. the API is defined by the Go files in the **`api`** directory.

Based on the source API types defined in `.go` files, the `edabuilder generate` creates the following components:

* Python models equivalent to your API structs defined in Go; stored in **`api/pysrc`** directory.
* Custom Resource Definitions (CRDs) in **`crds`** directory.
* OpenAPI schema files, which describe extensions to the schema of both Kubernetes and EDA and is located in **`openapiv3`** directory.

The [`generate`](edabuilder.md#generating-your-app) command can be run separately, but many subcommands (like `deploy` and `release`) start off by running `edabuilder generate` to make sure your app state is always up-to-date.

## Intents

[Intents (aka Scripts)](scripts/index.md), are executable Python code that is triggered by the changes made to the respective resources. These scripts are used to implement the logic of the application for non-Kubernetes-controller apps.

Intents are what most developers will write when building new applications on EDA or extending the existing apps provided by Nokia.

> Check the [Banner application walkthrough](scripts/banner-script.md) to see what makes up a simple intent-based application.

## Dashboards

The developers can create and bundle custom UI dashboards, adding observability and monitoring capabilities for their apps. The dashboards are defined using JSON files and can be found in the **`ui`** directory of the app.

## Workflows

Workflows are the "run to completion" applications that can be triggered by the resources, users or API clients. Workflows are typically used to implement the logic of the application for one-shot operations - things like upgrades, network pings, route information collection or other operations that are not perpetually ongoing.

Workflows are typically written in Go, but can be written in any language for which EDA Development Kit (EDK) support is available.

## Documentation

Each application contains its own documentation in the **`docs`** directory. The documentation is written in Markdown and includes the overview of the application, its components, license info, usage examples and documentation for each resource defined by the application.

## Manifest

The **`manifest.yaml`** file defines every aspect of the application packaging, including the application metadata, its components, dependencies, and other relevant information. EDA Store uses this manifest file to understand how to install, deploy and manage the application within an EDA platform.

Whenever a user adds a new application component with the `edabuilder` CLI, the manifest file is automatically updated to include the new components, therefore users typically should not need to edit this file too often manually.

## Other resources

Some applications may include more specialized components, but these are less common and the majority of applications will consist of the components described above.
