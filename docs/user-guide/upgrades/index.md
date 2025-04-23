# Upgrading EDA

Assuming you have a working EDA cluster, your upgrade process looks similar to an install[^1] + restore. An in place upgrade is not currently supported.

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
For geo redundant clusters, you currently may not run cluster members at different versions. Therefore cluster redundancy must be broken before the upgrade, and restored after the upgrade. This is done by removing the `.spec.cluster.redundant` section from the `EngineConfig` resource, documented below.
///
## Backing up your cluster

Backing up your existing cluster is as simple as executing:

```{.shell .no-select}
edactl platform backup
```

<div class="embed-result highlight">
```{.shell .no-select .no-copy}
Platform backup done at eda-backup-engine-config-2025-04-22_13-51-50.tar.gz
```
</div>

from the `eda-toolbox` Pod (typically in the `eda-system` Namespace). This will create a backup in a gzipped tarball format, which contains all the necessary information to restore your cluster.

If you do not plan on building a new Kubernetes cluster, this backup will not be used - but you should always take one anyway!

You should copy this backup outside of your `eda-toolbox` Pod - as this Pod will be destroyed and recreated during the upgrade. This can be accomplished with (replacing with your own Pod name and file name):

```{.shell .no-select}
kubectl cp eda-toolbox-6d598f6db7-thlj7:/eda/eda-backup-engine-config-2025-04-22_13-51-50.tar.gz /tmp/eda-backup.tar.gz
```


## Upgrading EDA kpt packages

If you have your previous installation directory (that with which `kpt` has been applied from), you may upgrade your kpt packages in place. This is the recommended approach, as it will keep your customizations intact.

```{.shell .no-select}
git pull --rebase --autostash -v
```

Or pull the new kpt packages into a new playground directory, and reapply your customizations:

<!-- --8<-- [start:pull-playground] -->
```shell
git clone https://github.com/nokia-eda/playground && \
cd playground
make download-tools download-pkgs update-pkgs
```
<!-- --8<-- [end:pull-playground] -->


### Customize kpt packages

If you have any customizations to your EDA installation, you should reapply them; see [Installation customization](../installation/customize-install.md) for more details.:

```{.shell .no-select}
make eda-configure-core
```

At a minimum you should ensure `EXT_DOMAIN_NAME` and `EXT_HTTPS_PORT` are set correctly in your `prefs.mk` file.

## Break geo redundancy (optional)

On your active cluster member, update your `EngineConfig` to remove the `.spec.cluster.redundant` section. This will break the geo redundancy and allow you to upgrade the active member without affecting the standby member.

/// admonition | Changes on standby members
    type: subtle-note
Do not update your `EngineConfig` on standby members - although stopped, if they were to start they must continue to look for the active member (and fail to do so) throughout the upgrade.
///

## Pause interactions

Place your `TopoNode` resources into `emulate` mode.
  * In this mode, EDA will not interact with targets - effectively pausing the clusters interaction with your infrastructure.
  * You are still able to interact with EDA and the `TopoNode` resources - changes will be pushed upon switching back to `normal` mode.


## Stop EDA

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

## Install the new version of EDA

```{.shell .no-select}
make install-external-packages eda-install-core eda-is-core-ready
```


## Restore your backup

You should execute this in the new `eda-toolbox` Pod (typically in the `eda-system` Namespace). This will restore your cluster to its previous state.

```{.shell .no-select}
edactl platform restore /tmp/eda-backup.tar.gz
```

## Upgrade your applications

A default install of EDA will install current-version applications, but your restore will have restored previous versions. These versions may be incompatible with the new version of EDA core, and must be upgraded immediately following the upgrade. The existing `Makefile` can be used to do so:

```{.shell .no-select}
make eda-install-apps
```

## Allow target interactions

Re-enable interactions with your targets by placing your `TopoNode` resources back into `normal` mode.

## Verify

You should check the following to ensure your cluster is healthy:
* All Pods are running and healthy.
* All `TopoNode` resources are in `normal` mode, and have synced with their targets.
* No transaction failures exist.
* All cluster members are synchronized.

[^1]: Installation of the new cluster is not covered in this guide. You should consult our install guide or your Kubernetes distro's documentation for this.