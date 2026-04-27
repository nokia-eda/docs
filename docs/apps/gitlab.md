# GitLab

| <nbsp> {: .hide-th } |                                                                                                                                     |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Description**      | GitLab application integrates Nokia EDA with GitLab issues and pipeline runs.                                                       |
| **Author**           | Nokia                                                                                                                               |
| **Catalog**          | [nokia-eda/catalog][catalog]                                                                                                        |
| **Language**         | Go                                                                                                                                  |

[catalog]: https://github.com/nokia-eda/catalog

## Overview

The GitLab application enables Nokia EDA to integrate with GitLab to support the following scenarios:

* Create [GitLab issues](#gitlab-issues) or run [GitLab pipelines](#gitlab-pipelines) based on the triggering events from EDA (alarms or queries).
* Create [GitLab issues](#gitlab-issues) or run [GitLab pipelines](#gitlab-pipelines) using the [workflow definition resources](#workflow-resources) provided by the application.

The app provides these resource groups:

* `GitlabInstance` and `ClusterGitlabInstance`: define how to connect to GitLab
* `GitlabIssue` and `ClusterGitlabIssue`: create and optionally close GitLab issues based on alarms or query events
* `GitlabPipeline` and `ClusterGitlabPipeline`: trigger GitLab pipelines based on alarms or query events
* `CreateGitlabIssue` and `RunGitlabPipeline`: run-to-completion workflow resources

## Installation

You can install the GitLab app via [EDA Store](../apps/index.md#eda-store) or by running an `AppInstaller` workflow with `kubectl` or `edactl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/gitlab/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/gitlab/install.yml"
EOF
```

///

### Configuration Notes

The current deployment template does not expose install-time `appSettings`.

The following controls the deployment in the EDA base namespace:

* proxy environment variables are read from the fixed ConfigMap name `proxy-config`
* container limits are fixed at `1` CPU and `1Gi` memory

> The default requests are fixed at `500m` CPU and `500Mi` memory.

## Getting Started

Create a GitLab instance first, then reference it from the `GitlabIssue` or `GitlabPipeline` resources.

Namespace rules:

* `GitlabInstance`, `GitlabIssue`, and `GitlabPipeline` are namespace-scoped and are typically created in a user namespace such as `eda`
* `ClusterGitlabInstance`, `ClusterGitlabIssue`, and `ClusterGitlabPipeline` are namespaced CRs, but are intended for use from the EDA base namespace

## GitLab Instances

A GitLab instance defines the target API endpoint and authentication token.

Notable specification fields:

* `apiBaseURL`: optional base URL. If omitted, the runtime defaults to `https://gitlab.com`
* `authSecretRef.name`: Secret name containing credentials (Personal Access Token)
* `authSecretRef.key`: validated by the API and typically set to `token`

Credential behavior:

* the runtime reads `data.token` from the referenced Secret
* it also accepts `username` and `password`, but PAT-based authentication is the most common authentication method
* the same Secret may also contain `tls.crt`, `tls.key`, and optional `ca.crt` for TLS client configuration
* for self-managed GitLab, set `apiBaseURL` to your GitLab API base URL

The resource status contains the fields related to the connectivity parameters of this instance:

* `connected`: indicates if the instance is connected to GitLab
* `error`: contains the error message if the instance is not connected
* `lastChecked`: the last time the instance was checked

/// tab | YAML

```yaml title="Example GitlabInstance resource"
--8<-- "docs/apps/gitlab/instance.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/gitlab/instance.yml"
EOF
```

///

## GitLab Issues

Use `GitlabIssue` or `ClusterGitlabIssue` to create issues in GitLab when an alarm or query event occurs.

Notable specification fields:

* `trigger.alarm`: create a GitLab issue when the matching alarm types occur
* `trigger.query`: create a GitLab issue when the matching query updates occur
* `repo`: GitLab project path, typically in `group/project` form
* `instance`: referenced instance resource
* `closeOnResolve`: close the GitLab issue when the alarm clears or the query object disappears
* `issue.title` and `issue.body`: Go templates rendered with the triggering event data
* `issue.assignees`, `issue.labels`, `issue.milestone`: optional GitLab issue metadata

Behavior notes:

* the runtime resolves assignees by GitLab username
* the app searches for an existing open issue by rendered title and appends a hash of the source path to keep one issue per source object
* if an issue already exists, the app adds a note instead of opening a duplicate
* current validation requires at least one assignee

### Duplicate Issue Handling

The app does not use the rendered issue title by itself as the unique key.

For each triggering alarm or query event, the app:

* renders `spec.issue.title`
* computes a hash from the triggering object path in EDA state
* builds the final GitLab issue title as `<rendered title> -- <hash>`

This means duplicate-looking issue titles are handled as follows:

* if the same source object triggers again, the hash is the same, so the app finds the existing open issue and adds a note instead of creating another issue
* if two different source objects render the same title text, their source paths are different, so the hashes differ and the app creates separate issues
* if `closeOnResolve` is enabled, the app looks up the same hashed title and closes that matching issue when the source alarm clears or the query object disappears

In practice, the visible title in GitLab is intentionally suffixed with a hash so the app can safely distinguish repeated events from different objects even when the human-readable part of the title is identical.

/// tab | YAML

```yaml title="Example GitlabIssue resource"
--8<-- "docs/apps/gitlab/issue.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/gitlab/issue.yml"
EOF
```

///

## GitLab Pipelines

Use `GitlabPipeline` or `ClusterGitlabPipeline` to trigger a GitLab pipeline when an alarm or query event occurs.

Notable specification fields:

* `trigger.alarm` or `trigger.query`: trigger a GitLab pipeline when the matching alarm types or query updates occur
* `repo`: GitLab project path, typically in `group/project` form
* `ref`: branch, tag, or commit reference
* `instance`: referenced instance resource
* `parameters[]`: pipeline variables

Parameters can be:

* static with `value.staticValue`
* dynamic with `value.dynamicValue`, which fetches a field from EDA using the `path`, `field`, and optional `where` conditions

/// tab | YAML

```yaml title="Example GitlabPipeline resource"
--8<-- "docs/apps/gitlab/pipeline.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/gitlab/pipeline.yml"
EOF
```

///

## Cluster-Scoped Resources

Use the cluster variants from the EDA base namespace when you want centralized automation across namespaces.

Cluster-specific behavior:

* `ClusterGitlabIssue` and `ClusterGitlabPipeline` can watch alarms across namespaces through `trigger.alarm.namespaces`
* query triggers can use fully qualified `.namespace` paths
* cluster resources must reference `ClusterGitlabInstance`

## Workflow Resources

The app also installs two workflow definition resources:

* `CreateGitlabIssue`
* `RunGitlabPipeline`

These workflows are run-to-completion programs that do not watch alarms or queries continuously; instead, they submit a single GitLab operation (issue or pipeline run) when the workflow is run.

/// admonition | Current behavior
    type: subtle-note

* although the workflow specification contains both `instance` and `clusterInstance`, the current version only supports `instance` (not `clusterInstance`)
* use a regular `GitlabInstance` for these workflow resources
///

//// tab | CreateGitlabIssue workflow resource
/// tab | YAML

```yaml title="Example CreateGitlabIssue workflow resource"
--8<-- "docs/apps/gitlab/create-gitlab-issue.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/gitlab/create-gitlab-issue.yml"
EOF
```

///
////

//// tab | RunGitlabPipeline workflow resource
/// tab | YAML

```yaml title="Example RunGitlabPipeline workflow resource"
--8<-- "docs/apps/gitlab/run-gitlab-pipeline.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/gitlab/run-gitlab-pipeline.yml"
EOF
```

///
////

## Validation Notes

When creating resources, follow these rules:

* instances require both `authSecretRef.name` and `authSecretRef.key`
* issues require `repo`, `instance`, `issue.title`, `issue.body`, at least one assignee, and either an alarm or query trigger
* issue title and body templates must be valid Go templates
* pipelines require `repo`, `pipeline`, `ref`, `instance`, and either an alarm or query trigger
* dynamic pipeline parameters must set at least one of `field` or `path`
