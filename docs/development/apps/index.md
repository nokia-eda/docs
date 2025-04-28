# There's an app for that

EDA is all about extensibility, and the packaging of this extensibility is referred to as an "app".

/// admonition | What's an app again?
    type: subtle-note
If you need a refresher on what an app is, check out [apps](../../apps/app-store.md).
///

With base configuration your EDA cluster points to an app catalog supplied by Nokia. This gives you access to official Nokia-supported applications, including upgrades via the EDA store. If you're anything like us you have your own opinions about how you'd like to solve your automation problems! This is where building your own app comes in.

Apps in general let you:

* Template inputs to resources within your cluster.  
    Have strong opinions about how your users interact with resources - set defaults, enforce constraints, and provide a consistent user experience.
* Define your own inputs, and the execution logic that should run in response to those inputs.  
    Generate configuration for targets, respond to telemetry events, trigger workflows, and much, much more.
* Generate alarms, normalize telemetry data.
* Define your own dashboards and other UI visualizations.
* Define your own workflows - one-shot operations that you'd like to expose to your users.

An application may consist of one or more of these components, or none of them!

## Why build on EDA?

You've likely used other infrastructure automation tools before, and you may be wondering why you should build on EDA. Here are a few reasons:

* EDA operates on a deterministic, declarative, abstracted, and event-driven model.  
    This means that you can define the state you want your infrastructure to be in, and EDA will take care of making sure it gets there. No more handling deltas or worrying about order of operations. This massively simplifies application logic - given a certain input what would you like the output to be?
* Built for all your state streaming needs.
    Simply define the set of things you'd like to monitor, and what you'd like to have happen on any updates. EDA takes care of subscriptions, and event triggers for you, providing a generic means to raise alarms, publish status of infrastructure, and normalize telemetry data.
* EDA is built on top of Kubernetes, which means you get all the benefits of Kubernetes - scalability, reliability, and a rich ecosystem of tools.
* And all of this comes with the multivendor capabilities.

## Development workflow

In its simplest form, an app builders workflow consists of the following steps:

* Define the resources you want to handle - the abstractions or inputs you expect your users to provide.
* Define the logic you need - the scripts (or sometimes referred to as intents) that will run in response to changes in those resources. These scripts are written in Python[^1].
* Define the relationships between the above - what logic is triggered by what resources.

In its more advanced form you may:

* Write Kubernetes-controller style apps, which are a bit more complex, but also more powerful.  
    This effectively lets you build and package your own Kubernetes controllers, which can be used to manage any Kubernetes resource, or any EDA resource.
* Define any views required - the dashboards that will display the state of your resources, or any other information you want to expose or visualize.
* Define the workflows you need - the one-shot operations that you want your users to be able to perform. Think ping, upgrade, verify, etc.

## Next steps

[:octicons-arrow-right-24: Setup the dev environment](setup-env.md)

[^1]: [MicroPython](https://micropython.org/) to be precise. We will explain why MicroPython in later sections.
