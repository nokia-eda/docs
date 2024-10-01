# Exposing the EDA UI

In a regular cluster you might have the [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) or [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/) controller installed to route the external traffic to the services running inside the cluster. The examples below provide copy-pastable snippets that would create resources to explose the EDA UI.

EDA UI exposed inside a cluster via the `eda-api` service of type LoadBalancer and its `apiserver` (port 80) and `apiserverhttps` (port 443) ports:

```bash title="service configuration"
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

## Nginx Ingress

If you're using Nginx Ingress controller, you can use the following example resources to configure NGINX Ingress to expose the EDA UI service:

* Terminating TLS on Ingress - [api-ingress-tls-terminate-https-internal.yaml](https://github.com/nokia-eda/kpt/blob/main/eda-external-packages/eda-api-ingress-https/api-ingress-tls-terminate-https-internal.yaml)
* Passing through TLS with termination on the eda-api side - [api-ingress-ssl-passthrough.yaml](https://github.com/nokia-eda/kpt/blob/main/eda-external-packages/eda-api-ingress-https-passthrough/api-ingress-ssl-passthrough.yaml)  
    Note, that NGINX controller has to be configured with the [passthrough option enabled](https://kubernetes.github.io/ingress-nginx/user-guide/tls/#ssl-passthrough).

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
