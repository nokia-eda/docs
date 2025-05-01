# Notifier

| <nbsp> {: .hide-th } |                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------ |
| **Description**      | Notifier creates and delivers custom notifications from a variety of sources to multiple destinations. |
| **Author**           | Nokia                                                                                                  |
| **Supported OS**     | SR Linux, SR OS                                                                                        |
| **Catalog**          | [nokia-eda/catalog][catalog]                                                                           |
| **Language**         | Go                                                                                                     |
| **Source Code**      | <small>coming soon</small>                                                                             |

[catalog]: https://github.com/nokia-eda/catalog

## Installation

Notifier app can be installed using [EDA Store](app-store.md) or by running the app-installer workflow with `kubectl`:

/// tab | YAML

```yaml
--8<-- "docs/apps/notifier/install.yml"
```

///
/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/notifier/install.yml"
EOF
```

///

## Configuration

After installing the app, you can configure your notification sources and destinations. You have the option to choose between two sources - Alarm or Query - and can send notifications to multiple destinations.

Sources are defined using the **Notifier** or **ClusterNotifier** Custom Resources (CRs), while destinations[^1] (referred to as Providers) are set up using the **Provider** or **ClusterProvider** CRs. You can mix and match sources, as well as send notifications to multiple destinations.

The **ClusterNotifier** and **ClusterProvider** Custom Resources (CRs) are deployed in the eda-system namespace and provide system-wide notification capabilities across all EDA namespaces.
In contrast, the regular **Notifier** and **Provider** CRs are namespace-scoped and can only generate notifications from alarms or queries within their own namespace.

### Notification source

#### Alarm

To configure the source of the notifications, you need to create a **Notifier** or **ClusterNotifier** CR. 

The example below shows a **ClusterNotifier** CR that genrates notifications based on any alarm across all namespaces and sends them to the referenced `discord` provider.

/// tab | YAML

```yaml
--8<-- "docs/apps/notifier/notifier_alarms.yml"
```

///
/// tab | Apply with `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/notifier/notifier_alarms.yml"
EOF
```

///

You can filter which alarms trigger notifications by specifying their `type` in the include/exclude lists (e.g., `InterfaceDown`, `TopoLinkDown`). For **ClusterNotifier** CRs, you can further refine the scope by specifying which namespaces to monitor.

#### Query

EQL queries can be used as a source for notifications. Users can specify the table, select relevant fields, and define conditions to trigger a notification. When the condition is met, a notification is generated and sent using the referenced providers.

The notification format can be customized using two fields: `title` and `template`, both use Go templates. These templates render based on a map that includes all selected fields and the keys returned by the table. The key names match the raw column names shown in the EDA UI query tool.

For example, querying the table `.namespace.node.srl.interface` returns the keys:

- `namespace.name`
- `namespace.node.name`
- `name` (this is the interface name)
- and any field that was explicitly requested under `fields`.

The example below shows a **ClusterNotifier** CR that generates notifications whenever an interface operational state changes to `down` while its administrative state is `enable`.

/// tab | YAML

```yaml
--8<-- "docs/apps/notifier/notifier_query.yml"
```

///
/// tab | Apply with `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/notifier/notifier_query.yml"
EOF
```

///

### Provider reference

The **Notifier**/**ClusterNotifier** CR references the notification destination(s) by name. In the examples above, the `discord` provider referenced in the **ClusterNotifier** CR is the name of the **ClusterProvider** CR that should exist in the `eda-system` namespace. When using namespace-scoped notifiers, both the Notifier and Provider CRs must be in the same namespace, e.g `namespace: eda`.

### Notification destination

Notifier supports multiple notification destinations (aka providers), and leverages the [shoutrrr](https://containrrr.dev/shoutrrr/) package to send notifications to the supported providers with a few provider using custom integrations. The full list of supported providers is available [at the shouterrr docs](https://containrrr.dev/shoutrrr/v0.8).

Notifier app knows which provider to use based on the `uri` field in the Provider or ClusterProvider CR.

#### Discord

To send notifications to Discord a user needs to create a Discord webhook[^2]. The webhook URL should look like this:

```shell
https://discord.com/api/webhooks/webhookid/token
```

Replace the `https://` scheme with `discord://`

```shell
discord://discord.com/api/webhooks/webhookid/token
```

Now everything is ready for the **ClusterProvider** CR creation with the following configuration:
/// tab | YAML

