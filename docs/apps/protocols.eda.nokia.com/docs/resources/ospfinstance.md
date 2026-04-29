---
resource_name: OSPFInstance
resource_name_plural: ospfinstances
resource_name_plural_title: OSPF Instances
resource_name_acronym: OI
crd_path: docs/apps/protocols.eda.nokia.com/crds/protocols.eda.nokia.com_ospfinstances.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# OSPF Instance

-{{% import 'icons.html' as icons %}}-

-{{icons.overlay_routing()}}- → -{{icons.circle(letter="OI", text="OSPF Instances")}}-

Open Shortest Path First, or OSPF, is a routing protocol to exchange IP routes. There are two versions of the OSPF protocol:

* Version 2 is configured on IPv4 interfaces and only exchances IPv4 prefixes
* Version 3 is configured on IPv6 interfaces and exchanges both IPv4 and IPv6 prefixes

OSPF sessions are always established between [`OSPFInterfaces`](ospfinterface.md) in an [`OSPFArea`](ospfarea.md), and never operate inter-area. To connect two OSPF areas to each other, an area border router (ABR) configures both areas in the same `OSPFInstance`. An `OSPFInstance` is an isolated process with its own Link State Database (LSDB).

!!! warning "Multiple OSPF instances"

    Not all operating systems support multiple OSPF instances in one network instance

> To set up an OSPF instance in the default VRF, use [`DefaultOSPFInstance`](defaultospfinstance.md) instead.

## Dependencies

The `OSPFInstance` resource has no dependencies.

## Referenced resources

The `OSPFInstance` does not reference any other resources.

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
