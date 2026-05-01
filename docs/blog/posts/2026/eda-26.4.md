---
date: 2026-04-30
authors:
    - bwallis
tags:
    - release
---

# EDA 26.4

It feels like releasing 25.12 was just a hop, skip, and jump ago :sweat:, but we are back again with another major EDA release - the EDA product team are pleased to announce the release of **EDA 26.4.1** :rocket::rocket::rocket:!

Being the first major release of 2026, and us having a longer six month development cycle, this release is jam-packed with shiny new capabilities for you to try. PLMs have been feverishly PRD (and CRD) writing, devs have been unremittingly coding, and testers have been aptly automating (yep I found my thesaurus). By the numbers we're introducing {==182 new generally available features==} into EDA, alongside an additional 40 beta features, and 25 alpha features.

This vast array of new features demands a deep dive, which we absolutely plan to provide in the coming weeks. For now, let's have a cursory look at what this release packs.

<!-- more -->

-{{image(url="../graphics/26-4-banner.webp", shadow=true, padding=20)}}-

Our theme for this release was **AIOps** and **CI/CD** - but there's so many goodies that need to be called out.

## AI Ops

Starting with AIOps - this release marks the first publicly-consumable version of [**Ask EDA**](../../../user-guide/ask-eda.md) :robot:!  
It was over eight months ago at SReXperts that we demonstrated interactions with EDA using conversational natural language, and you're now free to try this for yourselves.  
Root cause alarms, run pings, describe transactions, and design dashboards, all via the power of LLMs. We're marking use with OpenAI ChatGPT as GA, with support for Google Gemini and xAI Grok released as beta. The new [`Provider`](https://crd.eda.dev/providers.ai.core.eda.nokia.com/v1) resource allows you to customize what models and APIs are used for interactions with the LLM, and is your likely starting point. We're also releasing pre-baked `Provider` resources packaged as applications in the new OpenAI, Gemini, and xAI applications you'll find in your app store. Simply install the app of your choice, and provide your API key to get started.

> A small note that you will need OpenAI for embeddings even if you use one of the other providers as your main chat provider - we plan on removing this restriction at a later date.

Alongside AskEDA this release also brings the **EDA MCP server** (I have a note here that says this is the best MCP server you will ever use). Using off the shelf MCP clients EDA now provides a native MCP interface and in true EDA fashion this supports an extensible resource-driven model for adding tools and capabilities without us needing core revisions. Pick up your favorite MCP client and kick the tires. Documentation for this will follow over the next couple of days.

## CI/CD

On the CI/CD front, this release introduces [**merge requests**](../../../user-guide/merge-requests.md) and [**branches**](../../../user-guide/branches.md) - our first true digital-twin-enabled production use case.

Starting with merge requests, these function very similarly to git-style merge or pull requests - they allow you to stage a batch of changes, validate them, and then trigger a request to EDA to merge them. This allows staging of work before maintenance windows, and creates a new class of user in EDA that may propose changes, but may not merge them. This capability will be extended in upcoming releases to allow a clean approval workflow.

