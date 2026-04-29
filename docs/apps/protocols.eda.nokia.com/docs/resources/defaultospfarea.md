---
resource_name: DefaultOSPFArea
resource_name_plural: defaultospfareas
resource_name_plural_title: Default OSPF Area
resource_name_acronym: DO
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_defaultospfareas.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default OSPF Area

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Open Shortest Path First, or OSPF, is a routing protocol to exchange IP routes. There are two versions of the OSPF protocol:

* Version 2 is configured on IPv4 interfaces and only exchances IPv4 prefixes
* Version 3 is configured on IPv6 interfaces and exchanges both IPv4 and IPv6 prefixes

!!! note "Consider using a Fabric"

    This resource is typically created as a derived resource by the [`Fabric`](../../../fabrics.eda.nokia.com/docs/resources/fabric.md) resource, which takes care of building your entire datacenter fabric, and includes an option to use OSPF in the underlay. Whenever possible, use the [`Fabric`](../../../fabrics.eda.nokia.com/docs/resources/fabric.md) resource instead of manually creating a `DefaultOSPFArea`.

OSPF sessions in the default VRF are always established between [`DefaultOSPFInterfaces`](defaultospfinterface.md) in a `DefaultOSPFArea`, and never operate inter-area. To connect two OSPF areas to each other, an area border router (ABR) configures both areas in the same [`DefaultOSPFInstance`](defaultospfinstance.md). A [`DefaultOSPFInstance`](defaultospfinstance.md) is an isolated process with its own Link State Database (LSDB).

!!! note "OSPF area notation"

    In EDA, the area identifier follows the IP-like "Dotted Decimal Notation" to represent a 32-bit integer, meaning area `1` should be entered as `0.0.0.1`.

> To set up an OSPF area in the overlay, use [`OSPFArea`](ospfarea.md) instead.

## Dependencies

The `DefaultOSPFArea` resource has no dependencies.

## Referenced resources

The `DefaultOSPFArea` resource does not reference any other resources.

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
