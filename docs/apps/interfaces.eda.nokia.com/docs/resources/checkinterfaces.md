---
resource_name: CheckInterfaces
resource_name_plural: checkinterfacess
resource_name_plural_title: Check Interfaces
resource_name_acronym: CI
crd_path: docs/apps/interfaces.eda.nokia.com/crds/interfaces.eda.nokia.com_checkinterfacess.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Check Interfaces

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The `CheckInterfaces` workflow is used to check the health of [`Interfaces`](interface.md). It loops over all nodes selected by the `nodeSelectors` and `nodes` properties, and checks every interface that matches the label(s) specified in the `interfaceSelectors` property.

## Checks

By default, the workflow checks that all members of all selected [`Interfaces`](interface.md) are operationally up. Additional checks can be run against the counters of each interface. Each check monitors a particular metric for `waitTimeSeconds` seconds and fails if the timer has increased during this window. 

Unless explicitly mentioned, these checks are only supported on Nokia SR Linux and SR OS.

- `EthernetCRC`: checks if any CRC error frames were received 
- `EthernetFrameSize`: checks for oversized, undersized (< 64 bytes), and jabber (oversized with bad CRC) frames received on the interface
- `EthernetPauseFrames`: checks for received pause frames that indicate congestion
- `CarrierTransitions`: checks whether the link is "flapping"
- `DiscardedPackets`: checks whether packets were discarded on ingress or egress
- `TransceiverHealth`: checks whether the transceiver has reset during the time window
- `LACPErrors`: checks for any errors reported through the Link Aggregation Control Protocol (LACP)
- `IfPacketErrors`: checks for packet errors both in the ingress and egress direction

## Dependencies

The `CheckInterfaces` workflow does not depend on any other resources.

## Referenced resources

### `TopoNode`

The workflow selects nodes that it will check interfaces on through the `nodeSelectors` and `nodes` properties. 

!!! note

    Only interfaces that have a matching [`Interface`](interface.md) will be checked.

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