# Installing EDA

Installing EDA is as simple as:

:material-chevron-right: Making sure you have a Kubernetes cluster[^1], and a valid `kubeconfig` set up to talk to it.  
:material-chevron-right: Pulling down the EDA `kpt`[^2] package.  
:material-chevron-right: Installing the EDA core services via `kpt`.  
:material-chevron-right: Installing an initial set of EDA applications via `kubectl`.  

A [`Makefile`][makefile] that comes with the [`demo` repository][demo-repo] you have cloned in the [previous step](getting-access.md#clone-the-demo-repository) has simplified targets that can be called to enact the various installation steps. The use of this `Makefile` is not mandatory, but highly recommended as it substantially simplifies the installation process!

It is recommended that your Kubernetes cluster have at least[^3]:

:fontawesome-solid-microchip: 8 vCPUs  
:fontawesome-solid-memory: 16GB of RAM

Storage requirements are currently quite low.

## Dependencies

The getting started guilde assumes you run a Linux/amd64 system. Check out [Advanced Installation](../user-guide/install-advanced.md) section for other installation options.  
You are welcome to try your own distro[^7], but steps have been validated on Ubuntu 22.04, Debian 11, and Debian 12.

Your host executing the install needs `make`, [`kpt`](https://kpt.dev/installation/kpt-cli), and [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) CLI tools installed.

Install `make`[^4] if not done previously. And with `make` you can install the remaining dependencies with:

```shell
make download-tools
```

This will pull `kind`, `kubectl`, `kpt`, and `yq` into a `tools` folder relative to the current working directory.

<small .markdown>
Subsequent steps use these versions of the binaries - you may use your own distro packaged binaries for your own interactions. If you don't have `kubectl` in your `$PATH`, then consider copying the `kubectl` binary from the `tools` directory to a location in your `$PATH` to make use of it in the following steps.
</small>

## Need a cluster?

EDA automation suite runs on a Kubernetes cluster, if you don't have one, you can use Kubernetes-in-Docker, a.k.a [`kind`][kind-home], to quickly create a cluster and try out EDA.

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

<div class="embed-result">
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

<div class="embed-result">
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

<div class="embed-result">
```{.shell .no-select .no-copy}
Started
```
</div>

`Started` is good, anything else is bad!

///

### Deploying apps

EDA is an automation framework that is powered by [Applications](../apps/app-store.md) - these little nuggets of automation goodness that you're probably interested in using. Almost everything in EDA is considered an app - from the abstracted building blocks of the network services to the composite workflows enabling the automation of complex tasks.

EDA by default does not install any apps, so let's fix that by installing a basic set of applications that you can use to get started.

First, wait to ensure the AppStore[^6] controller has started:

```{.shell .no-select}
make is-apps-catalog-reachable
```

<div class="embed-result">
```{.shell .no-select .no-copy}
--> APP: APP Catalog is reachable
```
</div>

It may take a few minutes for an App Catalog to come online. Once App catalog is reachable, install applications:

```{.shell .no-select}
make eda-install-apps #(1)!
```

1. Curious which apps are going to be installed? Check the [`Makefile`][makefile-apps] for the list of apps.

<small>Apps installation takes ~2 minutes.</small>

## Bootstrap EDA

When we installed the apps in the previous step, we made EDA load the applications, including, but not limited to the following applications:

- `IpAllocationPool`: to manage IP address pools that may be used to allocate IP addresses to devices.
- `IndexAllocationPool`: to manage index pools like AS numbers, subinterface indexes, etc.

But we haven't created any concrete instances of these apps yet. In the bootstrap step we will create some example instances of these application types as well as some initial configuration.

```shell
make eda-bootstrap
```

The bootstrap step uses the [`eda-kpt-playground`][kpt-playground-pkg] kpt package that contains the bootstrapping resources.

You now have a ready-to-use EDA installation!

[:octicons-arrow-right-24: Onboard some nodes](onboarding-nodes.md)

[^1]: Don't have a cluster? No problem! As part of quick start we [install](#need-a-cluster) a [`kind` cluster][kind-home] together.
[^2]: kpt - pronounced "kept" - is a Kubernetes Packaging Tool. EDA uses `kpt` to package up all the resources needed to deploy EDA.  
See <https://kpt.dev> for more information.
[^3]: This as well accounts for the [demo topology](onboarding-nodes.md).
[^4]: for example on apt-based systems:
    ```shell
    sudo apt install -y make
    ```
[^5]: If you ran `make download-tools`, then `kind` is already installed in the `./tools` directory.
[^6]: The AppStore is a service that hosts a catalog of applications that can be installed on the EDA platform. It is a core service that is installed as part of the EDA core services.
[^7]: Or even [run it on macOS](../user-guide/install-advanced.md#eda-on-macos).

[kpt-home]: https://kpt.dev
[demo-repo]:
[kpt-repo]: https://github.com/nokia-eda/kpt
[kpt-playground-pkg]: TODO
[catalog-repo]: https://github.com/nokia-eda/catalog
[kind-home]: https://kind.sigs.k8s.io/
[kind-install]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
[makefile]: https://github.com/nokia-eda/docs/demo/Makefile
[makefile-apps]: https://github.com/nokia-eda/docs/demo/Makefile#L233
