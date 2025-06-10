---
date: 2025-06-10
comments: true
authors:
    - rdodin
---

# 150 minutes of EDA

A week ago we gathered for the 20th time with our partners and customers to share our vision for the future of networking. The sunny Tarragona hosted our **SReXperts EMEA 2025** and it was a blast. Many after-event social media postings[^1][^2][^3] can give you a taste of the event.

It was also the first time we hosted the EDA hackathon for the lucky hundred participants who were there with us on the first day to learn about the product and later solve some challenges we carefully outlined on the https://hack.srexperts.net website.

It was great to see so many people getting engaged and excited about the possibilities EDA brings to the industry and getting the most out of the practical exercises.

Yet, we understand that not everyone could make it to the event, and that's why we've decided to share the theoretical part of the hackathon with the community, as we believe in the power of knowledge sharing and collaboration.

<!-- more -->

When introducing EDA to the community, we wanted to cut it close to the wire and mix the slides with real demos. In fact, we had eight demos flawlessly executed from the stage as we were introducing the concepts to the audience.

Once I landed from Tarragona, I started to slice the single stream into topics, and this resulted in seven parts, each with a clear message and scope. We hope you enjoy the content and find it useful, as we had a lot of fun preparing it.

> Don't forget to join [our Discord](https://eda.dev/discord) if you want to connect with us and learn more.

## Building on K8s and "Try EDA"

Nokia EDA uses Kubernetes not only as a universal deployment platform that enables high availability and horizontal scaling, but also brings the Kubernetes Resource Model concepts to networking to ensure declarative configuration of resources.

In Part 1 we explore the benefits of using Kubernetes as a platform for infrastructure and network automation and explain how to make use of the "Try EDA" installation that brings the full-fledged EDA setup with a Digital Twin and a small DC pod on the side.

-{{youtube(url="https://www.youtube.com/embed/T1lEP-kZCOM ")}}-

## Declarative Abstractions, Labels, and Allocation Pools

The networking industry has pretty much converged on the benefits that abstractions bring to the table. Instead of exposing dozens of nerd knobs, we tend to create business-critical and user-friendly abstractions. Couple the abstracted input with declarative principles and you get a modern and simple network management solution. But simple is hard.

In Part 2 we present the core concepts of EDA, starting with Declarative Abstractions. All EDA resources (Interface, BGP Peer, Static Route, etc.) are declarative and abstract. This concept underpins the simplicity and multivendor design principles we strive to offer to users.

Next, we introduce the two ways a user can select and reference resources in EDA - by name or labels. The label-based selection plays a key role in automation at scale, where the mapping is done implicitly by dereferencing objects with a given label set.

At the end of this part we talk about Allocation Pools, a concept that allows users to reliably manage resources such as indices, IP addresses, ASNs and so on.

-{{youtube(url="https://www.youtube.com/embed/a7j_xKz7XhI")}}-

## Building an EVPN VXLAN Fabric

The concepts introduced in Part 2 https://youtu.be/a7j_xKz7XhI enable EDA users to declaratively build and manage complex networks by offering simple and abstracted input.

Take an EVPN VXLAN fabric, for instance. To build an EVPN VXLAN fabric one needs to sort out things like underlay addressing, BGP peer configuration, ASN assignments, ACL policy creation, overlay protocol setup and many other adjacent tasks.

A perfect task for an abstracted intent, don't you think? This is exactly our plan for this part where we build a fabric across our topology by providing the bare minimum configuration input, and the system takes care of the rest.

-{{youtube(url="https://www.youtube.com/embed/Q89hw05moX8")}}-

## Network-wide Transactions and Deviations

With great power comes great responsibility. Performing automation at scale without having reliability built-in is a recipe for a massive outage. With Nokia EDA you get best-in-class network-wide transaction support where a configuration change undergoes a set of checks:

- syntax check
- schema validation
- dependency check
- node-based check

And if any of the checks fail, the whole transaction reverts to ensure that you don't have partially rolled out configuration. Worry-free configuration push on Friday is closer than you might think.

-{{youtube(url="https://www.youtube.com/embed/AGf9pCIS6LE")}}-

## Network State and Query Language

In the DIY world of network automation we have a peculiar split - we perform configuration management with one set of tools (terraform, ansible, scrapli, napalm) and we deal with the network state using a completely different set of tools (zabbix, grafana, librenms).

This severance does not do justice for operations, though, asking the NOC teams to correlate raw state metrics with the deployed services. How do you know if your service for a particular tenant is running?

Things are different in the EDA realm where any given resource submitted to EDA has a corresponding state reported for it. If you configured the Fabric in part 3, you know that even this composite abstraction has a state associated with it. Knowing the health score of your Fabric gives you clear visibility into its performance and reduces the complexity in day 2+ operations.

Besides having the state of the resources, we bring you the real-time, distributed and network-wide query language that runs across all your network with blazing fast performance. Do you want to find that rogue MAC in your DC fabric? You can, even with natural language support.

Operations are often neglected in DIY solutions, and we are set to change that.

-{{youtube(url="https://www.youtube.com/embed/VNwhqJtgGjM")}}-

## Building Virtual Networks

As we start with datacenter automation, one of the prime-time automation activities is creating overlay networks on top of the EVPN VXLAN fabric.

Again, building on top of declarative abstraction principles, we offer you a range of resources to help achieve your goal. Do you need a layer 2 network? Take the Bridge Domain resource. Want to create a layer 3 network? Use the Router resource. Combine the two with the IRB Interface resource and you get a distributed L2/3 network.

On top of that you can create Routed Interfaces and set up BGP Peers on them to break out from your datacenter and achieve external connectivity.

The reusability of abstracted components in EDA makes it easy to mix and match and build tailored network designs without compromising the declarative principles.

-{{youtube(url="https://www.youtube.com/embed/dWP2wtQhbDY")}}-

## Automation and Extensibility

Not API-first, but API-only. EDA lives and breathes APIs and we hope you will appreciate our strong focus on automation. Everything you can do via EDA UI is possible to achieve with any REST API client, as EDA UI is just a client of the API.

But API alone is not enough to ensure you get the best out of the platform. EDA, like Kubernetes, is a platform to build upon, and we can't wait to see what you will build on it. To support you in this endeavor we offer developer experience tools like EDABuilder to help you build and package EDA apps.

Oh yes, apps - everything in EDA is an app and you can fork, edit an existing one or build your own app. Abstracting the provided abstractions? Possible.

To ensure your applications can be discovered and managed we implemented the EDA Store - a component that discovers applications from catalogs. You can publish your apps to your own catalog and make EDA watch it and discover apps from it. Lots of options to offer you full flexibility in how you create, host and distribute EDA apps.

-{{youtube(url="https://www.youtube.com/embed/920ZFoEKmhE")}}-

[^1]: https://www.linkedin.com/feed/update/urn:li:activity:7337432794446393344/
[^2]: https://www.linkedin.com/posts/vach-kompella-75846_nokia-srexperts-evpn-activity-7241886104923037696-T8IJ
[^3]: https://www.linkedin.com/posts/rdodin_autocon3-srexperts2025-containerlab-activity-7336793194862411778-QhtC
