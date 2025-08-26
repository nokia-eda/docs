# Banner Script Walkthrough

To better understand how script apps work, we invite you to walk through the demo Banner application that is bundled with EDABuilder CLI and was part of the [quickstart guide](../quick-start.md).

The Banner app has a very simple purpose: to provision a login banner on the supported targets by submitting an abstracted input. This is the task of the configuration component of the app.  
The state script of the Banner app simply lists the nodes that the Banner has been provisioned to.

The simple scope of the app allows us to focus on the generic app development, rather than going into the weeds of the implementation logic.

We are starting this walkthrough assuming you left off at the end of the quickstart guide, with the app named "banners" has been scaffolded with the Banner resource in it.

## API

Recall, that the "banners" application we created is meant to be a grouping for resources that make up the banners app. Each resource is an abstracted intent that is characterized by a set of inputs (spec) and outputs (status).

During the scaffolding process we added the Banner resource to the "banners" application. This Banner resource is our abstracted intent that should be able to provision a login banner message on a list of target nodes based on the node selector.

The starting point of the app development is defining the API surface of the resource to match the intent of the app. Application's API is defined in `.go` files following the [kubebuilder](https://github.com/kubernetes-sigs/kubebuilder) pattern that is familiar to most K8s app developers.

Let's have a look how `edabuilder` scaffolded the Banner resource API:

```shell title="executed from the root of the example repo"
tree -L 2 banners/api
```

<div class="embed-result">
```{.shell .no-copy .no-select}
banners/api
└── v1alpha1
    ├── bannerstate_types.go
    ├── banner_types.go
    ├── groupversion_info.go
    ├── pysrc
    └── zz_generated.deepcopy.go
```
</div>

We are focusing on the `banner_types.go` and `bannerstate_types.go` files, which defines the API surface of the Banner and BannerState resources.

/// admonition | Banner and BannerState?
    type: question
Why the two resources you may ask? When in the quickstart we scaffolded the Banner resource and provided the `-d` flag to it, we got two types of resource:

1. `Banner` - the [configuration type](config.md) that defines the abstracted input for the configuration intent.
2. `BannerState` - the [state type](state.md) that defines the abstracted input for the state intent.

These two resources are the two sides of the same coin. One is responsible for configuring the target based on the input, and the other one is responsible for gathering the state of the intent, generating alarms and populating the resource's status field with the relevant data.

///

### Configuration

Open up the `banner_types.go` file and you will see the following code:

```{.go .code-scroll-lg}
// BannerSpec defines the desired state of Banner
type BannerSpec struct {
    // List of nodes on which to configure the banners.
    Nodes []string `json:"nodes,omitempty"`

    // Labe selector to select nodes on which to configure the banners.
    NodeSelector []string `json:"nodeSelector,omitempty"`

    // This is the login banner displayed before a user has logged into the Node.
    LoginBanner string `json:"loginBanner,omitempty"`
}

// BannerStatus defines the observed state of Banner
type BannerStatus struct {
    // +eda:ui:title="Nodes"
    // List of nodes this banner has been applied to
    Nodes []string `json:"nodes,omitempty"`
}
```

The two Go types `BannerSpec` and `BannerStatus` define the specification and the status fields that our `Banner` resource should have. The fields in these two structure effectively describe the API surface of the Banner resource:

```go
// Banner is the Schema for the banners API
type Banner struct {
    metav1.TypeMeta   `json:",inline"` //(1)!
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   BannerSpec   `json:"spec,omitempty"`
    Status BannerStatus `json:"status,omitempty"`
}
```

1. `TypeMeta` and `ObjectMeta` fields are common to every k8s resource and implement the fields like `apiVersion`, `kind`, `namespace`, `labels` and so on.

/// details | What's with extra comments?
    type: subtle-question
Did you notice the extra comments all around the types and type fields? These are annotations:

