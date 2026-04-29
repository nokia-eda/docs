# Software upgrade

This document describes the procedure for an in-place upgrade of the existing Nokia EDA software without redeploying the underlying VMs and/or Kubernetes cluster.

If you already have a working Nokia EDA cluster, the upgrade procedure consists of the following steps:

1. Pause NPP interactions.
2. Backup the existing Nokia EDA cluster.
3. Update the [playground][playground] repository.
4. Uninstall the existing version of EDA.
5. Update and install the new EDA `kpt` packages (on both active and standby members if running a geo-redundant deployment).
6. Upgrade Nokia EDA applications.
7. Resume NPP interactions.

/// admonition | Nuances for air-gapped and Geo-redundant clusters
    type: info
Whether your cluster is Internet-connected or air-gapped, the upgrade procedure is the same. For air-gapped installations, upload the target app bundles to the [Assets Host](../air-gapped/uploading-assets.md) before proceeding with an upgrade.

In geo-redundant clusters, cluster members cannot run different versions. Therefore, before the software upgrade, you must first break cluster redundancy and then restore redundancy after the upgrade. To break the redundancy, remove the `.spec.cluster.redundant` section from the `EngineConfig` resource as described later in this document.
///

/// admonition | Version-specific upgrade considerations
    type: info
When upgrading from versions **older than 25.4.1**, ensure that the NodeGroup resources used by the nodes contain both gNOI and gNSI services.

```bash title="Example NodeGroup resource with gNOI and gNSI services"
kubectl get -n eda nodegroup sudo -o yaml
```

<div class="embed-result">
```{.shell .no-select .no-copy}
apiVersion: aaa.eda.nokia.com/v1alpha1
kind: NodeGroup
metadata:
  labels:
    eda.nokia.com/bootstrap: "true"
  name: sudo
  namespace: eda
spec:
  services:
  - GNMI
  - CLI
  - NETCONF
  - GNSI # <--- ensure gNSI is present
  - GNOI # <--- ensure gNOI is present
  superuser: true
```
</div>
///

/// admonition | Nokia EDA upgrade procedure scope
    type: subtle-note
This is the Nokia EDA software upgrade procedure; it does not cover upgrading Talos Linux or Kubernetes. Nokia EDA does not require upgrading Talos or Kubernetes for every EDA version upgrade, unless explicitly stated in the release notes.

If you want to upgrade Talos Linux, Kubernetes, or both, perform **one of** the following:
/// tab | Install a new EDA cluster
When running Nokia EDA cluster on virtual machines it might be easier to perform a new installation with the desired Talos and Kubernetes versions and restore your existing cluster backup into the new cluster:

