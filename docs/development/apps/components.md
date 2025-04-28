# Application Components

As was covered in the [Project Layout](project-layout.md) section, each app has its own directory in the EDA project. Taking the [quickstart app](quick-start.md) as a starting point, your project directory will contain the `banners` directory that hosts everything an application might feature.

```title="contents of the banners app directory"
.
├── api
├── crds
├── intents
├── openapiv3
├── rbac
├── workflows
├── test
├── ui
├── go.mod
├── go.sum
├── LICENSE
├── manifest.yaml
└── README.md
```

The components that can be found in an application bundle are:

* **Application API**:
    * To define application APIs, edabuilder uses the same pattern as kubebuilder, i.e. the API is defined by the Go files in the `api/` directory.
    * Based on the source API types defined in `.go` files, `edabuilder generate` manages the following components:
      * Python models equivalent to your API structs defined in Go
      * Custom Resource Definitions (CRDs)
      * OpenAPI schema files, which describe extensions to the schema of both Kubernetes and EDA  

      Many subcommands start off by running `edabuilder generate` to make sure your app state is always up-to-date.
* **Intents** aka Scripts, which are executable code that can be run in the context of a resource. These are typically used to implement the logic of the application for non-Kubernetes-controller apps.
* **Views**, which are UI dashboards. This is typically used to bundle dashboards alongside the resources within the application.
<!-- * Schemas, which extend the schema of EDB. EDB is the database that EDA uses to store its state, and are separate from RDs (which are a subset of the schema of EDB). This is typically used if an application provides a state script that needs to write back to the database. Even if your application does this, schemas are optional and simply help presentation of data in the UI. -->
* **Workflows**, which are run to completion logic that can be triggered by resources. This is typically used to implement the logic of the application for one-shot operations - things like upgrades or other operations that are not ongoing.
* **RBAC objects** - optional rbac roles that an application might require.
* **Bootstrap resources**, which are similar to resources, but are immutable - they're intended primarily as a means for bootstrapping new `Namespace` resources in EDA. It is typically to see things like allocation pools or default resources in this category.

A simple application may contain only one of the above, while a more complex application may contain all of them.