```go
type BannerSpec struct {
 // +kubebuilder:validation:Optional
 // +eda:ui:columnspan=2
 // +eda:ui:orderpriority=100
 // +eda:ui:autocomplete=`{"group":"core.eda.nokia.com", "version":"v1", "resource":"toponodes"}`
 // +eda:ui:title="Nodes"
 // List of nodes on which to configure the banners.
 Nodes []string `json:"nodes,omitempty"`
```

These are important parts of the API as with annotations we define validation rules, UI behavior and other aspects of the application. The annotations are covered in their own documentation section.
///

Looking again at the `BannerSpec` type, we can clearly see what the app is supposed to do:

1. The `Nodes` field is a list of string values that will accept target node names to which the login banner should apply.
2. The `NodeSelector` is a list of string values where each element is a valid label selector. With this field we extend our Banner API to not only work on exact target node names, but on a dynamic set of nodes based on their labels.
3. And the last element of the spec is the `LoginBanner` string - simply a message that will be displayed at login time.

The `BannerStatus` is rather simple, both in implementation and the desired behavior:

```go
// BannerStatus defines the observed state of Banner
type BannerStatus struct {
    // List of nodes this banner has been applied to
    Nodes []string `json:"nodes,omitempty"`
}
```

With the above we say that the Banner's status container will only have one field - `Nodes` - that is a list of node names this banner has been applied to.

Combining the spec, status and the common metadata fields, our API can be used with a resource defined in YAML format like this:

```yaml
apiVersion: banners.eda.local/v1alpha1
kind: Banner
metadata:
  name: example-banner
  namespace: eda
spec:
  nodeSelector:
    - eda.nokia.com/role=leaf
  loginBanner: Hello EDA!

```

### State

Besides the `Banner` resource, we have the `BannerState` resource that serves a trigger to the state script of our app. The concept of the configuration and state scripts being triggered by the Banner and BannerState resources respectively is a core concept of the EDA framework that might be new to you.

The reason the state script is triggered by its own resource is based on the high scalability aspect and the separation of concerns between the configuration and state scripts.

In case of the `BannerState` resource, the API is very simple - it only has a single `Nodes` field. This field defines a list of node names this banner has been applied to.

```go
// BannerStateSpec defines the desired state of BannerState
type BannerStateSpec struct {
    // List of TopoNodes this login banner has been applied to
    Nodes []string `json:"nodes,omitempty"`
}

// BannerStateStatus defines the observed state of BannerState
type BannerStateStatus struct {
}

// BannerState is the Schema for the bannerstates API
type BannerState struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   BannerStateSpec   `json:"spec,omitempty"`
    Status BannerStateStatus `json:"status,omitempty"`
}
```

We will see later how the configuration and state scripts make use of the API we defined for both `Banner` and `BannerState` resources.

## Config script

It is time to have a look at the actual application code of the configuration script that uses the API we discussed above and implements the intent of the app.

Both config and state intents are located in the `./<app-name>/intents` directory. In particular, the listing of the configuration script directory is as follows:

```shell
tree banners/intents/banner
```

<div class="embed-result">
```{.text .no-copy .no-select}
banners/intents/banner
├── config_intent.py
├── handlers.py
├── __init__.py
├── init.py
├── srl.py
└── sros.py
```
</div>

* `config_intent.py` - the main entrypoint of the configuration script.
* `handlers.py` - contains the logic to select the particular vendor implementation for the configuration task.
* `srl.py` - contains the logic of the configuration script for Nokia SR Linux.
* `sros.py` - contains the logic of the configuration script for Nokia SR OS.

### Entrypoint

When you create an instance of the Banner resource, it triggers the execution of the config script, and the entrypoint for the script is the `process_cr` function in the `banners/intents/banner/config_intent.py` file:

```python
def process_cr(cr):
```

The entrypoint function takes in a custom resource (cr) in form of a dictionary. The dictionary's content is a raw representation of the Banner resource as user submitted it to EDA.

For example, if you commit a Banner resource in the following form, you get the respective dictionary:

/// tab | Banner resource

