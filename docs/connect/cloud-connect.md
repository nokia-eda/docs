# Cloud Connect

## Overview

The EDA Cloud Connect solution (or "Connect") acts as a bridge between EDA and different cloud environments like Red Hat OpenShift, VMware vSphere and others.

Connect is aware of the different processes and workloads running on the servers that make up the cloud environment, while at the same time being aware of the fabric as configured on EDA itself.

This dual awareness enables Connect to configure the fabric dynamically based on workloads coming and going on the cloud platform. It does this by inspecting the cloud itself and learning the compute server, network interface and VLAN on which a specific workload is scheduled. By also learning the topology based on the LLDP information arriving in the fabric switches, it connects those two information sources.

## Components

The Connect solution is built around a central service, called the Cloud Connect Core, and plugins for each supported cloud environment.

The Connect Core is responsible for managing the plugins and the relation between Connect Interfaces (compute interfaces) and EDA Interfaces (Fabric Interfaces or Edge-Links). It keeps track of the LLDP information of EDA Interfaces and correlates that back to the Connect Interfaces created by Plugins to identify the different physical interfaces of the computes of a cloud environment.

Connect Plugins are responsible for tracking the state of compute nodes, their physical interfaces, the virtual networks created in the cloud environment and their correlation to the physical network interfaces. As applications create networks and virtual machines or containers, the plugins will inform Connect Core of the changes needed to the fabric. Plugins will also create or manage EDA Bridge Domains to make sure the correct sub-interfaces are created for the application connectivity.

## Installation of Cloud Connect Core

Cloud Connect is an Application in the EDA App eco-system. It can be easily installed using the App Store UI.

As an alternative, you can also create an `AppInstall` resource in the Kubernetes cluster of EDA with the following content:

=== "YAML Resource"
    ```yaml
    --8<-- "docs/connect/resources/connect-appinstall.yaml"
    ```

=== "`kubectl apply` command"
    ```bash
    kubectl apply -f - <<EOF
    --8<-- "docs/connect/resources/connect-appinstall.yaml"
    EOF
    ```
