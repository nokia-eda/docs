---
resource_name: NTPClient
resource_name_plural: ntpclients
resource_name_plural_title: NTP Clients
resource_name_acronym: NC
crd_path: docs/apps/timing.eda.nokia.com/crds/timing.eda.nokia.com_ntpclients.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# NTP Client

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

NTP servers are timekeeping entities that allow clients to request the current time periodically, preventing long-term drift and ensuring that all devices within an NTP domain use the same time reference.

NTP servers can in turn be clients of another NTP server. The `stratum` number indicates the number of synchronization hops between an NTP server and a reference clock. Stratum `1` servers are directly connected to a precise stratum `0` reference, such as an atomic clock or a GNSS receiver.

Use an `NTPClient` resource to configure network elements with the same reference time.

## Reachability

The NTP server can be reached through the out-of-band [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), or in-band through the [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-) or a virtual [`Router`](-{{ref_app_doc('services', 'router')}}-).

NTP uses UDP datagrams for low-latency, connectionless data delivery. Upon receipt of an NTP request, the server sends a reply to the request's source IP address.

The source IP address of the `NTPClient` is derived automatically from the available interfaces of the source router. It can also be defined explicitly by specifying a [`SystemInterface`](-{{ref_app_doc('routing', 'systeminterface')}}-) or [`DefaultInterface`](-{{ref_app_doc('routing', 'defaultinterface')}}-) reference for a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), or a [`RoutedInterface`](-{{ref_app_doc('services', 'routedinterface')}}-) or [`IRBInterface`](-{{ref_app_doc('services', 'irbinterface')}}-) reference for a virtual [`Router`](-{{ref_app_doc('services', 'router')}}-).

## Initial burst

Initial burst, or `iBurst`, is a configuration option that speeds up initial clock synchronization. The client sends a short sequence of packets instead of relying on the normal polling interval.

## Preferred server

Set `preferred` to `true` to mark a server as preferred when the client selects among suitable servers.

## Dependencies

The type of router that the `NTPClient` will use to reach out to the NTP server can be selected through the `routerKind` property.

### Router types

#### [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-)

If `routerKind` is set to `ManagementRouter`, the `router` property should contain a valid reference to a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-). The `NTPClient` will be deployed on all nodes that participate in the router.

#### [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-)

If `routerKind` is set to `DefaultRouter`, exactly one of the `router` and `routerSelectors` properties must select valid references to a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-). The `NTPClient` will be deployed on all nodes that participate in the selected router or routers.

#### [`Router`](-{{ref_app_doc('services', 'router')}}-)

If `routerKind` is set to `Router`, the `router` property should contain a valid reference to a [`Router`](-{{ref_app_doc('services', 'router')}}-). The `NTPClient` will be deployed on all nodes that participate in the router.

## Referenced resources

### Source interface types

The source address of NTP request packets can be derived by the node from the available interfaces of the router, or it can be specified explicitly using the `sourceInterface` property. When specifying an interface, set both `sourceInterfaceKind` and `sourceInterface`. A `ManagementRouter` does not support either property.

#### [`SystemInterface`](-{{ref_app_doc('routing', 'systeminterface')}}-)

If `routerKind` is set to `DefaultRouter` and `sourceInterfaceKind` is set to `SystemInterface`, the `sourceInterface` property should contain a valid reference to a [`SystemInterface`](-{{ref_app_doc('routing', 'systeminterface')}}-).

/// details | System interfaces can only be used in a `DefaultRouter`

If multiple nodes are selected by the `router` or `routerSelectors` property and the `sourceInterface` is a system interface, the `NTPClient` will only be deployed on the node that the [`SystemInterface`](-{{ref_app_doc('routing', 'systeminterface')}}-) is deployed on.

///

#### [`DefaultInterface`](-{{ref_app_doc('routing', 'defaultinterface')}}-)

If `routerKind` is set to `DefaultRouter` and `sourceInterfaceKind` is set to `DefaultInterface`, the `sourceInterface` property should contain a valid reference to a [`DefaultInterface`](-{{ref_app_doc('routing', 'defaultinterface')}}-).

/// details | Default interfaces can only be used in a `DefaultRouter`

If multiple nodes are selected by the `router` or `routerSelectors` property and the `sourceInterface` is a default interface, the `NTPClient` will only be deployed on the node that the [`DefaultInterface`](-{{ref_app_doc('routing', 'defaultinterface')}}-) is deployed on.

///

#### [`RoutedInterface`](-{{ref_app_doc('services', 'routedinterface')}}-)

If `routerKind` is set to `Router` and `sourceInterfaceKind` is set to `RoutedInterface`, the `sourceInterface` property should contain a valid reference to a [`RoutedInterface`](-{{ref_app_doc('services', 'routedinterface')}}-).

/// details | Routed interfaces can only be used in a virtual `Router`

If the selected `Router` spans multiple nodes and the `sourceInterface` is a routed interface, the `NTPClient` will be deployed only on the nodes where the [`RoutedInterface`](-{{ref_app_doc('services', 'routedinterface')}}-) is deployed.

///

#### [`IRBInterface`](-{{ref_app_doc('services', 'irbinterface')}}-)

If `routerKind` is set to `Router` and `sourceInterfaceKind` is set to `IRBInterface`, the `sourceInterface` property should contain a valid reference to an [`IRBInterface`](-{{ref_app_doc('services', 'irbinterface')}}-).

/// details | IRB interfaces can only be used in a virtual `Router`

If the selected `Router` spans multiple nodes and the `sourceInterface` is an IRB interface, the `NTPClient` will be deployed only on the nodes where the [`IRBInterface`](-{{ref_app_doc('services', 'irbinterface')}}-) is deployed.

The `NTPClient` will prefer IP addresses that are marked as `primary` in the [`IRBInterface`](-{{ref_app_doc('services', 'irbinterface')}}-).

///

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