```yaml
apiVersion: banners.eda.local/v1alpha1
kind: Banner
metadata:
  name: example-banner
  namespace: eda
spec:
  nodes:
    - leaf11
  loginBanner: Hello EDA!

```

///
/// tab | dictionary input

```python
{
    "metadata": {
        "name": "example-banner",
        "namespace": "eda"
    },
    "kind": "Banner",
    "spec": {
        "loginBanner": "Hello EDA!",
        "nodes": [
            "leaf11"
        ]
    }
}
```

///

### Initialization and Validation

After receiving the input to the entrypoint function, we can create an instance of the Banner class:

```python
from banners.api.v1alpha1.pysrc.banner import Banner
from utils.log import log_msg

def process_cr(cr):
    """Process Banner CR."""
    log_msg("Banner CR:", dict=cr)
    cr_obj = Banner.from_input(cr)
    if cr_obj is None:
        return

    cr_name = cr_obj.metadata.name
```

EDABuilder generates the python classes, such as `Banner`, from the API schema we defined. The python classes are stored in the `banners.api.v1alpha1.pysrc` python package and a class has a method `from_input` that creates an instance of the class from the raw input dictionary. We store that instance in the `cr_obj` variable.

When the object is created we can validate it and initialized some defaults if needed:

```python
from banners.intents.banner.init import init_globals_defaults, validate

def process_cr(cr):
# continuation of the process_cr function
    validate(cr_obj)
    init_globals_defaults(cr_obj)
```

In the Banner's case, these two functions are merely placeholder.

### Selecting targets

The script progresses to its next logical step: selecting targets. Almost all configuration scripts will have a piece of their logic dedicated to selecting the nodes to apply config to.

If you remember, the Banner's resource API provides two options how the targets can be selected by the user:

1. selecting the targets based on the provided list of names
2. selecting the targets based on the provided label selectors

EDA API provides convenience functions to support both methods of node selection, and since our API allows both, we have implementations for both:

```python
import utils.exceptions as e
import utils.node_utils as nutils

def process_cr(cr):
# continuation of the process_cr function
    nodes = {}

    if cr_obj.spec.nodeSelector is not None and len(cr_obj.spec.nodeSelector) > 0:
        log_msg("Filtering nodes with node selectors:", dict=cr_obj.spec.nodeSelector)
        for node_cr in nutils.list_nodes(filter=[], label_filter=cr_obj.spec.nodeSelector):
            node_name = node_cr["metadata"]["name"]
            nodes[node_name] = node_cr
            log_msg("Found node:", dict=node_name)

    if cr_obj.spec.nodes is not None and len(cr_obj.spec.nodes) > 0:
        for node in cr_obj.spec.nodes:
            if node not in nodes:
                node_cr = nutils.get_node(name=node)
                if node_cr is None:
                    msg = f"Node {node} not found"
                    raise e.InvalidInput(msg)
                nodes[node] = node_cr
```

Using the `list_node` and `get_node` functions from the `utils.node_utils` package we can get a list of nodes for a selector or a single node by its name. We store the list of Node objects in the `nodes` variable.

Once we have all nodes fetched, it is time to perform configuration action on them.

### Multivendor handlers

Regardless if we provided the nodes by name or by selectors, the node list may include Network OSes from different vendors. In the case of the Try EDA topology we have Nokia SR Linux and Nokia SR OS nodes, which are two very distinct operating systems.  
Yet, our Banner resource should be applied to all supported nodes, how does it work?

The answer lies in the NOS-specific handlers that each app implements individually. Let's look at the code block that follows the node selection:

