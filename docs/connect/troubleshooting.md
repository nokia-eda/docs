# Troubleshooting Cloud Connect

## Cloud Connect Custom Resources

Connect will introduce and expose four new CRDs in EDA and the EDA Kubernetes environment:

* `ConnectPlugin` - Logical representation of a Plugin, created and managed by a running Plugin.
* `ConnectPluginActionable` - An Actionable is an action that a Plugin must take, this can be created by the Connect Core itself or by a User who wants to trigger the action.
* `ConnectPluginHeartbeat` - A Plugin will send heartbeats at a well-defined interval and by doing so will update this resources linked to its `ConnectPlugin`. When a Plugin does not send heartbeats for a while (three times the expected interval), an alarm will be raised by the Core.
* `ConnectInterface` - Logical representation of a physical interface of a bare metal compute. The labels on the `ConnectInterface` are used to label the matching EDA `Interface`, so that they can be used as sub-interface label selectors for EDA `BridgeDomains`.

## Problem: Missing `ConnectPlugin` for deployed plugin

This indicates a connection problem from the Plugin towards the EDA Kubernetes cluster. Verify the following information:

* Check the Plugin logs for error messages
* Verify the Plugin's configuration, especially the Kubernetes information (location/url, certificates, user certificates, ...)

## Problem: Application connectivity

Application missing connectivity can have multiple causes, here are some of the most common:

* Check whether there are any alarms reported in EDA
* Check whether there are any transactionresults in FAILED state
* Check whether bridgedomain and vlan are up, and vlan is showing the expected number of UP subinterfaces
* Check ConnectInterface corresponding to the hypervisor nic where you expect to see traffic
    * If no ConnectInterface can be found, check the Plugin. It is responsible for creating the ConnectInterface.
    * If a ConnectInterface can be found, check the status.
        * If it is '' the connect-interface-controller is not online
        * If it is 'Disconnected' it cannot find a Interface to label
* Check the Interface corresponding to the NIC on the SRL that is connected to the relevant hypervisor
    * If it is not found: operator has to create the "downlink" interfaces
    * If it is found: check the status
        * If no members with the lldp info are found, check the lldp process on the hypervisor and on the SRL node
