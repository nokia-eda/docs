# Air-gapped setup

In case the installation will be Air-gapped, this section provides steps on how to set up the Assets VM and load it with the necessary assets for deploying EDA in an Air-gapped environment.

## Conceptual Overview

In an Air-Gapped environment, an Assets VM is deployed that will provide the services that will serve the container images, git repositories and artifacts used during installation of the EDA Talos Kubernetes cluster and EDA itself.

The goal of the Air-Gapped solution design is to allow flexibility in the deployment and content of the Assets VM in the Air-Gapped environment. By providing a standalone Assets VM without any assets automatically included, there is freedom of choice of what assets are uploaded to the Assets VM.

It allows for a single Assets VM to be used for multiple deployments and versions of EDA, as the assets for multiple versions of EDA can be uploaded to the same Assets VM.

Similarly, by splitting up the assets in bundles, it is possible to only upload specific content to the Assets VM. The bundle concept also allows for the creation of custom bundles, for instance for 3rd party Apps, so they can also be hosted on the Assets VM.

## Environments

Two environments will be discussed and used in an air-gapped installation:

*Public Environment*
: This environment has internet access. You use a system with Internet access to create the Assets VM image and to download all the necessary assets and tools.

*Air-Gapped Environment*
: This environment that does not have internet access. It is the environment in which EDA is deployed.

In each environment, you must have a system from which you can execute the steps. You can use a system to first connect to the internet, execute the steps for the public network and then move the same system to the Air-Gapped environment to continue. Or, you can have two systems, and you would copy the data from the public system to the Air-Gapped system. More details on the requirements for these systems are included later in this document.

For each section, there will be a note in which environment the section applies.