```yaml
--8<-- "docs/apps/notifier/provider_discord.yml"
```

///
/// tab | Apply with `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/notifier/provider_discord.yml"
EOF
```

///

The Discord username posting the notification can be customized using a query parameter `username` overwriting the default webhook bot name.
e.g : `discord://discord.com/api/webhooks/123456789/XXXXXXXXXXXXX?username=EDA`

Example of Discord notifications showing two different TopoLink alarm states: 

A critical alarm when all members are down (red), and a major alarm when the link is in degraded state (green).
Each notification includes detailed information about the resource, its state, and timing.

<figure markdown>
  ![discord](https://gitlab.com/-/project/69488741/uploads/20ad4c7f6748fa969208493ac125258c/notifier_discord_alarms.png)
  <figcaption>Discord alarm notifications</figcaption>
</figure>


#### Teams

The `teams` provider allows users to send **MS Teams** notifications when events occur in the network or within EDA.
The integration is done using **Teams** `Incoming Webhook Connector`, a guide can be found here[^3].

Copy the generated webhook address and replace the `https://` scheme with `teams://` to configure the teams provider.

/// tab | YAML

```yaml
--8<-- "docs/apps/notifier/provider_teams.yml"
```

///
/// tab | Apply with `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/notifier/provider_teams.yml"
EOF
```

///

Example of notifications from the EDA notifer app to Teams showing two consecutive messages: a TopoLinkDown alarm (critical severity, not cleared) indicating all members are down, followed by a TopoLinkDegraded alarm that has been cleared (major severity, cleared=true). Each notification provides structured information including namespace, resource details, severity level, and timestamp.

<figure markdown>
  ![teams](https://gitlab.com/-/project/69488741/uploads/4477d6f94782bfe9c10504fa14bb232a/notifier_teams_alarms.png)
  <figcaption>Teams alarm notifications</figcaption>
</figure>

#### Slack

The `slack` provider allows users to send **Slack** notifications when events occur in the network or within EDA.
The integration is done using **Slack** webhooks, a guide can be found here[^4].

Copy the generated webhook address and replace the `https://` scheme with `slack://` to configure the slack provider.

The Slack channel where the notification must be posted as well as the username posting it can optionally be customized using a query parameters `channel` and `username` overwriting the default webhook name and destination channel.
E.g : `slack://hooks.slack.com/services/XXXXX/YYYYYY/ZZZZZZ?username=EDA&channel=alerts`

/// tab | YAML

```yaml
--8<-- "docs/apps/notifier/provider_slack.yml"
```

///
/// tab | Apply with `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/notifier/provider_slack.yml"
EOF
```

///

Example of Slack notifications showing two consecutive messages: a TopoLinkDown alarm (critical severity, red icon) indicating all members are down, followed by a TopoLinkDegraded alarm that has been cleared (major severity with green checkmark, cleared=true). Both messages provide detailed information including namespace, resource name, group, severity, and timestamp.

<figure markdown>
  ![slack](https://gitlab.com/-/project/69488741/uploads/d15a5bab071f92f75590a5c0d1431f90/notifier_slack_alarm.png)
  <figcaption>Slack alarm notifications</figcaption>
</figure>

#### Email

The `email` provider allows users to send notifications as emails when events occur in the network or within EDA.
Notifier sends an email given an SMTP address and some additional parameters:

The SMTP address must start with `smtp://`.
If a username and password are required they must be part of the URI authority field `smtp://$user:$password@host`
Additional query parameters can be added to the URI:

* `from`     : The sender email address
* `to`       : The recipient email address
* `startTLS` : `yes | no`, if set to `yes` the connection to the SMTP server must use TLS.
* `useHTML`  : `yes | no`, if set to `yes` the email content type will be set to "text/html; charset=UTF-8" otherwise "text/plain; charset=UTF-8"

Example `email` ClusterProvider CR:

/// tab | YAML

```yaml
--8<-- "docs/apps/notifier/provider_email.yml"
```

///
/// tab | Apply with `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/notifier/provider_email.yml"
EOF
```

///

[^1]: The full list of supported destinations/providers is available [here](https://containrrr.dev/shoutrrr/v0.8).
[^2]: Refer to the [Discord docs](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for more information on how to create a Discord webhook.
[^3]: [Teams incoming webhook integration](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet).
[^4]: [Slack webhooks guide](https://api.slack.com/messaging/webhooks)
