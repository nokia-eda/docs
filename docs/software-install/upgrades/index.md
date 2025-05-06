# Upgrading EDA

Assuming you have a working EDA cluster, your upgrade process looks similar to an install + restore. An in place upgrade is not currently supported.

The upgrade procedure consists of:

1. Backup your existing cluster.
1. Pull the latest version of the `kpt` package.
1. Make any necessary edits to the `kpt` package.
1. Pause your clusters interaction with your infrastructure.
1. Stop EDA (on both the active and standby members if running geo redundant).
1. Install the new `kpt` package (on both active and standby members if running geo redundant).
1. Upgrade your applications.
1. Unpause your clusters interaction with your infrastructure.

/// details | Nuances for geo redundant clusters
    type: info
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

This will create a backup in a gzipped tarball format, which contains all the necessary information to restore your cluster.

Copy this backup outside of your `eda-toolbox` pod - as this pod is destroyed and recreated during the upgrade. Replace the file name with the one from the `edactl platform backup` command output and run:

```{.shell .no-select}
toolboxpod=$(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}")

kubectl cp eda-system/$toolboxpod:/eda/eda-backup-engine-config-2025-04-22_13-51-50.tar.gz \
    /tmp/eda-backup.tar.gz
```

The backup file will be copied to the `/tmp/eda-backup.tar.gz` file on your system.

## Upgrading EDA kpt packages

The workflow to upgrade the EDA kpt packages slightly differs depending on whether you have the original [playground directory](../preparing-for-installation.md#download-the-eda-installation-playground) present in a system that you used to install EDA originally from or not.

/// tab | If original playground repository present
If you have the original playground directory, you should upgrade your kpt packages in place. This is the recommended approach, as it will keep your customizations intact.

Change into the playground directory and run:

```{.shell .no-select}
git pull --rebase --autostash -v
```

///

/// tab | If playground repository missing
If you don't have the original playground directory, pull the repository again:

```shell
git clone https://github.com/nokia-eda/playground && \
cd playground
```

///

Then update the packages by executing the following command from the playground repository:

```shell
make download-tools download-pkgs update-pkgs
```

### Customizing kpt packages

If you have any customizations to your EDA installation, you should reapply them[^1] by setting the variables in the prefs.mk file as was done during the [installation phase](../deploying-eda/installing-the-eda-application.md#customizing-the-installation-file). Reconfigure the EDA core components using the following command:

```{.shell .no-select}
make eda-configure-core
```

At a minimum, ensure `EXT_DOMAIN_NAME` and `EXT_HTTPS_PORT` are set correctly in your `prefs.mk` file.

## Breaking geo redundancy (optional)

On your active cluster member, update your `EngineConfig` to remove the `.spec.cluster.redundant` section. This will break the geo redundancy and allow you to upgrade the active member without affecting the standby member.

/// admonition | Changes on standby members
    type: subtle-note
Do not update the EngineConfig resource on standby members. Although stopped, if the standby members were to start, they must continue to look for the active member (and fail to do so) throughout the upgrade.
///

## Pausing NPP interactions

Place your `TopoNode` resources into `emulate` mode by setting the resource's `.spec.npp.mode` from `normal` to `emulate`.

* In this mode, EDA does not interact with targets, effectively pausing the cluster's interaction with your infrastructure.
* You can still interact with EDA and the `TopoNode` resources; changes are pushed upon switching back to `normal` mode.

## Stopping EDA

To stop EDA, enter the following command:

```{.shell .no-select}
edactl cluster stop
```

This command returns no output, but will result in all Pods packaged as part of `eda-kpt-base` being stopped and removed from the cluster. You can verify this with (replace with your base namespace if you modified it):

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
For geo redundant clusters, execute the `edactl cluster stop` command on both active and standby members, via their respective `eda-toolbox` Pods.
///

## Installing the new version of EDA

Enter the following command:

```{.shell .no-select}
make install-external-packages eda-install-core eda-is-core-ready
```

## Restoring your backup

You should execute this in the new `eda-toolbox` pod (typically in the `eda-system` Namespace). This will restore your cluster to its previous state.

```{.shell .no-select}
edactl platform restore /tmp/eda-backup.tar.gz
```

## Upgrading your applications

A default install of EDA will install current-version applications, but your restore will have restored previous versions. These versions may be incompatible with the new version of EDA core, and must be upgraded immediately following the upgrade. The existing `Makefile` can be used to do so:

```{.shell .no-select}
make eda-install-apps
```

## Allowing NPP interactions

Re-enable interactions with your targets by placing your `TopoNode` resources back into `normal` mode by changing resource's `.spec.npp.mode` value from `emulate` to `normal`.

## Verifying cluster health

Check the following to ensure your cluster is healthy:

* All pods are running and healthy.
* All `TopoNode` resources are in `normal` mode, and have synced with their targets.
* No transaction failures exist.
* All cluster members are synchronized.

[^1]: see [Installation customization](../../software-install/customize-install.md) for more details