1. Take a backup of your existing Nokia EDA cluster.
2. Download an `edaadm` version that comes with the desired Talos and Kubernetes versions as per the [version matrix](../index.md#version-information).
3. Install a new Nokia EDA cluster following the [installation procedure](../index.md).
4. Restore your backup in the new cluster and upgrade your EDA applications if necessary.
///

/// tab | Upgrade in a running EDA cluster
Follow the [Talos Linux upgrade documentation](https://docs.siderolabs.com/talos/-{{talos_version}}-/configure-your-talos-cluster/lifecycle-management/upgrading-talos) for the Talos release installed on your cluster (replace `v1.11` in the URL with your version when it differs) when upgrading Talos Linux and Kubernetes in a running EDA cluster.
///
///

## Pausing NPP interactions

Prior to taking a backup of your cluster, place all `TopoNode` resources into `emulate` mode to avoid any ongoing interactions with the network devices during the upgrade process.

In this mode, Nokia EDA does not interact with target devices, effectively pausing the cluster's interaction with your infrastructure. You can still interact with Nokia EDA and the `TopoNode` resources; changes are pushed upon switching back to `normal` mode.

To set `emulate` mode in bulk, run the script from the [playground](https://github.com/nokia-eda/playground) repo directory on a machine where you have [`kubectl`](../../user-guide/command-line-tools.md#kubectl) configured with the access to your cluster:

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

## Backing up a cluster

/// admonition | Backup role
    type: info
The cluster backup file is not going to be used in the in-place EDA upgrade procedure as the Git repositories remain intact in the existing cluster. However, Nokia recommends that you take a backup of your cluster regardless.  
The backup file can be used to restore your cluster to a previous state in case you would want to deploy a new EDA cluster from scratch.
///

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

This will create a timestamped backup archive and put it in the `/tmp/eda-support/logs-<date>` directory on your system. The backup archive contains all the necessary information to restore your cluster.

/// warning | Testing the backup
Nokia highly recommends that you test the backup by restoring it in a test cluster before proceeding with the upgrade of your production cluster.
///

## Updating the Playground repository

The workflow to upgrade Nokia EDA slightly differs depending on whether you have the original [playground repository][playground] present in a system that you used to install Nokia EDA originally from or not.

[playground]: ../preparing-for-installation.md#download-the-nokia-eda-installation-playground

/// tab | Playground repository present

If you have an existing [playground repository][playground], ensure it is up to date by running:

```bash
git pull --rebase --autostash -v
```

This will update the playground repository while keeping any customizations you may have done to the `prefs.mk` file.

//// details | Resolving merge conflicts
The pull operation may result in a merge conflict if your customizations clash with the new changes in the `prefs.mk` file. For example, you may see the following prompt:

```text
Applying autostash resulted in conflicts.
Your changes are safe in the stash.
You can run "git stash pop" or "git stash drop" at any time.
```

And then the `prefs.mk` file will contain the merge conflict markers. For example:

```makefile hl_lines="1 16 41" title="conflict markers highlighted"
<<<<<< Updated upstream
# Option 2: If bringing your own Registry, Git or Artifacts hosting
#           for anything not being used from the unified asset-host
#           define the endpoints as:
# ASSET_HOST_REGISTRY := registry.bastion.corp.com
# ASSET_HOST_GIT := https://git.bastion.corp.com
# ASSET_HOST_ARTIFACTS := https://artifact.bastion.corp.com

# Specify auth as base64 encoded values
# B64_ASSET_HOST_GIT_USERNAME := ""
# B64_ASSET_HOST_GIT_PASSWORD := ""
# B64_ASSET_HOST_ARTIFACTS_USERNAME := ""
# B64_ASSET_HOST_ARTIFACTS_PASSWORD := ""
# B64_ASSET_HOST_REGISTRY_USERNAME := ""
# B64_ASSET_HOST_REGISTRY_PASSWORD := ""
=======
# Specify auth
# ASSET_HOST_GIT_USERNAME := ""
# ASSET_HOST_GIT_PASSWORD := ""
# ASSET_HOST_ARTIFACTS_USERNAME := ""
# ASSET_HOST_ARTIFACTS_PASSWORD := ""
NO_KIND := yes

# Specify auth
USE_ASSET_HOST := 1
ASSET_HOST := 10.0.0.30
ASSET_HOST_GIT_USERNAME := eda
ASSET_HOST_GIT_PASSWORD := eda
ASSET_HOST_ARTIFACTS_USERNAME := eda
ASSET_HOST_ARTIFACTS_PASSWORD := eda


METALLB_VIP = 10.0.0.25/32
EXT_DOMAIN_NAME = 10.0.0.25
EXT_HTTPS_PORT = 443
SINGLESTACK_SVCS = false

EDA_CORE_VERSION=25.12.4
EDA_APPS_VERSION=25.12.4

>>>>>> Stashed changes
```

The [merge conflict](https://docs.github.com/articles/resolving-a-merge-conflict-using-the-command-line) markers indicate the lines that have been changed both in the upstream repository from where you pulled the latest playground (marked with `<<<<<< Updated upstream`) and in your local repository where you have your customizations (marked with `>>>>>> Stashed changes`).

In this instance, the changes upstream introduced the new variables for the Asset Host credential configuration (prefixed with `B64_`). You can resolve this conflict by editing the `prefs.mk` and making the following changes:

1. Replacing the old credentials-related variables with the new ones.
2. Removing the merge conflict markers from the file.

After aligning the changes, the portion of the file where the conflict occurred may look like this:

```makefile
# Option 2: If bringing your own Registry, Git or Artifacts hosting
#           for anything not being used from the unified asset-host
#           define the endpoints as:
# ASSET_HOST_REGISTRY := registry.bastion.corp.com
# ASSET_HOST_GIT := https://git.bastion.corp.com
# ASSET_HOST_ARTIFACTS := https://artifact.bastion.corp.com

# Specify auth as base64 encoded values
B64_ASSET_HOST_GIT_USERNAME := ZWRh
B64_ASSET_HOST_GIT_PASSWORD := ZWRh
B64_ASSET_HOST_ARTIFACTS_USERNAME := ZWRh
B64_ASSET_HOST_ARTIFACTS_PASSWORD := ZWRh
# B64_ASSET_HOST_REGISTRY_USERNAME := ""
# B64_ASSET_HOST_REGISTRY_PASSWORD := ""

NO_KIND := yes

# Specify auth
USE_ASSET_HOST := 1
ASSET_HOST := 10.0.0.30

METALLB_VIP = 10.0.0.25/32
EXT_DOMAIN_NAME = 10.0.0.25
EXT_HTTPS_PORT = 443
SINGLESTACK_SVCS = false

EDA_CORE_VERSION=25.12.4
EDA_APPS_VERSION=25.12.4
```

After aligning the changes, save and commit the changes to your local repository.

```bash
git add prefs.mk
git commit -m "Resolve merge conflict in prefs.mk"
```

////

///

/// tab | Playground repository missing
If the original playground repository is missing, you should clone the repository again:

```bash
git clone https://github.com/nokia-eda/playground && \
cd playground && \
make download-tools
```

Identify what Nokia EDA version you are running using [edactl](../../user-guide/command-line-tools.md#edactl):

```bash
edactl cluster
```

<div class="embed-result">
```{.shell .no-select .no-copy}
Name           Address  ActivityState  BuildVersion                  CoreVersion  AvgLatency(ms)  Reachable  Synchronized
 engine-config  self     Active         v25.4.1-2504252348-g720b7d2e  v2.0.0-0                     true       true
```
</div>

In this example, the cluster reports Nokia EDA version `25.4.1`.

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

## Uninstalling Nokia EDA components

The existing EDA core components must be uninstalled before installing the new version.

### Breaking redundancy (geo-redundant clusters) <small>(optional)</small>

If you have a geo-redundant installation, on your active cluster member, update your `EngineConfig` to remove the `.spec.cluster.redundant` section. This breaks redundancy and allows you to upgrade the active member without affecting the standby member.

/// admonition | Changes on standby members
    type: subtle-note
Do not update the EngineConfig resource on standby members. Although stopped, if the standby members were to start, they must continue to look for the active member (and fail to do so) throughout the upgrade.
///

### Stopping Nokia the EDA platform

To stop Nokia EDA components, enter the following command:

```{.shell .no-select}
make eda-stop-core
```

This command returns no output but stops all pods that are packaged as part of `eda-kpt-base` and removes them from the cluster.

/// details | Nuances for geo-redundant clusters
    type: info
For geo-redundant clusters, execute the `edactl platform stop` command on both active and standby members, via their respective `eda-toolbox` pods.
///

### Uninstalling Nokia EDA core components

Proceed with uninstalling Nokia EDA core components:

```bash
make eda-uninstall-core
```

Confirm that core components deployed from `eda-kpt` are removed. List pods with the following command[^1]:

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

### Stopping Nokia EDA git servers

Continue with stopping Nokia EDA Git servers by scaling down the Nokia EDA Git deployments:

```{.shell .no-select}
make scale-down-git-servers
```

### Version-specific steps

When upgrading from versions older than 25.12.1, stop the fluentd daemonset:

```bash
make uninstall-external-package-fluentd
```

## Updating Nokia EDA kpt packages

Set the desired Nokia EDA version in the `prefs.mk` file to match the target version you want to upgrade to. For example, to choose the -{{eda_version}}- version:

```text
EDA_CORE_VERSION=-{{eda_version}}-
EDA_APPS_VERSION=-{{eda_version}}-
```

Download the tools and packages by executing the following command:

```shell
make download-tools download-pkgs
```

### Customizing kpt packages

If you started with a freshly cloned repository, you want to add customizations to your EDA installation by setting the variables in the `prefs.mk` file; this process is explained in detail at the [installation phase](../deploying-eda/installing-the-eda-application.md#customizing-the-installation).

> At a minimum, ensure `EXT_DOMAIN_NAME` and `EXT_HTTPS_PORT` are set correctly in your `prefs.mk` file.

Configure the packages downloaded for the target EDA version with the customizations you added to the `prefs.mk` file:

```{.shell .no-select}
make eda-configure-core
```

## Installing the new version of Nokia EDA

Install the new version of Nokia EDA core components by running:

```{.shell .no-select}
make install-external-packages eda-install-core eda-is-core-ready
```

## Upgrading your applications

After installing the new Nokia EDA core in the step above, you need to upgrade Nokia EDA applications as they are kept on their previous versions and may be incompatible with the new version of Nokia EDA core. Use the following command to install applications compatible with the new Nokia EDA core:

```{.shell .no-select}
make eda-install-apps eda-install-proxies
```

## Resuming NPP interactions

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

## Restoring a backup in a new cluster

/// admonition | Optional step
    type: subtle-note
This procedure applies only if you are deploying a new Nokia EDA cluster from scratch either by deploying a new set of VMs or by re-creating the Kubernetes cluster. It does not apply for in-place upgrades.
///

Copy the [collected backup file](#backing-up-a-cluster) from your machine back into the `eda-toolbox` pod of the new cluster:

```{.shell .no-select}
backupfile=/tmp/eda-support/logs-2025-12-18/eda-platform-backup-2025-12-18-21-37-42.tar.gz

toolboxpod=$(kubectl -n eda-system get pods \
-l eda.nokia.com/app=eda-toolbox -o jsonpath="{.items[0].metadata.name}")

kubectl -n eda-system cp $backupfile \
  $toolboxpod:/tmp/eda-backup.tar.gz
```

Restore your cluster to its previous state by running the following command:

```{.shell .no-select}
edactl platform restore /tmp/eda-backup.tar.gz
```

[^1]: Replace with your base namespace if you modified it.
