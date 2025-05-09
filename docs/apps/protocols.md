# Protocols

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                                                                           |
| -------------------- | ----------------------------------------------------------------------------------------- |
| **Description**      | The Protocols application manages BGP, static, and aggregate route resources to automatically generate routing configurations for network nodes in both default and custom VRFs. |
| **Supported OS**     | SR Linux, SR OS                                                                           |
| **Catalog**          | [nokia-eda/catalog][catalog] / [manifest][manifest]                                                             |
| **Source Code**      | <small>coming soon</small>                                                                |

[catalog]: https://github.com/nokia-eda/catalog
[manifest]: https://github.com/nokia-eda/catalog/blob/main/vendors/nokia/apps/protocols/manifest.yaml

The Protocols application enables users to create and manage various routing protocols in EDA and contains resources that are split between Overlay and Default routing categories. These two categories define the deployment model for the resource.

Resources from the Default Routing category will be used in the network element's default VRF, whereas resources listed under the Overlay Routing category designed to be associated with a custom, non-default VRF.

The application provides the following components:

/// tab | Resource Types

<div class="grid" markdown>
<div markdown>
-{{icons.default_routing()}}-

* Default BGP Groups
* Default BGP Peers
* Default Static Routes
* Default Aggregate Routes
* Default Route Reflectors
* Default Route Reflector Clients

</div>
<div markdown>
-{{icons.overlay_routing()}}-

* BGP Groups
* BGP Peers
* Static Routes
* Aggregate Routes
* Route Reflectors
* Route Reflector Clients

</div>
</div>
///

/// tab | Dashboards
Summary dashboards for the following resource types:

* Default BGP Peers
* Default BGP Groups
* Default Route Reflectors
* Default Route Reflector Clients
///

## Border Gateway Protocol (BGP)

BGP configuration in the Protocols application supports both default VRF and custom VRF deployments, with comprehensive features for peer management, route reflection, and policy control.

### Configuration Types

The application supports two primary BGP deployment models:

* **Default BGP:** Configuration in the default VRF using `DefaultBGPPeer` and `DefaultBGPGroup` custom resources (CRs).
* **Custom VRF BGP:** Configuration in custom IP-VRFs using `BGPPeer` and `BGPGroup` CRs.

### BGP Groups

BGP Groups enable centralized management of peer configurations, ensuring consistent policy application across multiple peers.

Because a BGP group in the default VRF and custom VRF usually have different configuration options and represent different groups, two BGP groups resource types are offered - `DefaultBGPGroup` and `BGPGroup`.

#### Default BGP Group Configuration

-{{icons.default_routing()}}- → -{{icons.circle(letter="DG", text="Default BGP Group")}}-

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/defaultbgpgroup.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/defaultbgpgroup.yaml"
EOF
```

///

#### Custom VRF BGP Group Configuration

-{{icons.overlay_routing()}}- → -{{icons.circle(letter="BG", text="BGP Group")}}-

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/bgpgroup.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/bgpgroup.yaml"
EOF
```

///

### BGP Peers

BGP peers represent individual BGP sessions and can inherit configurations from BGP groups. The Protocols application supports both explicit peer configuration and dynamic neighbor discovery.  Selecting an interface will bind the session to the Toponode on which the Interface is deployed.  The interface can be a DefaultInterface (interface in the default VRF) or a SystemInterface (primary loopback in the default VRF).

#### Default BGP Peer Configuration

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/defaultbgppeer.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/defaultbgppeer.yaml"
EOF
```

///

#### Custom VRF BGP Peer Configuration

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/bgppeer.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/bgppeer.yaml"
EOF
```

///

### Address Family Support

The Protocols application provides comprehensive support for multiple BGP address families including, but not limited to:

#### IPv4 Unicast

* Enable/disable IPv4 unicast routing
* Support for IPv6 next-hops (RFC 5549)
* Configurable maximum route limits
* Next-hop self options
* Independent policy control

#### IPv6 Unicast

