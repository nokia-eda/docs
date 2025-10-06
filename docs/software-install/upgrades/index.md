# Upgrading EDA

Assuming you have a working EDA cluster the upgrade procedure will consist of the following steps:

1. Backup your existing cluster.
2. Update the [playground][playground] repository.
3. Uninstall the existing version of EDA.
4. Install the new EDA `kpt` package (on both active and standby members if running geo redundant).
5. Restore your backup.
6. Upgrade your applications.

/// admonition | Nuances for Air-gapped and Geo-redundant clusters
    type: info
The upgrade procedure does not change based on whether you have the Internet or Air-gapped cluster. But keep in mind that with the Air-gapped installation the target release bundles should be [uploaded to the Assets VM](../air-gapped/deploying-the-assets-vm.md#uploading-the-assets-to-the-assets-vm) first before proceeding with an upgrade.

In geo redundant clusters, cluster members cannot run different versions. Therefore, before the software upgrade, you must first break cluster redundancy and then restore redundancy after the upgrade. To break the redundancy, remove the `.spec.cluster.redundant` section from the `EngineConfig` resource as described later in this document.
///

## Backing up your cluster

Backing up your existing cluster is performed using the [`edactl` CLI tool](../../user-guide/using-the-clis.md#edactl):

```{.shell .no-select}
edactl platform backup
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
Platform backup done at eda-backup-engine-config-2025-04-22_13-51-50.tar.gz
```
</div>

This will create a backup in a gzipped tarball format in the toolbox pod. The backup archive contains all the necessary information to restore your cluster.

Copy this backup outside of your `eda-toolbox` pod - as this pod is destroyed and recreated during the upgrade. Replace the file name with the one from the `edactl platform backup` command output and run:

```{.shell .no-select}
toolboxpod=$(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}")

kubectl cp eda-system/$toolboxpod:/eda/eda-backup-engine-config-2025-04-22_13-51-50.tar.gz \
    /tmp/eda-backup.tar.gz
```

The backup file will be copied to the `/tmp/eda-backup.tar.gz` file on your system.

## Updating playground repository

The workflow to upgrade EDA slightly differs depending on whether you have the original [playground repository][playground] present in a system that you used to install EDA originally from or not.

[playground]: ../preparing-for-installation.md#download-the-eda-installation-playground

/// tab | Playground repository present

If you have an existing [playground repository][playground] ensure it is up to date by running:

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

## Uninstalling EDA core components

The existing EDA core components must be uninstalled, before installing the new version.

### Breaking geo redundancy <small>(optional)</small>

If you have a geo-redundant installation, on your active cluster member, update your `EngineConfig` to remove the `.spec.cluster.redundant` section. This will break the geo redundancy and allow you to upgrade the active member without affecting the standby member.

/// admonition | Changes on standby members
    type: subtle-note
Do not update the EngineConfig resource on standby members. Although stopped, if the standby members were to start, they must continue to look for the active member (and fail to do so) throughout the upgrade.
///

### Pausing NPP interactions

Place your `TopoNode` resources into `emulate` mode by setting the resource's `.spec.npp.mode` from `normal` to `emulate`.

* In this mode, EDA does not interact with targets, effectively pausing the cluster's interaction with your infrastructure.
* You can still interact with EDA and the `TopoNode` resources; changes are pushed upon switching back to `normal` mode.

You can do this with running the following script in on your machine where you have `kubectl` configured to access your cluster:

```{.shell .no-select}
make set-npp-mode-emulate
```

After patching script is run, verify that the `TopoNode` resources are in `emulate` mode:

```{.shell .no-select}
kubectl get toponode -A \
-o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,MODE:.spec.npp.mode'
```

<div class="embed-result">
```{.shell .no-select .no-copy}
NAMESPACE       NAME     MODE
eda-telemetry   leaf1    emulate
eda-telemetry   leaf2    emulate
eda-telemetry   leaf3    emulate
eda-telemetry   leaf4    emulate
eda-telemetry   spine1   emulate
eda-telemetry   spine2   emulate
eda             leaf1    emulate
eda             leaf2    emulate
eda             spine1   emulate
```
</div>

### Stopping EDA platform

To stop EDA components, enter the following command:

```{.shell .no-select}
make eda-stop-core
```

This command returns no output, but will result in all Pods packaged as part of `eda-kpt-base` being stopped and removed from the cluster.

### Uninstalling EDA core

Proceed with EDA core components uninstallation:

```bash
make eda-uninstall-core
```

Now you should see no core components in your cluster. Check with the following command[^2]:

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
eda-toolbox-6d598f6db7-thlj7          1/1     Running   0          95m
trust-manager-69955c46b8-bghj6        1/1     Running   0          95m
```
</div>

/// details | Nuances for geo redundant clusters
    type: info
For geo redundant clusters, execute the `edactl platform stop` command on both active and standby members, via their respective `eda-toolbox` Pods.
///

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

Copy the backup file you extracted at the beginning of this procedure back into the new `eda-toolbox` pod:

```{.shell .no-select}
toolboxpod=$(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}")

kubectl -n eda-system cp /tmp/eda-backup.tar.gz \
  $toolboxpod:/tmp/eda-backup.tar.gz
```

Restore your cluster to its previous state by running:

```{.shell .no-select}
edactl platform restore /tmp/eda-backup.tar.gz
```

## Upgrading your applications

A default install of EDA will install current-version applications, but your restore will have restored previous versions. These versions may be incompatible with the new version of EDA core, and must be upgraded immediately following the upgrade. The existing `Makefile` can be used to do so:

```{.shell .no-select}
make eda-install-apps
```

## Verifying cluster health

Check the following to ensure your cluster is healthy:

* All pods are running and healthy.
* All `TopoNode` resources are in `normal` mode, and have synced with their targets.
* No transaction failures exist.
* All cluster members are synchronized.

[^1]: see [Installation customization](../../software-install/deploying-eda/installing-the-eda-application.md#customizing-the-installation) for more details.
[^2]: replace with your base namespace if you modified it.
