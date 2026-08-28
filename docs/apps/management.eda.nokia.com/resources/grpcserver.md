---
resource_name: GRPCServer
resource_name_plural: grpcservers
resource_name_plural_title: GRPC Servers
resource_name_acronym: GS
crd_path: docs/apps/management.eda.nokia.com/crds/management.eda.nokia.com_grpcservers.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# GRPC Server

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `GRPCServer` resource enables a node to function as a gRPC server for remote management.

/// admonition
    type: info

gRPC is a high-performance Remote Procedure Call (RPC) framework. It enables various management and telemetry interfaces, such as:

- `gNMI`: gRPC Network Management Interface
- `gNOI`: gRPC Network Operations Interface
- `gNSI`: gRPC Network Security Interface
- `gRIBI`: gRPC Routing Information Base Interface

Node users that may access the `GRPCServer` must have the appropriate permissions.

///

## OS-specific limitations

Some operating systems have specific implementation details that are worth considering.

### SR Linux

In SR Linux, each gRPC server is an independently configured instance that runs in a particular network instance. Multiple gRPC servers can run in the same network instance, provided each server uses a different port.

The following names are restricted for internal use, and cannot be used as the name of a `GRPCServer`:

- `discovery`
- `mgmt`

### SR OS

On SR OS, a single gRPC server supports concurrent sessions and can be reached through one or more network instances. Because EDA uses gNMI to communicate with an SR OS node, the management application prevents disabling the gNMI service that EDA relies on.

Only create a `GRPCServer` on SR OS to enable or disable certain additional gRPC-based services, or to allow access to the gRPC interfaces through a virtual [Router](-{{ref_app_doc('services', 'router')}}-).

## Dependencies

Each `GRPCServer` resource targets either a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), or a [`Router`](-{{ref_app_doc('services', 'router')}}-). While only one of the three is required, all three are listed as dependencies.

### [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-)

If the `GRPCServer` is reachable through a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), the resource referenced by the `router` property must exist.

/// note | Management routers cannot be selected through label selectors.
///

### [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-)

If the `GRPCServer` is reachable through a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), the resource referenced by the `router` property must exist.

Label selectors may be used to select multiple [`DefaultRouters`](-{{ref_app_doc('routing', 'defaultrouter')}}-).

### [`Router`](-{{ref_app_doc('services', 'router')}}-)

If the `GRPCServer` is reachable through a [`Router`](-{{ref_app_doc('services', 'router')}}-), the resource referenced by the `router` property must exist.

/// note | Routers cannot be selected through label selectors.
///

## Referenced resources

The `GRPCServer` does not reference any other EDA resources.

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
