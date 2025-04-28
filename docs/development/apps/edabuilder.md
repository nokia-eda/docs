# EDABuilder

`edabuilder` is a standalone CLI tool for performing EDA Store operations such as building and publishing EDA apps or scaffolding the boilerplate code for new apps. The download instructions are mentioned in [Environment setup](setup-env.md) page.

`edabuilder` has the following capabilities:

* `init`: initialise a directory as a project that will hold multiple apps.
* `create app`: scaffold the boilerplate for a new application.
* `create resource`: create a new API resource. These resources are the inputs and outputs of your app, i.e. the main way to interact with your app.
* `create intent`: scaffold boilerplate code for a new config/state intent for one of your API resources, if you hadn't done so already at the time of creating the resource.
* `create version`: create a new API version.
* `build-push`: package an app and host it in a registry[^1].
* `publish`: publish your app to a catalog[^1].
* `generate`: based on your API resources, defined in the Go files under `api/`, generate equivalent python models to be used as an SDK in your intents, CRDs, OpenAPI specs, and keep your manifest up-to-date.
* `deploy`: build, publish and install your application in your EDA cluster, allowing you to test it immediately and iteratively, during development[^1].

/// admonition | Working directories
    type: note
`edabuilder` will run using the current working directory as context. You should run project related commands from the root of your project (`edabuilder init` for example), and application related commands from the root of your applications (`edabuilder create` for example).
///

## Initialising a project

When you run `edabuilder init [<project-name>]`, either the current directory or a new one, named `project-name`, will be initialised for app development. This entails populating a couple of directories (`common/`, `test/`, `utils/`) with common libraries to be imported in the app scripts you will be writing, as well as creating a PROJECT file that keeps track of some project-wide parameters, such as the publishing authority of your apps, your production registry, etc. These parameters can all be passed via arguments to the command. To see the available options, run `edabuilder init -h`.

## Creating an app

Running `edabuilder create app <app-name>` from the root of your project will net you a new directory containing a scaffolded structure for an app with a couple of subdirectories created in it. They all have self-explanatory, categorised, names that suggest where to put app files. Additionally, a `manifest.yaml` file is created. The `edabuilder` tool will maintain parts of this manifest along the way. More on that in the other sections.

## Creating a resource

As stated earlier, resources are the main way to interact with your app. Run `edabuilder create resource MyCoolKind` to scaffold a barebones resource: the "API definition" is the Go file located at `api/<apiversion>/mycoolkind_types.go`.

From this file, the equivalent python models are generated at `api/<apiversion>/pysrc/mycoolkind.py`, as well as a CRD under `crds/` and the OpenAPI spec under `openapiv3/`. Your manifest is automatically kept up-to-date with this change, meaning this new `pysrc` and the CRD are ready to be packaged in your app already.

## Creating an intent

In and of itself, a resource consisting of only a CRD is not very useful. You likely intend to trigger some code when an instance of your resource is created, updated, or deleted. We call the scripts containing the code for these trigger events "intents".

Two types of intents exist: _config intents_ and _state intents_. The config intent is really meant for direct interaction: A user creates a resource with some desired parameters, and the intent code is subsequently triggered, performing some action in the cluster. A resource bundled with a config intent is called a "config resource".

The state intent will in most cases be more of a watcher: Based on some observed state of the cluster, the code e.g. performs some translations or exports some metrics. A resource bundled with a state intent is called a "state resource".

Since intents and resources are such tightly coupled concepts, intent code of either type can be scaffolded at the time of creating a resource, with the `--scaffold-config` or `--scaffold-state` options. If you forgot to scaffold the intent boilerplate at resource creation time, you can add it after the fact by using the `edabuilder create intent` subcommand.

After creating an intent (or creating a resource with one of the intent scaffolding options for that matter), your manifest is kept up-to-date with the appropriate scripts and trigger events.

## Creating a Version

Through `edabuilder create version` you can create a new API version, e.g. when you are introducing backwards compatibility breaking changes over the lifetime of your app. Here you have the option to carry over API resources from a previous version. If you choose to do so, a boilerplate migration script will be scaffolded per resource that is present in your old API version. The API version in the manifest specification is automatically updated to the new version, and conversion scripts are tracked in the manifest as well.

## Generating your app

`edabuilder generate` is an idempotent command designed to keep any generated code in your app up-to-date. It uses your API resources as input to generate a python SDK under `api/<apiversion>/pysrc`, CRDs and OpenAPI. It also ensures your manifest is up-to-date.

Many of the other subcommands use `generate` under the hood, so it's likely you won't have to run it explicitly very often.

[^1]: For more information packaging, publishing and iteratively deploying apps, refer to [Build and Publish](build-publish.md)
