# EDA on Windows (WSL)

Thanks to EDA's deployment model that uses Kubernetes, you can install EDA anywhere where a Kubernetes cluster can run. And Windows is no exception!  
Thanks to the [Windows Subsystem Linux](https://learn.microsoft.com/en-us/windows/wsl/install) (aka WSL). WSL allows Windows users to run a Linux distribution as a tightly-integrated VM.

## Installation prerequisites

### Hardware requirements

Before proceeding with the installation, users have to ensure they meet the hardware requirements for EDA Playground installation that are outlined in the [Try EDA](../../getting-started/try-eda.md) section:

--8<-- "docs/getting-started/try-eda.md:resources-reqs"

The CPU/Memory/Storage requirements should be available to the WSL virtual machine, and the default settings used by the WSL system may not be enough to meet those requirements.

Users can [fine tune the resource allocations](https://learn.microsoft.com/en-us/windows/wsl/wsl-config) for the WSL virtual machine to meet their needs. Make sure to allocate the required number of CPU/Memory/Storage resources to the WSL virtual machine.

### WSL version

An important prerequisite for installing EDA on WSL is to have WSL version at 2.5 version or later. Check what version of the WSL you have running on your Windows, by running the following command in the Windows terminal:

```shell
wsl --version
```

If the version is older than 2.5 you will need to upgrade it. At the time of this writing, the WSL version 2.5 is [available](https://github.com/microsoft/WSL/releases) as a pre-release, to update your WSL to the pre-release version, run the following:

```shell
wsl --update --pre-release
```

## WSL distributive

Windows offers you a choice of distributives you can install on WSL. While you can choose any Linux distributive, we can recommend running the [WSL-Containerlab](https://containerlab.dev/windows/#wsl-containerlab) distributive that has been preconfigured with tools like Docker engine.

Download the `.wsl` distributive file from the [releases page](https://github.com/srl-labs/wsl-containerlab/releases/latest) and simply double click on it to install WSL-Containerlab WSL distributive.

You should be able to see "Containerlab" as a program in your start menu, and by opening this program you will start the distributive.

## EDA installation

Once you are in the shell of a chosen WSL distributive, proceed with the EDA installation steps as laid out on the [Try EDA page](../../getting-started/try-eda.md). The only important difference is the value of the `EXT_DOMAIN_NAME` variable that the setup script will use to configure the access to the EDA instance.

With WSL you may install the EDA playground using the `localhost` value as your `EXT_DOMAIN_NAME`, for example the Step 5 from the [Try EDA page](../../getting-started/try-eda.md) would look like this:

```shell
export EXT_DOMAIN_NAME=localhost
make try-eda
```

## UI/API access

Once the installation of the EDA Playground is complete, you can start the UI/API port forward as outlined in Step 6 from the [Try EDA page](../../getting-started/try-eda.md).

If you used the `localhost` as your `EXT_DOMAIN_NAME` value, you can access the UI/API using the `https://localhost:9443` URL.
