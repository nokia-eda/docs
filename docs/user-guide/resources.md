# Resources

In EDA, a resource is a unit of automation and can represent virtually anything:

- an interface on a network device
- a complete fabric configuration
- a network service like a VPN or a VRF
- and even non-network related resources like a user account, a DNS record, or a firewall rule.

As a Kubernetes citizen, EDA represents its resources using Custom Resources (CRs) of Kubernetes that can be created using multiple methods including the Kubernetes (K8s) API, the EDA API, or through a User Interface (UI). By using CRs, EDA also implements the Kubernetes Resource Model, or KRM.

The KRM defines how Kubernetes resources are described, created, updated, and monitored. Kubernetes resources consist of a combination of fields that describe their state and behavior within the cluster, most importantly the `spec`, `status`, and `metadata` fields.

In Kubernetes, a resource is any object the Kubernetes API can create and manage. These resources represent various entities, such as `Pods`, `Services`, `Deployments`, `ConfigMaps`and so on., which are essential for orchestrating containerized applications.

Every resource in Kubernetes is defined using a standard structure that includes `metadata`, a `spec`, and a `status`. Where:

- `metadata` provides unique identifiers and metadata for resources.
- `spec` provides the specification for the resource - its configuration.
- `status` provides an interface for the controller/resource to publish relevant information back to the user/operator.

## Derived resources

As part of the execution of a transaction, EDA applications sometimes generate a set of resources. These resources are not "owned" by the user or operator; instead, they owned by the application that generated them. To ensure the ongoing operation of the owning application, such resources can only be changed by that same application.

In EDA, such a resource is known as a derived resource; it is a resource whose entire content is derived from some other resource.

The EDA GUI prevents you from modifying or deleting derived resources. To indicate that a resource is derived and cannot be modified or deleted, derived resources are presented as read-only, and the usual modification actions are restricted; for example, EDA does not allow you to use a Delete action to delete a derived resource. Unavailable actions are grayed out in action lists.

In data grids, rows displaying derived resources are shaded to indicate that those resources cannot be modified or deleted.

## Labels <span id="labels"></span>

EDA uses labels to organize and describe resources. Labels are among the metadata common to all resources in EDA. In the EDA GUI, labels can be viewed and entered in the Metadata panel for a resource.

-{{image(url="graphics/sc0226.png", title="Figure: Resource metadata", shadow=true, padding=20)}}-

Labels are not mere descriptions of objects; they are also used throughout EDA as the basis for selecting objects. You can apply the same label to a set of objects and then manipulate them as a group based on that shared label. This makes it easier for system administrators and operators to manage large-scale clusters.

A label consists of two pieces of information: a key, and a value. Labels are limited to key-value pairs of small size and are designed for simple, static values. For example:

- app=frontend
- version=v1.0
- environment=prod

The key can include up to 253 characters if using the DNS subdomain format (`<domain>/<key>=<value>`), and the value can include up to 63 characters.

Labels are particularly useful for selecting objects; for example, you can use a label to indicate which pods a service should treat as traffic destinations. The following illustration shows a segment of a fabric configuration in which participating leaf nodes are selected among those that possess the label "role" and its value is "leaf". Additional labels can be selected to narrow down the set of qualifying nodes.

-{{image(url="graphics/sc0227.png", title="Figure: Selecting objects based on labels", shadow=true, padding=20)}}-

Users and application writers can:

- apply labels arbitrarily to resources
- select resources within their application based on these labels

Label changes are considered normal changes for the purposes of transactions. A label change can trigger execution of scripts and if executions are successful, their changes are persisted to Git.

Labels are a flexible way to decouple the interactions between resources, but they do have some limitations. In particular, the value of a label is limited to 63 characters and Kubernetes resource names are limited to 253 characters. This means that labels cannot reliably encode a resource name, for example.

/// Note
Labels in EDA work slightly differently from labels in Kubernetes. EDA still stores labels in the metadata of a resource as does Kubernetes, but the means by which you select based on labels is slightly different. In particular, Kubernetes objects typically use the `metav1.LabelSelector` Go struct in order to select labels of a certain resource type. This `LabelSelector` is not supported in EDA.

Instead, EDA uses one or more string expressions to select. An expression can contain one or more selectors, separated by `,`. Selectors are AND'd together, similar to Kubernetes' `LabelSelector`. A selector supports various operators, including but not limited to `=`, `!=`, `in`, `notin`.
///

Some examples:

- `app=cat` means a resource is only returned if it has a label present named `app`, with a value of `cat`.
- `app in (cat)` is another way of writing the above, meaning a resource is only returned if it has a label named `app` with a value of `cat`.
- `app` returns a resource if it has a label present with the name `app`, with any value \(including an empty value\).
- `!app` returns a resource if it does not have a label present with the name `app`, with or without a value.
- `app in (cat, dog)` returns a resource if it has a label present with the name `app`, with a value of `cat` OR `dog`.
- `app in (cat, dog),env in (prod, demo)` returns a resource if it has both a label named `app` with values `cat` OR `dog`, AND a label named `env` with values `prod` OR `demo`.
- `app notin (elephant, rhino)` returns a resource if it does NOT contain a label named `app` with a value of either `elephant` OR `rhino`.
- `app=cat,env=prod` returns a resource if it has a label named `app` with the value `cat`, AND a label named `env` with value `prod`.

