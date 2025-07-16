# Try EDA Installation process

The unattended ["Try EDA"](try-eda.md) install procedure powered by the `make try-eda` step does a lot of steps in the background, making the installation process quick and easy. However, going over most important steps of the playground installation process will give you a better understanding of the underlying operations and can assist you in troubleshooting issues.

/// admonition | Note
    type: subtle-note

1. If you want just to install EDA the easy way, you can skip this chapter and use the [Try EDA](try-eda.md) procedure.
2. This chapter explains the generic installation steps based on the Makefile operations and is not a reference for a production installation.
3. The outlined steps are not meant to be executed in the way they presented. This page just explains some core installation steps, without maintaining a close relationship between them.
///

The key installation step that the "Try EDA"[^1] installation performs are:

:material-chevron-right: Setting up a development Kubernetes cluster if one does not exist.  
:material-chevron-right: Downloading and installing the external and EDA core packages using `kpt`[^2].  
:material-chevron-right: Installing an initial set of EDA applications provided by Nokia.  
:material-chevron-right: Exposing UI/API endpoint to a user.

The `make try-eda` command sets up the whole thing for you; Let us explain some steps it carries out in more details.

## Tools

Who likes to manually install a bunch of tools that are needed for the installation process manually? Not us! That's why we automated the tools procurement our installation process relies on:

<!-- --8<-- [start:tools-install] -->
```shell
make download-tools #(1)!
```

