# Introducing EDA

The Nokia Event Driven Automation framework \(EDA\) is an extensible, declarative, intent-based automation and operations NetOps platform that delivers agile and scalable network operations for data center and cloud environments of any size.

The EDA framework and capabilities include:

-   A truly event-driven platform.

    Configuration is an event. A state transition in the network is an event. Operational activities are events. The controller generically handles these events, no matter their source, with the goal to reconcile the state of managed elements to get closer to the intended state.

-   Declarative, extensible intent-based operations and automation across all aspects of device management.

    EDA simplifies and dramatically reduces effort across many operational and design tasks.

-   An open framework to build event-driven applications.

    Applications built upon EDA's open framework can provide simple configuration normalization or templating, handle state updates, generate and process their own resources, raise alarms, publish and populate GUI views, and much, much more. All out-of-the-box configuration and state handling is built on this framework and is open-source.

-   A stream-everything design.

    Receive on-change, real-time notifications on anything and everything in the system or network in the UI, over the API, or within custom event-driven applications.

-   Built on cloud-native design principles.

    Scale flexibly with microservices based on the number of managed resources and endpoints, simplifying integrations and controller interactions by providing a single API and automation layer no matter your scale.

-   Ubiquitous observability through “on-change” streaming telemetry from Nokia Service Router Linux \(SR Linux\).

    Every configuration and state path is available, all of the time.

-   A query language and corresponding endpoint.

    The EDA query language \(EQL\) provides filtered, ordered, on-demand retrieval and streaming of any YANG path on any managed elements network-wide, or any system-published data.

-   A Digital Sandbox.

    Enables a digital twin capability that emulates the network and is used to dramatically reduce both testing time and network risk.

-   A Continuous Integration/Continuous Deployment \(CI/CD\) framework embodying DevOps principles applied to the network.

    Write custom pre and post-checks, test changes in branches, and follow the GitOps model for merging changes into production.

-   Integration with major cloud management platforms.

    Integration enables the automation of network connectivity to support constantly changing application requirements.

-   Resource abstraction and selection via labels.

    With EDA, you can flexibly label resources to dynamically update dependencies.


## Fundamentals <span id="fundamentals"></span>

Within EDA, controllers continually reconcile managed elements based on external or internal events in the system with the help of pluggable automation applications.

These applications define their own resources and define the logic these resources enact when created, modified, or deleted. This is similar to the Kubernetes controller loop, and event-driven applications work similarly to Custom Resource Definition-based controllers and their reconciliation loop in Kubernetes.

Where EDA differs from the reconciliation loop is when only a partial state can be achieved. EDA uses a transaction concept for rolling changes onto groups of network elements. Transactions are flexible in their boundaries, allowing you to group changes that must succeed together into a single transaction, and avoid having to deal with ordering complexities or partially deployed changes.

Apps built on EDA leverage a generic intent framework that allows the building of event-driven applications to implement intents. The architecture allows custom resources with a user-defined schema to be loaded, and to have customized logic written in MicroPython that handles the creation and updates of these resources. Where this differs from other controllers is that applications are entirely stateless, run-to-completion entities, with the EDA ConfigEngine \(or CE\) automatically handling deltas between executions. Apps are simple to write, and can be iterated on using a CI/CD workflow in production.

Going beyond simple customizations, EDA provides a full-featured platform for application development. Application writers can build their own UIs using the EDA Rapid Application Development \(ERAD\) framework and handle state transitions of any YANG path in the MicroPython framework. Applications are able to generate alarms, normalize data and write it back to the EDB, or simply update the status of a resource, and more.

EDA takes CI/CD and the infra-as-code movement to heart. On the completion of a transaction, the resulting set of input resources are written to a local Git repository and can be pushed to one or more remotes, with this being the only required persistent database. This unique approach allows revision control on all resources in the system, a simplified backup and restore approach, and a simplified geo-redundancy model, with two or more sites configured with the same repository.

Additionally, using Git as a database allows the true CI/CD workflow in the modification of network resources. EDA supports a branching concept, in which one or more additional EDA instances can be instantiated on a branch off a main, production cluster. Changes can then be made on the branched cluster before merging them back using merge/pull requests into the main branch.

