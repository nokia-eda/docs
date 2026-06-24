---
resource_name: DefaultOSPFInstance
resource_name_plural: defaultospfinstances
resource_name_plural_title: Default OSPF Instances
resource_name_acronym: DO
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_defaultospfinstances.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Default OSPF Instance

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Open Shortest Path First, or OSPF, is a routing protocol to exchange IP routes. There are two versions of the OSPF protocol:

* Version 2 is configured on IPv4 interfaces and only exchances IPv4 prefixes
* Version 3 is configured on IPv6 interfaces and exchanges both IPv4 and IPv6 prefixes

!!! note "Consider using a Fabric"

    This resource is typically created as a derived resource by the [`Fabric`](../../../fabrics.eda.nokia.com/docs/resources/fabric.md) resource, which takes care of building your entire datacenter fabric, and includes an option to use OSPF in the underlay. Whenever possible, use the [`Fabric`](../../../fabrics.eda.nokia.com/docs/resources/fabric.md) resource instead of manually creating a `DefaultOSPFInstance`.

OSPF sessions in the default VRF are always established between [`DefaultOSPFInterfaces`](defaultospfinterface.md) in a [`DefaultOSPFArea`](defaultospfarea.md), and never operate inter-area. To connect two OSPF areas to each other, an area border router (ABR) configures both areas in the same `DefaultOSPFInstance`. A `DefaultOSPFInstance` is an isolated process with its own Link State Database (LSDB).

> To set up an OSPF instance in the overlay, use [`OSPFInstance`](ospfinstance.md) instead.

## Dependencies

The `DefaultOSPFInstance` resource has no dependencies.

## Referenced resources

The `DefaultOSPFInstance` does not reference any other resources.

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
