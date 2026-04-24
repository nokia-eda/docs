# Redundancy

As part of critical infrastructure, EDA must be resilient in case of outages to continue to support the infrastructure. Outages can be caused by power outages, network outages, storage outages, or any other dependent infrastructure outages and EDA must be able to mitigate the loss of visibility and automation during these events. Outages can also impact the connectivity between members of an EDA cluster; in these cases, EDA needs to avoid split brain scenarios.

EDA provides resiliency via redundancy, using the following strategies:

- Localized restartability: assuming any application can fail at any time, and the system must reconcile. EDA takes this approach and is relevant for services like ConfigEngine. In general, any service should be able to restart and the system should converge back to a golden state. When any EDA pod fails, either Kubernetes or ConfigEngine should restart it.
- Localized redundancy and microservices: multiple instances of a common service with load balancing. This strategy limits localized outages, and in most cases, only inflight requests are lost.
- Remote redundancy: multiple clusters \(or cluster members depending on hierarchy\). Typically referred to as geo-redundancy, where one or more cluster members are present and each one can operate the full load of management activities, with only one active at a time. In EDA, pushes to redundant sites are not synchronous as long as changes are persisted in the majority of configured Git servers. This does mean some inflight changes could be lost during a switchover.

## Local redundancy

EDA supports automatic recovery of local services in the event of a failure. EDA leverages Kubernetes for deployment of its core services, which provides out-of-the-box redundancy when more than one worker node is available, with EDA services able to be scheduled or rescheduled to remaining available nodes during failures.

## Cluster recovery

EDA supports cluster recovery by allowing the bootstrapping of a cluster from any member. This process removes all members, starts the active member, and then adds members back.

## Remote redundancy

Remote redundancy is accomplished by configuring a set of members within the `EngineConfig` resource in the `.spec.cluster.redundancy.members` context.

Synchronization occurs when changes are pushed to the set of Git servers for backup.

## Alarms

Support for the following alarms, generated only on the active cluster:

- When there is failure to reach any member of the redundancy cluster
- When latency to a member is above a specified threshold
- Any core-generated alarms from any standby member

    These alarms are forwarded to the active member for the active to display, with the node set to the name of the member that raised it.

## Geo-redundancy (remote redundancy) <span id="geo-redundancy"></span>

EDA supports two concepts of remote redundancy that can be used together or separately:

Git redundancy
:   EDA supports remote redundancy through the backup of configuration information and data to a set of Git servers and restoring backed up data from the same set of Git servers.

    The Git servers are defined in the `.spec.git.servers` context of the `EngineConfig` CR. Whenever a change occurs in the system, the active ConfigEngine asynchronously pushes changes to all Git servers, and from there, any other ConfigEngine can start with the same content via the same Git servers.

