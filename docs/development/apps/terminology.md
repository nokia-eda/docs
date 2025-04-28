# Terminology and concepts

Like any development environment, EDA has its own set of terminology and concepts that are useful to understand in order to build an app.

## Projects

Your initial starting point for building an app is a project. A project is a directory containing one or more app directories, and a collection of shared libraries that are used/lifecycled together for all apps in the project. You likely only need one project for your organization, but you may have more if you have different teams or different use cases. As a reference, Nokia has a single project for all of its apps.

## Applications

Within a project, you have one or more applications. Your packaging/distribution boundary is at the application level, NOT the project level. This means that you can have multiple applications in a single project, and each application can be versioned and distributed independently, all sharing a common set of libraries.

## Manifest

Like a packing slip that describes the contents of a parcel, the application manifest describes what the application consists of and where to find all of its contents.

## Application build context

The build context of an app is a location on your local file system. Combined with the build context, any relative path in an app's manifest should resolve to an actual file location.

## Resources

Resources are the core building blocks of an app. They are the inputs and outputs of your app, and are the primary way that users interact with your app. Resources can be of many types, but the most common are:

## Catalog

A catalog can be any git repository that is structured in a way that the EDA store can parse it for published apps. Using `edabuilder publish` with a git repository makes sure it is always structured as such.

## Registry

A registry is a location where apps are stored. In EDA, the apps are stored as OCI artifacts (container images) and therefore any OCI-compliant registry can be used as a registry.

## EDA Store

EDA Store is software component within EDA core that manages the lifecycle of the EDA applications. Through EDA Store users add/delete apps, and manage associated catalogs and registries.
