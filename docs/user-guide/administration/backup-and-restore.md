# Backup and restore

Critical systems are often backed up to ensure continuity in the event of an outage or other critical failure. Operators typically use backups for the following purposes:

- to replicate a customer issue when debugging
- to restore a cluster to a previous state \(often via re-installation\)

Nokia Event-Driven Automation (EDA) implementation for backup and restore include the following features:

- You can perform backups at any time with no outages or maintenance actions required.
- Backups are atomic and contain the lost known set of working configuration. The system waits until an in-progress transaction is completed before proceeding with a backup.
- You can restore into a dirty cluster and revert the cluster back to the state provided in the backup, auditing any resource as necessary.
- You can restore into a clean/freshly installed cluster.

## Backups
In Nokia EDA, a backup is simply the copy of all Git repositories in use at the time of the backup and an `EngineConfig` resource file from the source that can be optionally restored.

The `edactl platform backup` command is used to create a backup. At a high-level, this command does the following:

- Creates a tarball of all repositories, including the following:
    - Backup
    - Apps
    - User storage
    - Certificates
- Adds to this tarball the current `EngineConfig` resource file.
- Streams these files to the client performing the backup over gRPC.

The tarball created is created in the format `eda-backup-<cluster-member-name>-<date-and-time>.tgz` in the current directory. You can optionally provide a name for the tarball and provide an alternate destination by providing the name and the destination's path in the command.

## Restore process

The `edactl platform restore` command restores a backup. When you initiate a restore operation, the ConfigEngine on the destination cluster performs the following tasks:

- Receives the restore request via gRPC. The request contains the complete tarball generated via a backup.
- Unpacks the backup, overwriting all content as it goes.
- Pushes backed up repositories and files to any server identified in `EngineConfig` resource.
- Restarts, relying on Kubernetes to restart.
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

You can create a backup using the `edactl platform backup` command.
/// html | div.steps

1. From the eda-toolbox pod​ command line prompt, execute the `edactl platform backup` command.
2. Copy the backup from the eda-toolbox pod to a safe location.

///

## Restoring backups <span id="restore-backups"></span>

- The destination cluster must be running the same version as the cluster from where the backup was created.
- You must have rights and permissions on the cluster in which the backup is to be restored.

### Procedure

/// html | div.steps

1. Copy the saved backup to the eda-toolbox pod.
2. From the eda-toolbox pod, execute the `edactl platform restore <eda-backup.tar.gz>` command.

///
