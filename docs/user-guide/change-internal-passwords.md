# Changing internal passwords

EDA uses internal passwords to communicate between its internal services. These passwords are either hard-coded or are set before system installation.

After the system has been installed, administrators with cluster role privileges can update internal passwords for the following services using the applicable UI or scripts:

- Git passwords, Go Git server \(Gogs\) passwords
- Keycloak passwords and secrets
- PostgreSQL passwords

The following scripts are also available in the EDA toolbox pod:

- `reset-01-gogs-user-pass.sh`: resets the Gogs user password

- `reset-02-k8s-secret.sh`: resets the Kubernetes secret

- `reset-03-keycloak-admin-user.sh`: resets the Keycloak admin user password

- `reset-04-pgdb-password.sh`: resets the PostgreSQL database password

**Parent topic:** [Platform security](platform-security.md)

## Updating the Git server password <span id="updating-git-server-password"></span>

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

            Open a shell to the EDA toolbox pod. The following example resets the user password for eda-git and eda-git-replica.

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

    1. Open a shell to the EDA toolbox pod.

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

        `-n <namespace>` is the base namespace where EDA is deployed

        `-p <password>` is the Base64 encoded new password for the user

        ```
        /eda/tools/reset-02-k8s-secret.sh -n eda-system -s gogs-admin-user -p b3Jhbmdlcw==
        ```

3. Update the secret used by ConfigEngine.

    1. Open a shell to the EDA toolbox pod.

    2. Use the following command to change the Git secret:

        ```
        reset-02-k8s-secret.sh -n <namespace> -s git-secret -p <password>
        ```

        Where:

        `-n <namespace>` is the base namespace where EDA is deployed

        `-p <password>` is the new password for the user

        ```
        /eda/tools/reset-02-k8s-secret.sh -n eda-system -s git-secret -p oranges
        ```

4. Restart the EDA cluster.

    1. Open a shell to the EDA Toolbox.

    2. Enter the follow commands to gracefully restart the cluster:

        ```
        edactl platform stop
        edactl platform start
        ```

///

## Updating the Keycloak password <span id="keycloak-and-the-eda-ui"></span>

/// html | div.steps

1. Change the Git server password using the UI or the CLI script.

    - Using the UI:
        1. Go to the admin panel at `https://<domain:ip>/core/httpproxy/v1/keycloak`.
        2. Ensure that the Keycloak realm is selected from the upper left.
        3. Click **Users** from the left navigation bar
        4. Click the admin account.
        5. Click the **Credentials** tab, then click **Reset password** Follow the prompts to update the password.
    - Using the CLI script:
        1. Open a shell to the EDA toolbox pod.
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

    1. Open a shell to the EDA toolbox pod
    2. The following example changes the keycloak-admin-secret secret:

        ```
        /eda/tools/reset-02-k8s-secret.sh -n eda-system -s keycloak-admin-secret -p oranges
        ```

        Where:

        -n &lt;namespace&gt; is the base namespace where EDA is deployed

        -p &lt;password&gt; is the new password for the user

///

## Update the PostgreSQL database using the script <span id="update-postreg-database-using-script"></span>

/// html | div.steps

Perform this procedure using the `reset-04-pgdb-password.sh` script from the toolbox pod.

1. Open a shell to the EDA toolbox pod.

2. Update the database password.

    Use the following command:

    ```
    /eda/tools/reset-04-pgdb-password.sh -n <namespace> -p <password>
    ```

    Where:

    - `-n <namespace>` is the base namespace where EDA is deployed
    - `-p <password>` is the new password for the user
  
    ```
    -   `-n <namespace>` is the base namespace where EDA is deployed
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
