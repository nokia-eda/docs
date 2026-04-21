# Technical support

On occasion, it may be necessary to troubleshoot technical issues that arise in EDA clusters. When working with Nokia technical support engineers, collaboration often requires sharing a set of background data about the EDA system that can help pinpoint and resolve the issue.

To help collect the necessary data, EDA includes a shell script you can use to automatically collect and package the necessary technical data about your system and the status of relevant components.

To execute the shell script, open a shell to the `eda-toolbox` pod and run the `/tools/techsupport/techsupport.sh` script.

The output of the script is a gzipped tarball containing the following data:

- Logs from the cluster.
- Various information from Kubernetes, collected from all namespaces:
    - all `Services` data, including YAML.
    - all `Pods` data, including YAML.
    - all `Nodes` data, including YAML. Note that these are Kubernetes worker nodes, not EDA `TopoNodes`.
- Various information relating to EDA:
    - all CRDs, including YAML.
    - all resources of all CRDs, including YAML. This is essentially a full collection of all resources that are not native to Kubernetes.
    - all transactions, including YAML.
    - a system backup, which includes all Git repositories.

**Parent topic:** [Administration](administration.md)

**Related information**  
[Workflow Definition List page](workflows.md#)