* Enable/disable IPv6 unicast routing
* Configurable maximum route limits
* Independent policy control

#### L2VPN EVPN

* Enable/disable EVPN
* Support for IPv6 next-hops
* Configurable maximum route limits
* Integration with overlay services

### Route Reflection

Route reflection enables scalable iBGP deployments by eliminating the need for a full mesh of iBGP sessions. The Protocols application supports route reflection in both default and custom VRFs.

The router reflector resources can select the clients to connect to using a label selector. The label selector will select RouteReflectorClient or DefaultRouteReflectorClient resources; if the clients are not EDA resources, you may specify a list of client IPs to which the the route reflector will attempt to establish a session.

#### Configuration Types

* **Default VRF:** Using `DefaultRouteReflector` and `DefaultRouteReflectorClient`.
* **Custom VRF:** Using `RouteReflector` and `RouteReflectorClient`.

#### Route Reflector Configuration

##### Default VRF Example

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/defaultroutereflector.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/defaultroutereflector.yaml"
EOF
```

///

##### Custom VRF Route Reflector Example

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/routereflector.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/routereflector.yaml"
EOF
```

///

#### Route Reflector Client Configuration

Route reflector clients establish sessions with route reflectors based on selectors or explicit IP addresses.  The label selector will select DefaultRouteReflector or RouteReflector resources, or a list of IP addresses can be provided which the router relctor client will try to establish a session to.

##### Default VRF Client Example

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/defaultroutereflectorclient.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/defaultroutereflectorclient.yaml"
EOF
```

///

##### Custom VRF Client Example

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/routereflectorclient.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/routereflectorclient.yaml"
EOF
```

///

## Static Routes

Static routes provide explicit path control for network traffic.

### Configuration Types

The application supports two types of static route deployments:

* **Default Static Routes:** Configuration in the default VRF using a `DefaultStaticRoute` resource.
* **Custom VRF Static Routes:** Configuration in custom VRFs using a `StaticRoute` resource.

### Default VRF Static Route Configuration

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/defaultstaticroute.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/defaultstaticroute.yaml"
EOF
```

///

### Custom VRF Static Route Configuration

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/staticroute.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/staticroute.yaml"
EOF
```

///

## Route Aggregation

Route aggregation enables efficient route summarization and management.

### Configuration Types

The application supports two types of route aggregation:

* **Default Aggregate Routes:** Configuration in the default VRF using a `DefaultAggregateRoute` resource.
* **Custom VRF Aggregate Routes:** Configuration in custom VRFs using an `AggregateRoute` resource.

### Default VRF Aggregate Route Configuration

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/defaultaggregateroute.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/defaultaggregateroute.yaml"
EOF
```

///

### Custom VRF Aggregate Route Configuration

/// tab | YAML

```yaml
--8<-- "docs/apps/protocols/aggregateroute.yaml"
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/protocols/aggregateroute.yaml"
EOF
```

///

## Operational State and Verification

### BGP Status

```shell
# Check BGP peer status
kubectl get bgppeers
NAME         SESSION STATE   LAST CHANGE   ENABLED   OPERATIONAL STATE   PEER AS
example-peer Established    10m           true      up                  65100

# Check BGP group status
kubectl get bgpgroups
NAME          LAST CHANGE   OPERATIONAL STATE
example-group 10m          up

# Check route reflector status
kubectl get routereflectors
NAME    LAST CHANGE   OPERATIONAL STATE   NUM RR BGP PEERS   NUM RR BGP PEERS DOWN
rr-1    10m          up                  4                  0
```

### Static Route Status

```shell
# Check static route status
kubectl get staticroutes
NAME          LAST CHANGE   OPERATIONAL STATE   HEALTH
custom-route  10m          up                  100
```

### Aggregate Route Status

```shell
# Check aggregate route status
kubectl get aggregateroutes
NAME             LAST CHANGE   OPERATIONAL STATE   HEALTH
customer-summary 10m          up                  100
```
