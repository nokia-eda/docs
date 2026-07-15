# Hosting assets in the air-gapped environment

-{{ js_script("/javascripts/viewer-static.min.js") }}-

The Nokia EDA platform relies on three services being available during installation and operation:

1. Container registry - to store the container images for the EDA platform and its applications.
2. Git server - to host Git repositories containing EDA application catalogs.
3. Web server - to serve the file artifacts used by various EDA components (schema profiles, LLM-embeddings, and so forth).

In an air-gapped environment, these services can be provided in the following ways:

1. By deploying the [EDA Assets VM](assets-vm.md), which provides one or more of the required services. The Assets VM then runs the required services and makes them available to the EDA platform during installation and beyond.  
    We call the host serving the required services the *Assets Host*.
2. By providing the addresses and credentials to one or more of the existing services operated by the user.
3. By combining the two approaches - for example, deploying the EDA Assets VM to provide the container registry and Git server while using an existing web server to host file artifacts.

-{{ diagram(path='./diagrams/air-gapped-install-steps.drawio', title='Assets hosting options', page=1, zoom=1.0) }}-

## High availability considerations

Regardless of the chosen approach for hosting assets, the hosting services must remain available throughout the platform's lifetime. Continuous availability of these services is critical in the following scenarios:

- **Initial platform installation** - All required assets must be accessible during the installation process.
- **Workflow execution** - Container images must be pulled from the container registry when workflows are executed.
- **Node failure or maintenance events** - When a Kubernetes node becomes unavailable or is cordoned/drained, workloads are rescheduled onto other nodes.
- **Application installation or upgrade** - The Git repository hosting the application catalog must be available, along with the container registry hosting the corresponding application images.

/// warning | Load balancer/proxy requirements for high availability deployments
If the Assets Host or individual services run redundantly across multiple instances, clients must access those instances through a single DNS name or IP address. Configure the load balancer to route traffic to an appropriate asset-hosting service instance.

The load balancer service for the services hosting the assets is not provided by Nokia and needs to be deployed by the user.
///

## Requirements for user-provided hosting services

In case of user-provided hosting services, the following requirements must be met. When using the [Assets VM](assets-vm.md), these requirements are met by default.

### Container registry

Some EDA application packages use nested OCI image indexes to reference their operator and workflow container images. The registry must support nested image indexes as defined by the [OCI Image Format Specification v1.1](https://github.com/opencontainers/image-spec/blob/v1.1.1/image-index.md), including recursive `application/vnd.oci.image.index.v1+json` descriptors and `artifactType` fields.

Example container registries that support nested image indexes include GitHub Container Registry (GHCR), Docker Hub, Harbor, and Artifactory.

### Git server

For high-availability deployments using user-provided Git servers, at least two non-colocated Git servers must be available.

The Git server must support creating Git repositories.

### Web server

The web server must support serving static files and directories over HTTPS.
