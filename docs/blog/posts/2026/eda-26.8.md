---
date: 2026-08-27
authors:
    - bwallis
tags:
    - release
---

# EDA 26.8

The cycle continues - we are back again with another major EDA release. The EDA product team are pleased to announce the release of **EDA 26.8.1** :rocket::rocket::rocket:!

On time (as usual), a new slew of product capabilities are now available for you to sink your teeth into. By the numbers we're introducing {==183 new generally available features==} into EDA (that's one more than last release for those of you keeping count), alongside an additional 17 alpha/beta features.

We dusted off the manifesto and focused again this release on **reliable change** - completing the "CI/CD for infrastructure" story we've been rambling on about for what seems like an eternity with our new PipelineEngine, and extensions to merge requests.

<!-- more -->

## Pipelines

Let's dive right in and talk about [**pipelines**](../../../user-guide/pipelines.md). For those of you familiar with GitHub Actions or GitLab pipelines you're going to be right at home, and for those of you not familiar, don't worry; the fire is on and the hearth is warm. Pipelines are all around automating pre- and post-checks at a change boundary. Never again get confused about the difference between an active BGP peer and an established one - pipelines have you covered. Integrated seamlessly with our transactional model, you're now able to define per-GVK (or even per-field per-GVK) checks, allowing you to codify your MoPs and quash another avenue for human error. Pipelines also become the medium for sequencing a set of changes - with the predominant use case being upgrades of devices. We're still shipping the `DeployImage` workflow, but you'll see it paired with the new [`DeployImagePipeline`](../../../user-guide/administration/image-management.md) workflow that takes the concept and makes it much more flexible - handing over the set of things that matter to check to the user with a simplified framework. Define your triggers and jobs using the new `PipelineDefinition`, set, and forget.

## Merge requests

On the [merge request](../../../user-guide/merge-requests.md) front, we've added new capabilities to allow system administrators to require mandatory approvals, with additional optional restrictions on the author of the MR. This embraces the second-eye philosophy popularized via code reviews, providing a structure to mandate its implementation. We've also added a minor feature allowing you to mark MRs as draft, signaling to others that you're not quite ready yet, and preventing an in-progress MR from being merged.

## AskEDA and authentication

Alongside externally-visible capabilities, we've also conducted some brain surgery on how [AskEDA](../../../user-guide/ask-eda.md) routes queries, and how we authenticate user requests in the system. One of these you'll hopefully notice - the hit rate of AskEDA should perceptibly go up, and it'll be able to recover if it gets a course of action wrong initially. The other, hopefully not - up until now we've performed authentication and authorization at the API server, but we've now moved this into the various underlying gRPC endpoints, now that we have a large number of client-consumable gRPC capabilities (AskEDA being one of them). This moves our security perimeter into the services themselves, which has allowed us to remove the restriction limiting AskEDA to just admin-level users - any user should now be able to use AskEDA and have it operate using their set of permissions.

On the security front, we now also sign applications - you'll see new targets in the playground relating to this (especially if you're upgrading).

## ClientEngine

In other areas, this release also marks the preview release of our [**ClientEngine**](../../../user-guide/client-engine.md). This is our nomenclature for endpoints attached to the network - we are now capable of streaming ARP/ND from the network, and various endpoint information from our Connect plugins to give you VM/container/general client awareness, no matter where your clients might be attached. This infrastructure is pluggable, so expect us to add more client providers in the future.

## Apps

On the apps front, there's almost too much to list. You're now able to deploy AI fabrics using EVPN + VXLAN, and why not turn on DLB while you're there. Fabrics have a new protocol for you to play around with if you're so inclined, with the introduction of IS-IS for underlay (and overlay too!). We now generate alarms if your LLDP state doesn't match your defined topology, and SR-MPLS w/ IS-IS is available for all your DC-GW needs.

Obviously this only covers a subset of a subset - please read the release notes.

In other news, application documentation has had a major rework, with docs now existing for almost all resources.

As always don't be shy to provide your feedback on any of the above, or anything else that tickles your fancy.

## Resources

Now for follow-up resources.

- [Release notes](https://documentation.nokia.com/aces/cgi-bin/dbaccessfilename.cgi/3HE304450001TQZZA_V1_Event-Driven%20Automation%2026.4.1%20Release%20Notes.pdf) are now available for 26.8.1.
- The doc set at [docs.eda.dev](https://docs.eda.dev/) has been updated.
- A new set of 26.8 images has been pushed to the GitHub container registry, freely available for anyone who wants to get a taste of automation nirvana, with [Try EDA](../../../getting-started/try-eda.md) being updated to use them.
- I'll add a shameless plug for Discord again - you can join us via the invite link at [eda.dev/discord](https://eda.dev/discord) - please share this link with your friends, family, pets, and even people you don't like - it's open to anyone.
    - If you're a customer of EDA please reach out to get an appropriate role.

Enough reading - head on over to [docs.eda.dev](https://docs.eda.dev) to get started.

<small markdown>with :heart: from the EDA product team</small>
