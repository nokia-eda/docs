# Branches

Nokia Event-Driven Automation (EDA) supports the use of branches, which allow you to configure changes on a sandboxed EDA instance that you plan to merge later into the main EDA cluster.

In EDA, a "branch" is an EDA deployment that is a twin of the main, production EDA cluster.

There are two major types of branches:

- Local branches: these are branches running on the same Kubernetes cluster as the main EDA instance. These are always [vCluster][vcluster-repo] branches.

- Remote branches: these are branches running on remote Kubernetes clusters.

There is no limit to the number of remote or local branches you can create, however you are limited by the CPU and memory resources available in the cluster(s) hosting the branches.

## Branching concepts

To support branching, EDA provides the following capabilities:

- The managed spinning up and tearing down virtual clusters in the current EDA instance (local branches), where these virtual clusters operate functionally as branches. The clusters are populated with the same git repository content that is present in main. When using local branches, EDA selects individual Kubernetes workers that are only used for branches. This removes any possible contention between the main EDA instance and any locally running branches.

- The managed spinning up and tearing down of virtual clusters in a remote Kubernetes cluster where no EDA instance is present; these are remote branches. It can be useful to maintain a branch in the cloud to validate complex or large scale changes in EDA resources, and then remove the branch after validation is complete.

- The ability to tunnel traffic to and from remote branches. Branches can run in remote infrastructure that has no connectivity back to the main instance; EDA forwards operations across the open connection. Branches can operate in the public cloud, even when the main instance is behind a firewall, assuming the main instance is allowed to reach the remote Kubernetes cluster. This also puts the burden of connection on the main instance, providing better access controls. When a branch is removed, the connection from the main instance is also removed.

- Port forwarding for local branches. EDA exposes the EDA API server, Kubernetes API server, and the gRPC port of N branches on a single IP.

- Rebasing a branch. EDA can rebase a branch cluster to main, updating the branch cluster's main branch with to match the content of main on he live instance. EDA then reapplies any changes that had been made in the branch. This can trigger a three-way-merge to resolve any conflicts, if necessary.

- Resetting a branch. EDA can reset a branch cluster to main, effectively discarding any changes in the branch cluster and updating it to be aligned with main.

- Merge requests. EDA allows you to trigger a merge request from the branch, to merge any changes made in the branch with the main branch.

## Creating branches

Creating a branch is as simple as creating a `Branch` resource, which triggers two following operations:

- Creating the EDA cluster in which the branch will run.

- Creating the link between the branch and the main EDA instance.

### Creating branch environments

To support creating the environment to run branches, EDA introduces a new `ClusterProvider` resource alongside a new `Branch` resource, where a `ClusterProvider` describes the environment in which the branches are created, and the mechanism to reach that environment.

A `ClusterProvider` consists of:

- A `kubeconfigSecret`, which is a Kubernetes Secret that stores a Kubeconfig that can be used to reach the environment.

    The ClusterAPI in Kubernetes (which abstracts the creation/lifecycle of a Kubernetes cluster) generates a Secret that EDA uses to reach the cluster. This does not preclude you from creating your own arbitrary Kubeconfigs that allow EDA to use any Kubernetes cluster as a host for branches.

- The `noVirtualCluster` boolean, which allows a single Kubernetes cluster to be used without vCluster. If set to false, EDA uses vClusters as the default option. If set to true, only a single branch can operate using this provider.

- An `address`, which is the address that branches are exposed on. This defaults to the address used to reach the cluster (the EDA API server).

- A `startPortRange`, which is the initial port used to forward to the Kubernetes and EDA API servers, as well as the gRPC proxy in instances of branches.

A `ClusterProvider` is optional; you can choose to use only local branches.

/// details | Generating Kubernetes clusters to run branches
    type: info
