# Script Apps a.k.a. Intents

Script applications (also often referred to as _intents_) are EDA applications powered by Python scripts that are executed as a result of some external event. The simplest event is a user creating or modifying a resource in EDA that triggers a script app to be executed as a reaction to this event.

For example, when a user creates an instance of a `Banner` resource via any of the EDA interfaces, the script application associated with the `Banner` resource is triggered to execute its logic - in this case, to configure a banner message on a network device.

There exists three types of scripts:

* `config`
* `state`
* `conversion`

Among these, `config` and `state` are the most common.

`config` scripts[^1] are triggered when a resource is created, updated or deleted, and typically result in transactions to targets describing intended configuration.

`state` scripts[^2] are responsible for alarm generation, subscription and normalization of telemetry data, and publishing updates to the `status` field of resources, or the creation of state-only resources.

`conversion` scripts are run when a resource is converted from one version to another, i.e. only during upgrades and resource version translation.

<!-- # Updating resources in the system -->

<!-- # React to telemetry events -->

<div class="grid cards" markdown>

* :material-hammer-screwdriver:{ .middle } **App Example**

    ---

    Practical walkthrough of a simple script app.

    [:octicons-arrow-right-24: Banner application walkthrough](banner-script.md)

* :octicons-question-16:{ .middle } **More reading?**

    ---

    Learn more about the Config and State scripts.

    [:octicons-arrow-right-24: Config scripts](config.md)

</div>

[^1]: Execute inside EDA Config Engine.
[^2]: Execute inside EDA State Engine.