Merging into main in this context is equivalent to pushing changes into production. But before this, you can use the Digital Sandbox to test the impact of any changes in a digital twin of the production network, including simulated nodes.

### Importance of an open, model-driven, consumable NOS <span id="xxx"></span>

The declarative, intent-based framework and the automation capabilities of the Nokia Event Driven Automation framework are only made possible by leveraging a modern NOS that offers an open, model-driven, stream-anything foundation.

Nokia SR Linux couples each service with its own YANG data model, allowing for broad, deep and efficient network data access from any interface. This modular approach provides open streaming telemetry and network management that use gNMI \(gRPC Network Management Interface\) to stream network data and configure network devices.

By using this modern approach for the NOS, the Event Driven Automation framework has timely and efficient access to more granular data across the entire fabric. This data can then be used to understand the state of the network, which is essential for event-driven applications to determine if the network is behaving according to their intent. This approach is also highly scalable, which is essential in today’s networks.

## EDA as part of the Nokia Data Center Fabric solution <span id="data-center-solution"></span>

Since the advent of software-defined networking \(SDN\), the industry has experimented with the separation of the management, control, and data planes. For scalable and faster convergence in large-scale data center networks, the architectural approach that has gained industry momentum is a combination of distributed routing \(using control planes and data planes\) running on data center switches with the necessary network-wide control and automation functions implemented in an external controller. This approach combines the centralized control and programmability of a traditional SDN approach with the higher scalability and convergence of a distributed routing approach. This is the approach we have taken with the Nokia Data Center Fabric solution.

The Event Driven Automation framework is a key component of the Data Center Fabric solution, which also includes the following products:

-   Nokia Service Router Linux \(SR Linux\): An open, extensible, and model-driven network operating system \(NOS\) based on Linux® that enables scalability, flexibility, and efficiency in data center and cloud environments.

-   Nokia Data Center Fabric hardware platforms: A portfolio of next-generation leaf and spine switches that deliver massive scalability and performance while aggregating and interconnecting data center and cloud environments.


In support of fabric management, the Fabrics application exists to support the automation and operation of fabric topologies. Beyond this, EDA uses other generic applications to abstract overlay services, interfaces, underlay configurations, and so on.

## Architecture components <span id="architecture-components"></span>

The Nokia Event Driven Automation framework adopts a microservices design that is built on top of Kubernetes. These include both components native to EDA, and industry-standard third-party components.

### EDA components <span id="architecture-eda-components"></span>

#### APIServer

APIServer is the gateway into EDA. APIServer dynamically extends its endpoint coverage as new event-driven applications are onboarded, and provides streaming endpoints for all resources. APIServer also acts as the common authorization point for RBAC, providing a common AAA mechanism across all endpoints. AAA itself is implemented using Keycloak.

#### EDA store

EDA uses a variety of supporting applications to manage its wide range of capabilities. EDA uses an on-product EDA Store to display the set of available EDA applications, and assist in their installation, update, and removal. The EDA Store also tracks the status of all installed applications.

#### ArtifactServer

ArtifactServer is the artifact storage server. ArtifactServer provides a flexible artifact cache in the cluster, allowing network elements and API clients to store and retrieve artifacts of many kinds.

#### Bootstrap server - Zero-touch Provisioning \(ZTP\)

ZTP performs bootstrap and discovery of managed endpoints, allowing an end user to implement a simple “plug-and-power-up” approach to onboard new devices onto the controller and surrounding network.

#### ConfigEngine

ConfigEngine is the core of configuration in EDA. It is responsible for reconciling all configuration input to the system, and executing any EDA App logic before pushing changes to NPP instances as needed. ConfigEngine uses a unique dependency model that allows applications to simply request information they need to reconcile. These requests build a dependency tree that can then be triggered if any dependent resources update. All updates to resources trigger their dependent resources \(and their dependent resources in turn\) to execute. This dependency logic goes as far as allocation pools, meaning that simply changing an IP pool in use from IPv4 to IPv6 would result in all users of the pool being triggered to process the update. You can convert your entire network from IPv4 to IPv6 in one reversible transaction.

#### Digital Twin

