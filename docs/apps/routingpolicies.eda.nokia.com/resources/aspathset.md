---
resource_name: ASPathSet
resource_name_plural: aspathsets
resource_name_plural_title: AS Path Sets
resource_name_acronym: AP
crd_path: docs/apps/routingpolicies.eda.nokia.com/crds/routingpolicies.eda.nokia.com_aspathsets.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# AS Path Set

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `ASPathSet` resource groups one or more autonomous system numbers (ASNs) and can be referenced by a [routing policy](./policy.md) to match a route that has none, any, or all of these AS numbers.

## Match options

Whether the route is matched if **all**, **any**, or **none** of the members are found in the route's AS path is determined by the [`Policy`](./policy.md) statement, not the `ASPathSet`.

Members of the `ASPathSet` are regexes, which are checked against either the entire AS path or the individual AS numbers (see section about [regex modes](#regex-modes)).

### Regex modes

When `regexMode` is set to `ASN`, each ASN is treated as a single element that is matched against the member regexes defined in the `ASPathSet`. If `regexMode` is set to `Character`, the route's entire AS path is treated as a string and matched character by character, similar to traditional regex matching.

/// details | Example 1: matching any path that contains ASN 100 or 101
    type: example

In `Character` mode, AS paths containing ASNs such as 1000 or 2101 would also be matched.

```yaml
apiVersion: routingpolicies.eda.nokia.com/v1
kind: ASPathSet
metadata:
  name: leaf-asns
  namespace: routingpolicies
spec:
  members:
    - '100'
    - '101'
  regexMode: ASN
```

///

/// details | Example 2: matching any path where at least one ASN has a 9 in it
    type: example

In `ASN` mode, this expression would match only ASN 9, not any ASN containing the digit 9.

```yaml
apiVersion: routingpolicies.eda.nokia.com/v1
kind: ASPathSet
metadata:
  name: leaf-asns
  namespace: routingpolicies
spec:
  members:
    - '9'
  regexMode: Character
```

///

/// details | Example 3: matching any path containing a single ASN from 100 through 109
    type: example

In `Character` mode, this path would also match paths with ASN 1000 or 1099

```yaml
apiVersion: routingpolicies.eda.nokia.com/v1
kind: ASPathSet
metadata:
  name: leaf-asns
  namespace: routingpolicies
spec:
  members:
    - '^[100-109]'
  regexMode: ASN
```

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
