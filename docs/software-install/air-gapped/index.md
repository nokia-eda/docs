# Air-gapped setup

-{{ js_script("/javascripts/viewer-static.min.js") }}-

The Nokia Event-Driven Automation platform can be installed in an air-gapped[^1] environment. This section describes the elements of the air-gapped setup and the steps required to set it up.

> If the installation **is not** targeting an air-gapped environment, proceed to [Deploying EDA](../deploying-eda/index.md).

Two environments will be discussed and used in an air-gapped installation:

*Public Environment*
: This environment has Internet access and is also commonly referred to as the *Connected Environment*. You use a system with Internet access to download all the necessary assets and tools for the air-gapped installation.

*Air-gapped Environment*
: This environment does not have Internet access and is also commonly referred to as the *Disconnected Environment*. It is the environment in which Nokia EDA platform is deployed.

The air-gapped installation process involves the following steps:

1. Download the necessary assets and tools (EDA core components and applications, tools and resources) for the air-gapped installation from the Internet.
2. Transfer the downloaded assets from the public environment to the air-gapped environment. You can do this by copying the downloaded assets to the Installer host in the air-gapped environment, or by transferring the entire Installer host from the public environment to the air-gapped environment.
3. Choose the hosting method for the downloaded assets and tools:
    1. Use the unified hosting services provided by the [EDA Assets VM](assets-vm.md). The Assets VM provides a container registry, Git server, and web server in a single VM package[^2].
    2. Reuse existing hosting services in the air-gapped environment.
    3. Combine both approaches.
4. Upload the downloaded assets and tools to the hosting services.
5. Deploy the EDA platform in the air-gapped environment.

-{{ diagram(path='./diagrams/air-gapped-install-steps.drawio', title='Air-gapped installation flow', page=0, zoom=1.0) }}-

The container images, Git repositories, and file artifacts used by the EDA platform are grouped into *asset bundles*, which are described in the [Asset bundles](asset-bundles.md) section.

[:octicons-arrow-right-24: Asset bundles](asset-bundles.md)

[^1]: An air-gapped environment is an environment that does not have network connectivity to and from the Internet.
[^2]: The [Assets VM](assets-vm.md) is deployed in the air-gapped environment before the EDA platform to provide hosting services for the assets.
