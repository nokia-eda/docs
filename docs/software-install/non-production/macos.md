---
comments: true
---

# EDA on macOS

Do you want to get full EDA experience on your macOS machine? Well, can't judge you!

Typically, the management and automation platforms of EDA' caliber require a ton of resources to run. But that is not the case with EDA! The microservices architecture and reliance on Kubernetes as a deployment platform make it possible to run EDA on a laptop using open-source tools. And macOS-powered machines (even with M chips[^1]) is not an exception!

/// details | Watch the video
    type: subtle-note
-{{youtube(url='https://www.youtube.com/embed/QV8PwaSsNo8')}}-
///

This guide will talk you through installing the EDA Playground which consists of a [simulated network topology](../../getting-started/virtual-network.md) and full EDA platform installation. No EDA licenses are required to run the Playground.

## Playground repository

We will need the playground repository on our machine to run EDA installation steps. Pull it, as explained in the [Try EDA](../../getting-started/try-eda.md) section.

--8<-- "docs/getting-started/try-eda.md:pull-playground"

When the playground repo is cloned (you will need to install `git` to clone it), let's install the CLI tools that we will need to run EDA installation steps.

--8<-- "docs/getting-started/installation-process.md:tools-install"

The installer is smart enough to download the tools for the right OS/architecture.

## macOS prerequisites

Before we begin, let's ensure that you run macOS Sonoma v14.6.1 or newer, as the older versions of macOS might have issues with Rosetta emulation. The version can be checked with `sw_vers -productVersion` command in your terminal.

For Apple products with an M-chip the next step prescribes to check that macOS Rosetta virtualization support enabled. This can be done by running the following command:

```shell
softwareupdate --install-rosetta
```

## Docker

Now it is time to install Docker support on your macOS. There are many options available, the most common ones are:

