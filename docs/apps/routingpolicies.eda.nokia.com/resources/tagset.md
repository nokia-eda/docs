---
resource_name: TagSet
resource_name_plural: tagsets
resource_name_plural_title: Tag Sets
resource_name_acronym: TS
crd_path: docs/apps/routingpolicies.eda.nokia.com/crds/routingpolicies.eda.nokia.com_tagsets.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Tag Set

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `TagSet` resource is a list of internal tags that can be assigned to a route by a [routing policy](./policy.md). These tags are locally significant to the network device and are not communicated to peers.

Tags may be useful for classifying routes. This classification can then determine which routes are sent to which peers. For example, an operator may isolate part of the network from the internet without breaking internal connectivity by assigning a tag to all routes received from a particular BGP peer and preventing these routes from being readvertised to the internet gateway.

/// note

Currently, the number of tags per `TagSet` is limited to one.
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
