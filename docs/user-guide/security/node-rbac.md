# Node RBAC

Nokia Event-Driven Automation (EDA) supports the use of node RBAC to secure communication between Nokia EDA and nodes. System administrators can configure node security profile, node groups and node users using TACACS.

## Node groups <span id="node-groups"></span>

The `NodeGroup` resource defines a group on a node. It includes RBAC settings and the selection of services to which users belonging to the group have access, and TACACS configuration. A node group has the following attributes:

- an optional name override in `groupName`, allowing the resource name and local group name on the target to be different
- the set of enabled services
- an indicator if the group provides superuser permissions
- a set of rules, being target specific RBAC rules
- mapping to a privilege level in the TACACS container

A `NodeGroupDeployment` resource is used to deploy `NodeGroup` resources to target TopoNodes.

### Rules

Users of for node groups can define a set of rules that are specific to a specified operating system. The **Rules** section of the `NodeGroup` resource includes the following parameters that define a rule:

- An action, which can be one of the following:
    - `Deny`
    - `ReadWrite`
    - `Read`
- An `operatingSystem` - which OS to apply this rule to.
- A `match` - an OS-specific path, for example `interface` for SR Linux, or `configure port` for SR OS.

Rules that match the operating system of the target are deployed to that target.

The default for `action` is set to `ReadWrite`, and to simplify the majority of deployments the `operatingSystem` is set to `srl`.

### Superuser

Nokia EDA supports a `superuser` attribute; if enabled for a node user group, users that belong to the node group can perform all functions on the system, including `sudo` and `root` access, if available.

### TACACS+

System administrators commonly use TACACS+ to authenticate users, and then use the local device to enforce a locally-defined rule set, or role. In Nokia EDA, enforcement uses the privilege level in TACACS+. If TACACS+ is used for authentication and if a privilege level is returned, a user is granted the set of permissions from all groups that match that privilege level and lower (following TACACS+ implementation of higher privilege levels inheriting permissions of lower levels).

**Note:** TACACS+ server configuration is currently done through a `Configlet` application.

### Services

You can select the services (management services such as gNMI, NETCONF, CLI) that a group is allowed in the **Services** field. Select one or more of the following services:

- CLI
- FTP
- gNMI
- gNSI
- gRIBI
- Reflection
- JSON-RPC
- NETCONF

### Default sudo group

The default `sudo` node group is provided during the bootstrap process or playground deployment. This group enables critical services and provides read/write access to all paths. The `NodeGroup` resource is referenced by the admin `NodeUser` resource that is provided with playground KPT package.

The following example shows a `sudo``NodeGroup` resource:

```
apiVersion: core.eda.nokia.com/v1
kind: NodeGroup
metadata:
  name: sudo
  namespace: eda
spec:
  services:
  - GNMI
  - CLI
  - NETCONF
  superuser: true
```

### Creating node groups <span id="create-node-groups"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand **NODE MANAGEMENT**, then click **Node Groups**.

2. If not already selected, click **Resources** from the **Node Users** drop-down list.

3. Click **Create**.

4. Provide the following metadata for this resource:

    - name
    - namespace (if none is selected)
    - labels
    - annotations
  
5. Configure specifications for the node group.

    - Provide a group name. If you do not provide a name, the system uses the resource name.
    - In the **Services** drop-down list, select the services that users who belong to this group can access.
    - Set the **Superuser** field to **True** to make members of this node user group superusers.
  
6. In the **Rules** section, click **Add** to configure rules.

    Set the following fields to define the operating system match rule for this group:

    - **Action**: select an action from the drop-down list
    - **Operating System**: select **srl** for SR Linux or **sros** for SR OS.
    - **Match**: a string to match input against; for example, **interface** for SR Linux or **configure port** for SR OS. Rules here should be specified in the target specific format.
  
7. If TACACS is used for authentication, in the **TACACS** section, select the privilege level.

