---
resource_name: DefaultBGPGroup
resource_name_plural: defaultbgpgroups
resource_name_plural_title: Default BGP Groups
resource_name_acronym: DB
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_defaultbgpgroups.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default BGP Group

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `DefaultBGPGroup` resource is in many ways similar to the [`BGPGroup`](bgpgroup.md) resource, but is deployed in the default VRF instead of the overlay. 

This means that it has support for more routing protocols, which are required to distribute overlay (service) routes. It is a resource that defines parameters that are shared between [`DefaultBGPPeer`](defaultbgppeer.md) resources. Changes applied to this resource will be applied to all peers that reference this group, if those peers don't override these parameters.

## Dependencies

As the Default BGP Group is not configured on the node before a [`DefaultBGPPeer`](defaultbgppeer.md) references it, there are no prerequisites that must be fulfilled before this resource is created. Although every parameter can be overridden individually by the [`DefaultBGPPeer`](defaultbgppeer.md), a `DefaultBGPGroup` must be created first.

## Referenced resources

- [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md): specification of BGP import and export policies
- [`Keychain`](../../../security.eda.nokia.com/docs/resources/keychain.md): authentication parameters for the BGP session

## Examples

/// tab | YAML

```yaml
-{{ include_yaml('docs/snippets/%s.yaml' | format(resource_name | lower)) }}-
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
-{{ include_yaml('docs/snippets/%s.yaml' | format(resource_name | lower)) }}-
EOF
```

///

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
