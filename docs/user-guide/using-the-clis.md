# Using the CLIs

EDA exposes two north-bound APIs to its users: Kubernetes API and EDA API. You used the Kubernetes API when you managed EDA resources using the `kubectl` CLI in the [Getting Started guide](../getting-started/units-of-automation.md).

To interact with EDA API from the command line we provide you with 2 CLI tools: `edactl` and `e9s`. Both are essential to the management of EDA, but they differ significantly in their approach and user experience.

`edactl` provides a comprehensive suite of commands that allow users to create, query, update and delete resources within an EDA cluster, making it ideal for scripting and automation.

On the other hand, `e9s` offers a dynamic, real-time terminal-based UI that simplifies the interaction with clusters by providing a high-level overview and quick navigation options for common tasks.

While `edactl` demands precise command inputs, `e9s` excels in offering visual feedback and streamlined workflows, significantly reducing the complexity and time needed for cluster management tasks.

## Accessing the CLIs

Both `edactl` and `e9s` are made available as part of the `eda-toolbox` pod. You can either connect to the toolbox pod and execute the utilities directly from there, or you can setup handy aliases to make them more accessible.
/// tab | Connecting to the toolbox pod
<!-- --8<-- [start:open-toolbox] -->
You can log in to the `eda-toolbox` pod using the following command executed from the [playground repository](https://github.com/nokia-eda/playground):

```{.shell .no-select}
make open-toolbox
```
<!-- --8<-- [end:open-toolbox] -->
<div class="embed-result highlight">
```{.text .no-select .no-copy}
                     .:....
                .:=**+--:.
              :=*******##**+-:..
            .=+******###*++=-::.
           -+++******######***=...
          -++++******#######+----.
       .-++++++******#########*-:::.
      .++++++++******########=:=:.      EDA
   ..-=---=++++******#########+  ..
   ..      -++++=-:::-=+####::*=        K8s controller:  https://:
            =++:         +##*  .        IP in cluster:   10.244.0.25/24
            .:.           .-:
on eda-toolbox-58c8689c66-c48pg /eda
➜
```
</div>
///
/// tab | Setting up aliases
```bash title="edactl"
alias edactl='kubectl -n eda-system exec -it $(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}") \
-- edactl'
```

```bash title="e9s"
alias e9s='kubectl -n eda-system exec -it $(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}") \
-- sh -c "TERM=xterm-256color e9s"'
```

///

## edactl

`edactl` is your go-to tool for scripting and automating pipelines with EDA.
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
  intent       Show the CR children, parents, dependencies or deviations for a resource
  labels       Display the label key/values in use
  namespace    Display active namespaces
  node         Node related commands
  platform     Platform related commands
  query        Run an EQL query
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

To launch `e9s` app use the alias we set up [earlier](#accessing-the-clis) or, if you're in the playground repo, simply run:

```shell
make e9s
```

And behold the power of `e9s`!

![e9s](https://gitlab.com/rdodin/pics/-/wikis/uploads/f716432aa9db2dca2928faaf65bdb620/image.png)

Here is a quick demonstration on how to use the powerful [EDA Query Language (EQL)](queries.md) to run queries in `e9s`:

-{{ video(url='https://gitlab.com/rdodin/pics/-/wikis/uploads/c07acc0be3a26e8a93e23ae0e2e36d40/e9s_walkthrough.mp4') }}-
