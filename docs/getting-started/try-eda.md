# Try EDA

We believe that EDA embodies what a network automation of the modern age should look like - declarative and programmable abstractions for both configuration and state, streaming-based engine, equipped with network-wide queries, extensible and multivendor-capable.  
And we don't want you to blindly take our word for it, instead we made EDA easily accessible[^1] so that both network engineers and cloud practitioners could be the judge.  
With no license and no registration required, you are mere couple commands away from having the full EDA experience wherever you are - with your laptop, in the cloud or logged in the VM.

To deliver the "Try EDA" experience, we have created an [EDA playground][playground-repo] - a repository that contains everything you need to install and provision a demo EDA instance with the virtual network on the side. Let us guide you through the installation process.

/// html | div.steps

1. **Choose where to run EDA**

    Since EDA uses Kubernetes as its application platform, you can deploy the EDA Playground anywhere a k8s cluster runs.  
    The most popular way to install the demo EDA instance is on a Linux server/VM, but you can also [run it on macOS](../software-install/non-production/macos.md), in an [existing Kubernetes cluster](../software-install/non-production/on-prem-cluster.md), or on [Windows using WSL](../software-install/non-production/wsl.md).

    <small>If you get stuck with the installation, please reach out to us on [Discord](https://eda.dev/discord), we are happy to help!</small>

2. **Ensure minimal system requirements are met**

    Regardless of whether you run EDA Playground locally on a laptop, or in a VM locally or in the cloud, the underlying k8s cluster should have the following resources available to it[^2]:

    <!-- --8<-- [start:resources-reqs] -->
    :fontawesome-solid-microchip: 10 vCPUs  
    :fontawesome-solid-memory: 16GB of RAM  
    :fontawesome-solid-floppy-disk: 30GB of SSD storage
    <!-- --8<-- [end:resources-reqs] -->

    For a VM-based installation, this means that the VM should be provisioned with (at the minium) this amount of resources.

3. **Clone the EDA Playground repository**

    Proceed with cloning the [EDA playground repository][playground-repo] that contains everything you need to install and provision a demo EDA instance.

    <small>If you are using a Linux VM or a server to deploy the Playground, you should clone the repository on that VM/server.</small>

    You will need `git`[^3] to clone it:

    <!-- --8<-- [start:pull-playground] -->
    ```shell
    git clone https://github.com/nokia-eda/playground && \
    cd playground
    ```
    <!-- --8<-- [end:pull-playground] -->

4. **Prepare the VM/Server**

    If you are deploying the EDA Playground on a VM/Server, you should take care of the following:

    Install `make` that orchestrates the installation of the EDA Playground.

    /// tab | apt

    ```shell
    sudo apt install -y make
    ```

    ///

    /// tab | yum

    ```shell
    sudo yum install -y make
    ```

    ///

    Install `docker` using our automated installer, if you don't have it already installed:

    ```shell
    make install-docker
    ```

    Or install it manually, by following the [official Docker installation guide](https://docs.docker.com/engine/install/) for your OS. If you installed docker via the package manager of your distribution, remove it and install as per the Docker installation guide.

    /// details | Ensure sudo-less docker access
        type: info
    After completing the docker installation, check if you can run docker commands without `sudo` by running:

    ```shell
    docker ps
    ```

    If you get a `permission denied` error, then you need to add your user to the `docker` group:

    1. Create the docker group.

            ```bash
            sudo groupadd docker
            ```

    2. Add your user to the docker group.

            ```bash
            sudo usermod -aG docker $USER
            ```

    3. Log out and log back in so that your group membership is re-evaluated.
    ///

    Ensure the relevant sysctl values are properly sized by pasting and running the following:

    ```bash
    make configure-sysctl-params
    ```

5. **Install the EDA Playground**

    To configure the EDA Playground installation you need to provide a single variable - the domain name or IP address of the machine where you install EDA.

    * In case of a VM, it is the IP address or a domain name of the VM.
    * If you are using ssh tunnel to access the VM, then provide `localhost` as the `EXT_DOMAIN_NAME` value[^4].

    With the IP/domain-name noted, set the `EXT_DOMAIN_NAME` environment variable in your shell:

    ```shell
    export EXT_DOMAIN_NAME=<Insert-DNS-name-or-IP-of-the-VM/server>
    ```

    <h4>LLM Key for the Natural Language Query</h4>
    If you want to enable the Natural Language support for the [EDA Query](../user-guide/queries.md) functionality, provide the LLM key (OpenAI) with an additional environment variable[^5]:

    ```shell
    export LLM_API_KEY=<your-OpenAI-API-key>
    ```

    Now, run the EDA [installer][makefile]:

    ```bash
    make try-eda #(1)!
    ```

    1. If `EXT_DOMAIN_NAME` environment variable left unset, the hostname of the machine where you executed the `make` command will be used.

        /// admonition | preferences file
            type: subtle-note
        Instead of providing the configuration values such as `EXT_DOMAIN_NAME` and `EXT_HTTPS_PORT` on the command line, you can also provide them in a [`prefs.mk`][prefs-file] file that comes with the playground repository.
        ///

    The installation will take approximately 10 minutes to complete. Once it is done, you can optionally [verify](verification.md) the installation.

    /// details | EDA License
        type: info
    As you may have noticed, the EDA Playground installation does not require a license. We wanted to ensure that automation with EDA is accessible to everyone, anytime.  
    The EDA system can perfectly run without a license with the following caveats:

    * Only virtual, CX-nodes can be onboarded. These are SR Linux nodes that will be deployed for you by the time `make try-eda` step finishes. No hardware, nor containerlab nodes can be used in an unlicensed EDA mode.
    * No [integration](../connect/cloud-connect.md) with the cloud systems such as Openstack, VMware, etc.
    ///

6. **Access the UI**

    EDA is an API-first framework, with its UI being a client of the very same API. At the end of the `make try-eda` output you will find the URL to access the UI.

    ```shell
    --> The UI can be accessed using https://10.10.1.1:9443 #(1)!
    --> INFO: EDA is launched
    ```

    1. Instead of `10.10.1.1` IP you will see the value you provided in the `EXT_DOMAIN_NAME` environment variable.
  
    Open your web browser and navigate to provided URL to access the EDA UI. As you would expect, credentials are required in order to log in.
    The default credentials are as follow:

    * Username: `admin`  
    * Password: `admin`

///
Now that you completed the installation, you can either read more on the installation details, or continue with creating your first unit of automation with EDA.

<div class="grid cards" markdown>

* :material-hammer-screwdriver:{ .middle } **Creating a resource**

    ---

    Now, that you are logged in, you are ready for your first EDA automation experience!

    [:octicons-arrow-right-24: Creating your first unit of automation](units-of-automation.md)

* :octicons-question-16:{ .middle } **How does install work?**

    ---

    If you want to understand how EDA playground installer works and what makes up the EDA installation, you can continue with the Installation process section.

    [:octicons-arrow-right-24: Learn more about installation process](installation-process.md)

</div>

/// details | Production installation
    type: subtle-note
For a production installation instructions, please refer to the [Software Installation](../software-install/index.md) document.
///

[playground-repo]: https://github.com/nokia-eda/playground

[makefile]: https://github.com/nokia-eda/playground/blob/main/Makefile
[prefs-file]: https://github.com/nokia-eda/playground/blob/main/prefs.mk

[^1]: As no other framework of comparable scale.
[^2]: This as well accounts for the [playground network topology](virtual-network.md).
[^3]: Many distributions come with `git` preinstalled, but if not you should install it via your package manager.  
    For instance with `apt`-enabled systems:

    ```shell
    sudo apt install -y git
    ```

[^4]: In case of a local port forwarding you will access EDA UI via `https://localhost:9443` when establishing the tunnel with:

    ```shell
    ssh -L 9443:localhost:9443 -N -f demo-vm
    ```

[^5]: You can provide the LLM key after the installation as well.
