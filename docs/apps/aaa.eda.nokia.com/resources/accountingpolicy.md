---
resource_name: AccountingPolicy
resource_name_plural: accountingpolicies
resource_name_plural_title: Accounting Policies
resource_name_acronym: AP
crd_path: docs/apps/aaa.eda.nokia.com/crds/aaa.eda.nokia.com_accountingpolicies.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Accounting Policy

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

An `AccountingPolicy` selects which [`ServerGroup`](./servergroup.md) resources receive accounting records, and in which order those groups are tried on operating systems that support ordered accounting methods.

## Accounting mode

The required `mode` field is one of:

- `StartStop` sends a start record when a command begins and a stop record when it finishes
- `StopOnly` sends only the stop record after the command finishes

On SR Linux, `mode` applies to command accounting events. On SR OS, `mode` sets the TACACS+ accounting record type.

## Dependencies

### [`ServerGroup`](./servergroup.md)

The `serverGroups` field lists the [`ServerGroup`](./servergroup.md) resources that receive accounting records.

/// admonition | ServerGroup ordering on SR OS
    type: note

The order in which `ServerGroup` resources are listed is not supported on SR OS. SR OS follows the authentication order as defined by the [`AuthenticationPolicy`](./authenticationpolicy.md) when determining which server to send accounting logs to.

///

## Referenced resources

The `AccountingPolicy` does not reference any other EDA resources.

## Examples

/// tab | YAML

```yaml
-{{ include_snippet(resource_name) }}-
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
-{{ include_snippet(resource_name) }}-
EOF
```

///

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
