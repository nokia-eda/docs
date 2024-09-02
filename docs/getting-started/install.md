# Installing EDA

Installing EDA is as simple as:

:material-chevron-right: Making sure you have a Kubernetes cluster[^1], and a valid `kubeconfig` set up to talk to it.  
:material-chevron-right: Pulling down the EDA `kpt`[^2] package.  
:material-chevron-right: Installing the EDA core services via `kpt`.  
:material-chevron-right: Installing an initial set of EDA applications via `kubectl`.  

A [`Makefile`][makefile] that comes with the [`playground` repository][playground-repo] you have cloned in the [previous step](getting-access.md#clone-the-playground-repository) has simplified targets that can be called to enact the various installation steps. The use of this `Makefile` is not mandatory, but highly recommended as it substantially simplifies the installation process!

The [`playground` repository][playground-repo] supports both a quick start (or playground) method using KinD, and a method for installing to previously deployed Kubernetes clusters via the same `Makefile`.

If using the KinD approach, it is recommended that your Kubernetes cluster has at least[^3]:

:fontawesome-solid-microchip: 10 vCPUs  
:fontawesome-solid-memory: 16GB of RAM  
:fontawesome-solid-floppy-disk: 100GB of storage

<small>If you are installing a real production cluster, please see official documentation for infrastructure requirements, as these depend on scale.</small>

## Dependencies

The getting started guide assumes you run a Linux/amd64 system. Check out [Advanced Installation](../user-guide/install-advanced.md) section for other installation options.  
You are welcome to try your own distro[^7], but steps have been validated on Ubuntu 22.04, Debian 11, and Debian 12.

Your host executing the install needs `docker` installed as well as `make`, [`kpt`](https://kpt.dev/installation/kpt-cli), and [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) CLI tools.

Install `make`[^4] if not done previously. And with `make` you can install the remaining dependencies with (note, that `docker` needs to be installed separately):

```shell
make download-tools
```

This will pull `kind`, `kubectl`, `kpt`, and `yq` into a `tools` folder relative to the current working directory.

<small .markdown>
Subsequent steps use these versions of the binaries - you may use your own distro packaged binaries for your own interactions. If you don't have `kubectl` in your `$PATH`, then consider copying the `kubectl` binary from the `tools` directory to a location in your `$PATH` to make use of it in the following steps.
</small>

/// note | Sysctl settings
Some Linux distributions might be conservative about some settings such as max file descriptors available.

On such systems, you may need to increase the relevant sysctl settings to avoid pod crashes during the installation by creating the following configuration file:

```bash
sudo mkdir -p /etc/sysctl.d && \
sudo tee /etc/sysctl.d/90-eda.conf << EOF
fs.inotify.max_user_watches=1048576
fs.inotify.max_user_instances=512
EOF
```

And reloading the sysctl settings:

```bash
sudo sysctl --system
```

///

## Quick start

If you're just looking to try EDA locally with a simulated topology, a simplified target exists to complete an end-to-end KinD-based deployment of EDA, following best practices and populating an example topology:

```shell
make try-eda #(1)!
```

1. If you need your EDA playground to be equipped with the natural language support for EQL, provide the LLM key as an environment variable:

    ```shell
    LLM_API_KEY=<key> make try-eda
    ```

Once this process completes you can proceed to the verify the installation.

[:octicons-arrow-right-24: Verify](verification.md)

## Need a cluster?

If you decided not to use the quickstart method, you can use the `Makefile` targets to install EDA in a step-by-step fashion.

EDA is a set of containerized applications running on a Kubernetes cluster. If you don't have one, you can use Kubernetes-in-Docker, a.k.a [`kind`][kind-home], to quickly create a cluster and try out EDA.

/// details | Already have a cluster?
    type: warning

Using the `kind` cluster for the quickstart is the easiest way to get started, but you are welcome to try EDA on a cluster of your own and even use the same `Makefile` to install EDA on it.

Here are some things to consider when trying EDA on a non-`kind` cluster:

- if you run a cluster with a Pod Security Policy in place, make sure to allow a privileged policy for the `default` namespace. The `cert-manager-csi-driver` daemonset will say thank you.

    ```bash
    kubectl label namespace default pod-security.kubernetes.io/enforce=privileged
    ```

- the quickstart steps have been validated on `kind` and certain other clusters, but every cluster is different, so you may end up with some errors, so some k8s knowledge would come in handy.

///

KinD has the following requirements:

- [`kind` CLI][kind-install][^5].
- [`docker`](https://docs.docker.com/engine/install/) or some other container runtime for `kind`.

To create a kind cluster, run:

```shell
make kind
```

If cluster installation succeeds without errors you should be able to verify that a one-node cluster is running with:

```{.shell .no-select}
kubectl get nodes
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                                 STATUS   ROLES           AGE   VERSION
eda-home-rd-eda-demo-control-plane   Ready    control-plane   21m   v1.25.3
```
</div>

## Pull EDA

EDA is packaged using [`kpt`][kpt-home], and the `kpt` CLI can be used to interact with this package. You can retrieve the EDA package with:

```{.shell .no-select}
make download-pkgs
```

This should pull two artifacts and put them in the respective directories:

1. the EDA [kpt][kpt-repo] package in `eda-kpt` directory
2. the EDA built-in [catalog][catalog-repo] in `catalog` directory.

## Deploy external dependencies

EDA depends on common Kubernetes workloads like fluentd for logging, and certmanager for TLS. You may provide these as part of your own cluster installation, or the EDA install can add them for you. It is highly recommended if EDA is the only workload in the cluster to allow EDA to manage the installation of these dependencies. This can be achieved with:

```{.shell .no-select}
make install-external-packages
```

## Configure your deployment

It is common for EDA to be behind a load balancer, with clients terminating on the load balancer address and having their traffic forwarded from there. As EDA performs redirects it needs to know the name/IP clients will use to reach it. This can be accomplished via the concept if setters in `kpt`, but as with other steps the `Makefile` has a simple target to accomplish this for you:

```{.shell .no-select}
make EXT_IPV4_ADDR="<external-v4-ip>" \
     EXT_IPV6_ADDR="<external-v6-ip>" \
     EXT_HTTPS_PORT="<external-https-port>" \
     EXT_DOMAIN_NAME="<external-name>" \
     eda-configure-core
```

You should of course substitute your own values into the command.

### Nuances for deployments behind proxies

The optional variables `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`, and their lowercase counterparts must be set if your deployment is behind a proxy.

- ensure you set both the uppercase and lowercase version of the variable, with the same value.
- ensure you populate `NO_PROXY` correctly, so that any internal-to-cluster addresses are not proxied (Pods and Services primarily), and that any domain names used by Kubernetes are also not proxied.

## Deploy EDA

### Deploying the core

With EDA packages pulled, installing the EDA core services is just one command away:

```{.shell .no-select}
make eda-install-core #(1)!
```

1. Feel free to look at the [`Makefile`][makefile] to understand what happens during the install.

A couple of minutes later, you should have the EDA core services installed in your cluster and the make target should complete successfully. The services and controllers will be starting up after being installed, and after approximately 5 minutes you should be able to see the EDA core services running

/// details | Verify the deployment
    type: info

Check the deployment status with the following command, you want to see all the deployments ready:

```{.shell .no-select}
kubectl get deploy | awk 'NR==1 || /eda/'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
eda-api           1/1     1            1           20m
eda-appstore      1/1     1            1           20m
eda-asvr          1/1     1            1           20m
eda-bsvr          1/1     1            1           20m
eda-ce            1/1     1            1           22m
eda-cx            1/1     1            1           20m
eda-fe            1/1     1            1           20m
eda-git           1/1     1            1           22m
eda-git-replica   1/1     1            1           22m
eda-kc            1/1     1            1           22m
eda-pg            1/1     1            1           22m
eda-sa            1/1     1            1           20m
eda-sc            1/1     1            1           20m
```
</div>

You can also check the `EngineConfig` to verify the ConfigEngine has started correctly, checking the `.status.run-status` field:

```{.shell .no-select}
kubectl get engineconfig engine-config -o jsonpath='{.status.run-status}{"\n"}'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
Started
```
</div>

`Started` is good, anything else is bad!

///

You can quickly verify the deployment with yet another target!

```{.shell .no-select}
make eda-is-core-ready
```

### Deploying apps

EDA is an automation framework that is powered by [Applications](../apps/app-store.md) - the little nuggets of automation goodness that you're probably interested in using. Almost everything in EDA is considered an app - from the abstracted building blocks of the network services to the composite workflows enabling the automation of complex tasks.

EDA by default does not install any apps, so let's fix that by installing a basic set of applications through the EDA AppStore[^6] that you can use to get started.

```{.shell .no-select}
make eda-install-apps #(1)!
```

1. Curious which apps are going to be installed? Check the [`Makefile`][makefile-apps] for the list of apps.

<small>Apps installation takes ~5 minutes.</small>

## Bootstrap EDA

When we installed the apps in the previous step, we made EDA load the applications, including, but not limited to the following applications:

- `IPAllocationPool`: to manage IP address pools that may be used to allocate IP addresses to devices.
- `IndexAllocationPool`: to manage index pools like AS numbers, subinterface indexes, etc.

But we haven't created any concrete instances of these apps yet. In the bootstrap step we will create some example instances of these application types as well as some initial configuration.

```{.shell .no-select}
make eda-bootstrap
```

The bootstrap step uses the [`eda-kpt-playground`][kpt-playground-pkg] kpt package that contains the bootstrapping resources.

You now have a ready-to-use EDA installation!

[:octicons-arrow-right-24: Onboard some nodes](onboarding-nodes.md)

[^1]: Don't have a cluster? No problem! As part of quick start we [install](#need-a-cluster) a [`kind` cluster][kind-home] together.
[^2]: kpt - pronounced "kept" - is a Kubernetes Packaging Tool. EDA uses `kpt` to package up all the resources needed to deploy EDA.  
See <https://kpt.dev> for more information.
[^3]: This as well accounts for the [playground topology](onboarding-nodes.md).
[^4]: for example on apt-based systems:
    ```shell
    sudo apt install -y make
    ```
[^5]: If you ran `make download-tools`, then `kind` is already installed in the `./tools` directory.
[^6]: The AppStore is a service that hosts a catalog of applications that can be installed on the EDA platform. It is a core service that is installed as part of the EDA core services.
[^7]: Or even [run it on macOS](../user-guide/install-advanced.md#eda-on-macos).

[kpt-home]: https://kpt.dev
[playground-repo]: https://github.com/nokia-eda/playground
[kpt-repo]: https://github.com/nokia-eda/kpt
[kpt-playground-pkg]: https://github.com/nokia-eda/kpt/tree/main/eda-kpt-playground
[catalog-repo]: https://github.com/nokia-eda/catalog
[kind-home]: https://kind.sigs.k8s.io/
[kind-install]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
[makefile]: https://github.com/nokia-eda/playground/blob/main/Makefile
[makefile-apps]: https://github.com/nokia-eda/playground/blob/d32a8b20531fab252a13f33714bc783aa5986a2b/Makefile#L617
