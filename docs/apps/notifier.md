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

Notifier app can be installed using [EDA App Store](app-store.md) or by running the app-installer workflow with `kubectl`:

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

Sources are defined using the **Notifier** Custom Resource (CR), while destinations[^1] (referred to as Providers) are set up using the **Provider** CR. You can mix and match sources, as well as send notifications to multiple destinations.

### Notification source

To configure the source of the notifications, you need to create a **Notifier** CR. The example below shows a configuration for the notification source that will:

* use all Alarms as notification source
* send notifications to the `discord` provider.

/// tab | YAML

```yaml
--8<-- "docs/apps/notifier/notifier.yml"
```

///
/// tab | Apply with `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
--8<-- "docs/apps/notifier/notifier.yml"
EOF
```

///

#### Provider reference

The Notification Source references the Notification Destination by its name. In the example above, the `discord` provider referenced in the Notifier CR is the name of the Provider CR that should exist in the same namespace as the Notifier CR.

### Notification destination

The **Provider** CR defines the destination for the notifications produced by the Notification Source (aka Notifier CR). The below example shows a configuration for the notification destination that sends notification to the Discord webhook:

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

Note, that the Provider name in the `.metadata.name` field should match the provider name referenced in the Notifier CR.

## Providers

Notifier supports multiple notification destinations (aka providers), and leverages the [shoutrrr](https://containrrr.dev/shoutrrr/) package to send notifications to the supported providers. The full list of supported providers is available [at the shouterrr docs](https://containrrr.dev/shoutrrr/v0.8).

Notifier app knows which provider to use based on the `uri` field in the Provider CR.

### Discord

<small>:material-book: [shoutrrr/services/discord/](https://containrrr.dev/shoutrrr/v0.8/services/discord/)</small>

To send notifications to Discord a user needs to create a Discord webhook[^2]. The webhook URL should look like this:

```shell
https://discord.com/api/webhooks/webhookid/token
                                 ^^^^^^^^^ ^^^^^
```

Transform the original webhook URL into the format expected by the Notifier app:

```shell
discord://token@webhookid #(1)!
```

1. Pay attention to the order of the `webhookid` and `token` in the URL. The original webhook URL has the `token` after the `webhookid`, and the Notifier app expects the `token` to be before the `webhookid`.

Now everything is ready for the **Provider** CR creation with the following configuration:
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

<figure markdown>
  ![discord](https://gitlab.com/rdodin/pics/-/wikis/uploads/c648269d831919d0375bdb877d788c17/image.png)
  <figcaption>Discord notification</figcaption>
</figure>

### Slack

<small>:material-book: [shoutrrr/services/slack/](https://containrrr.dev/shoutrrr/v0.8/services/slack/)</small>

To send notifications to Slack a user may create a Slack application. Refer to [Slack's API documentation](https://api.slack.com/quickstart#installing) to create an app.

Once the app is created, and the right scope is given to it, extract the Bot User OAuth Token as explain in the [shouterrr docs](https://containrrr.dev/shoutrrr/v0.8/guides/slack/#getting_a_token). The token should look similar to this:

```
slack://xoxb-1122233344442-7670709334839-abcdefnY03YbI4HCDUh0bHa7@C07LTT12345
```

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

[^1]: The full list of supported destinations/providers is available [here](https://containrrr.dev/shoutrrr/v0.8).
[^2]: Refer to the [Discord docs](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for more information on how to create a Discord webhook.
