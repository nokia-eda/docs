# Advanced installation

## Customization

You may customize the install by using [`kpt fn`][kpt-fn-cli]. In particular this lets you point to your own image registry, set your own LLM keys, and enable/disable the `simulate` flag.

Kpt allows you to use setters to customize the resources in the package. To customize EDA installation users can leverage the apply-setters function with the ConfigMap that lists the desired values for the setters:

```{.yaml .code-scroll-sm}
--8<-- "docs/user-guide/eda-config.yml"
```

Download the `eda-config.yaml`:

```shell
curl -sLO https://github.com/nokia-eda/blob/main/docs/user-guide/eda-config.yaml
```

Execute the apply-setters function, to update manifests with configured values:

```shell
kpt fn eval \
  --image gcr.io/kpt-fn/apply-setters:v0.1.1 \
  --truncate-output=false \
  --fn-config eda-config.yaml
```

## EDA in a non-KinD cluster

The [quickstart guide](../getting-started/install.md) did a great job of getting you up and running with a local Kubernetes cluster powered KinD. However, you may be willing to step away from the beaten path and install EDA in a non-KinD cluster. Well, EDA welcomes courageous souls like you!

Alright, truth be told, the installation process is almost identical to the one you followed in the quickstart guide, it is just a matter of having a few things to consider. In this section we will install EDA in a real k8s cluster running on bare VMs.

First, let's see what we are working with:

```{.shell .no-select}
kubectl get nodes
```

<div class="embed-result">
```{.shell .no-select .no-copy}
NAME         STATUS   ROLES           AGE   VERSION
rd-eda1-cp   Ready    control-plane   14h   v1.30.1
rd-eda1-w1   Ready    <none>          14h   v1.30.1
rd-eda1-w2   Ready    <none>          14h   v1.30.1
rd-eda1-w3   Ready    <none>          14h   v1.30.1
```
</div>

:scream: A real 3-node k8s cluster running vanilla Kubernetes 1.30.1 release! Each node has 6vCPU and 24GB of RAM amounting to a total of 18vCPU and 72GB of RAM. This is a decent little cluster for running EDA.

/// note
If you run a cluster with a Pod Security Policy in place, make sure to allow a privileged policy for the `default` namespace. The `cert-manager-csi-driver` daemonset requires this to run.

```{.bash .no-select}
kubectl label namespace default pod-security.kubernetes.io/enforce=privileged
```

///