### Selecting or creating a label

In the EDA GUI, where a **Label** field is present, you can enter a label by clicking in the **Label** field and selecting from the list of available labels.

-{{image(url="graphics/sc0228.png", title="Figure: Selecting a label", shadow=true, padding=20)}}-

To use an existing label, select it in the list. To narrow the list of displayed labels, type the first few letters of a label you are looking for; the list filters to show only the labels that match the text provided.

To create a new label, click **Add** to open the label creation window:

-{{image(url="graphics/sc0230.png", title="Figure: Adding a key", shadow=true, padding=20)}}-

Enter a **Key** and a **Value**, then click **Add**.

## Annotations <span id="annotations"></span>

EDA uses annotations to organize and describe resources. Annotations are among the metadata common to all resources in EDA. In the EDA GUI, annotations can be viewed and entered in the Metadata panel for a resource.

-{{image(url="graphics//resource-metadata.png", title="Figure: Resource metadata", shadow=true, padding=20)}}-

Annotations are similar to labels, but are used for different purposes.

Like a label, an annotation consists of a key and a value. However, annotations values are not subject to the same length restrictions as labels. Annotations can store lengthy information that resembles the information contained in labels, but frequently overruns labels length restrictions.

Like labels, annotations are metadata about an object. But unlike labels, annotations do not influence the system’s behavior. Annotations are not used for selection or querying. They are not indexed and do not affect any selection logic. Annotations are more informational; and although they are not used by EDA's resource selection systems, they can still be useful to external systems, people, or automation tools.

Annotations are typically used to store arbitrary, unstructured data like configuration details, URLs, object tracking information, or any other information that does not need to be part of Kubernetes’ logic. They are useful for attaching large or complex data that does not need to be indexed, like CI/CD metadata, deployment signatures, or documentation links.

The EDA system uses annotations to store two types of data:

- ConfigEngine uses the annotations property to tag resources for which transactions have failed.

    The system-generated annotation text indicates that the resource is part of a failed transaction, and the Kubernetes-visible version of the resource may not be aligned with the running/actual version.

- The system uses the annotations property to store resource names.

    This is primarily used with derived resources, where it is useful to be able to see the hierarchy of resources - for example a `VirtualNetwork` generating a `BridgeDomain`.

Examples of possible annotations values:

- kubectl.kubernetes.io/last-applied-configuration="JSON"
- author=team-name
- description="Stores the last applied configuration of a resource for use by kubectl apply"

Annotation changes are considered normal changes for the purposes of transactions. They trigger execution of scripts, and if executions are successful, their changes are persisted to Git. However, there are a small number of exceptions. EDA does not trigger, monitor, or persist any annotations with the following keys:

- `core.eda.nokia.com/failed-transaction`
- `core.eda.nokia.com/running-version`
- `kubectl.kubernetes.io/last-applied-configuration`

### Selecting or creating an annotation

In the EDA GUI, where an **Annotation** field is present, you can enter an annotation by clicking in the **Annotation** field. Select from the list of available annotations:

-{{image(url="graphics/sc0263.png", title="Figure: Configuring annotations", shadow=true, padding=20)}}-

To use an existing annotation, select it from the list. To narrow the list of displayed annotations, type the first few letters of a label you are looking for; the list filters to show only the annotations that match the text provided.

To create a new annotation, click **Create a Key Value pair chip** to open the annotation creation window:

-{{image(url="graphics/sc0230.png", title="Figure: Adding a key to a notation", shadow=true, padding=20)}}-

Enter a **Key** and a **Value**, then click **Add**.

## Resource topologies <span id="resource-topologies"></span>

Because the volume of resources and their relationships within EDA is very large, it can be difficult to effectively grasp the relationship between one resources, and all of the other configured resources on which it somehow depends.

To help represent resources and their interconnections, EDA builds on its topology visualization framework by providing a Topology illustration. This illustration shows the selected resource, and the other EDA resources to which it is connected.

To see the topology view for a resource, open the Details view for an individual resource, and then select **Topology** from the drop-down list of available views.

For example, the following illustration shows the resource topology for a fabric. It shows not the fabric's physical topology, but its connection to the set of other resources configured within EDA:

- default routers
- ISLs
- routing policies
- system interfaces
- BGP groups
- prefix sets

-{{image(url="graphics/sc0310.png", title="Figure: An example of a fabric resource topology", shadow=true, padding=20)}}-

In the EDA UI, you can click any resource in the illustration to see more information in the Information panel.