One of the key requirements for modern data centers is the ability to make faster, periodic changes while still managing the risk of a change. To this end, the EDA framework delivers a cloud-native Digital Twin, a containerized virtual infrastructure that emulates the production network by creating its digital twin. EDA uses the Digital Twin to validate intent across the life cycle of the fabric. The Digital Twin is also an essential part of the network validation phase of the CI/CD pipeline process. The EDA framework integrates the Digital Twin in all its workflows to provide design validation and change management flexibility, thereby reducing the risk of changes in a dynamic data center environment. With this capability, operators can make faster, periodic, and independent changes to the network, lowering risk and increasing operational agility.

The Digital Twin is an integral part of Nokia’s approach for CI/CD and is used to trial and validate network changes before deploying them in the production network. Changes can include initial fabric design, initial service connectivity, software upgrades, introduction of new devices, policy configuration changes, and failure scenarios.

The Digital Twin provides a digital twin of the data center fabric, emulating network elements by deploying a containerized Nokia SR Linux and SR OS instance of each, which are used to test and validate any planned network changes.

The Digital Twin leverages on-change telemetry to maintain absolute parity of the network in configuration, routing, and state. It also can emulate external Border Gateway Protocol \(BGP\) speakers and generate synthetic traffic.

The Digital Twin allows any changes to the production network to be tested and validated before being deployed in the network, greatly reducing risk.

Some of the benefits of Digital Twin are:

-   Time and resource savings: Saves time and resources by quickly and efficiently testing network, configuration and routing scenarios in a virtualized, pre-built environment that is in absolute parity with the network.
-   Reduced risk: Greatly reduces risk to the network by first validating network changes in a fully emulated environment before deploying the changes in the network.
-   Lower lab expenses: Reduces the effort and cost of setting up lab environments to test and validate network changes.
-   Reduced power consumption: Drives a green approach to testing and validation by leveraging a virtualized environment that can be set up and changed in minutes.
-   Ease of use: A complete virtual infrastructure is built into the Event Driven Automation framework and is fully programmable and easily set up through an intuitive UI.

#### State Aggregator

EDA's StateAggregator acts as an aggregation point for EQL queries and state requests. It provides a single, uniform interface to the EDA database \(EDB\).

StateAggregator supports multiple instances using replicas; this is controlled using `EngineConfig`. It supports demuxing requests into request to multiple shards, and aggregating results.

StateAggregator provides gRPC endpoints, secured using mTLS, to support the following functions:

-   Verifying the liveness of SA.
-   Executing and auto-completing EQL queries.
-   Retrieving data from one or more shards matching filters, with various types of streaming and one-shot.
-   Retrieving and streaming the schema of any table.

#### StateController

StateController is the core of state queries in EDA. StateController provides a scalable common layer for EDB queries, and maintains the shard map - or the locations of other EDB shards.

#### StateEngine

StateEngine is the core of state processing in EDA, responsible for reconciling all state input to the system, and executing any EDA app logic before pushing deltas to EDB to trigger any dependent applications.

#### Applications

EDA apps are a set of applications that provide several types of intent, including Fabric \(Day 0 design\), VirtualNetwork \(Day 1 deployment\), and maintenance intents \(Day 2+ operations\). The intent framework of the Event Driven Automation framework allows operators to define, in an abstract manner, the intended end state of resources and configuration. By using streaming telemetry to understand the current state, the system can determine any discrepancies from the intended state and implement any required network changes.

#### UI 

EDA employs a simple, extensible, easy-to-use UI that allows for complete programmable operation and visualizations. Operations that can be performed through the UI can also be performed through EDA's REST APIs.

#### NPP 

NodePushPull is a purpose-built microservice that ingests the highly scalable streaming telemetry offered by SR Linux and SR OS, and manages configuration interactions with network elements.

#### EDB 

EDA DB is a purpose-built, sharded database that allows the distributed streaming and processing of state information in the cluster.

#### ERAD 

EDA Rapid Application Development environment allows you to build any UI view you like with drag-and-drop components and flexible streaming queries to EDB.

#### Connect 

Connect performs integration with cloud management platforms, allowing virtual machine \(VM\) or container “spin up” and “tear down” events to drive network change. This capability enables the data center fabric to react to workload and compute connectivity requirements. Connect integrates using REST APIs and a plugin-based model, enabling seamless, modular, and simple integration with cloud management platforms.

