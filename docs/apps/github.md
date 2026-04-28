# GitHub

| <nbsp> {: .hide-th } |                                                                 |
| -------------------- | --------------------------------------------------------------- |
| **Description**      | GitHub application integrates Nokia EDA with GitHub issues and workflow dispatches. |
| **Author**           | Nokia                                                           |
| **Catalog**          | [nokia-eda/catalog][catalog]                                    |
| **Language**         | Go                                                              |

[catalog]: https://github.com/nokia-eda/catalog

## Overview

The GitHub application enables Nokia EDA to integrate with GitHub to support the following scenarios:

* Create [GitHub issues](#github-issues) or run [GitHub Actions workflows](#github-actions) based on the triggering events from EDA (alarms or queries).
* Create [GitHub issues](#github-issues) or run [GitHub Actions workflows](#github-actions) using the workflow definition resources provided by the application.

## Installation

You can install the GitHub app via [EDA Store](index.md#nokia-eda-store) or by running an `AppInstaller` workflow with `kubectl` or `edactl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/github/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/github/install.yml"
EOF
```

///

### Install Settings

The app provides the following install-time settings:

* `proxyConfigName`: ConfigMap name used for `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`. Default: `proxy-config`
* `githubCPULimit`: CPU limit for the controller pod. Default: `"1"`
* `githubMemoryLimit`: memory limit for the controller pod. Default: `"1Gi"`

> The default requests are set to`500m` CPU and `500Mi` memory.

These settings control the deployment in the EDA base namespace and can be provided through `spec.apps[].appSettings` in the `AppInstaller` workflow or directly in the EDA UI.

/// tab | YAML

```yaml
--8<-- "docs/apps/github/install-with-settings.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/github/install-with-settings.yml"
EOF
```

///

## Getting Started

Create a GitHub instance first, then reference it from the `GitHubIssue` or `GitHubAction` resources.

Namespace rules:

* `GitHubInstance`, `GitHubIssue`, and `GitHubAction` are namespace-scoped and are typically created in a user namespace such as `eda`
* `ClusterGitHubInstance`, `ClusterGitHubIssue`, and `ClusterGitHubAction` are namespaced CRs, but are intended for use from the EDA base namespace

## GitHub Instances

A GitHub instance defines the target GitHub API endpoint and authentication token.

Notable specification fields:

* `apiBaseURL`: optional base URL. Leave empty or set `https://api.github.com` for the public GitHub (github.com) instance.
* `authSecretRef.name`: Secret name containing GitHub credentials (Personal Access Token)
* `authSecretRef.key`: validated by the API and typically set to `token`

Credential behavior:

* the runtime reads `data.token` from the referenced Secret
* it also accepts `username` and `password`, but GitHub PAT-based authentication is the most common authentication method
* for GitHub Enterprise, set `apiBaseURL` to the enterprise base URL, for example `https://ghe.example.com`

The resource status contains the fields related to the connectivity parameters of this instance:

* `connected`: indicates if the instance is connected to GitHub
* `error`: contains the error message if the instance is not connected
* `lastChecked`: the last time the instance was checked

/// tab | YAML

```yaml title="Example GitHubInstance resource"
--8<-- "docs/apps/github/instance.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/github/instance.yml"
EOF
```

///

## GitHub Issues

Use `GitHubIssue` or `ClusterGitHubIssue` to create issues in GitHub when an alarm or query event occurs.

Notable specification fields:

* `trigger.alarm`: create a GitHub issue when the matching alarm types occur
* `trigger.query`: create a GitHub issue when the matching query updates
* `repo`: repository name
* `instance`: referenced instance resource
* `closeOnResolve`: close the GitHub issue when the alarm clears or the query object disappears
* `issue.title` and `issue.body`: Go templates rendered with the triggering event data
* `issue.assignees`, `issue.labels`, `issue.milestone`: optional GitHub issue metadata

Behavior notes:

* the app searches for an existing open issue by rendered title and appends a hash of the source path to keep one issue per source object
* if an issue already exists, the app adds a comment instead of opening a duplicate

/// tab | YAML

```yaml title="Example GitHubIssue resource"
--8<-- "docs/apps/github/issue.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/github/issue.yml"
EOF
```

///

### Duplicate Issue Handling

The app does not use the rendered issue title by itself as the unique key.

For each triggering alarm or query event, the app:

* renders `spec.issue.title`
* computes a hash from the triggering object path in EDA state
* builds the final GitHub issue title as `<rendered title> -- <hash>`

This means duplicate-looking issue titles are handled as follows:

* if the same source object triggers again, the hash is the same, so the app finds the existing open issue and adds a comment instead of creating another issue
* if two different source objects render the same title text, their source paths are different, so the hashes differ and the app creates separate issues
* if the `closeOnResolve` field is set to `true`, the app looks up the same hashed title and closes that matching issue when the source alarm clears or the query object disappears

In practice, the visible title in GitHub is intentionally suffixed with a hash so the app can safely distinguish repeated events from different objects even when the human-readable part of the title is identical.

## GitHub Actions

Use `GitHubAction` or `ClusterGitHubAction` to dispatch a GitHub Actions workflow when an alarm or query event occurs.

Notable specification fields:

* `trigger.alarm` or `trigger.query`: dispatch GitHub Actions workflow when the matching alarm types or query updates occur
* `repo`: repository name
* `workflow`: workflow file name
* `ref`: branch, tag, or commit reference
* `instance`: referenced instance resource
* `parameters[]`: workflow input parameters

Parameters can be:

* static with `value.staticValue`
* dynamic with `value.dynamicValue`, which fetches a field from EDA using the `path`, `field`, and optional `where` conditions

/// tab | YAML

```yaml title="Example GitHubAction resource"
--8<-- "docs/apps/github/action.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/github/action.yml"
EOF
```

///

## Cluster-Scoped Resources

Use the cluster variants from the EDA base namespace when you want centralized automation across namespaces.

Cluster-specific behavior:

* `ClusterGitHubIssue` and `ClusterGitHubAction` can watch alarms across namespaces through `trigger.alarm.namespaces`
* query triggers can use fully qualified `.namespace` paths
* cluster resources must reference `ClusterGitHubInstance`

## Workflow Resources

The app also installs two workflow definition resources:

* `CreateGithubIssue`
* `RunGithubWorkflow`

These workflows are run-to-completion programs that do not watch alarms or queries continuously; instead, they submit a single GitHub operation (issue or workflow dispatch) when the workflow is run.

/// admonition | Current behavior
    type: subtle-note

* although the workflow specification contains both `instance` and `clusterInstance`, the current version only supports `instance` (not `clusterInstance`)
* use a regular `GitHubInstance` for these workflow resources
///

//// tab | CreateGithubIssue workflow resource
/// tab | YAML

```yaml title="Example CreateGithubIssue workflow resource"
--8<-- "docs/apps/github/create-github-issue.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/github/create-github-issue.yml"
EOF
```

///
////

//// tab | RunGithubWorkflow workflow resource
/// tab | YAML

```yaml title="Example RunGithubWorkflow workflow resource"
--8<-- "docs/apps/github/run-github-workflow.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/github/run-github-workflow.yml"
EOF
```

///
////

## Validation Notes

When creating resources, follow these rules:

* instances require both `authSecretRef.name` and `authSecretRef.key`
* issues require `repo`, `instance`, `issue.title`, `issue.body`, at least one assignee, and either an alarm or query trigger
* issue title and body templates must be valid Go templates
* actions require `repo`, `workflow`, `ref`, `instance`, and either an alarm or query trigger
* dynamic action parameters must set both `field` and `path` fields
