# Virtual network

To make sure that you can get the full EDA experience without upfronting any hardware investment, EDA is packaged with a Digital Sandbox solution called **CX**.  
CX is in charge of creating and managing virtual topologies running in the cluster.  

## Example topology

An example [3-node Leaf/Spine topology][3-node-example-topo-gh-url] is provided with this quickstart and is automatically deployed when you run the all-in-one [`try-eda`](try-eda.md) installation command.

As part of this command a separate make target is called to load the topology resources into the cluster which, in its turn, triggers CX controller to start spinning up the nodes and wiring links between them.

```{.shell .no-select}
make topology-load #(1)!
```

1. `topology-load` targets loads the example topology provided in the json file as a ConfigMap into the cluster. The CX controller watches for ConfigMap changes and creates the corresponding topology resources.

As a result you will get you the following topology running in your cluster:

<div class='mxgraph' style='max-width:100%;border:1px solid transparent;margin:0 auto; display:block;' data-mxgraph='{"page":0,"zoom":2,"highlight":"#0000ff","nav":true,"resize":true,"edit":"_blank","url":"https://raw.githubusercontent.com/hellt/tmp/diagrams/playground-topology.drawio"}'></div>

As you would expect, it takes some time to spin up the nodes and establish the connections, you can check the status of the deployed topology in the [Verify](verification.md#node-connectivity) section of the quickstart.

## Connecting to the nodes

Your network engineering roots may ask to check out what is going on on an individual node, which requires you to start a shell in the Pod running the SR Linux simulator. This can be accomplished with these simple commands:

```{.shell .no-select}
make leaf1-ssh #(1)!
```

1. Of course, changing `leaf1` to `leaf2` or `spine1` will log you in the other nodes.

<div class="embed-result highlight">
```{.text .no-select .no-copy}
Using configuration file(s): ['/etc/opt/srlinux/srlinux.rc']
Welcome to the srlinux CLI.
Type 'help' (and press <ENTER>) if you need any help using this.
--{ + running }--[  ]--
A:leaf1#
```
</div>

## Initial configuration

The SR Linux nodes (the leaf and spine switches) that make up the virtual network come up with a minimal node configuration - only the bits that are required by EDA to onboard the nodes. By connecting to the node and running `info` command you can see the initial configuration and verify that it has no configuration besides the basic management settings.

With this barebones topology deployed we can start exploring EDA automation powers. Let's explore how EDA framework can be used to provision complex services with simple declarative abstractions.

[:octicons-arrow-right-24: Automating fabric configuration](units-of-automation.md)

## Tearing down the topology

In case you break your topology nodes beyond repair, you can always start over by tearing down the topology:

```{.shell .no-select}
make teardown-topology
```

This will remove the topology nodes resources, the accompanying simulators and NPP pods associated with them.

[3-node-example-topo-gh-url]: https://github.com/nokia-eda/playground/blob/main/topology/3-nodes-srl.yaml

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>
