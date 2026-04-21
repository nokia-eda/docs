# Remote directories

EDA supports the use of external directories that the system can use to authenticate users who were not created locally on the system.

Federated users are imported the first time a user logs in or when the user list is read via the EDA API/UI. Additionally, you can configure periodic sync of created and updates users.

In the EDA UI, federated users are identified in the **Federated Users** field in **User Management Users** page.

**Note:** EDA only supports unsynchronized mode for Keycloak federation providers. This mode imports users and groups into EDA's Keycloak database, but does not write local changes back to the Lightweight Directory Access Protocol (LDAP) server.

The EDA API does not expose the full synchronization options from Keycloak to the federation provider. If full synchronization is required, it can be triggered via the Keycloak Administration Console.

EDA API server blocks all edits to federated users except for adding or removing the user to local groups. Local changes to federated groups are not supported; federated group membership must be configured on the LDAP server.

## Configuring remote directories

EDA supports:

- the configuration of up to five directories
- LDAP and Active Directory directories
- user synchronization from the directory
- group synchronization from the directory and user group membership mapping
- limiting imported users and groups using LDAP filters

When a remote directory is configured, system administrators can continue to create local users in EDA.

## Configuring TLS truststore for remote directories

When connecting a federation provider using LDAPS or STARTTLS, Keycloak must trust the server's TLS certificate authority. To add certificate authorities to the EDA Keycloak truststore, create a Kubernetes secret named `ldap-ca-secret` of type `Opaque` in the EDA base namespace with a base64 encoded PEM certificate in the `ca` field. For example:

```
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: ldap-ca-secret
  namespace: eda-system #Enter the base namespace of your EDA installation
data:
  ca: <base64(certificate authority)> # Base64 encoded PEM certificate
```

EDA monitors this secret and if it changes, EDA updates the certificate authority information used by Keycloak. Modifying the authority information results in a restart of the Keycloak server.

**Parent topic:** [Securing access to EDA](secure-access-eda.md)

## Configuring a federation <span id="configure-federation"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT** and select **User Management**.

2. From the **User Management** drop-down list, click **Federations**.

3. Click **Create**.

4. Configure settings for this federation instance.

    - a unique name
    - the LDAP provider Vendor
    - **Enabled**
    - **Import Users**

        **Note:** By default, this field is set to True; this field is ready-only.

5. Configure LDAP server settings.

    Set the following parameters:

    - **Connection URL**
    - **Use TLS**

        **Note:** If this field is set to True, the certificate should be established on the LDAP server side. After configuring certificate from LDAP server, create the LDAP CA secret (`ldap-ca-secret`) on the platform where EDA is managed.

    - **Bind Type**
    - **User DN**
    - **Username LDAP Attribute**
    - **Timeout**

        Click **Test Connection** to test the connection to the LDAP server.

    - **RDN LDAP Attribute**
    - **ID Attribute**
    - **User Object Classes**
    - **User Search Filter**
    - **Search Scope**
    - **Pagination**
    - **Periodic Sync**
    - **Read Only**
  
6. Enable and configure support for bind credentials.

    Set the following parameters:

    - **Bind Credential**
    - **Bind DN**
    Click **Test Authentication** to verify that the credentials are valid.

7. Enable and configure group federation support.

    If group support is disabled, groups are not synchronized with EDA. If group support is enabled, set the following parameters:

    - **Object Classes**
    - **Group LDAP DN**
    - **Name LDAP Attribute**
    - **Member Attribute**
    - **Membership Attribute Type**
    - **Membership User Attribute**
    - **Filter**
    - **Retrieval Strategy**
    - **Member Of Attribute**

8. Click **Save**.

///

## Deleting a federation <span id="delete-federation"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT** and click **User Management**.

2. From the **User Management** drop-down list, click **Federations**.

3. You can delete one federation or multiple federations at a time.

    - Locate the federation that you want to delete and at click **Delete** from the **Table row actions** menu.
    - Alternatively, you can select more than one federation, then, click the **Table settings &amp; actions** menu on the upper right of the page and select **Delete**. Click **Save**.

4. Click **Save**.
///
