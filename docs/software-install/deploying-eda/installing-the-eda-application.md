# Installing the EDA application

After setting up EDA nodes and bootstrapping the Talos Kubernetes cluster, you can now install Nokia EDA applications using the playground repository [cloned during the preparation phase](../preparing-for-installation.md#download-the-eda-installation-playground).

## Customizing the installation

The [Kpt][kpt-home] Kubernetes package manager is used to configure and install EDA components. As any other package manager, kpt packages can be customized to allow users to customize EDA installation according to their needs.

[kpt-home]: https://kpt.dev

### Preferences file

The most common customization options are provided in the [`prefs.mk`][prefs-file] preferences file you find at the playground directory's root.

[prefs-file]: https://github.com/nokia-eda/playground/blob/main/prefs.mk

This file contains customization parameters that you can set to adjust the essential installation parameters, such as the EDA version to install, the installation components to include, the Kubernetes namespace where EDA components are installed, proxy settings, the reachability settings for the EDA cluster, and so on.  
You will find the list of all the available parameters in the section below.

/// details | Customizable parameters in the `prefs.mk` file:
    type: subtle-note

/// html | table
//// html | th[style='text-align: center;']
Parameter
////
//// html | th[style='text-align: center;']
Description
////

//// html | tr
///// html | td[colspan="2"]
<h4>Namespace settings for EDA components</h4>
/////
////

//// html | tr
///// html | td[style='white-space: nowrap;']
`EDA_CORE_NAMESPACE`
/////
///// html | td
Sets the kubernetes namespace where the EDA core components are installed.

Default: `eda-system`
/////
////

//// html | tr
///// html | td
`EDA_USER_NAMESPACE`
/////
///// html | td
Sets the kubernetes and EDA namespace where the user components are installed.

Default: `eda`
/////
////

//// html | tr
///// html | td[colspan="2"]
<h4>Version selection for EDA packages</h4>
/////
////

//// html | tr
///// html | td
`EDA_CORE_VERSION`
/////
///// html | td
Version of the EDA core components to install.

Defaults to the latest stable version.
/////
////

//// html | tr
///// html | td
`EDA_APPS_VERSION`
/////
///// html | td
Version of the EDA applications to install.

Defaults to the latest stable version.
/////
////

//// html | tr
///// html | td[colspan="2"]
<h4>KinD cluster options</h4>
/////
////

//// html | tr
///// html | td
`NO_KIND`
/////
///// html | td
When set to any non-zero value will skip the KinD cluster deployment used for lab/demo installations.  
Must be set to `yes` for production installation.
/////
////

//// html | tr
///// html | td
`KIND_CONFIG_FILE`
/////
///// html | td
Path to the KinD configuration file.

Default: `configs/kind.yaml` - the path to the KinD configuration file in the playground directory.
/////
////

//// html | tr
///// html | td
`KIND_CLUSTER_NAME`
/////
///// html | td
Name of the KinD cluster.

Default: `eda-demo`.
/////
////

//// html | tr
///// html | td
`KIND_API_SERVER_ADDRESS`
/////
///// html | td
IP address to use for the KinD API server. If you want to reach your cluster from outside of the host machine, you must set this to the IP address of the host machine.

Default: `127.0.0.1`.
/////
////

//// html | tr
///// html | td
`NO_HOST_PORT_MAPPINGS`
/////
///// html | td
When set to `yes` will not create the extra port mappings in the KinD cluster and will not create the nodePort service to expose the EDA UI/API.

Default: variable is not set. Results in port mappings and nodePort service being created.
/////
////

//// html | tr
///// html | td[colspan="2"]
<h4>Cluster reachability settings</h4>
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
///// html | td[colspan="2"]
<h4>Proxy settings</h4>
/////
////

//// html | tr
///// html | td
`HTTPS_PROXY`  
and `https_proxy`
/////
///// html | td
Optional: The proxy address for the HTTPS proxy.
/////
////

//// html | tr
///// html | td
`HTTP_PROXY`  
and `http_proxy`
/////
///// html | td
Optional: The proxy address for the HTTP proxy.
/////
////

//// html | tr
///// html | td
`NO_PROXY`  
and `no_proxy`
/////
///// html | td
Optional: The list of IP addresses, IP ranges and hostnames that should not be proxied.
/////
////

//// html | tr
///// html | td[colspan="2"]
<h4>Asset host settings</h4>
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
///// html | td[style='white-space: nowrap;']
`ASSET_HOST_ARTIFACTS_PASSWORD`
/////
///// html | td
The password for the artifact server running on the Asset VM. Needs to be set to `eda`, in the future this will be changeable.
/////
////

//// html | tr
///// html | td[colspan="2"]
<h4>KPT settings</h4>
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

//// html | tr
///// html | td
`KPT_LIVE_INIT_FORCE`
/////
///// html | td
Set to `1` to ignore if a kpt package was already initialized against a cluster. Results in an overwrite of the existing inventory (resource group).

Default: `0`
/////
////

//// html | tr
///// html | td
`KPT_INVENTORY_ADOPT`
/////
///// html | td
Set to `1` to adopt already applied and unmanaged resources that the kpt package is trying to clear, it will update/reconcile any differences.

Default: `0`
/////
////

//// html | tr
///// html | td[colspan="2"]
<h4>External packages settings</h4>
/////
////

//// html | tr
///// html | td
`NO_CERT_MANAGER_INSTALL`
/////
///// html | td
Set to `yes` to skip the installation of the Cert Manager package. This is useful if you want to use an existing Cert Manager running in the `cert-manager` namespace.

Default: unset - the Cert Manager package is installed.
/////
////

//// html | tr
///// html | td
`NO_CSI_DRIVER_INSTALL`
/////
///// html | td
Set to `yes` to skip the installation of the Cert Manager's CSI driver. This is useful if you want to use an existing Cert Manager CSI driver running in the `cert-manager` namespace.

Default: unset - the Cert Manager CSI driver package is installed.
/////
////

//// html | tr
///// html | td
`NO_EDA_ISSUER_API_INSTALL`
/////
///// html | td
Set to `yes` to skip the installation of the certificate issuers for EDA.

Default: unset - the EDA certificate issuers are installed.
/////
////

//// html | tr
///// html | td[colspan="2"]
<h4>Other settings</h4>
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

///

///

You can find examples of the `prefs.mk` file contents for Internet based and Air-gapped installations for your reference:

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

### Kpt setters

For the most part, the `prefs.mk` file is just a hand-picked selection of the most common customization options that the installation procedure passes over to the Kpt package manager.

In Kpt, the customization of packages is done by setting the values of the parameters marked with the `kpt-set` annotation. Consider the [Catalog manifest](https://github.com/nokia-eda/kpt/blob/main/eda-kpt-base/appstore-gh/catalog.yaml) from the `eda-kpt-base` package:

```yaml hl_lines="8"
apiVersion: appstore.eda.nokia.com/v1
kind: Catalog
metadata:
  name: eda-catalog-builtin-apps
  namespace: eda-system # kpt-set: ${EDA_CORE_NAMESPACE}
spec:
  title: EDA built in apps catalog
  remoteURL: https://github.com/nokia-eda/catalog.git # kpt-set: ${APP_CATALOG}
  authSecretRef: gh-catalog
```

The `# kpt-set: ${APP_CATALOG}` annotation indicates that the `.spec.remoteURL` value of the manifest can be overwritten using the `APP_CATALOG` Kpt setter.

When you use the `prefs.mk` file and set the values for the variables exposed there you essentially provide the Kpt setters values, that will be used to customize the Kpt packages during the installation. However, the `prefs.mk` file exposes only a limited set of variables, while there are many more Kpt setters available in the EDA Kpt packages.

EDA uses three Kpt packages published in the [`nokia-eda/kpt`][kpt-repo] repository:

[kpt-repo]: https://github.com/nokia-eda/kpt

- `eda-external-packages` - the package that contains the external packages used by EDA, such as Fluentd and Cert Manager.
- `eda-kpt-base` - the core package that contains the EDA components, such as the Config Engine, the necessary secrets and configmaps.
- `eda-kpt-playground` - the package that contains the EDA resources that bootstrap your EDA cluster with the node profiles, allocation pools and node users.

Each package has its own set of Kpt setters that you can choose to use to overwrite the default values in the manifests. You will find the complete list of setters and the default values in the block below.

/// details | Kpt setters reference
    type: subtle-note

> Run `make list-kpt-setters-external-packages`, `make list-kpt-setters-core` or `make list-kpt-setters-playground` to see the list of setters for the respective package in your terminal and their current values.

//// tab | eda-external-packages

| Name | Current Value |
|------|---------------|
| **eda-external-packages/cert-manager/cert-manager.yaml** ||
| `CORE_IMG_CREDENTIALS` | core |
| `CMCA_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-cainjector:v1.16.2" |
| `CMCT_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-controller:v1.16.2" |
| `CM_ARGS` | Non scalar value, see the file for details. |
| `CMWH_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-webhook:v1.16.2" |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/csi-driver/cert-manager-csi-driver.in.yaml** ||
| `EDA_CORE_NAMESPACE` | eda-system |
| `CSI_REGISTRAR_IMG` | "ghcr.io/nokia-eda/ext/sig-storage/csi-node-driver-registrar:v2.12.0" |
| `CSI_LIVPROBE_IMG` | "ghcr.io/nokia-eda/ext/sig-storage/livenessprobe:v2.12.0" |
| `CSI_DRIVER_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-csi-driver:v0.10.1" |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/eda-api-ingress-https-passthrough/api-ingress-ssl-passthrough.yaml** ||
| `EXT_DOMAIN_NAME` | "" |
| `INT_HTTPS_PORT` | 443 |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/eda-api-ingress-https/eda-api-ingress-cert.yaml** ||
| `EXT_IPV4_ADDR` | "" |
| `EXT_IPV6_ADDR` | "" |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/fluentd/fluentd-bit-ds.yaml** ||
| `FB_IMG` | ghcr.io/nokia-eda/core/fluent-bit:3.0.7-amd64 |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/fluentd/fluentd.yaml** ||
| `FD_IMG` | ghcr.io/nokia-eda/core/fluentd:v1.17.0-debian-1.0 |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/git-no-pvc/gogs-admin-user.yaml** ||
| `EDA_GOGS_NAMESPACE` | eda-system |
| `GOGS_ADMIN_USER` | ZWRhCg== |
| `GOGS_ADMIN_PASS` | ZWRhCg== |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/git-no-pvc/gogs-deployment-no-pvc.yaml** ||
| `GOGS_IMG_TAG` | ghcr.io/nokia-eda/core/gogs:0.13.0 |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/git-no-pvc/gogs-replica-service.yaml** ||
| `GIT_SVC_TYPE` | ClusterIP |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/git/gogs-pv-claim.yaml** ||
| `GOGS_PV_CLAIM_SIZE` | 24Gi |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/git/gogs-replica-pv-claim.yaml** ||
| `GOGS_REPLICA_PV_CLAIM_SIZE` | 24Gi |

| Name | Current Value |
|------|---------------|
| **eda-external-packages/trust-manager/trust-manager.yaml** ||
| `EDA_TRUSTMGR_NAMESPACE` | eda-system |
| `TRUSTMGRBUNDLE_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-package-debian:20210119.0" |
| `TRUSTMGR_IMG` | "ghcr.io/nokia-eda/ext/jetstack/trust-manager:v0.15.0" |
| `TRUSTMGR_ARGS` | Non scalar value, see the file for details. |
| `EDA_TRUSTMGR_ISSUER_DNSNAMES` | Non scalar value, see the file for details. |
////
//// tab | eda-kpt-base
| Name | Current Value |
|------|---------------|
| **eda-kpt-base/appstore-gh/catalog-secret.yaml** ||
| `GH_CATALOG_TOKEN` | SomeCatalogToken |
| `GH_CATALOG_USER` | bm9raWEtZWRhLWJvdA== |
| `EDA_CORE_NAMESPACE` | eda-system |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/appstore-gh/catalog.yaml** ||
| `APP_CATALOG` | https://github.com/nokia-eda/catalog.git |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/appstore-gh/registry-secret.yaml** ||
| `GH_REGISTRY_TOKEN` | SomeRegistryToken |
| `GH_REGISTRY_USER` | bm9raWEtZWRhLWJvdA== |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/appstore-gh/registry.yaml** ||
| `APP_REGISTRY` | ghcr.io |
| `APP_REGISTRY_SKIPTLSVERIFY` | false |
| `APP_REGISTRY_MIRROR` | "" |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/core/apps/bootstrap.yaml** ||
| `INT_DHCPV6_PORT` | 547 |
| `INT_DHCPV4_PORT` | 67 |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/core/apps/ce-deployment.yaml** ||
| `CORE_IMG_CREDENTIALS` | core |
| `CE_IMG` | ghcr.io/nokia-eda/core/config-engine:25.4.3 |
| `CE_LIMIT_CPU` | "2" |
| `CE_LIMIT_MEM` | "2Gi" |
| `CE_REQ_CPU` | "1" |
| `CE_REQ_MEM` | "1Gi" |
| `HTTP_PROXY` | "" |
| `HTTPS_PROXY` | "" |
| `NO_PROXY` | "" |
| `http_proxy` | "" |
| `https_proxy` | "" |
| `no_proxy` | "" |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/core/apps/cxdp-image-config-map.yaml** ||
| `CXDP_IMG` | ghcr.io/nokia-eda/core/cxdp:25.4.3 |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/eda-toolbox/eda-toolbox-deployment.yaml** ||
| `EDA_TOOLBOX_IMG` | ghcr.io/nokia-eda/core/eda-toolbox:25.4.3 |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/engine-config/engineconfig.yaml** ||
| `CLUSTER_MEMBER_NAME` | engine-config |
| `GIT_SERVERS` | Non scalar value, see the file for details. |
| `EXT_DOMAIN_NAME` | "" |
| `EXT_HTTP_PORT` | 0 |
| `EXT_HTTPS_PORT` | 0 |
| `EXT_IPV4_ADDR` | "" |
| `EXT_IPV6_ADDR` | "" |
| `INT_HTTP_PORT` | 80 |
| `INT_HTTPS_PORT` | 443 |
| `GIT_REPO_CHECKPOINT` | /eda/customresources.git |
| `GIT_REPO_APPS` | /eda/apps.git |
| `GIT_REPO_USER_SETTINGS` | /eda/usersettings.git |
| `GIT_REPO_SECURITY` | /eda/credentials.git |
| `GIT_REPO_IDENTITY` | /eda/identity.git |
| `ASVR_IMG` | ghcr.io/nokia-eda/core/artifact-server:25.4.3 |
| `ASVR_LIMIT_CPU` | "" |
| `ASVR_LIMIT_MEM` | "" |
| `ASVR_REQ_CPU` | "" |
| `ASVR_REQ_MEM` | "" |
| `BSVR_IMG` | ghcr.io/nokia-eda/core/bootstrap-server:25.4.3 |
| `BSVR_LIMIT_CPU` | "" |
| `BSVR_LIMIT_MEM` | "" |
| `BSVR_REQ_CPU` | "" |
| `BSVR_REQ_MEM` | "" |
| `ECC_IMG` | ghcr.io/nokia-eda/core/cert-checker:25.4.3 |
| `ECC_LIMIT_CPU` | "" |
| `ECC_LIMIT_MEM` | "" |
| `ECC_REQ_CPU` | "" |
| `ECC_REQ_MEM` | "" |
| `CX_IMG` | ghcr.io/nokia-eda/core/cx:25.4.3 |
| `CX_LIMIT_CPU` | "" |
| `CX_LIMIT_MEM` | "" |
| `CX_REQ_CPU` | "" |
| `CX_REQ_MEM` | "" |
| `CXCLUSTER_ISAGENT` | false |
| `CXCLUSTER_ADDR` | eda-cx-standalone |
| `CXCLUSTER_PORT` | 52200 |
| `EMS_IMG` | ghcr.io/nokia-eda/core/metrics-server:25.4.3 |
| `EMS_LIMIT_CPU` | "" |
| `EMS_LIMIT_MEM` | "" |
| `EMS_REQ_CPU` | "" |
| `EMS_REQ_MEM` | "" |
| `NPP_IMG` | ghcr.io/nokia-eda/core/npp:25.4.3 |
| `NPP_LIMIT_CPU` | "" |
| `NPP_LIMIT_MEM` | "" |
| `NPP_REQ_CPU` | "" |
| `NPP_REQ_MEM` | "" |
| `SE_IMG` | ghcr.io/nokia-eda/core/state-engine:25.4.3 |
| `SE_REPLICAS` | 1 |
| `SE_LIMIT_CPU` | "" |
| `SE_LIMIT_MEM` | "" |
| `SE_REQ_CPU` | "" |
| `SE_REQ_MEM` | "" |
| `SA_IMG` | ghcr.io/nokia-eda/core/state-aggregator:25.4.3 |
| `SA_REPLICAS` | 1 |
| `SA_LIMIT_CPU` | "" |
| `SA_LIMIT_MEM` | "" |
| `SA_REQ_CPU` | "" |
| `SA_REQ_MEM` | "" |
| `SC_IMG` | ghcr.io/nokia-eda/core/state-controller:25.4.3 |
| `SC_LIMIT_CPU` | "" |
| `SC_LIMIT_MEM` | "" |
| `SC_REQ_CPU` | "" |
| `SC_REQ_MEM` | "" |
| `FE_IMG` | ghcr.io/nokia-eda/core/flow-engine:25.4.3 |
| `FE_LIMIT_CPU` | "" |
| `FE_LIMIT_MEM` | "" |
| `FE_REQ_CPU` | "" |
| `FE_REQ_MEM` | "" |
| `API_IMG` | ghcr.io/nokia-eda/core/api-server:25.4.3 |
| `API_REPLICAS` | 1 |
| `API_SVC_ENABLE_LB_NODE_PORTS` | false |
| `API_LIMIT_CPU` | "" |
| `API_LIMIT_MEM` | "" |
| `API_REQ_CPU` | "" |
| `API_REQ_MEM` | "" |
| `ASC_IMG` | ghcr.io/nokia-eda/core/appstore-server:25.4.3 |
| `ASC_LIMIT_CPU` | "" |
| `ASC_LIMIT_MEM` | "" |
| `ASC_REQ_CPU` | "" |
| `ASC_REQ_MEM` | "" |
| `ASF_IMG` | ghcr.io/nokia-eda/core/appstore-flow:25.4.3 |
| `TM_IMG` | ghcr.io/nokia-eda/core/testman:25.4.3 |
| `TM_LIMIT_CPU` | "" |
| `TM_LIMIT_MEM` | "" |
| `TM_REQ_CPU` | "" |
| `TM_REQ_MEM` | "" |
| `KC_IMG` | ghcr.io/nokia-eda/core/eda-keycloak:25.4.3 |
| `KC_LIMIT_CPU` | "" |
| `KC_LIMIT_MEM` | "" |
| `KC_REQ_CPU` | "" |
| `KC_REQ_MEM` | "" |
| `PG_IMG` | ghcr.io/nokia-eda/core/eda-postgres:25.4.3 |
| `PG_LIMIT_CPU` | "" |
| `PG_LIMIT_MEM` | "" |
| `PG_REQ_CPU` | "" |
| `PG_REQ_MEM` | "" |
| `LLM_API_KEY` | "" |
| `LLM_MODEL` | gpt-4o |
| `SIMULATE` | true |
| `SINGLESTACK_SVCS` | false |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/namespaces/eda.yaml** ||
| `EDA_USER_NAMESPACE` | eda |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/secrets/identity-realm-auth.yaml** ||
| `SECRET_EDA_ADMIN_USERNAME` | YWRtaW4= |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/secrets/keycloak-admin-secret.yml** ||
| `SECRET_KC_ADMIN_USERNAME` | YWRtaW4= |
| `SECRET_KC_ADMIN_PASSWORD` | YWRtaW4= |

| Name | Current Value |
|------|---------------|
| **eda-kpt-base/secrets/postgres-db-secret.yml** ||
| `SECRET_PG_DB_USERNAME` | cG9zdGdyZXM= |
| `SECRET_PG_DB_PASSWORD` | cGFzc3dvcmQ= |
////

//// tab | eda-kpt-playground

| Name | Current Value |
|------|---------------|
| **eda-kpt-playground/allocations/asn-pool.yaml** ||
| `EDA_USER_NAMESPACE` | eda |

| Name | Current Value |
|------|---------------|
| **eda-kpt-playground/cx/cx-cxdp-init.yaml** ||
| `EDA_CORE_NAMESPACE` | eda-system |

| Name | Current Value |
|------|---------------|
| **eda-kpt-playground/srlinux-ghcr-24.10.1/engine_v1_nodeprofile_srlinux_24.10.1.yaml** ||
| `SRL_24_10_1_GHCR` | ghcr.io/nokia/srlinux:24.10.1-492 |
| `CORE_IMG_CREDENTIALS` | core |

| Name | Current Value |
|------|---------------|
| **eda-kpt-playground/srlinux-ghcr-24.10.1/llm-embeddings-db-srlinux-24.10.1.yaml** ||
| `LLM_DB_REMOTE_URL` | https://github.com/nokia-eda/llm-embeddings/releases/download/nokia-srl-v24.10.1/llm-embeddings-srl-24-10-1.tar.gz |

| Name | Current Value |
|------|---------------|
| **eda-kpt-playground/srlinux-ghcr-24.10.1/yang-srlinux-24.10.1.yaml** ||
| `YANG_REMOTE_URL` | https://github.com/nokia/srlinux-yang-models/releases/download/v24.10.1/srlinux-24.10.1-492.zip |

| Name | Current Value |
|------|---------------|
| **eda-kpt-playground/srlinux-ghcr-24.10.2/engine_v1_nodeprofile_srlinux_24.10.2.yaml** ||
| `SRL_24_10_2_GHCR` | ghcr.io/nokia/srlinux:24.10.2-357 |

| Name | Current Value |
|------|---------------|
| **eda-kpt-playground/srlinux-ghcr-24.10.3/engine_v1_nodeprofile_srlinux_24.10.3.yaml** ||
| `SRL_24_10_3_GHCR` | ghcr.io/nokia/srlinux:24.10.3-201 |

| Name | Current Value |
|------|---------------|
| **eda-kpt-playground/srlinux-ghcr-24.10.4/engine_v1_nodeprofile_srlinux_24.10.4.yaml** ||
| `SRL_24_10_4_GHCR` | ghcr.io/nokia/srlinux:24.10.4-244 |

| Name | Current Value |
|------|---------------|
| **eda-kpt-playground/srlinux-ghcr-25.3.2/engine_v1_nodeprofile_srlinux_25.3.2.yaml** ||
| `SRL_25_3_2_GHCR` | ghcr.io/nokia/srlinux:25.3.2-312 |
////
///

If you need to customize the installation besides the parameters provided in the `prefs.mk` file, you should create the YAML file with the Kpt setters key/value pairs that follows the Kpt setters format like this:

```yaml title="<code>my-setters.yml</code>"
apiVersion: v1
kind: ConfigMap #(1)!
metadata:
  name: my-setters
data:
  GOGS_REPLICA_PV_CLAIM_SIZE: 10Gi #(2)!
  # add more setters if required
```

1. The setters file resembles a K8s ConfigMap resource, but it is not applied to your cluster, it is only used by the kpt tool to read the values from it.
2. The setter's key must match the name of the setter variable in the manifest file.

Now that you have your setters file with the necessary values, you should set the path to it in the preferences file:

```makefile
KPT_SETTERS_FILE := my-setters.yml
```

And that's it! The kpt will read the values from the setters file and apply them to the manifests when you run the installation commands.

### Credentials and secrets

Nokia EDA platform uses a set of credentials to authenticate and authorize access to various components. These credentials are set to their respective default values and can be modified pre and post installation. The tables below lists the components, the associated credentials and the matching [Kpt setters](#kpt-setters) that an admin can use to customize them at the installation time.

#### Git

| Component | Default value | Kpt Setter | Notes
|-----------|------------|------------| -- |
| Internal Git server (Gogs) admin username  | `eda` | `GOGS_ADMIN_USER` | Sets the username for the internal Git server. Not applicable if an external Git server is used. <small>Base64 encoded</small> |
| Internal Git server (Gogs) admin password  | `eda` | `GOGS_ADMIN_PASS` | Same note as for the admin username. <small>Base64 encoded</small> |
| Config Engine Git username  | `eda` | `CE_GIT_USERNAME` | Should match the Git server admin username. <small>Base64 encoded</small> |
| Config Engine Git password  | `eda` | `CE_GIT_PASSWORD` | Should match the Git server admin password. <small>Base64 encoded</small> |

In case the value of `GOGS_ADMIN_USER`/`CE_GIT_USERNAME` was changed, make sure to set the setters for the repository paths as per the table below. The path values are provided as raw text values.

| Component | Default value | Kpt Setter | Notes
|-----------|------------|------------| -- |
| Custom resources repo  | `/eda/customresources.git` | `GIT_REPO_CHECKPOINT` |  |
| Apps repo  | `/eda/apps.git` | `GIT_REPO_APPS` |  |
| User settings repo  | `/eda/usersettings.git` | `GIT_REPO_USER_SETTINGS` |  |
| Credentials repo  | `/eda/credentials.git` | `GIT_REPO_SECURITY` |  |
| Identity repo  | `/eda/identity.git` | `GIT_REPO_IDENTITY` |  |

#### EDA user

EDA users are managed by the Keycloak identity provider and by default an admin user is created during the installation process. Using the following setter it is possible to change the default admin user password[^1].

| Component | Default value | Kpt Setter | Notes
|-----------|------------|------------| -- |
| EDA admin password  | `admin` | `SECRET_EDA_ADMIN_PASSWORD` | <small>Base64 encoded</small> |

#### Keycloak

The Keycloak identity provider is managed by its own admin user and its credentials can be customized using the following setters:

| Component | Default value | Kpt Setter | Notes
|-----------|------------|------------| -- |
| Keycloak admin username  | `admin` | `SECRET_KC_ADMIN_USERNAME` | <small>Base64 encoded</small> |
| Keycloak admin password  | `admin` | `SECRET_KC_ADMIN_PASSWORD` | <small>Base64 encoded</small> |

#### Postgres DB

Lastly, there is a postgres database used by the Keycloak. The database password can also be customized:

| Component | Default value | Kpt Setter | Notes
|-----------|------------|------------| -- |
| Postgres DB password  | `password` | `SECRET_PG_DB_PASSWORD` | <small>Base64 encoded</small> |

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

2. Set the desired EDA version. <small>(optional)</small>

    To install a specific version of EDA instead of the latest version, set the `EDA_CORE_VERSION` and `EDA_APPS_VERSION` variables in the [preferences file](#preferences-file). For example, to choose the -{{eda_version}}- version of EDA, add the following lines to the `prefs.mk` file:

    ```text
    EDA_CORE_VERSION=-{{eda_version}}-
    EDA_APPS_VERSION=-{{eda_version}}-
    ```

    In the current release, both variables must be set to the same version.

3. Download EDA packages.

    ```bash
    make download-pkgs
    ```

4. Set up the [MetalLB](https://metallb.io/) environment for VIP management.

    ```bash
    make metallb
    ```

5. Install the necessary external packages.

    ```bash
    make install-external-packages
    ```

    /// admonition | Note
        type: subtle-note
    If this command exits with an error, wait 30 seconds and try again. Sometimes Kubernetes is a bit slower in reconciling the change than the command waits for.
    ///

6. Change the eda-git Kubernetes service to a ClusterIP service instead of a LoadBalancer type.

    ```bash
    kubectl -n eda-system patch service eda-git -p '{"spec": {"type": "ClusterIP"}}'
    ```

7. Generate the EDA core configuration.

    ```bash
    make eda-configure-core
    ```

8. Install EDA core components.

    ```bash
    make eda-install-core
    ```

    /// admonition | Note
        type: subtle-note
    If the command hangs for a long time (>5 minutes) on "reconcile pending" for a workflow definition, cancel the command and try again; KPT is designed to handle these cases. This can happen occasionally depending on the Kubernetes cluster.
    ///

9. Verify that the EDA Config Engine is up and running.

    ```bash
    make eda-is-core-ready
    ```

10. Install all the standard EDA apps.

    This step can take approximate 5 to 15 minutes, depending on your connectivity.

    ```bash
    make eda-install-apps
    ```

11. Bootstrap EDA.

    Bootstrapping will create base resources into the EDA cluster, such as IP pools.

    ```bash
    make eda-bootstrap
    ```

12. Configure two-networks deployment.

    If your deployment uses two networks, create a second VIP pool for the OAM VIP address.

    ```bash
    make metallb-configure-pools METALLB_VIP=<OAM VIP> LB_POOL_NAME=pool-nb
    ```

    And create the OAM UI/API service using the new VIP pool.

    ```bash
    make eda-create-api-lb-svc API_LB_POOL_NAME=pool-nb
    ```

13. Optional: Deploy an example topology.

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

[^1]: Note, that it is not possible to change the default admin username.