1. This will download `kind`, [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/), [`kpt`](https://kpt.dev/installation/kpt-cli), and `yq` into a `tools` folder relative to the current working directory.

    Subsequent steps use these versions of the binaries - you may use your own binaries for your own interactions. If you don't have `kubectl` in your `$PATH`, then consider copying the `kubectl` binary from the `tools` directory to a location in your `$PATH` to make use of it in the following steps.
<!-- --8<-- [end:tools-install] -->

You will have to install the container runtime (e.g. `docker`) manually.

## EDA packages

EDA is packaged using [`kpt`][kpt-home], and uses this package manager tool to install core EDA components as well as external tools like cert-manager. The installer downloads EDA kpt packages by cloning the [nokia-eda/kpt][kpt-repo].  
These packages install EDA core and some external components onto the k8s cluster in the later steps.

But EDA kpt packages only install the core EDA components, such as its config engine, digital sandbox and so on. The EDA applications, though, are distributed via [application catalogs](../apps/app-store.md#resources), which are just git repositories with application manifests. The [app catalog][catalog-repo] that "Try EDA" downloads contains Nokia apps such as Fabrics, Interfaces, AAA and other basic apps you get installed with EDA.

To clone both EDA kpt packages and the app catalog, the makefile packs the following target:

```{.shell .no-select}
make download-pkgs
```

## KinD cluster

EDA is a set of containerized applications that are meant to run in a Kubernetes cluster. Try EDA setup uses Kubernetes-in-Docker project, a.k.a [`kind`][kind-home], to setup a local k8s cluster[^3].

/// details | Already have a cluster?
    type: subtle-note

Using the `kind` cluster for the quickstart is the easiest way to get started, but you are welcome to try EDA on a cluster of your own and even use the same `Makefile` to install EDA on it. Here is a [short guide](../software-install/non-production/on-prem-cluster.md) how to do that.

///

The `make try-eda` step will setup the KinD cluster automatically for you and you should be able to verify that a one-node cluster is running with:

```{.shell .no-select}
kubectl get nodes #(1)!
```

1. `kubectl` is also installed during the `make download-tools` step; you will find the binary in the `./tools` directory.

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                     STATUS   ROLES           AGE   VERSION
eda-demo-control-plane   Ready    control-plane   88s   v1.25.3
```
</div>

## External packages

EDA relies on some open source projects like `fluentd` for logging, `certmanager` for certificate management and `gogs` for Git. You may provide these components as part of your own cluster installation, or the EDA install can add them for you. It is highly recommended if EDA is the only workload in the cluster to allow EDA to manage the installation of these dependencies.

The external packages that EDA uses are defined in the [`nokia-eda/kpt/eda-external-packages`][ext-packages] directory and is installed as part of the `try-eda` step via this target:

```{.shell .no-select}
make install-external-packages
```

## Deployment configuration

To provide configuration flexibility for EDA installation, `kpt` packages have a lot of fields marked with the `# kpt-set:` annotation. These fields can be set with the `kpt` CLI to change their default values.  
Parameters like TLS configuration, proxies, default credentials and more are configurable via `kpt` setters.

> [Installation Customization](../software-install/deploying-eda/installing-the-eda-application.md#customizing-the-installation) section provides a deep dive on all customization options.

For example, it is common for EDA to be behind a load balancer, with clients terminating on the load balancer address and having their traffic forwarded from there. As EDA performs redirects it needs to know the name/IP clients will use to reach it. This can be accomplished via the setters in `kpt`, but for persistency and convenience, the most common settings can be set via the [`prefs.mk`][prefs-file] file that is part of the playground repository.

```{.shell .no-select title="subset of the options in the prefs.mk file"}
# EXT_DOMAIN_NAME = "<Domain name or IP address>"
# EXT_HTTP_PORT = "<Port for http access>"
# EXT_HTTPS_PORT = "<Port for https access>"
# EXT_IPV4_ADDR = "<LB IP or external route>"
# EXT_IPV6_ADDR = "<Same thing but in ipv6>"
```

> Check out [Trying EDA Like a Pro](../blog/posts/2024/try-eda-pro.md) post for tips and tricks on how to configure EDA.

### HTTP Proxies

If your cluster requires an HTTP proxy to access the resources outside of it, you will need to set the `HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`, and their lowercase counterparts.

The logic inside the `eda-configure-core` target will set these values automatically to the values in your environment. But if you're installing on a machine that has different proxy settings, you will need to set them manually in the [`prefs.mk`][prefs-file] file before running the `eda-configure-core` target.

Once the desired values are set in the `prefs.mk` file, the `eda-configure-core` target can be run to set the values in the `eda-kpt` package:

```{.shell .no-select}
make eda-configure-core
```

The end result of this command is that the manifests contained in the `eda-kpt` directory will have the corresponding values set to the values you provided.

## Installing EDA

An EDA deployment is composed of three parts:

1. **External packages**: 3rd party, open source components EDA relies on. Like `fluentd` for logging or `cert-manager` for certificate management.  
    As we [already discussed](#external-packages) the external packages installation, the focus now is on the EDA core and apps.
2. **Core**: this is a set of applications that bring the core functionality of EDA. It includes applications like the Config Engine, EDA Store, State Controller, and others.
3. **Applications**: these are applications that extend EDA's core functionality. They are pluggable by nature and decoupled from the Core. Users can install and uninstall Nokia-provided applications as needed, as well as develop their own or consume third-party applications.

### Core

EDA Core is a `kpt` package located at [`nokia-eda/kpt/eda-kpt-base`][eda-core-package] directory and is installed as part of the `try-eda` step with:

```{.shell .no-select}
make eda-install-core #(1)!
```

1. Feel free to look at the [`Makefile`][makefile] to understand what happens during the install.

The EDA deployments, daemonsets and services will be created by this target, and after ~2-5 minutes you should be able to see the EDA core components running.

/// details | Check deployment status
    type: subtle-info

Check the deployment status with the following command, you want to see all the deployments ready:

```{.shell .no-select}
kubectl -n eda-system get deploy | awk 'NR==1 || /eda/'
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
kubectl -n eda-system get engineconfig engine-config -o jsonpath='{.status.run-status}{"\n"}'
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

A basic set of Nokia-provided applications delivered via the [default App Catalog][catalog-gh-url] is installed with:

```{.shell .no-select}
make eda-install-apps #(1)!
```

1. Curious which apps are going to be installed? Check the [`Makefile`][makefile] and the `eda-install-apps` target.

## Bootstrap EDA

By installing the applications we made EDA _aware_ of them, but we haven't created any concrete instances of these apps yet. In the bootstrap step we create some example instances of these application types as well as some initial configuration.

```{.shell .no-select}
make eda-bootstrap
```

The bootstrap step uses the [`eda-kpt-playground`][kpt-playground-pkg] kpt package that contains the instances of the installed applications. For example, the concrete allocation pools or bootstrap configs for the networking nodes.

## What's next?

You now have a ready-to-use EDA installation, with core services and some apps installed. What we miss is some network to automate. Let's have one!

[:octicons-arrow-right-24: Virtual network](virtual-network.md)

[kpt-home]: https://kpt.dev
[kpt-repo]: https://github.com/nokia-eda/kpt
[kpt-playground-pkg]: https://github.com/nokia-eda/kpt/tree/main/eda-kpt-playground
[kind-home]: https://kind.sigs.k8s.io/
[catalog-repo]: https://github.com/nokia-eda/catalog
[kind-install]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
[makefile]: https://github.com/nokia-eda/playground/blob/main/Makefile
[prefs-file]: https://github.com/nokia-eda/playground/blob/main/prefs.mk
[ext-packages]: https://github.com/nokia-eda/kpt/tree/main/eda-external-packages
[eda-core-package]: https://github.com/nokia-eda/kpt/tree/main/eda-kpt-base
[catalog-gh-url]: https://github.com/nokia-eda/catalog

[^1]: Try EDA is an installation mode for labs and demos. For production installation consult with the [Software Installation](../software-install/index.md) document.
[^2]: kpt - pronounced "kept" - is a Kubernetes Packaging Tool. EDA uses `kpt` to package up all the resources needed to deploy EDA.  
See <https://kpt.dev> for more information.
[^3]: If you are using [macOS](../software-install/non-production/macos.md) you might be using another, non-KinD, k8s provider.
