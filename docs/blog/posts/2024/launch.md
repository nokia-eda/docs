---
date: 2024-12-12
authors:
    - bwallis
tags:
    - media
    - nfd
---

# The beginning of an ~~era~~ EDA

<div class="grid" markdown>
<div markdown>
Today marks a huge milestone. You may have heard us talking about "EDA" at several public events - now you get to experience it for yourself.

It was a mere 24 months ago that we started the initial design for a next generation controller, which eventually adopted the codename EDA - Event Driven Automation.

Our goals were lofty; intents without inflexibility, simplified consumption of streaming telemetry, multi vendor, multi domain, CI/CD, pipelines, all encompassing revision control, all built for the modern tooling era.

Did we succeed? You get to be the judge!

</div>

<figure markdown>
  ![img](../../../images/eda.svg)
</figure>

</div>

<!-- more -->

## EDA?

If you've never heard of EDA before there is no better place to start than checking out the [NFD special](https://techfieldday.com/event/nfdxnokia24/) dedicated to this next generation automation controller.

Before diving into the technical details, we wanted to share a bit about our motivations. What problems we saw unsolved and how we saw EDA as a solution, and the world of declarative abstractions.

-{{youtube(url='https://www.youtube.com/embed/aNOyAz5A1Sw')}}-

What you will notice when reading through this engineering documentation portal is that we always try to put a demo behind the concepts we are describing. Our NFD appearance was not an exception - after explaining the design goals, drawing out the problem space and telling you how we think EDA is fit to solve them, we did a live demo of EDA in action.

How to deploy the whole fabric config in a network-wide transaction over a fleet of devices using declarative abstractions? How declarative abstractions can be nested and composed? How leveraging modeled network management interfaces can guarantee safety and reliability when used in conjunction with a transaction model?
This is all waiting for you in the next video:

-{{youtube(url='https://www.youtube.com/embed/qaMoBUBdUJU')}}-

After covering the configuration aspects of EDA we switch to _state_. What exactly do we mean by saying that abstractions should not only be for configuration, but also for state? How having state and configuration together can help operations? What would it look like to have a query language for your whole network, both for config and state?  
And lastly, if you came for AI bits - this video is for you!

-{{youtube(url='https://www.youtube.com/embed/PIw9CohK-4k')}}-

## Try EDA

The NFD videos are a great introduction to the concepts behind EDA, and it is highly likely we target the same problems you face with existing automation software. In that case, you would presumably willing to book an EDA demo...  
While booking a demo is absolutely possible, we are confident that you'll be able to recognize the value of EDA by running it in your own environment and on your own terms.

And with that said. the team[^1] is immensely proud to share EDA's first **public** release tagged with `24.12.1` version. This release is available for everyone to enjoy without a license and is available for download from the public GitHub container registry. No, really - no pay walls or registration walls.

<p align="center" markdown>
[Try EDA](../../../getting-started/try-eda.md){ .md-button .md-button--primary }
</p>

We're excited to see the yet-unimagined ways you'll use the framework to solve interesting automation problems.

## Community

EDA is a framework that allows users to create their own automation journey by creating custom abstractions, CI/CD workflows, composable UI dashboards, and applications that can be shared with the community. We wholeheartedly believe that the automation flourishes when it is open, collaborative, and accessible to everyone.

As with SR Linux, we host our community Discord server and invite everyone to join us as we push the boundaries of what is possible with automation.

<p align="center" markdown>
[:fontawesome-brands-discord: Join EDA Discord](https://eda.dev/discord){ .md-button .md-button--primary }
</p>

[^1]: From the EDA development, test, and product management teams.