The `ClusterProvider` is intended to be used alongside the `ClusterAPI` resource in Kubernetes, which upon creation will create a `Secret` resource with the Kubeconfig that EDA needs to reach the cluster. The `ClusterAPI` provides support for many different cloud providers, as well as on-premises solutions, and even kind clusters. This allows you to create branches in a wide variety of environments, and have EDA manage the lifecycle of these environments for you. See the [ClusterAPI documentation](https://cluster-api.sigs.k8s.io/) for more information around supported providers and usage.
///

### Creating branches

Whether using a `ClusterProvider` or not, you can use the `Branch` resource to create branches. These are normal resources exposed through all interfaces, and are included in transactions.

For example the following resource creates a local branch:

```yaml
apiVersion: core.eda.nokia.com/v1
kind: Branch
metadata:
  namespace: eda-system
  name: blue
spec:
```

The following resource creates a remote branch:

```yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterProvider
metadata:
  namespace: eda-system
  name: remote-cluster-south
spec:
  kubeconfigSecret: kubeconfig-secret-kind-south
  noVirtualCluster: false
  address: user.com
  startPortRange: 9400
---
apiVersion: core.eda.nokia.com/v1
kind: Branch
metadata:
  namespace: eda-system
  name: red
spec:
  clusterProvider: remote-cluster-south
```

The following resource creates a remote branch with no vCluster:

```yaml
apiVersion: core.eda.nokia.com/v1
kind: ClusterProvider
metadata:
  namespace: eda-system
  name: remote-cluster-south-bare
spec:
  kubeconfigSecret: kubeconfig-secret-kind-south
  noVirtualCluster: true
  address: user.com
  startPortRange: 9300
---
apiVersion: core.eda.nokia.com/v1
kind: Branch
metadata:
  namespace: eda-system
  name: red
spec:
  clusterProvider: remote-cluster-south-bare
```

A branch with no vCluster can only run a single instance per Kubernetes, since there is no virtualization to allow multiple instances of EDA to run. This is an atypical setup but allows using branches without virtualization if necessary. The recommendation is to use vCluster for branches.

### Branch placement

Branches should not interfere with the main branch instance even if they are part of the same EDA cluster, as long as the cluster has been dimensioned correctly. For all clusters, EDA also adds additional affinity rules to the pods belonging to the branch to ensure they can be grouped together on the same and/or dedicated nodes.

```yaml title="Affinity rules set on the pods belonging to the branch"
affinity:
  nodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      preference:
        matchExpressions:
        - key: eda.nokia.com/branch
          operator: In
          values:
          - blue #(1)!
    - weight: 100
      preference:
        matchExpressions:
        - key: eda.nokia.com/branch
          operator: Exists
```

1. The value of the `branch` label is the name of the branch.

You should label worker nodes you wish to use with branches with at minimum the `eda.nokia.com/branch` label, and EDA will use these nodes to run branches. If you do not label any nodes with the `eda.nokia.com/branch` label, EDA will run branches on any available node in the cluster, which can lead to resource contention between the main instance and branches. If you wish to run specific named branches on specific workers you may use the `eda.nokia.com/branch` label with the name of the branch as the value, and EDA will use nodes with that label to run the branch with the corresponding name.

Worker nodes can be labeled via `kubectl`:

```bash
kubectl label nodes <node-name> eda.nokia.com/branch=blue
```

### vCluster Plugin

When used with the EDA `vCluster` plugin, `vCluster` supports `cert-manager` to maintain trust and authentication in the cluster.

The vCluster plugin mirrors the cert-manager resources of `Certificate`, `CertificateRequest`, `Issuer` to the host `vCluster` namespace and relies on the host `cert-manager`.

Each pod has `CSI` driver options re-written to use name synced to host. The host `cert-manager` than issues certificates to the pods based on reflected resources.

A local version of `trust-manager` is installed to provide `Bundle` resource capabilities. It is not possible to use the host `trust-manager`, since it only reads `Configmaps` and `Secrets` from system namespace and does not want to pollute system namespace with branch resources.

`SharedIpService` resources are reflected back to the host to enable sharing of a single IP address across multiple branches.

### Branch synchronization

The main use case for branches it to stage changes to later be merged into main. So, synchronization is key. Unlike the conventional branches used for EDA merge requests, from a git perspective branch clusters behave as forks on main. This allows the branches to synchronize changes without modifying the main git repo.

### Access control in branches

Each branch cluster has its own API server and EDA UI, but the authentication provider (Keycloak) is shared between clusters. The access token granted when logging into the main EDA UI is valid for the branched cluster, allowing you to switch between clusters without re-authentication.

In the branch cluster, the user is allowed to commit resource changes for which they have `readPropose` permission on main. This means you can use branches to test changes that you are not permitted to commit directly in main and, when satisfied, propose your changes as a merge request in main.

/// admonition | Note
Users, user groups, and role assignments are stored in Keycloak and therefore synchronized automatically between main and branches.

However, the Cluster Roles and Roles themselves are resources local to the branch. When modifying a Cluster Role or Role on main, the branch will not apply these changes until the branch is rebased or restored from main.
///

## Branches in the EDA UI

The main EDA UI allows you to:

- create branches
- navigate to a branch cluster

If at least one branch exists, EDA displays a branch indicator and selector at the top of the page. When you are in the main branch, you can use the selector to switch to a different branch.

-{{image(url="graphics/sc0468.png", title="The Branch Selector", shadow=true, padding=20, scale=0.7)}}-

From a branch cluster UI, you can use the same selector:

- navigate to a the main cluster
- see **diffs** to identify differences between the current branch and main
- **restore** the branch from main. This removes all branch changes and applies the latest configuration from main
- **rebase** the branch from main. This stashes the branch changes as a merge request in the branch cluster, and applies the latest configuration from main
- Create a **merge request** on the main cluster containing the changes from the branch

-{{image(url="graphics/sc0467.png", title="Actions for a branch", shadow=true, padding=20, scale=0.7)}}-

When you are in a branch that is not main, the branch selector is shaded with color as as reminder that you are not in main.

Also, when you are in a branch that is not main, the Branch UI does not show the App management, User management, or Branches CR under Platform.

### Creating a branch

Follow these steps to create a new branch.

/// admonition | Note
    type: subtle-note
You must be in main cluster UI to create new branches. You can not create a new branch from a branch cluster UI.
///

/// html | div.steps

1. In the **System Administration** menu, select **Branches**.

1. Click **Create** at the top of the **Branches** page.

1. On the **Create Branch** page, enter a **Name** and, optionally, **Labels**, and **Annotations** for this branch.

1. If this is a remote branch, enter the name of a `ClusterProvider`.

1. Click **Commit** to immediately apply the changes or click **Add To Basket** to store these changes to be processed later as part of a transaction. Alternatively, select **Dry Run** to test your changes immediately, and reveal any issues before proceeding.

After you create at least one branch, the **Branch Selector** control displays at the top of the EDA UI.

///

### Managing a branch

When you have a branch open other than main, follow these steps to perform actions on that branch.

/// html | div.steps

1. In the **System Administration** menu, select **Branches**.

1. Click the **Branch Selector** and select your branch from the displayed list.

    EDA opens a new browser tab; in that tab, the UI switches to the selected branch. If you switched to a branch that is not main, the **Branch Selector** adopts color shading as an indicator that you are not in main.

1. Choose one of the following:

    - To update your branch with changes made to main since you first created the branch (or since your last rebase), go to step 4.
    - To update your branch to match the current state of main, go to step 5.
    - To view the differences between your current branch and main, go to step 6.
    - To create a merge request that will merge the changes in your current branch into main, go to step 7.

1. <span id="mbr-step-4"></span>To rebase your branch, do the following:

      1. Click the **Branch Selector** and select **Rebase** from the
      1. Click **OK** in the resulting confirmation dialog.

        EDA updates the current branch with changes that have been made on main since this branch was created, or since it was last rebased. The **Transactions** page displays, and the list includes the transaction used to rebase your branch and its status. Double-click the transaction row to see details about its execution.

        A rebase operation results in any changes in your branch being populated into a merge request in the branch cluster, which must be manually merged in the branch cluster before the rebase can complete. This allows you to resolve any conflicts that may arise during the rebase, and also gives you visibility into what changes from your branch are being reapplied after the rebase.

1. <span id="mbr-step-5"></span>To restore your branch, do the following:

      1. Click the **Branch Selector** and select **Restore** from the action list.
      1. Click **OK** in the resulting confirmation dialog.

        EDA updates the current branch to match the current state of main. The **Transactions** page displays, and the list includes the transaction used to rebase your branch and its status. Double-click the transaction row to see details about its execution.

1. <span id="mbr-step-6"></span>To view differences between your current branch and main, do the following:

      1. Click the **Branch Selector** and select **Diffs** from the action list.

        EDA displays a **Branch Diffs** view for your branch, showing where its resource configurations differ from those on main.  

      1. Optionally toggle between side-by-side and inline view using the buttons at the top right of the view.

      1. Click Close to return to close the **Branch Diffs** view.

        /// admonition | Note
            type: subtle-note
        Branch diffs are not removed from the branch until you perform a rebase on the branch.
        ///

1. <span id="mbranch-step-7"></span>To create a merge request to merge your branch into main do the following:

      1. Click the **Branch Selector** and select **Merge to Main** from the displayed list.

      2. The Create Merge Request dialog displays.  

      3. Enter a commit message for the transaction in the dialog and click **Create**.

        EDA creates a new merge request for this transaction. A new tab opens showing the Merge Requests details page in the main branch.

        From here, depending on the state of the merge request, you might be able to proceed immediately with the merge; or you might need to resolve merge conflicts before proceeding. For information about working with merge requests in EDA, see [Merge requests](../user-guide/merge-requests.md).

///

## Branches in edactl

`edactl` allows you to:

- create branches, using typical `edactl apply` (and related) commands with `Branch` resources
- list resources changed in a branch with `edactl branch changed-resources`
- trigger a merge request to main with `edactl branch merge`
- trigger a rebase of the branch with `edactl branch rebase`
- trigger a restore of the branch with `edactl branch restore`

To access `edactl` commands for branches, you must be targeting the branch cluster. The simplest way to do this is to access the `eda-toolbox` pod in the branch cluster and run `edactl` commands from there. You can also set up port forwarding to the branch cluster API server and use `edactl` from your local machine, or you can install `edactl` directly on your machine and configure it to reach the branch cluster API server.

/// admonition | Note
To generate an `EDACONFIG` to interact with a branch you may use `edactl config generate` as per normal, with your current Kubernetes context set to the branch cluster. This will generate an `EDACONFIG` with the correct API server address and credentials to interact with the branch cluster. If the branch cluster is exposed using a different address, you may need to use the `--address` flag to specify the correct address for the API server.
///

## Branches in "Try EDA"

Even the KinD-based [Try EDA](../getting-started/try-eda.md) environment supports locally-spawned branches. The KinD Kubernetes cluster is capable of hosting a nested vCluster-powered branch environment for demonstration and development purposes. The following considerations apply:

- `EXT_DOMAIN_NAME` should be set to a valid domain or IP address as this will be used to configure the proxy to the branch cluster.
- upon branch creation, the `make expose-try-eda-branch BRANCH_NAME=<branch-name>` target must be run to enable UI/API access to the branch cluster.  
    This target needs to be called only once per the named branch.
- Up to three branches are supported in the "Try EDA" environment.

[vcluster-repo]: https://github.com/loft-sh/vcluster