Cluster redundancy
:   In a true geo-redundant environment, multiple EDA deployments are running in different locations, where one deployment is designated the active, and the other deployment is designated as standby. Both deployments must have the same Git servers configured so they have access to the same data.

    An operator must define the members of a geo-redundant cluster, where each member is a standalone EDA deployment configured to be part of a cluster. It takes two members to form a cluster, with manual intervention currently required for switchovers to occur. For details, see [Switching the active deployment](redundancy.md#).

/// Admonition | Note
    type: subtle-note
These two concepts are distinct and can be used separately. For example, a single EDA deployment can use multiple Git servers so that data is stored redundantly across multiple Git servers. You can also deploy two EDA deployments for a redundant cluster with only a single Git server (the same one) configured for each deployment. If multiple deployments for a redundant cluster are used, the same Git servers must be configured on both deployments.
///

### Adding remotes <span id="adding-remotes"></span>

An operator can enable remote redundancy during initial installation or after installation. All cluster members must be running the same software version.

#### Initial standalone configuration

The following example shows the initial `EngineConfig` CR fields for the standalone member, `us-west-1`. This resource defines a single member cluster with two Git servers, exposed via a load balancer or directly via the address `10.0.0.1` for IPv4, or `2000::101` for IPv6, or is reachable via the domain name `cluster.eda.nokia.com` (which maps to the two IP addresses).

```
apiVersion: core.eda.nokia.com/v1
kind: EngineConfig
metadata:
  name: us-west-1
spec:
  git:
    servers:
      - name: git1
        url: https://git1.eda.nokia.com
        credential: git1-token
      - name: git2
        url: https://git2.eda.nokia.com
        credential: git2

  cluster:
    external:
      ipv4Address: 10.0.0.1
      ipv6Address: 2000::101
      domainName: cluster.eda.nokia.com
```

#### Adding another EDA instance

To grow this cluster, first, install another EDA instance into another Kubernetes cluster. The following sample `EngineConfig` CR is for the new EDA instance, `us-east-2`:

```
apiVersion: core.eda.nokia.com/v1
kind: EngineConfig
metadata:
  name: us-east-2
spec:
  git:
    servers:
      - name: git1
        url: https://git1.eda.nokia.com
        credential: git1-token
      - name: git2
        url: https://git2.eda.nokia.com
        credential: git2

  cluster:
    external:
      ipv4Address: 10.0.0.1
      ipv6Address: 2000::101
      domainName: cluster.eda.nokia.com

    redundancy:
      credential: cluster-cred
      active: us-west-1
      members:
        - name: us-west-1
          address: 10.0.0.2
          port: 55000
        - name: us-east-2
          address: 20.0.0.1
          port: 55001
```

Upon starting the `us-east-2` cluster, it attempts to connect to `us-west-1`, which is not yet currently configured as a cluster member. The attempt to join should fail, with `us-east-2` attempting to form a cluster at a back-off interval. The active cluster is then updated to:

```
apiVersion: core.eda.nokia.com/v1
kind: EngineConfig
metadata:
  name: us-west-1
spec:
  git:
    servers:
      - name: git1
        url: https://git1.eda.nokia.com
        credential: git1-token
      - name: git2
        url: https://git2.eda.nokia.com
        credential: git2
    backup:
      repo: sr/eda/backup
    userStorage:
      repo: sr/eda/user-storage
    apps:
      repo: sr/eda/apps
  cluster:
    external:
      ipv4Address: 10.0.0.1
      ipv6Address: 2000::101
      domainName: cluster.eda.nokia.com
      port: 51101
    redundancy:
      credential: cluster-cred
      active: us-west-1
      active: us-west-1
      members:
        - name: us-west-1
          address: 10.0.0.2
          port: 55000
        - name: us-east-2
          address: 20.0.0.1
          port: 55001
```

This resource describes a two-member cluster, where each member is aware of how to reach each other using the credential, address, and port provided. The address and port values can be a DNS name or IPv4/IPv6 address, and is mapped directly to the `ConfigEngine` resource in each cluster.

The `name` field in the `EngineConfig` resource differs per cluster, and should map to one of the `members` listed.

In this example, the cluster grows from 0 members to 2. Both members must specify the same member as active. In this sample configuration, the previously standalone member remains active.

### Removing remotes <span id="removing-remotes"></span>

After installation, you can decommission a remote and reinstall it or remove it entirely. You can remove a remote member even if it is unreachable. You can only remove a member that is a standby, so if you want to remove an active cluster, you should first switchover to a member that is not being removed.

The initial configuration below is for a cluster with three members.

```
apiVersion: core.eda.nokia.com/v1
kind: EngineConfig
metadata:
  name: us-west-1
spec:
  git:
    servers:
      - name: git1
        url: https://git1.eda.nokia.com
        credential: git1-token
      - name: git2
        url: https://git2.eda.nokia.com
        credential: git2
  cluster:
    external:
      ipv4Address: 10.0.0.1
      ipv6Address: 2000::101
      domainName: cluster.eda.nokia.com

    redundancy:
      credential: cluster-cred
      members:
        - name: us-west-1
          address: 10.0.0.2
          port: 55000
        - name: us-east-2
          address: 20.0.0.1
          port: 55001
        - name: us-east-3
          address: 30.0.0.1
          port: 55001
```

To update the configuration so there is only a standalone member, `us-west-1`, the following would need to occur:

/// html | div.steps

1. Make `us-west-1` the active member.
2. Remove the `us-east-3` member from `us-west-1` and `us-east-2`.
3. Uninstall `us-east-3`.
4. Remove `us-east-2` from `us-west-1`.
5. Uninstall `us-east-2`.

///

### Migrating to the new Git server in the active cluster in standalone mode <span id="migrate-new-git-server-active-cluster-standalone_mode"></span>

- Nokia recommends that you use the southbound interface for georedundancy configuration \(port 51201\).
- If the deployment has multiple active systems, that is, separate standalone systems, each system should point to a different set of Git servers.

#### Procedure

/// html | div.steps

1. Install two external Git servers.

    Create the following repos in both Git servers:

    - `/eda/customresources`
    - `/eda/apps`
    - `/eda/usersettings`
    - `/eda/credentials`
    - `/eda/identity`

2. Put the TopoNodes at the standalone cluster in emulate mode.

3. Back up the active cluster using the `edactl` command.

    For instructions, see [Creating backups](backup-and-restore.md#).

4. Stop the cluster.

    `edactl stop`

5. Update engine-config to point to the new set of Git servers.

6. Restart the cluster.

    `edactl start`

7. Restore the backup files on the new Git servers.

8. Put the TopoNodes at the standalone cluster in Normal mode.

///

### Cluster members <span id="cluster-members"></span>

The following fields in the in `EngineConfig` CR define the members of a cluster:

- In the `.spec.cluster.redundancy.members` context:
  
    - `name`: a user-friendly name for the member. This setting is validated against the name of the local `EngineConfig` resource to determine the cluster member the local ConfigEngine. This requires changes to the current `EngineConfig` name. If no members are provided, the cluster is assumed to be a single member cluster, and the name check does not occur.
    - `address`: either an IPv4 or IPv6 address, or domain name that can be resolved.

- `port`: the port on which a peer ConfigEngine (proxied through APIServer) is exposed. Both the address and port are external addresses; ports may live on a load balancer. If no value is set, port 51201 is the default value used.

For a geo-redundant deployment, the following settings apply to members of a cluster:

- The set of Git servers provided in the `.spec.git.servers` context must be identical.
- The number of replicas for the API server (`.spec.api.replicas`) and State Aggregator (`.spec.stateAggregator.replicas`) must be consistent between the clusters. This check ensures that standby clusters can take the load of the active cluster. This check occurs only initially while syncing a remote, as the values can change post run-time.
- The content of the`.spec.cluster` context must match. This includes members in `.spec.cluster.redundancy.members`, and information around external reachability of the cluster in the `.spec.cluster.external` context
- The content of `.spec.playground` and `.spec.simulate` must match.

### Modifying the cluster name <span id="modif-cluster-name"></span>

Use this procedure to change the cluster name before the cluster operates geo-redundant mode.
/// html | div.steps

1. Put the nodes in the cluster in emulate mode.

2. Stop the cluster.

3. Update the name of the resource in the `eda-kpt-base/engine-config/engineconfig.yaml` file.

4. Apply the change to the cluster.

    From the `eda-kpt-base` directory, enter the following command:

    ```
    kpt live apply
    ```

///

### Verifying the geo-redundancy state <span id="verify-geo-redundancy-state"></span>

To verify the state of the geo-redundant members of a cluster, use the EDA toolbox deployed in the EDA Kubernetes cluster to execute the following command:

```
./edactl platform
Name                 Address     Port   ActivityState  BuildVersion                  CoreVersion  AvgLatency(ms)  Reachable  Synchronized                         SyncedNpps  SyncedNodes
kube-cp-a-cluster-1  self        51201  Active         v25.8.0-2508191403-g01589f68  v3.0.0                       true       false
kube-cp-a-cluster-2  10.15.0.10  51201  Standby        v25.8.0-2508191403-g01589f68  v3.0.0       3               true       false - WaitingForGitHashFromActive  10/10       N/A
root in on eda-toolbox-6584b57449-lb59m /eda/tools
```

### Switching the active deployment <span id="switch-active-deployment"></span>

Before switching the active deployment, verify that the connectivity between the deployments is as expected. If both deployments are up and running, but there is no connectivity between them, a switchover can cause both deployments to think they are active, which can cause issues.

To switch which EDA deployment is active, open the EDA toolbox on the EDA deployment that needs to be made active and execute the following command:

```
edactl cluster take-activity <name of member to make active>
```

If the other deployment is still active and can be reached, the local deployment instructs it to go into standby mode, and make itself active.

If the other deployment is no longer available (or reachable), the local deployment assumes it to be lost and makes itself active.
