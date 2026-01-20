# Using the CLIs

EDA exposes two north-bound APIs to its users - Kubernetes API and [EDA API](../development/api/index.md) - and an in-cluster gRPC API. You used the Kubernetes API when you managed EDA resources using the `kubectl` CLI in the [Getting Started guide](../getting-started/units-of-automation.md). And you used the EDA's REST API when you, for example, opened the EDA UI in your browser.

On top of the offered APIs we build CLI tools like `edactl` and `e9s` which come handy in certain scenarios where CLI access is preferred.

`edactl` provides a comprehensive suite of commands that allow users to create, query, update and delete resources within an EDA cluster, making it ideal for scripting and automation.

On the other hand, `e9s` offers a dynamic, real-time terminal-based UI that simplifies the interaction with clusters by providing a high-level overview and quick navigation options for common tasks.  
While `edactl` demands precise command inputs, `e9s` excels in offering visual feedback and streamlined workflows, significantly reducing the complexity and time needed for cluster management tasks.

In addition to EDA-specific CLIs, users get to benefit from the vast ecosystem of tools available in the Kubernetes ecosystem. We will cover some of such tools in this section as well.

## edactl

`edactl` is your go-to tool for scripting, managing and automating pipelines with EDA. A swiss-knife for EDA users.

`edactl` is preinstalled in the `eda-toolbox` pod. You can either connect to the toolbox pod[^1] and execute the utility directly from there, or you can setup a handy alias (for example in your `~/.zshenv`) to make it easily accessible.

```bash title="Setting up <code>edactl</code> alias"
alias edactl='kubectl -n eda-system exec -it $(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox \
--field-selector=status.phase=Running \
-o jsonpath="{.items[0].metadata.name}") \
-- edactl'
```

It offers a comprehensive suite of commands that enable users to interact seamlessly with an EDA cluster.

```title="edactl commands"
Available Commands:
  cluster      Show the cluster status
  completion   Generate the autocompletion script for the specified shell
  config       Interactions with EDACONFIG
  edge-if-ping Ping from an edge interface
  get          Displays one or many resources
  git          Git related commands
  help         Help about any command
  intent       intent [config | state]
  labels       Display the label key/values in use
  namespace    Display active namespaces
  node         Node related commands
  platform     Platform related commands
  query        Run an EQL query
  sdk          Manipulate EDA sdk
  sub          Subscribe to state updates
  testman      testman related commands
  transaction  List transaction results
  workflow     Workflow related commands
```

For example, to query all interfaces with operational state `up` execute the following command while in the `eda-toolbox` pod:

```{.shell .no-select}
edactl query '.namespace.node.srl.interface where (oper-state = "up")'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy .code-scroll-sm}
 Namespace Name    Node Name    Name           Admin State    Mtu    Loopback Mode    Ifindex     Oper State    Oper Down Reason    Last Change               Linecard    Forwarding Complex    Forwarding Mode    Vlan Tagging    Tpid         Description              Num Physical Channels
 eda               leaf1        ethernet-1/1   enable         9232   none             16382       up                                2024-12-13T10:11:38.554Z  1           0                     store-and-forward  false           TPID_0X8100
 eda               leaf1        ethernet-1/2   enable         9232   none             49150       up                                2024-12-13T10:11:38.606Z  1           0                     store-and-forward  false           TPID_0X8100
 eda               leaf1        ethernet-1/3   enable         9232   none             81918       up                                2024-12-13T10:11:38.674Z  1           0                     store-and-forward  true            TPID_0X8100
```
</div>

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

![e9s](https://gitlab.com/rdodin/pics/-/wikis/uploads/f716432aa9db2dca2928faaf65bdb620/image.png)

Here is a quick demonstration on how to use the powerful [EDA Query Language (EQL)](queries.md) to run queries in `e9s`:

-{{ video(url='https://gitlab.com/rdodin/pics/-/wikis/uploads/c07acc0be3a26e8a93e23ae0e2e36d40/e9s_walkthrough.mp4') }}-

## kubectl

`kubectl` is the CLI to reach for when interacting with Kubernetes. It is also downloaded as part of the playground setup and can be found in the `tools` directory of the playground repository. If you don't `kubectl` installed, you can copy the binary from the playground repo like so:

```bash title="assuming your playground repo is in <code>~/nokia-eda/playground</code>"
sudo cp $(realpath ~/nokia-eda/playground/tools/kubectl) /usr/local/bin/kubectl
```

## k9s

[k9s](https://k9scli.io/) is a TUI for Kubernetes clusters that you can see in many of our demos. Once in a while you would want to inspect the state of your cluster in a more graphical way than just using `kubectl` - that is when `k9s` comes in handy.

As with `kubectl` you can copy it from the playground repo:

```bash title="assuming your playground repo is in <code>~/nokia-eda/playground</code>"
sudo cp $(realpath ~/nokia-eda/playground/tools/k9s) /usr/local/bin/k9s
```

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

The `helm` CLI is downloaded by the playground installer, so you can fetch it and use it right away like so:

```bash title="assuming your playground repo is in <code>~/nokia-eda/playground</code>"
sudo cp $(realpath ~/nokia-eda/playground/tools/helm) /usr/local/bin/helm

```

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