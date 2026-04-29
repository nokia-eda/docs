---
resource_name: OSPFArea
resource_name_plural: ospfareas
resource_name_plural_title: OSPF Area
resource_name_acronym: OA
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_ospfareas.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# OSPF Area

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

Open Shortest Path First, or OSPF, is a routing protocol to exchange IP routes. There are two versions of the OSPF protocol:

* Version 2 is configured on IPv4 interfaces and only exchances IPv4 prefixes
* Version 3 is configured on IPv6 interfaces and exchanges both IPv4 and IPv6 prefixes

OSPF sessions are always established between [`OSPFInterfaces`](ospfinterface.md) in an `OSPFArea`, and never operate inter-area. To connect two OSPF areas to each other, an area border router (ABR) configures both areas in the same [`OSPFInstance`](ospfinstance.md). An [`OSPFInstance`](ospfinstance.md) is an isolated process with its own Link State Database (LSDB).

!!! note "OSPF area notation"

    In EDA, the area identifier follows the IP-like "Dotted Decimal Notation" to represent a 32-bit integer, meaning area `1` should be entered as `0.0.0.1`.

> To set up an OSPF area in the default VRF, use [`DefaultOSPFArea`](defaultospfarea.md) instead.

## Dependencies

The `OSPFArea` resource has no dependencies.

## Referenced resources

The `OSPFArea` resource does not reference any other resources.

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