Using the same `playground` repository from the [Installation section](../getting-started/install.md), we can use the same `make` targets to perform the installation steps (if haven't done before).

1. `make download-tools` - to download the necessary tools.
2. `make download-pkgs` - to download the EDA `kpt` package.

Now, we can install the EDA core services.

```shell
make eda-install-core
```

Pause for a moment and let the installation complete, by checking the [verification steps](../getting-started/verification.md#verifying-the-eda-core).

Once all EDA deployments are running and appstore is reachable, proceed with the application install, just like in the [quickstart guide](../getting-started/install.md#deploying-apps).

```shell
make eda-install-apps
```

With apps loaded, bootstrap the EDA installation by running the following command, exactly like in the quickstart guide:

```shell
make eda-bootstrap
```

And that's it, EDA has been successfully installed in a non-KinD cluster. Now let's deploy the same sample topology, by following the steps from the ["Onboarding nodes"](../getting-started/onboarding-nodes.md) guide.

```shell
make topology-load
```

and your cluster now is busy pulling the simulators, starting them up and laying out the interfaces between them. Use the [verification commands](../getting-started/verification.md#verifying-node-connectivity) to make sure the topology is up and running.

This may take a while (watch your pods status), but it should eventually complete successfully:

```{.shell .no-select}
kubectl get toponodes
```

<div class="embed-result">
```{.shell .no-select .no-copy}
NAME   PLATFORM       VERSION   OS    ONBOARDED   NPP         NODE     AGE
dut1   7220 IXR-D3L   0.0.0     srl   true        Connected   Synced   6m28s
dut2   7220 IXR-D3L   0.0.0     srl   true        Connected   Synced   6m28s
dut3   7220 IXR-D5    0.0.0     srl   true        Connected   Synced   6m28s
```
</div>

![final-pods](https://gitlab.com/rdodin/pics/-/wikis/uploads/55b10f7ea1b74501ee2434641e17edc4/piceda1.webp){.img-shadow}

Now you have a fully functional EDA installation running in a real Kubernetes cluster. Congratulations :partying_face:

### Exposing the EDA UI

In a regular cluster you might have the [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) or [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/) controller installed to route the external traffic to the services running inside the cluster. The examples below provide copy-pastable snippets that would create resources to explose the EDA UI.

EDA UI exposed inside a cluster via the `eda-api` service of type LoadBalancer and its `apiserver` (port 80) and `apiserverhttps` (port 443) ports:

```bash title="service configuration"
kubectl get service eda-api -o yaml | yq e '.spec.ports[0,1]' - #(1)!
```

1. Using [`yq`](https://github.com/mikefarah/yq/#install) to extract the service port configuration.

<div class="embed-result">
```{.yaml .no-select .no-copy}
name: apiserver
nodePort: 32609
port: 80
protocol: TCP
targetPort: 9200
name: apiserverhttps
nodePort: 30302
port: 443
protocol: TCP
targetPort: 9443
```
</div>

#### Nginx Ingress

If you're using Nginx Ingress controller, you can use the following example resources to configure NGINX Ingress to expose the EDA UI service:

* Terminating TLS on Ingress - [api-ingress-tls-terminate-https-internal.yaml](https://github.com/nokia-eda/kpt/blob/main/eda-external-packages/eda-api-ingress-https/api-ingress-tls-terminate-https-internal.yaml)
* Passing through TLS with termination on the eda-api side - [api-ingress-ssl-passthrough.yaml](https://github.com/nokia-eda/kpt/blob/main/eda-external-packages/eda-api-ingress-https-passthrough/api-ingress-ssl-passthrough.yaml)  
    Note, that NGINX controller has to be configured with the [passthrough option enabled](https://kubernetes.github.io/ingress-nginx/user-guide/tls/#ssl-passthrough).

#### Gateway API

If you're riding the [Gateway API](https://gateway-api.sigs.k8s.io/) wave, you can create a [`Gateway`](https://gateway-api.sigs.k8s.io/api-types/gateway/) resource to define your cluster gateway. As with the Ingress, the choice is yours if you want to terminate the TLS on the Gateway or not.

As a demonstration, we will create the Gateway resource with the TLS listener so that we will pass the TLS traffic to the EDA UI service, without terminating it on the Gateway.

Here is how you can create the `Gateway` resource:

/// tab | YAML Resource

```yaml
--8<-- "docs/user-guide/ingress/gateway.yml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<'EOF'
--8<-- "docs/user-guide/ingress/gateway.yml"
EOF
```

///

Now, let's create the `TLSRoute` resource that will bind our `Gateway` to the `eda-api` resource to provide the connectivity to the EDA UI:

/// tab | YAML Resource

```yaml
--8<-- "docs/user-guide/ingress/tlsroute.yml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<'EOF'
--8<-- "docs/user-guide/ingress/tlsroute.yml"
EOF
```

///

Now you should be able to access the EDA UI by navigating to the Gateway's URL.

[kpt-fn-cli]: https://kpt.dev/reference/cli/fn/

## EDA on macOS

Do you want to get full EDA experience on your macOS machine? Well, can't judge you!

Typically, the management and automation platforms of EDA' caliber require a ton of resources to run. But that is not the case with EDA! The microservices architecture and reliance on Kubernetes as a deployment platform make it possible to run EDA on a laptop using open-source tools. And macOS-powered machines is no exception!

/// note
In this chapter, we will specifically focus on running EDA on macOS with ARM64 architecture, such as Apple MacBook with M chips.
///

First things first, we assume you're running macOS with an ARM64, check this with `uname -a` and make sure it returns `arm64`.

Then make sure you're running macOS Sonoma (v14) or newer, as the older versions of macOS have issues with Rosetta emulation. This can be checked with `sw_vers -productVersion` and should return `14.0` or newer.

Next step is to ensure we have macOS Rosetta virtualization support enabled. This can be done by running the following command:

```shell
softwareupdate --install-rosetta
```

Now it is time to install Docker support on your macOS. There are few options available:

1. [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. [Rancher Desktop](https://rancherdesktop.io/)
3. [OrbStack](https://orbstack.dev/)
4. [Colima](https://github.com/abiosoft/colima)

Below you will find some guidance on how to install EDA on macOS using some of the above-mentioned tools. If you already have one installed, you can skip to the next section.

/// tab | Colima
Colima is an open-source, free and lightweight CLI tool that brings container runtimes to macOS.

It has a variety of [installation options](https://github.com/abiosoft/colima/blob/main/docs/INSTALL.md), with Homebrew being likely the most popular one:

```bash
brew install colima
```

Colima does not provide the Docker CLI client, so you will need to install one separately if you don't have one installed already. Thankfully, it is as easy as running:

```bash
brew install docker
```

Now, Colima can launch a linux/arm64 VM for us; this VM runs the Docker daemon so that we could run KinD with EDA inside. Here is a command to start the VM with 8 vcpu cores and 16 GB of RAM; this should be enough to run the quickstart demo:

```bash
colima start --cpu 8 --memory 16 --profile eda \
--vm-type=vz --vz-rosetta --network-address
```

We can ensure that the VM is running by checking the status:

```bash
colima status -e --profile eda
INFO[0000] colima [profile=eda] is running using macOS Virtualization
INFO[0000] arch: aarch64                                
INFO[0000] runtime: docker                              
INFO[0000] mountType: virtiofs                          
INFO[0000] address: 192.168.107.3                       
INFO[0000] socket: unix:///Users/romandodin/.colima/eda/docker.sock 
INFO[0000] cpu: 8                                       
INFO[0000] mem: 16GiB                                   
INFO[0000] disk: 60GiB 
```

Your docker CLI should also "sense" the docker engine availability and set the context to the Colima VM:

```bash
docker context ls
NAME           DESCRIPTION                DOCKER ENDPOINT                                    ERROR
colima-eda *   colima [profile=eda]       unix:///Users/romandodin/.colima/eda/docker.sock   
```

//// details | Networking and Load Balancer with Colima
    type: tip
The downside of having a VM that runs the Docker daemon is that additional layer of networking is introduced. Hence, the MetalLB Load Balancer that we install in the kind cluster will use the IP range that is not visible from the macOS host.

You don't need Load Balancer to enjoy EDA, since you can always expose the UI and the necessary services using `kubectl expose` command, but if you want to have the Load Balancer you will have to setup additional routes[^3].
////

///

With the container runtime installed and running via one of the tools mentioned above, we are almost there!

Follow the [Getting Started/Install](../getting-started/install.md) guide as usual, but do one extra bit right after the `make kind` step. You will have better experience and startup time if you pull the container images that EDA relies on and upload them to the kind cluster before calling the `make eda-install-core` target.

```shell
make pull-images #(1)!
```

1. this can take some time, depending on your connection speed towards the registry

And once the images are pulled, upload them to the kind cluster:

```shell
make kind-load-images #(1)!
```

1. takes about 3 minutes

And then, carry on with the rest of the installation steps as usual. A couple of minutes later you will have EDA running on your macOS machine with the simulated topology, all within your macOS[^2]!

If something goes wrong during installation, or if you want to reinstall, or maybe you finished playing with EDA, feel free to teardown the cluster using:

```shell
make teardown-cluster
```

This will remove the kind cluster, but will not stop the Docker VM. You can stop the VM and start it later on when you want to come back to EDA, your pre-pulled images will still be there, and the installation will be much faster.

[^2]: These performance cores finally have a purpose!
[^3]: For example as explained in [this blog post](https://opencredo.com/blogs/building-the-best-kubernetes-test-cluster-on-macos/).
