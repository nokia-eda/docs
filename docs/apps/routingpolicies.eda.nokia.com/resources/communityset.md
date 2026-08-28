---
resource_name: CommunitySet
resource_name_plural: communitysets
resource_name_plural_title: Community Sets
resource_name_acronym: CS
crd_path: docs/apps/routingpolicies.eda.nokia.com/crds/routingpolicies.eda.nokia.com_communitysets.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Community Set

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `CommunitySet` resource defines a named collection of BGP community members and/or a match expression. A `CommunitySet` can be referenced by a [routing policy](./policy.md) to:

- match a route that has none, any, or all of these communities
- add, remove, or replace communities for a route

## CommunitySet types

A `CommunitySet` can be one of four types. The type determines the configuration path where the communities are configured, which is relevant for some operating systems.

### Hybrid

| Operating System | Configuration path |
| ---------------- | --------------------------------------------------------------- |
| SR Linux         | `.routing-policy.community-set`                                 |
| SR OS            | `.configure.policy-options.community`                           |
| EOS              | `.routing-policy.defined-sets.bgp-defined-sets.community-sets`  |
| NXOS             | `.System.rpm-items`                                             |

### Standard

| Operating System | Configuration path |
| ---------------- | --------------------------------------------------------------- |
| SR Linux         | `.routing-policy.standard-community-set`                        |
| SR OS            | Not supported                                                   |
| EOS              | Not supported                                                   |
| NXOS             | Not supported                                                   |

### Extended

| Operating System | Configuration path |
| ---------------- | --------------------------------------------------------------- |
| SR Linux         | `.routing-policy.extended-community-set`                        |
| SR OS            | `.configure.policy-options.extended-community-set`              |
| EOS              | Not supported                                                   |
| NXOS             | Not supported                                                   |

### Large

| Operating System | Configuration path |
| ---------------- | --------------------------------------------------------------- |
| SR Linux         | Not supported                                                   |
| SR OS            | Not supported                                                   |
| EOS              | Not supported                                                   |
| NXOS             | Not supported                                                   |

## Match options

When the community set is used in a [`Policy`](./policy.md) to take an action on routes that match a set of community members, the `CommunitySet` determines which routes are matched.

The `matchSetOptions` property accepts:

- `All` to require **all** listed communities
- `Any` to require **any** listed community
- `Invert` to require **none** of the listed communities

Support varies by operating system and community-set type. 

### Match expressions

The `expressionMatch` property may be used when more flexibility is required to match a route's communities. Expression syntax is platform-specific. The following examples use SR Linux syntax:

- `origin:65500:.*`: route-origin extended communities whose Global Administrator is AS 65500
- `target:10.0.0.1:.*`: routes with `10.0.0.1` as global administrator
- `gbp-tag:.*:9.*`: SR Linux Group Policy ID extended communities whose Group Policy ID begins with 9

/// note | Using both members and expressions

SR Linux and SR OS configure both `members` and `expressionMatch` when both are provided. EOS and NXOS Hybrid sets require either `members` or `expressionMatch`, but not both.

///

## Dependencies

This resource does not have any dependencies.

## Referenced resources

This resource does not reference any other resource.

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
