# Interfaces

-{{% import 'icons.html' as macros %}}-

| <nbsp> {: .hide-th } |                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------ |
| **Description**      | The interfaces application enables the configuration and management of network interfaces across your infrastructure, supporting various interface types including single interfaces, LAGs, and loopback interfaces. |
| **Supported OS**     | SR Linux, SR OS                                                                                        |
| **Catalog**          | [nokia-eda/catalog][catalog]                                                                           |
| **Source Code**      | <small>coming soon</small>                                                                             |

[catalog]: https://github.com/nokia-eda/catalog

The Interfaces application provides two resources - Interface and Breakout.

## Interface

-{{macros.topology_icon(text="TOPOLOGY")}}- → -{{macros.circle_icon(letter="I", text="Interface")}}-

The Interface resource declaratively defines abstracted network interfaces for the range of supported network operating systems and supports three primary interface types:

- **Standard Interface:** Individual physical interfaces
- **LAG (Link Aggregation Group):** Bundled interfaces operating as a single logical link
- **Loopback:** Virtual interfaces for management and routing purposes

### Basic Configuration Fields

In the basic scenario of configuring a simple interface the following basic configuration fields are typically set:

- **Type:** An interface type - `standard`, `lag` or `loopback`.
- **Members:** A list of objects where each object is a reference to a node name and its associated physical interface name.  
    The interface name is provided in the normalized way, non alphanumerical characters are replaced with `-` (dash). For example, original interface name `ethernet-1/13` becomes `ethernet-1-13`.
- **Enabled State:** Interfaces are enabled by default but can be explicitly disabled
- **Description:** Optional text description of the interface
- **MTU:** Maximum Transmission Unit (range: 1450-9500)

Add the metadata blob that includes the Interface resource **Name**, **Namespace** and **Labels**, and you get a valid EDA resource that you can apply, for example to your [Try EDA][try-eda] cluster.

[try-eda]: ../getting-started/try-eda.md

When applied, the resource presented below will create a simple physical network interface configuration on the supported network OS with the user-provided values and the resource defaults.

/// tab | YAML

```yaml title="basic Interface resource definition"
--8<-- "docs/apps/interfaces/simple-interface.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/interfaces/simple-interface.yaml"
EOF
```

///

### Interface Naming and Normalization

The Interface application employs a standardized, or normalized, format for interface names within its configurations. This approach ensures consistency when defining interfaces across diverse network operating systems (NOS). The system subsequently translates these normalized names into the specific format required by each target OS.

A key aspect of EDA's interface modeling is the use of normalized interface names. Typically, an OS-native interface name like `ethernet-1/13` is represented as `ethernet-1-13` in EDA configurations by replacing non-alphanumeric characters (like `/`) with a dash (`-`). This normalized name is then used by the system to derive the OS-specific interface identifier.

The following subsections detail how these normalized EDA interface names are translated for various supported operating systems, based on the underlying logic.

#### SR Linux

- Native interface name `ethernet-1/1` is normalized as `ethernet-1-1`.
- Breakout interfaces like `ethernet-1/1/1` become `ethernet-1-1-1`.
- Loopback interfaces such as `lo0` translate to `loopback-0`.
- LAG interfaces like `lag10` translate to `lag-10`.

#### SR OS

- Native port identifier `1/1/1` translates to `ethernet-1-a-1` name, where "a" is the first MDA on a 1st line card.
- The system supports more complex mappings for different hardware configurations:
    - Port `2/2/1` translates to `ethernet-2-b-1` (representing linecard 2, MDA "b"[^2], port 1).
    - Breakout (implicit MDA 1): `1/1/c1/1` translates to `ethernet-1-1-1`.
    - Breakout (explicit "a" for MDA 1): `1/1/c2/1` translates to `ethernet-1-a-2-1` (where MDA "a" maps to 1, and "2-1" defines the port as `c2/1`).
    - XIOM MDA: `1/x1/1/1` translates to `ethernet-1-1-a-1`.
- Loopback interfaces like `lo0` become `loopback-0`.
- LAG interfaces retain names like `lag-10`.

