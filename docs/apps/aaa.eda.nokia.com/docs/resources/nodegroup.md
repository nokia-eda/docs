---
resource_name: NodeGroup
resource_name_plural: nodegroups
resource_name_plural_title: Node Groups
resource_name_acronym: NG
crd_path: docs/apps/aaa.eda.nokia.com/crds/aaa.eda.nokia.com_nodegroups.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Node Group

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `NodeGroup` defines what a user can or cannot do. It is a set of rules for all users that belong to the `NodeGroup`, where each rule consists of a state path or command and an action.

!!! warning "Rule ordering"

    The **order** in which the rules appear may matter, depending on the operating system. For SR Linux, longest path match decides on the action that is taken, while SR OS is strictly numbered, meaning it will execute the action of the first rule that matches.

Each rule in the list matches a particular operating system. If the deploy target of the `NodeGroup` does not match the operating system of that rule, the rule will not be configured on the node. The syntax of the rule should match the target operating system. On which nodes a `NodeGroup` is deployed is determined by [AuthenticationPolicy](authenticationpolicy.md) and [ServerGroup](servergroup.md) resources or by `NodeUser` group bindings.

!!! info "State paths vs commands"

    Rules are either command-based or path-based. **Commands** match what the user types in the CLI, while **paths** match the underlying state information that the command accesses. The behavior and syntax of the rules depend on the operating system that the rule targets. A practical example comparing SR OS and SR Linux is provided below.

### SR OS vs SR Linux: an example

/// tab | SR OS (command-based)

SR OS does authorization through configuration profiles, where each rule matches a specific **command**. The example below allows users assigned to this group to access the interface if-1/1/c1/1, but no others.

```yaml
apiVersion: aaa.eda.nokia.com/v1alpha1
kind: NodeGroup
metadata:
  name: my-sros-node-group
  namespace: eda
spec:
  rules:
    - action: Read
      match: configure router Base interface if-1/1/c1/1-1
      operatingSystem: sros
    - action: Deny
      match: configure router Base interface
      operatingSystem: sros
  services:
    - CLI
  superuser: false
```

Example execution (both interfaces exist)

```
[gl:/configure]
A:operator@leaf-2# info router interface "if-1/1/c1/1-1"
    admin-state enable
    port 1/1/c1/1:1
<...snipped...>

[gl:/configure]
A:operator@leaf-2# info router interface "if-1/1/c1/2-1"

[gl:/configure]
A:operator@leaf-2#

[gl:/configure]
A:operator@leaf-2# /show router interface
MINOR: MGMT_CORE #2020: Permission denied - unauthorized use of 'interface'
```

///
/// tab | SR Linux (path-based)

SR Linux does authorization through configuration roles, where each rule matches a state path. The example below allows users assigned to this group to access the interface ethernet-1/1, but no others.

```yaml
apiVersion: aaa.eda.nokia.com/v1alpha1
kind: NodeGroup
metadata:
  name: my-srl-node-group
  namespace: eda
spec:
  rules:
    - action: Read
      match: interface ethernet-1/1
      operatingSystem: srl
    - action: Deny
      match: interface *
      operatingSystem: srl
  services:
    - CLI
  superuser: false
```

Example execution (both interfaces exist)

```
--{ + running }--[  ]--
A:operator@leaf-1# info / interface ethernet-1/1
    admin-state enable
    vlan-tagging true
    subinterface 1 {
        admin-state enable
<...snipped...>

--{ + running }--[  ]--
A:operator@leaf-1# info / interface ethernet-1/2

--{ + running }--[  ]--
A:operator@leaf-1# /show interface brief | as json
{
  "IfBrief": [
    {
      "Port": "ethernet-1/1",
      "Admin State": "enable",
      "Oper State": "up",
      "Speed": "100G"
    }
  ]
}
```

///

## Referenced resources

No resource types are referenced during the creation of a `NodeGroup`. A `NodeGroup` may be referenced by [ServerGroup](servergroup.md) resources (via `nodeGroupSelectors` or `nodeGroups`) to indicate that the group should be deployed on the same nodes where that [`ServerGroup`](servergroup.md) is used for authentication.

## Examples

/// tab | YAML

```yaml
-{{ include_snippet(resource_name) }}-
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
-{{ include_snippet(resource_name) }}-
EOF
```

///

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