1. [OrbStack](https://orbstack.dev/) <small>Our pick!</small>
2. [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
3. [Rancher Desktop](https://rancherdesktop.io/)
4. [Colima](https://github.com/abiosoft/colima)

Below you will find short guides on how to install Docker on your macOS using some of the tools mentioned above. If you already have one installed, you can skip to the next section.

//// tab | OrbStack

[OrbStack][orbstack-home] is a relatively new software that brings Docker support to macOS. The reason we can recommend it is that it has a great UX, has a VM management support, comes with a [lightweight k8s cluster](https://docs.orbstack.dev/kubernetes/) and free for personal use.

It is a native macOS app for both Intel and ARM64-based macs, so the installation is as easy as downloading the `dmg` file and installing it as usual. OrbStack installer will install the Docker CLI on your system, and will provide the Docker VM to run containers and k8s clusters, and enable the kubernetes cluster on the <kbd>Kubernetes</kbd> tab:

If you are installing Orbstack for the first time, you will see a dialog that asks you what do you plan to use OrbStack for, select "Kubernetes".

When OrbStack is installed, you can check the app settings to ensure that you have the sufficient resources allocated to an internal VM that runs docker daemon:

![resources](https://gitlab.com/rdodin/pics/-/wikis/uploads/ea34fdb13d588225aa3f718d5c1b4467/image.png)

Check the minimum requirements on the [Try EDA](../../getting-started/try-eda.md) page, but it is best to have more CPU and Memory available to the OrbStack VM. On the screenshot above 24GB and all CPUs are allocated to the OrbStack VM, and this has no negative/noticable impact on the overall system performance.

////

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

## Kubernetes cluster

With the container runtime installed and running via one of the tools mentioned above, we need to ensure we have a k8s cluster running on our macOS. You typically have two options:

1. Use the embedded k8s cluster provided by the tool that adds Docker support on your mac
2. Setup the kind cluster manually using `kind`/`k3s`/etc.

The first option might be the easiest way to get started, since it offers more tight integration with the macOS environment, for example by exposing services and providing a LoadBalancer implementation out of the box.

/// tab | OrbStack
If you're running OrbStack, you can spin up an embedded, one-node, lightweight cluster by checking the <kbd>Enable Kubernetes cluster</kbd> box in the settings (if unchecked):
![k8s-settings](https://gitlab.com/rdodin/pics/-/wikis/uploads/ef79bf6e405dfad44deeca5000adbfe3/image.png)

When OrbStack is done with creating a k8s cluster for you, you will be able to use regular cluster management tools like `kubectl`/`k9s`/etc to manage your cluster.

```{.shell .no-select}
kubectl get nodes #(1)!
```

1. `kubectl` is also installed during the `make download-tools` step.

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME       STATUS   ROLES                  AGE   VERSION
orbstack   Ready    control-plane,master   28m   v1.29.3+orb1
```
</div>

Now, your cluster is ready to run its first EDA installation!
///
/// tab | KinD
Should you choose not to use embedded k8s support in the tool of your choice, you can install a KinD cluster manually.

Run the following command from your playground repository to install a KinD cluster:

```shell
make kind
```

///

## Installing EDA

When running docker/k8s on a mac we have some layered networking to deal with, as the k8s cluster runs in a VM.

First, we need to make record of the following variables:

* `EXT_DOMAIN_NAME`: to the domain name or IP of the k8s cluster node (assuming you're running a single node cluster)
* `EXT_IPV4_ADDR` and/or `EXT_IPV6_ADDR`: set to the IP address of the cluster node. You can get these addresses in the output of:

    ```shell
    kubectl get nodes -o jsonpath='{.items[0].status.addresses}'
    ```

And also set a pair of no proxy variables set to the cluster cidr of your cluster. You can get it with:

```shell
kubectl get nodes -o jsonpath='{.items[0].spec.podCIDR}'
```

And once all the variables are known, you can start the installation. If you are running OrbStack, you can use the following command verbatim to install EDA:

```shell
EXT_DOMAIN_NAME=eda-api.k8s.orb.local \
EXT_IPV4_ADDR=198.19.249.2 \
EXT_IPV6_ADDR=fd07:b51a:cc66::2 \
EXT_HTTPS_PORT=443 \
NO_PROXY=192.168.194.0/25 \
no_proxy=192.168.194.0/25 \
make try-eda NO_KIND=yes NO_LB=yes
```

/// admonition | Potential turbulence
    type: warning
You may experience some hiccups during install, for example

1. Some application is stuck during install
2. Simulator nodes not starting up
3. NPP pods not starting up

This is all due to the fact that the majority of the images are running under Rosetta virtualization (they are not available yet in ARM64 arch). The workaround is to restart the `eda-ce` deployment when things get stuck.

///

## Connecting to the UI/API

Depending on the tool you're using to run k8s, your method of connecting to the UI will vary.

/// tab | OrbStack
In OrbStack, the k8s services are already exposed to your by the software, making it possible to access the UI by opening https://eda-api.k8s.orb.local/ in your browser.

This integration, though, will make our generic installer bark about the port being already in use when we try to setup the port-forward for the UI access at the very end of the `make try-eda` command. Please ignore this error, as OrbStack already took care of the UI access for you.

//// warning | macOS 15+
If your browser can not resolve the `eda-api.k8s.orb.local` domain, you need to add enable Local Network access policy for the browser of your choice since `.local` domain is resolved via mDNS. Check the Apple's [documentation](https://support.apple.com/guide/mac-help/control-access-to-your-local-network-on-mac-mchla4f49138/mac) and this [screenshot](https://gitlab.com/rdodin/pics/-/wikis/uploads/b91bbb7b7e6da5963736d24f43f64ce6/image.png) showing where the settings are located.
////

![ui](https://gitlab.com/rdodin/pics/-/wikis/uploads/1180ab27c1aa9017c1db3339ccae5f74/image.png)

The default EDA credentials are `admin:admin`.
///

## Tearing down

If something goes wrong during installation, or if you want to reinstall, or maybe you finished playing with EDA, feel free to destroy the cluster following the documentation for the tool you're using to run k8s.

/// tab | In OrbStack
To remove the k8s cluster provided by OrbStack run the following command in the terminal:

```
orb delete k8s
```

This will remove the VM that backs up the k8s cluster. To bring back the empty k8s cluster run

```
orb start k8s
```

and now you can restart the EDA installation.

///

[orbstack-home]: https://orbstack.dev/

[^1]: These performance cores finally have a purpose!
