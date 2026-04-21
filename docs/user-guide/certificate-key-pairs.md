# Certificate key pairs

A certificate key pair consist of a `Certificate` and `Key` objects. Certificate key pairs are used by either servers or clients within an application.

A certificate key pair is generated and distributed for the following uses:

- for EDA components (client or server) to use for internal communication
- to install on a node or to rotate a certificate on a node
- for an EDA API server

**Parent topic:** [EDA certificate management](certificate-management.md)

## Certificate key pairs for EDA components <span id="certificate-key-pairs-eda-components"></span>

For EDA components, Cert-Manager (an x.509 certificate controller) generates, signs, and distributes the signed certificates and keys to the relevant pods.

EDA uses Cert-Manager to inject the generated certificate and key into a volume mounted to the pod where the application is running. Using this driver ensures that the private key and corresponding signed certificate is unique to each pod and is stored on disk to the node on which that pod is scheduled. This driver also handles renewal of live certificates as needed.

The life cycle of the certificate key pair matches that of the pod; the certificate is issued when the pod is created and destroyed when the pod is terminated.

The example below shows a `Pod` CR with two sets of certificate and key pairs that requests the signing of each of the certificates from Cert-Manager. The CSI driver generates a private key and requests a certificate from Cert-Manager based on the `volumeAttributes` settings.

``` 
apiVersion: v1
kind: Pod
metadata:
  name: eda-internal-sample-app
  labels:
    app: eda-internal-sample-app
spec:
  containers:
    - name: eda-internal-sample-app
      image:
      volumeMounts:
      - mountPath: "/var/run/eda/tls/external"
        name: tls-external
      - mountPath: "/var/run/eda/tls/internal"
        name: tls-internal
  volumes:
    - name: tls-external
      csi:
        driver: csi.cert-manager.io
        volumeAttributes:
          csi.cert-manager.io/issuer-name: eda-external-ca
          csi.cert-manager.io/dns-names: ${POD_NAME}.${POD_NAMESPACE}.svc.cluster.local
    - name: tls-internal
      csi:
        driver: csi.cert-manager.io
        volumeAttributes:
          csi.cert-manager.io/issuer-name: eda-internal-ca
          csi.cert-manager.io/dns-names: ${POD_NAME}.${POD_NAMESPACE}.svc.cluster.local
```

## Certificate key pairs for nodes <span id="certificate-key-pairs-nodes"></span>

EDA uses the gNSI Certz or gNOI certificate management protocols to generate, distribute, and rotate the certificate and key and cert-manager to sign the certificate for nodes.

The bootstrap server uses the following parameters for rotating certificates (these settings cannot be modified in the current release):

- `RotationThreshold`: the percentage of remaining certificate validity at which the bootstrap server rotates the certificate. This value is set to 50%.
- `CriticalFailedRotationThreshold`: if the certificate rotation fails, this is the percentage of remaining certificate validity at which the bootstrap server generates a critical alarm. This value is set to 70%.
- `BackoffTimer`: the backoff duration (set to 60 seconds) to wait between failed rotation attempts.

### Nodes that support gNSI Certz

During bootstrap, the initial configuration provided to the node must contain at least two gRPC servers to handle the gNMI and gNSI services:

- `bootstrap` server: the gNMI server configured with the network-instance `mgmt` and port `50052`; it uses the default TLS profile (`default-tls-profile: true`)
- `mgmt` server: the gNSI server configured with network-instance `mgmt`, port `57400`; it uses a TLS profile named `EDA`

### Initial certificate key pair generation

The bootstrap server adds the initial certificate key pair to the node using the gNSI protocol. The bootstrap server discovers the node by periodically sending gNMI capabilityRequest messages on port 50052 without verifying the self-signed certificate. When the node is discovered, the bootstrap server creates the certificate key pair and rotates the TLS profile called `EDA` on the node.

### Certificate key pair rotation

The bootstrap server rotates the node certificate and key pair when the certificate is about to expire, according to the configured validity time and the rotation threshold.

### Change in node issuer certificate triggers certificate rotation

When the node issuer certificate changes, the bootstrap server triggers the node certificate rotation regardless of the certificate validity time.

### EDA alarms on certificate rotation failure

EDA generates alarms on it detects failure in the rotation of certificates. It generates an initial (Major) alarm when the certificate rotation fails at the rotation threshold and a second (Critical) alarm when it reaches the `CriticalFailedRotationThreshold`.

These alarms should be cleared when the node certificate is successfully rotated. The alarm should specify the node name, the profile name that failed to be rotated.