8. Click **Commit** to commit your change immediately or click **Add To Transaction** to add this item to transactions to commit later.

///

## Node users <span id="node-users"></span>

The `NodeUser` resource defines a node user using the following parameters:

- username and password
- node groups to which the user belongs
- SSH public keys to be deployed for the user

### Creating node users <span id="create-node-users"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand **NODE MANAGEMENT**, then click **Node Users**.

2. If not already selected, click **Resources** from the **Node Users** drop-down list.

3. Click **Create**.

4. Provide the following metadata for the node user:

    - name
    - namespace (if none is selected)
    - labels
    - annotations
  
5. Configure the specifications for this node user.

    In the **Specification** section, provide a username and password for this user.

6. Configure group bindings.

    In the **Group Bindings** section, click **Add**.

    - Select the TopoNodes.
  
        - To use a label selector to select nodes, in the **Node Selector** section, click **Add a Label Selector**.
        - To identify specific nodes, in the **Nodes** section, click **Add item** to select TopoNodes from the drop-down list.
  
    - In the **Groups** section, click **Add** to specify the node groups to which this user belongs.

7. In the **SSH Public Keys** field, click **Add item** to set the SSH public key to deploy for the user.

8. Click **Commit** to commit your change immediately or click **Add To Transaction** to add this item to transactions to commit later.

///

#### `NodeUser` resource

```yaml title="Example: NodeUser resource"
apiVersion: core.eda.nokia.com/v1
kind: NodeUser
metadata:
  name: node-user
spec:
  username: test
  password: testPassword
  groups:
  - admin
  nodeSelector:
  - eda.nokia.com/role=spine
  - eda.nokia.com/role=leaf
  - eda.nokia.com/role=superspine
  sshPublicKeys:
  - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCsYFM9U5hwi+hcZGr5EPjbcneMB+CRmJ1zYDI5wXq8BgtJdXLCqRnsHtdTpfXn5agwGfkMntsw+/whDjJj3HBX6FxAnB9CO/tHw0AZ7wwAagfp5TFkQwGsUVroJlqUfiu1I1yHqNx+etS8DrAAyLtiUMaEvSLztpqjG/4E3TsEvR1pRgt5OkEfX7CX8PIuCtKvuFBh7aaU6W8a5kvInQaL0TrxEWHb3cnqwTryRri+ohtHFaSFvpJsTT07in3j2UwPw8ICpi75xd8PMKC8CIqijIACIHMIADK0qUIhB+VEXhFp0RPihXraX8v+l7IFRBHLHqIW8ygJ5PUXQKx6+p+TRDhCNtuhL7pd+TWFJPqD9bZigIWEYfQE3dQ2ZNabXr+5sOxyeHot1nYUj5TiFLuCtNz36i3TkXNbHfKxuMymoLEiSOZyD2EkKNlzvxiW4RJl2wZAjjg9pqZILNkbkFVNo0gE3QSkr6fzIRFy27xUBWmG8zi06T4iumEvmhL05Ri3cPDzWQa4FoI9kzt1iCgCFqhHioK882CjZoWt9vX5+JqqddKXJV7oix5jlTvKtEQBYFSKTra2Mt+Gwpbn5bG3TtaumtpX4rK9PVPKnfCLccwRnp+mpijxcGA91N7+2Ud9fSPe8JX/jdGfSXAyU1GuCNI/pHjp0ILqFy2GwQseGQ== admin"

```

## Node security profile <span id="node-security-profile"></span>

The `NodeSecurityProfile` resource provides the parameters that define how to secure communication between Nokia EDA and a node. The `NodeSecurityProfile` resource facilitates the configuration, generation, and rotation of TLS certificates, trust bundle management, and secure communication with specified nodes.

### Node selection

In `NodeSecurityProfile` resource, you can select nodes using the following methods:

