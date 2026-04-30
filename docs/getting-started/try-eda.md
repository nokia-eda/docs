# Try Nokia EDA

We believe that Nokia Event-Driven Automation (EDA) embodies what a network automation of the modern age should look like - declarative and programmable abstractions for both configuration and state, streaming-based engine, equipped with network-wide queries, extensible and multivendor-capable.  
And we don't want you to blindly take our word for it, instead we made Nokia EDA easily accessible[^1] so that both network engineers and cloud practitioners could be the judge.  
With no license and no registration required, you are mere couple commands away from having the full EDA experience wherever you are - with your laptop, in the cloud or logged in the VM.

To deliver the "Try EDA" experience, we have created an [EDA playground][playground-repo] - a repository that contains everything you need to install and provision a demo EDA instance with the virtual network on the side. Let us guide you through the installation process.

/// details | Quickstart video walkthrough
    type: example
If you prefer a video walkthrough that starts from the very beginning, we have you covered! Check out the [**Event-Driven Automation playlist**](https://www.youtube.com/watch?v=5Qk8opmjixk&list=PLgKNvl454BxdqOqs3xzCXFxmRna71C90T) where Andy Lapteff walks you through the entire process step-by-step starting with installing a hypervisor all the way to the running EDA instance.

-{{youtube(url='https://www.youtube.com/embed/egPEqhbtlPs')}}-
///

/// html | div.steps

1. **Choose where to run EDA**

    Since EDA uses Kubernetes as its application platform, you can deploy the EDA Playground anywhere a k8s cluster runs.  
    The most popular way to install the demo EDA instance is on a Linux server/VM, but you can also [run it for free in Codespaces](#try-nokia-eda-in-codespaces), or on an [existing Kubernetes cluster](../software-install/non-production/on-prem-cluster.md), and even on a laptop running [macOS](../software-install/non-production/macos.md) or [Windows](../software-install/non-production/wsl.md).

    <small>If you get stuck with the installation, please reach out to us on [Discord](https://eda.dev/discord), we are happy to help!</small>

2. **Ensure minimal system requirements are met**

    Regardless of whether you run EDA Playground locally on a laptop, or in a VM locally or in the cloud, the underlying k8s cluster should have the following resources available to it[^2]:

    <!-- --8<-- [start:resources-reqs] -->
    :fontawesome-solid-microchip: 8 vCPUs  
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

    A single command separates you from the EDA Playground installation. But before you run it, if you want to enable the Natural Language support for the [EDA Query](../user-guide/eda-query-language.md) functionality, provide the LLM key (OpenAI) with an environment variable[^4]:

    ```shell
    export LLM_API_KEY=<your-OpenAI-API-key>
    ```

    Now, run the EDA [installer][makefile]:

    ```bash
    make try-eda
    ```

    The installation will take approximately 10 minutes to complete.

    /// details | EDA License
        type: info
    As you may have noticed, the EDA Playground installation does not require a license. We wanted to ensure that automation with EDA is accessible to everyone, anytime.  
    The EDA system can perfectly run without a license with the following caveats:

    * Only the nodes inside the EDA's Digital Twin can be used. These include the SR Linux nodes that will be deployed for you by the time `make try-eda` step finishes as well as any 3rd party vendors supported by EDA's Digital Twin. No hardware nodes can be used in an unlicensed EDA mode[^5].
    * No [integration](../apps/connect/index.md) with the cloud systems such as OpenShift, VMware, etc.
    ///

6. **Access the UI**

    EDA is an API-first framework, with its UI being a client of the very same API. After the `make try-eda` finishes, you will be able to access the EDA UI using the address printed in the terminal:

    ```shell
    --> The UI can be accessed using https://10.10.1.1:9443 #(1)!
    --> INFO: EDA is launched
    ```

    1. Instead of `10.10.1.1` IP you may see the IP address of the VM/Server where you installed EDA Playground or its hostname. You can use any address that resolves to the VM/Server hosting the Try EDA installation, not only the one printed in the terminal.
  
    Open your web browser and navigate to provided URL to access the EDA UI. As you would expect, credentials are required in order to log in.
    The default credentials are as follow:

    * Username: `admin`  
    * Password: `admin`

///

And that's it! You now have a fully functional EDA instance suitable for learning, development, and demonstration that comes preloaded with a small, but functional Digital Twin network topology.

-{{ js_script("/javascripts/viewer-static.min.js") }}-

-{{ diagram(path='./diagrams/digital-twin.drawio', title='', page=0, zoom=1.2) }}-

With Try EDA up and running, you are all set to embark on your EDA journey by following our [Tour Of EDA](../tour-of-eda/index.md) exercises or explore EDA on your own.

<div class="grid cards" markdown>

* :fontawesome-solid-route:{ .middle } **The Tour Of EDA**

    ---

    Learning by doing is the best way to get familiar with the EDA capabilities. Our Tour Of EDA offers a collection of hands-on exercises everyone can run on their Try EDA instance to learn the basics of EDA.

    [:octicons-arrow-right-24: Start the tour](../tour-of-eda/index.md)

* :material-hammer-screwdriver:{ .middle } **Production Installation**

    ---

    For a production installation instructions, please refer to the Software Installation document.

    [:octicons-arrow-right-24: Software Installation](../software-install/index.md)

</div>

<h2> Resetting the Playground</h2>

To start afresh, or to shut down your playground, run the following command:

```shell
make teardown-cluster
```

This will remove the KinD cluster and all the resources created by the EDA Playground.

Next remove the existing `kpt` packages and build artifacts:

```shell
rm -rf eda-kpt build
```

And you are ready to start over!

## Try Nokia EDA in Codespaces

Even though all it takes to Try EDA on your own compute is a couple of commands, nothing beats an environment that one can run without fronting the hardware, anytime, with a single click and {==for free==}.

EDA in Codespaces is exactly that - the real "Try EDA" installation in a free[^5], cloud-based VM, available to everyone with a single-click spin up. All you need is a GitHub account and a web browser.

Here is how it works. When you see the "Run in Codespaces" button somewhere in our docs or in one of the repositories it invites you to spin up the EDA environment in the Github Codespaces.

<div align=center markdown>
<a href="https://github.com/codespaces/new?repo=1129099670&ref=main">
<img src="https://gitlab.com/-/project/7617705/uploads/3f69f403e1371b3b578ee930df8930e8/codespaces-btn-4vcpu-export.svg"/></a>

**Run EDA in Codespaces for free**.  
<small>Machine type: 4 vCPU · 16 GB RAM</small>
</div>

Clicking on a button will open up a GitHub web page asking you to confirm the creation of a Codespaces environment. Once you confirm, a VS Code window will open in your browser, and the EDA installation will kick off. Depending on the performance of the Codespaces VM, it may take anywhere between 10 to 20 minutes to have the full EDA environment up and running.

When the installation is complete, you will see the EDA welcome message in the terminal window, and the EDA GUI URL will be printed out for you to open in a separate browser tab. Now everything is ready, and you can start using EDA in your browser.

-{{video(url="https://gitlab.com/-/project/7617705/uploads/5a1460fb3e94efc4f557b632ad5c0ab3/eda-cs-demo.mp4", title="EDA in Codespaces demo")}}-

In the VS Code window in your browser you have the full access to the terminal where we preinstalled some EDA tools like `edactl`, `kubectl`, `k9s` and you can install other tools as you see fit. The Codespaces environment is a Debian Linux VM in the cloud, so you can use it as you would use any other Linux machine.

### Is It Free?

The best part about the [Github Codespaces][codespaces-doc] is that it offers a generous free tier - **120 cpu-hours for free each month**[^6] to all GitHub users. The "EDA in Codespaces" uses the 4vcpu/16GB RAM machine type, which means that you can run the EDA environment for 30 hours each month. For free.

The cpu-hours counter is reset at the beginning of each calendar month, so you can use the free plan every month.

> By default each GitHub user has a **$0** spending limit, and no payment method is required to start using Codespaces. You won't be charged unless you explicitly add a payment method and increase your spending limit.

[:octicons-arrow-right-24: Learn more about running EDA in Codespaces](../software-install/non-production/codespaces.md)

[codespaces-doc]: https://github.com/features/codespaces

[playground-repo]: https://github.com/nokia-eda/playground

[makefile]: https://github.com/nokia-eda/playground/blob/main/Makefile

[^1]: As no other framework of comparable scale.
[^2]: This as well accounts for the [virtual network topology that comes with the Playground](../tour-of-eda/nodes.md). Running a bigger topology or changing the node types may require more resources.
[^3]: Many distributions come with `git` preinstalled, but if not you should install it via your package manager.  
    For instance with `apt`-enabled systems:

    ```shell
    sudo apt install -y git
    ```

[^4]: You can provide the LLM key after the installation as well.
[^5]: Containerlab-deployed SR Linux nodes are planned to be supported in the unlicensed mode in the future.
[^5]: Limited by the free tier offered by GitHub Codespaces.
[^6]: The terms of the free plan may be subject to change, consult with the [official documentation](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#monthly-included-storage-and-core-hours-for-personal-accounts) for the current terms and conditions.
