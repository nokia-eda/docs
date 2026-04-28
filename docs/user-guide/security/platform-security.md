# Platform security

This section discusses how to secure the Nokia EDA infrastructure and manage internal passwords.

## Changing internal passwords

Nokia EDA uses internal passwords to communicate between its internal services. These passwords are either hard-coded or are set before system installation.

After the system has been installed, administrators with cluster role privileges can update internal passwords for the following services using the applicable UI or scripts:

- Git passwords, Go Git server (Gogs) passwords
- Keycloak passwords and secrets
- PostgreSQL passwords

The following scripts are also available in the Nokia EDA toolbox pod:

- `reset-01-gogs-user-pass.sh`: resets the Gogs user password

- `reset-02-k8s-secret.sh`: resets the Kubernetes secret

- `reset-03-keycloak-admin-user.sh`: resets the Keycloak admin user password

- `reset-04-pgdb-password.sh`: resets the PostgreSQL database password

### Updating the Git server password <span id="updating-git-server-password"></span>

/// html | div.steps

1. Change the Git server password using the UI or the CLI script.

    - Using the UI:
        1. Log in to the Git UI. If you are using the git-server provided cluster, you can reach the UI using the following URLs:<br>
           ```<eda-url>/core/httpproxy/v1/gogs/```<br>
           ```<eda-url>/core/httpproxy/v1/gogs-replica/```
  
        2. Click the user icon, then from the navigation bar on the right, go to **Your Settings** &gt; **Password**.

        3. Change your password.
        4. Log out and then log back in.

    - Using the CLI script:
        1. Generate a token for the admin user.
            1. Log in to the Git UI.
            2. Navigate to **Your Settings**.
            3. From the right sidebar, select **Applications** &gt; **Generate New Token**. This token is required to access some admin-level REST endpoints.
        2. Change the user password.

            Open a shell to the Nokia EDA toolbox pod. The following example resets the user password for eda-git and eda-git-replica.

            ```
            /eda/tools/reset-01-gogs-user-pass.sh \
            -u eda \
            -p oranges \
            -g http://eda-git:3000 \
            -t 79b6e0ada8dc74bf60751a0e56683d6377792070
            
            /eda/tools//reset-01-gogs-user-pass.sh \
            -u eda \
            -p oranges \
            -g http://eda-git-replica:3000 \
            -t 70dd66f925678f35eb02d5073ce3b051b1bb640d
            ```

            Where:

            -u &lt;username&gt; is the username of the account

            -p &lt;password&gt; is the new password for the user

            -g &lt;git server url&gt; is the URL to reach the Gogs server

            -t &lt;access token&gt; is the access token from an admin user

2. Update the Gogs initialization secret.

    1. Open a shell to the Nokia EDA toolbox pod.

    2. Base64 encode the new password.

        ```
        echo -n "oranges" | base64
        ```

    3. Change the gogs-admin-user secret.

        The Gogs initialization secret is used on first boot of a new Gogs deployment.

        Use the following command:

        ```
        reset-02-k8s-secret.sh -n <namespace> -s gogs-admin-user -p <password>
        ```

        Where:

        `-n <namespace>` is the base namespace where Nokia EDA is deployed

        `-p <password>` is the Base64 encoded new password for the user

        ```
        /eda/tools/reset-02-k8s-secret.sh -n eda-system -s gogs-admin-user -p b3Jhbmdlcw==
        ```

3. Update the secret used by ConfigEngine.

    1. Open a shell to the Nokia EDA toolbox pod.

    2. Use the following command to change the Git secret:

        ```
        reset-02-k8s-secret.sh -n <namespace> -s git-secret -p <password>
        ```

        Where:

        `-n <namespace>` is the base namespace where Nokia EDA is deployed

        `-p <password>` is the new password for the user

        ```
        /eda/tools/reset-02-k8s-secret.sh -n eda-system -s git-secret -p oranges
        ```

4. Restart the Nokia EDA cluster.

    1. Open a shell to the Nokia EDA Toolbox.

    2. Enter the follow commands to gracefully restart the cluster:

        ```
        edactl platform stop
        edactl platform start
        ```

///

### Updating the Keycloak password <span id="keycloak-and-the-eda-ui"></span>

/// html | div.steps

1. Change the Git server password using the UI or the CLI script.

    - Using the UI:
        1. Go to the admin panel at `https://<domain:ip>/core/httpproxy/v1/keycloak`.
        2. Ensure that the Keycloak realm is selected from the upper left.
        3. Click **Users** from the left navigation bar
        4. Click the admin account.
        5. Click the **Credentials** tab, then click **Reset password** Follow the prompts to update the password.
    - Using the CLI script:
        1. Open a shell to the Nokia EDA toolbox pod.
        2. Set a temporary Keycloak password.

            For example:

            ```
            /eda/tools/reset-03-keycloak-admin-user.sh -e https://eda-api -r admin -t temporary -a admin -p admin
            ```

            Where:

            -r &lt;username&gt; is the user for which to trigger a password reset

            -t &lt;password&gt; is the temporary password for the user

            -a &lt;username&gt; is the admin user to fetch an API token

            -p &lt;password&gt; is the admin user password to fetch an API token

        3. Log in to the Keycloak UI with the temporary password. Follow the prompts to update the password.

2. Update the keycloak-admin-secret secret in Kubernetes

    1. Open a shell to the Nokia EDA toolbox pod
    2. The following example changes the keycloak-admin-secret secret:

        ```
        /eda/tools/reset-02-k8s-secret.sh -n eda-system -s keycloak-admin-secret -p oranges
        ```

        Where:

        -n &lt;namespace&gt; is the base namespace where Nokia EDA is deployed

        -p &lt;password&gt; is the new password for the user