- by listing the nodes: in the `nodes` field, list the `TopoNodes` to which the profile applies
- by label: in the `nodeSelector` field, select a label that applies to `TopoNodes` that meet the criteria selected. This field can contain a list of label selectors; a `TopoNode` must contain at least one of the labels to inherit the profile's settings.

    A `nodeSelector` set to an empty string (`""`) means that the profile applies to all nodes.

The `nodes` field takes precedence over the `nodeSelector` setting. If multiple profiles match a node's labels, the profile whose name is first in alphabetic order is applied.

### TLS configuration

The `tls` context indicates whether the connection to the node is secure (with TLS) or insecure (without TLS). The absence of the `tls` field implies an insecure connection, while its presence signals a secure connection.

### Nokia EDA-managed certificates

When Nokia EDA is responsible for managing node certificates, the `tls` context must include the following entries:

- `issuerRef`: a reference to a CertManager Issuer, which is responsible for issuing the certificates.

- `csrParams`: the Certificate Signing Request (CSR) parameters define the parameters for certificate generation and rotation.

    - `csrSuite`: the key and digest set to be used for generating the CSR.
    - `commonName`: the common name (CN) to include in the certificate. This value is auto-generated.
    - `country`: the legally registered country of the organization.
    - `state`: the state or province where the organization is located.
    - `city`: the city in which the organization is based.
    - `org`: the name of the organization requesting the CSR.
    - `orgUnit`: the department or division within the organization requesting the certificate.
    - `certificateValidity`: the duration for which the certificate remains valid post-issuance.
    - `SAN` \(Subject Alternative Names\):
        - `dns`: List of DNS names used to access the node.
        - `emails`: Email addresses associated with the certificate.
        - `ips`: IP addresses that the certificate should validate.
        - `uris`: Specific URIs that the certificate needs to authenticate.

The following is an example of a `nodeSecurityProfile` CR where Nokia EDA manages certificates:

```yaml  title="Connect to the Node without TLS"
apiVersion: core.eda.nokia.com/v1
kind: NodeSecurityProfile
metadata:
  name: insecure
  namespace: eda
spec:
  nodeSelector:
    - eda.nokia.com/security-profile=insecure
```

```yaml title="Connect to the Node with a TLS profile managed by Nokia EDA"
apiVersion: core.eda.nokia.com/v1
kind: NodeSecurityProfile
metadata:
  name: managed-tls
  namespace: eda
spec:
  nodeSelector:
    - eda.nokia.com/security-profile=managed
  tls:
    csrParams:
      certificateValidity: 2160h
      city: Sunnyvale
      country: US
      csrSuite: CSRSUITE_X509_KEY_TYPE_RSA_2048_SIGNATURE_ALGORITHM_SHA_2_256
      org: NI
      orgUnit: EDA
      state: California
    issuerRef: eda-node-issuer
```

```yaml title="Connect to the Node with a TLS profile managed outside of Nokia EDA"
apiVersion: core.eda.nokia.com/v1
kind: NodeSecurityProfile
metadata:
  name: unmanaged-tls
  namespace: eda
spec:
  nodeSelector:
    - eda.nokia.com/security-profile=unmanaged
  tls:
    trustBundle: eda-node-trust-bundle
```

### External certificate management

If certificates are managed outside of Nokia EDA, the `tls` section must reference an external trust bundle. The `trustBundle` field contains a reference to a ConfigMap that holds a CA certificate. Nokia EDA uses this CA certificate to verify the node’s certificate whenever it establishes a connection. The trust bundle must be provided if node certificate management is performed outside of Nokia EDA, allowing the node to validate certificates through an external authority.

```yaml title="Connect to the Node with a TLS profile managed outside of Nokia EDA"
apiVersion: core.eda.nokia.com/v1
kind: NodeSecurityProfile
metadata:
  name: example-node-security-profile
spec:
  nodeSelector:
    - "eda.nokia.com/role=leaf"
  tls:
    trustBundle: "node-trust-bundle"
```
