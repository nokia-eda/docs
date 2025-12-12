# Building Abstractions

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js" async></script>

One of the key pillars of EDA is the notion of abstractions. Abstractions allow users to express a higher-level intent in a way that is decoupled from the underlying implementation details and/or vendor specific knowledge.  
In EDA, every application is typically made up of one or more abstracted resources.

Some resources provide a low-level abstraction - e.g., a familiar [Banner resource](banner-script.md) that abstracts away the vendor-specific configuration details of configuring a banner and MOTD on a network device, but is still fairly close to the actual configuration model of the target device.  
Other resources provide a much higher abstraction that is built on top of a bunch of smaller abstractions - like a Fabric resource that on its own abstracts away all configuration details required to build an EVPN VXLAN fabric on a set of multivendor devices and uses Interfaces, BGP Peers, Route Reflectors, and so on.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/253d383de8874dbe7e3cdbfff8dca4db/CleanShot_2025-12-06_at_22.39.22.png", padding=20, shadow=True, title='Fabric resource and its lower-level abstractions it is based on')}}-

When do you need to build an app on top of existing abstractions? Typically, the following goals call for building new abstractions:

* **simplification** - you want to provide a simpler interface for users to interact with, hiding fields and options that are not relevant to the use case at hand or setting sensible defaults for them.
* **customization** - you want to encode specific operational logic or policies into the allocated resources that would otherwise require users to manually provide input.
* **composition** - you want to combine multiple existing abstractions into a single higher-level abstraction that fits a specific use case.

In this in-depth tutorial, we will learn how to build applications that leverage existing EDA resources to provide customized abstractions that fit a desired use case.

## Simple Fabrics Application

/// warning
This tutorial assumes you are running

* EDA 25.12 or later
* Fabrics app 5.0.0 or later.
///

To keep things real, we are going to build an application that provisions a fully functional EVPN VXLAN fabric, but with a very minimal set of options exposed to the user. We are going to call this application **Simple Fabrics**.

As the name suggests, the Simple Fabrics app will build an abstraction on top of the existing Fabric resource that EDA provides out of the box as part of the Fabrics application.

EDA's native Fabric resource is an already abstracted resource, yet it is very flexible and exposes dozens of options to ensure many different fabric designs can be accommodated.  
However, in many cases, as an operator, you may want to standardize the way your fabrics are built, limit the number of options that users can choose from, and set meaningful defaults for the rest. This is exactly the goal of the Simple Fabrics application that we are going to build.

-{{diagram(url='nokia-eda/docs/diagrams/simple-fabric',page=0, title='Simple Fabric provides abstraction on top of Fabric resource', zoom=1.5)}}-

Our Simple Fabric app should be able to build an EVPN VXLAN fabric with the following design requirements:

* use IPv6-LLA unnumbered addressing in the underlay
* use eBGP as the underlay routing protocol
* use eBGP as the overlay routing protocol
* default to `asn-pool` for ASN allocation
* auto-select leaf, spine and ISL label selectors based on pre-defined labels assigned to the resources in EDA
* create the underlying Fabric app with a distinct name pattern to backtrack it to the Simple Fabric resource
* report state from the underlying Fabric resource for ease of monitoring

With these requirements in mind, we can derive all inputs for the original Fabric app, thus reducing the cognitive load for an operator. Let's compare the original Fabric resource input and the Simple Fabric resource we are going to build.

/// tab | Original Fabric Resource Input

```yaml
apiVersion: fabrics.eda.nokia.com/v1alpha1
kind: Fabric
metadata:
  name: original-fabric
  namespace: eda
spec:
  leafs:
    leafNodeSelector:
      - eda.nokia.com/role=leaf
  spines:
    spineNodeSelector:
      - eda.nokia.com/role=spine
  interSwitchLinks:
    linkSelector:
      - eda.nokia.com/role=interSwitch
    unnumbered: IPV6
  systemPoolIPV4: systemipv4-pool
  underlayProtocol:
    protocol:
      - EBGP
    bgp:
      asnPool: asn-pool
  overlayProtocol:
    protocol: EBGP
```

///
/// tab | Simple Fabric Resource Input

```yaml
apiVersion: simple-fabrics.eda.local/v1alpha1
kind: SimpleFabric
metadata:
  namespace: eda
  name: simple-fabric
spec:
  underlayASNPool: asn-pool #(1)!
```

1. This is a default, pre-filled value.

///

Comparing the two resource specs shows how the design goal of the Simple Fabrics app is achieved - by exposing only a minimal set of options to the user while setting sensible defaults for the rest. While not strictly needed, we will expose one option to allow users to choose the ASN pool for the underlay BGP protocol to demonstrate how to pass user-provided input down to the underlying Fabric resource. However, you can imagine that even this option could be assumed by the app if desired, further simplifying the user input.

> Building applications that reuse existing **Fabric** and **Virtual Networks** resources is a popular use case to tailor these abstractions to specific design requirements.

## Initializing the Project

To begin the development of our Simple Fabrics application, we first need to initialize a new project using [`edabuilder`](../edabuilder.md) CLI. The project may contain one or more applications, each in its own sub-directory. And while we plan to build only one application in this tutorial, we will still need to create a project that hosts it.

Navigate to a directory where you want to create the project and run:

```bash
edabuilder init --vendor eda-labs simple-fabric #(1)!
```

1. The `vendor` parameter specifies the vendor name that applications in this project will inherit. It is a free-form text field, and you can choose any name you like here. If you plan to publish your application to the catalog in the future, pick a vendor name that is unique to you or your organization.

    > You may see an informational message about a missing registry parameter. The registry parameter is used to specify a custom registry for publishing applications, but it is not required for local development or for this tutorial, so you can safely ignore this message.

    The project name `simple-fabric` is also arbitrary and can be changed to any name you prefer, it does not have to match the application name and is only used to create the project directory.

This command will create a new directory called simple-fabric containing the initial project structure and files. Open this project directory in your favorite code editor to continue development.

Initialize the python environment for this project. If you are using `uv`, simply run:

```bash
uv sync
```

This will create a virtual environment and install all required dependencies for the project.

