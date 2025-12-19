| Name | Value |
|------|---------------|
| **eda-kpt-base/appstore-gh/catalog-secret.yaml** ||
| `GH_CATALOG_TOKEN` | sometoken |
| `GH_CATALOG_USER` | someuser |
| `EDA_CORE_NAMESPACE` | eda-system |

| Name | Value |
|------|---------------|
| **eda-kpt-base/appstore-gh/catalog.yaml** ||
| `APP_CATALOG` | https://github.com/nokia-eda/catalog.git |

| Name | Value |
|------|---------------|
| **eda-kpt-base/appstore-gh/registry-secret.yaml** ||
| `GH_REGISTRY_TOKEN` | sometoken |
| `GH_REGISTRY_USER` | someuser |

| Name | Value |
|------|---------------|
| **eda-kpt-base/appstore-gh/registry.yaml** ||
| `APP_REGISTRY` | ghcr.io |
| `APP_REGISTRY_SKIPTLSVERIFY` | false |
| `APP_REGISTRY_MIRROR` | "" |

| Name | Value |
|------|---------------|
| **eda-kpt-base/core/apps/ce-deployment.yaml** ||
| `CORE_IMG_CREDENTIALS` | core |
| `CE_IMG` | ghcr.io/nokia-eda/core/config-engine:25.12.1 |
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
| `POD_NAMESPACE_IN_CSI` | "" |
| `EDA_INTERNAL_CERT_DURATION` | 720h |

| Name | Value |
|------|---------------|
| **eda-kpt-base/core/apps/cxdp-image-config-map.yaml** ||
| `CXDP_IMG` | ghcr.io/nokia-eda/core/cxdp:25.12.1 |

| Name | Value |
|------|---------------|
| **eda-kpt-base/eda-toolbox/eda-toolbox-deployment.yaml** ||
| `EDA_TOOLBOX_IMG` | ghcr.io/nokia-eda/core/eda-toolbox:25.12.1 |