#### Workflow Engine

In EDA, both workflow and CI/CD functionality is supported through the WorkflowEngine. The WorkflowEngine acts as the controller behind the instantiation, status, and interaction with the `Workflow` and `WorkflowDefinition` resources.

### Third-party components <span id="xxx"></span>

In addition to its own internal, native components, EDA uses a collection of well-known, industry-standard third-party components to support its operations.

#### Kubernetes

Kubernetes provides an event-driven microservices foundation. Running natively in Kubernetes has numerous benefits, including providing abstraction from physical compute resources, as well as the ability to define the entire deployment through infrastructure-as-code \(IaC\) principles using Helm charts and kpt as package managers.

#### Cert Manager

EDA uses CertManager, an extensible X.509 certificate controller, to generate, sign, and distribute the signed certificates and keys for pods. CertManager validates certificates for public and private issuers, and can assist in renewing certificates before they expire.

#### Fluent Bit and Fluent Operator

EDA uses Fluent Bit to assist with the processing of logging data. EDA uses a Fluent Bit pod on each Kubernetes worker node to collect logs from the EDA microservices to collect logs from the EDA microservices and one additional Fluent Bit pod as a log aggregator. By default, the Fluent Bit aggregator writes API access logs in their own file, logs each microservice data in their own directories, and maintains an aggregate errors log.

Fluent Operator manages the Fluent Bit configuration and simplifies adding output destinations such as a syslog server.

#### Git

EDA uses Git to store data for all successful transactions. This allows EDA to support reverting of transactions and restoring to previous states. Most often Git capabilities are used to support revision control over individual resources or sets of resources.

#### Keycloak

EDA uses Keycloak to support authentication, and passes authentication to Keycloak directly instead of using intermediate APIs. Authentication \(and subsequent authorization\) are required to interact with all non-login APIs in EDA.

#### Metrics Server

EDA uses Kubernetes Metrics Server to collect and share resource metrics.

## Declarative, intent-based automation <span id="xxx"></span>

The Nokia Event Driven Automation framework allows operators to represent the configuration and initial state of the data center fabric in a declarative, intent-based way. With this declarative approach, the intended configuration and state of the fabric can be specified up front in a simplified or abstract way that defines how the fabric should operate. This intended state, which is stored centrally, represents “the single source of truth” and can be used to iteratively validate the actual state of the network.

### Day 0 intent-driven design 

By taking an abstract, intent-based approach for Day 0 design, the data center operator can focus on high-level aspects of the design, identifying the minimal information needed to build a data center fabric. For example, the operator needs to input only a few parameters, such as the number of racks and the number of servers per rack.

The system uses this information to automatically generate the rest of the detailed configuration based on Nokia-certified design templates. The result is a standard BGP-based IP fabric design \(for example, number of racks, number of servers per rack, IPv4/IPv6 addressing, BGP configuration, cable map, and so on\) that can be validated using the Digital Sandbox before being deployed to the data center fabric.

With this intent-based approach, multiple leaf-spine fabrics can be created by easily replicating the first one created or by creating a customized fabric.

### Day 1 intent-driven deployment 

For Day 1 deployment, one of the initial tasks performed by the Event Driven Automation framework is fabric discovery and node bootstrap. The Event Driven Automation framework offers Zero Touch Provisioning \(ZTP\) to turn up new leafs and spines, allowing the adoption of a simple plug-and-power-up approach to onboard new nodes onto the fabric.

After the new nodes are onboarded, the Event Driven Automation framework can then push Day 0’s validated design to the fabric, thereby completing deployment of the initial network underlay portion of the fabric.

Day 1 deployment uses the concept of Virtual Networks to automate the creation of the required overlay connectivity, to support the initial application workloads that are hosted on attached compute resources. To create this connectivity, the Event Driven Automation framework leverages Ethernet VPN \(EVPN\) Layer-2 and Layer-3 services within and across the data center fabric.

The Virtual Network application abstracts the complexity of the EVPN configuration by enabling the data center operator to focus on specifying high-level parameters. This high-level intent can be as simple as identifying the set of downlinks an application workload uses to connect to the fabric. Virtual networks can be validated using the Digital Sandbox before being deployed into the production network.

