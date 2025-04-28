# Setting up the dev environment

Before you start building an app, you'll need to prepare the development environment. This guide assumes you have EDA installed already and if you don't, you can quickly spin one up by following the [Try EDA](../../getting-started/try-eda.md) guide.

Your primary tools when developing an app:

* `edabuilder` for scaffolding, building, and publishing your app.
* `go` sdk for authoring the API of your custom resources.
* `python` runtime for getting syntax highlighting and IDE support when writing intents <small>optional</small>.
* `kubectl` for creating resources.
* `edactl` for verifying installation workflows and debugging.

These tools are available for all major OSes and architectures, so you can develop on your preferred platform, no matter where you are.

/// tab | `edabuilder`
`edabuilder` is a CLI tool that helps to scaffold a new EDA app, build the container for it and then publish the application to the catalog. The CLI can be downloaded from the [GitHub repository][edabuilder-repo-release] as well as from the `eda-toolbox`[^1] Pod.

[edabuilder-repo-release]: https://github.com/nokia-eda/edabuilder/releases

//// tab | Download from GitHub
Download the latest `edabuilder` binary from the [GitHub repository][edabuilder-repo-release] directly, or leverage the downloader script that comes with the [EDA Playground](https://github.com/nokia-eda/playground):

```bash title="Run in the EDA Playground repository"
make download-edabuilder
```

This will download the `edabuilder` binary to the `./tools` directory in the EDA Playground repository. For convenience, you can move the binary somewhere to your `$PATH`.
////
//// tab | Download from eda-toolbox

If you're developing on a linux/amd64 machine, you can get the `edabuilder` binary from the `eda-toolbox` Pod:

```shell
TOOLBOX_POD=$(kubectl get -n eda-system pod -l eda.nokia.com/app=eda-toolbox \
  -o jsonpath='{.items[0].metadata.name}')
kubectl -n eda-system \
cp ${TOOLBOX_POD}:/eda/tools/edabuilder /usr/local/bin/edabuilder
sudo chmod +x /usr/local/bin/edabuilder
```

////
///

/// tab | `go`
We will define the API of our declarative apps exactly like in Kubernetes - by crafting the Go files that extend the API of the EDA core. For this, we need a Go SDK.

Install Go SDK by following [the upstream installation instructions](https://go.dev/doc/install).

The minimum Go version required is `1.22`.
///

/// tab | `python`
While being optional, we recommend installing the Python runtime and initialize a virtual environment for development.

If you already have a Python environment dialed in, you can skip this step, but if not, then the easiest way to get Python on your dev machine is by installing [uv](https://docs.astral.sh/uv/getting-started/installation/) - a modern multiplatform Python distribution and package manager.
///

/// tab | `kubectl`
[`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) is the Kubernetes command-line tool. During development, you may find it easier to create resources with it, rather than venturing into the EDA UI.

If you have completed the Try EDA step, then kubectl has already been downloaded for you and you can just copy it out to a permanent location in your `$PATH`.
///

/// tab | `edactl`
`edactl` will help you query the EDA cluster and debug your application. You don't even need to download it directly, you can use an alias to run it from within the EDA cluster as explained in the [CLI Tools](../../user-guide/using-the-clis.md#edactl) guide.
///

And now with these tools in your toolchest, you've got everything you need to start building your first app! Choose your preferred path, would you want to put the code to the compiler right away or want to beef up your knowledge on the matter?

<div class="grid cards" markdown>

* :material-hammer-screwdriver:{ .middle } __Quick start__

    ---

    Prefer to dive into a hands on example?

    [:octicons-arrow-right-24: Create your first app](quick-start.md)

* :octicons-question-16:{ .middle } __More reading?__

    ---

    Thirsting for knowledge?

    [:octicons-arrow-right-24: Learn what makes up an app](components.md)

</div>

[^1]: `eda-toolbox` pod is by default deployed in the `eda-system` namespace.