As for branches - these are EDA-managed EDA clusters that are synchronized with the main cluster, and act as sandboxes (with simulated devices) to experiment with changes before they are merged into production.  
Cleanly integrated into the UI, you're able to create branches using the new [`Branch`](https://crd.eda.dev/branches.core.eda.nokia.com/v1) resource, navigate into the branch (which has its own UI and surrounding EDA services), make changes, before generating a merge request back to the main cluster. Branches support the use of virtual clusters, allowing common Kubernetes infrastructure to support as many branches as resources will allow. We're also introducing the [`ClusterProvider`](https://crd.eda.dev/clusterproviders.core.eda.nokia.com/v1) resource, allowing you to run branches on any remote Kubernetes cluster.

## Bulk resource changes

As another major point to call out ({==and a bit of a warning==}), this release packs in version updates to the vast majority of non-core resources in EDA, with styling changes to provide more consistent and clearer field names.  
As you'd expect these changes are made for you on upgrade, and edactl has support for migrating on-disk resources using the new `edactl platform upgrade convert` command.

> Read [the blog post](styling-changes.md) describing these changes in more detail, and if you have API integrations with EDA you'll need make the necessary changes to them.

## Multi-vendor

This release also provides limited availability support for **Arista EOS** (including simulations inside our CX digital twin). A limited set of apps are available at the moment - please see [release notes](https://documentation.nokia.com/aces/cgi-bin/dbaccessfilename.cgi/3HE304450001TQZZA_V1_Event-Driven%20Automation%2026.4.1%20Release%20Notes.pdf).

## Edactl

The all-so-powerfule [`edactl`](../../../user-guide/command-line-tools.md#edactl) CLI tool has finally been made available outside of the EDA Toolbox pod. What this means for you is

- you can now pretty much abandon the `kubectl` and embrace transaction-based resource management with `edactl`
- leverage the shell completions without the hassle and get back the joy of tab completion
- explore the sheer command set that `edactl` has to offer, from the simple-yet-powerful resource management, to the nodes config exploration, synthetic traffic testing, workflow execution, and many, many more.

The revamped [Command line tools](../../../user-guide/command-line-tools.md) documentation section tells you all you need to know about `edactl`, and other CLI tools in the EDA ecosystem.

## AI Docs

With the revamped documentation site and the aggregation of all the documentation articles into a single, unified source - docs.eda.dev - we also took the opportunity to bring you the **AI Docs assistant**. As EDA spans so many different knowledge domains and use cases, it's not a small feat to navigate the documentation set and find the information you need without some artificial intelligence to give you a digital hand.

By clicking the "magic dust" icon in the top bar you'll summon a chatbot that is going to try its best to answer your question in a conversational manner with direct links to the relevant documentation articles it has based its answer on. The full documentation set and our CRD reference documentation are all indexed and available for search.

-{{image(url="../graphics/kapa-icon.webp", shadow=true, padding=20, scale=0.8)}}-

> When using the AI Docs assistant, please smash that :material-thumbs-up-down-outline: button to help us improve the documentation set by giving us feedback on the quality of the answers.

## App docs

Staying with docs for a little longer, we've started to add [application documentation](../../../apps/index.md) to the docs.eda.dev site as well as providing them in the EDA UI. Synchronized, versioned, searchable, and air-gap friendly.  
You will notice that many applications have just a placeholder documentation page at the moment - we're working to get more of them up to speed with the rest of the documentation set.

Now on every resource group page you'll find the "Go to documentation" link hidden under the ellipsis menu. Yeah, we hid it well.

-{{image(url="../graphics/in-cluster-docs.webp", shadow=true, padding=20, scale=0.8)}}-

## Alarm policies

Alarms are funny. Everyone wants as many of them supported as possible, but everyone wants to suppress/clear them as soon as possible. This release introduces [**alarm policies**](../../../user-guide/alarms.md#alarm-policies) - a new way to manage alarms lifecycle. All in the same declarative paradigm, naturally.

## MPLS

The first foray into MPLS support - you're now able to use LDP in the underlay alongside IPVPN services to enable easier automation of DC GWs. We've also introduced the [`RouterInterconnect`](../../../apps/services.eda.nokia.com/docs/resources/routerinterconnect.md) and [`BridgeDomainInterconnect`](../../../apps/services.eda.nokia.com/docs/resources/bridgedomaininterconnect.md) resources to allow you to easily stitch services at the DC GW across the WAN.

## Nutanix

In the cloud connect domain, we added the [Nutanix Prism Central](../../../apps/connect/nutanix/index.md) plugin. This extends the range of connected platforms to include the most popular virtualization and orchestration platforms.

## Micro segmentation

We started to roll out the support for [Micro segmentation](../../../apps/microsegmentation.eda.nokia.com/docs/index.md) with the initial Beta release for a standalone application enabling micro segmentation policies to be applied to the network.

This first release focuses on the task of configuring micro segmentation - expect additions in upcoming releases to provide a more visual approach to constructing your policies.

## And many more...

- The login screen has had a refresh, including better support for dark mode.
- An alarm overlay is now available with topologies.
- Speaking of topologies. Edge links are now visualized.
- Lots of improvements to `edabuilder` with a big announcement planned for 26.8. Hang tight!
- We now support all 7750 SR hardware - no more checking if a certain platform is supported.
- You can now [preview](../../../user-guide/resources.md#label-selector-previews) items matched by a label selector in forms.
- Satellites are now supported with 7750 SR/SR OS.
- Enhancements to our AIFabric app supporting more flexible allocation modes, and support for untagged interfaces.
- More management services and AAA configurable.

> What is your favorite feature? Share it with us on [Discord](https://eda.dev/discord)!

Enough reading - time to give this features a good spin!

<small markdown>with :heart: from the EDA product team</small>
