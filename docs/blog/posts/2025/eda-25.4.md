---
date: 2025-05-01
authors:
    - bwallis
tags:
    - release
---

# EDA 25.4

It is that time again :partying_face: The EDA product team are pleased to announce the release of EDA 25.4.1 :rocket:

The team have been hard at work; introducing our first non-SR Linux OS, a boatload of QoL UI improvements (bulk edits!), and a number of app extensions to cover additional use cases.

To some numbers! In this release we delivered **152 GA features**, 14 alpha features, and 90 beta features (I'll come back to this later).

<!-- more -->

Our big themes for this release were DX (or Developer Experience) and productizing SR OS as a first class citizen.

To look at DX first, with EDA 25.4 we are providing:

* Extensions to `edactl` to support intent debuggability (under edactl intent debug).
    This includes the ability to trigger instances of intents to run, with DEBUG toggled to allow more logging verbosity.

    It includes the ability to monitor execution of instances (including the immediate monitor + trigger). This massively improves intent debuggability, dumping any logs, subscriptions, inputs, and outputs your application received/emitted.

    For performance debugging, stats are provided for all execution of all intents, including number of executions and cumulative execution time.

* The [new `edabuilder` tool](../../../development/apps/index.md).

    Purposefully built for developing applications on EDA (intent-based or otherwise).  
    The initial focus of the tool is primarily to assist with the scaffolding/packaging/testing/publishing of an application, including its resources and intents.
    A [new section of documentation](../../../development/apps/index.md) dedicated to the above.

Now for **Nokia SR OS** - our first litmus test on our claims of supporting multiple operating systems. We are releasing this as **beta in EDA 25.4.1**, with the expectation that this graduates to GA in 25.8.1. The large number of beta features mentioned above relate to this.

You are free to try EDA with SR OS in a lab environment, with most apps already providing support.

There are minor gaps in app coverage for SR OS (upgrades are not supported for example), but you should find coverage for the common use cases we support SR Linux for, including:

* ZTP (including component configuration)
* Underlay via the Fabric resource and its dependencies.
* Overlay via the VirtualNetwork resource and its dependencies.
* The surrounding set of policies/profiles in filters, QoS, routing policies, and almost everything else.
* Queries with EQL, including natural language.  
    Use `sros:` as a prefix to force a query to only SR OS devices.
* Normalization of all state data, including overlays (CPU, memory, disk).
* Lots, lots more.

This covers SR OS both as a DC GW (using option A), and as any of the roles used by SR Linux today - leaf, spine, superspine.

/// admonition | Supported SR OS releases
    type: subtle-note
You must use SR OS 24.10R4 or above, or 25.3R2 or above.
///

For now you must run SR OS nodes in containerlab, or interact with real hardware in your physical lab.

Beyond these themes you'll find new overlays, extensions to our integrations with Prometheus, ServiceNow, PagerDuty, and NetBox, and enhancements in our integration with OpenStack.

You'll also (if you're paying attention) notice huge speed improvements in transactions and general scale improvements at scale. We were already blazing fast here (deploying scaled fabrics in seconds) but we have managed to squeeze a measly 10x improvement in some intent apps, with most seeing somewhere in the 5-8x range.

With that said, onwards!

If you aren't there yet, join the EDA Discord server: https://eda.dev/discord.

<small>with :heart: from the EDA product team</small>
