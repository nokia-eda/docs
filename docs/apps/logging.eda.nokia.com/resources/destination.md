---
resource_name: Destination
resource_name_plural: destinations
resource_name_plural_title: Destinations
resource_name_acronym: D
crd_path: docs/apps/logging.eda.nokia.com/crds/logging.eda.nokia.com_destinations.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Destination

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A logging `Destination` receives log messages captured by one or more [`Source`](./source.md) resources. The [`Log`](./log.md) deploys the `Destination` to a node and determines which `Source` resources are used for it.

The application supports three destination types:

- Stored in **memory** on the node that the [`Log`](./log.md) is configured on
- Stored in a **file** on the node that the [`Log`](./log.md) is configured on
- Sent to an external **syslog** server

## Rotation and retention

Different operating systems accept different parameters for `Destination` resources of type `Memory` and `File`. Some, such as SR Linux, monitor file size, while others, such as SR OS, monitor the number of lines or the log file's time span.

If the `rotation` parameters are not defined, the defaults for that particular operating system are used. If they are defined, then the `Destination` may not be configurable across multiple operating systems.

## Syslog router

For a `Destination` of type `Syslog`, the syslog server can be reached through the out-of-band [ManagementRouter](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), the [DefaultRouter](-{{ref_app_doc('routing', 'defaultrouter')}}-), or a virtual [`Router`](-{{ ref_app_doc('services', 'router' )}}-).

## Dependencies

### [`Router`](-{{ref_app_doc('services', 'router')}}-)

If the `routerKind` is set to `Router`, then a valid [`Router`](-{{ref_app_doc('services', 'router')}}-) resource reference must be provided.

## Referenced resources

The `Destination` does not reference any other EDA resources.

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

To browse the Custom Resource Definition, go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
