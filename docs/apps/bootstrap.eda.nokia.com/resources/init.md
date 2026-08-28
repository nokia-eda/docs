---
resource_name: Init
resource_name_plural: inits
resource_name_plural_title: Inits
resource_name_acronym: I
crd_path: docs/apps/bootstrap.eda.nokia.com/crds/bootstrap.eda.nokia.com_inits.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Bootstrap

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `Init` resource, also known as the `Bootstrap` resource in the UI, prepares nodes for first contact with EDA. It pushes configuration that EDA needs in order to reach the node, such as the management interface, the [management router](./managementrouter.md), the gRPC server, and the hostname.

In addition to creating configuration objects, it creates `TargetNode` resources for TLS onboarding, a companion `ManagementRouter`, and `Artifact` resources such as the ZTP bootstrap script for each node and the initial ZTP configuration that the script retrieves.

## Modify initial configuration

The `Init` resource can be modified with additional configuration options, such as extra static routes for the management network instance or a different MTU on the out-of-band management interface.

## Override initial configuration

Sometimes it is necessary to override the default configuration pushed by the `Init` resource. One example is the [`AuthenticationPolicy`](-{{ref_app_doc('aaa', 'authenticationpolicy')}}-), which can override the default authentication order (the order in which remote authentication servers and local authentication are attempted).

In EDA, each configuration object has a priority value. You can read more about priorities in the [configuration application](-{{ref_app_doc('config', 'configlet')}}-#priorities).

The configuration objects pushed by the `Init` resource have their priority value set to `-100`, and are therefore overwritten by any higher-priority configuration pushed by other resources to the same configuration paths.

## Dependencies

The `Init` resource does not have any dependencies.

## Referenced resources

The `Init` resource does not reference any other EDA resources.

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
