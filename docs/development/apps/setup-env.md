# Setting up the dev environment

Before you start building an app, you'll need to prepare the development environment. This guide assumes you have EDA installed already and if you don't, you can quickly spin one up by following the [Try EDA](../../getting-started/try-eda.md) guide.

Your primary tools when developing an app:

* `edabuilder` for scaffolding, building, and publishing your app.
* `go` SDK for authoring the API of your custom resources.
* `python` runtime for getting syntax highlighting and IDE support when writing intents <small>optional</small>.
* `edactl` and `kubectl` for managing resources in the EDA cluster.

These tools are available for all major OSes and architectures, so you can develop on your preferred platform, no matter where you are.

///////// tab | `edabuilder`
`edabuilder` is a CLI tool that helps to scaffold a new EDA app, build the container for it and then publish the application to the catalog. The CLI can be downloaded from the [GitHub repository][edabuilder-repo-release] as well as from the `eda-toolbox`[^1] Pod.

[edabuilder-repo-release]: https://github.com/nokia-eda/edabuilder/releases

//// tab | Download via Playground
Download the latest `edabuilder` binary using the downloader script that comes with the [EDA Playground](https://github.com/nokia-eda/playground):

```bash title="Run in the EDA Playground repository"
make download-edabuilder
```

This will download the `edabuilder` binary to the `./tools` directory in the EDA Playground repository. For convenience, you can move the binary somewhere to your `$PATH`.

> The binary is also available in the [GitHub repository][edabuilder-repo-release] directly.

////
//// tab | Download from EDA toolbox

If you're developing on a linux/amd64 machine, you can get the `edabuilder` binary from the `eda-toolbox` Pod:

```shell
TOOLBOX_POD=$(kubectl get -n eda-system pod -l eda.nokia.com/app=eda-toolbox \
  -o jsonpath='{.items[0].metadata.name}')
kubectl -n eda-system \
cp ${TOOLBOX_POD}:/eda/tools/edabuilder /usr/local/bin/edabuilder
sudo chmod +x /usr/local/bin/edabuilder
```

////

You can add the `eb` alias for `edabuilder` to your shell configuration file to type less:

/// tab | Bash

```bash
echo 'alias eb="edabuilder"' >> ~/.bashrc
```

///

/// tab | Zsh

```bash
echo 'alias eb="edabuilder"' >> ~/.zshrc
```

///

/// details | `edabuilder` shell completions
To assist you with the commands and objects hierarchy, `edabuilder` provides shell completions for the common shells.

//// tab | Bash

Ensure that bash-completion is installed on your system.

To load completions for the current session:

```bash
source <(edactl completion bash)
```

To load completions for each session:

/// tab | Linux

```bash
edabuilder completion bash > /etc/bash_completion.d/edabuilder
```

///
/// tab | macOS

```bash
edabuilder completion bash > /usr/local/etc/bash_completion.d/edabuilder
```

///

To also autocomplete for the `eb` command alias, add the following to your `.bashrc` or `.bash_profile`:

```bash
complete -o default -F __start_edabuilder eb
```

////
//// tab | ZSH
If shell completion is not already enabled in your environment you have to enable it by ensuring zsh completions are loaded by adding the following to your `~/.zshrc`:

```bash
autoload -U compinit; compinit
```

To load completions for each session generate the completion script and store it somewhere in your `$fpath`:

```bash title="This examples assumes oh-my-zsh is installed"
edabuilder completion zsh | \
sed '1,2c\#compdef edabuilder eb\ncompdef _edabuilder eb' > \
~/.oh-my-zsh/custom/completions/_edabuilder
```

///// details | Completion script location
    type: subtle-note
The example above uses the `~/.oh-my-zsh/custom/completions` directory, which might not exist by default.

`echo $fpath` will show the directories zsh reads files from. You can either use one of the available completions directories from this list or add a new directory:

```
mkdir -p ~/.oh-my-zsh/custom/completions
```

and then add this directory to the `fpath` list by adding it in your .zshrc file:

```bash
fpath=(~/.oh-my-zsh/custom/completions $fpath)
```

Now you can use `~/.oh-my-zsh/custom/completions` for your completions as shown above.
/////

////
Start a new shell for this setup to take effect.
///

/////////

///////// tab | `go`
We will define the API of our declarative apps exactly like in Kubernetes - by crafting the Go files that extend the API of the EDA core. For this, we need a Go SDK.

Install Go SDK by following [the upstream installation instructions](https://go.dev/doc/install).

/// note
The minimum required Go version is `1.26.4`.
///
/////////

///////// tab | `python`
While being optional, we recommend installing the Python runtime and initialize a virtual environment for development.

If you already have a Python environment dialed in, you can skip this step, but if not, then the easiest way to get Python on your dev machine is by installing [uv](https://docs.astral.sh/uv/getting-started/installation/) - a modern multiplatform Python distribution and package manager.
/////////

///////// tab | `kubectl` and `edactl`
During the development process, you will find it useful to create, read and modify resources in the EDA cluster. `edactl` and `kubectl` are the tools to help you with that. Follow the instructions in the [CLI Tools](../../user-guide/command-line-tools.md) guide to install them.
/////////

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
