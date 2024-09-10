# Installation process

The unattended install procedure powered by the [`make try-eda`](try-eda.md) step hides a lot of machinery from a user, making the installation process quick and easy. However, going over most important steps of the playground installation process will give you a better understanding of the underlying operations and can assist you in troubleshooting issues.

/// admonition | Note
    type: subtle-note
This chapter explains the generic installation steps based on the Makefile operations and is not a reference for a production installation.
///

A generic EDA installation procedure is as simple as:

:material-chevron-right: Making sure you have a Kubernetes cluster[^1], and a valid `kubeconfig` set up to talk to it.  
:material-chevron-right: Pulling down the EDA `kpt`[^2] package.  
:material-chevron-right: Installing the EDA core components via `kpt`.  
:material-chevron-right: Installing an initial set of EDA applications via `kubectl`.

The `make try-eda` command sets up the whole thing for you; Let's unwrap it step by step.

## Tools

Who likes to install a bunch of tools that are needed for the installation process manually? Not us! That's why the first step of the installation process is to install the tools our installation process relies on.

--8<-- "docs/getting-started/try-eda.md:tools-install"

You will have to install the container runtime (e.g. `docker`) manually.

## EDA packages

EDA is packaged using [`kpt`][kpt-home], and uses this package manager tool to install core EDA components. The installer downloads two kpt packages by pulling the relevant git repositories.

```{.shell .no-select}
make download-pkgs
```

This pulls two git repositories to the respective directories:

1. the EDA [kpt][kpt-repo] package in `eda-kpt` directory
2. the EDA built-in [catalog][catalog-repo] in `catalog` directory.

## KinD cluster

EDA is a set of containerized applications that are meant to run in a Kubernetes cluster. EDA Playground uses Kubernetes-in-Docker project, a.k.a [`kind`][kind-home], to setup a local k8s cluster.

/// details | Already have a cluster?
    type: subtle-note

Using the `kind` cluster for the quickstart is the easiest way to get started, but you are welcome to try EDA on a cluster of your own and even use the same `Makefile` to install EDA on it.

Here are some things to consider when trying EDA on a non-`kind` cluster:

- if you run a cluster with a Pod Security Policy in place, make sure to allow a privileged policy for the `default` namespace. The `cert-manager-csi-driver` daemonset will say thank you.

    ```bash
    kubectl label namespace default pod-security.kubernetes.io/enforce=privileged
    ```

///

KinD has the following requirements:

