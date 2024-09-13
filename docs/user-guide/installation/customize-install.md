# Installation customization

If you haven't skipped the [Installation process](../../getting-started/installation-process.md) section, you already know that EDA uses [kpt][kpt-home] package manager to install EDA components. Without getting too much into the details of kpt, you can expect that as other package managers, kpt packages can be customized before the actual manifests will be applied to the cluster.  
This allows users to customize EDA installation according to their needs.

/// admonition | What about a Makefile?
    type: subtle-question
In the [Quickstart](../../getting-started/try-eda.md) section we have been using the Makefile to make the installation easier. Some customization has been incorporated into the Makefile, so that you could use it to customize the most important bits and pieces, but by no means this Makefile customization is a replacement for the proper customization of the catalog.

This section explains how to customize everything related to EDA installation using [kpt][kpt-home] package manager.
///

In kpt, the customization is done by setting the values of the parameters marked with the `kpt-set` annotation. Consider the [Catalog manifest](https://github.com/nokia-eda/kpt/blob/main/eda-kpt-base/appstore-gh/catalog.yaml) from the `eda-kpt-base` package:

```yaml
apiVersion: appstore.eda.nokia.com/v1
kind: Catalog
metadata:
  name: eda-catalog-builtin-apps
spec:
  title: EDA built in apps catalog
  remoteURL: https://github.com/nokia-eda/catalog.git #kpt-set: ${APP_CATALOG}
  authSecretRef: gh-catalog
```

The `#kpt-set: ${APP_CATALOG}` annotation is used to set indicate that this value can be set by `kpt` and overwrite the default value. If you were to install EDA with another catalog, you would do the following:

1. Clone the [`nokia-eda/kpt`][kpt-repo] repository
2. Change into the `eda-kpt-base` package directory. This directory is the root of the package and contains the `Kptfile`.
3. Run the `kpt` function[^1] with the setter image to modify the `APP_CATALOG` parameter:

    ```bash
    kpt fn eval --image ghcr.io/srl-labs/kpt-apply-setters:0.1.1 \
    --truncate-output=false -- \
    APP_CATALOG=https://github.com/acme/my-custom-catalog.git
    ```

4. Once the `APP_CATALOG` parameter is set, you can apply the EDA package:

    ```bash
    kpt live apply
    ```

Below you will find all the parameters that can be customized per package that we have in the [`nokia-eda/kpt`][kpt-repo] repository.

## Core package

<small>Package location: [eda-kpt-base][eda-kpt-base-gh-url]</small>

| Name                       | Example Value                                                     | Type    | Description |
| -------------------------- | ----------------------------------------------------------------- | ------- | ----------- |
| `API_IMG`                  | `ghcr.io/nokia-eda/core/api-server:24.8.1-rc`                     | `str`   |             |
| `API_REPLICAS`             | `1`                                                               | `int`   |             |
| `APP_REGISTRY`             | `ghcr.io`                                                         | `str`   |             |
| `ASC_IMG`                  | `ghcr.io/nokia-eda/core/appstore-server:24.8.1-rc`                | `str`   |             |
| `ASVR_IMG`                 | `ghcr.io/nokia-eda/core/artifact-server:24.8.1-rc`                | `str`   |             |
| `BSVR_IMG`                 | `ghcr.io/nokia-eda/core/bootstrap-server:24.8.1-rc`               | `str`   |             |
| `CE_IMG`                   | `ghcr.io/nokia-eda/core/config-engine:24.8.1-rc`                  | `str`   |             |
| `CLUSTER_MEMBER_NAME`      | `engine-config`                                                   | `str`   |             |
| `CORE_IMG_CREDENTIALS`     | `gitlab-core`                                                     | `str`   |             |
| `CXDP_IMG`                 | `ghcr.io/nokia-eda/core/cxdp:24.8.1-rc`                           | `str`   |             |
| `CX_IMG`                   | `ghcr.io/nokia-eda/core/cx:24.8.1-rc`                             | `str`   |             |
| `EDA_TOOLBOX_IMG`          | `ghcr.io/nokia-eda/core/eda-toolbox:24.8.1-rc`                    | `str`   |             |
| `EXT_DOMAIN_NAME`          | `devbox`                                                          | `str`   |             |
| `EXT_HTTPS_PORT`           | `443`                                                             | `int`   |             |
| `EXT_HTTP_PORT`            | `9200`                                                            | `int`   |             |
| `EXT_IPV4_ADDR`            | `10.1.0.11`                                                       | `str`   |             |
| `EXT_IPV6_ADDR`            | `fd7a:115c:a1e0::be01:ff2f`                                       | `str`   |             |
| `FE_IMG`                   | `ghcr.io/nokia-eda/core/flow-engine:24.8.1-rc`                    | `str`   |             |
| `GIT_REPO_APPS`            | `/eda/apps.git`                                                   | `str`   |             |
| `GIT_REPO_CHECKPOINT`      | `/eda/customresources.git`                                        | `str`   |             |
| `GIT_REPO_IDENTITY`        | `/eda/identity.git`                                               | `str`   |             |
| `GIT_REPO_SECURTIY`        | `/eda/credentials.git`                                            | `str`   |             |
| `GIT_REPO_USER_SETTINGS`   | `/eda/usersettings.git`                                           | `str`   |             |
| `GIT_SERVERS`              | `[, ]`                                                            | `array` |             |
| `KC_IMG`                   | `ghcr.io/nokia-eda/core/eda-keycloak:24.8.1-rc`                   | `str`   |             |
| `LLM_API_KEY`              | `some-key`                                                        | `str`   |             |
| `LLM_MODEL`                | `gpt-4o`                                                          | `str`   |             |
| `NO_PROXY`                 | `,10.244.0.0/16,10.96.0.0/16,.local,.svc,eda-git,eda-git-replica` | `str`   |             |
| `NPP_IMG`                  | `ghcr.io/nokia-eda/core/npp:24.8.1-rc`                            | `str`   |             |
| `PG_IMG`                   | `ghcr.io/nokia-eda/core/eda-postgres:24.8.1-rc`                   | `str`   |             |
| `SA_IMG`                   | `ghcr.io/nokia-eda/core/state-aggregator:24.8.1-rc`               | `str`   |             |
| `SA_REPLICAS`              | `1`                                                               | `int`   |             |
| `SC_IMG`                   | `ghcr.io/nokia-eda/core/state-controller:24.8.1-rc`               | `str`   |             |
| `SECRET_KC_ADMIN_PASSWORD` | `YWRtaW4=`                                                        | `str`   |             |
| `SECRET_KC_ADMIN_USERNAME` | `YWRtaW4=`                                                        | `str`   |             |
| `SECRET_PG_DB_PASSWORD`    | `cGFzc3dvcmQ=`                                                    | `str`   |             |
| `SECRET_PG_DB_USERNAME`    | `cG9zdGdyZXM=`                                                    | `str`   |             |
| `SE_IMG`                   | `ghcr.io/nokia-eda/core/state-engine:24.8.1-rc`                   | `str`   |             |
| `SE_REPLICAS`              | `1`                                                               | `int`   |             |
| `SIMULATE`                 | `true`                                                            | `bool`  |             |
| `SINGLESTACK_SVCS`         | `false`                                                           | `bool`  |             |
| `TM_IMG`                   | `ghcr.io/nokia-eda/core/testman:24.8.1-rc`                        | `str`   |             |
| `no_proxy`                 | `,10.244.0.0/16,10.96.0.0/16,.local,.svc,eda-git,eda-git-replica` | `str`   |             |

## External packages

<small>Package location: [eda-external-packges][eda-external-packges-gh-url]</small>

| Name | Example Value | Type | Description|
|------|-------|------|-|
| `CMCA_IMG` | `ghcr.io/nokia-eda/ext/jetstack/cert-manager-cainjector:v1.14.4` | `str` |  |
| `CMCT_IMG` | `ghcr.io/nokia-eda/ext/jetstack/cert-manager-controller:v1.14.4` | `str` |  |
| `CMWH_IMG` | `ghcr.io/nokia-eda/ext/jetstack/cert-manager-webhook:v1.14.4` | `str` |  |
| `CM_ARGS` | `[--acme-http01-solver-image=ghcr.io/nokia-eda/ext/jetstack/cert-manager-acmesolver:v1.14.4, --cluster-resource-namespace=$(POD_NAMESPACE), --leader-election-namespace=kube-system, --max-concurrent-challenges=60, --v=2]` | `array` |  |
| `CORE_IMG_CREDENTIALS` | `gitlab-core` | `str` |  |
| `CSI_DRIVER_IMG` | `ghcr.io/nokia-eda/ext/jetstack/cert-manager-csi-driver:v0.8.0` | `str` |  |
| `CSI_LIVPROBE_IMG` | `ghcr.io/nokia-eda/ext/sig-storage/livenessprobe:v2.12.0` | `str` |  |
| `CSI_REGISTRAR_IMG` | `ghcr.io/nokia-eda/ext/sig-storage/csi-node-driver-registrar:v2.10.0` | `str` |  |
| `FB_IMG` | `ghcr.io/nokia-eda/core/fluent-bit:3.0.7-amd64` | `str` |  |
| `FD_IMG` | `ghcr.io/nokia-eda/core/fluentd:v1.17.0-debian-1.0` | `str` |  |
| `GOGS_ADMIN_PASS` | `ZWRhCg==` | `str` |  |
| `GOGS_ADMIN_USER` | `ZWRhCg==` | `str` |  |
| `GOGS_IMG_TAG` | `ghcr.io/nokia-eda/core/gogs:0.13.0` | `str` |  |
| `GOGS_PV_CLAIM_SIZE` | `24Gi` | `str` |  |
| `GOGS_REPLICA_PV_CLAIM_SIZE` | `24Gi` | `str` |  |
| `TRUSTMGRBUNDLE_IMG` | `ghcr.io/nokia-eda/ext/jetstack/cert-manager-package-debian:20210119.0` | `str` |  |
| `TRUSTMGR_IMG` | `ghcr.io/nokia-eda/ext/jetstack/trust-manager:v0.9.1` | `str` |  |

## Playground

<small>Package location: [eda-playground][eda-playground-gh-url]</small>

| Name | Example Value | Type | Description|
|------|-------|------|-|
| `CORE_IMG_CREDENTIALS` | `gitlab-core` | `str` |  |
| `SRL_24_7_1_GHCR` | `ghcr.io/nokia/srlinux:24.7.1-330` | `str` |  |
| `YANG_REMOTE_URL` | `https://github.com/nokia/srlinux-yang-models/releases/download/v24.7.1` | `str` |  |

[kpt-home]: https://kpt.dev
[kpt-repo]: https://github.com/nokia-eda/kpt
[eda-kpt-base-gh-url]: https://github.com/nokia-eda/kpt/tree/main/eda-kpt-base
[eda-external-packges-gh-url]:https://github.com/nokia-eda/kpt/tree/main/eda-external-packages
[eda-playground-gh-url]: https://github.com/nokia-eda/kpt/tree/main/eda-kpt-playground

[^1]: Read more about kpt functions in the [kpt book](https://kpt.dev/book/04-using-functions/01-declarative-function-execution)
