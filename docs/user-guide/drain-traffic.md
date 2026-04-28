# Draining traffic

Draining is the concept of gracefully reducing traffic on a device to reduce the risk and reduce the impact of some planned or unplanned activity. Common examples include:

- Removing a device from service to perform a maintenance activity, such as an upgrade.
- Mitigating traffic loss during a brown out or similar event, that is, a fabric module failure in a system that has no fabric redundancy.

In Nokia EDA, draining uses a `Drain` resource to select the default routers to drain traffic from default routers. The `Drain` resource:

- modifies routing policies to ensure that the selected default router is used only for terminating traffic, that is, all traffic that has another route would use those other routes (unless they were also being drained)
- generates an alarm that a drain is present on the default router
- generate a `DrainState` resource to update the set of nodes where the `Drain` resource is present

You can set the following attributes in the `Drain` resource to select the target default routers using label selectors or by listing the target routers:

- `defaultRouterSelector`: specify a label
- `defaultRouters`: list the `DefaultRouters` resources

```
apiVersion: routing.eda.nokia.com/v1alpha1
kind: Drain
metadata:
    name: drain-redundancy-group-a
    namespace: eda
spec:
   defaultRouterSelector:
   - 'eda.nokia.com/redundancy-group=a'
```

**Note:** After a `Drain` resource is applied, the system raises the relevant Drain Active alarms, which are cleared upon deleting the drain.
