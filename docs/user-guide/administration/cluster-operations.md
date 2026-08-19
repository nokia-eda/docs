# Talos Kubernetes cluster operations

This chapter describes the operations that can be performed on the Talos Kubernetes cluster powering the Nokia EDA platform.

## Making cluster configuration changes

The Talos Kubernetes cluster configuration is defined declaratively in a set of Talos machine configuration files. The EDA installation tool, `edaadm`, uses a single [EDAADM configuration file](../../software-install/deploying-eda/setting-up-the-eda-virtual-machine-nodes.md#edaadm-configuration-file-fields) to define the cluster configuration. This file provides a higher-level abstraction of the cluster configuration, and `edaadm generate` command translates it into the Talos-specific manifests.

In order to make configuration changes to the live cluster, follow this procedure:

1. Edit the EDAADM configuration file to reflect the changes you want to make.
2. Run the `edaadm generate` command to generate the set of Talos-specific manifests.
3. Apply the changes to each node of the EDA cluster using the following command:

    ```bash
    # apply to all nodes in the EDA cluster
    edaadm apply-config --reprovision -c <path to the EDAADM configuration file> \
    -n <name of the node>
    ```

To illustrate the complete workflow, let's work through an example of changing the nameservers for all Kubernetes nodes in the EDA cluster.

For this example, the EDAADM configuration file defines `"10.171.0.1","10.171.0.2","10.171.0.3"` as the nameservers. Verify the configured nameservers with the `talosctl` command:

```bash title="endpoint and node addresses are specific for this example"
talosctl --talosconfig talosconfig.yaml get resolvers -n 192.168.123.101 -e 192.168.123.101

NODE              NAMESPACE   TYPE             ID          VERSION   RESOLVERS                                  SEARCH DOMAINS
192.168.123.101   network     ResolverStatus   resolvers   3         ["10.171.0.1","10.171.0.2","10.171.0.3"]   []
```

Change the `.k8s.nameservers.servers` list in the EDAADM configuration file to your desired set of nameservers, e.g. `["10.171.0.1","8.8.8.8","1.1.1.1"]`:

```diff
git diff eda-6-node.yaml

diff --git a/blueprints/eda-6-node.yaml b/blueprints/eda-6-node.yaml
index 386c861..1730cec 100644
--- a/blueprints/eda-6-node.yaml
+++ b/blueprints/eda-6-node.yaml
@@ -32,8 +32,8 @@ k8s:
   nameservers:
     servers:
       - 10.171.0.1
-      - 10.171.0.2
-      - 10.171.0.3
+      - 8.8.8.8
+      - 1.1.1.1
   primaryNode: vm-cp-01
   stack: dual
   time:
```

After the edits are made, run the `edaadm generate` command to generate the set of Talos-specific manifests:

```bash
edaadm generate -c eda-6-node.yaml
```

This will regenerate the set of Talos-specific manifests with the new nameservers.

Next, apply the changes to each node of the EDA cluster using the `edaadm apply-config --reprovision` command:

```bash
edaadm apply-config --reprovision -c eda-6-node.yaml -n vm-cp-01 #(1)!

Applied configuration without a reboot
```

1. This command applies the changes to a single node of the EDA cluster. Repeat the command for each node of the EDA cluster.

> Talos allows nameserver changes to be applied immediately, so the command immediately applies the changes to the node:

The change of nameservers is allowed to be applied immediately, so the command will apply the changes without a reboot:

```bash
talosctl --talosconfig talosconfig.yaml get resolvers -n 192.168.123.101 -e 192.168.123.101
NODE              NAMESPACE   TYPE             ID          VERSION   RESOLVERS                            SEARCH DOMAINS
192.168.123.101   network     ResolverStatus   resolvers   4         ["10.171.0.1","8.8.8.8","1.1.1.1"]   []

```

/// warning | Immediate apply of configuration changes
The `edaadm apply-config --reprovision` command immediately applies the changes to the live cluster if Talos [allows the configuration changes to be applied immediately](https://docs.siderolabs.com/talos/-{{talos_version}}-/configure-your-talos-cluster/system-configuration/editing-machine-configuration).

If Talos cannot apply the configuration changes immediately, the command returns an error. Cordon/drain the node and add the `--reboot` flag to the `edaadm apply-config --reprovision` command to apply the changes in the reboot mode.
///
