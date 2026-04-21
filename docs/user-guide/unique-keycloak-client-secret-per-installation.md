# Unique Keycloak client secret per installation

To avoid the risk of a secret revealed at one customer can affect the installations of other installations, internal secrets used by the different EDA components must be unique for each installation. This practice is especially important for the Keycloak secrets that are used by the API server to configure and communicate with the Keycloak API server.

**Parent topic:** [Platform security](platform-security.md)

## Changing the Keycloak secret <span id="changing-the-keycloak-secret"></span>

/// html | div.steps

By default, a unique secret is generated per installation. Use this procedure to regenerate a new Keycloak secret.

1. From your web browser, navigate to `{EDA_URL}/core/httpproxy/v1/keycloak`.

2. Log in with the Keycloak administrator username and password.

3. From the **Keycloak** drop-down list on the upper left, select **Event Driven Automation eda**.

4. Select **Clients** from the menu on the left.

5. Select "eda" in the client table in the main web page area.

6. Select **"Credentials"** in the tab bar containing, **"Settings/Keys/Credentials/Roles/..."**

7. Note the current "Client Secret".

8. Click **Regenerate** to generate a new random value for the secret.

///

## Changing the Keycloak admin password <span id="change-keycloak-user-pw"></span>

Use this procedure to change the Keycloak admin password.
/// html | div.steps

1. From your web browser, navigate to `{EDA_URL}/core/httpproxy/v1/keycloak`.

2. Log in with the current Keycloak administrator username and password.

3. From the user drop-down list on the upper right, select **Manage Account**.

4. From the menu on the left, select **Account Security** &gt; **Signing In**.

5. Click **Update** next to **My Password**.

6. Configure a new password and save it.

7. Generate the Base 64 hash of the new password.

8. Using a system with access to the Kubernetes API of the EDA deployment, execute the following command:

    ```
    kubectl -n eda-system patch secret keycloak-admin-secret -p
            '{"data": { "password": "<NEW BASE64 HASH>" }}'
    ```

9. Restart the Keycloak service.

    ```
    kubectl -n eda-system rollout restart deployment/eda-keycloak
    ```

///
