---
resource_name: SSHServer
resource_name_plural: sshservers
resource_name_plural_title: SSH Servers
resource_name_acronym: SS
crd_path: docs/apps/management.eda.nokia.com/crds/management.eda.nokia.com_sshservers.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# SSH Server

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `SSHServer` resource enables a node to function as an SSH server for remote login.

## OS-specific limitations

Some operating systems have specific implementation details that are worth considering.

### SR OS

On SR OS, SSH is enabled by default in the [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-) and the [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-).

- If access in both should be disabled, create an `SSHServer` resource on either the `ManagementRouter` or the `DefaultRouter` and set the `enabled` property to `false`.
- If one should be enabled but not the other, consider using [CPM filters](-{{ref_app_doc('filters', 'controlplanefilter')}}-).

### SR Linux

On SR Linux, SSH is enabled by default in the [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-). If access should be disabled, create an `SSHServer` resource that targets the [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-) and set the `enabled` property to `false`.

## Dependencies

Each `SSHServer` resource targets either a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), or a [`Router`](-{{ref_app_doc('services', 'router')}}-). While only one of the three is required, all three are listed as dependencies.

### [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-)

If the `SSHServer` is reachable through a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), the resource referenced by the `router` property must exist.

/// note | Management routers cannot be selected through label selectors.
///

### [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-)

If the `SSHServer` is reachable through a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), the resource referenced by the `router` property must exist.

Label selectors may be used to select multiple [`DefaultRouters`](-{{ref_app_doc('routing', 'defaultrouter')}}-).

### [`Router`](-{{ref_app_doc('services', 'router')}}-)

If the `SSHServer` is reachable through a [`Router`](-{{ref_app_doc('services', 'router')}}-), the resource referenced by the `router` property must exist.

/// note | Routers cannot be selected through label selectors.
///

## Referenced resources

The `SSHServer` does not reference any other EDA resources.

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
