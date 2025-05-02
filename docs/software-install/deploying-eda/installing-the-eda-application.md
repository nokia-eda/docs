# Installing the EDA application

After setting up EDA nodes and bootstrapping the Talos Kubernetes cluster, you can now install Nokia EDA applications using the playground repository [cloned during the preparation phase](../preparing-for-installation.md#download-the-eda-installation-playground).

## Customizing the installation file

Change into the playground directory and update the parameters in the [`prefs.mk`][prefs-file] file found at the directory's root to control the way EDA is installed.

[prefs-file]: https://github.com/nokia-eda/playground/blob/main/prefs.mk

Customizable parameters in the `prefs.mk` file:

/// html | table
//// html | th[style='text-align: center;']
Parameter
////
//// html | th[style='text-align: center;']
Description
////

//// html | tr
///// html | td
`NO_KIND`
/////
///// html | td
When set to any non-zero value will skip the KinD cluster deployment used for lab/demo installations.  
Must be set to 1 for production installation.
/////
////

//// html | tr
///// html | td
`METALLB_VIP`
/////
///// html | td
Specifies the VIP address of your EDA deployment. Make sure to use a CIDR format, preferably as a /32 (or /128 for an IPv6 VIP).

If you use two networks, this VIP address must be the one used on the fabric management network. ​​If you use a single network, this setting must match the VIP address used for `​EXT_DOMAIN_NAME​` FQDN or IP.​

Example: `203.0.113.10/32`
/////
////

//// html | tr
///// html | td
`EXT_DOMAIN_NAME`
/////
///// html | td
The FQDN that resolves to the EDA VIP or the VIP itself.

This value must be the FQDN or VIP address that is used to access the UI. If you use two networks, this value must be the FQDN or IP address of the OAM network.
/////
////

//// html | tr
///// html | td
`EXT_HTTP_PORT`
/////
///// html | td
The HTTP port that the EDA UI/API should use to redirect to HTTPS.  
Set to 80.
/////
////

//// html | tr
///// html | td
`EXT_HTTPS_PORT`
/////
///// html | td
The HTTPS port on which the EDA UI/API listens.  
Set to 443.
/////
////

//// html | tr
///// html | td
`EXT_IPV4_ADDR`
/////
///// html | td
The IPv4 IP address used as the VIP address.

If you use two networks, this VIP address must be the one used on the fabric management network.​ ​If you use a single network, this VIP address must be the VIP that matches your ​EXT_DOMAIN_NAME​ FQDN (or IP address).
/////
////

//// html | tr
///// html | td
`EXT_IPV6_ADDR`
/////
///// html | td
The IPv6 IP address used as the VIP.

If you use two networks, this VIP address must be the one used on the fabric management network.​ ​If you use a single network, this VIP address must be the VIP that matches your ​EXT_DOMAIN_NAME​ FQDN (or IP address).
/////
////

//// html | tr
///// html | td
`HTTPS_PROXY` and `https_proxy`
/////
///// html | td
Optional: The proxy address for the HTTPS proxy.
/////
////

//// html | tr
///// html | td
`HTTP_PROXY` and `http_proxy`
/////
///// html | td
Optional: The proxy address for the HTTP proxy.
/////
////

//// html | tr
///// html | td
`NO_PROXY` and `no_proxy`
/////
///// html | td
Optional: The list of IP addresses, IP ranges and hostnames that should not be proxied.
/////
////

//// html | tr
///// html | td
`LLM_API_KEY`
/////
///// html | td
Optional: The OpenAI API key for the EDA Natural Language Query functionality.
/////
////

//// html | tr
///// html | td
`SINGLESTACK_SVCS`
/////
///// html | td
Optional: Indicates that internal services should be single stack instead of dual stack, if Kubernetes is dual stack.  
Boolean.
/////
////

//// html | tr
///// html | td
`SIMULATE`
/////
///// html | td
Specifies if the EDA deployment is to manage simulated workloads (Digital Sandbox) or real hardware.

Values:

- `true` - EDA installation will manage only simulated nodes (Digital Sandbox)
- `false` - EDA installation will manage only real hardware nodes.

By default, this parameter is set to `true` if the parameter is not provided in the file.

////// caution
The simulation mode can't be changed post-install.
//////
/////
////

//// html | tr
///// html | td
`USE_ASSET_HOST`
/////
///// html | td
Must be set to `1` for an Air-gapped Installation and set to `0` for an Internet based installation. `0` is the default value if not set.
/////
////

//// html | tr
///// html | td
`ASSET_HOST`
/////
///// html | td
The IP address of the Assets VM for the Air-gapped installation.
/////
////

//// html | tr
///// html | td
`ASSET_HOST_GIT_USERNAME`
/////
///// html | td
The username for the git server running on the Asset VM. Needs to be set to `eda`, in the future this will be changeable.
/////
////

//// html | tr
///// html | td
`ASSET_HOST_GIT_PASSWORD`
/////
///// html | td
The password for the git server running on the Asset VM. Needs to be set to `eda`, in the future this will be changeable.
/////
////

//// html | tr
///// html | td
`ASSET_HOST_ARTIFACTS_USERNAME`
/////
///// html | td
The username for the artifact server running on the Asset VM. Needs to be set to `eda`, in the future this will be changeable.
/////
////

//// html | tr
///// html | td
`ASSET_HOST_ARTIFACTS_PASSWORD`
/////
///// html | td
The password for the artifact server running on the Asset VM. Needs to be set to `eda`, in the future this will be changeable.
/////
////

//// html | tr
///// html | td
`KPT_SETTERS_FILE`
/////
///// html | td
Advanced configuration file for kpt.
/////
////

///

## The `prefs.mk` file

You can find examples of the `prefs.mk` file contents for Internet based and Air-gapped installations:

/// tab | Internet based installation

```makefile
--8<-- "docs/software-install/resources/prefs-example.mk"
```

///
/// tab | Air-gapped installation

```makefile
--8<-- "docs/software-install/resources/prefs-example.mk"
USE_ASSET_HOST=1
ASSET_HOST=192.0.2.228
ASSET_HOST_GIT_USERNAME="eda"
ASSET_HOST_GIT_PASSWORD="eda"
ASSET_HOST_ARTIFACTS_USERNAME="eda"
ASSET_HOST_ARTIFACTS_PASSWORD="eda"
```

///

## Installing Nokia EDA

When the necessary parameters are set, follow these steps to install EDA.

/// admonition | Note
    type: subtle-note
Steps 1 and 2 can be skipped if these have already been executed during the [preparation phase](../preparing-for-installation.md#download-the-eda-installation-playground) of the installation procedure.
///

//// html | div.steps

1. Download the latest tools.

    ```bash
    make download-tools
    ```

2. Download the latest packages, including the eda-kpt package.

    ```bash
    make download-pkgs
    ```

3. Set up the [MetalLB](https://metallb.io/) environment for VIP management.

    ```bash
    make metallb
    ```

4. Install the necessary external packages.

    ```bash
    make install-external-packages
    ```

    /// admonition | Note
        type: subtle-note
    If this command exits with an error, wait 30 seconds and try again. Sometimes Kubernetes is a bit slower in reconciling the change than the command waits for.
    ///

5. Change the eda-git Kubernetes service to a ClusterIP service instead of a LoadBalancer type.

    ```bash
    kubectl -n eda-system patch service eda-git -p '{"spec": {"type": "ClusterIP"}}'
    ```

6. Generate the EDA core configuration.

    ```bash
    make eda-configure-core
    ```

7. Install EDA core components.

    ```bash
    make eda-install-core
    ```

    /// admonition | Note
        type: subtle-note
    If the command hangs for a long time (>5 minutes) on "reconcile pending" for a workflow definition, cancel the command and try again; KPT is designed to handle these cases. This can happen occasionally depending on the Kubernetes cluster.
    ///

8. Verify that the EDA Config Engine is up and running.

    ```bash
    make eda-is-core-ready
    ```

9. Install all the standard EDA apps.

    This step can take approximate 5 to 15 minutes, depending on your connectivity.

    ```bash
    make eda-install-apps
    ```

10. Bootstrap EDA.

    Bootstrapping will create base resources into the EDA cluster, such as IP pools.

    ```bash
    make eda-bootstrap
    ```

11. Configure two-networks deployment.

    If your deployment uses two networks, create a second VIP pool for the OAM VIP address.

    ```bash
    make metallb-configure-pools METALLB_VIP=<OAM VIP> LB_POOL_NAME=pool-nb
    ```

    And create the OAM UI/API service using the new VIP pool.

    ```bash
    make eda-create-api-lb-svc API_LB_POOL_NAME=pool-nb
    ```

12. Optional: Deploy an example topology.

    If you configured EDA to manage the simulated network (Digital Sandbox), you can load an example topology that will be instantiated as virtual simulators in the same EDA cluster by running:

    ```bash
    make topology-load
    ```

////

## Accessing the EDA deployment

You can now access the new EDA deployment using the following methods:

- use `https://OAM-VIP` if Virtual IP (VIP) was provided as `EXT_DOMAIN_NAME` in the preferences file used during the installation.
- if an FQDN is configured for the `EXT_DOMAIN_NAME` field, use `https://FQDN`

Both examples assume that `EXT_HTTPS_PORT` was set to `443` in the preferences file.
