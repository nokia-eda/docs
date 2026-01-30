# Certificate Management

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

EDA integrates with [Cert-Manager](https://cert-manager.io/) to provide Kubernetes-native certificate lifecycle management, including generation, signing, rotation, and distribution.
During installation, a local PKI is bootstrapped using Cert-Manager Issuer and Certificate resources, with configurable options to adapt certificate authorities and trust distribution to the various trust domains used by EDA.

> This document assumes users are familiar with fundamental [Cert-Manager](https://cert-manager.io/docs/) concepts, including [Issuers][cm-issuer-concept-doc], [Certificates](https://cert-manager.io/docs/concepts/certificate/), [CertificateRequests](https://cert-manager.io/docs/concepts/certificaterequest/), [Bundles](https://cert-manager.io/docs/projects/trust-manager/), and the [CSI Driver](https://cert-manager.io/docs/usage/csi/). If you are new to these topics, please refer to the Cert-Manager documentation at the provided links before proceeding.

[cm-issuer-concept-doc]: https://cert-manager.io/docs/concepts/issuer/
[cm-ca-issuer-doc]: https://cert-manager.io/docs/configuration/ca/

## Issuers

Cert-Manager handles certificate signing through a resource called [`Issuer`][cm-issuer-concept-doc].

EDA uses six different Cert-Manager Issuers:

- **Root issuer**: This is a [SelfSigned Issuer](https://cert-manager.io/docs/configuration/selfsigned/) used to bootstrap the remaining EDA `CA` Issuers.
- **API issuer**: A [CA Issuer][cm-ca-issuer-doc] that signs certificates for the EDA API server and Keycloak.
- **Node issuer**:  A [CA Issuer][cm-ca-issuer-doc] that signs certificates installed on network nodes after discovery (depending on `NodeSecurityProfile` settings).
- **Internal issuer**: A [CA Issuer][cm-ca-issuer-doc] that signs certificates for EDA's internal pods.
- **Webhook issuer**: A [CA Issuer][cm-ca-issuer-doc] that signs certificates for Mutating/Validating webhooks used by controller-based apps.
- **Bootstrap issuer**: A [CA Issuer][cm-ca-issuer-doc] that signs SR OS nodes bootstrap certificate.
These certificates are downloaded during ZTP and later replaced by certificates signed by the Node issuer using gNOI CertificateManagement.

To be able to sign certificates, each Issuer requires its own CA certificate and private key that are generated at EDA install time using a Cert-Manager `Certificate` Custom Resource. The `Certificate` for an Issuer is signed by the EDA root issuer (a `selfSigned` Cert-Manager issuer).

-{{ diagram(url='nokia-eda/docs/diagrams/eda-tls-issuers.drawio', title='', page=0, zoom=1.1) }}-

The signed Issuer CA certificate and the corresponding private key are stored in a Kubernetes Secret and is referenced by the Issuer resource.

```yaml title="Example: EDA API CA certificate and Issuer resources"

---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: eda-api-ca
  namespace: eda-system
spec:
  commonName: eda-api-ca
  duration: 2160h
  isCA: true
  issuerRef:
    group: cert-manager.io
    kind: Issuer
    name: eda-root-ca-issuer #(1)!
  privateKey:
    algorithm: ECDSA
    rotationPolicy: Always
    size: 256
  renewBefore: 1440h
  secretName: eda-api-ca #(2)!
  secretTemplate: #(3)!
    labels:
      eda.nokia.com/ca: api
  subject:
    organizationalUnits:
    - NI
    organizations:
    - Nokia
  usages:
  - digital signature
  - cert sign
  - key encipherment
  - server auth
  - client auth
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: eda-api-issuer
  namespace: eda-system
spec:
  ca:
    secretName: eda-api-ca #(4)!
```

1. The EDA API CA Certificate is signed by the EDA Root Issuer (`selfSigned`)
2. Kubernetes Secret name where the resulting certificate, private key and the certificate authority are stored
3. The secretTemplate allows labeling the Secret for easy trust distribution.
4. The Issuer references the generated secret.

## Trust Domains

EDA is composed of multiple trust domains:

- **Northbound**: Includes EDA API and Keycloak pods.
- **Internal**: Includes EDA pods involved in internal inter-pod communication as well as communication with the kubernetes API server.
- **Southbound**: Includes the managed nodes and the EDA pods interfacing with said nodes.

### Northbound

The API Issuer signs certificates that secure EDA's **API and Keycloak server pods**. It has a fixed name[^1], `eda-api-issuer`, is of type `CA`, and is backed by a secret called `eda-api-ca`.

-{{ diagram(url='nokia-eda/docs/diagrams/eda-tls-issuers.drawio', title='Northbound trust domain', page=1, zoom=1.0) }}-

> See the [Bring your own API Certificate](#bring-your-own-api-certificate) section for options for modifying this Issuer.

#### Certificate Generation and Distribution

EDA API certificates are generated and distributed to the API and Keycloak pods using [Cert-Manager CSI driver](https://cert-manager.io/docs/usage/csi-driver/) - a daemon set that facilitates the generation, signing and mounting of TLS certificate keypair to Kubernetes pods.

Using the CSI driver for certificate distribution offers several advantages:

- **Automatic renewal**: Certificates are automatically renewed before expiration without pod restarts.
- **Ephemeral storage**: Private keys exist only in the pod's memory and are never persisted to disk.
- **Dynamic configuration**: Certificate parameters are defined declaratively in the pod spec.
- **Simplified operations**: No need to manually create or manage Certificate resources.

The API server and Keycloak pods have Kubernetes volumes of type `csi` with `csi.cert-manager.io` attributes to request certificates from the `eda-api-issuer`:

```yaml title="snippet from the pod spec showing Cert-Manager CSI driver volume for API certificates"
spec:
  volumes:
  - name: eda-api-issuer
    csi:
      driver: csi.cert-manager.io
      readOnly: true
      volumeAttributes:
        csi.cert-manager.io/dns-names: ${EDA_API_HOSTNAME},eda-api,eda-api.${POD_NAMESPACE}.svc.cluster,eda-keycloak.${POD_NAMESPACE}.svc,eda-keycloak.${POD_NAMESPACE}.svc.cluster,eda-keycloak.${POD_NAMESPACE}.svc.cluster.local,eda-api.${POD_NAMESPACE},eda-api.${POD_NAMESPACE}.svc,eda-api.${POD_NAMESPACE}.svc.cluster.local,eda-keycloak,eda-keycloak.${POD_NAMESPACE}
        csi.cert-manager.io/duration: 720h0m0s
        csi.cert-manager.io/ip-sans: ${EDA_IPV4_ADDR},${EDA_IPV6_ADDR} #(1)!
        csi.cert-manager.io/issuer-name: eda-api-issuer
        csi.cert-manager.io/key-algorithm: ECDSA
        csi.cert-manager.io/renew-before: 240h0m0s
```

1. The variables seen here are for illustration purposes. Actual values are rendered during installation.

The CSI driver volume attributes configure certificate generation with the following parameters:

| Attribute | Description |
|-----------|-------------|
| `dns-names` | DNS Subject Alternative Names (SANs) to include in the certificate. These cover all service names and their fully qualified variants. |
| `duration` | Certificate validity period (30 days in this example). |
| `ip-sans` | IP addresses to include as SANs, allowing direct IP-based access. |
| `issuer-name` | The Cert-Manager Issuer used to sign the certificate. |
| `key-algorithm` | Cryptographic algorithm for key generation (ECDSA provides strong security with smaller keys). |
| `renew-before` | Time before expiration when Cert-Manager automatically renews the certificate (10 days in this example). |

> See [CSI driver docs](https://cert-manager.io/docs/usage/csi-driver/#supported-volume-attributes) for all supported volume attributes.

#### Bring your own API certificate

EDA API certificates can be customized to integrate with your organization's PKI infrastructure. There are two approaches: modify the API Issuer to chain EDA certificates to your CA, or providing pre-generated certificates directly.

##### Option 1: Modify the API Issuer

This approach integrates EDA into your organization's trust domain by modifying the default `eda-api-issuer` to chain to your enterprise CA. The CSI driver continues to handle certificate generation and automatic renewal, but certificates are now signed by your CA hierarchy.

-{{ diagram(url='nokia-eda/docs/diagrams/eda-tls-issuers.drawio', title='EDA API User CA Issuer', page=3, zoom=1.0) }}-

-{{ diagram(url='nokia-eda/docs/diagrams/eda-tls-issuers.drawio', title='EDA API Vault Issuer', page=4, zoom=1.0) }}-

> You can use any Cert-Manager Issuer type. Refer to the Cert-Manager documentation to choose and configure the Issuer that best fits your needs.

The procedure to modify the API Issuer to use your own (intermediate) CA includes the following steps:

/// html | div.steps

1. **Create a Secret with your CA credentials**

    Create a Kubernetes Secret containing your intermediate CA certificate and private key:

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: enterprise-api-ca
      namespace: eda-system
    type: kubernetes.io/tls
    data:
      tls.crt: <base64-encoded-intermediate-ca-certificate(s)> # The whole intermediate chain must be included in tls.crt.
      tls.key: <base64-encoded-intermediate-ca-private-key>
      ca.crt: <base64-encoded-root-ca-certificate>
    ```

Note that the rotation of the intermediate CA certificate(s) and key is the user's responsibility.

2. **Update a Cert-Manager Issuer**

    Update the `eda-api-issuer` `.spec.ca.secretName` to point to the newly created secret:

    ```yaml
    apiVersion: cert-manager.io/v1
    kind: Issuer
    metadata:
      name: eda-api-issuer
      namespace: eda-system
    spec:
      ca:
        secretName: enterprise-api-ca
    ```

    Alternatively, if your organization uses a different issuer type (such as Vault, Venafi, or an ACME server), configure the Issuer accordingly:

    ```yaml
    # Example: HashiCorp Vault issuer (or the community-driven fork OpenBao)
    apiVersion: cert-manager.io/v1
    kind: Issuer
    metadata:
      name: eda-api-issuer
      namespace: eda-system
    spec:
      vault:
        server: https://vault.example.com
        path: pki_int/sign/eda-api
        auth:
          kubernetes:
            role: eda-issuer
            mountPath: /v1/auth/kubernetes
    ```

3. **Restart the platform**

    If the Issuer has been modified after the initial EDA installation, restart the platform to ensure that the API and Keycloak pods request new certificates signed by your CA:

    ```bash
    edactl platform stop
    edactl platform start
    ```

///

**When to use this approach:**

- You want automatic certificate renewal managed by Cert-Manager
- Your organization has a centralized PKI and requires all certificates to chain to a corporate root CA
- You need to comply with security policies that mandate enterprise CA signing

##### Option 2: Provide your own certificates

This approach bypasses Cert-Manager entirely for the API certificates. You supply via a Kubernetes Secret the pre-generated certificates that EDA serves directly. EDA will mount them to the right pods.

-{{ diagram(url='nokia-eda/docs/diagrams/eda-tls-issuers.drawio', title='API User Certificates', page=2, zoom=1.5) }}-

The procedure to provide your own API certificates includes the following steps:

/// html | div.steps

1. **Create a secret with certificate material**

    Create a secret called `eda-api-user-certs` in the EDA base namespace (default: `eda-system`). It must be labeled with `eda.nokia.com/ca: api`

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      labels:
        eda.nokia.com/ca: api
      name: eda-api-user-certs
      namespace: eda-system
    type: kubernetes.io/tls
    data:
      tls.crt: <base64-encoded-certificate>
      tls.key: <base64-encoded-private-key>
      ca.crt: <base64-encoded-ca-certificate> # <-- required
    ```

2. **Restart the platform**

    If the migration from the self-signed certificates to user-provided ones happened after the initial EDA installation, restart the platform for the changes to take effect:

    ```bash
    edactl platform stop
    edactl platform start
    ```

///

/// warning | Custom certificates considerations

1. It is a user's responsibility to monitor certificate expiration and rotating certificates before they expire.

2. All required SANs (DNS names and IP addresses) must be present in the certificate:

    - **DNS Names:**  

        ```
        ${EDA_API_HOSTNAME}
        eda-api
        eda-api.${EDA_BASE_NAMESPACE}.svc.cluster
        eda-keycloak.${EDA_BASE_NAMESPACE}.svc
        eda-keycloak.${EDA_BASE_NAMESPACE}.svc.cluster
        eda-keycloak.${EDA_BASE_NAMESPACE}.svc.cluster.local
        eda-api.${EDA_BASE_NAMESPACE}
        eda-api.${EDA_BASE_NAMESPACE}.svc
        eda-api.${EDA_BASE_NAMESPACE}.svc.cluster.local
        eda-keycloak
        eda-keycloak.${EDA_BASE_NAMESPACE}
        ```

    - **IP Addresses:**  
    EDA IPv4 and/or IPv6 addresses, if IP access is allowed.
///

**When to use this approach:**

- Your organization has strict certificate issuance processes that cannot integrate with Cert-Manager
- You need certificates issued by an external CA that doesn't have a Cert-Manager integration
- You want complete control over the certificate lifecycle

#### Distributing trust

Clients that connect to the servers that use certificates signed by the EDA API Issuer must trust the EDA API CA certificate. The distribution of this CA certificate is handled using Cert-Manager's [**TrustManager Bundle**](https://cert-manager.io/docs/trust/trust-manager/#usage).

The EDA API CA certificate is needed by a handful of pods: Keycloak, Toolbox and CertChecker.  
EDA API CA is distributed using `eda-api-trust-bundle` Bundle resource:

```yaml
apiVersion: trust.cert-manager.io/v1alpha1
kind: Bundle
metadata:
  labels:
    eda.nokia.com/backup: "true"
  name: eda-api-trust-bundle
spec:
  sources:
  - secret: #(1)!
      key: ca.crt
      selector:
        matchLabels:
          eda.nokia.com/ca: api
  - configMap: #(2)!
      key: shadow-trust-bundle.pem
      selector:
        matchLabels:
          eda.nokia.com/shadow-ca: api
  target: # (3)!
    configMap:
      key: trust-bundle.pem
    namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: eda-system
```

1. This bundle distributes `ca.crt` certificates from any secret with label `eda.nokia.com/ca: api` in `eda-system` namespace.
2. This bundle distributes `shadow-trust-bundle.pem` certificates from any secret with label `eda.nokia.com/shadow-ca: api` in `eda-system` namespace.
3. The resulting set of certificates collected from `sources` is written to a configMap called `eda-api-trust-bundle` under key `trust-bundle.pem` in `eda-system` namespace.

The TrustManager Bundle collects the current API CA certificate (`ca.crt`) and previously used (up to two) CA certificates stored under the `shadow-trust-bundle.pem` key in ConfigMaps labeled with `eda.nokia.com/shadow-ca: api`. It then consolidates these certificates into a single trust bundle, which is written to a ConfigMap named `eda-api-trust-bundle` within EDA's base namespace. Any system or component that needs to trust the EDA API should import this trust bundle.

To retrieve the current trust bundle, use:

```shell
kubectl get -n eda-system cm eda-api-trust-bundle -o jsonpath='{.data.trust-bundle\.pem}'
```

<div class="embed-result">
```{.text .no-copy .no-select}
-----BEGIN CERTIFICATE-----
MIIBxDCCAWqgAwIBAgIRAKXQ1oWky+lKgqiFMxBQdNYwCgYIKoZIzj0EAwIwMjEO
MAwGA1UEChMFTm9raWExCzAJBgNVBAsTAk5JMRMwEQYDVQQDEwplZGEtYXBpLWNh
....
-----END CERTIFICATE-----
```
</div>

### Internal

Internal EDA communication encompasses all traffic between EDA pods, as well as with the Kubernetes API.

#### EDA Pods

This traffic uses mTLS (Mutual TLS), with both client and server certificates signed by the `eda-internal-issuer`. Internal certificates are generated and distributed using the Cert-Manager CSI driver, while trust bundles are distributed using `eda-internal-trust-bundle` [**TrustManager Bundle**](https://cert-manager.io/docs/trust/trust-manager/#usage) Custom Resource.

To ensure that internal pods can continue communicating during issuer rotation, the previous internal CAs are preserved in a ConfigMap populated by a TrustManager Bundle:

```yaml
apiVersion: trust.cert-manager.io/v1alpha1
kind: Bundle
metadata:
  labels:
    eda.nokia.com/backup: "true"
  name: eda-internal-trust-bundle
spec:
  sources:
  - secret:
      key: ca.crt
      selector:
        matchLabels:
          eda.nokia.com/ca: internal
  - configMap:
      key: shadow-trust-bundle.pem
      selector:
        matchLabels:
          eda.nokia.com/shadow-ca: internal
  target:
    configMap:
      key: trust-bundle.pem
    namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: eda-system
```

This Bundle aggregates the current internal CA certificate (`ca.crt`) along with any previous CAs stored under the key `shadow-trust-bundle.pem` in ConfigMaps labeled `eda.nokia.com/shadow-ca: internal`. The combined trust bundle is written to a ConfigMap called `eda-internal-trust-bundle` in EDA's base namespace, which all internal pods mount to access the internal CA trust bundle.

#### Kubernetes Webhooks

The webhook issuer is used by controller-based applications that need to create Validating or Mutating webhooks.

The issuer signs webhook certificates for the application pods using the Cert-Manager CSI driver:

```yaml
spec:
  volumes:
  - name: webhook-certs
    csi:
      driver: csi.cert-manager.io
      readOnly: true
      volumeAttributes:
        csi.cert-manager.io/dns-names: eda-nats-exporter-webhook-service.${POD_NAMESPACE}.svc
        csi.cert-manager.io/issuer-name: eda-webhook-issuer
```

Kubernetes webhooks require mTLS connections, meaning the Kubernetes API server must trust certificates signed by the webhook issuer. The webhook issuer's CA certificate is injected into webhook configurations using the Cert-Manager annotation `cert-manager.io/inject-ca-from`, which automatically populates the `caBundle` field:

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  name: eda-nats-exporter-mutating-webhook-configuration
  annotations:
    cert-manager.io/inject-ca-from: "eda-system/eda-webhook-ca" #(1)!
webhooks:
   ...
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: eda-nats-exporter-validating-webhook-configuration
  annotations:
    cert-manager.io/inject-ca-from: "eda-system/eda-webhook-ca" #(2)!
webhooks:
  ...
```

1. This annotation injects the CA ca.crt value in the `clientConfig` section of the Webhook. CA [Injector docs](https://cert-manager.io/docs/concepts/ca-injector/)
2. This annotation injects the CA ca.crt value in the `clientConfig` section of the Webhook. CA [Injector docs](https://cert-manager.io/docs/concepts/ca-injector/)

### Southbound

The EDA southbound interface connects EDA to managed network nodes. EDA can manage the installation and rotation of node certificates used during the onboarding process (if required) and by the gRPC servers that EDA communicates with.

-{{ diagram(url='nokia-eda/docs/diagrams/eda-tls-issuers.drawio', title='EDA Node Certificate lifecycle', page=5, zoom=1.0) }}-

#### NodeSecurityProfile

The `NodeSecurityProfile` Custom Resource defines how TLS certificates are managed for network nodes in EDA. It specifies critical parameters such as which certificate issuer to use, how to select the nodes the profile applies to, and the details of the certificate signing requests (CSR), including validity, key algorithm, and organization information.  
By creating and configuring different `NodeSecurityProfile` resources, you can control whether EDA automatically manages node certificates or if certificates are handled outside EDA. The profile directly impacts node onboarding security and operational model.

EDA supports multiple TLS management modes, each selected and configured through the `NodeSecurityProfile` Custom Resource:

| Mode | Description |
|------|-------------|
| **Managed TLS** | Node certificates are generated and rotated by EDA. |
| **Unmanaged TLS** | Node certificates are installed out-of-band. Users must provide a trust bundle for EDA services communicating with nodes to verify the certificates. |
| **Unmanaged TLS (without verify)** | Node certificates are installed out-of-band. EDA skips server certificate verification. |
| **Insecure** | Communication with nodes uses plaintext. Not recommended beyond preliminary tests, labs, or troubleshooting. |

The recommended mode is **Managed TLS**.

```yaml
apiVersion: core.eda.nokia.com/v1
kind: NodeSecurityProfile
metadata:
  labels:
    eda.nokia.com/bootstrap: "true"
  name: managed-tls
  namespace: eda-system
spec:
  nodeSelector:
  - eda.nokia.com/security-profile=managed
  tls:
    issuerRef: eda-node-issuer
    csrParams:
      certificateValidity: 2160h
      city: Sunnyvale
      country: US
      csrSuite: CSRSUITE_X509_KEY_TYPE_RSA_2048_SIGNATURE_ALGORITHM_SHA_2_256
      org: NI
      orgUnit: EDA
      state: California
```

This profile applies to nodes with the label `eda.nokia.com/security-profile: managed`. Depending on the platform, EDA uses either gNSI Certz (SR Linux) or gNOI CertificateManagement (SR OS) gRPC services to manage node certificates.

EDA creates a TLS profile called `EDA` on each node, either during ZTP or upon discovery. EDA leverages the node's ability to generate CSRs locally, ensuring that private keys never leave the device.

#### Bootstrapping

The process of setting up initial configuration on the network nodes to enable secure and trusted communication with EDA is called bootstrapping. This process is performed by the EDA Bootstrap Server (`eda-bsvr`) component and involves installing TLS profiles and configuring gRPC servers on the nodes to perform initial discovery and subsequent management.

##### SR Linux

SR Linux supports [gNSI Certz](https://github.com/openconfig/gnsi/tree/main/certz) for certificate management. During ZTP, the node downloads an initial configuration containing two gRPC servers:

**discovery**: Uses the SR Linux default TLS profile (managed by gNSI Certz).

```bash
--{ + running }--[ system grpc-server discovery ]--
A:user@leaf-1# info
    admin-state enable
    rate-limit 65535
    session-limit 1024
    metadata-authentication true
    default-tls-profile true # (4)!
    network-instance mgmt # (1)!
    port 50052 # (3)!
    services [ # (2)!
        gnmi
        gnoi
        gnsi
    ]
    gnmi {
        commit-save false
    }
```

1. The server is bound to the mgmt network instance.
2. gNMI and gNSI gRPC services must be enabled.
3. The discovery gRPC server port number is hardcoded.
4. Use the device default TLS Profile.

**mgmt**: References a TLS profile called `EDA`, this profile is dynamic (created and managed by gNSI Certz)

```bash
--{ + running }--[ system grpc-server mgmt ]--
A:user@leaf-1# info
    admin-state enable
    rate-limit 65535
    session-limit 1024
    metadata-authentication true
    tls-profile EDA # (4)!
    network-instance mgmt # (1)!
    port 57400 # (3)!
    services [ # (2)!
        gnmi
        gnoi
        gnsi
    ]
    gnmi {
        commit-save false
    }
```

1. The server is bound to the mgmt network instance.
2. gNMI and gNSI gRPC services must be enabled.
3. The mgmt gRPC server port is configurable in the NodeProfile resource.
4. Use the rotated `EDA` TLS Profile.

When the node boots after ZTP, EDA's bootstrap server discovers it through continuous gNMI capabilities requests on port 50052 toward TopoNodes that haven't been discovered yet. Upon receiving a response, the bootstrap server:

1. Sends a gNSI Certz `AddProfile` RPC to create the `EDA` TLS profile.
2. Initiates a gNSI Certz `Rotate` RPC to generate, sign, and install the node's certificate.

During the Rotate streaming RPC:

1. The bootstrap server requests the node to generate a Certificate Signing Request (CSR) based on parameters from the node's `NodeSecurityProfile`.
2. The node generates a private key and CSR locally, then sends only the CSR back to the bootstrap server.
3. The bootstrap server creates a Cert-Manager `CertificateRequest` CR with the CSR and specifies the issuer from the `NodeSecurityProfile` as the signing issuer.
4. Cert-Manager signs the CSR and stores the resulting certificate in the CertificateRequest `.status.certificate`.
5. The bootstrap server uploads the signed certificate to the node using a gNSI Certz `CertificatesUpload` RPC within the same Rotate stream.

The bootstrap server continuously monitors certificate status using TLS handshakes and gNMI capabilities on both the bootstrap gRPC server port (to detect re-ZTP events) and the main EDA management gRPC server (default port 57400).

##### SR OS

SR OS supports the [gNOI CertificateManagement service](https://github.com/openconfig/gnoi/blob/main/cert/cert.proto). During ZTP, the node downloads an initial configuration with a single gRPC server (SROS supports only one gRPC server) that references a TLS server profile called `bootstrap`.
This profile uses a certificate and private key pair (called bootstrap) that was downloaded during ZTP.

The bootstrap keypair is generated per TopoNode, signed by the `eda-bootstrap-issuer`, and uploaded to EDA's artifact server. When the node boots, its gRPC server comes up with the bootstrap keypair.

The bootstrap server detects newly booted nodes through continuous gNMI capabilities requests to the node's IP address on port 57400. It performs a TLS handshake to retrieve the certificate and verifies that it was signed by the `eda-bootstrap-issuer`: This indicates a newly ZTP'd SR OS node.

The bootstrap server then:

1. Installs a certificate profile called `EDA` using gNOI CertificateManagement.
2. Switches the gRPC server's TLS profile reference to use the new `EDA` profile via gNMI Set RPC with [commit confirmed extension](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-commit-confirmed.md).

#### Certificate Rotation

Bootstrap server maintains a continuous loop that monitors and rotates the nodes certificates. The certificates are rotated when their lifetime reaches the `RotationThreshold` (50% of total certificate validity).

If a node certificate rotation fails, the bootstrap server generates a `NodeCertificateRotationThresholdReached` alarm:

- **Major** severity: When rotation fails at the `RotationThreshold`.
- **Critical** severity: When the certificate lifetime reaches the `CriticalFailedRotationThreshold` (70% of total validity).

The alarm is cleared once the certificate is successfully rotated.

If any of this alarm is generated, it is advised to check the status of EDA's Cert-Manager, related CertificateRequest custom resources, bootstrap server logs and ensure the node is reachable so that its certificate keypair can be rotated.

#### Bring your own Node Issuer

You can replace the default `eda-node-issuer` with a custom Cert-Manager Issuer that integrates with your organization's PKI. This allows node certificates to be signed by your enterprise CA while EDA continues to handle automatic certificate generation and rotation.

Unlike the API Issuer (which is a single issuer for all API certificates), node issuers are referenced per `NodeSecurityProfile`. This enables different groups of nodes to use different issuers based on their security requirements or organizational boundaries.

-{{ diagram(url='nokia-eda/docs/diagrams/eda-tls-issuers.drawio', title='EDA Node Certificate lifecycle', page=6, zoom=1.0) }}-

##### Step 1: Create a Cert-Manager Issuer

Create a Cert-Manager Issuer backed by your enterprise CA. You can use any issuer type supported by Cert-Manager (CA, Vault, Venafi, etc.).

```yaml title="Example: CA Issuer with enterprise intermediate CA"
apiVersion: v1
kind: Secret
metadata:
  name: enterprise-node-ca
  namespace: eda-system
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-intermediate-ca-certificate>
  tls.key: <base64-encoded-intermediate-ca-private-key>
  ca.crt: <base64-encoded-ca-certificate>
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: enterprise-node-issuer
  namespace: eda-system
spec:
  ca:
    secretName: enterprise-node-ca
```

```yaml title="Example: HashiCorp Vault Issuer"
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: vault-node-issuer
  namespace: eda-system
spec:
  vault:
    server: https://vault.example.com
    path: pki_int/sign/network-nodes
    auth:
      kubernetes:
        role: eda-node-issuer
        mountPath: /v1/auth/kubernetes
```

##### Step 2: Create a NodeSecurityProfile referencing your Issuer

Create a `NodeSecurityProfile` that references your custom issuer in the `issuerRef` field:

```yaml
apiVersion: core.eda.nokia.com/v1
kind: NodeSecurityProfile
metadata:
  name: enterprise-managed-tls
  namespace: eda-system
spec:
  nodeSelector:
  - eda.nokia.com/security-profile=enterprise
  tls:
    csrParams:
      certificateValidity: 2160h
      city: Frankfurt
      country: DE
      csrSuite: CSRSUITE_X509_KEY_TYPE_RSA_2048_SIGNATURE_ALGORITHM_SHA_2_256
      org: ACME Corp
      orgUnit: Network Operations
      state: Hesse
    issuerRef: enterprise-node-issuer  # Reference your custom issuer
```

##### Step 3: Label nodes to use the profile

Apply the appropriate label to nodes that should use this security profile:

```bash
kubectl label toponodes.core.eda.nokia.com <node-name> \
              eda.nokia.com/security-profile=enterprise
```

Make sure to remove any conflicting labels that might influence the NodeSecurityProfile.

##### Using multiple Issuers for different node groups

You can create multiple `NodeSecurityProfile` resources with different issuers to segment your network by trust domain. For example:

| Profile | Node Selector | Issuer |
|---------|---------------|--------|
| `us-west-tls` | `eda.nokia.com/security-profile=us-west` | `us-west-issuer` |
| `eu-west-tls` | `eda.nokia.com/security-profile=eu-west` | `eu-west-issuer` |
| `ap-east-tls` | `eda.nokia.com/security-profile=ap-east` | `ap-east-issuer` |

Each node can only be associated with one `NodeSecurityProfile` at a time. If multiple profiles match a node's labels, the first profile (sorted by name) is used.

#### Distributing trust

For EDA services to establish secure connections with managed nodes, the appropriate trust bundles must be distributed to the pods that communicate directly with the nodes.
Only a subset of EDA pods interface directly with network nodes: **NPP**, **FE**, **ToolBox**.

##### Automatic trust distribution (Managed TLS)

When using Managed TLS with the default `eda-node-issuer` or a custom issuer created in the `eda-system` namespace, EDA automatically distributes the CA trust bundle to the relevant pods using TrustManager Bundles.

The node CA certificate is aggregated into a trust bundle and mounted into pods that need to verify node certificates:

```yaml
apiVersion: trust.cert-manager.io/v1alpha1
kind: Bundle
metadata:
  labels:
    eda.nokia.com/backup: "true"
  name: eda-node-trust-bundle
  namespace: eda-system
spec:
  sources:
  - secret:
      key: ca.crt
      selector:
        matchLabels:
          eda.nokia.com/ca: node
  - configMap:
      key: ca.crt
      selector:
        matchLabels:
          eda.nokia.com/ca: node
  - configMap:
      key: shadow-trust-bundle.pem
      selector:
        matchLabels:
          eda.nokia.com/shadow-ca: node
  target:
    configMap:
      key: trust-bundle.pem
    namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: eda-system
```

##### Custom issuer trust distribution

When using a custom issuer, ensure your CA certificate is included in the node trust bundle. Label your CA secret appropriately:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: enterprise-node-ca
  namespace: eda-system
  labels:
    eda.nokia.com/ca: node  # Required for automatic trust distribution
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-ca-certificate>
  tls.key: <base64-encoded-ca-private-key>
  ca.crt: <base64-encoded-root-ca-chain>  # Include full chain if needed
```

The `eda.nokia.com/ca: node` label ensures the TrustManager Bundle automatically includes your CA in the trust bundle distributed to EDA pods.

##### Unmanaged TLS trust distribution

When using Unmanaged TLS mode (certificates installed out-of-band), you must manually provide the trust bundle for node certificate verification. Create a ConfigMap or Secret containing your CA certificates and reference it in the `NodeSecurityProfile` under `spec.tls.trustBundle`:

```yaml
apiVersion: core.eda.nokia.com/v1
kind: NodeSecurityProfile
metadata:
  labels:
    eda.nokia.com/bootstrap: "true"
  name: unmanaged-tls
  namespace: eda-system
spec:
  nodeSelector:
  - eda.nokia.com/security-profile=unmanaged
  tls:
    trustBundle: eda-node-unmanaged # must include a trust bundle under the key `ca.crt`
```

The referenced configMap must be labeled with `eda.nokia.com/ca: node` so that the trustbundle is distributed to EDA pods.

[^1]: By default, EDA system components are installed in the `eda-system` namespace.
