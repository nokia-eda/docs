---
resource_name: FTPServer
resource_name_plural: ftpservers
resource_name_plural_title: FTP Servers
resource_name_acronym: FS
crd_path: docs/apps/management.eda.nokia.com/crds/management.eda.nokia.com_ftpservers.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# FTP Server

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `FTPServer` resource enables a node to function as an FTP server for file transfers.

/// admonition
    type: info

Node users that may access the `FTPServer` must have the `FTP` service permission.

///

## OS-specific limitations

Some operating systems have specific implementation details that are worth considering.

### SR OS

On SR OS, an `FTPServer` resource configured on a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-) will also enable the FTP server on the [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), and vice versa. If one should be enabled but not the other, consider using [CPM filters](-{{ref_app_doc('filters', 'controlplanefilter')}}-).

An `FTPServer` resource configured on a [`Router`](-{{ref_app_doc('services', 'router')}}-) will also enable the FTP server on the [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-) and the [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-). To disable the FTP server on those routers, create an additional `FTPServer` with type `ManagementRouter` or `DefaultRouter` and set the `enabled` property to `false`.

## Dependencies

Each `FTPServer` resource targets either a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), or a [`Router`](-{{ref_app_doc('services', 'router')}}-). While only one of the three is required, all three are listed as dependencies.

### [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-)

If the `FTPServer` is reachable through a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), the resource referenced by the `router` property must exist.

/// note | Management routers cannot be selected through label selectors.
///

### [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-)

If the `FTPServer` is reachable through a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), the resource referenced by the `router` property must exist.

Label selectors may be used to select multiple [`DefaultRouters`](-{{ref_app_doc('routing', 'defaultrouter')}}-).

### [`Router`](-{{ref_app_doc('services', 'router')}}-)

If the `FTPServer` is reachable through a [`Router`](-{{ref_app_doc('services', 'router')}}-), the resource referenced by the `router` property must exist.

/// note | Routers cannot be selected through label selectors.
///

## Referenced resources

The `FTPServer` does not reference any other EDA resources.

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
