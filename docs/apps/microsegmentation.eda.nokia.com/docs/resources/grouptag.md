---
resource_name: GroupTag
resource_name_plural: grouptags
resource_name_plural_title: Group Tags
resource_name_acronym: GT
crd_path: docs/apps/microsegmentation.eda.nokia.com/crds/microsegmentation.eda.nokia.com_grouptags.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Group Tags

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `GroupTag` is used to create micro segments in the network, tagging endpoints with a similar security posture, allowing for easy management of security rules. 
Group tags can be assigned to [`BridgeInterfaces`](../../../services.eda.nokia.com/docs/resources/bridgeinterface.md), [`RoutedInterfaces`](../../../services.eda.nokia.com/docs/resources/routedinterface.md), [`IRBInterfaces`](../../../services.eda.nokia.com/docs/resources/irbinterface.md), [`VLANs`](../../../services.eda.nokia.com/docs/resources/vlan.md), and [`StaticRoutes`](../../../protocols.eda.nokia.com/docs/resources/staticroute.md) through a [`GroupTagAssociationPolicy`](../resources/associationpolicy.md)

## Scopes

`GroupTags` are uniquely identified by a "Group Tag ID" which is automatically assigned by EDA and is used by the node to distribute the `GroupTags` through the control plane. The `Group Tag IDs` are allocated from predefined `IndexAllocationPools` bootstrap resources named `group-tag-pool-global` and `group-tag-pool-local`. 

!!! info "Manually creating the Group Tag Pools"
    By default the `IndexAllocationPools` bootstrap resources named `group-tag-pool-global` and `group-tag-pool-local` are installed during the installation of the micro segmentation app, and in new namespaces with bootstrap enabled. When using micro segmentation in a namespace that is created without bootstrapping, the `IndexAllocationPools` can be created manually with the same names.

Because there is a limited range from which to assign "Group Tag IDs", EDA introduces a concept of local and global "scopes" where an ID is uniquely defined. Scopes can be either global (the whole namespace) or local (the Virtual Network or highest level service abstraction used, for example, a [`Router`](../../../services.eda.nokia.com/docs/resources/router.md) or [`BridgeDomain`](../../../services.eda.nokia.com/docs/resources/bridgedomain.md)).

!!! info "The use of Virtual Networks abstractions is recommended"

    Scopes are automatically derived by the highest level service abstraction. When `Virtual Networks` are used, each Virtual Network becomes a scope and a dedicated instance of the group-tag-pool-local is assigned. This guarantees optimal ID reuse across services. 
    When lower level service abstractions such as `Bridge Domain` or `Router` are used to compose a service, the use of Global `GroupTags` is recommended to guarantee the GroupTag is defined using the same ID across the service end to end.

### Global scope 

A global scope is only recommended when

* `GroupTags` are leaked between different services (for example shared infrastructure such as DNS, storage, NTP, etc)
* A service is manually composed of individual service abstractions such as a [`Router`](../../../services.eda.nokia.com/docs/resources/router.md) or [`BridgeDomain`](../../../services.eda.nokia.com/docs/resources/bridgedomain.md) etc. 

If a `GroupTag` is created with a global scope, the "Group Tag ID" is reserved in the group-tag-pool-global `IndexAllocationPool`. The ID is reserved within the namespace before association, at the time of creation. 

For example: a global `GroupTag` is assigned ID 11; this ID is reserved in all services of the namespace.

### Local scope

A local `GroupTag` can have different IDs in different scopes.
If a `GroupTag` is created with a local scope a "Group Tag ID" will be reserved in an instance of the group-tag-pool-local `IndexAllocationPool` for each scope where the `GroupTag` is used.

For example a `GroupTag` "blue" is created with a local scope and `GroupTag` "blue" is associated with a [`BridgeInterface`](../../../services.eda.nokia.com/docs/resources/bridgeinterface.md) in [`VirtualNetwork`](../../../services.eda.nokia.com/docs/resources/virtualnetwork.md) Service-1, an ID (e.g. 64) will be allocated from a `group-tag-pool-local` instance dedicated to Service-1. When "blue" is associated with an interface or route in another [`VirtualNetwork`](../../../services.eda.nokia.com/docs/resources/virtualnetwork.md) Service-2, an ID (e.g. 92) will be allocated from a `group-tag-pool-local` instance dedicated to Service-2. 
The `GroupTag` "blue" can have different IDs in different scopes depending on the availability of indices in the pool instance. 



## Dependencies

The `IndexAllocationPool` resources named `group-tag-pool-global` and `group-tag-pool-local` are required in order for a "Group Tag ID" to be allocated for the `GroupTag`. They are created during namespace bootstrapping or can be created manually.

## Referenced resources
There are no references to other resources.

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
