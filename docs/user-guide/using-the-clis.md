# Using the CLIs

EDA comes with 2 CLI tools: `edactl` and `e9s`. Both are essential to the management of EDA, but they differ significantly in their approach and user experience.

`edactl` provides a comprehensive suite of commands that allow users to create, query, update and delete resources within an EDA cluster, making it ideal for scripting and automation.

On the other hand, `e9s` offers a dynamic, real-time terminal-based UI that simplifies the interaction with clusters by providing a high-level overview and quick navigation options for common tasks.

While `edactl` demands precise command inputs, `e9s` excels in offering visual feedback and streamlined workflows, significantly reducing the complexity and time needed for cluster management tasks.

## Accessing the CLIs

Both `edactl` and `e9s` are made available as part of the `eda-toolbox` pod.
<!-- --8<-- [start:open-toolbox] -->
You can log in to the `eda-toolbox` pod using the following command:

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

## edactl

`edactl` is your go-to tool for scripting and automating pipelines with EDA.
It offers a comprehensive suite of commands that enable users to interact seamlessly with an EDA cluster.

```

Available Commands:
  cluster      Show the cluster status
  completion   Generate the autocompletion script for the specified shell
  config       Interactions with EDACONFIG
  edge-if-ping Ping from an edge interface
  flow         Display flows
  get          Display resources
  git          Git related commands
  help         Help about any command
  intent       Show the CR children, parents, dependencies or deviations for a resource
  node         Node related commands
  platform     Platform related commands
  query        Run an EQL query
  sub          Subscribe to state updates
  transaction  List transaction results

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
 eda               leaf1        ethernet-1/4   enable         9232   none             114686      up                                2024-12-13T10:11:38.722Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf1        ethernet-1/5   enable         9232   none             147454      up                                2024-12-13T10:11:38.782Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf1        ethernet-1/6   enable         9232   none             180222      up                                2024-12-13T10:11:38.858Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf1        ethernet-1/7   enable         9232   none             212990      up                                2024-12-13T10:11:38.922Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf1        ethernet-1/8   enable         9232   none             245758      up                                2024-12-13T10:11:38.994Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf1        ethernet-1/9   enable         9232   none             278526      up                                2024-12-13T10:11:39.054Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf1        ethernet-1/10  enable                none             311294      up                                2024-12-13T10:11:39.114Z  1           0                     store-and-forward                               lag-leaf1-e1011-local
 eda               leaf1        ethernet-1/11  enable                none             344062      up                                2024-12-13T10:11:39.182Z  1           0                     store-and-forward                               lag-leaf1-e1011-local
 eda               leaf1        ethernet-1/12  enable                none             376830      up                                2024-12-13T10:11:39.246Z  1           0                     store-and-forward                               lag-leaf1-2-e1212-local
 eda               leaf1        lag1           enable         9232                    536887294   up                                2024-12-13T10:12:38.479Z                                                       true            TPID_0X8100  lag-leaf1-e1011-local
 eda               leaf1        lag2           enable         9232                    536903678   up                                2024-12-13T10:12:38.483Z                                                       true            TPID_0X8100  lag-leaf1-2-e1212-local
 eda               leaf1        mgmt0          enable         1514                    1077952510  up                                2024-12-13T10:10:38.170Z                                    store-and-forward
 eda               leaf2        ethernet-1/1   enable         9232   none             16382       up                                2024-12-13T10:11:38.481Z  1           0                     store-and-forward  false           TPID_0X8100
 eda               leaf2        ethernet-1/2   enable         9232   none             49150       up                                2024-12-13T10:11:38.554Z  1           0                     store-and-forward  false           TPID_0X8100
 eda               leaf2        ethernet-1/3   enable         9232   none             81918       up                                2024-12-13T10:11:38.555Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf2        ethernet-1/4   enable         9232   none             114686      up                                2024-12-13T10:11:38.606Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf2        ethernet-1/5   enable         9232   none             147454      up                                2024-12-13T10:11:38.674Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf2        ethernet-1/6   enable         9232   none             180222      up                                2024-12-13T10:11:38.738Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf2        ethernet-1/7   enable         9232   none             212990      up                                2024-12-13T10:11:38.822Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf2        ethernet-1/8   enable         9232   none             245758      up                                2024-12-13T10:11:38.882Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf2        ethernet-1/9   enable         9232   none             278526      up                                2024-12-13T10:11:38.938Z  1           0                     store-and-forward  true            TPID_0X8100
 eda               leaf2        ethernet-1/10  enable                none             311294      up                                2024-12-13T10:11:38.982Z  1           0                     store-and-forward                               lag-leaf2-e1011-local
 eda               leaf2        ethernet-1/11  enable                none             344062      up                                2024-12-13T10:11:39.042Z  1           0                     store-and-forward                               lag-leaf2-e1011-local
 eda               leaf2        ethernet-1/12  enable                none             376830      up                                2024-12-13T10:11:39.098Z  1           0                     store-and-forward                               lag-leaf1-2-e1212-local
 eda               leaf2        lag1           enable         9232                    536887294   up                                2024-12-13T10:12:38.482Z                                                       true            TPID_0X8100  lag-leaf2-e1011-local
 eda               leaf2        lag2           enable         9232                    536903678   up                                2024-12-13T10:12:38.482Z                                                       true            TPID_0X8100  lag-leaf1-2-e1212-local
 eda               leaf2        mgmt0          enable         1514                    1077952510  up                                2024-12-13T10:10:37.090Z                                    store-and-forward
 eda               spine1       ethernet-1/1   enable         9232   none             16382       up                                2024-12-13T10:11:38.542Z  1           0                     store-and-forward  false           TPID_0X8100
 eda               spine1       ethernet-1/2   enable         9232   none             49150       up                                2024-12-13T10:11:38.610Z  1           0                     store-and-forward  false           TPID_0X8100
 eda               spine1       ethernet-1/3   enable         9232   none             81918       up                                2024-12-13T10:11:38.686Z  1           0                     store-and-forward  false           TPID_0X8100
 eda               spine1       ethernet-1/4   enable         9232   none             114686      up                                2024-12-13T10:11:38.766Z  1           0                     store-and-forward  false           TPID_0X8100
 eda               spine1       mgmt0          enable         1514                    1077952510  up                                2024-12-13T10:10:34.566Z                                    store-and-forward
```
</div>

## e9s

`e9s` is the go-to tool for building a dynamic Terminal UI (TUI) and obtaining a quick overview of the EDA cluster.

To launch `e9s` app, execute a simple `make` command:

```shell
make e9s
```

And behold the power of `e9s`!

![e9s](https://gitlab.com/rdodin/pics/-/wikis/uploads/f716432aa9db2dca2928faaf65bdb620/image.png)

Here is a quick demonstration on how to use the powerful [EDA Query Language (EQL)](queries.md) to run queries in `e9s`:

<video width="100%" controls playsinline><source src="https://gitlab.com/rdodin/pics/-/wikis/uploads/c07acc0be3a26e8a93e23ae0e2e36d40/e9s_walkthrough.mp4" type="video/mp4"></video>
