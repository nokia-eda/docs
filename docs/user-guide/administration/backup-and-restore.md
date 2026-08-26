# Backup and restore

Nokia Event-Driven Automation (EDA) clusters can be backed up and restored, include the following features:

- A backup can be performed at any time without stopping the application.
- Backups are atomic and contain the last golden set of working configuration. The system waits until an in-progress transaction is completed before proceeding with a backup.
- An administrator may restore into a currently-running or populated cluster, resulting in the cluster reverting back to the state provided in the backup.
- An administrator can restore into a clean/freshly installed cluster.

## Backups

In Nokia EDA, a backup is simply the copy of all Git repositories in use at the time of the backup and an `EngineConfig` resource file from the source that can be optionally restored.

The `edactl platform backup` command is used to create a backup. At a high-level, this command does the following:

- Creates a tarball of all repositories, including the following:
  - Backup (the set of resources used in the cluster)
  - Apps (the set of installed applications in the cluster)
  - User storage (user-generated content including dashboards)
  - Certificates and secrets
  - Identity (the set of users, groups, and roles)
- Adds to this tarball the current `EngineConfig` resource file.
- Streams these files to the client performing the backup over gRPC.

The tarball created is created in the format `eda-backup-<cluster-member-name>-<date-and-time>.tgz` in the current directory. You can optionally provide a name for the tarball and provide an alternate destination by providing the name and the destination's path in the command.

### Extracting the backup file

An administrator can use the  `edactl platform backup extract --filename <filepath> <path>` command to extract the contents of a backup tar file, where:

- `<filepath>` is the path to the directory of the backup tar file (in `.tar.gz` format). For example, */home/user/backup.tar.gz*
- `<path>` is the path to the directory where you want to extract the backup files. For example, */home/user/extracted/*. The directory is recursively created if it does not exist.

This command extracts the specified backup tar file into the specified directory. This command extracts any git packs, so you can easily investigate the files within them.

### Displaying the backup summary

An administrator can use `edactl platform backup summary --filename <filepath>` command to display the summary for the backup tar file, where `<filepath>` is the path of the backup tar file (in `.tar.gz` format), for example,  */home/dev/backup.tar.gz*.

This command takes the specified backup file, and prints the following information:

- The base namespace used in the backup.
- The EDA version used in the backup.
- The list of namespaces used in the backup.
- The list of installed apps in the backup.
- The per-GVK count of resources in the backup.
- The size of each repository in the backup.

The summary also lists the resources of the credentials/security repository. For example:

```text
repositories:
# other repos
- name: security
  size: "127590"
  resources:
    - namespace: _base_ # taken from the repo dir path
      gvks:
        - core.eda.nokia.com/v1/NodeSecurityProfile:
          - insecure
          - managed-tls
        - core.eda.nokia.com/v1/License:
          - eda-non-prod-license
        - trust.cert-manager.io/v1alpha1/Bundle:
          - eda-api-trust-bundle
        - v1/Secret:
        - v1/ConfigMap:

```

## Restore process

The `edactl platform restore` command restores a backup. When you initiate a restore operation, the ConfigEngine on the destination cluster performs the following tasks:

- Receives the restore request via gRPC. The request contains the complete tarball generated via a backup.
- Unpacks the backup, overwriting all content as it goes.
- Pushes backed up repositories and files to any server identified in the `EngineConfig`.
- Exits, relying on Kubernetes to restart.
- Starts again as if it had started clean from the repositories.

/// Admonition | Note
    type: subtle-note
A restore operation restarts the ConfigEngine, so use the command with caution.
///

By default, all repositories are backed up, but you can use the following options to exclude some repositories:

- **--exclude-identity-git-repo**: excludes the identity repository
- **--exclude-security-git-repo**: excludes the security repository

    Excluding the security repository prevents you from restoring an old security repository with expired certificates.

## Creating backups <span id="create-backups"></span>

An administrator can create a backup using the `edactl platform backup` command.
/// html | div.steps

1. From the eda-toolbox pod​ command line prompt, execute the `edactl platform backup` command.
2. Copy the backup from the eda-toolbox pod to a safe location.

///

## Restoring backups <span id="restore-backups"></span>

- The destination cluster must be running the same or newer version as the cluster from where the backup was created.
- You must have rights and permissions on the cluster in which the backup is to be restored.

### Procedure

/// html | div.steps

1. Copy the saved backup to the eda-toolbox pod.
2. From the eda-toolbox pod, execute the `edactl platform restore <eda-backup.tar.gz>` command.

///
