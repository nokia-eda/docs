# Try EDA

We made sure that trying EDA is as easy as running a single command. Literally.

The [`Makefile`][makefile][^1] that comes with the [`playground` repository][playground-repo] you have cloned in the [previous step](getting-access.md#clone-the-playground-repository) has everything that is needed to enact the various installation steps. The use of this `Makefile` is not mandatory, but highly recommended as it substantially simplifies the quickstart installation process!

EDA is cloud-native platform deployed on top of Kubernetes (k8s); and not just because Kubernetes is a common orchestration system, but because it leverages the Kubernetes-provided declarative API, the tooling and the ecosystem built around it.  
It is required that your Kubernetes cluster satisfies the following requirements[^2]:

:fontawesome-solid-microchip: 10 vCPUs  
:fontawesome-solid-memory: 16GB of RAM  
:fontawesome-solid-floppy-disk: 100GB of storage

/// admonition | I don't have a cluster! Am I out?
    type: subtle-question
You don't have a cluster yet! We will get you a suitable k8s cluster in no time during this quickstart.
///

<small>If you are installing on a production cluster, please see official documentation for infrastructure requirements, as these depend on scale.</small>

## Dependencies

The getting started guide assumes you run a Linux/amd64 system. Check out [Advanced Installation](../user-guide/install-advanced.md) section for other installation options.  
You are welcome to try your own distro[^3], but steps have been validated on Ubuntu 22.04, Debian 11 and 12.

Your host executing the install needs `make`[^4] and [`docker`](https://docs.docker.com/engine/install/)[^5] installed. With `make` you can install the remaining dependencies:
<!-- --8<-- [start:tools-install] -->
```shell
make download-tools #(1)!
```

1. This will download `kind`, [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/), [`kpt`](https://kpt.dev/installation/kpt-cli), and `yq` into a `tools` folder relative to the current working directory.

    Subsequent steps use these versions of the binaries - you may use your own binaries for your own interactions. If you don't have `kubectl` in your `$PATH`, then consider copying the `kubectl` binary from the `tools` directory to a location in your `$PATH` to make use of it in the following steps.

<!-- --8<-- [end:tools-install] -->

/// admonition | Sysctl settings
    type: subtle-note
Some Linux distributions might be conservative about some settings such as max file descriptors available.

We recommend increasing the relevant sysctl values to avoid pod crashes during the installation by creating the following configuration file:

```bash
sudo mkdir -p /etc/sysctl.d && \
sudo tee /etc/sysctl.d/90-eda.conf << EOF
fs.inotify.max_user_watches=1048576
fs.inotify.max_user_instances=512
EOF
```

And reloading the sysctl settings:

```bash
sudo sysctl --system && sudo systemctl restart docker
```

///

## Quick start

The quickest way to experience EDA is by using a simple command to complete an end-to-end KinD-based deployment of EDA with a [virtual 3-node networking topology](virtual-network.md).

```shell
export EXT_DOMAIN_NAME=${DNS-name-or-IP} \
make try-eda #(1)!
```

1. You may want to provide an `EXT_DOMAIN_NAME` environment variable to indicate what domain name or IP address you are going to use when reaching EDA UI/API. This can be a domain name or an IP address of a compute where you execute the quickstart installation.
    <!-- --8<-- [start:ext-name-note-1] -->
    If you're trying EDA on a remote machine, then you typically would set the DNS name or IP address of this machine in the `EXT_DOMAIN_NAME` variable.  
    Another popular option is to use SSH local port forwarding to access the EDA UI, in this case you would need to set the `EXT_DOMAIN_NAME` variable to `localhost` and `EXT_HTTPS_PORT` to the local port you are using for the port forwarding.
    <!-- --8<-- [end:ext-name-note-1] -->

    /// admonition | preferences file
        type: subtle-note
    Instead of providing the configuration values such as `EXT_DOMAIN_NAME` and `EXT_HTTPS_PORT` on the command line, you can also provide them in a [`pref.mk`][pref-file] file that comes with the playground repository.
    ///

    <h4>LLM Key</h4>
    To enable the Natural Language support for the [EDA Query](../user-guide/queries.md) functionality, provide the LLM key (OpenAI) with an additional environment variable or set it in the `pref.mk` file:

    ```shell
    export EXT_DOMAIN_NAME=${DNS-name-or-IP} \
    LLM_API_KEY=<key> \
    make try-eda
    ```

The installation will take approximately 10 minutes to complete. Once the it is done, you can optionally verify the installation.

[:octicons-arrow-right-24: Verify](verification.md)

## Web UI

EDA comes with a Web user interface that allows you to interact with the framework.

/// admonition | Note
    type: subtle-note
EDA is an API-first framework, and the UI is just a client that interacts with its API. The usage of the UI is optional, and you can interact with EDA using the [CLI tools](../user-guide/using-the-clis.md) such as `edactl`, `e9s` and/or by directly leveraging K8s API.
///

EDA UI is exposed in a cluster via a Service of type `LoadBalancer`, but since you a local `kind`-powered k8s cluster deployed you may not be able to reach it if you don't run `kind` on the same machine where your browser is!

Nothing a `kubectl port-forward` can't solve! In the very end of the installation log you should see a message inviting you to run the following command:

```shell
make start-ui-port-forward
```

This target will forward the https port of the `eda-api` service and display the URL to use in your browser.

Point your browser to `https://<eda-domain-name>:<ext-https-port>` where `eda-domain-name` is the `EXT_DOMAIN_NAME` value set during the install step and `ext-https-port` is the https[^6] port value set in the `EXT_HTTPS_PORT`.  
This should open the EDA UI. The default username is `admin`, and the password is `admin`.

<div class="grid cards" markdown>

- ::material-hammer-screwdriver:{ .middle } __Creating a resource__

    ---

    Now, that you are logged in, you are ready for your first EDA automation experience!

    [:octicons-arrow-right-24: Creating your first unit of automation](units-of-automation.md)

- :octicons-question-16:{ .middle } __How does install work?__

    ---

    If you want to understand how EDA playground installer works and what makes up the EDA installation, you can continue with the Installation process section.

    [:octicons-arrow-right-24: Learn more about installation process](installation-process.md)

</div>

[playground-repo]: https://github.com/nokia-eda/playground

[makefile]: https://github.com/nokia-eda/playground/blob/main/Makefile
[pref-file]: https://github.com/nokia-eda/playground/blob/main/pref.mk

[^1]: The [`playground` repository][playground-repo] supports both a try EDA (or playground) method using KinD, and a method for installing EDA to previously deployed Kubernetes clusters via the same `Makefile`.  
The latter is covered in the [Installation process section](installation-process.md).

[^2]: This as well accounts for the [playground topology](virtual-network.md).
[^3]: Or even [run it on macOS](../user-guide/install-advanced.md#eda-on-macos).

[^4]: Install with `sudo apt install -y make` or its `yum`/`dnf`-based equivalent.

[^5]: https://docs.docker.com/engine/install/  
You can try running the quickstart with `podman` instead of docker, although bear in mind that `podman`-based installation was not validated.

[^6]: EDA UI/API is served only over HTTPS.
