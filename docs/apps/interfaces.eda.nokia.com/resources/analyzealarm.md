---
resource_name: AnalyzeAlarm
resource_name_plural: analyzealarms
resource_name_plural_title: Analyze Alarms
resource_name_acronym: AA
crd_path: docs/apps/interfaces.eda.nokia.com/crds/interfaces.eda.nokia.com_analyzealarms.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Analyze Alarm

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

This workflow is used for AIOps purposes, and provides a tool for the AI to diagnose interface alarms. The workflow takes as input the name of an alarm, and looks for the [`Interface`](interface.md) that is linked to it. When found, the workflow looks for any `TopoLink` resources that include this `Interface`, and checks for any alarm on the other end of the `TopoLink`. 

This is useful in cases where an interface is down because of a problem on the remote end. For example, the link between nodes `A` and `B` may be disabled due to excessive packet errors received by the interface on `B`, which may be caused by a faulty transceiver. In this scenario, `A` would not have an idea as to why the interface is operationally down. The workflow allows an AI to reason as to why this interface is down, if both ends of the link are managed by EDA.

## Dependencies

The `AnalyzeAlarm` workflow has no strict dependencies on any EDA resources. If an alarm with the provided `alarmName` does not exist, it completes gracefully.

## Referenced resources

No resources are referenced by the `AnalyzeAlarm` workflow.

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-