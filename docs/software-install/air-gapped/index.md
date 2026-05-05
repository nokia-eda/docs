# Air-gapped setup

Nokia Event-Driven Automation platform can be installed in the air-gapped[^1] environment. This section describes the elements of the air-gapped setup and the steps required to set it up.

> In case the installation is **not** targeting the air-gapped environment, please proceed to the [Deploying EDA](../deploying-eda/index.md) section.

Two environments will be discussed and used in an air-gapped installation:

*Public Environment*
: This environment has Internet access. You use a system with Internet access to download all the necessary assets and tools for the air-gapped installation.

*Air-gapped Environment*
: This environment does not have Internet access. It is the environment in which Nokia EDA platform is deployed.

In each environment, you must have a system from which you can execute the steps. You can use a system to first connect to the Internet, execute the steps for the public environment and then move the same system to the air-gapped environment to continue. Or, you can have two systems, and you would copy the data from the public system to the air-gapped system. More details on the requirements for these systems are included later in this document.

For each section, there will be a note in which environment the section applies.

## Hosting services in air-gapped environment

Nokia EDA platform relies on three services to be available during the installation process:

* Container registry - to store the container images for the EDA platform and its applications.
* Git server - to host Git repositories containing EDA application catalogs.
* Web server - to serve the file artifacts used by various EDA components (schema profiles, LLM-embeddings, and so forth).

In an air-gapped environment, these components can be provided in two ways:

1. By deploying the EDA Assets VM that provides one or more of the required services. The Assets VM then runs the required services and makes them available to the EDA platform during the installation process and beyond.  
    We call the host serving the required services the *Assets Host*.
2. By providing the addresses and credentials to one or more of the existing services operated by the user.

> It is possible to use any combination of the two approaches, for instance to deploy the EDA Assets VM to provide the container registry and git server, and to use the existing web server for the file artifacts.

## Asset bundles

The goal of the air-gapped solution design is to allow users to choose which applications, resources and artifacts (colloquially referred to as "assets") to include in the air-gapped environment. This flexibility is provided by the air-gap bundles.

An air-gap bundle is a YAML file that defines a group of related assets. For instance, a bundle for the core components of EDA for a specific version, or a bundle of the standard applications for a specific version.

```yaml title="Example air-gap bundle for EDA core components version 25.12.4"
version: 1.0.0
name: core-25.12.4
assets:
  registries:
    - name: ghcr.io
      images:
        - name: nokia-eda/core/api-server
          tags:
            - 25.12.4
        - name: nokia-eda/core/appstore-server
          tags:
            - 25.12.4
        - name: nokia-eda/core/appstore-flow
          tags:
            - 25.12.4
# snipped for brevity
  repos:
    - remote: https://github.com/nokia-eda/playground.git
      name: playground
    - remote: https://github.com/nokia-eda/kpt.git
      name: kpt
    - remote: https://github.com/nokia-eda/catalog.git
      name: catalog
```

You can download the bundles using the [`edaadm`](../preparing-for-installation.md#download-edaadm-tools) CLI tool from the Internet, and then upload them to the Assets Host[^2] using the `edaadm` tool.  
The product comes with a [set of standard bundles](https://github.com/nokia-eda/edaadm/tree/main/bundles) and custom bundles can be created by the user.

Regardless of the approach used to host the services, your first step is to download the assets that will be used to deploy the EDA platform in the air-gapped environment.

[:octicons-arrow-right-24: Download the assets](downloading-the-assets.md)

[^1]: An air-gapped environment is an environment that does not have network connectivity to and from the Internet.
[^2]: An Asset Host can be provided by Nokia in the form of the EDA Assets VM, or by the user in the form of an existing service.
