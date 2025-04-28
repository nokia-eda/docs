# State scripts

State scripts enable EDA's unique ability to provide and act on the state of abstracted resources. They are being executed inside State Engine and are responsible for alarm generation, subscription and normalization of telemetry data, and publishing updates to the status field of resources, or the creation of state-only resources.

State scripts perform more work than just providing the state of a declarative abstracted intent. It adds operational capabilities to the EDA platform in a broad sense.

## Triggering scripts

A state script is _attached_ to a particular resource via the applications `manifest.yaml` exactly the same way as [configuration script](config.md#triggering-scripts):

```yaml hl_lines="10-14" title="snippet of the Banner app manifest"
apiVersion: core.eda.nokia.com/v1
kind: Manifest
metadata:
  name: banners
spec:
  components:
    - crd:
        path: banners/crds/banners.eda.local_bannerstates.yaml
        schema: banners/openapiv3/eda_oas_banners.eda.local_bannerstates.json
    - script:
        path: banners/intents/bannerstate/state_intent.py
        trigger:
          kind: BannerState
        type: state
```

The manifest presented above results in the logic contained in `banners/intents/bannerstate/state_intent.py` script being run whenever a `BannerState` resource is created or updated. The `BannerState` resource is added to the EDA API via the `crd` component defined in the same manifest file.

The state-related custom resource (`BannerState` in the example above) is typically created by the configuration script attached to the resource it represents.

## Entrypoint

Again, similar to configuration scripts, the entrypoint to a state script is the `process_state_cr` function, which is called by State Engine with the state resource object passed as a dictionary to the function.

```python
def process_state_cr(cr):
    """Process Banner State CR."""
    ...
```

The state script then can:

* query the EDA in-memory database (EDB) for more state information using `eda_state.list_db` method
* update the EDB using `eda_state.update_db` method
* generate alarms using `eda_state.update_alarm` method when thresholds are crossed
* normalize paths and present the state data in a vendor-agnostic way