///

### Updating the PostgreSQL database using the script <span id="update-postreg-database-using-script"></span>

/// html | div.steps

Perform this procedure using the `reset-04-pgdb-password.sh` script from the toolbox pod.

1. Open a shell to the Nokia EDA toolbox pod.

2. Update the database password.

    Use the following command:

    ```
    /eda/tools/reset-04-pgdb-password.sh -n <namespace> -p <password>
    ```

    Where:

    - `-n <namespace>` is the base namespace where Nokia EDA is deployed
    - `-p <password>` is the new password for the user
  
    ```
    -   `-n <namespace>` is the base namespace where Nokia EDA is deployed
    -   `-p <password>` is the new password for the user
    ```

    /eda/tools/reset-04-pgdb-password.sh -n eda-system -p oranges

    ```

3. Update the Kubernetes secret password.

    ```
    /eda/tools/reset-02-k8s-secret.sh -n eda-system -s postgres-db-secret -p oranges
    ```

4. Restart the Postgres and Keycloak deployments.

    ```
    kubectl rollout restart deployment eda-postgres eda-keycloak
    ```

///

## Unique Keycloak client secret per installation

To avoid the risk of a secret revealed at one customer can affect the installations of other installations, internal secrets used by the different Nokia EDA components must be unique for each installation. This practice is especially important for the Keycloak secrets that are used by the API server to configure and communicate with the Keycloak API server.

### Changing the Keycloak secret <span id="changing-the-keycloak-secret"></span>

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

### Changing the Keycloak admin password <span id="change-keycloak-user-pw"></span>

Use this procedure to change the Keycloak admin password.
/// html | div.steps

1. From your web browser, navigate to `{EDA_URL}/core/httpproxy/v1/keycloak`.

2. Log in with the current Keycloak administrator username and password.

3. From the user drop-down list on the upper right, select **Manage Account**.

4. From the menu on the left, select **Account Security** &gt; **Signing In**.

5. Click **Update** next to **My Password**.

6. Configure a new password and save it.

7. Generate the Base 64 hash of the new password.

8. Using a system with access to the Kubernetes API of the Nokia EDA deployment, execute the following command:

    ```
    kubectl -n eda-system patch secret keycloak-admin-secret -p
            '{"data": { "password": "<NEW BASE64 HASH>" }}'
    ```

9. Restart the Keycloak service.

    ```
    kubectl -n eda-system rollout restart deployment/eda-keycloak
    ```

///

## Proxy forward headers

Forward headers are required for accurate access-logging of the source IP on proxied servers, notably, Keycloak.
The engine-config parameter `ProxyMode` controls Keycloak endpoint handles these headers. It has the following settings:

- `None` (the default): if Nokia EDA is deployed behind a reverse proxy, the setting cannot be `None`; the setting must be `Forwarded` or `XForward`.
- `Forward`: the API server trusts the `Forwarded` header on incoming traffic and forwards it unchanged to the destination. All `X-Forwarded-*` headers are dropped.
- `XForward`: the API server trusts the `X-Forwarded-*` HTTP header on incoming traffic and forwards them unchanged to the destination. The `Forwarded` header is dropped.

/// Admonition | Note
    type: subtle-note
The end user is responsible for the secure configuration of forward headers on their reverse proxy.
///

The setting for `ProxyMode` interacts with Keycloak configuration as follows:

- If `ProxyMode` is set to None  or forwarded, configure Keycloak with "--proxy-headers forwarded"
- If `ProxyMode` is set to **XForward**, configure Keycloak with "--proxy-headers xforwarded"

Table: Summary of how Keycloak handles forward headers

|    | `relaxDomainNameEnforcement`=FALSE | `relaxDomainNameEnforcement`=TRUE |
|---|---|---|
| `ProxyMode`=`None` | --proxy-headers forwarded | --hostname-strict false --proxy-headers forwarded |
| `ProxyMode`=`Forward` | --proxy-headers forwarded | --hostname-strict false --proxy-headers forwarded |
| `ProxyMode`=`XForward` | --proxy-headers xforwarded | --hostname-strict false --proxy-headers xforwarded |

Table: Summary of how the API-server handles forward headers

|  | `relaxDomainNameEnforcement = FALSE` | `relaxDomainNameEnforcement = TRUE` |
| ----------- | -------------------------------------- | -------------------------------------- |
| `ProxyMode`=`None`  | • Drop `Forwarded` and `X‑Forwarded‑*` headers.<br>• Generate a new `Forwarded` header containing a `for=` directive.<br>• Add a `host=` directive only for the built‑in identity proxy. | Pass all `Forwarded` and `X‑Forwarded‑*` headers unchanged. |
| `ProxyMode`=`Forward` | • If a `Forwarded` header exists, append a `for=` directive and forward the rest unchanged.<br>• If absent, create a `Forwarded` header with a `for=` directive.<br>• Drop all `X‑Forwarded‑*` headers.<br>• No extra `host=` directives for the built‑in identity proxy. | Pass all `Forwarded` and `X‑Forwarded‑*` headers unchanged. |
| `ProxyMode`=`XForward` | • If an `X‑Forwarded‑For` header exists, append the client IP to the list<br>• If absent, create an `X‑Forwarded‑For` header with the client IP.<br>• Forward other `X‑Forwarded‑*` headers unchanged.<br>• Drop the `Forwarded` header.<br>• No `X‑Forwarded‑Host` header for the built‑in identity proxy. | Pass all `Forwarded` and `X‑Forwarded‑*` headers unchanged. |