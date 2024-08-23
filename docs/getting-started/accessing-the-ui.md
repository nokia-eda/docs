# Accessing the UI

EDA comes with a web-based user interface that allows you to interact with the framework. This guide will show you how to access the EDA UI.

Note, that EDA is an API-first framework, and the UI is just a client that interacts with its API. The usage of the UI is optional, and you can interact with EDA using the [CLI tools](../user-guide/using-the-clis.md) such as `edactl`, `e9s` and/or by directly leveraging K8s API.

## Forwarding when nested

EDA is exposed in your cluster via a Service of type `LoadBalancer`, but if you're running in a `kind` cluster you may not be able to reach it! A proxy using `kubectl` can be used to expose the EDA API server on the host running the cluster:

```shell
make start-ui-port-forward
```

This forwards port `9200` on your host to port `9200` of the EDA API service. You can then point your browser to `http://<host-machine>:9200`.

## Logging in

Point your browser to `https://<host-machine>:9200`. This should open the EDA UI. The default username is `admin`, and the password is `admin`.
