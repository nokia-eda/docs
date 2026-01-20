# Upgrading EDA

Assuming you have a working EDA cluster the upgrade procedure will consist of the following steps:

1. Pause NPP interactions.
2. Backup your existing cluster.
3. Update the [playground][playground] repository.
4. Uninstall the existing version of EDA.
5. Install the new EDA `kpt` package (on both active and standby members if running geo redundant).
6. Restore your backup.
7. Upgrade your applications.
8. Resume NPP interactions.

/// admonition | Nuances for Air-gapped and Geo-redundant clusters
    type: info
The upgrade procedure does not change based on whether you have the Internet or Air-gapped cluster. But keep in mind that with the Air-gapped installation the target release bundles should be [uploaded to the Assets VM](../air-gapped/deploying-the-assets-vm.md#uploading-the-assets-to-the-assets-vm) first before proceeding with an upgrade.

In geo redundant clusters, cluster members cannot run different versions. Therefore, before the software upgrade, you must first break cluster redundancy and then restore redundancy after the upgrade. To break the redundancy, remove the `.spec.cluster.redundant` section from the `EngineConfig` resource as described later in this document.
///

/// admonition | EDA upgrade procedure scope
    type: subtle-note
This is the Nokia EDA software upgrade procedure, it does not cover upgrading Talos Linux or Kubernetes. Nokia EDA does not require upgrading Talos or Kubernetes for every EDA version upgrade, unless explicitly stated in the release notes.

In case Talos and/or Kubernetes upgrade is desired perform **one of** the following:
/// tab | Install a new EDA cluster
When running EDA cluster on virtual machines it might be easier to perform a new installation with the desired Talos and Kubernetes versions and restore your existing cluster backup into the new cluster:

1. Take a backup of your existing EDA cluster.
2. Download an `edaadm` version that comes with the desired Talos and Kubernetes versions as per the [version matrix](../index.md#version-information).
3. Install a new EDA cluster following the [installation procedure](../index.md).
4. Restore your backup in the new cluster and upgrade your EDA applications if necessary.
///
/// tab | Upgrade in a running EDA cluster
Follow the respective [Talos Linux upgrade documentation](https://docs.siderolabs.com/talos/v1.11/configure-your-talos-cluster/lifecycle-management/upgrading-talos) for upgrading Talos Linux and Kubernetes versions in a running EDA cluster.
///
///

## Pausing NPP interactions

Prior to taking a backup of your cluster, place all `TopoNode` resources into `emulate` mode to avoid any ongoing interactions with the network devices during the upgrade process.

In this mode, EDA does not interact with target devices, effectively pausing the cluster's interaction with your infrastructure. You can still interact with EDA and the `TopoNode` resources; changes are pushed upon switching back to `normal` mode.

To set `emulate` mode in bulk, run the script from the [playground](https://github.com/nokia-eda/playground) repo directory on a machine where you have [`kubectl`](../../user-guide/using-the-clis.md#kubectl) configured with the access to your cluster:

```{.shell .no-select}
make set-npp-mode-emulate
```

After the script has been run, verify that the `TopoNode` resources are in `emulate` mode:

```{.shell .no-select}
kubectl get toponode -A \
-o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,MODE:.spec.npp.mode'
```

<div class="embed-result">
```{.shell .no-select .no-copy}
NAMESPACE       NAME     MODE
my-other-ns     leaf1    emulate
my-other-ns     leaf2    emulate
my-other-ns     leaf3    emulate
my-other-ns     leaf4    emulate
my-other-ns     spine1   emulate
my-other-ns     spine2   emulate
eda             leaf1    emulate
eda             leaf2    emulate
eda             spine1   emulate
```
</div>

## Backing up your cluster

Backing up your existing cluster is performed using the `collect-backup` target provided in the [`Makefile`](https://github.com/nokia-eda/playground/blob/main/Makefile) of the playground repository.

```{.shell .no-select}
make collect-backup
```

<div class="embed-result">
```{.shell .no-select .no-copy}
[ INFO ] Starting backup
Platform backup done at /tmp/eda-platform-backup-2025-12-18-21-37-42.tar.gz
[  OK  ] Collected backup
[ INFO ] Transferring to host /tmp/eda-support/logs-2025-12-18/eda-platform-backup-2025-12-18-21-37-42.tar.gz
tar: Removing leading `/' from member names
[  OK  ] Transferred to /tmp/eda-support/logs-2025-12-18/eda-platform-backup-2025-12-18-21-37-42.tar.gz
```
</div>

This will create a timestamped backup archive in the toolbox pod and copy it to the system where make target was run in the `/tmp/eda-support/logs-<date>` directory. The backup archive contains all the necessary information to restore your cluster.

/// warning | Testing the backup
It is highly recommended to test the backup by restoring it in a test cluster before proceeding with the upgrade of your production cluster.
///

## Updating playground repository

The workflow to upgrade EDA slightly differs depending on whether you have the original [playground repository][playground] present in a system that you used to install EDA originally from or not.

[playground]: ../preparing-for-installation.md#download-the-eda-installation-playground

/// tab | Playground repository present

If you have an existing [playground repository][playground], ensure it is up to date by running:

```bash
git pull --rebase --autostash -v
```

This will update the playground repository while keeping any customizations you may have done to the `prefs.mk` file.

///

/// tab | Playground repository missing
If the original playground repository is missing, you should clone the repository again:

```bash
git clone https://github.com/nokia-eda/playground && \
cd playground && \
make download-tools
```

Identify what EDA version you are running using [edactl](../../user-guide/using-the-clis.md#edactl):

```bash
edactl cluster
```

<div class="embed-result">
```{.shell .no-select .no-copy}
Name           Address  ActivityState  BuildVersion                  CoreVersion  AvgLatency(ms)  Reachable  Synchronized
 engine-config  self     Active         v25.4.1-2504252348-g720b7d2e  v2.0.0-0                     true       true
```
</div>

In this example, we have EDA version `25.4.1`.

Set the `EDA_CORE_VERSION` and `EDA_APPS_VERSION` variables in the `prefs.mk` file to the **existing** version you noted above if it is not already set. For example:

```text title="snippet from prefs.mk"
EDA_CORE_VERSION=25.4.1
EDA_APPS_VERSION=25.4.1
```

Apply any other customizations required to the `prefs.mk` file as explained on the [installation page](../deploying-eda/installing-the-eda-application.md#customizing-the-installation).

With the existing version set and customizations added to the `prefs.mk` file, download the EDA packages for the currently running EDA system:

```bash
make download-pkgs
```

<div class="embed-result">
```{.shell .no-select .no-copy}
❯ make download-pkgs
--> INFO: Updating /home/rd/nokia-eda/playground/eda-kpt
--> INFO: Updating /home/rd/nokia-eda/playground/catalog
--> INFO: /home/rd/nokia-eda/playground/eda-kpt - selected version: 25.4.1
--> INFO: /home/rd/nokia-eda/playground/eda-kpt - is at 25.4.1
--> INFO: /home/rd/nokia-eda/playground/catalog - selected version: 25.4.1
--> INFO: /home/rd/nokia-eda/playground/catalog - is at 25.4.1
```
</div>

///

Ensure the package inventory is in sync with your existing cluster:

```bash
make cluster-restore-inventory
```

## Uninstalling EDA components

The existing EDA core components must be uninstalled, before installing the new version.

### Breaking geo redundancy <small>(optional)</small>

If you have a geo-redundant installation, on your active cluster member, update your `EngineConfig` to remove the `.spec.cluster.redundant` section. This will break the geo redundancy and allow you to upgrade the active member without affecting the standby member.

/// admonition | Changes on standby members
    type: subtle-note
Do not update the EngineConfig resource on standby members. Although stopped, if the standby members were to start, they must continue to look for the active member (and fail to do so) throughout the upgrade.
///

### Stopping EDA platform

To stop EDA components, enter the following command:

```{.shell .no-select}
make eda-stop-core
```

This command returns no output, but will result in all Pods packaged as part of `eda-kpt-base` being stopped and removed from the cluster.

/// details | Nuances for geo redundant clusters
    type: info
For geo redundant clusters, execute the `edactl platform stop` command on both active and standby members, via their respective `eda-toolbox` Pods.
///

### Uninstalling EDA core components

Proceed with uninstalling EDA core components:

```bash
make eda-uninstall-core
```

You should now see no core components in your cluster. Check with the following command[^1]:

```{.shell .no-select}
kubectl get pods -n eda-system
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
NAME                                  READY   STATUS    RESTARTS   AGE
cert-manager-csi-driver-n9bwk         3/3     Running   0          95m
eda-fluentbit-b7fns                   1/1     Running   0          96m
eda-fluentd-7cd48db9c5-9pvvp          1/1     Running   0          96m
eda-git-5db9dfc7bc-mn4rw              1/1     Running   0          95m
eda-git-replica-f69b9c9f4-bngf8       1/1     Running   0          95m
trust-manager-69955c46b8-bghj6        1/1     Running   0          95m
```
</div>

### Stopping EDA git servers

Continue with stopping EDA Git servers by scaling down the EDA Git deployments:

```{.shell .no-select}
make scale-down-git-servers
```

## Updating EDA kpt packages

Set the desired EDA version in the `prefs.mk` file to match the target version you want to upgrade to. For example, to choose the -{{eda_version}}- version:

```text
EDA_CORE_VERSION=-{{eda_version}}-
EDA_APPS_VERSION=-{{eda_version}}-
```

Download the tools and packages by executing the following command:

```shell
make download-tools download-pkgs
```

### Customizing kpt packages

If you started with a freshly cloned repository, you want to add customizations to your EDA installation by setting the variables in the `prefs.mk` file; this process is explained in details at the [installation phase](../deploying-eda/installing-the-eda-application.md#customizing-the-installation).

> At a minimum, ensure `EXT_DOMAIN_NAME` and `EXT_HTTPS_PORT` are set correctly in your `prefs.mk` file.

Configure the packages downloaded for the target EDA version with the customizations you added to the `prefs.mk` file:

```{.shell .no-select}
make eda-configure-core
```

## Installing the new version of EDA

Install the new version of EDA core components by running:

```{.shell .no-select}
make install-external-packages eda-install-core eda-is-core-ready
```

## Restoring your backup

Copy the backup file you [collected at the beginning](#backing-up-your-cluster) of this procedure from your machine back into the new `eda-toolbox` pod:

```{.shell .no-select}
backupfile=/tmp/eda-support/logs-2025-12-18/eda-platform-backup-2025-12-18-21-37-42.tar.gz

toolboxpod=$(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}")

kubectl -n eda-system cp $backupfile \
  $toolboxpod:/tmp/eda-backup.tar.gz
```

Restore your cluster to its previous state by running:

```{.shell .no-select}
edactl platform restore /tmp/eda-backup.tar.gz
```

## Upgrading your applications

Installing the new version of EDA will deploy application versions according to the installed release; however, the backup restore operation will have restored application versions as they were set in the original cluster. These versions may be incompatible with the new version of EDA core, and must be upgraded immediately following the EDA backup restore. The existing `Makefile` can be used to do so:

```{.shell .no-select}
make eda-install-apps
```

## Resume NPP interactions

To resume NPP interactions, set all `TopoNode` resources back to the `normal` mode.

```{.shell .no-select}
make set-npp-mode-normal
```

After the script has been run, verify that the `TopoNode` resources are in `normal` mode:

```{.shell .no-select}
kubectl get toponode -A \
-o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,MODE:.spec.npp.mode'
```

<div class="embed-result">
```{.shell .no-select .no-copy}
NAMESPACE       NAME     MODE
my-other-ns     leaf1    normal
my-other-ns     leaf2    normal
my-other-ns     leaf3    normal
my-other-ns     leaf4    normal
my-other-ns     spine1   normal
my-other-ns     spine2   normal
eda             leaf1    normal
eda             leaf2    normal
eda             spine1   normal
```
</div>

## Verifying cluster health

Check the following to ensure your cluster is healthy:

* All pods are running and healthy.
* All `TopoNode` resources are in `normal` mode, and have synced with their targets.
* No transaction failures exist.
* All cluster members are synchronized.

[^1]: replace with your base namespace if you modified it.
