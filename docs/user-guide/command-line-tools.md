# Command Line Tools

Nokia Event-Driven Automation (EDA) exposes three north-bound APIs to its users:

* Kubernetes API
* REST API
* gRPC API

A number of industry-standard and custom-built CLI tools work on top of the offered APIs, such as:

* `edactl` operates on top of the gRPC API and offers a comprehensive suite of commands tailored for Nokia EDA.  
* `kubectl` and `k9s` from the Kubernetes ecosystem make use of the K8s API and allow users to manage the underlying Kubernetes cluster as well as Nokia EDA resources.  
* Various custom CLI tools have been developed internally and externally that make use of the Nokia EDA REST API.

You have already used the Kubernetes API and the Nokia EDA's gRPC API when you managed EDA resources using the `kubectl` and `edactl` tools in the [Tour of Nokia EDA](../tour-of-eda/index.md). And you interacted with the platform's REST API when you, for example, opened the EDA UI in your browser or used [Ansible](../development/ansible/index.md) or [Terraform](../development/terraform/index.md) to manage EDA resources.

> In addition to EDA-specific CLIs, users get to benefit from the vast ecosystem of tools available in the Kubernetes ecosystem. We will cover some of such tools in this section as well.

You will find the majority of the tools already downloaded as part of the [installation process](../software-install/preparing-for-installation.md#installing-tools) and located in the `./tools` directory in the Playground repository. To make these tools available in your shell, add the Playground's directory containing the binaries to your shell's `$PATH`.

/// tab | Add permanently

Assuming your Playground repository is located at `~/nokia-eda/playground`, add the following line to your shell configuration file:

/// tab | Bash

```bash title="Adding the tools directory to the Bash PATH"
echo 'export PATH=$(realpath ~/nokia-eda/playground/tools):$PATH' >> ~/.bashrc
```

///
/// tab | Zsh

```bash title="Adding the tools directory to the Zsh PATH"
echo 'export PATH=$(realpath ~/nokia-eda/playground/tools):$PATH' >> ~/.zshrc
```

///
Restart your shell to apply the changes.

///
/// tab | Add temporarily
To temporarily add the tools directory to your `$PATH`, you can run the following command:

```bash
export PATH=$(realpath ~/nokia-eda/playground/tools):$PATH
```

///

Check if the tools are available in your shell by running:

```bash
which edactl
which kubectl
which k9s
```

If the tools are not available, check your shell configuration file for the correct path.

> Most of the tools are also available in the `eda-toolbox` pod.

## kubectl

`kubectl` is the CLI to reach for when interacting with Kubernetes. EDA users typically use it to manage and operate the underlying Kubernetes cluster and its components.

The `kubectl` requires a Kubernetes configuration (called `kubeconfig`) file to operate. This file is fetched from the K8s cluster as part of the [Kubernetes installation process](../software-install/deploying-eda/bootstrap-the-talos-kubernetes-cluster.md#obtaining-the-kubernetes-config-file) or automatically provisioned if the [Try EDA installation](../getting-started/try-eda.md) is used.

> While `kubectl` can also be used to manage EDA resources, it is not the preferred tool for doing so as it can't apply multiple resources in a single transaction.

If the correct kubeconfig file is obtained and available in your shell's `$KUBECONFIG` environment variable, you can verify `kubectl` is working by running:

```bash
kubectl get nodes
```

If the nodes are listed, your `kubectl` is correctly configured.

## edactl

`edactl` is a swiss-knife for EDA users, the go-to tool for managing resources, scripting, running queries, creating branches, scheduling workflows, running synthetic traffic tests, and automating pipelines with EDA.

It offers a comprehensive suite of commands that enable users to interact with a wide array of features and capabilities of the platform.

```title="edactl commands"
Available Commands:
  aaa          aaa user command
  alarms       List alarms or details of a specific alarm
  apply        Apply a configuration to a resource by file name or stdin
  branch       Branch operations
  certificates Certificate related commands
  completion   Generate the autocompletion script for the specified shell
  config       Interactions with EDACONFIG
  create       Create a resource from a file or from stdin
  delete       Delete resources by file name
  dhcp         DHCP related commands
  edge-if-ping Ping from an edge interface
  get          Displays one or many resources
  git          Git related commands
  help         Help about any command
  intent       intent
  labels       Display the label key/values in use
  mergerequest List merge requests
  namespace    Display active namespaces
  node         Node related commands
  patch        Update fields of a resource using JSON patch
  platform     Show cluster status and platform related commands
  query        Run an EQL query
  replace      Replace a resource by file name or stdin
  schema       Print Json Schema for given path
  sdk          Manipulate EDA sdk
  sub          Subscribe to state updates
  testman      testman related commands
  transaction  List transaction results
  workflow     Workflow related commands
```

Before you can use `edactl`, you need to fetch its configuration file from the Kubernetes cluster, and for this you need to have a valid kubeconfig file available. If you have done the [`kubectl` configuration](#kubectl) you can proceed to fetch the edactl configuration file with the following command:

```bash
edactl config generate
```

<div class="embed-result highlight">
```{.text .no-copy .no-select}
Config written to /home/roman/.eda/config.yml
```
</div>

The `edactl` configuration file is written to `~/.eda/config.yml` by default and resembles kubeconfig in its structure. To ensure that `edactl` is configured correctly, run the following command:

```bash
edactl platform
```

<div class="embed-result highlight">
```{.text .no-copy .no-select}
Name           Address  Port  ActivityState  BuildVersion                 CoreVersion  AvgLatency(ms)  Reachable  Synchronized  SyncedNpps  SyncedNodes
engine-config  self           Active         v0.0.0-2603282119-gfdcd02b8  v4.0.0-0                     true       true          1/1         1/1  
```
</div>

If the `edactl platform` command returns the platform information, you are ready to use `edactl` to its full potential. In case the command does not work, inspect the `edactl` config file that contains the external address of the `eda-api` service and the port (`51206` by default) the grpc api proxy listens on. Make sure the address and port are correct and the service is reachable.

It is recommended to add the `e` alias for `edactl` to your shell configuration file to make it easier to use:

//// tab | Bash

```bash
echo 'alias e="edactl"' >> ~/.bashrc
```

////

//// tab | Zsh

```bash
echo 'alias e="edactl"' >> ~/.zshrc
```

////

/// details | Shell completions
`edactl` acts as a drop-in replacement for `kubectl` when used for EDA resource management. The `get`, `apply`, `replace`, `delete`, and `patch` commands are supported and work similarly to their `kubectl` counterparts. To assist you with the commands and objects hierarchy, `edactl` provides shell completions for the common shells.

//// tab | Bash

Ensure that bash-completion is installed on your system.

To load completions for the current session:

```bash
source <(containerlab completion bash)
```

To load completions for each session:

/// tab | Linux

```bash
edactl completion bash > /etc/bash_completion.d/edactl
```

///
/// tab | macOS

```bash
edactl completion bash > /usr/local/etc/bash_completion.d/edactl
```

///

To also autocomplete for the `e` command alias, add the following to your `.bashrc` or `.bash_profile`:

```bash
complete -o default -F __start_edactl e
```

////
//// tab | ZSH
If shell completion is not already enabled in your environment you have to enable it by ensuring zsh completions are loaded. The following can be added to your `zshrc`:

```bash
autoload -U compinit; compinit
```

To load completions for each session generate the completion script and store it somewhere in your `$fpath`:

```bash
edactl completion zsh | \
sed '1,2c\#compdef edactl e\ncompdef _edactl e' > \
~/.oh-my-zsh/custom/completions/_edactl
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

## k9s

[k9s](https://k9scli.io/) is a TUI for Kubernetes clusters that you can see in many of our demos. Once in a while you would want to inspect the state of your cluster in a more graphical way than just using `kubectl` - that is when `k9s` comes in handy.

## e9s

`e9s` is the Terminal UI (TUI) for EDA and can help you interact with the platform similar to how you'd use the famous `k9s` for Kubernetes.

It comes preinstalled in the `eda-toolbox` pod. You can either connect to the toolbox pod[^1] and execute the utility directly from there, or you can setup a handy alias (for example in your `~/.zshenv`) to make it easily accessible.

```bash title="e9s"
alias e9s='kubectl -n eda-system exec -it $(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox \
--field-selector=status.phase=Running \
-o jsonpath="{.items[0].metadata.name}") \
-- sh -c "TERM=xterm-256color e9s"'
```

And behold the power of `e9s`!
/// tab | e9s main screen
![e9s](https://gitlab.com/rdodin/pics/-/wikis/uploads/f716432aa9db2dca2928faaf65bdb620/image.png)
///
/// tab | e9s query screen
Here is a quick demonstration on how to use the powerful [EDA Query Language (EQL)](queries.md) to run queries in `e9s`:

-{{ video(url='https://gitlab.com/rdodin/pics/-/wikis/uploads/c07acc0be3a26e8a93e23ae0e2e36d40/e9s_walkthrough.mp4') }}-
///

## lnav

EDA is composed of many microservices, and it is often useful to have a log viewer to quickly inspect the logs distributed across the pods.

The log aggregation that EDA uses is based on fluentbit/fluentd combination with the logs aggregated in the `eda-fluentd` deployment. To browse the logs you can use the [lnav](https://lnav.org/) CLI you would find in this deployment.

For convenience, you can set up an alias to quickly access the TUI logs viewer:

```bash
alias edalogs='kubectl -n eda-system exec -it $(kubectl -n eda-system get pods \
-l eda.nokia.com/app=fluentd -o jsonpath="{.items[0].metadata.name}") \
-- sh -c "TERM=xterm-256color lnav /var/log/eda/*/*/*.log"'
```

## helm

[Helm](https://helm.sh/) is one of the many package managers for Kubernetes. You might want to add it to your PATH to install additional apps and deployments on your cluster. For example, you may install the NetBox stack and test EDA<->NetBox integration, all done in a single cluster.

[^1]:  
<!-- --8<-- [start:open-toolbox] -->
    You can log in to the `eda-toolbox` pod using the following alias:
    
    ```bash
    alias edatoolbox='kubectl -n eda-system exec -it "$(kubectl -n eda-system get pods \
      -l eda.nokia.com/app=eda-toolbox \
      --field-selector=status.phase=Running \
      -o jsonpath="{.items[0].metadata.name}")" -- env TERM=xterm-256color bash -l'
    ```
<!-- --8<-- [end:open-toolbox] -->
