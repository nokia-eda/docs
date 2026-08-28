---
resource_name: PrefixSet
resource_name_plural: prefixsets
resource_name_plural_title: Prefix Sets
resource_name_acronym: PS
crd_path: docs/apps/routingpolicies.eda.nokia.com/crds/routingpolicies.eda.nokia.com_prefixsets.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Prefix Set

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `PrefixSet` resource is used to check whether a route belongs to a logical group of prefixes. It is used in the match criteria of a routing [`Policy`](./policy.md) to take an action on an imported or exported route, such as preventing the route from being advertised, adding an internal [`Tag`](./tagset.md), or modifying its BGP [`Communities`](./communityset.md).

Each `PrefixSet` contains prefix entries. Each entry consists of an IP subnet and, optionally, a prefix-length range for matching more-specific routes.

## Example 1: matching all point-to-point subnets

The following `PrefixSet` matches any IPv4 `/30` or `/31` subnet:

```yaml
apiVersion: routingpolicies.eda.nokia.com/v1
kind: PrefixSet
metadata:
  name: point-to-points
  namespace: eda
spec:
  prefixes:
    - endRange: 31
      prefix: 0.0.0.0/0
      startRange: 30
```

## Example 2: matching all routes to private IP ranges

The following `PrefixSet` matches any route in the private IPv4 address space defined in RFC 1918.

```yaml
apiVersion: routingpolicies.eda.nokia.com/v1
kind: PrefixSet
metadata:
  namespace: eda
  name: private-ip-subnets
spec:
  prefixes:
    - prefix: 10.0.0.0/8
      startRange: 8
      endRange: 32
    - prefix: 172.16.0.0/12
      startRange: 12
      endRange: 32
    - prefix: 192.168.0.0/16
      startRange: 16
      endRange: 32
```

## Example 3: matching the exact route to a subnet

The following `PrefixSet` matches the route to a particular subnet. It does not match routes with shorter or longer prefix lengths.

```yaml
apiVersion: routingpolicies.eda.nokia.com/v1
kind: PrefixSet
metadata:
  namespace: eda
  name: management-subnet
spec:
  prefixes:
    - prefix: 10.10.10.0/24
      exact: true
```

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
