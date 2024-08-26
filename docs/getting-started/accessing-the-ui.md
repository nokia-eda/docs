# Accessing the UI

EDA comes with a web-based user interface that allows you to interact with the framework. This guide will show you how to access the EDA UI.

Note, that EDA is an API-first framework, and the UI is just a client that interacts with its API. The usage of the UI is optional, and you can interact with EDA using the [CLI tools](../user-guide/using-the-clis.md) such as `edactl`, `e9s` and/or by directly leveraging K8s API.

## Forwarding when nested

EDA is exposed in your cluster via a Service of type `LoadBalancer`, but if you're running in a `kind` cluster you may not be able to reach it! A proxy using `kubectl` can be used to expose the EDA API server on the host running the cluster:

```shell
make start-ui-port-forward
```

This target will forward the https port of the `eda-api` service and display the URL to use in your browser.

## Logging in

Point your browser to `https://<eda-domain-name>` where `eda-domain-name` is the `EXT_DOMAIN_NAME` value set during the install step. This should open the EDA UI. The default username is `admin`, and the password is `admin`.
