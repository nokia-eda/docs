# Exposing the EDA UI/API

In a regular cluster you typically have an [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) or [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/) controller that handles the external traffic and routes them to the services running inside the cluster. For instance, to let external users reach the EDA UI/API service.  
These controllers are not part of EDA installation, and are typically managed by the cluster administrator.

Still, in this chapter we will talk about how to configure Ingress or Gateway resources to expose the EDA UI/API service particularly.

EDA UI and API are exposed inside a cluster via the `eda-api` service of type "LoadBalancer" and its `apiserver` (port 80) and `apiserverhttps` (port 443) ports:

```bash
kubectl get service eda-api -o yaml | yq e '.spec.ports[0,1]' - #(1)!
```

1. Using [`yq`](https://github.com/mikefarah/yq/#install) to extract the service port configuration.

<div class="embed-result highlight">
```{.yaml .no-select .no-copy}
name: apiserver
nodePort: 32609
port: 80
protocol: TCP
targetPort: 9200
name: apiserverhttps
nodePort: 30302
port: 443
protocol: TCP
targetPort: 9443
```
</div>

Despite having port 80 in the service configuration, EDA UI/API is only served over HTTPS inside the cluster, therefore the external traffic should be routed to the `apiserverhttps` port. Generally speaking, there are two modes of exposing the EDA UI/API service using Ingress or Gateway API:

1. **Terminating TLS on Ingress/Gateway**
    External users have their TLS session terminated on the Ingress/Gateway and then the another HTTPS connection is established from the Ingress/Gatway to the `eda-api` deployment via the same-named service and its `apiserverhttps` port.
2. **Pass-through TLS**
    External users have their TLS session transparently passed through Ingress/Gateway and terminated on the `eda-api` deployment that has internal TLS certificate configured.

Terminating TLS on Ingress/Gateway has an undeniable benefit of allowing users to use their own TLS certificates on ingress. Whereas the pass-through mode uses the internal TLS certificate configured on the `eda-api` deployment and raise a warning in the browser since the certificate is not trusted.

In this section we will show how both modes can be configured using Ingress and Gateway API resources.

## Cert Manager

By default, Ingress controllers come with a self-generated TLS certificate to allow TLS termination in test and development environments. For production installations users strive to have an Ingress service with a trusted certificate configured using the domain name designated for EDA UI/API access.

Creation of a TLS certificate is easy when using [cert-manager](https://cert-manager.io/) - a Kubernetes-native way to automate the management and issuance of TLS certificates from various issuing sources. EDA itself uses cert-manager to issue the internal TLS certificates for various components, thus users can also leverage it and create the [Issuer](https://cert-manager.io/docs/configuration/) that will handle the certificate creation.

Creation of an Issuer is out of the scope of this guide, and is well explained in the cert-manager documentation.

## Ingress Nginx

[Ingress Nginx](https://kubernetes.github.io/ingress-nginx/) is a popular community-managed Ingress Controller based on NGINX.

### Terminating TLS on Ingress

To configure Ingress Nginx to terminate the TLS on the Ingress, you can create an Ingress resource with the following configuration.

<small>The code block annotations explain the important fields of the resource.</small>

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: HTTPS #(1)!
    cert-manager.io/issuer: letsencrypt-issuer #(2)!
    nginx.ingress.kubernetes.io/add-base-url: "false"
    nginx.ingress.kubernetes.io/affinity: cookie
    nginx.ingress.kubernetes.io/proxy-buffer-size: 128k
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
    nginx.ingress.kubernetes.io/session-cookie-name: route
  name: ingress
  namespace: default #(3)!
spec:
  ingressClassName: nginx
  rules: #(4)!
    - host: eda.rocks
      http:
        paths:
          - backend:
              service:
                name: eda-api
                port:
                  number: 443
            path: /
            pathType: Prefix
  tls: #(5)!
    - hosts:
        - eda.rocks
      secretName: eda-rocks-cert
```

1. EDA UI/API is only served over HTTPS inside the cluster, therefore the external traffic should be routed to TLS secured `apiserverhttps` port. For this reason we need to set HTTPS as a backend protocol.
2. For cert-manager to issue the certificate, we need to configure the `cert-manager.io/issuer` annotation with the name of the `Issuer` resource that has to be present in the same namespace as the Ingress resource.
3. If eda-api service is deployed in the `default` namespace, we need to create the Ingress resource in the same namespace.
4. The Ingress's `rules` section defines the access rules and the routing of the incoming requests. Here we say that the requests destined to the `eda.rocks` domain should be routed to the `eda-api` service and its 443 port.
5. The `tls` section defines the TLS configuration for the Ingress. Here we say that the Ingress should use the `eda-rocks-cert` secret to terminate the TLS and the SAN field in the cert should contain `eda.rocks` domain.

With an Ingress resource like this created, users would be able to access the EDA UI/API using the `eda.rocks` domain.

## Gateway API

If you're riding the [Gateway API](https://gateway-api.sigs.k8s.io/) wave, you can create a [`Gateway`](https://gateway-api.sigs.k8s.io/api-types/gateway/) resource to define your cluster gateway. As with the Ingress, the choice is yours if you want to terminate the TLS on the Gateway or not.

As a demonstration, we will create the Gateway resource with the TLS listener so that we will pass the TLS traffic to the EDA UI service, without terminating it on the Gateway.

Here is how you can create the `Gateway` resource:

/// tab | YAML Resource

```yaml
--8<-- "docs/user-guide/ingress/gateway.yml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<'EOF'
--8<-- "docs/user-guide/ingress/gateway.yml"
EOF
```

///

Now, let's create the `TLSRoute` resource that will bind our `Gateway` to the `eda-api` resource to provide the connectivity to the EDA UI:

/// tab | YAML Resource

```yaml
--8<-- "docs/user-guide/ingress/tlsroute.yml"
```

///
/// tab | `kubectl apply` command

```bash
kubectl apply -f - <<'EOF'
--8<-- "docs/user-guide/ingress/tlsroute.yml"
EOF
```

///

Now you should be able to access the EDA UI by navigating to the Gateway's URL.
