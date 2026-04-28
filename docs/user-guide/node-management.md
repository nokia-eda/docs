# Node management

This chapter provides the following information:

- bootstrapping and related procedures
- background information about zero-touch provisioning (ZTP)
- how to display information about and interact with nodes using the following views from the **Nodes** section the Nokia Event-Driven Automation (EDA) UI:
    - Resources view
    - Deleted Resources view
    - Discovered Resources view

## Bootstrapping

The `Init` application generates an initial configuration file for nodes that require bootstrapping. The input to the `Init` application is an `Init` resource, which specifies which TopoNodes to select and for which TopoNodes to create an initial configuration.

The initial configuration file is stored in the artifact server. When nodes connect to NPP, NPP pushes the initial configuration file to the node.

Additionally, the `Init` application generates the Python provisioning script for SR Linux and bootstrap files needed for SR OS or other operating systems. Based on the same selection criteria, a bootstrap file or Python provisioning script is generated for the selected nodes.

The bootstrap file or Python provisioning script ensures that the node boots into the version specified in the TopoNode. The software and any other artifacts are downloaded to the node during ZTP using HTTP/HTTPS.

By default, if no TopoNode selectors are present in the `Init` resource, an initial configuration file is generated for every TopoNode present in Nokia EDA.

### Management interface IP address assignment