```python hl_lines="11-12 15-16"
from banners.intents.banner.handlers import get_config_handler
from common.constants import PLATFORM_SRL, PLATFORM_SROS

def process_cr(cr):
# continuation of the process_cr function

    for node, node_cr in nodes.items():
        if node_cr is not None:
            node_spec = node_cr["spec"]
            if node_spec.get("operatingSystem", None) is not None:
                if node_spec.get("operatingSystem") == PLATFORM_SRL:
                    srl_handler = get_config_handler(PLATFORM_SRL)
                    if srl_handler is not None:
                        srl_handler.handle_cr(cr_obj, node_cr)
                elif node_spec.get("operatingSystem") == PLATFORM_SROS:
                    sros_handler = get_config_handler(PLATFORM_SROS)
                    if sros_handler is not None:
                        sros_handler.handle_cr(cr_obj, node_cr)
                else:
                    msg = f"Operating system unsupported for {node}, os is {node_spec.get('operatingSystem', None)}"
                    raise e.InvalidInput(msg)
            else:
                msg = f"Operating system unsupported for {node}, os is {node_spec.get('operatingSystem', None)}"
                raise e.InvalidInput(msg)
```

Here, the nodes we iterate on are the [`TopoNode`][topoNode-crd] objects from the `core.eda.nokia.com` API group. Based on the `operatingSystem` value in the TopoNode spec, the code selects either SR Linux or SR OS handler.

[topoNode-crd]: https://crd.eda.dev/toponodes.core.eda.nokia.com/v1

The handler-selection function is quite simple:

```python title="banners/intents/banner/handlers.py"
from common.constants import PLATFORM_SRL, PLATFORM_SROS
from .srl import SrlBaseConfigHandler
from .sros import SrosBaseConfigHandler

_config_handlers = {
    f"{PLATFORM_SRL}": SrlBaseConfigHandler(),
    f"{PLATFORM_SROS}": SrosBaseConfigHandler(),
}


def get_config_handler(os) -> SrlBaseConfigHandler | SrosBaseConfigHandler | None:
    return _config_handlers.get(os)  # pragma: no cover
```

The corresponding handler class is typically stored in its own file - `banners/intents/banner/srl.py|sros.py` - and this class implements translation of the abstracted vendor-agnostic intent to the node-specific configuration.

### Node-specific config

Now that we know how different handlers are instantiated, let's have a look again at how they are being used:

```python hl_lines="11 15"
def process_cr(cr):
# continuation of the process_cr function

    for node, node_cr in nodes.items():
        if node_cr is not None:
            node_spec = node_cr["spec"]
            if node_spec.get("operatingSystem", None) is not None:
                if node_spec.get("operatingSystem") == PLATFORM_SRL:
                    srl_handler = get_config_handler(PLATFORM_SRL)
                    if srl_handler is not None:
                        srl_handler.handle_cr(cr_obj, node_cr)
                elif node_spec.get("operatingSystem") == PLATFORM_SROS:
                    sros_handler = get_config_handler(PLATFORM_SROS)
                    if sros_handler is not None:
                        sros_handler.handle_cr(cr_obj, node_cr)
```

Based on the `operatingSystem` field in the node CR, the appropriate handler is instantiated and the `handle_cr` method is called with the Banner instance and the TopoNode passed as arguments.  
At this point, we pass the abstracted, high-level Banner intent, and we expect that the appropriate handler will turn this into the node-specific config.

Here is how the implementation of the SR Linux handler class:

```python
class SrlBaseConfigHandler:
    def handle_cr(self, cr_obj: Banner, node_cr=None):
        configs = []
        log_msg(f"cr_obj: {cr_obj}")
        log_msg(f"node_cr: {node_cr}")
        node_name = node_cr[Y_METADATA][Y_NAME]
        self._generate_config(cr_obj, configs)
        eda.update_cr(
            schema=s.CONFIG_SCHEMA,
            name=f"banner-{cr_obj.metadata.name}-{node_name}",
            spec={"node-endpoint": node_name, "configs": configs},
        )

    def _generate_config(self, cr_obj: Banner, configs: list):
        _config = {}
        if cr_obj.spec.loginBanner is not None:
            _config["login-banner"] = cr_obj.spec.loginBanner

        configs.append(
            {
                "path": ".system.banner",
                "config": json.dumps(_config),
                "operation": "Create",
            },
        )
```

We focus on the `handle_cr` method that receives the Banner and the TopoNode resources. The high-level operation of any handler function would look like this:

