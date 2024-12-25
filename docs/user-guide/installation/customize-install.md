# Installation customization

If you followed the [Installation process](../../getting-started/installation-process.md) section, you already know that EDA uses [kpt][kpt-home] k8s package manager to install its components. Without getting too much into the details of kpt, you can expect that as any other package manager, kpt packages can be customized before the actual manifests will be applied to the cluster.  
This allows users to customize EDA installation according to their needs.

/// admonition | What about a Makefile?
    type: subtle-question
In the [Quickstart](../../getting-started/try-eda.md) section we have been using the Makefile to install the EDA Playground - a ready-to-use environment for trying EDA out. The Makefile allows user to [customize the Playground](#playground) installation, but is not suitable for production installation of EDA.

This section explains how to customize the EDA installation using [kpt][kpt-home] package manager.
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

In the [KPT Setters Reference](#kpt-setters-reference) section you will find all the setters parameters that can be customized per package that we have in the [`nokia-eda/kpt`][kpt-repo] repository.

## Playground

An EDA installation that is deployed with a set of pre-configured components and a small virtual network is called a _playground_. The [Getting Started guide](../../getting-started/try-eda.md) introduces EDA to the users by deploying the EDA Playground on a [KinD](https://kind.sigs.k8s.io/)-based kubernetes cluster.

Users can deploy the playground using a single `make` command that will come up with some sane defaults for all platform settings. While this is sufficient for the most common use cases, we also provide a way to customize the playground installation via:

* make variables in the preferences file or inline
* kpt setters file

### Preferences file

The preferences file is a file that contains high-level variables that are taken into account by the [Makefile][make-gh] used to orchestrate the playground deployment.

[make-gh]: https://github.com/nokia-eda/playground/blob/main/Makefile

The EDA Playground repository contains the [`prefs.mk`][prefs-file] preference file that lists these high-level variables along with a short description of their purpose.

```{.Makefile .code-scroll-lg title="prefs.mk file"}
--8<-- "https://raw.githubusercontent.com/nokia-eda/playground/refs/heads/main/prefs.mk"
```

Users can set the variables in this file to the intended values and then run the `make` command to deploy the playground with the desired settings. To use a custom location of the preferences file instead of the default `./prefs.mk` set the `PLAYGROUND_PREFS_FILE` environment variable to the desired path[^2].

[prefs-file]: https://github.com/nokia-eda/playground/blob/main/prefs.mk

### KPT Setters file

When the preferences file contains a set of high-level variables, the KPT setters file may contain values for every KPT setter used in [nokia-kpt][nokia-kpt-repo] KPT repository. The complete list of setters, their example values and types are provided in the KPT Setters Reference section as well as in the [kpt-setters.yaml][kpt-setters-yaml] file.

[kpt-setters-yaml]: https://github.com/nokia-eda/playground/blob/main/configs/kpt-setters.yaml
[nokia-kpt-repo]: https://github.com/nokia-eda/kpt

To use your own KPT setters file, create a copy of the [`kpt-setters.yaml`][kpt-setters-yaml] file with the required parameters set and set the `KPT_SETTERS_FILE` variable in the [preferences file](#preferences-file) to the path of your setters file.

## Keycloak admin password

The Keycloak administrator password can be updated during install with KPT setters, or post-install with the following procedure:

1. Navigate in web browser to `{EDA_URL}/core/httpproxy/v1/keycloak`
2. Login with the current Keycloak administrator username and password.
3. Select "Manage Account" on the top right dropdown for the user.
4. Select "Account Security > Signing In" from the left menu.
5. Click "Update" next to "My Password".
6. Configure a new password and save it.
7. Generate the Base 64 hash of the new password.
8. Using a system with access to the Kubernetes API of the EDA deployment, update the keycloak-admin-secret and restart Keycloak:

```shell
kubectl -n eda-system patch secret keycloak-admin-secret \
-p '{"data": { "password": "<NEW BASE64 HASH>" }}'

kubectl -n eda-system rollout restart deployment/eda-keycloak
```

## KPT Setters Reference

### Core package

<small>Package location: [eda-kpt-base][eda-kpt-base-gh-url]</small>

| Name                        | Example Value                                     | Type    | Description |
| --------------------------- | ------------------------------------------------- | ------- | ----------- |
| `API_IMG`                   | `ghcr.io/nokia-eda/core/api-server:24.12.1`       | `str`   |             |
| `API_REPLICAS`              | `1`                                               | `int`   |             |
| `APP_CATALOG`               | `https://github.com/nokia-eda/catalog.git`        | `str`   |             |
| `APP_REGISTRY`              | `ghcr.io`                                         | `str`   |             |
| `ASC_IMG`                   | `ghcr.io/nokia-eda/core/appstore-server:24.12.1`  | `str`   |             |
| `ASF_IMG`                   | `ghcr.io/nokia-eda/core/appstore-flow:24.12.1`    | `str`   |             |
| `ASVR_IMG`                  | `ghcr.io/nokia-eda/core/artifact-server:24.12.1`  | `str`   |             |
| `BSVR_IMG`                  | `ghcr.io/nokia-eda/core/bootstrap-server:24.12.1` | `str`   |             |
| `CE_IMG`                    | `ghcr.io/nokia-eda/core/config-engine:24.12.1`    | `str`   |             |
| `CLUSTER_MEMBER_NAME`       | `engine-config`                                   | `str`   |             |
| `CORE_IMG_CREDENTIALS`      | `core`                                            | `str`   |             |
| `CXDP_IMG`                  | `ghcr.io/nokia-eda/core/cxdp:24.12.1`             | `str`   |             |
| `CX_IMG`                    | `ghcr.io/nokia-eda/core/cx:24.12.1`               | `str`   |             |
| `EDA_CORE_NAMESPACE`        | `eda-system`                                      | `str`   |             |
| `EDA_TOOLBOX_IMG`           | `ghcr.io/nokia-eda/core/eda-toolbox:24.12.1`      | `str`   |             |
| `EDA_USER_NAMESPACE`        | `eda`                                             | `str`   |             |
| `EMS_IMG`                   | `ghcr.io/nokia-eda/core/metrics-server:24.12.1`   | `str`   |             |
| `EXT_HTTPS_PORT`            | `0`                                               | `int`   |             |
| `EXT_HTTP_PORT`             | `0`                                               | `int`   |             |
| `FE_IMG`                    | `ghcr.io/nokia-eda/core/flow-engine:24.12.1`      | `str`   |             |
| `GH_CATALOG_TOKEN`          | `some-value`                                      | `str`   |             |
| `GH_CATALOG_USER`           | `some-value`                                      | `str`   |             |
| `GIT_REPO_APPS`             | `/eda/apps.git`                                   | `str`   |             |
| `GIT_REPO_CHECKPOINT`       | `/eda/customresources.git`                        | `str`   |             |
| `GIT_REPO_IDENTITY`         | `/eda/identity.git`                               | `str`   |             |
| `GIT_REPO_SECURITY`         | `/eda/credentials.git`                            | `str`   |             |
| `GIT_REPO_USER_SETTINGS`    | `/eda/usersettings.git`                           | `str`   |             |
| `GIT_SERVERS`               | `[, ]`                                            | `array` |             |
| `KC_IMG`                    | `ghcr.io/nokia-eda/core/eda-keycloak:24.12.1`     | `str`   |             |
| `LLM_API_KEY`               | `your-open-ai-key`                                | `str`   |             |
| `LLM_MODEL`                 | `gpt-4o`                                          | `str`   |             |
| `NPP_IMG`                   | `ghcr.io/nokia-eda/core/npp:24.12.1`              | `str`   |             |
| `PG_IMG`                    | `ghcr.io/nokia-eda/core/eda-postgres:24.12.1`     | `str`   |             |
| `SA_IMG`                    | `ghcr.io/nokia-eda/core/state-aggregator:24.12.1` | `str`   |             |
| `SA_REPLICAS`               | `1`                                               | `int`   |             |
| `SC_IMG`                    | `ghcr.io/nokia-eda/core/state-controller:24.12.1` | `str`   |             |
| `SECRET_EDA_ADMIN_USERNAME` | `some-value`                                      | `str`   |             |
| `SECRET_KC_ADMIN_PASSWORD`  | `some-value`                                      | `str`   |             |
| `SECRET_KC_ADMIN_USERNAME`  | `some-value`                                      | `str`   |             |
| `SECRET_PG_DB_PASSWORD`     | `some-value`                                      | `str`   |             |
| `SECRET_PG_DB_USERNAME`     | `some-value`                                      | `str`   |             |
| `SE_IMG`                    | `ghcr.io/nokia-eda/core/state-engine:24.12.1`     | `str`   |             |
| `SE_REPLICAS`               | `1`                                               | `int`   |             |
| `SIMULATE`                  | `true`                                            | `bool`  |             |
| `SINGLESTACK_SVCS`          | `false`                                           | `bool`  |             |
| `TM_IMG`                    | `ghcr.io/nokia-eda/core/testman:24.12.1`          | `str`   |             |

### External packages

<small>Package location: [eda-external-packges][eda-external-packges-gh-url]</small>

| Name                           | Example Value                                                                                                                                                                                                                                                                                 | Type    | Description |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ----------- |
| `CMCA_IMG`                     | `quay.io/jetstack/cert-manager-cainjector:v1.14.4`                                                                                                                                                                                                                                            | `str`   |             |
| `CMCT_IMG`                     | `quay.io/jetstack/cert-manager-controller:v1.14.4`                                                                                                                                                                                                                                            | `str`   |             |
| `CMWH_IMG`                     | `quay.io/jetstack/cert-manager-webhook:v1.14.4`                                                                                                                                                                                                                                               | `str`   |             |
| `CM_ARGS`                      | `[--acme-http01-solver-image=ghcr.io/nokia-eda/ext/jetstack/cert-manager-acmesolver:v1.14.4, --cluster-resource-namespace=$(POD_NAMESPACE), --leader-election-namespace=kube-system, --max-concurrent-challenges=60, --v=2]`                                                                  | `array` |             |
| `CORE_IMG_CREDENTIALS`         | `core`                                                                                                                                                                                                                                                                                        | `str`   |             |
| `CSI_DRIVER_IMG`               | `quay.io/jetstack/cert-manager-csi-driver:v0.8.0`                                                                                                                                                                                                                                             | `str`   |             |
| `CSI_LIVPROBE_IMG`             | `registry.k8s.io/sig-storage/livenessprobe:v2.12.0`                                                                                                                                                                                                                                           | `str`   |             |
| `CSI_REGISTRAR_IMG`            | `k8s.gcr.io/sig-storage/csi-node-driver-registrar:v2.10.0`                                                                                                                                                                                                                                    | `str`   |             |
| `EDA_CORE_NAMESPACE`           | `eda-system`                                                                                                                                                                                                                                                                                  | `str`   |             |
| `EDA_GOGS_NAMESPACE`           | `eda-system`                                                                                                                                                                                                                                                                                  | `str`   |             |
| `EDA_TRUSTMGR_ISSUER_DNSNAMES` | `[trust-manager.eda-system.svc]`                                                                                                                                                                                                                                                              | `array` |             |
| `EDA_TRUSTMGR_NAMESPACE`       | `eda-system`                                                                                                                                                                                                                                                                                  | `str`   |             |
| `EXT_DOMAIN_NAME`              | `k1.rd.lab.eda.dev`                                                                                                                                                                                                                                                                           | `str`   |             |
| `FB_IMG`                       | `cr.fluentbit.io/fluent/fluent-bit:3.0.7`                                                                                                                                                                                                                                                     | `str`   |             |
| `FD_IMG`                       | `ghcr.io/nokia-eda/core/fluentd:v1.17.0-debian-1.0`                                                                                                                                                                                                                                           | `str`   |             |
| `GIT_SVC_TYPE`                 | `ClusterIP`                                                                                                                                                                                                                                                                                   | `str`   |             |
| `GOGS_ADMIN_PASS`              | `ZWRhCg==`                                                                                                                                                                                                                                                                                    | `str`   |             |
| `GOGS_ADMIN_USER`              | `ZWRhCg==`                                                                                                                                                                                                                                                                                    | `str`   |             |
| `GOGS_IMG_TAG`                 | `ghcr.io/gogs/gogs:0.13.0`                                                                                                                                                                                                                                                                    | `str`   |             |
| `GOGS_PV_CLAIM_SIZE`           | `24Gi`                                                                                                                                                                                                                                                                                        | `str`   |             |
| `GOGS_REPLICA_PV_CLAIM_SIZE`   | `24Gi`                                                                                                                                                                                                                                                                                        | `str`   |             |
| `TRUSTMGRBUNDLE_IMG`           | `quay.io/jetstack/cert-manager-package-debian:20210119.0`                                                                                                                                                                                                                                     | `str`   |             |
| `TRUSTMGR_ARGS`                | `[--default-package-location=/packages/cert-manager-package-debian.json, --log-level=1, --metrics-port=9402, --readiness-probe-path=/readyz, --readiness-probe-port=6060, --trust-namespace=$(TRUST_NAMESPACE), --webhook-certificate-dir=/tls, --webhook-host=0.0.0.0, --webhook-port=6443]` | `array` |             |
| `TRUSTMGR_IMG`                 | `quay.io/jetstack/trust-manager:v0.9.1`                                                                                                                                                                                                                                                       | `str`   |             |

### Playground packages

<small>Package location: [eda-playground][eda-playground-gh-url]</small>

| Name                   | Example Value                                                             | Type  | Description |
| ---------------------- | ------------------------------------------------------------------------- | ----- | ----------- |
| `CORE_IMG_CREDENTIALS` | `core`                                                                    | `str` |             |
| `EDA_CORE_NAMESPACE`   | `eda-system`                                                              | `str` |             |
| `EDA_USER_NAMESPACE`   | `eda`                                                                     | `str` |             |
| `SRL_24_10_1_GHCR`     | `ghcr.io/nokia/srlinux:24.10.1-492`                                       | `str` |             |
| `YANG_REMOTE_URL`      | `https://github.com/nokia/srlinux-yang-models/releases/download/v24.10.1` | `str` |             |

[kpt-home]: https://kpt.dev
[kpt-repo]: https://github.com/nokia-eda/kpt
[eda-kpt-base-gh-url]: https://github.com/nokia-eda/kpt/tree/main/eda-kpt-base
[eda-external-packges-gh-url]:https://github.com/nokia-eda/kpt/tree/main/eda-external-packages
[eda-playground-gh-url]: https://github.com/nokia-eda/kpt/tree/main/eda-kpt-playground

[^1]: Read more about kpt functions in the [kpt book](https://kpt.dev/book/04-using-functions/01-declarative-function-execution)
[^2]: The Playground git repo has the `./private` directory ignored, so the users can create a copy of the preference file in the `./private` directory.
