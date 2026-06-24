---
resource_name: BGPGroup
resource_name_plural: bgpgroups
resource_name_plural_title: BGP Groups
resource_name_acronym: BG
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_bgpgroups.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# BGP Group

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `BGPGroup` enables centralized management of BGP peer configurations. This resource allows setting a description, common BGP settings, and peer-specific configurations, simplifying the consistent application of policies across multiple peers. It also includes transport settings, such as local TCP address configuration, passive mode, and TCP MSS.

A `BGPGroup` resource defines BGP protocol parameters that are inherited by the [`BGPPeer`](bgppeer.md) resources that reference this group. The parameters set on the [`BGPPeer`](bgppeer.md) level override the group-level parameters.

> To set up BGP groups for use in the default VRF, use [`DefaultBGPGroup`](defaultbgpgroup.md) resource.

## Dependencies

The BGP Group is not instantiated on the targeted network elements before a [`BGPPeer`](bgppeer.md) referencing it is created.

Although every group-level parameter can be overridden individually on the [`BGPPeer`](bgppeer.md) level, a `BGPGroup` must be created and referenced by the peer.

## Referenced resources

The following resources are referenced in the specification of the `BGPGroup`:

### [`Policy`](../../../routingpolicies.eda.nokia.com/docs/resources/policy.md)

The [`BGPPeer`](bgppeer.md) resources that the `RouteReflector` creates towards each selected [`RouteReflectorClient`](routereflectorclient.md) inherit import/export policies from the assigned [`BGPGroup`](#dependencies). This behavior can be overridden by specifying policies in the `RouteReflector`. Click [here](bgppeer.md#policy) for more information on BGP import/export policies.

### [`KeyChain`](../../../security.eda.nokia.com/docs/resources/keychain.md)

To secure the connection between two BGP peers, a secret authentication key can be configured in a keychain. This ensures that only BGP speakers with the password can establish a connection. Multiple keys can be defined in a [`Keychain`](../../../security.eda.nokia.com/docs/resources/keychain.md) to enable automatic key rollover.

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
