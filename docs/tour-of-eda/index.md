# The Tour of EDA

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

Event Driven Automation (EDA) is the state-of-the-art automation platform that completes Nokia's Data Center portfolio:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/e32a57e04b7985cb3475d5d0301d5e1f/CleanShot_2025-12-14_at_12.59.08.png", padding=10, shadow=true)}}-

The design goals behind EDA were lofty and our ambitions were to create an infrastructure automation platform that addresses many challenges seen in the data center networking and beyond. All our expertise in the model-driven network management, large-scale orchestration, and network automation were poured into EDA to create a platform that redefines how network automation is done.

In the {==configuration management==} domain EDA breaks the status quo of imperative, box-by-box, screen-scraping-dominant configuration process and leverages declarative and abstracted configuration model. In this model a user declares what services or components they want to get deployed by providing its desired state in the form of an input that abstracts the vendor-specific complexities and implementation details.  
Using this approach EDA takes care of all the low-level details of how to translate the abstracted intent into device-specific configurations and how to concurrently and reliably orchestrate the deployment across the network devices to ensure a smooth and reliable rollout.  
EDA's configuration engine is built for performance and safety, being able to validate changes before deployment and to automatically roll them back across the whole network in case of node-level failures.

The state of the art configuration management is not the only variable in the infrastructure automation equation. Being able to accurately track and manage the state of the infrastructure deployed with automation is often more important and challenging.  
To address the divide between the configuration management and observability/monitoring tools, EDA also takes care of the {==state handling==} for every abstracted configuration intent it deployed.  
For example, a network-wide service like L3VPN that spans multiple network elements will have its overall aggregate state reliably tracked in real time by EDA and reported back to the user as state information associated with the original intent.  
Having the state of the system aligned with the configuration inputs is crucial for reliable and consistent operations since the complex task of correlating the state of the individual low-level metrics to the network-wide service parameters is lifted from the operations teams and handled automatically by EDA.

For {==operations teams==} EDA provides a set of operational dashboards that reflect the real-time state of the configured services and components. The dashboards are driven by EDA's State Engine and its ability to provide the real-time aggregated state and metrics for the abstracted configuration intents. The dashboard designer allows users to create custom dashboards that fit their operational needs.  
In addition to the dashboards, EDA offers an instant, network-wide view of the running configuration and state via its EDA Query Language (EQL). A query that runs over your whole network and provides instant and live results is an extremely powerful tool for auditing, troubleshooting and state correlation.

While the concepts of declarative and abstracted configuration management are not new, in EDA we made sure our users can {==extend and program==} almost every aspect of the platform. Do not agree how we modeled a DC fabric inputs? You have all the instruments to change it or even create your own implementation of it.  
Besides the ability to develop custom applications for EDA platform, we also provide a rich set of {==API and CLI==} interfaces to interact with the platform programmatically or via command line. Ranging from REST APIs covering all EDA functionalities to integrations with popular DevOps tools like Ansible and Terraform, EDA is built to fit in your existing toolchain.

And it would be a miss to keep EDA anchored to Nokia-only devices, that is why we ensured that EDA core is {==multivendor==} and users can leverage EDA superpowers even with other 3rd party devices[^1].

## Starting The Tour

The "Tour Of EDA" is a collection of hands-on exercises carefully selected by the EDA product team that puts you in the judge's seat to rule on EDA capabilities first hand. It is a mix of theory and practice that starts with the basic concepts of EDA and progresses to more advanced use cases.

To begin your journey, make sure you have the "Try EDA" environment running as described in the [Getting Started](../getting-started/try-eda.md) guide. The Try EDA environment is a fully functional EDA installation for demo/development purposes that comes with a Digital Twin network that we will use in the first exercises.

-{{ diagram(url='nokia-eda/docs/diagrams/digital-twin.drawio', title='', page=0, zoom=1.2) }}-

As you progress through the tour exercises, you will modify the original three-node lab topology to add more devices and services.

/// admonition | Tour of EDA in Codespaces
    type: example
Don't have your own compute to run the Try EDA environment? No worries, you can run it for free in GitHub Codespaces! Check out our [EDA in Codespaces](../getting-started/codespaces.md) guide to learn how to get started. Or simply click the button:

<div align=center markdown>
<a href="https://github.com/codespaces/new?repo=1129099670&ref=main">
<img src="https://gitlab.com/-/project/7617705/uploads/3f69f403e1371b3b578ee930df8930e8/codespaces-btn-4vcpu-export.svg"/></a>

**Start the Tour of EDA in Codespaces for free**.
</div>
///

## Packing The Tools

Every serious explorer needs a set of tools to help them navigate the unknown. And mark our words, there will be plenty of interesting discoveries along your journey. You'll need just these two to begin with:

* `kubectl` - to interact with the underlying Kubernetes cluster
* `edactl` - to use EDA's specific APIs and commands

These tools have already been downloaded as part of the Try EDA environment setup and you will be able to copy[^3] them from the `playground` repository using the commands outlined in the [Using the CLIs](../user-guide/using-the-clis.md) document.

## Checklist

Let's use the tools we just packed to verify that everything in our environment is ready to go.

> Don't worry if your output does not match ours, and nothing works, join our [**Discord**](https://eda.dev/discord) server to get help.

Starting with Config Engine - the brain of EDA - we can use `kubectl` to check that the `engine-config` resource reports `Started` in its status:

```{.shell .no-select}
kubectl -n eda-system get engineconfig engine-config \
-o jsonpath='{.status.run-status}'
```

<div class="embed-result highlight">
```{.text .no-select .no-copy}
Started
```
</div>

`Started` is good, anything else is bad!

Next, let's verify that our network topology is up and running. The topology deployed as part of the Try EDA consists of topology nodes and links, with each node represented by an SR Linux simulator. The topology nodes in EDA are represented by the `TopoNode` resource, and this resource has a status field to indicate its health.

Let's put `edactl` to work[^2]:

```{.shell .no-select}
edactl -n eda get toponodes #(1)!
```

1. The demo topology is created in the `eda` namespace, hence the `-n eda` flag.

<div class="embed-result highlight">
```{.text .no-select .no-copy}
NAME     PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE
leaf1    7220 IXR-D3L   25.10.1   srl   true        normal   Connected   Synced
leaf2    7220 IXR-D3L   25.10.1   srl   true        normal   Connected   Synced
spine1   7220 IXR-D5    25.10.1   srl   true        normal   Connected   Synced
```
</div>

If you do not see all nodes in `Synced` state, something went wrong and you should retry the Try EDA deployment.

<div class="grid cards" markdown>

* :fontawesome-solid-route:{ .middle } **Where to next?**

    ---

    We encourage you to follow the tour path as this ensures a nice and steady build up of knowledge and skills.

    Our first stop is EDA's Graphical User Interface, which offers a user-friendly way to interact with the platform.

    [:octicons-arrow-right-24: **EDA UI**](ui.md)

</div>

/// admonition | Work in Progress
    type: subtle-note
This tour is a work in progress and we are continuously adding more exercises and improving the existing ones. Check back often to see what's new and join our [**Discord**](https://eda.dev/discord) server to share your feedback and suggestions.
///

[^1]: Pending vendors' maturity of YANG models and modern management interfaces.
[^2]: `kubectl` would work the same in this example.
[^3]: If using EDA in Codespaces, the tools are already in your PATH.
