---
resource_name: Policy
resource_name_plural: policys
resource_name_plural_title: Policies
resource_name_acronym: P
crd_path: docs/apps/routingpolicies.eda.nokia.com/crds/routingpolicies.eda.nokia.com_policys.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Policy

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `Policy` resource in this app is an abstraction for a routing policy that controls the distribution of reachability information, both internally (local to the device) and externally to peers.

A `Policy` can be applied in two directions:

- An import `Policy` controls which received routes are installed in the routing table.
- An export `Policy` controls which installed routes are advertised to a routing peer.

Routing `Policies` are also used to [leak](../index.md#route-leaking) routes from one virtual [Router](-{{ ref_app_doc('services', 'router') }}-) to another.

## Policy statements

A routing `Policy` consists of an ordered list of policy statements. Each statement has a required name and may define match criteria and an action. The action may modify matching routes and may set a policy result that controls evaluation.

Match criteria, actions, and policy results are discussed below.

### Match criteria

The routing policy can look at several aspects of a route. Some examples are:

- The protocol type of the route (BGP, IS-IS, ...)
- The address family of the route (IPv4 unicast, EVPN, ...)
- Whether the route matches a certain [`PrefixSet`](./prefixset.md)
- Whether there is an internal routing tag associated with the route that belongs to a certain [`TagSet`](./tagset.md)

Specific to BGP routes:

- Whether the AS path of a route matches an [`ASPathSet`](./aspathset.md)
- Whether the BGP route has route attributes that match a certain [`CommunitySet`](./communityset.md)

If a route matches **all** match criteria, the [action](#actions) is taken (if specified), and the [policy result](#policy-result) of the statement is evaluated.

### Actions

When the route that is being evaluated matches all [match criteria](#match-criteria), the route can be modified. This may be useful to tag all routes that are received from a particular BGP peer, or to evaluate whether a route should be redistributed to other network elements. Some examples of route modifications are:

- Adding an internal routing [`tag`](./tagset.md) to the route
- Modifying the route preference for the route

Specific to BGP routes:

- Modifying BGP attributes like the local preference and MED values
- Prepending to, removing, or replacing the AS path
- Adding, removing, or replacing BGP communities
- Rewriting the next-hop for the route

After the actions have been executed on the route, the [policy result](#policy-result) of the statement is evaluated.

Action and policy-result support is platform- and version-specific. On the current EOS and NX-OS implementations, `NextPolicy` and `NextStatement` do not retain the semantics described below.

### Policy result

When the route being evaluated matches all [match criteria](#match-criteria), and the appropriate [actions](#actions) have been taken to modify the route, the policy result of the statement determines what happens next:

- `Accept`: accept the route and do not evaluate any other policy statements (including the [default policy statement](#default-policy-statement)). Do not evaluate any other `Policies` for this route.
- `Reject`: reject the route and do not evaluate any other policy statements (including the [default policy statement](#default-policy-statement)). Do not evaluate any other `Policies` for this route.
- `NextPolicy`: do not evaluate any other policy statements (including the [default policy statement](#default-policy-statement)). Continue evaluation in the next `Policy`.
- `NextStatement`: continue evaluating the remaining statements of the `Policy`.

### Default policy statement

If all `Policy` statements have been evaluated, and the route is neither rejected nor accepted, the default action determines what happens to the route.

## Dependencies

This resource does not have any depencies.

## Referenced resources

### [`PrefixSet`](./prefixset.md)

`PrefixSets` can be used in the [match criteria](#match-criteria) of a [policy statement](#policy-statements) to determine what [actions](#actions) are performed on matching routes.

### [`ASPathSet`](./aspathset.md)

`ASPathSets` can be used in the [match criteria](#match-criteria) of a [policy statement](#policy-statements) to determine what [actions](#actions) are performed on BGP routes that have a certain Autonomous System (AS) path.

### [`CommunitySet`](./communityset.md)

`CommunitySets` can be used in the [match criteria](#match-criteria) of a [policy statement](#policy-statements) to determine what [actions](#actions) are performed based on whether a BGP route's community values match the set.

They can also be used to add, remove, or replace the BGP communities of a matching route with the communities in the set.

### [`TagSet`](./tagset.md)

`TagSets` can be used in the [match criteria](#match-criteria) of a [policy statement](#policy-statements) to determine what [actions](#actions) are performed on routes that have none, one, or more associated internal routing tags in the set.

They can also be used to set the internal routing tag of a matching route.

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