- [`kind` CLI][kind-install][^3].
- [`docker`](https://docs.docker.com/engine/install/) or other kind-supported container runtime.

To create a kind cluster, run:

```shell
make kind
```

If cluster installation succeeds without errors you should be able to verify that a one-node cluster is running with:

```{.shell .no-select}
kubectl get nodes #(1)!
```

1. `kubectl` is also installed during the `make download-tools` step.

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                     STATUS   ROLES           AGE   VERSION
eda-demo-control-plane   Ready    control-plane   88s   v1.25.3
```
</div>

## External packages

Because the playground setup assumes a virgin k8s cluster, we will also install some common applications like `fluentd` for logging, `certmanager` for TLS and a `git` server. You may provide these components as part of your own cluster installation, or the EDA install can add them for you. It is highly recommended if EDA is the only workload in the cluster to allow EDA to manage the installation of these dependencies.

```{.shell .no-select}
make install-external-packages #(1)!
```

1. Installation takes approximately 3-5 minutes.

External packages are defined in the [`kpt/eda-external-packages`][ext-packages] directory.

## Configure your deployment

To provide configuration flexibility for EDA installation, `kpt` packages have a lot of fields marked with the `# kpt-set:` annotation. These fields can be set with the `kpt` CLI to change their default values.  
Parameters like TLS configuration, proxies, default credentials and more are configurable via `kpt` setters.

For example, it is common for EDA to be behind a load balancer, with clients terminating on the load balancer address and having their traffic forwarded from there. As EDA performs redirects it needs to know the name/IP clients will use to reach it. This can be accomplished via the setters in `kpt`, but for persistency and convenience, the most common settings can be set via the [`pref.mk`][pref-file] file that is part of the playground repository.

```{.shell .no-select title="subset of the options in the pref.mk file"}
# EXT_DOMAIN_NAME = "<Domain name or IP address>"
# EXT_HTTP_PORT = "<Port for http access>"
# EXT_HTTPS_PORT = "<Port for https access>"
# EXT_IPV4_ADDR = "<LB IP or external route>"
# EXT_IPV6_ADDR = "<Same thing but in ipv6>"
```

### HTTP Proxies

If your cluster requires an HTTP proxy to access the resources outside of it, you will need to set the `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`, and their lowercase counterparts.

The logic inside the `eda-configure-core` target will set these values automatically to the values in your environment. But if you're installing on a machine that has different proxy settings, you will need to set them manually in the [`pref.mk`][pref-file] file before running the `eda-configure-core` target.

Once the desired values are set in the `pref.mk` file, the `eda-configure-core` target can be run to set the values in the `eda-kpt` package:

```{.shell .no-select}
make eda-configure-core
```

The end result of this command is that the manifests contained in the `eda-kpt` directory will have the corresponding values set to the values you provided.

## Installing EDA

An EDA deployment is composed of two parts:

1. **Core**: this is a set of applications that bring the core functionality of EDA. It includes applications like the Config Engine, App Store, State Controller, and others.
2. **Applications**: these are applications that extend EDA's core functionality. They are pluggable by nature and decoupled from the Core. Users can install and uninstall Nokia-provided applications as needed, as well as develop their own or consume third-party applications.

### Core

EDA Core is a `kpt` package located at [`kpt/eda-kpt-base`][eda-core-package] that is installed with:

```{.shell .no-select}
make eda-install-core #(1)!
```

1. Feel free to look at the [`Makefile`][makefile] to understand what happens during the install.

In a minute, you should have the EDA core services deployed in your cluster and the make target should complete successfully. The services and controllers will be starting up after being installed, and after ~2-5 minutes you should be able to see the EDA core services running.

/// details | Check deployment status
    type: subtle-info

Check the deployment status with the following command, you want to see all the deployments ready:

```{.shell .no-select}
kubectl get deploy | awk 'NR==1 || /eda/'
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
eda-api           1/1     1            1           117s
eda-appstore      1/1     1            1           117s
eda-asvr          1/1     1            1           117s
eda-bsvr          1/1     1            1           117s
eda-ce            1/1     1            1           2m37s
eda-cx            1/1     1            1           117s
eda-fe            1/1     1            1           117s
eda-fluentd       1/1     1            1           41m
eda-git           1/1     1            1           40m
eda-git-replica   1/1     1            1           40m
eda-keycloak      1/1     1            1           117s
eda-postgres      1/1     1            1           117s
eda-sa            1/1     1            1           117s
eda-sc            1/1     1            1           117s
eda-toolbox       1/1     1            1           2m37s
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

If everything checks out, you're ready to install the apps!

### Apps

EDA is an automation framework that is powered by [Applications](../apps/app-store.md) - the little nuggets of automation goodness that you're probably interested in using. Almost everything in EDA is considered an app - from the abstracted building blocks of the network services to the composite workflows enabling the automation of complex tasks.

So far we've only installed the EDA core components, let's fix that by installing a basic set of applications through the EDA AppStore[^4] and its [default Catalog][catalog-gh-url] provided by Nokia.

```{.shell .no-select}
make eda-install-apps #(1)!
```

1. Curious which apps are going to be installed? Check the [`Makefile`][makefile] and the `eda-install-apps` target.

<small>Apps installation takes ~5 minutes.</small>

## Bootstrap EDA

When we installed the apps in the previous step, we made EDA load the applications, including, but not limited to the following ones:

- `IPAllocationPool`: to manage IP address pools that may be used to allocate IP addresses to devices.
- `IndexAllocationPool`: to manage index pools like AS numbers, subinterface indexes, etc.

By installing the applications we made EDA _aware_ of them, but we haven't created any concrete instances of these apps yet. In the bootstrap step we will create some example instances of these application types as well as some initial configuration.

```{.shell .no-select}
make eda-bootstrap
```

The bootstrap step uses the [`eda-kpt-playground`][kpt-playground-pkg] kpt package that contains the instances of the installed applications. For example, the concrete allocation pools or bootstrap configs for the networking nodes.

You now have a ready-to-use EDA installation, with core services and some apps installed. What we miss is some network to automate. Let's have one!

[:octicons-arrow-right-24: Virtual network](virtual-network.md)

[kpt-home]: https://kpt.dev
[kpt-repo]: https://github.com/nokia-eda/kpt
[kpt-playground-pkg]: https://github.com/nokia-eda/kpt/tree/main/eda-kpt-playground
[kind-home]: https://kind.sigs.k8s.io/
[catalog-repo]: https://github.com/nokia-eda/catalog
[kind-install]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
[makefile]: https://github.com/nokia-eda/playground/blob/main/Makefile
[pref-file]: https://github.com/nokia-eda/playground/blob/main/pref.mk
[ext-packages]: https://github.com/nokia-eda/kpt/tree/main/eda-external-packages
[eda-core-package]: https://github.com/nokia-eda/kpt/tree/main/eda-kpt-base
[catalog-gh-url]: https://github.com/nokia-eda/catalog

[^1]: Don't have a cluster? No problem! As part of the quickstart we [install](#kind-cluster) a [`kind` cluster][kind-home] for you.
[^2]: kpt - pronounced "kept" - is a Kubernetes Packaging Tool. EDA uses `kpt` to package up all the resources needed to deploy EDA.  
See <https://kpt.dev> for more information.
[^3]: If you ran `make download-tools`, then `kind` is already installed in the `./tools` directory.
[^4]: The AppStore is a service that hosts a catalog of applications that can be installed on the EDA platform. It is a core service that is installed as part of the EDA core services.
