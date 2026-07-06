# Deploying on the OpenShift platform

Nokia Event-Driven Automation (EDA) can be installed on an existing Red Hat OpenShift cluster in either Internet-connected or air-gapped (disconnected) environments.

/// admonition | Note
    type: subtle-note
OpenShift-based installation is an alternative deployment model to the Talos-based installation covered in the [Deploying EDA](../deploying-eda/index.md) section.

Supported OpenShift versions: 4.20+

///

## Installation paths

Depending on the environment, the high-level installation steps are as follows:

//// tab | Internet-connected environment
/// html | div.steps

1. Install OpenShift  
    Install OpenShift 4.20+ using the standard OpenShift installation process.

2. Add OpenShift Security Context Constraint (SCC)  
    Apply the SCC resource prior to installing Nokia EDA. The SCC manifest is provided in the [nokia-eda/edaadm/openshift/eda-scc.yaml](https://github.com/nokia-eda/edaadm/blob/main/openshift/eda-scc.yaml) file.

3. [Deploy Nokia EDA](../deploying-eda/index.md)  
    Deploy Nokia EDA on the OpenShift cluster using the standard Nokia EDA installation process.
///
////

//// tab | Air-gapped environment
/// html | div.steps

1. Prepare the air-gapped EDA assets.

2. Install OpenShift 4.20+ in the air-gapped environment.

3. Configure the air-gapped OpenShift for Nokia EDA installation.

4. Install the Nokia EDA application.

///

See the [Installing Nokia EDA on OpenShift in an air-gapped environment](#installing-nokia-eda-on-openshift-in-an-air-gapped-environment) section for more details.
////

## Requirements

Before you begin, ensure the following requirements are met:

* The target OpenShift version is supported by Nokia EDA (4.20 or later).

    /// admonition | Note
    Nokia EDA releases up to and including 26.4 support OpenShift versions up to and including 4.22.
    ///

* You have cluster administrator access to the OpenShift environment.
* The air-gapped environment includes a mirror registry that supports OCI images with nested indices and is reachable by every OpenShift node.
* For air-gapped environments, the OpenShift API and application ingress DNS records are planned and configured prior to ISO generation.
* The [Nokia EDA SCC manifest](https://github.com/nokia-eda/edaadm/blob/main/openshift/eda-scc.yaml) is applied before Nokia EDA packages are installed.

## Installing Nokia EDA on OpenShift in an air-gapped environment

This procedure describes how to install the Nokia EDA application on OpenShift in an air-gapped environment.

/// html | div.steps

1. Prepare the air-gapped EDA assets  

    The default procedure to install OpenShift in a disconnected scenario uses the internal Quay container registry that does not support OCI images with nested indices[^1]. Therefore, you need to set up a compatible registry[^2] that supports such images or deploy the [EDA Assets Host](../air-gapped/deploying-the-assets-vm.md) that provides the required services.

    [Download](../air-gapped/downloading-the-assets.md) the Nokia EDA assets and upload them to the EDA Assets Host or to your existing registry, Git server, and web server.

2. Install OpenShift in the air-gapped environment  
    Follow the [OpenShift in a disconnected environment documentation][ocp-in-disconnected-environment] to install the cluster.

3. Configure OpenShift for Nokia EDA installation  
    The default OpenShift installation uses the internal registry, which does not support OCI images with nested indices. Therefore, you need to create a container registry that supports such images and configure OpenShift image mirrors targeting this registry.

    For example, if your registry endpoint is `registry.example.com:8443`, apply the following image tag mirror manifest to ensure that all required images are pulled from the configured registry.

    //// tab | YAML Resource

    ```yaml title="quay-tag-mirror.yaml"
    --8<-- "docs/software-install/resources/ocp-mirror-tag.yaml"
    ```

    ////

    //// tab | `oc apply` command

    ```bash
    oc apply -f - <<EOF
    --8<-- "docs/software-install/resources/ocp-mirror-tag.yaml"
    EOF
    ```

    ////

    Apply the SCC manifest to the OpenShift cluster.

    ```bash
    oc apply -f https://raw.githubusercontent.com/nokia-eda/edaadm/main/openshift/eda-scc.yaml
    ```

4. Install the Nokia EDA application  
    Use the procedure described in [Installing the EDA application](../deploying-eda/installing-the-eda-application.md) to install Nokia EDA on the Kubernetes cluster running on OpenShift.

///

[ocp-in-disconnected-environment]: https://docs.redhat.com/en/documentation/openshift_container_platform/4.20/html/disconnected_environments/index

[^1]: The Quay registry (v3.12.14) used with OpenShift 4.20 did not support OCI images with nested indices. See https://github.com/quay/quay/pull/3721.
[^2]: For example, Harbor, Artifactory, ghcr.io, AWS ECR, GCR.
