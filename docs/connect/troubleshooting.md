# Troubleshooting Cloud Connect

## Cloud Connect Custom Resources

Connect will introduce and expose four new CRDs in EDA and the EDA Kubernetes environment:

* `ConnectPlugin` - The logical representation of a plugin, created and managed by a running plugin.
* `ConnectPluginActionable` - An actionable is an action that a plugin must take. This can be created by the Connect Core itself or by a user who wants to trigger the action.
* `ConnectPluginHeartbeat` - A plugin sends heartbeats at a well-defined interval, and by doing so, updates this resources linked to its `ConnectPlugin`. When a plugin does not send heartbeats for a while (three times the expected interval), an alarm will be raised by the Core.
* `ConnectInterface` - The logical representation of a physical interface of a bare metal compute. The labels on the `ConnectInterface` are used to label the matching EDA `Interface`, so that they can be used as sub-interface label selectors for EDA `BridgeDomains`.

## Problem: Missing `ConnectPlugin` for deployed plugin

This indicates a connection problem from the plugin towards the EDA Kubernetes cluster. Verify the following information:

* Check the plugin logs for error messages.
* Verify the plugin's configuration, especially the Kubernetes information (location/URL, certificates, user certificates, and so forth).

## Problem: Application connectivity

An application missing connectivity can have multiple causes; here are some of the most common:

* Check whether there are any alarms reported in EDA.
* Check whether there are any transaction results in FAILED state.
* Check whether the bridge domain and VLAN are up, and the VLAN is showing the expected number of UP subinterfaces
* Check the Connect interface corresponding to the hypervisor NIC where you expect to see traffic.
    * If no Connect interface can be found, check the plugin. It is responsible for creating the Connect interface.
    * If a Connect interface can be found, check the status.
        * If it is '', the connect-interface-controller is not online.
        * If it is 'Disconnected', it cannot find an interface to label.
* Check the interface corresponding to the NIC on the SRL that is connected to the relevant hypervisor.
    * If it is not found: the operator has to create the "downlink" interfaces
    * If it is found: check the status
        * If no members with the LLDP information are found, check the LLDP process on the hypervisor and on the SRL node
