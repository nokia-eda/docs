---
resource_name: TPIStorage
resource_name_plural: tpistorages
resource_name_plural_title: TPI Storages
resource_name_acronym: TS
crd_path: docs/apps/tpi.eda.nokia.com/crds/tpi.eda.nokia.com_tpistorages.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# TPI Storage

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Defines how to reach a storage server. A `TPIStorage` configures access to the file server that [`TPIExport`](./tpiexport.md) uploads the produced workbook to, and that [`TPIImport`](./tpiimport.md) (or [`TPIImportDryRun`](./tpiimportdryrun.md)) downloads the workbook from. Create your own `TPIStorage` for a file server you operate (with TLS and appropriate access controls in production).

## Storage server

TPI currently supports only `HTTP(S)`. TPI uses **GET** to download files, **PUT** to upload files, and **HEAD** on the storage root path for the `TPIStorage` reachability probe. Other methods (`POST`, `PATCH`), WebDAV-only flows, multipart uploads, and similar patterns are **not** used by TPI.

| Item | Import | Export | Probe |
|------|--------|--------|-------|
| Method | **GET** | **PUT** | **HEAD** |
| Body | Raw bytes of the workbook (response) | Raw workbook bytes (request) | - |
| Success | Response status code **must be `200`** | Any **2xx** status is accepted | Any HTTP response counts as reachable, except `401`/`403`, since those indicate authentication failures |
| Failure | Any non-`200` status is treated as an error | Any status **outside 2xx** is treated as an error | Network or transport errors, or HTTP codes `401`/`403` |

### Root path

The full path of a workbook is the `spec.rootPath` joined with the `spec.path` from the [`TPI`](./tpi.md) or [`TPIExport`](./tpiexport.md) workflow. The root path can contain forward slashes as allowed by the CRD. The full path must resolve to a single file object on the storage server. The directory on the storage server that backs `spec.rootPath` must **exist** and be **writable** by the process that serves **PUT** (for example, `nginx` under its configured user/group). Otherwise exports can fail with `500`.

## Authentication

`TPIStorage` supports two authentication mechanisms that can be used independently or combined: HTTP Basic authentication (application layer) and mutual TLS (transport layer).

### HTTP Basic

For HTTP Basic authentication, use a Kubernetes [Basic authentication Secret](https://kubernetes.io/docs/concepts/configuration/secret/#basic-authentication-secret) in the **same namespace** as the `TPIStorage`, and set `spec.http.basicAuthSecret` to that Secret’s name. **The EDA UI does not create this Secret** — create it in the cluster yourself (for example with `kubectl`, `oc`, GitOps, or a manifest).

**Example** for creating the Secret with `kubectl`:

```bash
kubectl create secret generic tpi-storage-basic-auth \
    -n <NAMESPACE> \
    --type=kubernetes.io/basic-auth \
    --from-literal=username=myusername \
    --from-literal=password=mypassword
```

If `basicAuthSecret` is unset, the client sends **no** `Authorization` header. If the server still requires Basic authentication, requests fail with `401`.

### Mutual TLS (mTLS)

For **mTLS** (TLS client authentication over HTTPS), reference a Kubernetes `Secret` in the **same namespace** as the `TPIStorage` from `spec.http.https.clientTlsSecret`. Enable `spec.http.https` on the `TPIStorage`. **The EDA UI does not create this Secret** — create it yourself (for example `kubectl`, `oc`, GitOps, or a manifest).

TPI requires the same `data` layout as a [TLS Secret](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets): `tls.crt`, `tls.key`, and optional `ca.crt`. That matches `kubectl create secret tls` and typical [cert-manager](https://cert-manager.io/docs/usage/certificate/) `Certificate`-backed Secrets. When `ca.crt` is set, PEM-encoded CA certificate(s) are merged into the pool used to verify the server certificate (in addition to the system trust store), unless `spec.http.https.skipVerify` is true.

**Example** for creating the Secret with `kubectl`:

```bash
kubectl create secret generic tpi-storage-mtls \
    -n <NAMESPACE> \
    --type=kubernetes.io/tls \
    --from-file=tls.crt=client.pem \
    --from-file=tls.key=client-key.pem \
    --from-file=ca.crt=ca-chain.pem
```

Omit `--from-file=ca.crt=...` if you rely only on the system trust store (and `skipVerify` is false). When you do **not** need `ca.crt`, the Secret can be created with `kubectl`:

```bash
kubectl create secret tls tpi-storage-mtls \
    -n <NAMESPACE> \
    --cert=client.pem \
    --key=client-key.pem
```

If `spec.http.https.clientTlsSecret` is unset, the client does **not** present a client certificate. If `https` is unset, connections use plain HTTP and mTLS does not apply.

## Dependencies

The `TPIStorage` resource has no dependencies on other EDA resources.

## Referenced resources

A `TPIStorage` optionally references Kubernetes `Secret` resources in the same namespace:

- `spec.http.basicAuthSecret` -- for HTTP Basic authentication (see [HTTP Basic](#http-basic))
- `spec.http.https.clientTlsSecret` -- for TLS client authentication (see [Mutual TLS (mTLS)](#mutual-tls-mtls))

## Examples

/// tab | YAML

```yaml
-{{ include_snippet(resource_name) }}-
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
-{{ include_snippet(resource_name) }}-
EOF
```

///

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
