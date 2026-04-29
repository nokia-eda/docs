---
resource_name: PrefixSet
resource_name_plural: prefixsets
resource_name_plural_title: Prefix Sets
resource_name_acronym: PS
crd_path: docs/apps/filters.eda.nokia.com/crds/filters.eda.nokia.com_prefixsets.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Prefix Set

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural ) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `PrefixSet` is a collection of IP prefixes. They are used in [`Filter`](filter.md) resources to match the source or destination IP of a packet against a certain prefix range, to determine whether to accept or drop a packet. Some common use cases are:

- Allowing SSH connections from a subnet of IP addresses associated with internal, privileged clients
- Restricting DNS traffic to a few IP addresses, to enable content filtering

!!! warning

    This article discusses the `PrefixSet` resource used for configuring packet [`Filters`](filter.md). The [`PrefixSet`](../../../routingpolicies.eda.nokia.com/docs/resources/prefixset.md) resource used by [`RoutingPolicies`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md) is a different resource (same name, different app)

## Dependencies

The `PrefixSet` has no dependencies on other resources.

## Referenced resources

The `PrefixSet` resource does not reference any other resources.

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
