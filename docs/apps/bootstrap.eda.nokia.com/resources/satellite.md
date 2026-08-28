---
resource_name: Satellite
resource_name_plural: satellites
resource_name_plural_title: Satellites
resource_name_acronym: S
crd_path: docs/apps/bootstrap.eda.nokia.com/crds/bootstrap.eda.nokia.com_satellites.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Satellite

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

A satellite in the context of EDA is a physical switch that extends the capabilities of its uplink host. Typical uses include:

- Acting as an aggregator switch in a remote location
- Splitting one higher-capacity port into multiple lower-capacity ports without using "octopus" or breakout cables

The key difference between a satellite and a [breakout switch](-{{ref_app_doc('services', 'vlan')}}-#uplinks) is how the nodes are managed. A **breakout** switch is a standalone managed switch, whereas a **satellite** switch is managed through its uplink host. A protocol runs on the link between the satellite and the host so that the correct software and configuration are pushed to the satellite. From a CLI point of view, the satellite ports show up next to the host ports on the host switch.

/// note

Satellite switches cannot be created manually. Instead, they are created by the [`Init`](./init.md) resource when it detects that a `TopoNode` has satellite nodes.

///

## Supported hardware

Satellites are only supported on SR OS. The following platforms are supported to manage satellites:

- Nokia 7750 SR-1se
- Nokia 7750 SR-2s
- Nokia 7750 SR-2se
- Nokia 7750 SR-1-48D
- Nokia 7750 SR-1x-48D

On those platforms, the following hardware satellite platforms are supported:

### Nokia 7250 IXR-e

Only the variant with 24x10G ports, 8x25G ports, and 2x100G ports is supported.

- CPM: cpm-ixr-e
- Linecard: imm24-sfp++8-sfp28+2-qsfp28

/// details | Example: a 7750 SR-2se with 2 IXR-e satellites
    type: example

The following resources showcase the creation of a 7750 host node that has two satellites attached to it.

- Both satellites are connected to the host system via a single 100G uplink port (port 33)
- On the host, the satellites are connected to ports 17 and 18
- Both satellites have 32 downlinks toward edge devices

/// details | The node resource
    type: info
```yaml
apiVersion: core.eda.nokia.com/v1
kind: TopoNode
metadata:
  labels:
    eda.nokia.com/role: leaf
    eda.nokia.com/security-profile: managed
  name: satellite-host
  namespace: bootstrap
spec:
  component:
    - kind: lineCard
      slot: '1'
      type: xcm-2se
    - kind: fabric
      slot: '1'
      type: sfm-2se
    - kind: mda
      slot: 1-a
      type: x2-s18-800g-qsfpdd
    - kind: connector
      slot: 1-a-1
      type: c10-10g
    - kind: connector
      slot: 1-a-2
      type: c10-10g
    - kind: connector
      slot: 1-a-3
      type: c10-10g
    - kind: connector
      slot: 1-a-4
      type: c10-10g
    - kind: connector
      slot: 1-a-16
      type: c1-100g
    - kind: connector
      slot: 1-a-17
      type: c1-100g
    - kind: connector
      slot: 1-a-18
      type: c1-100g
    - kind: powerShelf
      slot: '1'
      type: ps-a4-shelf-dc
    - kind: powerModule
      slot: 1-1,1-2
      type: ps-a-dc-6000
    - kind: powerModule
      slot: 1-3,1-4
      type: ps-a-dc-6000
  nodeProfile: sros-25.10.1
  npp:
    mode: normal
  operatingSystem: sros
  platform: 7750 SR-2se
  productionAddress: {}
  satelliteNodes:
    - components:
        - kind: lineCard
          slot: '1'
          type: imm24-sfp++8-sfp28+2-qsfp28
        - kind: controlCard
          slot: a
          type: cpm-ixr-e/imm24-sfp++8-sfp28+2-qsfp28
      id: '1'
      macAddress: '00:00:00:00:00:01'
      operatingSystem: sros
      platform: 7250 IXR-e
      portTemplate:
        connectors:
          - kind: connector
            slot: 1-33
            type: c1-100g
        name: satellite-port-template-1
        uplinks:
          - downlinks:
              - 1-1
              - 1-2
              - 1-3
              - 1-4
              - 1-5
              - 1-6
              - 1-7
              - 1-8
              - 1-9
              - 1-10
              - 1-11
              - 1-12
              - 1-13
              - 1-14
              - 1-15
              - 1-16
              - 1-17
              - 1-18
              - 1-19
              - 1-20
              - 1-21
              - 1-22
              - 1-23
              - 1-24
              - 1-25
              - 1-26
              - 1-27
              - 1-28
              - 1-29
              - 1-30
              - 1-31
              - 1-32
            name: 1-c33-u1
      satelliteProfile: sros-25.10.1-satellite
      type: es24-sfpp+8-sfp28+2-qsfp28
      uplinkInterfaces:
        - hostPort: ethernet-1-17-1
          satellite: 1-c33-u1
      version: 25.10.1
    - components:
        - kind: lineCard
          slot: '1'
          type: imm24-sfp++8-sfp28+2-qsfp28
        - kind: controlCard
          slot: a
          type: cpm-ixr-e/imm24-sfp++8-sfp28+2-qsfp28
      id: '2'
      macAddress: '00:00:00:00:00:02'
      operatingSystem: sros
      platform: 7250 IXR-e
      portTemplate:
        connectors:
          - kind: connector
            slot: 1-33
            type: c1-100g
        name: satellite-port-template-1
        uplinks:
          - downlinks:
              - 1-1
              - 1-2
              - 1-3
              - 1-4
              - 1-5
              - 1-6
              - 1-7
              - 1-8
              - 1-9
              - 1-10
              - 1-11
              - 1-12
              - 1-13
              - 1-14
              - 1-15
              - 1-16
              - 1-17
              - 1-18
              - 1-19
              - 1-20
              - 1-21
              - 1-22
              - 1-23
              - 1-24
              - 1-25
              - 1-26
              - 1-27
              - 1-28
              - 1-29
              - 1-30
              - 1-31
              - 1-32
            name: 1-c33-u1
      satelliteProfile: sros-25.10.1-satellite
      type: es24-sfpp+8-sfp28+2-qsfp28
      uplinkInterfaces:
        - hostPort: ethernet-1-18-1
          satellite: 1-c33-u1
      version: 25.10.1
  version: 25.10.1
```

///

/// details | The satellite profile resource
    type: info

```yaml
apiVersion: core.eda.nokia.com/v1
kind: SatelliteProfile
metadata:
  name: sros-25.10.1-satellite
  namespace: bootstrap
spec:
  containerImage: ...[fill in only if simulating nodes]...
  imagePullSecret: ...[fill in only if simulating nodes]...
  images:
    - image: ftp://user:pass@192.0.2.10/ixr/
  license: ...[fill in only if simulating nodes]...
  operatingSystem: sros
  version: 25.10.1
```

///

///

### Nokia 7210 SAS-S(x)

Both the `SAS-S` variant with 48x1G ports and 4x10G ports, and the `SAS-Sx` variant with 64x1/10G ports and 4x100G ports are supported.

- `SAS-S` type: es48-sass-1gb-sfp
- `SAS-Sx` type: es64-10gb-sfpp+4-100gb-qsfp28

/// note

The 7210 SAS platforms do not have a containerized image, and therefore cannot be simulated by EDA.
///

## Host uplinks

Uplink interfaces are the interfaces that connect the satellite to the node that manages it. Configuring a satellite port as an uplink has several implications for that port, and to distinguish them from client ports the letter `u` is used in the port name.

For example:

- Satellite port name `1/1/1` means that port 1 of the satellite is used as a client port
- Satellite port name `1/1/u1` means that port 1 of the satellite is configured as an uplink port, which significantly changes the inner workings of that port

For more information, including which ports can be configured as uplinks, refer to the SR OS satellite documentation.

## MAC address

The configured MAC address is used to validate that the correct satellite is being configured, and avoids sending configuration or software images to the wrong one.

## Upgrading satellites

Satellite nodes cannot currently be upgraded through EDA. To upgrade a satellite, update the `satelliteProfile` on the host `TopoNode` satellite declaration so that it points to the new software repository. After that, follow the SR OS satellite documentation for upgrade instructions.

## Dependencies

### `SatelliteProfile`

The satellite profile defines certain operational parameters for the satellite, including but not limited to:

- the location where the satellite OS images are stored
- the container image for the satellite (for simulating satellite containers)
- the container image license for the satellite

/// note

Only 7250 IXR satellites can be simulated at this time.

///

## Referenced resources

The `Satellite` resources does not reference any other EDA resource.

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