1. Receive the abstracted intent
2. Process the received abstracted intent and emit sub resource(s)
      1. The sub resource may be any sub resource registered within EDA, for example the Fabric application may emit BridgeDomain, ISL and so on.
      2. For simple apps that can translate the abstracted intent directly into the node configuration, they emit `NodeConfig` resource that Config Engine provisions on the nodes via NPPs.
3. Create the state intent to trigger the state processing.

Looking more closely at the `handle_cr` of our Banner script we can spot that it follows this pattern to the dot and generates the `NodeConfig` resource as part of its operation.

With `eda.update_cr` method we create a `NodeConfig` resource in EDA by providing the schema of the NodeConfig resource and its specification:

```python
eda.update_cr(
    schema=s.CONFIG_SCHEMA, #(1)!
    name=f"banner-{cr_obj.metadata.name}-{node_name}",
    spec={"node-endpoint": node_name, "configs": configs},
)
```

1. `schema=s.CONFIG_SCHEMA` - the schema of the `NodeConfig` resource

The specification of the `NodeConfig` gets the node-endpoint which is the node name fetched from the `node_cr` variable and the `configs` which is the list of configurations generated in the `_generate_config` method.

The same process is followed by the SR OS handler, which you will find in the `sros.py`.

Ultimately, even if an application script does not directly generate the `NodeConfig` resource, the emitted sub-resources will eventually resolve to the `NodeConfig` instances and this is how EDA unwraps the high level abstract intent to an actual node-level implementation.

### Creating state resource

At the very end of the `banners/intents/banner/config_intent.py` script you will find a peculiar code piece:

```python
eda.update_cr(
    schema=BANNERSTATE_SCHEMA,
    name=cr_name,
    spec={
        "nodes": list(nodes.keys()),
    },
)
```

This is how the configuration intent triggers the state intent run - it creates the `BannerState` resource for this. As we just defined the API specification of the `BannerState` resource ourselves, we know that the `BannerState` specification receives a list of nodes to which we provisioned the login banner.

In the same spirit as with the configuration script, the corresponding state script will be triggered based on the fact that the `BannerState` resource appeared in the system.

## State script

State scripts are executed in the State Engine component and are triggered by the corresponding state resource. State scripts are meant to be used to achieve the following:

1. Compute the state for the corresponding abstracted resource
2. Generate alarms for the resource

State script is not a mandatory app component, but you will find that most applications have one.

Our Banner application has a state script and you can find it in the `bannerstate` directory:

```shell
tree banners/intents/bannerstate 
```

<div class="embed-result">
```{.text .no-copy .no-select}
banners/intents/bannerstate
├── eda.py
├── __init__.py
├── init.py
├── state_handlers.py
└── state_intent.py
```
</div>

The entrypoint for the state script is, like in the config script case, implemented as the `process_cr` function found in the `state_intent.py` file. It takes in the customer resource input:

```python
def process_state_cr(cr):
    log_msg("BannerState CR:", dict=cr)
    cr_obj = BannerState.from_input(cr)
    validate(cr_obj)
    init_globals_defaults(cr_obj)
    handler = get_state_handler(PLATFORM_EDA)
    handler.handle_cr(cr_obj)
```

In contrast with the config intent, the state script does not have require different NOS-specific handlers, instead a single EDA handler is used.

The handler does a trivial task of updating the status field of the `Banner` resource:

```python
class EdaStateHandler:
    def handle_cr(self, cr_obj: BannerState):
        nodes = cr_obj.spec.nodes
        eda.update_cr(
            schema=BANNER_SCHEMA,
            name=cr_obj.metadata.name,
            status={
                Y_NODES: nodes,
            },
        )
```

It is worth reiterating, that the state script does not target the state BannerState resource, but updates the status field of the configuration - `Banner` - resource. It is somewhat and indirect way of populating the status field of the Banner resource and is done in that way to achieve high scale.

Technically, the `Banner` resource does not need a state script at all, as we could've updated its status directly from the config script, but this is done to demonstrate how state scripts work when you start writing applications that compute some more elaborated state.