The `Init` resource allows you to configure the management interface IP assignment method using DHCP or by defining static IP addresses. For details, see [Enabling DHCP clients](#enabling-dhcp-clients) and [Setting static management IP addresses](#setting-static-management-ip-addresses).

### Saving node configuration on commit

To specify whether the node configuration is saved after each commit or not, in the `Init` CR include the entry `commitSave: true`. The `Init` script must reflect the `commitSave` value in the generated initial configuration.

### Preparing for bootstrapping

Ensure that you meet the following requirements:

- The NodeSecurityProfile resource (for TLS) must be configured to ensure successful onboarding. For details, see [Node security profile](security/node-rbac.md#node-security-profile).

- A node requires the relevant Nokia EDA License resource to be applied. Without this license, the node will not be onboarded.

    ```yaml
    apiVersion: core.eda.nokia.com/v1
    kind: License
    metadata:
      name: eda-license
      namespace: eda-system #(1)!
    spec:
      enabled: true
      data: "ACoAgOlJq7AABoAU6V6W6XAERezbcYa+ZRZLg8M5IyqMgAABAATAEVEQS1bQkNdLTAuMC4qAAACABIATm9raWEuY29tLOVEQQAAAMAAMQCjorJ+SPKP3if9pcD3OhqlyaWK1VE89JWreOWkyOJcbIWO602C+iwp+FFp8AwAAAADAB4ARWRhIGxpY2Vuc2UgSW50ZXJuYWwgVGVzdAAAAAUAHADl0zNnAAAAAABgKWcAAAAAADohaAAAAADAACQAoKr6XCCQCZj1rWFYik1dGbiqG7TWRK2orh+0sjUKXNYBACkAMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwAAAAAAYADAABAAQAAAAAAMAAMAC/KQqX7Di/m1d0zYz9quIyghaHatF0yDvDgK/fFr011Wa/7FN3LO/OoD3aHg8AXQFkOEh6ejQrTlFyNmVJNTNsVW9SMi9JV2xXd1NqMUF3QVh0eEd6LzhGdlp0WXphTkdOQ1RWRnNCQ3wwZ0p2b21pSDNiZHFTSFBYQ2R6d0xxVlNhM3FZZUZuL1BGMnhoSjN6OS8yS3RlVGpmUngreWFNS1NwZ0p5OE12YlBVbmw2TUFpNHRXR1g4U3R0WXFBN21uVUNhVHp5eXpLOWtXcWgwZVZtR1oyV09RTURML0thaWY1RGMva21tc0NVY042RUdNZUNiTmdvV2RKUFlXZ1o4c2hlaG03b2tsZHdsSDBxMXZWdjhHMjZ4OVUxbTd2ellBN3BDNkFXODJyZ3FsaExWTUJxYm11VDdKSzdPWWhzYVp4Q3h4a2lIbWZ5KytNY3FLVHFBUk1McWhYRzRIb290ME0xK1RaRVZTdUJKNFl5a3pkeHdVV3pGZGRZdjg5Ym5uUHBsdXc9PQAAAAA="
    ```

    1. If you changed your base namespace, make sure to update the namespace in the metadata.

- The node's images must be uploaded to the artifacts server before bootstrapping. The upload process is triggered by creating an `Artifact` resource that references the source file by the `remoteFileUrl` field and supports http(s), ftp and sftp protocols.

    ```yaml title="Example Artifact resource to upload the SR Linux image to the artifacts server"
    apiVersion: v1
    kind: Secret
    metadata:
      name: srl-ftp-cred
      namespace: eda
    type: Opaque
    data:
      username: base64(username)
      password: base64(password)
    ---
    apiVersion: artifacts.eda.nokia.com/v1
    kind: Artifact
    metadata:
      name: srlinux-24.10.1-492
      namespace: eda
    spec:
      repo: images
      filePath: srl.bin
      remoteFileUrl:
        fileUrl: ftp://10.10.10.10/eda/srl_images/srlinux-24.10.1-492.bin
      secret: srl-ftp-cred
    ```

### Enabling DHCP clients

To enable the IPv4 and IPv6 DHCP clients on the management interface, in the `Init` resource, include the following entries in the `mgmt`context:

`ipv4DHCP: true`

`ipv6DHCP: true`

In the `mgmt` section, by default, both `ipv4DHCP` and `ipv6DHCP` are set to `true`. Optionally, you can also set the IP MTU, as shown in the following example:

```yaml
apiVersion: bootstrap.eda.nokia.com/v1alpha1
kind: Init
metadata:
  name: init-config
spec:
  nodeSelector:
  - 'eda.nokia.com/role=leaf'
  - 'eda.nokia.com/role=spine'
  - 'eda.nokia.com/role=borderleaf'
  - 'eda.nokia.com/role=superspine'
  - 'eda.nokia.com/role=backbone'
  mgmt:
    ipv4DHCP: true
    ipv6DHCP: true
    ipMTU: 9000
```

/// Admonition | Note
    type: subtle-note
If the `ipv4DHCP` or `ipv6DHCP` parameters are set to `true`, the settings are not reflected in the DHCP client-related config in BOF for SR OS.
///

### Setting static management IP addresses <span id="setting-static-management-ip-addresses"></span>

To set the management IP address statically, the `init` script must use the `productionAddress` setting from the `Toponode` resource as the IPv4 or IPv6 address in the generated configuration.

The `init` script sets the address as either IPv4 or IPv6 and sets the prefix length.

The table below displays the different combinations of `ipv4DHCP`, `ipv6DHCP` and `productionAddress` settings and the corresponding resulting initial configuration.

|Init resource|TopoNode setting|Result|
|-------------|----------------|------|
|`ipv4DHCP: true`|\*|The management interface IPv4 client is enabled in the initial configuration.|
|`ipv6DHCP: true`|\*|The management interface IPv6 client is enabled in the initial configuration.|
|`ipv4DHCP: false`|IPv4 productionAddress is set|The production address is set as the IPv4 address of the management interface in the initial configuration.|
|`ipv4DHCP: false`|IPv6 productionAddress is set|The IPv4 address is left unset in the initial configuration and the IPv4 DHCP client is not enabled.|
|`ipv6DHCP: false`|IPv4 productionAddress is set|The IPv6 address is left unset in the initial configuration and the IPv6 DHCP client is not enabled.|
|`ipv6DHCP: false`|IPv6 productionAddress is set|The production address is set as the IPv6 address of the management interface in the initial configuration.|
|`ipv4DHCP: false` `ipv6DHCP: false`|productionAddress is not set|Results in an error; add productionAddress to TopoNode or enable a DHCP client.|

#### Static Routes

To define the static routes in the `Init` CR, specify an IP prefix and a next hop. The `Init` script adds static routes to the management network instance. For example:

```yaml
apiVersion: bootstrap.eda.nokia.com/v1alpha1
kind: Init
metadata:
  name: init-config
spec:
  nodeSelector:
  - 'eda.nokia.com/role=leaf'
  - 'eda.nokia.com/role=spine'
  - 'eda.nokia.com/role=borderleaf'
  - 'eda.nokia.com/role=superspine'
  - 'eda.nokia.com/role=backbone'
  mgmt:
    ipv4DHCP: true
    ipv6DHCP: true
    ipMTU: 9000
    staticRoutes:
      - prefix: 10.10.0.0/16
        nextHop: 172.16.255.29
      - prefix: 2001:10:10::/64
        nextHop: "200::"
```

## Zero-touch provisioning

Zero Touch Provisioning (ZTP) allows for a device to be installed in a rack, powered on, and without any additional input from an operator, boot up, pull down the software version of its operating system, an initial configuration and any other boot artifacts required for it to be managed.

Most ZTP implementations rely on DHCP to provide an IP address to the DUT and use DHCP options to inform the DUT of the location of any boot artifacts it requires to complete its ZTP process. In SR Linux, the DHCP server provides the URL of a Python provisioning script which is then used by the DUT to perform actions such as software upgrade and applying an initial configuration. In SR OS, the DHCP server provides a URL to a provisioning file which is a text file containing URLs to software images and configuration files.

For devices running SR OS and SR Linux, the devices send a DHCP Discover message with option 61 (client-id) set to the chassis serial number. This setting is used on the DHCP server to associate a DHCP discover message with a specific DUT and allows for the DHCP server to allocate static DHCP leases (IP addresses) and potentially device-specific boot artifacts (Python script or boot file).

Nokia EDA supports the following modes of operation for DHCP aspect of ZTP:

- Use of an internal DHCP server (hosted and managed by Nokia EDA)
- Use of an external DHCP server (hosted and managed outside of Nokia EDA)

To serve the boot artifacts (Python script, boot file, software, or any other files needed during the bootstrapping process), an artifact server must be present in Nokia EDA. An intent is used to allow for artifacts to be added to the server, which is then retrieved by the devices during boot.

### DHCP server

In deployments that use Nokia EDA to handle ZTP in its entirety, a DHCP server is required to provide IP addresses to devices.

When a device issues a DHCP discovery message, the client-id option (61) attribute includes their chassis serial number. This serial number is used to associate real devices with node objects in EDA. Additionally, an IP address is assigned to device via a `Target` object.

The DHCP server must support the following capabilities:

- Static lease assignment using the client-id (option 61) as the binding between an IP address and a device
- Ability to receive DHCP packets from a DHCP relay (the DHCP relay between the devices and the DHCP server)
- When providing an IP address to the device, the DHCP server must be able to populate option 66 or 67 in the DHCP offer. This option provides HTTPs. The URL points to the ZTP provisioning script or boot file hosted on the artifact server.
- Ability to populate other options as required by the operator, for example:
    - Router option 3
    - Time Server option 4
    - Name Server option 5
    - Domain Server option 6
    - Log server option 7
- Support both IPv4 and IPv6 IP addressing

## Working with nodes from the Nokia EDA UI

This section provides information about how to work with nodes using the UI.

### Node Resources view

-{{image(url="graphics/sc0279.png", title="Figure: Nodes Resources view", shadow=true, padding=20)}}-

The following table lists the default columns shown in the **Node Resources** page.

|Column|Description|
|------|-----------|
|Name|The name of the resource.|
|Namespace|The namespace to which this node belongs.|
|Labels|The labels assigned to this node.|
|Annotations|The annotations assigned to this node.|
|NPP|The current state of the connection between ConfigEngine and NPP.|
|NPP Pod|The NPP pod name.|
|NPP Address|The NPP address and port for this TopoNode.|
|Node|The current state of the connection between NPP and the node, which can be one of the following:<br><ul><li>TryingToConnect: NPP is attempting to establish connectivity to the node.</li><li>WaitingForInitialCfg: NPP is connected to the node but is waiting for the initial config to push.</li><li>Committing: NPP is in the process of committing.</li><li>RetryingCommit: NPP lost sync to the node and is re-pushing current config.</li><li>Synced : NPP is in a fully synched state.<li>Standby: On geo-redundant clusters, NPP is running in standby mode</li><li>NoIpAddress: NPP is running, but the node has no IP address; occurs only in simulator setups when CX has not created the simulated node or the simulated pod failed to launch because of an image error.</li></ul>|
|Node Address|The address and port used to connect to the node.|
|Platform|The operational platform type of this node.|
|Version|The software version of this node.|
|Onboarded|Indicates if the node has been bootstrapped or is reachable using the configured credentials.|
|Operating System|The operating system running on this node.|
|MAC Address|The MAC address associated with this node.|
|Serial Number|The serial number of this node.|
|System Interface|Deprecated - no longer used.|
|License|The reference to a ConfigMap containing a license for the TopoNode.|
|Components|Details about the hardware:<br><ul><li>Kind: identifies the component, for example, if it is a line card.</li><li>Type: the type of hardware provisioned.</li><li>Slot: the slot in which this component resides. 1 indicates the line card in slot 1, 1/1 indicates line card slot 1, mda slot 1.|
|Mode|The mode in which this node is functioning: <br><ul><li>`Normal`: (the default) indicates that NPP is expecting an endpoint to exist and accepts and confirm changes only if the endpoint accepts them.</li><li>`maintenance`: no changes accepted for the TopoNode, regardless of whether the endpoint is up and reachable, except if an upgrade is occurring, in which case changes are accepted.</li><li>`null`: changes are accepted from CRs and no NPP is spun up. NPP validation does not occur.</li><li>`emulate`: changes are accepted at the NPP level, without pushing them to a endpoint. NPP validation still occurs. Also displayed if no IP address is present.</li></ul>|
|Node Profile|The node profile applied to this node.|
|Production address:|The production addresses that this TopoNode uses.|

Click the **Row actions menu** for a node to display the actions that you can perform on the node. For example:

-{{image(url="graphics/sc0280.png", title="Figure: Row actions", scale=0.25, shadow=true, padding=20)}}-

You can select from one of the following options:

- **View**: display details about a selected node, including status, mode of operation, and so forth.

    You can also double-click a node from the list to display the details for a node.

- **Edit:** edit the settings of a node
- **Duplicate**: create a new TopoNode based on an existing node
- **Delete**: delete a node
- **Node Configuration**: view the node configuration (its CR)
- Under the **Workflows** options, you can run the following tasks with the node as the target:
    - update the image of the node
    - ping the node
    - create a help package for tech support
    - do a route lookup
    - do a route trace
    - do an attachment lookup

    For more information about these workflows, see [Workflow Definition List page](workflows.md#workflow-definition-list-page).

### Creating a TopoNode

/// html | div.steps

1. Create a new node from the **Node Resource** view using one of the following options.

    - Create a new node by copying the settings of an existing node. Locate the node and click the **Table row actions** icon at the end of its row. Select **Duplicate**. In the form that displays, some fields are pre-populated, but you need to provide node-specific information, such as the name, MAC address, serial number, license, and production addresses for the new node.
    - Click **Create**. In the form that displays, the fields are all blank.

2. Configure the metadata for this node.

    Provide the following information:

    - Name of the node.
    - Labels for the node.
    - Annotations for the node.

3. Enter the specifications for the TopoNode. If you duplicated a node, verify the pre-populated settings and modify as needed.

    Provide the following information:

    - Platform
    - Version
    - Onboarded
    - Operating System
    - Node Profile
    - MAC Address
    - Serial Number (deprecated)
    - System Interface
    - License

4. In the Components section, click **+ Add**.

    In the form that opens, provide the following information for the node you are provisioning:

    - the kind of component
    - the type
    - the slot in which this component resides

5. Set the production address for this node.

    These settings are required if the TopoNode is not bootstrapped by Nokia EDA. If left blank, an address is allocated from the management IP pool specified in the referenced NodeProfile resource.

    Click the **Specification \| Production Address** toggle to enter the IPv4 and IPv6 production addresses for this node.

6. Specify the operating mode of the node.

    The default setting is normal.

///

### Deleted Resources page

The **Deleted Resources** page displays all of the nodes that have previously been deleted from the system. From here you can view details about the reverted nodes, and if necessary, revert the deletion.

-{{image(url="graphics/sc0281.png", title="Figure: The Deleted Resources view", shadow=true, padding=20)}}-

|\#|Name|Function|
|:---:|----|--------|
|1|Actions menu|Use the Actions menu to perform the following actions on a selected node:<br><ul><li>**View**: Opens the Detail view for the deleted node, clearly marked as a deleted version. Buttons on this view allow you to **Cancel** (close the Detail view) or **Revert** (to open the Revert view for this deleted node).</li><li>**Revert**: Opens the **Detail** view for the deleted node, clearly marked as a deleted version. Buttons on this view allow you to **Revert** (to immediately restore this configuration of the deleted node) or **Add to Transaction** (to add the reversion to a transaction to be committed later).</li></ul>|

The list of nodes in the **Deleted Resources** page displays the following columns by default:

|Column|Description|
|------|-----------|
|Name|The name of the deleted node.|
|Namespace|The namespace to which the deleted node belonged.|
|Transaction ID|The ID of the transaction within EDA that deleted this node.|
|Commit Hash|The commit hash for the commit within EDA that deleted this node.|
|Commit Time|The date and time at which the deletion of this node was committed.|

### Discovered Nodes page

The **Discovered Nodes** page contains a list of discovered nodes that have not been assigned to a fabric. When a discovered node is assigned to a fabric, it is removed from the Discovered Nodes list and added to the main list of nodes.

|\#|Name|Function|
|:---:|----|--------|
|1|Actions menu|Use the Actions menu to perform the following actions on a selected node:<br><ul><li>**Create new node**: Allows you to create a node from scratch or from an existing node</li><li>**Associate to existing node**: Allows you to copy relevant discovered node fields into a selected existing node.</li></ul>|

The list of nodes in the **Discovered Nodes** view displays the following columns by default.

|Column|Description|
|------|-----------|
|Client ID|Indicates the ID sent by the client. The Client ID may refer to serial numbers, MAC addresses, or any other arbitrary string.|
|Version|Indicates the software version of the selected node.|
|Client ID Type|Indicates a string provided by the client.|
|Hardware Address|The MAC address of the client.|
|IP Address|The IP address of the client.|
|Last Received|Indicates the time at which a packet was last received by the client.|
|Namespace|Indicates the namespace to which the node belongs.|
|Node Name|Indicates the name of the node.|
|Relay Circuit ID|The parsed version of the Relay Info, indicating only the Circuit ID value, if any.|
|Relay Info|A raw dump of options passed by the DHCP, if any.|
|Relay Remote ID|The parsed version of the Relay Info, indicating only the Remote ID value, if any.|
|Transaction ID|The DHCP protocol specific transaction ID.|
|Vendor Class|The vendor class of the client.|

### Creating a new node

You can create a new node from scratch or from an existing node.

/// html | div.steps

1. At the right side of the Discovered Nodes list, click the **Table row actions** button.

2. Click **Create a new node**.

    EDA opens the Create a new node page. To create a new node from scratch, go to step [3](node-management.md#nm-step3). To create a new node from an existing node, go to step [4](node-management.md#nm-step4).

3. <span id="nm-step3"></span>To create a node from scratch:

    1. In the Create a new node page, click **Skip**.

        A blank form opens where you can create a new node from scratch.

    2. Fill out the following required fields:

        - Name
        - Namespace
        - Platform
        - Version
        - Operating System
        - Node Profile

    3. Click **Commit** to commit your change immediately or click **Add To Transaction** to add this item to transactions to commit later.

4. <span id="nm-step4"></span>To create a node from an existing node:

    1. In the **Create a new node** page, select a single existing node from the list.

    2. Click **Next**.

        A pre-filled form opens where relevant values are taken from the existing node. The following fields are pre-filled:

        - Namespace
        - Labels
        - Platform
        - Version
        - Operating System
        - Node Profile

    3. Fill out any remaining required fields.

    4. Click **Commit** to commit your change immediately or click **Add To Transaction** to add this item to transactions to commit later.

///

### Associating to an existing node

You can associate a selected discovered node to an existing node.

/// html | div.steps

1. At the right side of the Discovered Nodes list, click the **Table row actions** button.

2. Click **Associate to existing node**.

    Nokia EDA opens the **Associate to existing node** page where you can select an available existing node to associate the discovered node to.

3. Click **Next**.

    After a discovered node has been associated with an existing node, the discovered node is removed from the Discovered Nodes list.

///

## Retrieving log files from nodes

The `edactl node log` command retrieves logs from all nodes. You can specify a node to limit the logs retrieved to that specific node (see the example that follows).

/// Admonition | Note
    type: subtle-note
This command is supported only on SR Linux nodes.
///

Use the following options to filter the logs retrieved:

- `--debug <app>`: Retrieves debug logs for the specified application, matching the filename on the filesystem (for example, sr_bgp_mgr).
- `--errors`: Retrieves only error-level logs.
- `--from <timestamp>`: Sets the start of the collection period; retrieves only logs with a timestamp greater than or equal to the supplied value.
- `--to <timestamp>`: Sets the end of the collection period. Use with `--from` to define an interval.
- `--prior <duration>`: Retrieves logs from the most recent duration (for example, `5m` for the last five minutes).  When combined with `--to`, the collection window is limited to the period ending at the `--to` timestamp; if `--to` is absent, the window ends at the current time.
- `--ignore  <severity>`: Ignores logs with certain severities. For example, `--ignore NI` ignores notification and informational logs.

You can enter a timestamp in one the following formats:

- Syslog format: `Aug 21 03:48:00`
- Linux date format: `Apr 16 09:41:30 AM PDT 2026`
- RFC3339 format: `2025-08-20T19:20:03.487197+00:00`

```title="Example: Retrieving logs from the <code>leaf-1</code> node in the <code>eda</code> namespace"
edactl node log leaf-1 -n eda

Sep 28 04:56:16 leaf-1 sr_supportd: log|13683|13683|00001|I: File /var/log/messages has been rolled over
Sep 28 04:56:20 leaf-1 sr_aaa_mgr: aaa|3227|13661|00059|N: Opened session 2243 for user admin from host 10.244.0.213 in network-instance mgmt
Sep 28 04:56:20 leaf-1 sr_aaa_mgr: aaa|3227|13661|00060|N: User admin on session 2243 successfully authenticated from host 10.244.0.213 in network-instance mgmt
Sep 28 04:56:20 leaf-1 sr_aaa_mgr: aaa|3227|13661|00061|N: Closed session 2243 for user admin from host 10.244.0.213 in network-instance mgmt
Sep 28 04:56:30 leaf-1 sr_aaa_mgr: aaa|3227|13668|00035|N: Opened session 2244 for user admin from host 10.244.0.213 in network-instance mgmt
Sep 28 04:56:30 leaf-1 sr_aaa_mgr: aaa|3227|13668|00036|N: User admin on session 2244 successfully authenticated from host 10.244.0.213 in network-instance mgmt
Sep 28 04:56:30 leaf-1 sr_aaa_mgr: aaa|3227|13661|00062|N: Closed session 2244 for user admin from host 10.244.0.213 in network-instance mgmt
Sep 28 04:56:40 leaf-1 sr_aaa_mgr: aaa|3227|13668|00037|N: Opened session 2245 for user admin from host 10.244.0.213 in network-instance mgmt
Sep 28 04:56:40 leaf-1 sr_aaa_mgr: aaa|3227|13668|00038|N: User admin on session 2245 successfully authenticated from host 10.244.0.213 in network-instance mgmt
Sep 28 04:56:40 leaf-1 sr_aaa_mgr: aaa|3227|13661|00063|N: Closed session 2245 for user admin from host 10.244.0.213 in network-instance mgmt`
```
