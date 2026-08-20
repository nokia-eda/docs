# EDA UI localization

Nokia EDA has partial internationalization (i18n) support of the user interface. EDA ships with a default English localization (l10n) and administrators may add additional translation files.

/// Admonition | i18n Support
    type: info

i18n is supported for:

- Core UI components
- error messages from Core APIs
- application resource schemas[^1], including:
    - titles
    - descriptions
    - enum values

i18n is not yet supported for:

- alarms
- app documentation
- dashboards
- EDA Store catalogs
- intent script errors
- non-enum strings in resources
- right-to-left (RTL) localization
- workflow stage names

///

## Managing localization files with edactl

Use the `edactl i18n` command to list, download, and upload localization files. You can:

- Upload and persist l10n files.
- Download a default language file, to be used as a template for translation.

To display help for the `edactl i18n` command, run:

```text
edactl i18n -h
```

```text
Manage i18n resources

Usage:
  edactl i18n [command]

Available Commands:
  get         Get language file
  list        List localization files.
  put         Add or Replace a translation file

Flags:
  -h, --help   help for i18n

Global Flags:
  -A, --all-namespaces         Select all namespaces
      --config string          config file (default is $HOME/.eda/config.yml)
  -c, --context string         Context to use for this execution
      --eda-namespace string   EDA base namespace to use with this request, only used for config generation
      --kubeconfig string      Path to kubeconfig file
  -n, --namespace string       Namespace to use with this request

Use "edactl i18n [command] --help" for more information about a command.
```

### Listing localization files

Use the following command to list localization files for each app group. If an app does not have i18n enabled, the output reports that.

```text
edactl i18n list
```

Example:

```text
Group: aaa.eda.nokia.com
  - i18n not enabled for this app.
Group: ai.core.eda.nokia.com
  - en_US (default)
Group: aifabrics.eda.nokia.com
  - i18n not enabled for this app.
Group: appstore.eda.nokia.com
  - en_US (default)
Group: bootstrap.eda.nokia.com
  - i18n not enabled for this app.
Group: certcheck.eda.nokia.com
  - en_US (default)
Group: components.eda.nokia.com
  - i18n not enabled for this app.
Group: config.eda.nokia.com
  - i18n not enabled for this app.
Group: core.eda.nokia.com
  - en_US (default)
Group: coreext.eda.nokia.com
  - i18n not enabled for this app.
Group: demo.eda.nokia.com
  - en_US (default)
Group: environment.eda.nokia.com
  - i18n not enabled for this app.
Group: fabrics.eda.nokia.com
  - i18n not enabled for this app.
Group: filters.eda.nokia.com
  - i18n not enabled for this app.
Group: interfaces.eda.nokia.com
  - i18n not enabled for this app.
Group: logging.eda.nokia.com
  - i18n not enabled for this app.
Group: management.eda.nokia.com
  - i18n not enabled for this app.
Group: microsegmentation.eda.nokia.com
  - i18n not enabled for this app.
Group: mpls.eda.nokia.com
  - i18n not enabled for this app.
Group: netbox.eda.nokia.com
  - i18n not enabled for this app.
Group: oam.eda.nokia.com
  - i18n not enabled for this app.
Group: os.eda.nokia.com
  - i18n not enabled for this app.
Group: platformmetrics.eda.nokia.com
  - en_US (default)
Group: protocols.eda.nokia.com
  - i18n not enabled for this app.
Group: qos.eda.nokia.com
  - i18n not enabled for this app.
Group: routing.eda.nokia.com
  - i18n not enabled for this app.
Group: routingpolicies.eda.nokia.com
  - i18n not enabled for this app.
Group: security.eda.nokia.com
  - i18n not enabled for this app.
Group: services.eda.nokia.com
  - i18n not enabled for this app.
Group: siteinfo.eda.nokia.com
  - i18n not enabled for this app.
Group: support.eda.nokia.com
  - i18n not enabled for this app.
Group: timing.eda.nokia.com
  - i18n not enabled for this app.
Group: topologies.eda.nokia.com
  - i18n not enabled for this app.
```

### Downloading a default language file

Download the default language file for an app and use it as a template for translation. This example redirects the output to a JSON file.

```text
edactl i18n get core.eda.nokia.com --default > en_US.json
```

### Uploading a translation file

Use the `edactl i18n put` command to add or replace a translation file. The uploaded file is persisted in Nokia EDA. To display usage information, run:

```text
edactl i18n put --help
```

[^1]: In release 26.8.1, i18n is enabled for Core resources. Other Nokia apps will enable i18n in a future release.