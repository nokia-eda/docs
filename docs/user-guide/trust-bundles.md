# Trust bundles

Trust bundles are collections of root certificates that a client or a server trusts. EDA uses root certificates to sign generated certificates before distributing them to applications or nodes. EDA applications use these root certificates to validate the authenticity of the certificates presented by a Transport Layer Security (TLS) peer during a TLS handshake.

Trust bundles are auto-generated during installation. EDA uses the following trust bundle (CertManager) issuers:

- internal issuer
- API issuer
- node issuer

Trust bundles are distributed to EDA components using the `CertManager Bundle` CR. The `Bundle` CR allows a user to create a trust bundle from multiple sources (ConfigMaps, Secrets) and make them available to an application through a different ConfigMap than the sources.

During installation, applications that need to use trust bundles can mount the resulting ConfigMap to have access to the assembled trust bundle.

**Parent topic:** [EDA certificate management](certificate-management.md)

## Internal issuer

The internal issuer is a CertManager certificate authority (CA) issuer that is responsible for signing the key pairs used by EDA pods for internal communication, including both client and server interactions.

### Internal Issuer

The internal issuer includes the CertManager `Certificate` and `Issuer` CRs.

```
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: eda-internal-ca
spec:
  isCA: true
  commonName: eda-internal-ca
  subject:
    organizations:
      - Nokia
    organizationalUnits:
      - NI
  secretName: eda-internal-ca
  secretTemplate:
    labels:
      eda.nokia.com/ca: "internal"
  usages:
    - digital signature
    - cert sign
    - key encipherment
    - server auth
    - client auth
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: eda-root-ca-issuer
    kind: Issuer
    group: cert-manager.io
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: eda-internal-issuer
spec:
  ca:
    secretName: eda-internal-ca
```

## API issuer

The API issuer is the CertManager issuer that signs the key pairs used by EDA API pods for exposing a TLS HTTP server.

This issuer is configured using the `CertManager Certificate` and `Issuer` CRs.

```
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: eda-api-ca
spec:
  isCA: true
  commonName: eda-api-ca
  subject:
    organizations:
      - Nokia
    organizationalUnits:
      - NI
  secretName: eda-api-ca
  secretTemplate:
    labels:
      eda.nokia.com/ca: "api"
  usages:
    - digital signature
    - cert sign
    - key encipherment
    - server auth
    - client auth
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: eda-root-ca-issuer
    kind: Issuer
    group: cert-manager.io
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: eda-api-issuer
spec:
  ca:
    secretName: eda-api-ca
```

### User-provided key pair

During installation, you can optionally provide a key pair (public and private keys) for the API server to use as certificate and key. In this case, you are responsible for the rotation of the provided key-pair.

To provide the API server public and private keys, create a Kubernetes `Secret` resource called `eda-api-user-certs` that contains the certificate and key under `tls.crt` and `tls.key`, respectively. For example:

```
apiVersion: v1
kind: Secret
metadata:
  name: eda-api-user-certs
  labels:
    eda.nokia.com/ca: api
type: kubernetes.io/tls
data:
  # base 64 encoded certificate
  tls.crt: |
    LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUNVakNDQWJzQ0FnMytNQTBHQ1NxR1NJYjNE
    UUVCQlFVQU1JR2JNUXN3Q1FZRFZRUUdFd0pLVURFT01Bd0cKQTFVRUNCTUZWRzlyZVc4eEVEQU9C
    Z05WQkFjVEIwTm9kVzh0YTNVeEVUQVBCZ05WQkFvVENFWnlZVzVyTkVSRQpNUmd3RmdZRFZRUUxF
    dzlYWldKRFpYSjBJRk4xY0hCdmNuUXhHREFXQmdOVkJBTVREMFp5WVc1ck5FUkVJRmRsCllpQkRR
    VEVqTUNFR0NTcUdTSWIzRFFFSkFSWVVjM1Z3Y0c5eWRFQm1jbUZ1YXpSa1pDNWpiMjB3SGhjTk1U
    TXcKTVRFeE1EUTFNVE01V2hjTk1UZ3dNVEV3TURRMU1UTTVXakJMTVFzd0NRWURWUVFHREFKS1VE
    RVBNQTBHQTFVRQpDQXdHWEZSdmEzbHZNUkV3RHdZRFZRUUtEQWhHY21GdWF6UkVSREVZTUJZR0Ex
    VUVBd3dQZDNkM0xtVjRZVzF3CmJHVXVZMjl0TUlHYU1BMEdDU3FHU0liM0RRRUJBUVVBQTRHSUFE
    Q0JoQUo5WThFaUhmeHhNL25PbjJTbkkxWHgKRHdPdEJEVDFKRjBReTliMVlKanV2YjdjaTEwZjVN
    Vm1UQllqMUZTVWZNOU1vejJDVVFZdW4yRFljV29IcFA4ZQpqSG1BUFVrNVd5cDJRN1ArMjh1bklI
    QkphVGZlQ09PekZSUFY2MEdTWWUzNmFScG04L3dVVm16eGFLOGtCOWVaCmhPN3F1TjdtSWQxL2pW
    cTNKODhDQXdFQUFUQU5CZ2txaGtpRzl3MEJBUVVGQUFPQmdRQU1meTQzeE15OHh3QTUKVjF2T2NS
    OEtyNWNaSXdtbFhCUU8xeFEzazlxSGtyNFlUY1JxTVQ5WjVKTm1rWHYxK2VSaGcwTi9WMW5NUTRZ
    RgpnWXcxbnlESnBnOTduZUV4VzQyeXVlMFlHSDYyV1hYUUhyOVNVREgrRlowVnQvRGZsdklVTWRj
    UUFEZjM4aU9zCjlQbG1kb3YrcE0vNCs5a1h5aDhSUEkzZXZ6OS9NQT09Ci0tLS0tRU5EIENFUlRJ
    RklDQVRFLS0tLS0K
  # base64 encoded private key
  tls.key: |
    RXhhbXBsZSBkYXRhIGZvciB0aGUgVExTIGNydCBmaWVsZA==
```

## Node issuer

The node issuer is a CertManager issuer that is responsible for signing the key pairs that EDA installs on the nodes to secure the configured gRPC servers. This issuer is configured using the CertManager `Certificate` and `Issuer` CRs, as shown in the following example:

```
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: eda-node-ca
spec:
  isCA: true
  commonName: eda-node-ca
  subject:
    organizations:
      - Nokia
    organizationalUnits:
      - NI
  secretName: eda-node-ca
  secretTemplate:
    labels:
      eda.nokia.com/ca: "node"
  usages:
    - digital signature
    - cert sign
    - key encipherment
    - server auth
    - client auth
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: eda-root-ca-issuer
    kind: Issuer
    group: cert-manager.io
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: eda-node-issuer
spec:
  ca:
    secretName: eda-node-ca
```

During installation, a provider can supply the root CA (public and private keys) that EDA uses as an issuer for the node key-pairs. The user does this by creating a secret and a CA issuer that references the secret.
