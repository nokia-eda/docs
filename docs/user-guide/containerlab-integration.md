---
eda_crd_version: 24.12.1
---

# Containerlab Integration

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

To facilitate end-to-end testing and validation of configuration changes, EDA comes equipped with its own multi vendor network emulation engine abbreviated as **CX**. CX is a highly scalable network emulation platform that powers EDA's Digital Twin capabilities.

Acknowledging that EDA CX is a new network emulation platform that is still in the process of maturing, we wanted to offer a way to integrate EDA with multitude of existing network topologies built with [Containerlab](https://containerlab.dev/).

In this section we cover how to integrate EDA with a lab built with Containerlab in a fully [automated](#automated-integration) way first, and then explain how to do this [manually](#manual-integration) with a deep dive on things involved in the onboarding process. To keep things practical, we will take a real lab built with Containerlab - [srl-labs/srlinux-vlan-handling-lab](https://github.com/srl-labs/srlinux-vlan-handling-lab) and integrate it with EDA.

-{{ diagram(url='srl-labs/srlinux-vlan-handling-lab/diagrams/vlan.drawio', title='VLAN handling lab', page=0) }}-

This tiny lab consists of two SR Linux nodes and two clients connected to it which is all we need to demonstrate the integration. Let's deploy it like any other containerlab topology:

```bash
sudo containerlab deploy -t srl-labs/srlinux-vlan-handling-lab #(1)!
```

1. The lab will be cloned to the current working directory and deployed.

///admonition | Containerlab, SR Linux, and EDA versions
    type: subtle-note
For a successful integration you need to ensure the following minimal version requirements:

* Containerlab 0.62.2
* SR Linux 24.10.1
* EDA 24.12.1

This article was validated using the following versions:

* Containerlab: 0.62.2
* SR Linux: 24.10.1
* EDA: 24.12.1

///

Our end game is to install EDA and integrate it with the Containerlab topology so that we could manage the lab nodes using EDA. The integration scenario is depicted in the diagram below.

-{{ diagram(url='nokia-eda/docs/diagrams/clab-integration.drawio', title='', page=0) }}-

## Installing EDA

The reason we started this section with a mention of EDA CX is because as of EDA v24.12.1 the platform is installed by default with the CX engine enabled. What this means is that EDA will spin up virtual simulator nodes using the CX engine for every topology node.  
To let EDA manage external nodes (either real hardware or virtual nodes spawned outside of EDA) we need to provide a specific installation option.

Clone the [EDA Playground repository](https://github.com/nokia-eda/playground) if you haven't already and uncomment the following line in the [preferences (`prefs.mk`) file](../software-install/customize-install.md#preferences-file) :

```Makefile
SIMULATE = false
```

Set other installation parameters in the `prefs.mk` file as explained in the [Try EDA section](../getting-started/try-eda.md) and deploy EDA:

```bash
make try-eda #(1)!
```

1. The necessary installation parameters like `EXT_DOMAIN_NAME` in this case are provided in the preferences file. See [Try Eda Like a Pro](../blog/posts/2024/try-eda-pro.md) post to learn some neat installation tricks.

With the disabled simulation mode, EDA will be installed without the `eda-cx` deployment present and no topology loaded.

/// danger | License required
Unfortunately, the nodes spawned outside of EDA CX are currently considered as hardware nodes and are licensed. Even the virtual SR Linux nodes that are spawned by Containerlab :sob:

You can reach out to the EDA PLM team member in discord to check if they can help acquire one.

If you have a license, apply it to your cluster like this:

//// tab | License manifest

```yaml title="eda-license.yaml"
apiVersion: core.eda.nokia.com/v1
kind: License
metadata:
  name: eda-license
  namespace: eda-system
spec:
  enabled: true
  data: "YoUrLiCeNsEDaTa"
```

////
//// tab | apply command

```bash
kubectl apply -f eda-license.yaml
```

////
///

## Reachability requirements

For EDA to manage nodes spawned outside of the Kubernetes cluster it is deployed in, it must be able to reach them. In this tutorial we are installing EDA in the KinD cluster that comes as a default with the EDA Playground installation; so our EDA installation will be running alongside the Containerlab topology on the same host machine.

Yet, even though KinD and Containerlab are running on the same host, these two environments are isolated from each other as prescribed by the Docker networking model and enforced by iptables. In order to allow KinD cluster to communicate with Containerlab nodes Containerlab 0.62.2 release installs allowing iptables rules to the `DOCKER-USER` chain for v4 and v6 families.

To confirm that the communication is indeed allowed, we can take a management IP of one of our Containerlab nodes and ping it from the `eda-bsvr` pod that is one of the pods requiring connectivity with the Containerlab nodes.

Let's issue a ping from the `eda-bsvr` pod to the `clab-vlan-srl1` node:

```bash title="copy-paste command to srl1"
kubectl -n eda-system exec -i \
$(kubectl -n eda-system get pods -l eda.nokia.com/app=bootstrapserver \
-o=jsonpath='{.items[*].metadata.name}') \
-- ping -c 2 $(sudo docker inspect -f '{{.NetworkSettings.Networks.clab.IPAddress}}' clab-vlan-srl1)
```

If you managed to copy-paste things right, you should see packets happily flying between EDA and Containerlab nodes. OK, now, with the containerlab topology running, EDA installed and connectivity requirements satisfied, we can proceed with the actual integration.

## Automated integration

In pursue of a one-click integration experience, we have created the [`clab-connector`][clab-connector-repo] CLI tool that automates the integration process.

[clab-connector-repo]: https://github.com/eda-labs/clab-connector

### Installation

The `clab-connector` tool is easily installable using `uv` package manager, therefore start with [installing `uv`](https://docs.astral.sh/uv/getting-started/installation/) and then `clab-connector`:

/// tab | Install clab-connector (requires uv)

```bash
uv tool install git+https://github.com/eda-labs/clab-connector.git
```

///
/// tab | Install uv
If you wanted to save a click, here is a quick one-liner installer from uv website:

```bash title="for Linux and macOS"
curl -LsSf https://astral.sh/uv/install.sh | sh
```

///

### Usage

Clab-connector leverages Kubernetes API, EDA API and Containerlab topology export data to automate the integration process. Consequently, the host machine where the `clab-connector` tool is installed must have access to the kube config file, EDA API endpoint and Containerlab's `topology-data.json`[^1] file.

#### Integrate

If you haven't changed any of the default credentials in your EDA installation, you can integrate EDA with Containerlab as simply as:

```bash
clab-connector integrate \
--eda-url https://your.eda.host \
-t ~/path/to/your-lab/clab-yourlab/topology-data.json #(1)!
```

1. The `topology-data.json` file is located in the Containerlab [Lab Directory](https://containerlab.dev/manual/conf-artifacts/#identifying-a-lab-directory), which is created next to the lab's topology file.

If you happen to change the default user credentials, you can provide them with `--eda-user` and `--eda-password` flags. Run `clab-connector integrate --help` to see all the available flags.

The connector tool will create a new EDA namespace matching the Containerlab lab name and will create the required resources in it. This allows you to managed as many distinct labs as you want, without having clashing resources between them.

#### Remove

To remove the EDA integration, run:

```bash
clab-connector remove \
--eda-url https://your.eda.host \
-t ~/path/to/your-lab/clab-yourlab/topology-data.json
```

This will remove the previously created namespace and all the resources inside it.

## Manual integration

/// details | TLDR
    type: subtle-note
To integrate SR Linux nodes spawned by Containerlab with EDA in the manual mode you need to:

1. Apply an EDA license to be able to integrate with SR Linux nodes spawned outside of EDA CX
2. <small>optional</small> Change the default NodeUser resource to use the `NokiaSrl1!` password
3. Create a [NodeProfile](#node-profile) resource with the OS/version/yang fields set to the corresponding values
4. Create a [TopoNode](#toponode) resource for each SR Linux node
5. Create an [Interface](#interface) resource per each endpoint of SR Linux nodes.
6. Create a [TopoLink](#topolink) resource for each link referencing the created Interface resources

//// details | Copy/Paste snippets
    type: code-example
If you want to quickly onboard SR Linux nodes after spawning the [srl-labs/srlinux-vlan-handling-lab](https://github.com/srl-labs/srlinux-vlan-handling-lab) containerlab topology, you can copy paste the following snippet entirely in your terminal.

```{.shell .code-scroll-lg}
cat << EOF | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/nodeUser.yaml:2"
$(ssh-add -L | awk '{print "    - \""$0"\""}')
EOF

cat << 'EOF' | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/nodeProfile.yaml:2"
EOF

cat << EOF | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/topoNodes.yaml:2:15"
    ipv4: $(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' clab-vlan-srl1)
--8<-- "docs/user-guide/clab-integration/topoNodes.yaml:17:30"
    ipv4: $(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' clab-vlan-srl2)
EOF

cat << 'EOF' | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/interface.yaml:1"
EOF

cat << 'EOF' | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/topoLink.yaml:2"
EOF
```

////
///

Even though automated integration makes the integration so easy, it is the manual integration that explains the moving parts and the underlying concepts. By completing this section you will get a decent understanding of the onboarding process and will breeze through the automated integration later on.

### SR Linux configuration

Our goal is to have EDA to discover and onboard the SR Linux nodes running as part of the Containerlab topology. When Containerlab[^2] spins up the SR Linux nodes it will add two EDA-specific gRPC servers to the default config; these servers will allow EDA to discover and later manage the nodes.

```{.bash .no-select}
sudo docker exec clab-vlan-srl1 sr_cli info system grpc-server 'eda*'
```

<div class="embed-result" markdown>
```{.bash .no-select .no-copy}
    system {
        grpc-server eda-discovery {
            admin-state enable
            rate-limit 65535
            session-limit 1024
            metadata-authentication true
            default-tls-profile true
            network-instance mgmt
            port 50052 #(1)!
            services [
                gnmi
                gnsi
            ]
        }
# snipped for brevity
        grpc-server eda-mgmt {
            ### Unable to retrieve TLS profile 'EDA'
            admin-state enable
            rate-limit 65535
            session-limit 1024
            metadata-authentication true
            tls-profile EDA #(2)!
            network-instance mgmt
            port 57410 #(3)!
            services [
                gnmi
                gnoi
                gnsi
            ]
        }
    }
```

1. EDA expects the discovery gRPC server to listen on port 50052.
2. The `EDA` TLS profile is a hardcoded name of the TLS profile that the EDA bootstrap server will install during the onboarding process. Since this profile does not exist until the onboarding process is completed, the annotation says that the profile with this name can not be retrieved. This annotation will be removed once the onboarding process is completed and the TLS profile is created by the bootstrap server.
3. Since Containerlab already sets up the `mgmt` gRPC server on port 57400 for the SR Linux nodes, the additional `eda-mgmt` gRPC server is configured to listen on a custom port 57410 that references the `EDA` TLS profile.

</div>

You will find the `eda-discovery` grpc server that is used by EDA to discover the node and setup the TLS certificates and the `eda-mgmt` grpc server that is used by EDA to manage the node after the initial discovery using the provisioned TLS certificates.

### TopoNode

It is time to let EDA know about the Containerlab topology and onboard the two SR Linux nodes that are running under the names `clab-vlan-srl1` and `clab-vlan-srl2`. But how do we do it?

It all starts with the [TopoNode][topoNode-crd] resource. The TopoNode resource is part of the EDA core and describes an abstracted node in the topology. In order to let EDA know about a node it needs to manage, we need to create a TopoNode resource per each SR Linux node in our Containerlab topology.

[topoNode-crd]: https://doc.crds.dev/github.com/nokia-eda/kpt/core.eda.nokia.com/TopoNode/v1@v-{{ eda_crd_version }}-

TopoNode's [Custom Resource Definition (CRD) documentation][topoNode-crd] describes the fields a resource of this type might have, but we need only a subset of them. Here are our two TopoNode resources named according to the container names of our SR Linux nodes in the topology:

```yaml linenums="1"
--8<-- "docs/user-guide/clab-integration/topoNodes.yaml:2"
```

If you feel lost, don't worry, we will explain what these fields mean in a moment.

#### Metadata

Following the Kubernetes Resource Model (KRM), we specify the `apiVersion` and `kind` of the resource we are describing in YAML format. The TopoNode resource belongs to the `core.eda.nokia.com` API group of the `v1` version and the resource kind is - `TopoNode`.

Next comes the **metadata** section. There, we specify the desired resource **name**. The name of the TopoNode resource does not have to match anything specific, but to keep things consistent with the Containerlab topology, we will use the corresponding container name of the SR Linux node.

In the **labels** section we need to add a label that describes how the node TLS certificates should be handled. EDA is a secure-first platform where all the communications are secured by default, and interactions with the networking nodes are no exception. With the `eda.nokia.com/security-profile: managed` label we tell EDA that it needs to manage the certificate lifecycle for the node.  
Without going into the details, this mode ensures fully automated certificate management for the node.

EDA Playground installation comes with a pre-created user **namespace** called `eda`. This pre-provisioned namespace should contain all user-provided resources, like TopoNode. Hence, we set the namespace to `eda` in the `metadata` section.

#### System information

Jumping over to the `.spec` object of the TopoNode resource, we can spot a block with System Information data:

```yaml
--8<-- "docs/user-guide/clab-integration/topoNodes.yaml:12:14"
```

* The `operatingSystem` field is set to `srl` for Nokia SR Linux nodes we about to get onboarded.
* And the `platform` field should contain the SR Linux platform name in its full text form. Since in the Containerlab topology we did not specify the SR Linux platform type, it defaults to 7220 IXR-D2L
* The `version` field must match the version of the SR Linux container image we are using in our topology.

#### Address

Since our SR Linux nodes were deployed with Containerlab, EDA can't possibly know the nodes IP addresses. We need to provide this information, and TopoNode resource has a field for that:

```yaml
--8<-- "docs/user-guide/clab-integration/topoNodes.yaml:15:16"
```

We chose to use the IPv4 address assigned by Containerlab, but IPv6 addresses are also supported. EDA will use this IP address to reach the node and start the onboarding process once the TopoNode resource is created in cluster.

> Providing the production address information disables the whole DHCP/ZTP workflow at the bootstrap server side, as the node is considered to be bootstrapped by an external system (like Containerlab).
>
> Bootstrap server in this case will just ensure that the node is reachable and setup a valid TLS certificate.

#### Node profile

The last piece in the TopoNode resource that we must set is a [NodeProfile][nodeProfile-crd].

[nodeProfile-crd]: https://doc.crds.dev/github.com/nokia-eda/kpt/core.eda.nokia.com/NodeProfile/v1@v-{{ eda_crd_version }}-

```yaml
--8<-- "docs/user-guide/clab-integration/topoNodes.yaml:11:11"
```

The NodeProfile, surprise-surprise, defines the profile of the node that a particular TopoNode resource is going to use.

```yaml linenums="1"
--8<-- "docs/user-guide/clab-integration/nodeProfile.yaml:2"
```

It contains more details about the node transport parameters, imaging information and YANG schema. Let's cover the most important fields of this resource.

##### OS and version

The first thing you see in the NodeProfile spec is the OS and version information. It has to match the OS and version provided in the associated TopoNode resource. Besides that, it also has to specify the path in JSPath notation to use to fetch the version value from the node and the regex to match against the fetched version value.

```yaml
--8<-- "docs/user-guide/clab-integration/nodeProfile.yaml:9:12"
```

##### Image

When a hardware node running SR Linux uses the ZTP process, the Bootstrap server provides a ZTP script that contains the initial bootstrap configuration and the target image URL.  
The URL that the Bootstrap server uses is provided with the `.spec.images[].image` field of the NodeProfile resource.

```yaml
--8<-- "docs/user-guide/clab-integration/nodeProfile.yaml:13:15"
```

You might ask why we need that for a Containerlab-spawned virtual node that does not need to be imaged? Good question. Since this field is marked as _required_ in the CRD we have to provide some value but for the virtual nodes we can provide a dummy URL.  
This is exactly what we did in our NodeProfile resource.

##### gRPC port

With the `port` field we specify the gRPC port number for the server that EDA will use to manage the node.  
If you remember, in the [SR Linux configuration section](#sr-linux-configuration) we mentioned that Containerlab adds `eda-mgmt` gRPC server listening on port 57410. This port is set in the NodeProfile resource and EDA will use it to connect to the node once the onboarding process is done.

##### YANG schema

One of the EDA's core features is its ability to validate the intents before applying them to the nodes. The validation piece is crucial for the mission-critical networks and EDA takes care of that.

To validate the intents, no matter how complex they are, EDA needs to know the YANG schema of the node it talks to. This requirement makes YANG schema a mandatory field in the NodeProfile resource; it should point to an HTTP location where EDA can fetch the YANG schema. We call this YANG bundle a Schema Profile.

```yaml
--8<-- "docs/user-guide/clab-integration/nodeProfile.yaml:17:17"
```

As part of the EDA Playground installation, the schema profile for SR Linux 24.10.1 version is already provided and is server by the EDA's Artifact server.

##### User

EDA uses gNMI protocol to communicate with the nodes, starting from discovery and onboarding. The gNMI server authenticates the client using the username and password pair provided in the gRPC metadata.

For the onboarding step to be successful, a pair of credentials needs to be provided via the `onboardingUsername` and `onboardingPassword` fields.

```yaml
--8<-- "docs/user-guide/clab-integration/nodeProfile.yaml:18:19"
```

When EDA will reach to the node's discovery gRPC server over the predefined `50052` port it will supply this credentials in the gRPC metadata. The provided credentials must be valid and since we are using the default `admin` credentials in these fields we can rest assured that the authentication will succeed.

But the onboarding user might not be the same as the one used for the ongoing management of the node. When EDA creates the **Node Push/Pull (NPP)** pods that are responsible for the configuration push and pull operations, these pods will use the credentials of a user defined in the NodeUser resource that we refer to in the NodeProfile as well:

```yaml
--8<-- "docs/user-guide/clab-integration/nodeProfile.yaml:20:20"
```

The `admin` [NodeUser][nodeUser-crd] resource has been created as part of the EDA Playground installation, but it uses a non-default SR Linux password, that we would like to change. To do that, we will craft a resource manifest that uses the default `NokiaSrl1!` password, as well as add a public key[^3] to enable typing-free SSH access.

[nodeUser-crd]: https://doc.crds.dev/github.com/nokia-eda/kpt/core.eda.nokia.com/NodeUser/v1@v-{{eda_crd_version}}-

```yaml linenums="1"
--8<-- "docs/user-guide/clab-integration/nodeUser.yaml:2"
```

The NodeUser resource references the NodeGroup resource that contains the AAA parameters this user should inherit.

### TopoLink

If we were to apply the TopoNode resource right now, we would end up getting the following topology diagram in EDA UI:

![topoNode-only](https://gitlab.com/rdodin/pics/-/wikis/uploads/1beaf38e89e64dd19716aee05cd94e45/topo.webp)

There is obviously a piece missing - the topology doesn't have any links! And the reason is simple - we haven't defined any topology link resources.

The [TopoLink][topoLink-crd] resource is responsible for defining the topology links. As the CRD description says:

> TopoLink represents a logical link between two TopoNodes. It may include more than one physical link, being used to represent a LAG or multihomed link.

[topoLink-crd]: https://doc.crds.dev/github.com/nokia-eda/kpt/core.eda.nokia.com/TopoLink/v1@v-{{eda_crd_version}}-

Looking at our lab diagram we can identify three topology links (highlighted in cyan):

-{{ diagram(url='nokia-eda/docs/diagrams/clab-integration.drawio', title='TopoLink objects', page=1) }}-

In EDA, we call links between the switches **inter switch** links, links between the switches and the clients **edge** links, and loopback links are called just **loopback**. So our three topology links will be:

1. The link between `srl1` and `client1` - `edge` link
2. The link between `srl1` and `srl2` switches - `interSwitch` link
3. The link between `srl2` and `client2` - `edge` link

The TopoLink resource [definition][topoLink-crd] has a straightforward specification:

```yaml
spec:
  links:
    - local: # required
        interface:
        interfaceResource: # required
        node: # required
      remote: # same as local
      speed:
      type: # required
```

A TopoLink, like any other link-like object is identified by a local endpoint and an optional remote endpoint. The local/remote endpoints are "connecting" to the TopoNode objects via `node` field.

But this is not everything a TopoLink needs. It also requires us to provide a link to the Interface resource via the [`interfaceResource`][interfaceResource-crd] field, as this is the bind point for the link in a particular node.

[interfaceResource-crd]: https://doc.crds.dev/github.com/nokia-eda/kpt/core.eda.nokia.com/TopoLink/v1@v-{{eda_crd_version}}-#spec-links-local-interfaceResource

#### Interface

The Interface resource creates a physical interface on the node. In our topology we have two physical interfaces per each managed SR Linux node:

-{{ diagram(url='nokia-eda/docs/diagrams/clab-integration.drawio', title='Interface objects', page=2) }}-

/// admonition | Interface CRD
    type: subtle-note
The Interface resource is part of an `interface.eda.nokia.com` application and its CRD is currently not published for us to link you to the doc.crds.dev.
///

For a TopoLink resource to be valid, the Interface resources must be created first and then referenced in the TopoLink specification.

Here is how you would define the `ethernet-1/1` interface on SR Linux node `srl1` that connects it to the `client1` node:

```yaml
--8<-- "docs/user-guide/clab-integration/interface.yaml:5:20"
```

As indicated in the spec, the Interface resource has a `members` field that can contain one (for a single interface) or multiple (for a LAG) interfaces objects. An implementation detail worth calling out is that the physical interface name should be normalized, i.e. SR Linux's `ethernet-1/1` becomes `ethernet-1-1`.

As we do not have LAG interfaces in our lab topology, all our interfaces will have identical configuration.

### Applying the resources

Let's summarize what we have learned so far:

1. The TopoNode resource defines the node in the EDA topology.
2. Creation of the TopoNode resource triggers onboarding process for the node.
3. TopoNode resource references the NodeProfile resource that defines the lower level node parameters used in bootstrapping/onboarding and the management workflows.
4. Onboarding happens over the well-known gRPC port 50052, this gRPC server is configured by Containerlab[^2] automatically for the SR Linux nodes.
5. Onboarding/Bootstrapping procedure sets up the `EDA` TLS profile using gNSI for SR Linux nodes. Once the certificate is installed, the node is marked as `onBoarded=true`.
6. Onboarding user and the user used for the EDA management might be different. The "permanent" user is declaratively defined by the NodeUser resource.
7. The gRPC server used for the management of the node is tied to the NodeProfile resource and is identified by the `port` field. This server should reference a dynamic `EDA` TLS profile that EDA's bootstrap server sets up during the onboarding workflow.
8. When the node is onboarded, the NPP pod is spawned and connects to the node; it **replaces** the existing node configuration with the configuration calculated by EDA based on the defined intents.
9. To create TopoLink resources, we need to create Interface resources first and then reference them in the TopoLink resource.

Before we rush to apply the resources, let's capture the state of the current config present on our SR Linux nodes and verify that the configuration will be wiped out and replaced once EDA starts to manage the nodes.

If you take a look at the [lab's topology file](https://github.com/srl-labs/srlinux-vlan-handling-lab/blob/main/vlan.clab.yml), you will notice that the two SR Linux nodes are defined with the startup config blobs that create a pair of interfaces and attach them to a bridge domain `bridge-1`. It is easy to verify that:

/// tab | interfaces

```{.bash .no-select}
docker exec -t clab-vlan-srl1 sr_cli \
'show interface ethernet-1/{1,10} brief'
```

<div class="embed-result">
```{.no-copy .no-select}
+---------------------+----------+----------+----------+----------+----------+
|        Port         |  Admin   |   Oper   |  Speed   |   Type   | Descript |
|                     |  State   |  State   |          |          |   ion    |
+=====================+==========+==========+==========+==========+==========+
| ethernet-1/1        | enable   | up       | 25G      |          |          |
| ethernet-1/10       | enable   | up       | 25G      |          |          |
+---------------------+----------+----------+----------+----------+----------+
```
</div>
///
/// tab | network instance

```{.bash .no-select}
docker exec -t clab-vlan-srl1 sr_cli \
'show network-instance bridge-1 interfaces'
```

<div class="embed-result">
```{.no-copy .no-select}
==================================================================================
Net instance    : bridge-1
Interface       : ethernet-1/1.0
Type            : bridged
Oper state      : up
==================================================================================
Net instance    : bridge-1
Interface       : ethernet-1/10.0
Type            : bridged
Oper state      : up
==================================================================================
```
</div>
///

#### NodeUser

With the initial state captured, let's start applying the resources in the bottom-up order, starting with the NodeUser resource:

/// tab | NodeUser

```yaml
--8<-- "docs/user-guide/clab-integration/nodeUser.yaml:2"
```

///
/// tab | `kubectl` apply

In this command we retrieve the public keys from the SSH agent and add add them to the NodeUser resource.

```{.bash .no-select}
cat << EOF | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/nodeUser.yaml:2"
$(ssh-add -L | awk '{print "    - \""$0"\""}')
EOF
```

///

#### NodeProfile

With `admin` NodeUser modified to feature the `NokiaSrl1!` password, let's create the NodeProfile resource named `srlinux-clab-24.10.1`:

/// tab | NodeProfile

```yaml
--8<-- "docs/user-guide/clab-integration/nodeProfile.yaml:2"
```

///
/// tab | `kubectl` apply

```{.bash .no-select}
cat << 'EOF' | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/nodeProfile.yaml:2"
EOF
```

///

#### TopoNode

So far the resources that we have modified or created did not trigger any activity in our EDA cluster; we just prepared the grounds for the next step of creating the TopoNode resources:

/// tab | TopoNode resources

When applying the TopoNode resources, the difference between the resources (besides the resource name) is in the `productionAddress` field. The `kubectl` apply tab shows how to programmatically fetch the current assigned IP address from the docker state and populate the resources accordingly so that you can copy and paste the command on the host that runs the containerlab topology.

```yaml
--8<-- "docs/user-guide/clab-integration/topoNodes.yaml:2"
```

///
/// tab | `kubectl` apply

```{.bash .no-select}
cat << EOF | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/topoNodes.yaml:2:15"
    ipv4: $(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' clab-vlan-srl1)
--8<-- "docs/user-guide/clab-integration/topoNodes.yaml:17:30"
    ipv4: $(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' clab-vlan-srl2)
EOF
```

///

#### Interface

A topology without links is not a topology. Time to add the links between the nodes. And a prerequisite to creating the TopoLink resources is to create the Interface resources.

/// tab | Interface resources

```{.yaml .code-scroll-lg}
--8<-- "docs/user-guide/clab-integration/interface.yaml:1"
```

///
/// tab | `kubectl` apply

```{.bash .no-select .code-scroll-sm}
cat << 'EOF' | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/interface.yaml:1"
EOF
```

///

The moment we created the Interface resources, EDA will configure the associated physical interfaces on the SR Linux nodes. We will see it in the Verification section. Yet, the topology UI will not show the interfaces until we create the TopoLink resources.

#### TopoLink

Now, that we have the Interfaces created we can create the last resource type - TopoLink.

/// tab | Interface resources

```{.yaml .code-scroll-lg}
--8<-- "docs/user-guide/clab-integration/topoLink.yaml:2"
```

///
/// tab | `kubectl` apply

```{.bash .no-select .code-scroll-sm}
cat << 'EOF' | kubectl -n eda apply -f -
--8<-- "docs/user-guide/clab-integration/topoLink.yaml:2"
EOF
```

///

### Verifying integration

Applying the TopoNode resources triggers a lot of activity in EDA. Starting with Bootstrap server to setup the dynamic TLS profile named `EDA` as part of the bootstrap workflow, finishing with NPP pods connecting to the SR Linux nodes and replacing the existing configuration with the configuration calculated by EDA based on the intents defined in the system.

You should see the TopoNode resources and their associated state looking like this after approximately 30-60s after applying the TopoNode resources:

```{.bash .no-select}
kubectl -n eda get toponodes
```

<div class="embed-result">
```{.no-copy .no-select}
NAME             PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE     AGE
clab-vlan-srl1   7220 IXR-D2L   24.10.1   srl   true        normal   Connected   Synced   12m
clab-vlan-srl2   7220 IXR-D2L   24.10.1   srl   true        normal   Connected   Synced   12m
```
</div>

If you don't see the same output, check the TransactionResults resource that will reveal any potential issues with the transactions.

```{.bash .no-select}
kubectl -n eda-system get transactionresults
```

If your TopoNode resources look all good, how about the SR Linux nodes? What has changed there? Remember that we warned you about the config replacement that happens the moment the nodes become managed by EDA?
Let's check the configuration on the `clab-vlan-srl1` node using the same `sr_cli` commands as we did in the beginning of the [Applying the resources](#applying-the-resources) section.

/// tab | interfaces

```{.bash .no-select}
docker exec -t clab-vlan-srl1 sr_cli \
'show interface ethernet-1/{1,10} brief'
```

<div class="embed-result">
```{.no-copy .no-select}
+---------------------+---------+---------+---------+---------+---------+
|        Port         |  Admin  |  Oper   |  Speed  |  Type   | Descrip |
|                     |  State  |  State  |         |         |  tion   |
+=====================+=========+=========+=========+=========+=========+
| ethernet-1/1        | enable  | up      | 25G     |         |         |
| ethernet-1/10       | enable  | up      | 25G     |         |         |
+---------------------+---------+---------+---------+---------+---------+
```
</div>

Note, that the interfaces are all up, because they have been configured when we created [Interface](#interface) resources.
///
/// tab | network instance

```{.bash .no-select}
docker exec -t clab-vlan-srl1 sr_cli \
'show network-instance bridge-1 interfaces'
```

<div class="embed-result">
```{.no-copy .no-select}
================================================================================
================================================================================
```
</div>

But contrary to the Interfaces, the `bridge-1` mac-vrf network instance is completely gone, because we have not created any resources that would trigger a network instance creation.

///
/// tab | EDA dynamic TLS profile
Besides things that were removed, EDA added a new dynamic TLS profile named `EDA`. The Bootstrap server created it and the `eda-mgmt` gRPC server has been referring to it as part of the default configuration of SR Linux.

```{.bash .no-select}
docker exec -t clab-vlan-srl1 sr_cli \
'info from state system tls server-profile EDA'
```

<div class="embed-result">
```{.no-copy .no-select}
    system {
        tls {
            server-profile EDA {
                key $aes1$AW7HyIAIvykjUG8=$0...Rk=
                certificate "-----BEGIN CERTIFICATE-----
MIIC5DCCAoqgAwIBAgIRANnUH/DLuCeMdQd5vp3VLw8wCgYIKoZIzj0EAwIwMzEO
...
QJNoWhdMyz++Nl83AzQOzRXKB7VbWxO7
-----END CERTIFICATE-----
"
                authenticate-client false
                dynamic true
                cipher-list [
                    ecdhe-ecdsa-aes256-gcm-sha384
                    ecdhe-ecdsa-aes128-gcm-sha256
                    ecdhe-rsa-aes256-gcm-sha384
                    ecdhe-rsa-aes128-gcm-sha256
                ]
                certz {
                    ssl-profile-id EDA
                    certificate {
                        version eda-01_05_25_16_01_13
                        created-on "2025-01-05T16:01:13.000Z (an hour ago)"
                    }
                }
            }
        }
    }
```
</div>

///

This completes the manual integration of EDA with a topology created by Containerlab. You were the witness of the process that is, well, manual, but the good news is that we you can use the [clab-connector](#automated-integration) to automate the process.

[^1]: `topology-data.json` file is generated by Containerlab when the lab is deployed. It can be found in the Containerlab's [Lab Directory](https://containerlab.dev/manual/conf-artifacts/#identifying-a-lab-directory).
[^2]: versions >= 0.61.0
[^3]: set your own public key, this one is for demonstration purposes only