> The project also contains an `.envrc` file that can be used with [direnv](https://direnv.net/) to automatically load the virtual environment when navigating to the project directory.

Initialize a git repository in the project directory to track the changes as we progress with the development:

```bash
git init
```

## Creating the Application

After initializing the project, we can proceed with the Simple Fabrics application creation. To do so, run the following command from the project root directory:

```bash
edabuilder create app simple-fabrics 
```

This command will create a new application named `simple-fabrics` in the `simple_fabrics` sub-directory of the project. The application directory will contain the initial structure and files needed for the application development.

/// details | Application Directory Structure

```text
❯ tree simple_fabrics
simple_fabrics
├── alarms
│   └── pysrc
├── api
│   └── v1alpha1
│       ├── groupversion_info.go
│       └── pysrc
│           ├── __init__.py
│           └── constants.py
├── build
├── crds
├── docs
│   ├── CHANGELOG.md
│   ├── LICENSE.md
│   ├── README.md
│   ├── SUPPORT.md
│   ├── media
│   ├── resources
│   └── snippets
├── examples
├── go.mod
├── intents
├── manifest.yaml
├── openapiv3
├── rbac
├── test
├── ui
└── workflows
```

///

The files and folders you get with the initial application creation are explained in detail in the [Application Components](../components.md) section.

## Creating the Resource

On its own, the application we just created has no functionality; it merely serves as a container for the resources, workflows, and other components that developers build next. In our case, we need to create a new resource - Simple Fabric - that will implement the desired abstraction and logic on top of the existing Fabric resource.

To create the resource, provide the resource kind name[^1] and the application name via the `--app` argument and run the command from the project root directory:

```bash
edabuilder create resource SimpleFabric --app simple-fabrics
```

This operation will create a set of files defining the API of the SimpleFabric resource, but since `edabuilder` can't quite read our minds yet, it will just lay down a skeleton structure of the API without any fields defined in the spec or status sections. We need to fill in the details ourselves.

## Resource API

EDA is 100% API-defined, meaning that every resource is described by its API/schema. For the API definition, EDA uses the [Kubernetes Resource Model](https://github.com/kubernetes/design-proposals-archive/blob/main/architecture/resource-management.md) as its foundation with some EDA-specific extensions to make the resource rules even more expressive.  

Every resource typically has the following main sections in its API definition:

* `apiVersion` - defines the API group and version of the resource.
* `kind` - defines the resource kind name.
* `metadata` - contains standard fields like `name`, `namespace`, `labels`, and `annotations` that are common to all Kubernetes resources.
* `spec` - contains the desired state of the resource, defined by the user.
* `status` - contains the observed state of the resource, typically filled in by the controller.

For our newly created SimpleFabric resource, we need to define the **`spec`** and **`status`** sections to reflect the desired abstraction and functionality; the other sections have already been scaffolded by `edabuilder` for us.

Both specification and status API definitions are located in the `simple_fabrics/api/v1alpha1/simplefabric_api_types.go` file that was created by `edabuilder`. Open this file and you will see the scaffolded API definition in Go language:

```go
package v1alpha1 //(1)!

// SimpleFabricSpec defines the desired state of SimpleFabric
type SimpleFabricSpec struct {
	// INSERT ADDITIONAL SPEC FIELDS - define desired state of cluster
	// Important: Run "edabuilder generate" to regenerate code after modifying this file
	Foo string `json:"foo"`
}

// SimpleFabricStatus defines the observed state of SimpleFabric
type SimpleFabricStatus struct {
	// INSERT ADDITIONAL STATUS FIELDS - define observed state of cluster
	// Important: Run "edabuilder generate" to regenerate code after modifying this file
	Baz string `json:"baz,omitempty"`
}
```

1. The package name matches the API version of the resource, and since we did not specify any custom version during the resource creation, it defaults to `v1alpha1`.

As you can see, the `spec` and `status` sections of a resource are expressed as Go structs, but fear not, you don't need to be a Go programmer to create an application API.

Following the design requirements we [outlined earlier](#simple-fabrics-application) for the Simple Fabrics app, we can start defining the fields our app needs. Starting with the `spec` section, let's remove the placeholder `Foo` field and add the `underlayASNPool` field that we want to expose to the user:

```go
type SimpleFabricSpec struct {
	UnderlayASNPool string `json:"underlayASNPool"`
}
```

> If you recall, our Simple Fabrics app only exposes one field to the user, the ASN pool for the underlay BGP protocol, the rest of the parameters are defaulted by the app to reduce the complexity for the user and further abstract the fabric creation.

To add a new field to the `spec`, we have to come up with a field name in PascalCase format (`UnderlayASNPool`), define its type (`string`), and provide the JSON tag that defines how the field will be represented in the YAML/JSON manifest of the resource (e.g., `json:"underlayASNPool"`). For those familiar with Kubernetes CRD development, this should look very familiar.

With these changes, our API definition kept in the `simplefabric_api_types.go` file now looks like this:

```go
package v1alpha1

// SimpleFabricSpec defines the desired state of SimpleFabric
type SimpleFabricSpec struct {
	UnderlayASNPool string `json:"underlayASNPool"`
}

// SimpleFabricStatus defines the observed state of SimpleFabric
type SimpleFabricStatus struct {
}
```

## Deploying the App

When developing an application, it is often useful to deploy it to a running EDA instance to test and validate its functionality. Making sure iterating on the application is easy and fast was one of the main goals when designing `edabuilder`.

Even though our Simple Fabrics app is not yet functional, we can still deploy it to EDA to ensure that the API definition we created is valid, installable, and shows up in the EDA UI.

To deploy the application at any given point during the development, simply run:

```bash
edabuilder deploy --app simple-fabrics
```

The `edabuilder deploy` command takes care of building the application, setting up the internal container registry in the active EDA cluster, pushing the application image to it, and installing the app via the regular EDA App Installer workflow. A lot of magic happens under the hood, but the developer only needs to run this single command to get the application deployed.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/47c427c42b32ed844b8f03dd36dd5460/CleanShot_2025-12-08_at_21.01.05.png", title="Application installation via Workflow")}}-

Now that our app is installed, where do we find it in the UI? If you search for "simple" in the EDA sidebar, you will find the app listed under the "Simple Fabrics" section:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/3602dd1ccd55176b911582bad16328b7/CleanShot_2025-12-08_at_21.35.43.png", title="Simple Fabrics App in EDA UI")}}-

As evident from the screenshot above, the app is categorized under the "SIMPLE FABRICS" category and the resource is titled "simplefabrics" - both values come from the `simple_fabrics/manifest.yaml` file created by `edabuilder`. We will see how to customize these values later in the tutorial.

If you select the "simplefabrics" resource from the sidebar and click on "Create" button, you will see the schema form for this resource, which should look like this:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/12c855313e9723a8417f591e95358870/CleanShot_2025-12-09_at_13.52.43.png", title="Simple Fabric Resource Schema Form")}}-

Even though our resource does not have any functionality yet, we can see that the basic API definition we created is valid, and the `underlayASNPool` field is correctly represented in the schema form.

Also note the "SimpleFabricSpec defines the desired state of SimpleFabric" description under the Specification section in the screenshot above. It comes straight from the comment we added above the `SimpleFabricSpec` struct in the API definition file. Developers can add such comments and additional metadata to the API fields to enrich the schema. This is the topic of the next section.

## API Annotations

Through comments and annotations in the API definition, developers can provide additional metadata about the resource and its fields, add constraints, defaults, validation rules, and drive the UI representation of the resource.

### Descriptions

The most basic form of metadata that can be provided in the API definition Go file is comments. Comments can be added to the structs as well as to the individual fields. For example, our default descriptions are meaningless, so let's improve them by updating the comments in the `simplefabric_api_types.go` file as follows:

```diff
@@ -16,8 +16,16 @@ limitations under the License.
 
 package v1alpha1
 
-// SimpleFabricSpec defines the desired state of SimpleFabric
+// This app demonstrates how developers
+// can build abstractions using the existing resources.
+// The Simple Fabric application configures the EVPN VXLAN fabric
+// with a simplified set of inputs when compared to the Fabrics app.
+// It assumes the default values for the node selectors, protocol configuration, etc,
+// while exposing a minimal set of parameters to a user.
 type SimpleFabricSpec struct {
+       // The ASN pool used for the underlay network.
+       // The `asn-pool` default value is the default ASN pool
+       // that comes with "Try EDA" installation.
        UnderlayASNPool string `json:"underlayASNPool"`
}
```

By adding comments above the SimpleFabricSpec struct and the UnderlayASNPool field, we have enriched the API definition with meaningful descriptions that will show up in the UI schema form, making it easier for users to understand the purpose of the resource and its fields.

If you were to call `edabuilder deploy --app simple-fabrics` again after saving these changes and reload the UI, you would see the updated descriptions in the schema form.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/f6e63323bd8c057c97333015be6baae9/CleanShot_2025-12-09_at_14.20.23.png", title="Updated Descriptions in Schema Form")}}-

### Title

By default, the field names in the schema form are generated from the JSON tags defined in the API struct fields. That is why you see `underlayASNPool` as the field name in the form, which is not pretty.

To change the title of any given field, add `+eda:ui:title="Your title goes here"` annotation above it. For example, to change the title of the `underlayASNPool` field to "Underlay ASN Pool", we can update the API definition as follows:

```diff
@@ -26,6 +26,7 @@ type SimpleFabricSpec struct {
        // The ASN pool used for the underlay network.
        // The `asn-pool` default value is the default ASN pool
        // that comes with "Try EDA" installation.
+       // +eda:ui:title="Underlay ASN Pool"
        UnderlayASNPool string `json:"underlayASNPool"`
}
```

### Default Value

Right now, the `underlayASNPool` field is mandatory, and users have to provide a value for it when creating a SimpleFabric resource. However, we want to set a default value of `asn-pool` for this field so that users don't have to specify it unless they want to override it.

> Setting the defaults as per the design is a popular pattern in custom applications

To provide the default value of `asn-pool`, we leverage another annotation - `+kubebuilder:default="default-value"` - that can be added to a field. Updating the API definition as follows will set the desired default for the `underlayASNPool` field:

```diff
@@ -27,6 +27,7 @@ type SimpleFabricSpec struct {
        // The `asn-pool` default value is the default ASN pool
        // that comes with "Try EDA" installation.
        // +eda:ui:title="Underlay ASN Pool"
+       // +kubebuilder:default="asn-pool"
        UnderlayASNPool string `json:"underlayASNPool"`
}
```

To see the effect of this change, redeploy the app again, and open the schema form for the SimpleFabric resource. You will see that the `Underlay ASN Pool` field now has a default value of `asn-pool` pre-filled in the form - beautiful!

-{{image(url="https://gitlab.com/-/project/7617705/uploads/49990e8f34e25bb1c0fa3fc085e06670/CleanShot_2025-12-09_at_19.45.24.png", title="Default Value set in the Schema Form")}}-

### Autocompletion

With the default value set, users can rely on a sensible default when creating a SimpleFabric resource. However, they may still want to choose a different ASN pool, and right now they have to find the desired pool name and set it manually, which is not very user-friendly.

To further improve the user experience when filling in the schema form, we can make use of the autocompletion annotation that looks like this

```go
+eda:ui:autocomplete=`{"group":"core.eda.nokia.com", "resource":"indexallocationpools"}`
```

With the autocompletion annotation configured in this way, EDA will query for all existing `IndexAllocationPool` resources from the API group `core.eda.nokia.com` in the cluster and provide their names as suggestions when the user puts the cursor in the `Underlay ASN Pool` field in the schema form.

Let's add it:

```diff
@@ -28,6 +28,7 @@ type SimpleFabricSpec struct {
        // that comes with "Try EDA" installation.
        // +eda:ui:title="Underlay ASN Pool"
        // +kubebuilder:default="asn-pool"
+       // +eda:ui:autocomplete=`{"group":"core.eda.nokia.com", "resource":"indexallocationpools"}`
        UnderlayASNPool string `json:"underlayASNPool"`
}
```

And now after redeploying the app and opening the schema form, when you focus on the `Underlay ASN Pool` field, you will see a dropdown with all available ASN pools in the cluster:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/1a09746a80b2c059268a1b8f5d93f5bf/CleanShot_2025-12-09_at_20.56.39.png", title="Autocompletion in Schema Form")}}-

The section and field descriptions, titles, default values, and autocompletion are just a few of the annotations available to EDA developers to enrich their resource API definitions. For the sake of this tutorial, we will stop here and move on to implementing the actual logic of the Simple Fabrics app.

## Adding Config Script

As an application developer, your work typically gets split between three main areas:

* deciding what resources and components your application will consist of
* defining the individual resources API
* implementing the application logic

We have already taken care of the first two parts by defining the SimpleFabric resource API. Now it is time to put some code in place to implement the logic of our Simple Fabrics app, guided by the design requirements we outlined earlier.

> An EDA application that only leverages internal EDA resources and **does not** need to interact with external systems is called an [**Intent or Script app**](../scripts/index.md).

The application logic that results in configuration being applied to the target devices is implemented in the so-called **config intent** - a MicroPython script that receives the resource instance as input and uses EDA's Intent API to create, read, update, or delete resources as needed.

To create the scaffolded python file for the SimpleFabrics resource that will hold our application logic, run the following command from the project root directory:

```bash
edabuilder --app simple-fabrics create intent SimpleFabric config 
```

where `SimpleFabric` should match the resource kind we added at the [Creating the Resource](#creating-the-resource) step and `config` is the intent type.

You'll have a bunch of new files added as a result of this command. Edabuilder will scaffold the python files in the `simple_fabrics/intents/simplefabric` directory:

```text
❯ tree ./simple_fabrics/intents/
./simple_fabrics/intents/
└── simplefabric
    ├── __init__.py
    ├── config_intent.py
    ├── eda.py
    ├── handlers.py
    ├── init.py
    ├── srl.py
    └── sros.py
```

> The main entrypoint for our intent script is the `config_intent.py` file.

It will also update the manifest.yaml file to register the new script intent. This is an important concept in EDA - every intent is associated with a resource through an explicit registration in the manifest file. The screenshot below shows how the `config_intent.py` script is associated with the SimpleFabric resource via the manifest file by the `trigger` section:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/9cc687c5df87cff5912feecf74812f18/CleanShot_2025-12-09_at_22.36.44.png", title="Intent Registration in Manifest", padding=20)}}-

By associating the intent script with the resource, the EDA Config Engine knows which script to execute when a SimpleFabric resource is created, updated, or deleted.

## Config Entrypoint

The main entrypoint for our config intent is in the `simple_fabrics/intents/simplefabric/config_intent.py` file `process_cr` function. Edabuilder scaffolded this file for us with the basic structure:

```python title="Default content in config_intent.py"
#!/usr/bin/env python3

# imports omitted for brevity

def process_cr(cr):
    """Process SimpleFabric CR."""
    log_msg("SimpleFabric CR:", dict=cr)
    cr_obj = SimpleFabric.from_input(cr)
    if cr_obj is None:
        return

    cr_name = cr_obj.metadata.name
    validate(cr_obj)
    init_globals_defaults(cr_obj)
```

The `process_cr` function is called each time there is a change to a SimpleFabric resource instance - be it creation, update, or deletion. The function receives the resource instance as input in the form of a dictionary called `cr`, which contains the resource manifest as provided by the user. Let's see this in action by deploying the app in its current state and creating a debug session for the SimpleFabric config intent using [`edactl`](../../../user-guide/using-the-clis.md#edactl):

```bash
edactl -n eda intent config debug simplefabric
```

This command will start the debug session and wait for a SimpleFabric resource to be modified. The log message says "Matched 0 instances in namespace eda" because we don't have any SimpleFabric resources yet. Let's create one using `kubectl`:

```bash title="Paste the command in your terminal to create a SimpleFabric resource"
cat <<EOF | kubectl apply -f -
apiVersion: simple-fabrics.eda.local/v1alpha1
kind: SimpleFabric
metadata:
  name: my-simple-fabric
  namespace: eda
spec:
  underlayASNPool: asn-pool
EOF
```

Running this command will create an instance of the SimpleFabric resource named `my-simple-fabric`. As soon as the resource is created, you will see the debug session output show the following:

```text
────────── eda SimpleFabric/v1alpha1/SimpleFabric my-simple-fabric ───────────
InputCR:
    {
      "kind": "SimpleFabric",
      "metadata": {
        "name": "my-simple-fabric",
        "namespace": "eda"
      },
      "spec": {
        "underlayASNPool": "asn-pool"
      }
    }
Stdout:
SimpleFabric CR:
{"metadata": {"name": "my-simple-fabric", "namespace": "eda"}, "kind": "SimpleFabric", "spec": {"underlayASNPool": "asn-pool"}}

InputDb:
OutputDb:
```

The debug output shows the input resource manifest in the **InputCR** block and the log message that is part of our `process_cr` function in the **Stdout** section. This confirms that our intent script is being executed correctly when a SimpleFabric resource is created and we receive the resource manifest in its entirety.

## SimpleFabric Object

The first step to take care of in the `process_cr` function is to instantiate a proper Python object representing our SimpleFabric resource based on the input that the config script received. Thankfully, everything is made ready by `edabuilder`, and we can leverage the `SimpleFabric.from_input(cr)` method that is already present in the scaffolded code. This method takes care of converting the input dictionary into a strongly typed Python object that we can work with in the rest of the script.

Here are the changes in the `config_intent.py` we make compared to the scaffolded code:

```diff
 #!/usr/bin/env python3
-import eda_common as eda
-import utils.node_utils as nutils
-import utils.exceptions as e
-import simple_fabrics.api.v1alpha1.pysrc.constants as c
-
-from common.constants import PLATFORM_SRL, PLATFORM_SROS
-from utils.log import log_msg
 
 from simple_fabrics.api.v1alpha1.pysrc.simplefabric import SimpleFabric
 from simple_fabrics.intents.simplefabric.handlers import get_config_handler
 from simple_fabrics.intents.simplefabric.init import init_globals_defaults, validate
 
+
 def process_cr(cr):
     """Process SimpleFabric CR."""
-    log_msg("SimpleFabric CR:", dict=cr)
-    cr_obj = SimpleFabric.from_input(cr)
-    if cr_obj is None:
+    sf = SimpleFabric.from_input(cr)
+    if sf is None:
         return
 
-    cr_name = cr_obj.metadata.name
-    validate(cr_obj)
-    init_globals_defaults(cr_obj)
+    validate(sf)
+    init_globals_defaults(sf)
```

We remove the imports that are not needed at this stage and rename the `cr_obj` variable to `sf` to better reflect that it is a SimpleFabric object. The rest of the code remains unchanged for now.

The `SimpleFabric.from_input(cr)` method will parse the input dictionary and populate the fields of the SimpleFabric object accordingly. The `SimpleFabric` Python class is defined in the `simple_fabrics/api/v1alpha1/pysrc/simplefabric.py` file and is generated by `edabuilder` based on the Go API definition we created earlier.

> Working with fully typed Python object is a great convenience for developers, as it allows them to leverage IDE features like autocompletion, type checking, and so on.

## Config Handler

Now that we have the SimpleFabric object instantiated, we need to create an entity that will take the SimpleFabric object as input and implement the logic to create the underlying Fabric resource based on the design requirements. This entity is called a **config handler** in EDA terminology as it handles the configuration logic of the resource.

Every EDA intent application has a config handler class that is responsible for implementing the configuration logic. Based on the application design, you will see two types of config handlers:

* EDA config handler - used when the application only creates other EDA resources and does not emit node-level configuration.
* Network OS config handler - used when the application needs to generate device-level configuration snippets for a Network OS. Based on the target OS, different config handlers are implemented - e.g., SROS config handler, SR Linux config handler, and so on.

For our app that only creates an underlying Fabric resource, we need to leverage an EDA config handler, identified by the `PLATFORM_EDA` constant. Open the `simple_fabrics/intents/simplefabric/config_intent.py` and add the highlighted lines:

```python title="adding config handler to config_intent.py" linenums="1" hl_lines="3 18-19"
#!/usr/bin/env python3

from common.constants import PLATFORM_EDA
from simple_fabrics.api.v1alpha1.pysrc.simplefabric import SimpleFabric
from simple_fabrics.intents.simplefabric.handlers import get_config_handler
from simple_fabrics.intents.simplefabric.init import init_globals_defaults, validate


def process_cr(cr):
    """Process SimpleFabric CR."""
    sf = SimpleFabric.from_input(cr)
    if sf is None:
        return

    validate(sf) #(1)!
    init_globals_defaults(sf)

    eda_handler = get_config_handler(PLATFORM_EDA)
    eda_handler.handle_cr(sf)
```

1. The `validate` and `init_globals_defaults` functions are utility functions that can be used to validate the resource and initialize any global defaults needed by the application. We will leave these functions unimplemented.

The `get_config_handler(PLATFORM_EDA)` function call retrieves the EDA config handler for our application. We pass the `PLATFORM_EDA` constant to indicate that we want the EDA config handler. The returned handler object is an empty object of a `EdaBaseConfigHandler` class that is defined in the `simple_fabrics/intents/simplefabric/eda.py` file.

```python title="simple_fabrics/intents/simplefabric/eda.py"
#!/usr/bin/env python3
import json

import eda_common as eda
import utils.schema as s
from common.metadata import Y_METADATA, Y_NAME
from simple_fabrics.api.v1alpha1.pysrc.simplefabric import SimpleFabric


class EdaBaseConfigHandler:
    def handle_cr(self, cr_obj: SimpleFabric):
        # implement this
        pass
```

The scaffolded `EdaBaseConfigHandler` class has a `handle_cr` method that takes the SimpleFabric object as input with an empty body. This is where we should implement the logic to create the underlying Fabric resource based on the defaults and inputs from the SimpleFabric resource.

## Dependencies

The Simple Fabrics app builds on top of the existing Fabric application, by effectively being a wrapper around it and setting sensible defaults and computing the required inputs. Therefore, our Simple Fabrics app has a dependency on the Fabrics app.

To declare this dependency, and furthermore get access to the Fabric resource API in our application code, we need to import this application as a dependency in our Simple Fabrics app. Edabuilder makes this easy by providing a command that downloads the Python API for a given application.

```bash
edabuilder import pyapi --app simple-fabrics \
  --app-image ghcr.io/nokia-eda/apps/fabrics:v5.0.0
```

The `edabuilder import pyapi` command takes two arguments:

* `--app` - specifies the application where the dependency should be added. In our case, it is the `simple-fabrics` app we are building that needs to add a dependency on the Fabrics app.
* `--app-image` - specifies the application image to use to extract the Python API from. Here we provide the OCI image URL of the Fabrics app version 5.0.0[^2] from the public GitHub Container Registry.

Running this command will download the Python files representing the API of the Fabrics app (all of its resources) and add it as a dependency in the `simple_fabrics/manifest.yaml` file. The downloaded API files will be placed in the `deps` subdirectory of the application:

```text
tree ./simple_fabrics/deps
./simple_fabrics/deps
└── fabrics_eda_nokia_com
    └── v5_0_0
        └── api
            └── v1alpha1
                └── pysrc
                    ├── __init__.py
                    ├── constants.py
                    ├── fabric.py
                    ├── fabricstate.py
                    ├── isl.py
                    ├── islping.py
                    └── islstate.py
```

The dependency directory - `deps` is also added to the `manifest.yaml` file to instruct edabuilder to include it when building the application image:

```diff title="simple_fabrics/manifest.yaml"
@@ -17,6 +17,8 @@ spec:
         path: simple_fabrics/api/v1alpha1/pysrc
     - file:
         path: simple_fabrics/intents
+    - file:
+        path: simple_fabrics/deps
```

Because our app requires the Fabrics app to be installed we also need to add the Fabrics app as a required app in the `manifest.yaml` file:

```diff title="simple_fabrics/manifest.yaml"
@@ -40,3 +40,6 @@ spec:
         trigger:
           kind: SimpleFabric
         type: config
+  requirements:
+    - appId: fabrics.eda.nokia.com
+      version: v5.0.*
```

The App ID is the fully qualified name of the Fabrics app as registered in the EDA App Catalog. It matches the `group` value in the apps' manifest.yaml file and can be seen in the URL when viewing the app details in the EDA Store UI.

The version field sets the required version of an app we depend on. A loose version constraint like `v5.0.*` can be set to allow any minor or patch version of the Fabrics app in the 5.0 series to satisfy the dependency.

If you now deploy the Simple Fabrics app again and open the EDA Store UI, you will see how the Fabrics app (and all the apps that Fabrics app requires) are automatically listed as requirements.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/a8e960815c428607df3d561f2c297e10/CleanShot_2025-12-11_at_10.06.36.png", title="App Requirements in EDA Store")}}-

## Creating the Fabric

With the dependency added, we are finally ready to write code that creates the underlying Fabric resource with the desired defaults governed by the Simple Fabrics app design.

As we established earlier, the configuration logic should go into the `handle_cr` method of the `EdaBaseConfigHandler` class in the `simple_fabrics/intents/simplefabric/eda.py` file. Let's start with importing the fabric package from the Fabrics app API that we added as a dependency:

```python title="simple_fabrics/intents/simplefabric/eda.py" linenums="1" hl_lines="6"
#!/usr/bin/env python3
import json

import eda_common as eda

import simple_fabrics.deps.fabrics_eda_nokia_com.v5_0_0.api.v1alpha1.pysrc.fabric as fabric
import utils.schema as s
from common.metadata import Y_METADATA, Y_NAME
from simple_fabrics.api.v1alpha1.pysrc.simplefabric import SimpleFabric
```

Now, lets instantiate a Fabric object in the `handle_cr` method and set its spec fields based on the SimpleFabric input:

```python title="Adding Fabric creation logic to simple_fabrics/intents/simplefabric/eda.py" linenums="1"
class EdaBaseConfigHandler:
    def handle_cr(self, sf: SimpleFabric):
        assert sf.metadata is not None
        assert sf.spec is not None

        fabricName = f"sf-{sf.metadata.name}"

        _fabric = fabric.Fabric(
            metadata=fabric.Metadata(
                name=fabricName,
                namespace=sf.metadata.namespace,
            ),
            spec=fabric.FabricSpec(
                leafs=fabric.Leafs(
                    leafNodeSelector=["eda.nokia.com/role=leaf"],
                ),
                spines=fabric.Spines(
                    spineNodeSelector=["eda.nokia.com/role=spine"],
                ),
                interSwitchLinks=fabric.InterSwitchLinks(
                    linkSelector=["eda.nokia.com/role=interSwitch"],
                    unnumbered="IPV6",
                ),
                systemPoolIPV4="systemipv4-pool",
                underlayProtocol=fabric.UnderlayProtocol(
                    bgp=fabric.UnderlayBGP(asnPool=sf.spec.underlayASNPool),
                    protocol=["EBGP"],
                ),
                overlayProtocol=fabric.OverlayProtocol(
                    protocol="EBGP",
                ),
            ),
        )
```

> Note how importing the Fabric API allows us to instantiate a fully typed and API-driven Fabric object. No more brittle Jinja2 templates or string manipulations - just pure Python code working with strongly typed objects.

The code above creates a Fabric object with the name `sf-<simple-fabric-name>` in the same namespace as the SimpleFabric resource. We add the `sf` prefix to the underlying Fabric resource to additionally distinguish it from other Fabrics that may exist in the cluster. This technique is often used in abstractions.

The spec of the Fabric resource is populated with the desired defaults as per the Simple Fabrics app design. The only field that is set based on the SimpleFabric input is `underlayASNPool`, which is taken from the `sf.spec.underlayASNPool` field.  
If you remember, we default this field to `asn-pool` in the SimpleFabric spec, so unless the user overrides it, the underlying Fabric will always be created with this default ASN pool.

As per our design, the Fabric resource uses the predefined labels to select the leaf, spine, and inter-switch link nodes. The underlay protocol is configured to use BGP with EBGP as the protocol type, and the overlay protocol is also set to EBGP.

Now that we constructed the Fabric object stored in the `_fabric` variable, the last step is to create it in the cluster using the EDA Intent API. For this we use the `update_cr` method from the already imported `eda_common` package:

```python title="Finalizing Fabric creation logic in simple_fabrics/intents/simplefabric/eda.py" linenums="1" hl_lines="22"
import eda_common as eda

class EdaBaseConfigHandler:
    def handle_cr(self, sf: SimpleFabric):
        # code omitted for brevity
        _fabric = fabric.Fabric(
            # code omitted for brevity
        )

        eda.update_cr(**_fabric.to_input())
```

The `eda.update_cr(**_fabric.to_input())` line takes care of converting the Fabric object into the input dictionary format expected by the EDA Intent API and calls the `update_cr` method to create or update the Fabric resource in the cluster. The effect of this line is the same as if we were to create the Fabric resource using the UI or `kubectl` by passing the Fabric manifest.

/// details | Full code listing of simple_fabrics/intents/simplefabric/eda.py

Removing the unused imports and putting everything together, the final code of the `simple_fabrics/intents/simplefabric/eda.py` file looks like this:

```python
#!/usr/bin/env python3
import eda_common as eda

import simple_fabrics.deps.fabrics_eda_nokia_com.v5_0_0.api.v1alpha1.pysrc.fabric as fabric
from simple_fabrics.api.v1alpha1.pysrc.simplefabric import SimpleFabric


class EdaBaseConfigHandler:
    def handle_cr(self, sf: SimpleFabric):
        assert sf.metadata is not None
        assert sf.spec is not None

        fabricName = f"sf-{sf.metadata.name}"

        _fabric = fabric.Fabric(
            metadata=fabric.Metadata(
                name=fabricName,
                namespace=sf.metadata.namespace,
            ),
            spec=fabric.FabricSpec(
                leafs=fabric.Leafs(
                    leafNodeSelector=["eda.nokia.com/role=leaf"],
                ),
                spines=fabric.Spines(
                    spineNodeSelector=["eda.nokia.com/role=spine"],
                ),
                interSwitchLinks=fabric.InterSwitchLinks(
                    linkSelector=["eda.nokia.com/role=interSwitch"],
                    unnumbered="IPV6",
                ),
                systemPoolIPV4="systemipv4-pool",
                underlayProtocol=fabric.UnderlayProtocol(
                    bgp=fabric.UnderlayBGP(asnPool=sf.spec.underlayASNPool),
                    protocol=["EBGP"],
                ),
                overlayProtocol=fabric.OverlayProtocol(
                    protocol="EBGP",
                ),
            ),
        )

        eda.update_cr(**_fabric.to_input())

```

///

## UI Category and Resource Naming

Right now, our app shows up in the EDA UI under the "SIMPLE FABRICS" category with the resource named "simplefabrics". These values are derived from the default settings in the `simple_fabrics/manifest.yaml` file created by `edabuilder`.

To demonstrate how to customize these values, let's achieve the following:

* Change the simplefabrics resource name to "Simple Fabrics"
* Change the app category from "SIMPLE FABRICS" to "Fabrics", where the original Fabrics resource is located.

Open the `simple_fabrics/manifest.yaml` file and change the fields under the `ui` category of the SimpleFabrics CRD entry:

```diff title="simple_fabrics/manifest.yaml"
@@ -33,8 +33,8 @@ spec:
         path: simple_fabrics/crds/simple-fabrics.eda.local_simplefabrics.yaml
         schema: simple_fabrics/openapiv3/eda_oas_simple-fabrics.eda.local_simplefabrics.json
         ui:
-          category: Simple Fabrics
-          name: simplefabrics
+          category: Fabrics
+          name: Simple Fabrics
     - script:
         path: simple_fabrics/intents/simplefabric/config_intent.py
         trigger:
```

Redeploying the app and reloading the UI will now show the Simple Fabrics resource under the Fabrics category with the desired name:

-{{image(url="https://gitlab.com/-/project/7617705/uploads/1d6046388ec49680a280b43dc98fee1b/CleanShot_2025-12-11_at_11.51.27.png", title="Customized Resource Name and Category")}}-

## Using the Simple Fabrics App

We have implemented the configuration portion of the Simple Fabrics app; now it is time to see it in action! To do so, redeploy the app one last time to make sure all the latest changes are applied.

```bash
edabuilder deploy --app simple-fabrics
```

Once the app is deployed, open the EDA UI and navigate to the Simple Fabrics resource under the Fabrics category. Click on "Create" to open the schema form for creating a new SimpleFabric resource.

-{{video(url="https://gitlab.com/-/project/7617705/uploads/a18e1452ebb0aaaf9fbd267f4e688c48/sf-demo2.mp4", title="Creating a SimpleFabric Resource")}}-

The video shows how to create a SimpleFabric resource named `my-simple-fabric` using the schema form. We accept the default value for the Underlay ASN Pool field, which is `asn-pool` and add the resource to the transaction basket. We then run the dry run to ensure everything is valid and finally commit the transaction to create the resource.

The creation of the Simple Fabric resource triggers the config intent script we implemented, which in turn creates the underlying Fabric resource with the desired configuration. The created Fabric resource has the lock icon next to it, indicating that it is a **derived resource** - a resource that is created by some other resource and not by a user directly.

## Handling State

We achieved our goal of building a simple abstraction on top of the existing Fabrics app, providing a simplified interface for users to create fabrics with sensible defaults. However, there is one bit that is still missing - our Simple Fabrics resource does not show the status of the underlying Fabric resource. While we can navigate to the derived Fabric resource to see its status, it would be much more convenient if our abstracted resource showed this information directly.

As an EDA developer, you have ultimate freedom to decide what state to show in your resource and how to compute it. In our case, the Simple Fabrics resource does not have any state of its own, so we will simply propagate the state of the underlying Fabric resource to the SimpleFabric resource. To achieve this, we need to create a **state intent** for our SimpleFabric resource.  
The state intent is very similar to the config intent we created earlier, but instead of creating other resources or device-level configuration, it is responsible for fetching the state from the nodes and updating the status of the resource it is associated with.

Let's go over the steps to create and implement the state intent, and since it is very similar to the config intent, we will keep the explanation brief.

### Resource state API

First, we need to extend the SimpleFabric resource API to include a status field that will hold the state information. Open the `simple_fabrics/api/v1alpha1/simplefabric_api_types.go` file and add the fields under the `SimpleFabricStatus` struct:

```go
// SimpleFabricStatus defines the observed state of SimpleFabric
type SimpleFabricStatus struct {
	// +eda:ui:title="Derived Fabric Name"
	// The name of the backing Fabric that the Simple Fabric created.
	FabricName string `json:"fabricName,omitempty"`
	// +eda:ui:title="Operational State"
	// Operational state of the Simple Fabric uses the operational state
	// of the backing fabric.
	OperationalState string `json:"operationalState,omitempty"`
}
```

Via this API declaration, we add two fields to the status of the SimpleFabric resource:

* `fabricName` - holds the name of the underlying Fabric resource created by the Simple Fabrics app.
* `operationalState` - holds the operational state of the Simple Fabric, which we will derive from the operational state of the underlying Fabric resource.

### How State Intents Work

Let's break down how state intents work in EDA and what are the required components by following the sequence of events that happen when we create a Simple Fabric resource. When a SimpleFabric resource is created, to trigger the state intent, the config script should also emit the associated state resource that represents the state intent for the SimpleFabric resource.

-{{diagram(url="nokia-eda/docs/diagrams/simple-fabric", page=1, title="Step 1. Config Intent creates the associated State resource")}}-

When the Config Intent creates the associated State resource, it should pass the necessary information to its spec so that the state intent can use it for fetching the state. In our case, the only information needed is the name of the underlying Fabric resource that was created. Therefore, the state resource spec will have a single field called `fabricName` that holds this information.

The state intent will use the Intent API and its spec to fetch the state it needs, which in our case is the status of the underlying Fabric resource.

-{{diagram(url="nokia-eda/docs/diagrams/simple-fabric", page=2, title="Step 2. State Intent fetches the necessary state using EDA Intent API and EDA DB")}}-

Once the state intent has fetched the necessary state information, it will compute the status fields of the SimpleFabric resource and update it accordingly. The key point here is that the State resource that was originally created by the config intent does not need to have state fields of its own; instead, it computes the state that the SimpleFabric resource has.

-{{diagram(url="nokia-eda/docs/diagrams/simple-fabric", page=3, title="Step 3. Computing the state fields for Simple Fabric resource and updating it")}}-

In other words, the State resource acts as a helper resource that fetches the state for the SimpleFabric resource and updates its status.

### State Resource

Now that we understand the role of a State resource, we need to create one that will represent the state intent for our SimpleFabric resource. Similar to the config intent, we use `edabuilder` to scaffold the state resource for us, but this time we add additional flags to indicate that we want to scaffold a state resource and it should not be visible in the UI[^3].

```bash
 edabuilder create --app simple-fabrics resource SimpleFabricState --scaffold-state --suppress-ui
```

Note how the state resource kind is named `SimpleFabricState`. Appending the `State` suffix to the resource kind when creating a state intent is a convention in EDA.

This command will scaffold a new resource and its API definition in the `simple_fabrics/api/v1alpha1/simplefabricstate_api_types.go` file. Here is how we model the state resource API:

```go
package v1alpha1

// SimpleFabricStateSpec defines the desired state of SimpleFabricState
type SimpleFabricStateSpec struct {
	// FabricName is the name of the underlying fabric that SimpleFabric creates.
	FabricName string `json:"fabricName"`
}

// SimpleFabricStateStatus defines the observed state of SimpleFabricState
type SimpleFabricStateStatus struct {
	// SimpleFabricState has no status.
}
```

And the manifest of our app will be automatically updated by `edabuilder` to register the new resource CRD and its associated state intent script:

```yaml
    - crd:
        path: simple_fabrics/crds/simple-fabrics.eda.local_simplefabricstates.yaml
        schema: simple_fabrics/openapiv3/eda_oas_simple-fabrics.eda.local_simplefabricstates.json
    - script:
        path: simple_fabrics/intents/simplefabricstate/state_intent.py
        trigger:
          kind: SimpleFabricState
        type: state
```

### Creating State Resource in Config Script

Our config intent needs to create an instance of the SimpleFabricState resource each time a SimpleFabric resource is processed. This will trigger the state intent to run and fetch the state for the SimpleFabric resource.

All we need to do is go back to our config handler implementation in the `simple_fabrics/intents/simplefabric/eda.py` file and add the logic to create the state resource after creating the underlying Fabric resource:

```python title="Adding State Resource creation logic to simple_fabrics/intents/simplefabric/eda.py" linenums="1" hl_lines="25-30"
import simple_fabrics.api.v1alpha1.pysrc.simplefabricstate as simplefabricstate

class EdaBaseConfigHandler:
    def handle_cr(self, sf: SimpleFabric):
        # code omitted for brevity

        sf_state = simplefabricstate.SimpleFabricState(
            metadata=simplefabricstate.Metadata(
                name=sf.metadata.name,
                namespace=sf.metadata.namespace,
            ),
            spec=simplefabricstate.SimpleFabricStateSpec(fabricName=fabricName),
        )

        eda.update_cr(**sf_state.to_input())
```

We import the `simplefabricstate` package that was generated by `edabuilder` for the SimpleFabricState resource API. Then, after creating the Fabric resource, we instantiate a SimpleFabricState object with the same name and namespace as the SimpleFabric resource and set its `fabricName` spec field to the name of the underlying Fabric resource we created earlier.

Finally, we call the `eda.update_cr` method to create the SimpleFabricState resource in the cluster. This will trigger the state intent to run and fetch the state for our SimpleFabric resource.

### State Handler

Next, we need to implement the state intent script that will fetch the state from the underlying Fabric resource and update the SimpleFabric status accordingly. As with the config script, the state script follows the same structure, with the main entrypoint being the `process_state_cr` function in the `simple_fabrics/intents/simplefabricstate/state_intent.py` file and a state handler class that implements the logic.

Here is the entrypoint of the state intent:

```python title="simple_fabrics/intents/simplefabricstate/state_intent.py"
#!/usr/bin/env python3
from common.constants import PLATFORM_EDA
from simple_fabrics.api.v1alpha1.pysrc.simplefabricstate import SimpleFabricState
from simple_fabrics.intents.simplefabricstate.init import init_globals_defaults, validate
from simple_fabrics.intents.simplefabricstate.state_handlers import get_state_handler


def process_state_cr(cr):
    sf_state = SimpleFabricState.from_input(cr)
    if sf_state is None:
        return

    validate(sf_state)
    init_globals_defaults(sf_state)

    handler = get_state_handler(PLATFORM_EDA)
    handler.handle_cr(sf_state)
```

The handler logic goes into the `handle_cr` method of the state handler class defined in the `simple_fabrics/intents/simplefabricstate/eda_state.py` file:

```python title="simple_fabrics/intents/simplefabricstate/eda_state.py"
#!/usr/bin/env python3
import eda_common as eda

import simple_fabrics.api.v1alpha1.pysrc.simplefabric as simplefabric
from simple_fabrics.api.v1alpha1.pysrc.simplefabricstate import SimpleFabricState
from utils.state import get_state_params


class EdaStateHandler:
    def handle_cr(self, sf_state: SimpleFabricState):
        _oper_state = "UNKNOWN"
        fabric_path = f'.resources.cr.fabrics_eda_nokia_com.v1alpha1.fabric{{.name=="{sf_state.spec.fabricName}"}}'

        fields = [
            "status.operationalState",
        ]
        fabric_cr_fields = get_state_params(fabric_path, fields, False)
        if not fabric_cr_fields or not isinstance(fabric_cr_fields, dict):
            return

        # Safely access nested dictionary with proper type checks
        status = fabric_cr_fields.get("status")
        if isinstance(status, dict):
            _oper_state = status.get("operationalState", "UNKNOWN")

        sf = simplefabric.SimpleFabric(
            metadata=simplefabric.Metadata(
                name=sf_state.metadata.name,
                namespace=sf_state.metadata.namespace,
            ),
            status=simplefabric.SimpleFabricStatus(fabricName=sf_state.spec.fabricName, operationalState=_oper_state),
        )
        eda.update_cr(**sf.to_input())
```

Here is a breakdown of the code:

1. The `EdaStateHandler` class that has been scaffolded by `edabuilder` contains the `handle_cr` method that we populate with the state fetching logic.
2. Fetching the state. We want to fetch the `operationalState` field from the status of the underlying Fabric resource. We can do this by querying the EDA DB (EDB) using the Intent API utility function `get_state_params`. The steps are as follows:
    2. Define the `fabric_path` variable that holds the EDA DB path to the underlying Fabric resource based on the `fabricName` spec field from the state resource.
    3. Define the `fields` list that contains the status fields we want to fetch from the Fabric resource.
    4. Call the `get_state_params` utility function (available by default) to fetch the specified fields from the Fabric resource using the EDA DB path.
    5. Safely access the nested dictionary to extract the `operationalState` field from the Fabric status.
3. Instantiate a SimpleFabric object with the same name and namespace as the SimpleFabricState resource and set **only its status fields** based on the fetched information.
4. Finally, call the `eda.update_cr` method to update the SimpleFabric resource with the computed status fields.

Now, this state intent will run each time the **SimpleFabricState** resource is created or updated, fetch the state from the underlying Fabric resource, and update the SimpleFabric resource status accordingly. This is a perpetual process, so whenever the underlying Fabric resource state changes, the SimpleFabric resource status will be updated to reflect the latest state.

Deploy the app one last time to apply the state intent changes, and fetch the status of the SimpleFabric resource[^4], for example via `kubectl`:

```bash
kubectl -n eda get simplefabrics my-simple-fabric -o yaml
```

<div class="embed-result">
```{.yaml .no-copy .no-select hl_lines=12-14}
apiVersion: simple-fabrics.eda.local/v1alpha1
kind: SimpleFabric
metadata:
  creationTimestamp: "2025-12-11T11:05:48Z"
  generation: 1
  name: my-simple-fabric
  namespace: eda
  resourceVersion: "55753"
  uid: 373b271e-9cd8-41a7-9e8f-6f43e8098bd6
spec:
  underlayASNPool: asn-pool
status:
  fabricName: sf-my-simple-fabric
  operationalState: up
```
</div>

Beautiful, the status of the SimpleFabric resource now shows the name of the underlying Fabric resource and its operational state, just as we intended!

## Summary

It was a long journey, but app development on EDA is quite rewarding and powerful. Despite the verbose explanations, the actual code we wrote to implement the Simple Fabrics app is quite concise and straightforward. We spent more time explaining the machinery and concepts behind EDA resources and file structure than actually writing code.

With the Simple Fabrics app, we demonstrated how to build an abstraction on top of an existing EDA app by creating a new resource that simplifies the user experience while leveraging the power of the underlying app. This technique can be used to build opinionated variations of existing apps tailored to the design requirements of your organization.

> You can find the resulting code of our application in the [eda-labs/simple-fabrics repository](https://github.com/eda-labs/simple-fabrics).

While we left out many cool features so as not to make this tutorial a novel, you can further explore the development documentation to learn about other EDA capabilities. For example, while we were deploying the app dozens of times today, but we pushed it to the internal development catalog. You probably want to learn how to publish your app to EDA Store, for this - refer to the [Build and Publish](../build-publish.md) guide.

[^1]: Resource kind should be in PascalCase format, starting with an uppercase letter.
[^2]: You can choose any version of the Fabrics app that is compatible with your EDA installation. v5.0.0 is the latest version available for EDA 25.12.1 at the time of writing this tutorial. You can derive the OCI image URL of any Nokia app by appending its name and version to the base URL `ghcr.io/nokia-eda/apps/`.
[^3]: State resources are not meant to be created or managed by users directly, they are merely helpers to trigger the state intent scripts.
[^4]: Assuming you did not delete the SimpleFabric resource created earlier in the tutorial.
