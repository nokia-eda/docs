# Platform logging

Like many applications in Kubernetes, Nokia EDA services write their logs to `stdout` and `stderr`. The allows other services in the Kubernetes cluster to retrieve and forward the logs.

For convenience, Nokia EDA includes a logging service based on [Fluent Bit](https://fluentbit.io/){:target="_blank"}. When enabled, a DaemonSet schedules a log forwarder pod on each Kubernetes node in the cluster and a Deployment schedules a central collector pod to aggregate logs.

If you prefer to use your own logging service, you can disable Nokia EDA's Fluent Bit by setting `.spec.logging.enabled` to `false` in the Nokia EDA `EngineConfig`.

## Syslog forwarding

If using the Nokia EDA logging service, syslog destinations can be configured using the `LogOutput` Resource.

TLS is supported for syslog connections. TLS trust bundles are loaded from the `eda-logoutput-trust-bundle` configmap in the Kubernetes namespace where EDA is deployed.

For mTLS authentication, set `.spec.tls.clientCert` to true in the `LogOutput`. This will configure the Fluent Bit pod with a key pair from the Cert-Manager integration issuer.

/// admonition | Note
    type: subtle-note
When a `LogOutput` resource is created or modified, EDA re-configures the outputs on the log forwarders. This may trigger the restart of the Fluent Bit pods.
///

To configuring syslog forwarding from the EDA UI:

**Procedure**
/// html | div.steps

1. From the **System Administration** navigation panel, click **Log Outputs** in the **Platform** category.
2. Click **Create**.
3. Enter a name
4. Click the **Syslog** toggle.
5. Specify a host, either a domain name or the IP address of the remote server.
6. Review the default values for the following fields and modify values as needed:

      - **Port**: port of the remote server
      - **Mode**: TCP or UDP
      - **Syslog Format**: RFC5424 or RFC3164
      - **Max Size**: the maximum message size, in bytes

7. Optionally enable TLS, and configure settings:
      - **Skip Verify**: disable server-certificate verification
      - **Client Certificate**: enabled mTLS authentication
  
///
