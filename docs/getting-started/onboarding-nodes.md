# Onboarding nodes

To make sure that users can get the full EDA experience without upfronting any hardware investment, EDA is packaged with the **CX** component. CX provides the Digital Sandbox functionality in EDA. In other words, CX is in charge of creating and managing virtual topologies running in the cluster.  
CX is triggered off the creation of certain resources, in particular `TopoNode` and `TopoLink`.

Based on these resources being created NOS simulators are spun up, and tunnels are dynamically created to build the interfaces between the simulator nodes.

## Example topology

You can add `TopoNode` and `TopoLink` resources at any time effectively building a custom topology of your choice, but let's leave this for later and deploy a simple example topology to get started.

An example topology is provided for you with two leaves and one spine, and is the quickest way to get started. You can load it with:

```{.shell .no-select}
make topology-load
```

This will get you the following topology running in your cluster:

```{.text .no-select}
                                            
               ┌────────────┐               
               │            │               
               │            │               
               │    dut3    │               
               │            │               
               │10 11  12 13│               
               └─┬─┬────┬─┬─┘               
                 │ │    │ │                 
                 │ │    │ │                 
 ┌────────────┐  │ │    │ │  ┌────────────┐ 
 │            │  │ │    │ │  │            │ 
 │           9├──┘ │    │ └──┤10          │ 
 │    dut1    │    │    │    │    dut2    │ 
 │          10├────┘    └────┤9           │ 
 │            │              │            │ 
 └────────────┘              └────────────┘ 
                                            
```

As you would expect, it takes some time to spin up the nodes and establish the connections, you can check the status of the deployed topology in the [Verify](verification.md#verifying-node-connectivity) section of the quickstart.

## Talking to nodes directly

Your network engineering roots may ask to check out what is going on on an individual node, which requires you to start a shell on the Pod simulating that node. This can be accomplished with these simple commands:

```{.shell .no-select}
make dut1-ssh #(1)!
```

1. Of course, changing `dut1` to `dut2` or `dut3` will get you to the other nodes.

<div class="embed-result highlight">
```{.text .no-select .no-copy}
Using configuration file(s): ['/etc/opt/srlinux/srlinux.rc']
Welcome to the srlinux CLI.
Type 'help' (and press <ENTER>) if you need any help using this.
--{ + running }--[  ]--
A:dut1#
```
</div>

The topology you have just deployed comes with some very minimal configuratio, where nodes have the most minimal config to get managed by EDA.

/// details | node configuration

```
--{ + running }--[  ]--
A:dut1# info from running
    interface ethernet-1/3 {
        admin-state enable
    }
    interface ethernet-1/9 {
        admin-state enable
    }
    interface ethernet-1/10 {
        admin-state enable
    }
    interface mgmt0 {
        admin-state enable
        subinterface 0 {
            admin-state enable
            ipv4 {
                admin-state enable
                dhcp-client {
                    trace-options {
                        trace [
                            messages
                        ]
                    }
                }
            }
            ipv6 {
                admin-state enable
                dhcp-client {
                    trace-options {
                        trace [
                            messages
                        ]
                    }
                }
            }
        }
    }
    interface system0 {
        admin-state enable
    }
    system {
        aaa {
            authentication {
                authentication-method [
                    local
                ]
            }
            server-group local {
                type local
            }
        }
        ssh-server mgmt {
            admin-state enable
            network-instance mgmt
        }
        name {
            host-name dut1
        }
        grpc-server mgmt {
            admin-state enable
            rate-limit 65535
            session-limit 1024
            metadata-authentication true
            network-instance mgmt
            port 57400
            services [
                gnmi
                gnoi
                gnsi
            ]
        }
    }
    network-instance mgmt {
        type ip-vrf
        admin-state enable
        description "Management network instance"
        interface mgmt0.0 {
        }
        protocols {
            linux {
                import-routes true
                export-routes true
            }
        }
    }
```

///

With this barebones topology at our hands, [let us show you](creating-a-resource.md) how EDA framework can be used to provision complex services with simple instructions.

## Undeploying the topology

In case you break your topology nodes beyond repair, you can always start over by undeploying the topology:

```{.shell .no-select}
make teardown-topology
```

This will remove the topology nodes resources, the accompanying simulators and NPP pods.

[:octicons-arrow-right-24: Working with resources](creating-a-resource.md)

[:octicons-arrow-right-24: Verify](verification.md)