### Ethernet Configuration

The Interface application provides extensive Ethernet-specific configurations through the `ethernet` property, including:

- **Speed:** Interface speed (100G, 40G, 25G, 10G, 1G, etc.)
- **Forward Error Correction (FEC):** Various FEC modes (disabled, rs528, rs544, baser, rs108)
- **Timers:** Hold-up, hold-down, and reload delay timers
- **Storm Control:** Traffic rate limiting for broadcast, multicast, and unknown unicast
- **L2CP Protocol Transparency:** Configuration for tunneling various L2CP protocols

#### Storm Control Configuration

Storm control helps protect the network from traffic storms by setting rate limits:

/// tab | YAML

```yaml
--8<-- "docs/apps/interfaces/simple-interface-storm-control.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/interfaces/simple-interface-storm-control.yaml"
EOF
```

///

### LAG Configuration

Link Aggregation Groups (LAGs) provide link redundancy and increased bandwidth. The Interface application supports both regular/local LAGs (with static and LACP-based configurations) as well as ESI-based[^1] multihoming LAGs.

The following set of Interface objects is relevant for the LAG interface configuration:

- **Minimum Links:** Minimum required number of active links in a LAG to be operational
- **LACP Settings:** Mode, interval, system priority, and admin key
- **Multi-homing:** ESI configuration for multi-chassis operation

#### Example LAG Configuration

/// tab | YAML

```yaml
--8<-- "docs/apps/interfaces/simple-lag.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/interfaces/simple-lag.yaml"
EOF
```

///

### Multi-homing Support

The Interface application supports sophisticated multi-homing configurations for LAGs based on EVPN standard, enabling high availability and load balancing:

- **Modes:** all-active, single-active, or port-active
- **ESI:** Ethernet Segment Identifier configuration
- **Active Node Preference:** Preferred node selection for single-active scenarios
- **Revertive Behavior:** Controls failback behavior

#### Multi-homing Configuration Example

/// tab | YAML

```yaml
--8<-- "docs/apps/interfaces/simple-mh-lag.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF'  | kubectl apply -f -
--8<-- "docs/apps/interfaces/simple-mh-lag.yaml"
EOF
```

///

### Operational State

The Interface application maintains detailed operational state information, including:

- Administrative and operational status
- Interface speed
- Last state change timestamp
- Member status and neighbor discovery
- LAG-specific operational details

You can verify the interface operational state using:

```shell
kubectl -A get interfaces
```

<div class="embed-result">
```{.text .no-copy}
NAME               ENABLED   OPERATIONAL STATE   SPEED   LAST CHANGE   AGE
customer-facing    true      up                 100G    2m            10m
```
</div>

## Breakout

-{{macros.topology_icon(text="TOPOLOGY")}}- → -{{macros.circle_icon(letter="B", text="Breakout")}}-

The Breakout resource allows for the configuration of interface breakouts on specified Nodes. This resource specifies the Nodes, parent Interfaces, the number of breakout channels, and the speed of each channel.

### Configuration Fields

- **`node`**: A list of references to TopoNodes where the parent interfaces are to be broken out.
- **`interface`**: A list of normalized parent interface/port names to be broken out.
- **`channels`**: (Required) The number of breakout channels to create (integer, min: 1, max: 8).
- **`speed`**: (Required) The speed of each breakout channel. Supported speeds are: 800G, 400G, 200G, 100G, 50G, 40G, 25G, 10G.
- **`nodeSelector`**: An alternative way to specify the TopoNode(s) where the parent interfaces are to be broken out.

### Example Breakout Configuration

This example demonstrates how to configure a breakout port.

/// tab | YAML

```yaml
--8<-- "docs/apps/interfaces/simple-breakout.yaml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF'  | kubectl apply -f -
--8<-- "docs/apps/interfaces/simple-breakout.yaml"
EOF
```

///

[^1]: A standards-based alternative to proprietary Multi-chassis LAGs.
[^2]: Letter "b" means 2nd MDA.
