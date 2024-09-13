# EDA on an on-premises k8s cluster

/// admonition | Work in progress
    type: danger
This document has not been updated and contains outdated information.
///

The [quickstart guide](../../getting-started/installation-process.md) did a great job of getting you up and running with a local Kubernetes cluster powered KinD. However, you may be willing to step away from the beaten path and install EDA in a non-KinD cluster. Well, EDA welcomes courageous souls like you!

Alright, truth be told, the installation process is almost identical to the one you followed in the quickstart guide, it is just a matter of having a few things to consider. In this section we will install EDA in a real k8s cluster running on bare VMs.

First, let's see what we are working with:

```{.shell .no-select}
kubectl get nodes
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME         STATUS   ROLES           AGE   VERSION
rd-eda1-cp   Ready    control-plane   14h   v1.30.1
rd-eda1-w1   Ready    <none>          14h   v1.30.1
rd-eda1-w2   Ready    <none>          14h   v1.30.1
rd-eda1-w3   Ready    <none>          14h   v1.30.1
```
</div>

:scream: A real 3-node k8s cluster running vanilla Kubernetes 1.30.1 release! Each node has 6vCPU and 24GB of RAM amounting to a total of 18vCPU and 72GB of RAM. This is a decent little cluster for running EDA.

/// note
If you run a cluster with a Pod Security Policy in place, make sure to allow a privileged policy for the `default` namespace. The `cert-manager-csi-driver` daemonset requires this to run.

```{.bash .no-select}
kubectl label namespace default pod-security.kubernetes.io/enforce=privileged
```

///

Using the same `playground` repository from the [Installation section](../../getting-started/installation-process.md), we can use the same `make` targets to perform the installation steps (if haven't done before).

1. `make download-tools` - to download the necessary tools.
2. `make download-pkgs` - to download the EDA `kpt` package.

Now, we can install the EDA core services.

```shell
make eda-install-core
```

Pause for a moment and let the installation complete, by checking the [verification steps](../../getting-started/verification.md#eda-core).

Once all EDA deployments are running and appstore is reachable, proceed with the application install, just like in the [quickstart guide](../../getting-started/installation-process.md#apps).

```shell
make eda-install-apps
```

With apps loaded, bootstrap the EDA installation by running the following command, exactly like in the quickstart guide:

```shell
make eda-bootstrap
```

And that's it, EDA has been successfully installed in a non-KinD cluster. Now let's deploy the same sample topology, by following the steps from the ["Onboarding nodes"](../../getting-started/virtual-network.md) guide.

```shell
make topology-load
```

and your cluster now is busy pulling the simulators, starting them up and laying out the interfaces between them. Use the [verification commands](../../getting-started/verification.md#node-connectivity) to make sure the topology is up and running.

This may take a while (watch your pods status), but it should eventually complete successfully:

```{.shell .no-select}
kubectl get toponodes
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME     PLATFORM       VERSION    OS    ONBOARDED   NPP         NODE     AGE
leaf1    7220 IXR-D3L   24.7.1     srl   true        Connected   Synced   6m28s
leaf2    7220 IXR-D3L   24.7.1     srl   true        Connected   Synced   6m28s
spine1   7220 IXR-D5    24.7.1     srl   true        Connected   Synced   6m28s
```
</div>

![final-pods](https://gitlab.com/rdodin/pics/-/wikis/uploads/55b10f7ea1b74501ee2434641e17edc4/piceda1.webp){.img-shadow}

Now you have a fully functional EDA installation running in a real Kubernetes cluster. Congratulations :partying_face:
