---
resource_name: PolicyDeployment
resource_name_plural: policydeployments
resource_name_plural_title: Policy Deployments
resource_name_acronym: PD
crd_path: docs/apps/qos.eda.nokia.com/crds/qos.eda.nokia.com_policydeployments.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Policy Deployment

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

??? abstract "A brief introduction to QoS"

    Quality of Service (QoS) is a set of technologies and mechanisms used to manage traffic prioritization, often but not exclusively used in scenarios of network congestion. A full explanation of QoS is beyond the scope of this documentation, as the concepts are often as complex as the implementation of them on various network operating systems, along with chip-specific capabilities and limitations.

The `PolicyDeployment` is a resource that configures [`IngressPolicies`](./ingresspolicy.md) and [`EgressPolicies`](./egresspolicy.md) on a node. It specifies which interfaces follow a particular QoS policy. For example, some interfaces could be connected to a "premium" service without traffic [policers](./ingresspolicy.md#policing), while non-premium users have bandwidth restrictions. The `PolicyDeployment` decides which interfaces follow which rules.

!!! warning "Interface types"

    Some hardware platforms like SR OS have different QoS capabilities for network ports (connected to other routers) compared to access ports. The `PolicyDeployment` resource only supports QoS policies for access interfaces. The `interfaceType` parameter is ignored for now.

## PolicyDeployment vs PolicyAttachment

Some parameters like the [queue mapping](./egresspolicy.md#forwarding-class-mapping) are configured for all subinterfaces on the interface: this is done by the `PolicyDeployment` resource. 

Other parameters such as [rewrite policies](./egresspolicy.md#rewrite-policies) and [classifiers](./ingresspolicy.md#classification) are configured on the sub-interface level: this is done by the [`PolicyAttachment`](./policyattachment.md).

A [`PolicyAttachment`](./policyattachment.md) automatically emits a `PolicyDeployment` as a derived resource. 

## Dependencies

### [`IngressPolicy`](./ingresspolicy.md)

The `PolicyDeployment` deploys QoS policies onto a node. If [`IngressPolicies`](./ingresspolicy.md) are used, these must be created first.

### [`EgressPolicy`](./egresspolicy.md)

The `PolicyDeployment` deploys QoS policies onto a node. If [`EgressPolicies`](./egresspolicy.md) are used, these must be created first.

## Referenced resources

The `PolicyDeployment` does not reference any other EDA resources.

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
