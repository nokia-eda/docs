# EDA on an on-prem k8s cluster

The [quickstart guide](../../getting-started/installation-process.md) did a great job of getting you up and running with a local Kubernetes cluster powered by KinD. However, you may be willing to step away from the beaten path and install EDA in a non-KinD cluster. Well, EDA welcomes courageous souls like you!

/// admonition | Note
    type: subtle-note

1. In this section we are not going into the details of how to install EDA in a production setting, since there are many environment-specific considerations to take into account. Instead, we will focus on bringing up the **playground** environment on a non-KinD k8s cluster.
2. The default installation procedure assumes that `cert-manager` does not exist in the cluster and will be installed by the playground installer.

    If you already have the cert-manager installed in your cluster (cert-manager and cert-manager-csi-driver) you can skip the installation of cert-manager by setting the `NO_CERT_MANAGER_INSTALL := yes` in your [preferences file](../installation/customize-install.md#preferences-file).
///

Alright, truth be told, the installation process is almost identical to the one you followed in the [quickstart guide](../../getting-started/try-eda.md). This is one of the perks of running on top of Kubernetes that EDA enjoys - no matter what cluster it is (GKE, Openstack, k3s, minikube, etc), the installation process for the greater part would be the same.

Take a seat, we are going to install EDA on a "real" k8s cluster running on bare VMs. But first, let's see what we are working with:

```{.shell .no-select}
kubectl get nodes
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME         STATUS   ROLES           AGE   VERSION
rd-eda1-cp   Ready    control-plane   31d   v1.30.1
rd-eda1-w1   Ready    <none>          31d   v1.30.1
rd-eda1-w2   Ready    <none>          31d   v1.30.1
rd-eda1-w3   Ready    <none>          31d   v1.30.1
rd-eda1-w4   Ready    <none>          31d   v1.30.1
rd-eda1-w5   Ready    <none>          31d   v1.30.1
rd-eda1-w6   Ready    <none>          31d   v1.30.1
```
</div>

:scream: A 6-node k8s cluster running vanilla Kubernetes 1.30.1 release! Each node has 4vCPU and 16GB of RAM amounting to a total of 24vCPU and 96GB of RAM. This is a decent-sized cluster for running EDA [playground][pg-repo].

## Storage classes

Alright, first thing to ensure (besides of having the right context set in your `kubectl` of course) is that your cluster has some storage provider that gives you the default storage class. EDA Git deployments will have some PV claims and something needs to satisfy them, right?

There are plenty of [cloud-native storage solutions](https://landscape.cncf.io/guide#runtime--cloud-native-storage) to choose from, pick one that suites your needs in case your cluster doesn't have one.

To ensure you have one:

```{.shell .no-select}
kubectl get storageclass
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                 PROVISIONER          RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
longhorn (default)   driver.longhorn.io   Delete          Immediate           true                   36d
longhorn-static      driver.longhorn.io   Delete          Immediate           true                   36d
```
</div>

## Security context

If you run a cluster with a Pod Security Policy in place (like in case of a Talos cluster with defaults), make sure to allow a privileged policy for the `eda-system` namespace. The `cert-manager-csi-driver` daemonset requires this to run.

```{.bash .no-select}
kubectl create namespace eda-system

kubectl label namespace eda-system \
pod-security.kubernetes.io/enforce=privileged \
eda.nokia.com/core-ns=eda-system
```

## Playground repository

We will drive the installation process using the instrumentation provided by the Makefile stored in the [playground repository][pg-repo]. If you haven't done so yet, clone the repository and change into it:

--8<-- "docs/getting-started/try-eda.md:pull-playground"

If you already have the repository cloned, make sure to pull in the latest changes and remove the `eda-kpt` and `catalog` directories before proceeding.

## Parametrizing the installation

To no-one's surprise, the EDA installation process on an existing cluster would require us at least to skip the creation of the KinD cluster that `make try-eda` target would call otherwise. Let's do that by using the [prefs.mk](../../getting-started/installation-process.md#configure-your-deployment) file that the playground repository provides and set the following variables:

```makefile
# KinD cluster options
# -----------------------------------------------------------------------------|
# Do not deploy the kind cluster
# Uncomment this variable to perform playground installation
# on an already available k8s cluster
NO_KIND := yes

# How do clients reach your cluster?
#  EXT_DOMAIN_NAME can also be set to an ipv4/6 address if no domain record
#  is present. In that case EXT_IPV4_ADDR = $(EXT_DOMAIN_NAME) or its ipv6
#  counterpart.
# -----------------------------------------------------------------------------|
EXT_DOMAIN_NAME = "eda.mydomain.com" #(1)!
EXT_HTTPS_PORT = "443"
```

1. Set the DNS name or IP address of the cluster' ingress/gateway endpoint.

The key variables to set would be `NO_KIND := yes` to skip the creation of the KinD cluster and `EXT_DOMAIN_NAME` and `EXT_HTTPS_PORT` to set the ingress/gateway endpoint and port.

## Running the installation

With the `prefs.mk` file populated, we can simply run:

```{.shell .no-select}
make try-eda
```

Right, the same target that would otherwise install EDA on a local development KinD cluster can be used to install EDA on an existing cluster, like the one we have in this guide. After the installation process completes, you can use the [verification commands](../../getting-started/verification.md) to make sure everything is up and running.

![final-pods](https://gitlab.com/rdodin/pics/-/wikis/uploads/55b10f7ea1b74501ee2434641e17edc4/piceda1.webp){.img-shadow}

Now you have a fully functional EDA installation running in a real Kubernetes cluster. Congratulations :partying_face:

With a real cluster, you would likely want to have a GatewayAPI or Ingress configured so that you can access the EDA UI and API. We've prepared a [separate guide](../exposing-ui-api.md) to help you with that.

[pg-repo]: https://github.com/nokia-eda/playground
