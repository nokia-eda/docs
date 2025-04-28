# Configuration scripts

Configuration scripts execute in Config Engine, and are deterministic, run-to-completion logic that is responsible for deriving the set of configurations to push to targets. Scripts can do this by either creating any other resource (like the script in the `Fabric` app creates VNET resource and so on), or by directly emitting `NodeConfig` resources - being the lowest level resource that is pushed to a target.

Due to executing in Config Engine, configuration scripts are limited to the following libraries available in its runtime:

* `eda_common`
* `eda_config`, for interacting with allocation pools (resources)

## Triggering scripts

A configuration script is _attached_ to a particular resource via the applications `manifest.yaml`:

```yaml hl_lines="15-19" title="snippet of the Banner app manifest"
apiVersion: core.eda.nokia.com/v1
kind: Manifest
metadata:
  name: banners
spec:
  components:
    - crd:
        api:
          expose: readWrite
        path: banners/crds/banners.eda.local_banners.yaml
        schema: banners/openapiv3/eda_oas_banners.eda.local_banners.json
        ui:
          category: Banner
          name: Banner
    - script:
        path: banners/intents/banner/config_intent.py
        trigger:
          kind: Banner
        type: config
```

The manifest presented above results in the logic contained in `banners/intents/banner/config_intent.py` script being run whenever a `Banner` resource is created or updated. The `Banner` resource is added to the EDA API via the `crd` component defined in the same manifest file.

## Entrypoint

The entrypoint to a configuration script is the `process_cr` function, which is called by Config Engine with the resource object passed as a dictionary to the function.

```python
def process_cr(cr):
    """Process Banner CR."""
    ...
```

The main task of a configuration script is to take this input dict which represents the declarative abstracted intent and either directly transform it to the node-specific configuration blob, or to emit sub-resources which will be processed by other scripts.

The configuration script also emits the input for the [state](state.md) script and triggers its execution.

<!-- TODO: Add example of retrieving resources -->
<!-- ## Retrieving resources

Configuration scripts

## Updating resources

Configuration scripts can create or update resources via the `eda_common` library. -->

<!-- ## Interactions with namespaces -->

<!-- ## Interactions with allocation pools -->