Complexities such as switch-to-switch EVPN and allocation of VXLAN network identifiers, route distinguishers, route targets, Ethernet segment IDs and Ethernet virtual interfaces are all abstracted and left to the Event Driven Automation framework to generate according to the high-level intent parameters specified by the operator.

### Day 2+ intent-driven maintenance 

During Day 2+ operations, the EDA framework uses maintenance intents \(such as hardware intents and software intents\) to define the intended state of the network in terms of software and hardware. With these two intent types defined, the intended software load and hardware version across the network is defined for each leaf, spine, or super-spine switch.

For Day 2+ operations, the EDA framework constantly monitors the fabric by leveraging on-change telemetry it receives directly from various sources in the network. The EDA framework compares this information with various intents and analyzes the results to find configuration inconsistencies, faults or other deviations that may lead to network issues.

Each inconsistency, fault, or other deviation is flagged and presented to the operator to be either accepted or rejected. These inconsistencies can often require a change to the network \(for example, a configuration change or software upgrade\) to fix the problem. With the EDA framework, the operator can automate the testing and validation of these network changes using the Digital Sandbox. If these changes pass validation, they can be scheduled for automatic deployment into the production network.

This process of automated testing and validation dramatically lowers the risk of deploying network changes because it identifies any potential problems before a change is deployed in the network.

## Fabric observability <span id="xxx"></span>

To operate today’s modern data center fabrics, real-time observability information is required to support various operational tasks. Fabric observability is needed to monitor the fabric, and is achieved by accessing a combination of on-change, streaming telemetry and log data that represents the network state and is collected directly from the data center fabric.

Multi-dimensional telemetry comes from various sources, including:

-   Basic telemetry: Faults, standard statistics, TCAM/LPM, and so on.
-   The control plane: Link Layer Discovery Protocol/Link Aggregation Control Protocol \(LLDP/LACP\) state and events, BGP adjacency, BGP routing information base \(RIB\), forwarding information base \(FIB\), and so on.
-   The fabric workload layer: Topology, number of apps, number of flows, and so on.

The EDA framework constantly receives this information using the SR Linux gNMI and leverages instances of NPP to ingest this streaming telemetry while scaling as required. The EDA framework enables a cloud-native, scale-out collector architecture to ensure that collection capabilities are highly distributed.

## Fabric operations <span id="xxx"></span>

After the data center fabric is designed and deployed, the Day 2+ operations phase begins. In this phase the Event Driven Automation framework compares both design and workload intent \(that is, single source of truth\) with all the telemetry data collected from the fabric to both optimize operational tasks and ensure that the network is operating as expected.

### Fabric integrations

The EDA framework provides an open REST API that allows third parties to have full access to the system. A flexible, cloud-native approach enables integration of the EDA framework with many different customer cloud environments.

Cloud-native architectures, built with microservices and containers, are pushing the limits of network scalability and performance, requiring networks to be much more responsive to changes in applications. Modern data center fabrics need to be synchronized with applications to remove the network as an obstacle to innovation. There needs to be a symbiotic relationship between the applications and the network that serves them.

To tackle this requirement head-on, the EDA framework has implemented a Connect microservice that allows for integration, using a plugin infrastructure, with cloud management platforms such as OpenStack, VMware vSphere, and Kubernetes. With this integration, any change events to workloads \(both virtualized network functions and containerized network functions\) are immediately understood by the Connect service. This allows the fabric to react in real-time to these events and ensures that Layer-2 and Layer-3 fabric connectivity always supports these changes. This type of integration is essential to scale next-generation data center networks.

## Conclusion <span id="conclusion"></span>

As the demands on data center networks continue to drive openness, flexibility, and agility, the Nokia Data Center Fabric solution was purpose-built to meet these challenges. As part of this solution, the Nokia Event Driven Automation framework delivers declarative, abstract intent where automation and simplification are needed while also delivering detailed insights by monitoring every aspect of the data center fabric. This combination of abstract intent-based automation plus detailed openness and visibility allows the data center operator to perform Day 0 design, Day 1 deployment, and Day 2+ configuration, operation, measurement, and analysis of a data center fabric.

