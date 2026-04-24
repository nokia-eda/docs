# Image management

The `Image` resource is the workflow that is used to change image of the operating system on nodes, via an upgrade or downgrade. For more information about workflows, see [Workflows](../workflows.md).

You can use the `Image` workflow to perform the following tasks:

- Reimage a single node, a list of nodes by name, a set of nodes using a label selector, or tranches of nodes, including support for canaries
- Perform a configurable set of pre and post checks to verify:
    - that all interfaces are up \(with an option to use a label selector\)
    - that all default BGP peers are up
    - reachability on ISLs
    - reachability between system addresses

In the `Image` resource, provide the input for the following fields:

- `Type`: the type of workflow. Set to `node`, `nodeselector`, or `tranche`
- `nodeProfile`: set to the destination `NodeProfile` resource.
- `version`: set to the destination version in the `NodeProfile` resource.

The following settings are optional:

- `prompt`: specifies when the workflow prompts an operator to continue. Set to `AfterPreChecks` or `AfterPostChecks`. These options can force a prompt even when checks pass.
- `checks`: a container that includes options for pre and post checks. You can set the following options:
    - `skip`: indicates that checks should be skipped \(not run\).
    - `force`: indicates that checks should be run without prompts, even if checks fail.
    - `checks`: lists the checks to run. If not provided, all checks are run. Valid checks are `Interface`, `DefaultBGP`, `PingISL`, and `PingSystem`.

## Requirements for re-imaging nodes

Before running an image workflow, ensure that deviations in the system, if any, have all been accepted or rejected.

Ensure that node groups and node users have the necessary privileges to perform the operations. For example, the GNOI/GNSI privilege is required to execute operational commands such as reboot.

## Re-imaging failure

If re-imaging fails, the workflow terminates with the appropriate reason. Operators are responsible for cleaning up any configuration created by the workflow, including the following recovery steps:

- Cleaning up drain policies created by the workflow.
- Removing any configlets created by the workflow.
- Reverting the node profile and setting the NPP mode if necessary.

Operators can attempt re-imaging by creating a new workflow.

## Reimaging individual nodes <span id="reimage-individual-nodes"></span>

You can reimage individual nodes using the `Image` workflow or using the `edactl` tool.

### Workflow resource for re-imaging specific nodes

To reimage individual nodes using the `Image` workflow, provide the following input:

- `nodes`: set to the name of the `TopoNodes` to be reimaged
- `nodeProfile`: set the Node Profile which contains the software image to use

```
apiVersion: os.eda.nokia.com/v1alpha1
kind: DeployImage
metadata:
  namespace: eda
  name: upgrade-leaf1
spec:
  nodes:
    - leaf-1
  nodeProfile: srlinux-25.7.1
```

## Reimaging nodes using labels <span id="reimage-nodes-using-labels"></span>

You can reimage nodes using the `Image` workflow and applying labels to select TopoNodes or using the `edactl` tool.

### Workflow resource for re-imaging nodes using a label selector

To reimage a set of nodes using a label selector, provide the following input:

- `nodeSelectors`: provide a list of label selectors to select `TopoNodes`.
- `nodeProfile`: set the node profile which contains the software image to use

```
apiVersion: os.eda.nokia.com/v1alpha1
kind: DeployImage
metadata:
  namespace: eda
  name: upgrade-rack1
spec:
  nodeSelectors:
    - eda.nokia.com/redundancy-group=rack1
  nodeProfile: srlinux-25.7.1
```

### Using the edactl tool with a GVK workflow definition

```
edactl workflow run operatingsystem-image-gvk workflow-fabric-upgrade-bylabel --bg -n eda type nodeselector nodeSelector[i] 0:maintenancenodes=fabric1 nodeProfile srlinux-24.10.3-201 version 24.10.3 checks.skip true drains.skip true
```

## Reimaging node tranches <span id="tranches"></span>

To reimage sets of groups of nodes with an ordered list of label selectors, provide the following input:

- `tranches`: set to a list of `nodeSelector`, nesting the node selector type
- `canaries`: optionally used with tranches; specify as a pre-tranche to be reimaged before all others
- `nodeProfile`: set to the node `nodeProfile` resource that contains the software image to use

Imaging proceeds as follows:
/// html | div.steps

1. Canaries are imaged first, executing any pre and post checks along with any waits. Assuming these operations succeed, the workflow continues.
2. The tranche with index 0 is imaged next, following the same run-to-completion workflow.
3. The tranche with the next index is imaged next; this step repeats until all tranches have been upgraded.

///

### Workflow resource for re-imaging tranches of nodes

```
apiVersion: os.eda.nokia.com/v1alpha1
kind: DeployImage
metadata:
  namespace: eda
  name: upgrade-tranches
spec:
  tranches:
    - name: tranche1
      nodeSelectors:
        - eda.nokia.com/redundancy-group=rack1
    - name: tranche2
      nodeSelectors:
        - eda.nokia.com/redundancy-group=rack2
  nodeProfile: srlinux-25.7.1
```

## Node imaging checks <span id="node-imaging-checks"></span>

The `Image` workflow supports the following checks during node imaging:

- Verifying that interlink switch interfaces are operational. This check gets any `Interface` resource with the label `eda.nokia.com/role=interSwitch` where the current node is a member. The list of up interfaces is stored for comparison later.
- Verifying that BGP peers are up in the default network instance. As with interfaces, the list of up default BGP peers is stored for comparison later.
- Verifying connectivity on every ISL. This check triggers the ping workflow to run, passing in `isl` as the `pingType`.

- Verifying connectivity between all system addresses of nodes. This triggers the ping workflow to run, passing in `system` as the `pingType`.

These checks are executed before an upgrade batch takes place, and after the upgrade batch completes. If any check fails, the administrator is prompted to continue, but only after completing the execution of each test. If an operator rejects continuing in post checks, the image reverts to its previous version.
