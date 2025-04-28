# Debugging

<small>Generic debugging capabilities first introduced in 25.4.1</small>

EDA script apps run in a remote execution environment (config or state engine, depending on the script type) and this makes the usual debugging techniques not easy to apply. Adding `print` statements to the script files and fish for a printed message in a potentially very crowded stream of logs messages is not a great developer experience.

Yet, it is crucial to give developers a way to introspect the data their scripts operate on or produce. And EDA has a built-in mechanism to help with that.

## `edactl` debug

If you look at the demo `banners` application scaffolded by `edabuilder`, you will notice that both configuration and state scripts[^1] have the `log_msg`[^2] function; it is used to log debug messages in such a way that can be intercepted by the `edactl` tool and printed out for you on demand. During the normal application operation no debug messages are being printed, they are only printed when a developer uses `edactl intent debug` command.

To start debugging a state or a configuration script, use the following command:

```shell
edactl -n <namespace> intent [config | state] debug <resource kind>
```

Let's see how this debugging workflow works.

## Logging and monitoring

To get us a clean start, let's remove any instances of the Banner resource from your cluster:

```shell
kubectl delete --all -A banners.banners.eda.local
```

We will start with a basic task of seeing what exactly happens within our Banner application when we create the Banner resource. We can use the `edactl intent config debug <config resource kind>` command to start monitoring the logs of this app.

Split the shell in two panes, and start the debug monitor in the left pane:

```shell
edactl intent config debug banners
```

This starts a debug monitor for the configuration intent of the `banners` app. The associated intent script is going to run when we create the Banner resource that triggers the script to run in the config engine pod. Let's create one in the right panel:

```shell
cat << 'EOF' | kubectl -n eda apply -f -
apiVersion: banners.eda.local/v1alpha1
kind: Banner
metadata:
  name: demo-banner
  namespace: eda
spec:
  nodes:
    - leaf11
  loginBanner: Hello EDA!
EOF
```

Immediately after creating the Banner resource you should see the debug messages appear in the left pane:

-{{video(url='https://gitlab.com/rdodin/pics/-/wikis/uploads/556640d8eebd97c1c76b7055e1c44172/eda-debug1.mp4')}}-

The debug monitor will show the `Input CR` that triggered the intent script to run as well as every `log_msg` function call. For instance, the following output that you find in the output:

```
Banner CR:
{"metadata": {"name": "demo-banner", "namespace": "eda"}, "kind": "Banner", "spec": {"loginBanner": "Hello EDA!", "nodes": ["leaf11"]}}
```

comes from the `log_msg` function defined in the `config_intent.py` script of the Banner app:

```python
from utils.log import log_msg

def process_cr(cr):
    """Process Banner CR."""
    log_msg("Banner CR:", dict=cr) #(1)!
```

1. This log message is rudimentary, since the Input CR is printed by default by the debug monitor.

/// admonition | `log_msg`
    type: subtle-note
The `log_msg` function has the following signature:

```python
def log_msg(*msg, dict=None)
```

///
You can also see that the debug output outputs any Errors raised during the script execution, and we happen to have one in the script:

```
Error:
Traceback (most recent call last):
  File "banners/intents/banner/config_intent.py", line 40, in process_cr
```

Having a look at the line 40 in our `config_intent.py` file we can spot what raises that:

```python linenums="34"
    if cr_obj.spec.nodes is not None and len(cr_obj.spec.nodes) > 0:
        for node in cr_obj.spec.nodes:
            if node not in nodes:
                node_cr = nutils.get_node(name=node)
                if node_cr is None:
                    msg = f"Node {node} not found"
                    raise e.InvalidInput(msg) #(1)!
```

1. The error is raised using the utility module `import utils.exceptions as e` which has different classes for different types of errors.

Since our input CR provided a node name in the `nodes` field of the spec, the script went up querying the TopoNode resources for the one with the name `leaf11`, but our topology does not have such a node. This raised an error and our script execution stopped. Thanks to `edactl intent debug` we can clearly find the error in the logs.

Let's fix our typo in the node name by passing a corrected Banner resource that references the `leaf-1` node that we have in our topology:

```shell
cat << 'EOF' | kubectl -n eda apply -f -
apiVersion: banners.eda.local/v1alpha1
kind: Banner
metadata:
  name: demo-banner
  namespace: eda
spec:
  nodes:
    - leaf-1
  loginBanner: Hello EDA!
EOF
```

With the corrected resource our debug monitor shows that the script completes and displays the resources the script generated and written to the EDB:

-{{video(url='https://gitlab.com/rdodin/pics/-/wikis/uploads/383083029322d1af97e418972a2ed665/eda-debug2.mp4')}}-

The config script for the Banner app generated two custom resources during its run:

1. `BannerState` resource to trigger the state script
2. `NodeConfig` resource that contains the configuration snippets for the nodes matching our node selection.

Similarly, you can debug state scripts by changing the command to `edactl -n <namespace> intent state debug <state resource kind>`

## Triggering your resource

In the previous section we triggered the configuration script execution by creating or changing the `Banner` resource. But during the development cycle it is not convenient to delete+add or modify the resource whenever you want the config or state script to run.

To assist with this workflow, the `debug` subcommand is equipped with the `--trigger | -t` flag that can be used to trigger the associated script to run as if the resource was created or changed. Here is a demonstration of this in action.

If we were to start the debug monitor for the bannerstate resource just like before, we would not see anything in the output, because the BannerState resource has been created once the config script finished execution.

```shell
edactl -n eda intent state debug bannerstate
Matched 1 instances in namespace eda
```

If we want to run our state script again without republishing BannerState CR, we could add the `-t` flag to the command, and this would trigger the script execution with the same BannerState CR passed to it as was recorded before:

```shell
edactl -n eda intent state debug bannerstate -t
```

<div class="embed-result">
```{.text .no-copy .no-select}
Matched 1 instances in namespace eda
Triggered 1 instances
────────── eda BannerState/v1alpha1/BannerState demo-banner ───
InputCR:
    {
      "kind": "BannerState",
      "metadata": {
        "name": "demo-banner",
        "namespace": "eda"
      },
      "spec": {
        "nodes": [
          "leaf-1"
        ]
      }
    }
Stdout:
BannerState CR:
{"kind": "BannerState", "metadata": {"name": "demo-banner", "namespace": "eda"}, "spec": {"nodes": ["leaf-1"]}}

InputDb:
OutputDb:
  .namespace{.name=="eda"}.resources.cr-status.banners_eda_local.v1alpha1.banner{.name=="demo-banner"}
    -> {"apiVersion":"banners.eda.local/v1alpha1","kind":"Banner","metadata":{"name":"demo-banner"},"status":{"nodes":["leaf-1"]}}
Subscriptions:

```
</div>

The trigger flag can be added to both config and state intents.

[^1]: You will find them by the following paths:

    * `banners/intents/banner/config_intent.py`
    * `banners/intents/bannerstate/state_intent.py`

[^2]: imported with `from utils.log import log_msg`
