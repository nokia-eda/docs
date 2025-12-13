
# Bootstrap the Talos Kubernetes cluster

When all the virtual machines are deployed and running, you can set up the Kubernetes cluster on the virtual machines using Talos.

/// admonition | Note
    type: subtle-note
The procedures in this chapter use the `edaadm` command. Ensure that the command is available, as well as the original EDAADM configuration file from which you generated Talos files.
///

## Bootstrapping Kubernetes on the primary node

After booting the Talos VMs, you can now bootstrap the Kubernetes cluster using the `edaadm` command.

Execute the following command:

```bash
edaadm bootstrap-k8s -c eda-input-6-node.yaml #(1)!
```

1. `-c`: Specifies the EDAADM configuration file.

Wait for several minutes for the Kubernetes cluster to come up and for all the nodes join the cluster. The process should take less than 15 minutes.

## Obtaining the Kubernetes config file for kubectl

Use the talosctl command to obtain the Kubernetes configuration file for use with kubectl.

Obtain the Kubernetes configuration file with:

```bash
edaadm get-kubeconfig -c eda-6-node-deployment.yaml #(1)!
```

1. `-c`: Specifies the EDAADM configuration file.

You can configure your environment to use the `​kubeconfig`​ file for use with the kubectl command.

```bash
export KUBECONFIG=eda-compute-cluster/kubeconfig
```

Inspect your k8s cluster and check if all nodes are up and running.

```bash
kubectl get nodes
```

When all the nodes are up and Kubernetes is stable, continue with [Setting up the Rook Ceph storage cluster](#setting-up-the-rook-ceph-storage-cluster).

## Setting up the Rook Ceph storage cluster

EDA uses Rook Ceph as a secure, distributed, and redundant data store for all the data it stores. Using Ceph guarantees redundancy and high availability of all data by providing multiple copies of all data. The following steps guide you through the configuration and deployment of Rook Ceph.

/// html | div.steps

1. Add the Rook Ceph Helm chart.

    /// admonition | Caution
        type: note
    Only do this step for an **Internet based installation**, not for an Air-Gapped installation.
    ///

    ```
    helm repo add rook-release https://charts.rook.io/release
    ```

2. Using the `rook-ceph-operator-values.yaml` file that edaadm generated based on the configuration, deploy the Rook Ceph Operator.

    /// tab | Internet based installation

    ```bash
    helm install --create-namespace \
      --namespace rook-ceph \
      --version -{{ rook_ceph_version }}- \
      -f path/to/rook-ceph-operator-values.yaml \
      rook-ceph rook-release/rook-ceph
    ```

    ///

    /// tab | Air-gapped installation

    ```bash
    helm install --create-namespace \
      --namespace rook-ceph \
      --version -{{ rook_ceph_version }}- \
      -f path/to/rook-ceph-operator-values.yaml \
      rook-ceph \
      http://eda:eda@<ASSETS VM IP>/artifacts/rook-ceph--{{ rook_ceph_version }}-.tgz
    ```

    ///

3. Using the `rook-ceph-cluster-values.yaml` file that the `edaadm` tool generated, deploy the Rook Ceph Cluster.

    /// tab | Internet based installation

    ```
    helm install \
      --namespace rook-ceph \
      --set operatorNamespace=rook-ceph \
      -f path/to/rook-ceph-cluster-values.yaml \
      rook-ceph-cluster rook-release/rook-ceph-cluster
    ```

    ///

    /// tab | Air-gapped installation

    ```bash
    helm install \ 
      --namespace rook-ceph \ 
      --set operatorNamespace=rook-ceph \ 
      -f path/to/rook-ceph-cluster-values.yaml \ 
      rook-ceph-cluster \
      http://eda:eda@<ASSETS VM IP>/artifacts/rook-ceph-cluster-v1.15.0.tgz
    ```

    ///

    The output from this command can report missing CRDs; wait until the Rook Ceph Operator is running in the Kubernetes cluster.

4. Using `kubectl` commands, verify that the operator is deployed and the necessary pods are deployed before installing the EDA application.
    This example is for a six-node cluster, with six storage nodes.

    ```
    kubectl -n rook-ceph get pods
    ```

    <div class="embed-result">
    ```
    NAME                                               READY   STATUS      RESTARTS        AGE
    csi-cephfsplugin-22rmj                             2/2     Running     1 (6m32s ago)   7m6s
    csi-cephfsplugin-25p9d                             2/2     Running     1 (6m30s ago)   7m6s
    csi-cephfsplugin-2gr8v                             2/2     Running     4 (5m16s ago)   7m6s
    csi-cephfsplugin-48cwk                             2/2     Running     1 (6m30s ago)   7m6s
    csi-cephfsplugin-fknch                             2/2     Running     2 (5m32s ago)   7m6s
    csi-cephfsplugin-provisioner-67c8454ddd-mpq4w      5/5     Running     1 (6m1s ago)    7m6s
    csi-cephfsplugin-provisioner-67c8454ddd-qmdrq      5/5     Running     1 (6m18s ago)   7m6s
    csi-cephfsplugin-vfxnf                             2/2     Running     1 (6m32s ago)   7m6s
    rook-ceph-mds-ceph-filesystem-a-7c54cdf5bc-lmf6n   1/1     Running     0               2m40s
    rook-ceph-mds-ceph-filesystem-b-6dc794b9f4-2lc64   1/1     Running     0               2m37s
    rook-ceph-mgr-a-55b449c844-wpps8                   2/2     Running     0               4m30s
    rook-ceph-mgr-b-5f97fd5746-fzngx                   2/2     Running     0               4m30s
    rook-ceph-mon-a-76fcb96c4c-vscnc                   1/1     Running     0               5m53s
    rook-ceph-mon-b-68bf5974bb-p2vnj                   1/1     Running     0               4m57s
    rook-ceph-mon-c-6d7c64dcb6-phs99                   1/1     Running     0               4m47s
    rook-ceph-operator-5f4c4bff8d-2fsq2                1/1     Running     0               7m54s
    rook-ceph-osd-0-bf89f779-zh4kd                     1/1     Running     0               3m49s
    rook-ceph-osd-1-64dcd64c5f-7xcbm                   1/1     Running     0               3m49s
    rook-ceph-osd-2-54ddd95489-5qkdt                   1/1     Running     0               3m49s
    rook-ceph-osd-3-56cbd54bd6-7mt8w                   1/1     Running     0               3m39s
    rook-ceph-osd-4-567dcff476-wljll                   1/1     Running     0               2m56s
    rook-ceph-osd-5-6f69c998b6-2l5wp                   1/1     Running     0               2m54s
    rook-ceph-osd-prepare-eda-dev-node01-7rfkn         0/1     Completed   0               4m8s
    rook-ceph-osd-prepare-eda-dev-node02-rqdkx         0/1     Completed   0               4m8s
    rook-ceph-osd-prepare-eda-dev-node03-xtznb         0/1     Completed   0               4m8s
    rook-ceph-osd-prepare-eda-dev-node04-db4v8         0/1     Completed   0               4m7s
    rook-ceph-osd-prepare-eda-dev-node05-29wwm         0/1     Completed   0               4m7s
    rook-ceph-osd-prepare-eda-dev-node06-zxp2x         0/1     Completed   0               4m7s
    rook-ceph-tools-b9d78b5d4-8r62p                    1/1     Running     0               7m6s
    ```
    </div>

    /// admonition | Note
        type: subtle-note
    Some of the pods may restart as they initiate Ceph. This behavior is expected.
    ///

///
