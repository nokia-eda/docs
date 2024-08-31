# Working with resources

EDA is an automation framework that follows declarative principles. You define the desired state of the resource and EDA takes care of the deployment, provisioning, configuration and reconciliation of the resource.

/// admonition | What is a `Resource`?
    type: question
A resource in EDA is a unit of automation and can be represent by virtually anything:

- an interface on a network device
- a complete fabric configuration[^2]
- a network serivice like a VPN or a VRF[^3]
- and even non-network related resources like a user account, a DNS record, or a firewall rule.
///

As a Kubernetes citizen, EDA represents its resources via [Custom Resources (CRs)][CR-k8s-doc] of Kubernetes that can be created using multiple methods including the Kubernetes (K8s) API, the EDA API, or through a User Interface (UI).

You probably wonder what resources are available in EDA and how to interact with them. Great question!  
EDA resources become available as soon as you install an [**EDA Application**](../apps/app-store.md) which is a way to extend EDA with new resources and capabilities. Applications may be provided by anyone: Nokia, our partners or indie developers - EDA is an open platform!

Nothing beats a hands-on experience, so let's learn more about Resources by following a short but powerful example of configuring a fabric on top of our 3-node topology deployed in a [previous step](onboarding-nodes.md).

## A Fabric resource

You heard it right! We will configure a DC fabric using a single EDA resource in a fully declarative way. The Fabric resource is a high-level abstraction that allows you to define a fabric configuration suitable for environments ranging from small, single-node edge configurations to large, complex multi-tier and multi-pod networks.

The [Fabric resource documentation][fabric-app-docs] provides a detailed description of the resource, its attributes and behavior. To not repeat ourselves, we will proceed with creating a Fabric resource and leave the exploration of its attributes to a reader.

Recall, that you can create EDA resources using the Kubernetes API, the EDA API or through a User Interface (UI). Let's start with the Kubernetes API.

## Using the Kubernetes API with Kubectl

To create a resource via the Kubernetes API, you must first define a Kubernetes Custom Resource (CR) specific to your needs. As we set ourselves to create a Fabric resource, we need to define a Fabric CR using [Fabric resource documentation][fabric-app-docs].

Using `kubectl` apply the CR on a system that has `kubectl` installed[^1].

/// tab | `kubectl`

```bash
cat << 'EOF' | tee my-fabric.yaml | kubectl apply -f -
--8<-- "docs/examples/my-fabric.yaml"
EOF
```

///
/// tab | YAML

```yaml
--8<-- "docs/examples/my-fabric.yaml"
```

///

Just like that, in a single command we deployed the Fabric CR that configures the fabric on our 3-node topology. You see the power of abstraction and automation in action, where the complex configuration task is reduced to a single declarative statement.

Note, that the Fabric CR is a high-level resource, it creates, references and uses other resources to configure the fabric.

Don't take our word for it, let's connect to the nodes and check what config they have now. Do you remember that all the nodes in our fabric [had no configuration](onboarding-nodes.md#talking-to-nodes-directly) at all? Let's see what changed after we applied the fabric resource:

//// details | Checking the running configuration on `dut1`
We can connect to the nodes with a single command like `make dut1-ssh` and check the running configuration.

```{.srl .code-scroll-sm}
--{ + running }--[  ]--
A:dut1# info
    interface ethernet-1/3 {
        admin-state enable
    }
    interface ethernet-1/9 {
        admin-state enable
        subinterface 0 {
            admin-state enable
            ipv4 {
                admin-state enable
                address 12.0.0.6/31 {
                }
            }
        }
    }
    interface ethernet-1/10 {
        admin-state enable
        subinterface 0 {
            admin-state enable
            ipv4 {
                admin-state enable
                address 12.0.0.2/31 {
                }
            }
        }
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
        subinterface 0 {
            admin-state enable
            ipv4 {
                admin-state enable
                address 11.0.0.2/32 {
                }
            }
        }
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
    network-instance default {
        type default
        admin-state enable
        router-id 11.0.0.2
        interface ethernet-1/10.0 {
        }
        interface ethernet-1/9.0 {
        }
        interface system0.0 {
        }
        protocols {
            bgp {
                admin-state enable
                autonomous-system 102
                router-id 11.0.0.2
                ebgp-default-policy {
                    import-reject-all true
                    export-reject-all true
                }
                afi-safi evpn {
                    admin-state enable
                    evpn {
                        inter-as-vpn true
                    }
                }
                afi-safi ipv4-unicast {
                    admin-state enable
                }
                preference {
                    ebgp 170
                }
                route-advertisement {
                    wait-for-fib-install true
                }
                group defaultbgpgroup-ebgp-my-fabric {
                    admin-state enable
                    export-policy [
                        ebgp-isl-export-policy-my-fabric
                    ]
                    import-policy [
                        ebgp-isl-import-policy-my-fabric
                    ]
                    afi-safi evpn {
                        admin-state enable
                    }
                    afi-safi ipv4-unicast {
                        admin-state enable
                    }
                    afi-safi ipv6-unicast {
                        admin-state disable
                    }
                }
                neighbor 12.0.0.3 {
                    admin-state enable
                    description "Connected to ethernet-1-11 on node dut3"
                    peer-as 101
                    peer-group defaultbgpgroup-ebgp-my-fabric
                }
                neighbor 12.0.0.7 {
                    admin-state enable
                    description "Connected to ethernet-1-10 on node dut3"
                    peer-as 101
                    peer-group defaultbgpgroup-ebgp-my-fabric
                }
            }
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
    routing-policy {
        policy ebgp-isl-export-policy-my-fabric {
            default-action {
                policy-result reject
            }
            statement 10 {
                match {
                    protocol local
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 15 {
                match {
                    protocol bgp
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 20 {
                match {
                    protocol aggregate
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 25 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                1
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 30 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                2
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 35 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                3
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 40 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                4
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 45 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                5
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
        }
        policy ebgp-isl-import-policy-my-fabric {
            default-action {
                policy-result reject
            }
            statement 10 {
                match {
                    protocol bgp
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 25 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                1
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 30 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                2
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 35 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                3
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 40 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                4
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
            statement 45 {
                match {
                    bgp {
                        evpn {
                            route-type [
                                5
                            ]
                        }
                    }
                }
                action {
                    policy-result accept
                    bgp {
                        local-preference {
                            set 100
                        }
                    }
                }
            }
        }
    }
```

The result of the deployed Fabric app is a fully configured BGP EVPN fabric that is configured on all of the nodes in our topology.

We can list the BGP neighbors on `dut1` to see that it has established BGP sessions with `dut2` and `dut3`.

```srl
--{ + running }--[  ]--
A:dut1# show network-instance default protocols bgp neighbor *
-------------------------------------------------------------------------------------------------------------------------------------------------------
BGP neighbor summary for network-instance "default"
Flags: S static, D dynamic, L discovered by LLDP, B BFD enabled, - disabled, * slow
-------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------
+-----------------+------------------------+-----------------+------+---------+--------------+--------------+------------+------------------------+
|    Net-Inst     |          Peer          |      Group      | Flag | Peer-AS |    State     |    Uptime    |  AFI/SAFI  |     [Rx/Active/Tx]     |
|                 |                        |                 |  s   |         |              |              |            |                        |
+=================+========================+=================+======+=========+==============+==============+============+========================+
| default         | 12.0.0.3               | defaultbgpgroup | S    | 101     | established  | 0d:5h:6m:58s | evpn       | [0/0/0]                |
|                 |                        | -ebgp-my-fabric |      |         |              |              | ipv4-      | [6/4/3]                |
|                 |                        |                 |      |         |              |              | unicast    |                        |
| default         | 12.0.0.7               | defaultbgpgroup | S    | 101     | established  | 0d:5h:6m:59s | evpn       | [0/0/0]                |
|                 |                        | -ebgp-my-fabric |      |         |              |              | ipv4-      | [7/0/7]                |
|                 |                        |                 |      |         |              |              | unicast    |                        |
+-----------------+------------------------+-----------------+------+---------+--------------+--------------+------------+------------------------+
```

////

Everything a fabric needs has been provisioned and configured on the nodes in a declarative way, taking the inputs from the Fabric CR.

## Verifying state of a resource

The status of the resource is updated by the state application associated with the resource. You can access the status of the resource using `edactl`, `kubectl`, or through the User Interface (UI).

Not all resources are published into K8s and therefore it is recommended to use `edactl` to view the status of resources.  
EDActl is a CLI tool that runs in the toolbox pod in a cluster and provides a way to interact with the EDA API. To leverage `edactl`, paste the following command into your terminal to install a shell alias that would execute `edactl` in the toolbox pod each time you call it.

```{.shell .no-select title="Install edactl alias"}
alias edactl='kubectl exec -it $(kubectl get pods \
-l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}") \
-- edactl'
```

Now we can inspect the created Fabric resource using both `edactl` and `kubectl`.

/// tab | `edactl`

```
edactl get fabrics my-fabric -o yaml
```

///
/// tab | `kubectl`

```bash
kubectl get fabrics my-fabric -o yaml
```

///

## Updating a resource with a manual transaction

When you create a resource, EDA automatically initiates a transaction and publishes its result. To view the list of transactions, execute the following `edactl` command:

```{.bash .no-select}
edactl transaction
```

<div class="embed-result">
```{.text .no-copy}
 ID  Result  Age     Detail   Username    Description
 1   OK      24m44s  SUMMARY  eda         startup - final load
 39  OK      17m3s   SUMMARY  kubernetes
 40  OK      17m     FULL     kubernetes  Installing routing:{v0.1.0+24.4.0-a1 semver} (from eda-catalog-builtin-apps)
 41  OK      17m     SUMMARY  kubernetes
 42  OK      16m59s  SUMMARY  kubernetes
 43  OK      16m59s  SUMMARY  kubernetes
 44  OK      16m56s  FULL     kubernetes  Installing routingpolicies:{v0.1.0+24.4.0-a1 semver} (from eda-catalog-builtin-apps)
 45  OK      16m56s  SUMMARY  kubernetes
 46  OK      16m54s  SUMMARY  kubernetes
 47  OK      16m54s  SUMMARY  kubernetes
 48  OK      16m47s  FULL     kubernetes  Installing services:{v0.1.0+24.4.0-a1 semver} (from eda-catalog-builtin-apps)
 49  OK      16m46s  SUMMARY  kubernetes
 50  OK      16m44s  SUMMARY  kubernetes
 51  OK      16m43s  SUMMARY  kubernetes
 52  OK      16m41s  FULL     kubernetes  Installing system:{v0.1.0+24.4.0-a1 semver} (from eda-catalog-builtin-apps)
 53  OK      16m41s  SUMMARY  kubernetes
 54  OK      16m38s  SUMMARY  kubernetes
 55  OK      16m38s  DEBUG    kubernetes
 56  OK      16m33s  DEBUG    kubernetes  Installing fabrics:{v0.1.0+24.4.0-a1 semver} (from eda-catalog-builtin-apps)
 57  OK      16m33s  DEBUG    kubernetes
 58  OK      16m30s  DEBUG    kubernetes
 59  OK      16m30s  DEBUG    kubernetes
 60  OK      16m26s  DEBUG    kubernetes  Installing oam:{v0.1.0+24.4.0-a1 semver} (from eda-catalog-builtin-apps)
 61  OK      16m26s  DEBUG    kubernetes
 62  OK      1m36s   DEBUG    kubernetes
 63  OK      1m36s   DEBUG    kubernetes
```
</div>

The transaction list shows the transaction ID, the status and the user who initiated the transaction. The transaction ID can be used to view the details of the transaction, including the changes made to the resources.

Alternatively, transactions can be manually initiated to enhance control and facilitate grouping of changes into a single "shared fate" transaction. Transactions support a dry-run mode, where all configurations are generated and validated by the NPP without affecting the Toponodes. If the dry-run results are satisfactory, you can proceed to finalize the transaction, disabling the dry-run mode, to apply the changes in the production environment.

If you want to change the my-fabric resource to use iBGP instead of eBGP as its overlay protocol, you can create a transaction and dry-run the changes.

/// tab | `kubectl`

```bash hl_lines="8"
cat << 'EOF' | tee my-fabric-update-transaction-dryrun.yaml | kubectl apply -f -
--8<-- "docs/examples/my-fabric-update-transaction-dryrun.yaml"
EOF
```

///
/// tab | YAML

```yaml hl_lines="7"
--8<-- "docs/examples/my-fabric-update-transaction-dryrun.yaml"
```

///

To check the result of your transaction:

```
edactl transaction
```

For detailed results of the dry-run:

```
edactl transaction <id> 
```

To view diffs of the node configs or any other CRs affected by your change:

```
edactl transaction <id> node-change dut1
```

Once satisfied with the changes, create a new transaction to push to production. Here, we disable dry-run to indicate that we want to push the changes to our DUTs:

/// tab | `kubectl`

```bash hl_lines="8"
cat << 'EOF' | tee my-fabric-update-transaction-prod.yaml | kubectl apply -f -
--8<-- "docs/examples/my-fabric-update-transaction-prod.yaml"
EOF
```

///
/// tab | YAML

```yaml hl_lines="7"
--8<-- "docs/examples/my-fabric-update-transaction-prod.yaml"
```

///

Check out the result of your transaction!

```
edactl transaction
```

Your fabric is now using iBGP as its overlay protocol. You can verify the changes by checking the running configuration on the nodes.

[CR-k8s-doc]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
[fabric-app-docs]: ../apps/fabric.md

[^1]: You can use the `kubectl` tool in the playground repository or the one installed in the [toolbox pod](../user-guide/using-the-clis.md#accessing-the-clis).
[^2]: Like the [Fabric resource][fabric-app-docs].
[^3]: Like the [Virtual Network resource](../apps/virtualnetwork.md) documented in the Apps section.
