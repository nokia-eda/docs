# Platform operations

The `edactl platform` utility provides a set of commands for managing Nokia EDA operations such as taking EDA offline for maintenance, restarting the system, and uninstalling Nokia EDA.

You can use the `edactl platform` command options:

- `--stop`: disables the cluster, deletes deployments, and stops the processing of transactions. Without any arguments, it removes the following resources from the cluster:

    - `DaemonSet`
    - `Pod`
    - `StatefulSet`
    - `Deployment`

    To stop only the core, use the `--core-only` argument.

- `--start`: triggers the system to start up and recreates the resources removed by `--stop`.

- `--uninstall`: performs a full clean-up of the cluster, removing every object created by ConfigEngine and every Nokia EDA-related app. After this command, the cluster is in a pre-EDA state.

    From this cleaned state you can:

    - Start the cluster again using `edactl platform start`. This command restores everything (including CRDs).
    - Complete an uninstall by removing the EngineConfig CRD, and the eda-ce Deployment. At this point the cluster would be "clean" - that is, in a pre-EDA state.
  