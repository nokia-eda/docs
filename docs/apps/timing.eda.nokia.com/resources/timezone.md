---
resource_name: TimeZone
resource_name_plural: timezones
resource_name_plural_title: Time Zones
resource_name_acronym: TZ
crd_path: docs/apps/timing.eda.nokia.com/crds/timing.eda.nokia.com_timezones.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Time Zone

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A `TimeZone` determines the time zone that a router applies to timestamps when sending information to external systems, most notably when writing or sending log messages.

More than 400 IANA time zones are supported and grouped into nine regions. Region and place values follow IANA time zone names:

- America
- Europe
- Asia
- Australia
- Indian
- Africa
- Pacific
- Antarctica
- Atlantic
- Arctic

Alternatively, a `TimeZone` resource can configure routers to use UTC by setting `useUTC` to `true`.

## Selecting a time zone

Due to the large number of places available, and to ensure a user-friendly UI experience, the `region` property must be set along with the respective `<region-name>Place` property.

## Dependencies

The `TimeZone` resource has no dependencies on other resources.

## Referenced resources

### `TopoNode`

The `TimeZone` is a global configuration setting for a node. The nodes where the `TimeZone` is deployed can be specified through the `nodes` property or by using labels in the `nodeSelectors` property.

Prefer deployment using labels over explicit configuration wherever possible.

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
