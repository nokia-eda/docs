| Name | Value |
|------|---------------|
| **eda-external-packages/cert-manager/cert-manager.yaml** ||
| `CORE_IMG_CREDENTIALS` | core |
| `CMCA_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-cainjector:v1.16.2" |
| `CMCT_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-controller:v1.16.2" |
| `CM_ARGS` | Non scalar value, see the file for details. |
| `CMWH_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-webhook:v1.16.2" |

| Name | Value |
|------|---------------|
| **eda-external-packages/csi-driver/cert-manager-csi-driver.in.yaml** ||
| `EDA_CORE_NAMESPACE` | eda-system |
| `CSI_REGISTRAR_IMG` | "ghcr.io/nokia-eda/ext/sig-storage/csi-node-driver-registrar:v2.12.0" |
| `CSI_LIVPROBE_IMG` | "ghcr.io/nokia-eda/ext/sig-storage/livenessprobe:v2.12.0" |
| `CSI_DRIVER_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-csi-driver:v0.10.1" |

| Name | Value |
|------|---------------|
| **eda-external-packages/eda-api-ingress-https-passthrough/api-ingress-ssl-passthrough.yaml** ||
| `EXT_DOMAIN_NAME` | "" |
| `INT_HTTPS_PORT` | 443 |

| Name | Value |
|------|---------------|
| **eda-external-packages/eda-api-ingress-https/eda-api-ingress-cert.yaml** ||
| `EXT_IPV4_ADDR` | "" |
| `EXT_IPV6_ADDR` | "" |

| Name | Value |
|------|---------------|
| **eda-external-packages/fluent-operator/fluent-bit-collector/eda-fbc-deployment.yaml** ||
| `FO_FC_IMG` | ghcr.io/nokia-eda/core/eda-fluentbit-collector:v4.0.1-debian-1.0 |

| Name | Value |
|------|---------------|
| **eda-external-packages/fluent-operator/fluent-operator/manifests/fluent-bit-operator-ds.yaml** ||
| `FO_FB_IMG` | ghcr.io/nokia-eda/ext/fluent/fluent-operator/fluent-bit:v4.0.1 |

| Name | Value |
|------|---------------|
| **eda-external-packages/fluent-operator/fluent-operator/manifests/fluent-bit-operator.yaml** ||
| `FO_IMG` | ghcr.io/nokia-eda/ext/fluent/fluent-operator/fluent-operator:3.4.0 |

| Name | Value |
|------|---------------|
| **eda-external-packages/fluentd/fluentd-bit-ds.yaml** ||
| `FB_IMG` | ghcr.io/nokia-eda/core/fluent-bit:3.0.7-amd64 |

| Name | Value |
|------|---------------|
| **eda-external-packages/fluentd/fluentd.yaml** ||
| `FD_IMG` | ghcr.io/nokia-eda/core/fluentd:v1.17.0-debian-1.0 |

| Name | Value |
|------|---------------|
| **eda-external-packages/git-no-pvc/gogs-admin-user.yaml** ||
| `EDA_GOGS_NAMESPACE` | eda-system |
| `GOGS_ADMIN_USER` | ZWRhCg== |
| `GOGS_ADMIN_PASS` | ZWRhCg== |

| Name | Value |
|------|---------------|
| **eda-external-packages/git-no-pvc/gogs-replica-service.yaml** ||
| `GIT_SVC_TYPE` | ClusterIP |

| Name | Value |
|------|---------------|
| **eda-external-packages/git-no-pvc/gogs-deployment-no-pvc.yaml** ||
| `GOGS_TOLERATION_NODE_UNREACHABLE` | 300 |
| `GOGS_TOLERATION_NODE_NOT_READY` | 300 |
| `GOGS_IMG_TAG` | ghcr.io/nokia-eda/core/gogs:0.13.0 |

| Name | Value |
|------|---------------|
| **eda-external-packages/git/gogs-pv-claim.yaml** ||
| `GOGS_PV_CLAIM_ACCESSMODE` | ReadWriteOnce |
| `GOGS_PV_CLAIM_SIZE` | 24Gi |

| Name | Value |
|------|---------------|
| **eda-external-packages/git/gogs-replica-pv-claim.yaml** ||
| `GOGS_REPLICA_PV_CLAIM_ACCESSMODE` | ReadWriteOnce |
| `GOGS_REPLICA_PV_CLAIM_SIZE` | 24Gi |

| Name | Value |
|------|---------------|
| **eda-external-packages/trust-manager/trust-manager.yaml** ||
| `EDA_TRUSTMGR_NAMESPACE` | eda-system |
| `TRUSTMGRBUNDLE_IMG` | "ghcr.io/nokia-eda/ext/jetstack/cert-manager-package-debian:20210119.0" |
| `TRUSTMGR_IMG` | "ghcr.io/nokia-eda/ext/jetstack/trust-manager:v0.15.0" |
| `TRUSTMGR_ARGS` | Non scalar value, see the file for details. |
| `EDA_TRUSTMGR_ISSUER_DNSNAMES` | Non scalar value, see the file for details. |
