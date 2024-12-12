# FSS Cluster Deployment

It is possible to use just the Kubernetes cluster that the FSS Deployer installs to run EDA, without the FSS application. This gives an easy to deploy Kuberenetes cluster of 1, 3 or 6 nodes.

/// details | Tested Deployment Configurations
    type: note
The following deployment configurations have been tested up to the point that EDA is running, accessible and a Digital Sandbox environment was deployed, including a Fabric:

* IPv4 only (Dual Stack has not been tested).
* 1, 3 or 6 VM Deployments
  * Single node is only allowed for very small scale testing
* Single OAM+Node network
* Split OAM & Node networks
* MTU 9000 and MTU 1500 on interfaces
///

/// admonition | A VIP for the OAM network is a must for access to EDA, even for a single node
    type: warning
///

## Deploying the FSS Kubernetes Cluster

Using the FSS Deployer, it is possible to deploy only a Kubernetes cluster with Ceph storage and MetalLB on one, three or six VMs. Follow these steps while referencing the FSS Installation Guide:

1. Deploy the latest FSS Deployer VM, as per the FSS Installation Guide.
2. Create 1, 3 or 6 VMs from the latest FSS Base VM image, as per the FSS Documentation.
3. Create an `eda-deployment.json` installer configuration file for the FSS Deployer VM (also referred to as the `input.json` file), make sure to configure:
    * An `lbconfig` entry with a unique IPv4 IP for at least the OAM network.
    * Set `domainhost` to the FQDN that resolves to your OAM VIP.
4. Guarantee password-less SSH between Deployer and the Base VMs (Key based).
5. Execute the configure command on the FSS Deployer VM using your `eda-deployment.json` file:

    ```bash
    /root/bin/fss-install.sh configure eda-deployment.json
    ```

6. Execute the command to only install the Kubernetes cluster from the FSS Deployer VM:

    ```bash
    /root/bin/setup-k8s.sh
    ```

7. Wait until the K8s installation is finished and verify the cluster is up and running.

/// details | Example `eda-deployment.json`
    type: note

```json
--8<-- "docs/user-guide/resources/eda-deployment-example.json"
```

///

## Deploying EDA inside the FSS Kubernetes Cluster

/// details | Requirements to run the procedure
    type: note

The system used to run this procedure should be a different Linux system than the Deployer VM or the Kubernetes nodes. This platform requires Docker running and make to be available, just as if you were running the install using Kind or on another external Kubernetes environment.
///

With a few important exceptions, the steps to deploy EDA in the FSS Kubernetes cluster are very similar to the regular installation process as documented before.

/// admonition | Before starting, make sure all pods in the FSS Kubernetes cluster are in a running state.
    type: warning
///

Follow these steps and pay careful attention to the differences specifically highlighted:

1. Make sure you have the playground cloned and up to date, as described in the [Getting Started Guide](../../getting-started/try-eda.md) chapter.
2. Download the latest tools:

    ```bash
    make download-tools
    ```

3. Download the latest packages, including the `eda-kpt` package:

    ```bash
    make download-pkgs
    ```

4. Install the necessary external packages:

    ```bash
    make install-external-packages
    ```

5. Generate the correct EDA Core configuration.

    /// details | Use the appropriate parameters
        type: warning

It is crucial that you provide the correct parameters in this step to make sure the EDA cluster is aware of the correct Virtual IP and port connections to the API and UI will use.

Make sure to properly set:

* `EXT_DOMAIN_NAME` to the FQDN or Virtual IP configured in the `eda-deployment.json` created in [step 3 of the Deploying the FSS Kubernetes Cluster](#deploying-the-fss-kubernetes-cluster) section. If you choose the FQDN, it must resolve to the Virtual IP.
* `EXT_HTTP_PORT` to 80
* `EXT_HTTPS_PORT` to 443
* `EXT_IPV4_ADDR` to the Virtual IP configured in the `eda-deployment.json` created in [step 3 of the Deploying the FSS Kubernetes Cluster](#deploying-the-fss-kubernetes-cluster) section.
* `EXT_IPV6_ADDR` to an empty string (`""`).
///

    ```bash
    EXT_DOMAIN_NAME="<VIP IP/FQDN>" EXT_HTTP_PORT=80 EXT_HTTPS_PORT=443 EXT_IPV4_ADDR="<VIP IP>" EXT_IPV6_ADDR="" make eda-configure-core
    ```

6. Change the `eda-git` Kubernetes Service to be a `ClusterIP` service instead of a `LoadBalancer` type

    /// details | Changing the service type and its impact
        type: note
This is needed to free up the VIP that is assigned to MetalLB from the `eda-deployment.json` configuration so it can be used by the actual EDA API Server.

This will not negatively impact the EDA deployment. The VIP for the Git service inside EDA is only needed in case the git server should be directly reachable on a VIP, which is not advised.
///

    ```bash
    kubectl -n default patch service eda-git -p '{"spec": {"type": "ClusterIP"}}'
    ```

7. Install the EDA Core components:

    ```bash
    make eda-install-core
    ```

    /// admonition | Wait for all the EDA pods to be up and running.
        type: note
    ///

8. Verify that the EDA Config Engine is up and running:

    ```bash
    make is-ce-first-commit-done
    ```

9. Verify that the App Store Catalog is operational:

    ```bash
    make is-apps-catalog-operational
    ```

10. Verify that the App Store Registry is reachable:

    ```bash
    make is-apps-registry-reachable
    ```

11. Install all the standard EDA Apps.

    /// admonition | This can take over 5 minutes, depending on your connectivity.
        type: note
    ///

    ```bash
    make eda-install-apps
    ```

12.  Bootstrap EDA:

    ```bash
    make eda-bootstrap
    ```

13. (Optional) Deploy an example topology:

    ```bash
    make topology-load
    ```

### Accessing the new EDA Deployment

The new EDA Deployment can now be accessed using `https://VIP` or, if configured in [step 5 of the previous section](#deploying-eda-inside-the-fss-kubernetes-cluster), using the FQDN with `https://FQDN`.
