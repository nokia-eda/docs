# Scripts

Scripts (also often referred to as _intents_) are MicroPython code that is executed as a result of some external event. The simplest event is a user creating a resource with a script watching it.

There exists three types of scripts:

* `config`
* `state`
* `conversion`

Among these, `config` and `state` are the most common. `config` scripts execute inside Config Engine, and result in transactions to targets and Kubernetes describing intended configuration.

`state` scripts execute inside State Engine and are responsible for alarm generation, subscription and normalization of telemetry data, and publishing updates to the `status` field of resources, or the creation of state-only resources.

`conversion` scripts are run when a resource is converted from one version to another, i.e. only during upgrades and resource version translation.

<!-- # Updating resources in the system -->

<!-- # React to telemetry events -->