| Name | Value |
|------|---------------|
| **eda-kpt-base/engine-config/engineconfig.yaml** ||
| `CLUSTER_MEMBER_NAME` | engine-config |
| `GIT_SERVERS` | Non scalar value, see the file for details. |
| `EXT_DOMAIN_NAME` | "" |
| `EXT_RELAX_DOMAIN_NAME_ENFORCEMENT` | false |
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
| `EAE_IMG` | ghcr.io/nokia-eda/core/ai-engine:25.12.1 |
| `EAE_LIMIT_CPU` | "" |
| `EAE_LIMIT_MEM` | "" |
| `EAE_REQ_CPU` | "" |
| `EAE_REQ_MEM` | "" |
| `ASVR_IMG` | ghcr.io/nokia-eda/core/artifact-server:25.12.1 |
| `ASVR_LIMIT_CPU` | "" |
| `ASVR_LIMIT_MEM` | "" |
| `ASVR_REQ_CPU` | "" |
| `ASVR_REQ_MEM` | "" |
| `BSVR_IMG` | ghcr.io/nokia-eda/core/bootstrap-server:25.12.1 |
| `BSVR_LIMIT_CPU` | "" |
| `BSVR_LIMIT_MEM` | "" |
| `BSVR_REQ_CPU` | "" |
| `BSVR_REQ_MEM` | "" |
| `ECC_IMG` | ghcr.io/nokia-eda/core/cert-checker:25.12.1 |
| `ECC_LIMIT_CPU` | "" |
| `ECC_LIMIT_MEM` | "" |
| `ECC_REQ_CPU` | "" |
| `ECC_REQ_MEM` | "" |
| `CX_IMG` | ghcr.io/nokia-eda/core/cx:25.12.1 |
| `CX_LIMIT_CPU` | "" |
| `CX_LIMIT_MEM` | "" |
| `CX_REQ_CPU` | "" |
| `CX_REQ_MEM` | "" |
| `CXCLUSTER_ISAGENT` | false |
| `CXCLUSTER_ADDR` | eda-cx-standalone |
| `CXCLUSTER_PORT` | 52200 |
| `EMS_IMG` | ghcr.io/nokia-eda/core/metrics-server:25.12.1 |
| `EMS_LIMIT_CPU` | "" |
| `EMS_LIMIT_MEM` | "" |
| `EMS_REQ_CPU` | "" |
| `EMS_REQ_MEM` | "" |
| `NPP_IMG` | ghcr.io/nokia-eda/core/npp:25.12.1 |
| `NPP_LIMIT_CPU` | "" |
| `NPP_LIMIT_MEM` | "" |
| `NPP_REQ_CPU` | "" |
| `NPP_REQ_MEM` | "" |
| `SE_IMG` | ghcr.io/nokia-eda/core/state-engine:25.12.1 |
| `SE_REPLICAS` | 1 |
| `SE_LIMIT_CPU` | "" |
| `SE_LIMIT_MEM` | "" |
| `SE_REQ_CPU` | "" |
| `SE_REQ_MEM` | "" |
| `SA_IMG` | ghcr.io/nokia-eda/core/state-aggregator:25.12.1 |
| `SA_REPLICAS` | 1 |
| `SA_LIMIT_CPU` | "" |
| `SA_LIMIT_MEM` | "" |
| `SA_REQ_CPU` | "" |
| `SA_REQ_MEM` | "" |
| `SC_IMG` | ghcr.io/nokia-eda/core/state-controller:25.12.1 |
| `SC_LIMIT_CPU` | "" |
| `SC_LIMIT_MEM` | "" |
| `SC_REQ_CPU` | "" |
| `SC_REQ_MEM` | "" |
| `FE_IMG` | ghcr.io/nokia-eda/core/flow-engine:25.12.1 |
| `FE_LIMIT_CPU` | "" |
| `FE_LIMIT_MEM` | "" |
| `FE_REQ_CPU` | "" |
| `FE_REQ_MEM` | "" |
| `API_IMG` | ghcr.io/nokia-eda/core/api-server:25.12.1 |
| `API_REPLICAS` | 1 |
| `API_SVC_ENABLE_LB_NODE_PORTS` | false |
| `API_LIMIT_CPU` | "" |
| `API_LIMIT_MEM` | "" |
| `API_REQ_CPU` | "" |
| `API_REQ_MEM` | "" |
| `ASC_IMG` | ghcr.io/nokia-eda/core/appstore-server:25.12.1 |
| `ASC_LIMIT_CPU` | "" |
| `ASC_LIMIT_MEM` | "" |
| `ASC_REQ_CPU` | "" |
| `ASC_REQ_MEM` | "" |
| `ASF_IMG` | ghcr.io/nokia-eda/core/appstore-flow:25.12.1 |
| `TM_IMG` | ghcr.io/nokia-eda/core/testman:25.12.1 |
| `TM_LIMIT_CPU` | "" |
| `TM_LIMIT_MEM` | "" |
| `TM_REQ_CPU` | "" |
| `TM_REQ_MEM` | "" |
| `KC_IMG` | ghcr.io/nokia-eda/core/eda-keycloak:25.12.1 |
| `KC_LIMIT_CPU` | "" |
| `KC_LIMIT_MEM` | "" |
| `KC_REQ_CPU` | "" |
| `KC_REQ_MEM` | "" |
| `PG_IMG` | ghcr.io/nokia-eda/core/eda-postgres:25.12.1 |
| `PG_LIMIT_CPU` | "" |
| `PG_LIMIT_MEM` | "" |
| `PG_REQ_CPU` | "" |
| `PG_REQ_MEM` | "" |
| `LLM_API_KEY` | "" |
| `LLM_MODEL` | gpt-4o |
| `SIMULATE` | true |
| `SINGLESTACK_SVCS` | false |

| Name | Value |
|------|---------------|
| **eda-kpt-base/namespaces/eda.yaml** ||
| `EDA_USER_NAMESPACE` | eda |

| Name | Value |
|------|---------------|
| **eda-kpt-base/proxies/bootstrap-server-udp.yaml** ||
| `INT_DHCPV6_PORT` | 547 |
| `INT_DHCPV4_PORT` | 67 |

| Name | Value |
|------|---------------|
| **eda-kpt-base/secrets/git-secret.yml** ||
| `CE_GIT_USERNAME` | ZWRh |
| `CE_GIT_PASSWORD` | ZWRh |

| Name | Value |
|------|---------------|
| **eda-kpt-base/secrets/identity-realm-auth.yaml** ||
| `SECRET_EDA_ADMIN_USERNAME` | YWRtaW4= |
| `SECRET_EDA_ADMIN_PASSWORD` | YWRtaW4= |

| Name | Value |
|------|---------------|
| **eda-kpt-base/secrets/keycloak-admin-secret.yml** ||
| `SECRET_KC_ADMIN_USERNAME` | YWRtaW4= |
| `SECRET_KC_ADMIN_PASSWORD` | YWRtaW4= |

| Name | Value |
|------|---------------|
| **eda-kpt-base/secrets/postgres-db-secret.yml** ||
| `SECRET_PG_DB_USERNAME` | someuser |
| `SECRET_PG_DB_PASSWORD` | somepassword |
