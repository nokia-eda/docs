# Using the CLIs

EDA comes with 2 CLI tools: `edactl` and `e9s`. Both are essential to the management of EDA, but they differ significantly in their approach and user experience.

`edactl` provides a comprehensive suite of commands that allow users to create, query, update and delete resources within an EDA cluster, making it ideal for scripting and automation.

On the other hand, `e9s` offers a dynamic, real-time terminal-based UI that simplifies the interaction with clusters by providing a high-level overview and quick navigation options for common tasks.

While `edactl` demands precise command inputs, `e9s` excels in offering visual feedback and streamlined workflows, significantly reducing the complexity and time needed for cluster management tasks.

## Accessing the CLIs

Both `edactl` and `e9s` are made available as part of the `eda-toolbox` pod.

You can log in to the `eda-toolbox` pod using the following command:

```{.shell .no-select}
make open-toolbox
```

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

```shell
edactl query '.node.srl.interface where (oper-state = "up")'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
 Node Name    Name           Admin State    Loopback Mode    Ifindex     Oper State    Oper Down Reason    Last Change               Linecard    Forwarding Complex    Mtu    Vlan Tagging    Tpid         Description
 dut1         ethernet-1/3   enable         none             81918       up                                2024-04-29T15:55:13.059Z  1           0                     9232   false           TPID_0X8100
 dut1         ethernet-1/9   enable         none             278526      up                                2024-04-29T15:55:13.103Z  1           0                     9232   false           TPID_0X8100
 dut1         ethernet-1/10  enable         none             311294      up                                2024-04-29T15:55:13.127Z  1           0                     9232   false           TPID_0X8100
 dut1         mgmt0          enable                          1077952510  up                                2024-04-29T15:54:20.747Z                                    1514
 dut1         system0        enable                          1086341118  up                                2024-04-29T15:55:12.943Z
 dut2         ethernet-1/4   enable         none             114686      up                                2024-04-29T15:55:13.067Z  1           0                     9232   false           TPID_0X8100
 dut2         ethernet-1/9   enable         none             278526      up                                2024-04-29T15:55:13.127Z  1           0                     9232   false           TPID_0X8100
 dut2         ethernet-1/10  enable         none             311294      up                                2024-04-29T15:55:13.159Z  1           0                     9232   false           TPID_0X8100
 dut2         mgmt0          enable                          1077952510  up                                2024-04-29T15:54:18.079Z                                    1514
 dut2         system0        enable                          1086341118  up                                2024-04-29T15:55:12.948Z
 dut3         ethernet-1/10  enable         none             311294      up                                2024-04-29T15:55:13.103Z  1           0                     9232   false           TPID_0X8100
 dut3         ethernet-1/11  enable         none             344062      up                                2024-04-29T15:55:13.159Z  1           0                     9232   false           TPID_0X8100
 dut3         ethernet-1/12  enable         none             376830      up                                2024-04-29T15:55:13.059Z  1           0                     9232   false           TPID_0X8100
 dut3         ethernet-1/13  enable         none             409598      up                                2024-04-29T15:55:13.075Z  1           0                     9232   false           TPID_0X8100
 dut3         mgmt0          enable                          1077952510  up                                2024-04-29T15:54:19.091Z                                    1514
 dut3         system0        enable                          1086341118  up                                2024-04-29T15:54:57.702Z
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
