---
resource_name: AssociationPolicy
resource_name_plural: associationpolicies
resource_name_plural_title: Association Policies
resource_name_acronym: AP
crd_path: docs/apps/microsegmentation.eda.nokia.com/crds/microsegmentation.eda.nokia.com_associationpolicies.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Group Tag Association Policies

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural ) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

An `AssociationPolicy` associates one or more [`Group Tags`](../resources/grouptag.md) to one or more network resources or `associationTargets`.
The policy consists of entries allowing to group multiple associations between [`Group Tags`](../resources/grouptag.md) and `associationTargets` in a single policy.  

Possible `associationTargets` include:


* [`BridgeInterfaces`](-{{ ref_app_doc('services', 'bridgeinterface') }}-)
* [`RoutedInterfaces`](-{{ ref_app_doc('services', 'routedinterface') }}-)
* [`IRBInterfaces`](-{{ ref_app_doc('services', 'irbinterface') }}-)
* [`VLANs`](-{{ ref_app_doc('services', 'vlan') }}-)
* [`StaticRoutes`](-{{ ref_app_doc('protocols', 'staticroute') }}-)

These resources can be selected by name or using their corresponding label selectors.

For example: a policy entry could associate the Quarantine `GroupTag` with all [`BridgeInterfaces`](-{{ ref_app_doc('services', 'bridgeinterface') }}-) with the label "eda.nokia.com/security=quarantine".

/// admonition | Group Tags can not be associated with network resources from in the underlay
    type: info

Group Tags are not supported on [`DefaultInterfaces`](-{{ ref_app_doc('routing', 'defaultinterface') }}-).
///

## Dependencies

An `AssociationPolicy` associates [`GroupTags`](../resources/grouptag.md)  to `associationTargets`.

One or more [`GroupTags`](../resources/grouptag.md) are required to create an `AssociationPolicy`.

One or more `associationTargets` are required to create an `AssociationPolicy`.

* [`BridgeInterfaces`](-{{ ref_app_doc('services', 'bridgeinterface') }}-)
* [`RoutedInterfaces`](-{{ ref_app_doc('services', 'routedinterface') }}-)
* [`IRBInterfaces`](-{{ ref_app_doc('services', 'irbinterface') }}-)
* [`VLANs`](-{{ ref_app_doc('services', 'vlan') }}-)
* [`StaticRoutes`](-{{ ref_app_doc('protocols', 'staticroute') }}-)

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
