---
resource_name: SNMPServer
resource_name_plural: snmpservers
resource_name_plural_title: SNMP Servers
resource_name_acronym: SS
crd_path: docs/apps/management.eda.nokia.com/crds/management.eda.nokia.com_snmpservers.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# SNMP Server

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

The Simple Network Management Protocol (SNMP) is used to monitor and manage network elements.

Over the decades, multiple versions of SNMP have been created:

- `SNMPv1` ([RFC 1157](https://datatracker.ietf.org/doc/html/rfc1157)) is the original version and has largely been superseded by later versions.
- `SNMPv2c` ([RFC 1901](https://datatracker.ietf.org/doc/html/rfc1901)) is the community-based variant of SNMPv2. It adds protocol operations and operational improvements but retains community-based security.
- `SNMPv3` ([RFC 3414](https://datatracker.ietf.org/doc/html/rfc3414)) adds user-based authentication and privacy features.

The `SNMPServer` resource currently supports `SNMPv2c` and `SNMPv3`.

## SNMP communities

When `SNMPv2c` is selected, access control happens through SNMP communities, which are shared secret strings used to determine which requests the client can make. If the client uses a community that is not known by the SNMP server, the request is rejected.

/// admonition | Community strings are not secure
    type: warning

Although it is a best practice to treat community strings as passwords, they are sent alongside the SNMP request in cleartext. Therefore, SNMPv2c cannot be considered secure. If security is required, prefer SNMPv3 over SNMPv2c.
///

/// details
    type: example

As an example, the following two communities may be used:

- `public` for read-only monitoring requests
- `private` for write (configuration) requests

///

[Access permissions](#permissions) are associated with the community and determine which object identifiers (OIDs) requests using that community can access.

## SNMP users

When `SNMPv3` is selected, a list of `NodeUser` resources that may access the SNMP server must be defined. These users can be selected individually or through label selectors. At least one `NodeGroup` to which each `NodeUser` belongs must have the `SNMP` service enabled.

[Access permissions](#permissions) are associated with the users and determine which object identifiers (OIDs) each user can access.

## Permissions

A community string or user credentials can grant the following levels of access:

- `Read` for read-only access to non-security OIDs
- `ReadWrite` for read and write access to non-security OIDs
- `ReadWriteAll` for read and write access to all OIDs, including security OIDs

## OS-specific implementation notes

On **SR Linux**, SNMP write requests are not supported. The `accessPermission` property is ignored.

Refer to the **SR OS** documentation to see which object IDs are excluded by the `no-security` view, which is used when the access permission is `Read` or `ReadWrite`. For `ReadWriteAll`, the `iso` view is used. Custom views are not currently supported.

## Dependencies

Each `SNMPServer` resource targets either a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), or a [`Router`](-{{ref_app_doc('services', 'router')}}-). While only one of the three is required, all three are listed as dependencies.

### [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-)

If the `SNMPServer` is reachable through a [`ManagementRouter`](-{{ref_app_doc('bootstrap', 'managementrouter')}}-), the resource referenced by the `router` property must exist.

/// note | Management routers cannot be selected through label selectors.
///

### [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-)

If the `SNMPServer` is reachable through a [`DefaultRouter`](-{{ref_app_doc('routing', 'defaultrouter')}}-), the resource referenced by the `router` property must exist.

Label selectors may be used to select multiple [`DefaultRouters`](-{{ref_app_doc('routing', 'defaultrouter')}}-).

### [`Router`](-{{ref_app_doc('services', 'router')}}-)

If the `SNMPServer` is reachable through a [`Router`](-{{ref_app_doc('services', 'router')}}-), the resource referenced by the `router` property must exist.

/// note | Routers cannot be selected through label selectors.
///

## Referenced resources

The `SNMPServer` does not reference any other EDA resources.

## Examples

/// tab | YAML

```yaml
-{{ include_snippet(resource_name) }}-
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
-{{ include_snippet(resource_name) }}-
EOF
```

///

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
