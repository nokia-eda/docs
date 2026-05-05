# Nokia EDA MCP server

---

## Overview

EDA exposes a built-in [Model Context Protocol](https://modelcontextprotocol.io)
(MCP) server as part of the API server, reachable under the path `/core/mcp` over
the MCP Streamable HTTP transport. Once enabled, MCP-aware clients (Claude
Desktop, Cursor, custom agents, and so forth) can discover and call EDA tools,
resources, and prompts over an authenticated HTTP endpoint. And in proper
EDA fashion, the server is configured **declaratively** through Kubernetes
custom resources in the `ai.core.eda.nokia.com/v1` API group.

Four custom resource kinds shape the server:

- `MCPSettings`: the global on/off switch for the MCP server, plus
  capability flags that advertise which optional MCP features (list-changed
  notifications, completions, logging, etc.) the server supports. A single
  `MCPSettings` custom resource named `mcp-settings` controls the whole server.
- `MCPToolDefinition`: declares an MCP **tool**, a callable action the
  client can invoke. Each tool is backed by exactly one provider (an EDA
  workflow, an EQL query, or an HTTP call), and its inputs and outputs are
  described with JSON schema so MCP clients can validate arguments and
  render forms.
- `MCPResourceDefinition`: declares an MCP **resource** (read-only data
  the client can fetch by URI) or, when `arguments` are present, a
  **resource template** that the client can parameterize. Resources can be
  served from static content, an EQL query, or an HTTP endpoint.
- `MCPPromptTemplate`: declares an MCP **prompt**, a named, parameterized
  message (or sequence of messages, optionally referencing resources) that
  the client can render and send to its model.

The API server watches these Custom Resources continuously and reflects every add, update,
and delete into the live MCP server, so adding a tool or editing a prompt
takes effect immediately. Note that whenever `MCPSettings` itself changes,
any currently connected MCP sessions are disconnected and clients will need
to reconnect.

### Endpoints

| Path | Purpose |
|---|---|
| `POST/GET /core/mcp` | MCP Streamable HTTP transport (the server itself). |
| `GET /.well-known/oauth-protected-resource` | RFC 9728 metadata. Points clients at the EDA API server as the authorization server and at `/core/mcp` as the protected resource. |
| `GET /.well-known/oauth-protected-resource/core/mcp` | Same metadata, MCP-spec-aliased path. |
| `GET /.well-known/openid-configuration` | Proxied to the EDA Keycloak realm so MCP client auto-discovery works. |

## Enabling the server

Create an `MCPSettings` named `mcp-settings` (only that name is honored; see
the note below) in any namespace. The recommended namespace is the one where
your other EDA app custom resources live.

```yaml
apiVersion: ai.core.eda.nokia.com/v1
kind: MCPSettings
metadata:
  name: mcp-settings
  namespace: eda
spec:
  enabled: true
  capabilities:
    promptListChangedNotifications: true
    resourceListChangedNotifications: true
    toolListChangedNotifications: true
    resourceSubscribeSupport: false
    enableCompletions: false
    enableLogging: false
```

Setting `enabled: false` (or deleting the custom resource) tears the server
down. Toggling it causes a clean rebuild of the MCP server and
re-registration of all tools, resources, and prompts.

/// admonition | Note
    type: subtle-note
Some `capabilities` fields (`resourceSubscribeSupport`,
`enableCompletions`, `enableLogging`) are reserved for future use and
are not yet honored.
///

## Defining MCP primitives

MCP servers expose three kinds of building blocks to clients: **tools** are
callable actions the model can invoke, **resources** are read-only data the
client can fetch by URI, and **prompts** are parameterized message templates
the client can render and send to its model. EDA defines each one with a
dedicated Custom Resource (`MCPToolDefinition`, `MCPResourceDefinition`, and
`MCPPromptTemplate`).

All three must be created in the EDA base namespace. Their `metadata.name`
becomes the MCP identifier exposed to clients (the tool name, prompt name,
or resource name), so pick stable, client-friendly names.

### Tools

A tool has a `provider` of **exactly one** of: `workflowRef`, `query`, or
`http`.

#### Workflow-backed tool

The tool input schema is derived automatically from the referenced
`WorkflowDefinition`'s `flowDefinitionResource` CRD. Calls are dispatched
through the EDA workflow engine with a **30 second timeout**. The caller is
checked for `Create` permission on the target CRD before the workflow runs.

```yaml
apiVersion: ai.core.eda.nokia.com/v1
kind: MCPToolDefinition
metadata:
  name: rotate-node-certificate
  namespace: eda-system
spec:
  title: Rotate Node Certificate
  description: Rotate a Node certificate given its name and namespace
  provider:
    workflowRef: bootstrap-rotatecert-gvk
```

#### HTTP-backed tool

The body sent by the MCP client (`input`) is forwarded to the configured URL. If
`includeEDAAuth: true`, the caller's bearer is forwarded, which is required when the
target is the EDA API server.

```yaml
apiVersion: ai.core.eda.nokia.com/v1
kind: MCPToolDefinition
metadata:
  namespace: eda-system
  name: create-core-eda-nokia-com-v1-namespaces
spec:
  provider:
    http:
      url: https://<eda-api-address>/apps/core.eda.nokia.com/v1/namespaces
      method: POST
      timeoutSeconds: 30
      includeEDAAuth: true
  title: Create EDA Namespace
  description: create an EDA Namespace
  inputSchema: |
    {
      "properties": {
        "apiVersion": {
          "default": "core.eda.nokia.com/v1",
          "pattern": "^core\\.eda\\.nokia\\.com/v1$",
          "type": "string"
        },
        "kind": {
          "default": "Namespace",
          "pattern": "^Namespace$",
          "type": "string"
        },
        "metadata": {
          "properties": {
            "annotations": {
              "additionalProperties": {
                "type": "string"
              },
              "type": "object"
            },
            "labels": {
              "additionalProperties": {
                "type": "string"
              },
              "type": "object"
            },
            "name": {
              "maxLength": 253,
              "pattern": "^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$",
              "type": "string"
            },
            "namespace": {
              "default": "eda-system",
              "type": "string"
            }
          },
          "required": [
            "name"
          ],
          "type": "object"
        },
        "spec": {
          "description": "A Namespace is a logical partition within the cluster that provides a mechanism for isolating resources.\nNamespaces allow for resource segmentation, enabling multiple teams or applications to share the same cluster without conflict.",
          "properties": {
            "bootstrap": {
              "description": "Bootstrap configuration for the namespace - if empty no bootstrapping is performed and namespace will be empty.",
              "properties": {
                "fromNamespace": {
                  "description": "The namespace from which to bootstrap resources.  If empty, bootstrap resources are taken from the installed applications' specifications.",
                  "title": "From namespace",
                  "type": "string"
                }
              },
              "title": "Bootstrap",
              "type": "object"
            },
            "description": {
              "description": "An optional description of the use of the namespace.",
              "title": "Description",
              "type": "string"
            }
          },
          "title": "Specification",
          "type": "object"
        }
      },
      "required": [
        "apiVersion",
        "kind",
        "metadata",
        "spec"
      ],
      "type": "object"
    }
  # Optional
  # outputSchema:  
```

The MCP client supplies a JSON body matching `inputSchema`; the EDA MCP
server JSON-marshals it and sends it as the request body. With
`includeEDAAuth: true` the caller's bearer is forwarded, so the call hits
the EDA API server as the same user.

`inputSchema` and `outputSchema` are JSON schema strings. They are validated
before registration; the schema **must** have `"type": "object"` or it is
rejected (with a warning logged) to avoid breaking the MCP server.

`http.trustBundle` is optional. If set, it must reference a `ConfigMap` with
key `trust-bundle.pem` in the EDA namespace. Otherwise the API server's trust
bundle is used.

#### Query-backed tool

The expression is an EQL query, executed via `GET /core/query/eql` using the
caller's bearer. Arguments from the MCP client are substituted into the
expression with `{{name}}` placeholders.

```yaml
apiVersion: ai.core.eda.nokia.com/v1
kind: MCPToolDefinition
metadata:
  name: eql
  namespace: eda-system
spec:
  title: Run EQL Expression
  description: >
    Run an EQL query.
    The eql param is required. The eql param is a string. Examples:
      .namespace.resources.cr.core_eda_nokia_com.v1.toponode
      .namespace.alarms.v1.alarm
      .namespace.node.srl.interface where (.namespace.name = "eda")
      .namespace.node.srl.interface where (.namespace.name = "eda" and name = "ethernet-1/1")
    The result is a JSON object.
  inputSchema: |-
    {
      "type": "object",
      "properties": {
        "eql": { "type": "string", "description": "The EQL query to run" }
      },
      "required": ["eql"]
    }
  provider:
    query:
      expression: '{{eql}}'
```

### Resources

MCP itself defines two related primitives:

- **`Resource`**: a fixed URI the client can fetch directly. The client
  sees it in `resources/list` and reads it with `resources/read`.
- **`ResourceTemplate`**: an RFC 6570 URI template the client must
  parameterize before fetching. The client sees it in
  `resources/templates/list` and is expected to fill in the template
  variables (typically by prompting the user) before issuing
  `resources/read` against the resulting concrete URI.

A single `MCPResourceDefinition` becomes one or the other depending on
whether you declare `arguments`:

- If `spec.arguments` is empty (or omitted), the server registers the CR
  as an MCP **`Resource`** with `spec.uriTemplate` taken as a literal
  URI. Any `{{name}}` placeholders in the provider configuration that
  don't have a value will not be expanded.
- If `spec.arguments` has at least one entry, the server registers the CR
  as an MCP **`ResourceTemplate`**. At read time, the client supplies
  concrete values for the template variables in the request URI; those
  values are extracted with the URI-template library and used to expand
  `{{name}}` placeholders in the provider configuration before the
  resource is resolved.

Provider is **exactly one** of `static`, `query`, or `http`.

#### Static resource

A static resource serves fixed content embedded directly in the custom resource. It is useful for
documentation, schemas, or other small payloads that do not need to be
fetched at request time. URI parameters can still be substituted into the
content.

```yaml
apiVersion: ai.core.eda.nokia.com/v1
kind: MCPResourceDefinition
metadata:
  name: fabric-docs
  namespace: eda-system
spec:
  title: "EDA Fabric App Documentation"
  uriTemplate: "eda://docs/fabric-docs/{version}"
  description: "EDA Fabric App documentation"
  mimeType: "text/markdown"
  provider:
    static:
      content: |
        # EDA Fabric App        
        ## ....
```

#### Query-backed resource

A query-backed resource runs an EQL query via `GET /core/query/eql` using the caller's bearer and
returns the result as the resource body. Arguments declared in `arguments`
are substituted into the expression with `{{name}}` placeholders.

```yaml
apiVersion: ai.core.eda.nokia.com/v1
kind: MCPResourceDefinition
metadata:
  name: srl-node-chassis
  namespace: eda-system
spec:
  title: "SR Linux Node Chassis"
  uriTemplate: "eda://{namespace}/node/{node}/srl/platform/chassis"
  description: "Node chassis"
  mimeType: "application/json"
  arguments:
    - name: namespace
      autocomplete: '{"type":"gvr","group":"core.eda.nokia.com","resource":"namespaces"}'
    - name: node
      autocomplete: '{"type":"gvr","group":"core.eda.nokia.com","resource":"toponodes"}'
  provider:
    query:
      expression: '.namespace.node.srl.platform.chassis where (.namespace.name = "{{namespace}}" AND .namespace.node.name = "{{node}}")'
```

#### HTTP-backed resource

An HTTP-backed resource fetches content from the configured URL and returns it as the resource
body. URI arguments are substituted into the URL (and into headers and
body, if set) with `{{name}}` placeholders. Use this resource type for content that
lives in another EDA service.

```yaml
apiVersion: ai.core.eda.nokia.com/v1
kind: MCPResourceDefinition
metadata:
  name: alarm-definition
  namespace: eda-system
spec:
  title: Alarm definition
  uriTemplate: eda://alarm-definition/{name}
  arguments:
    - name: name
      autocomplete: '{"type":"gvr","group":"core.eda.nokia.com","resource":"alarmdefinitions"}'
  mimeType: application/json
  provider:
    http:
      url: https://<eda-api-server-address>/apps/core.eda.nokia.com/v1/alarmdefinitions/{{name}}
      includeEDAAuth: true
      method: GET
      timeoutSeconds: 30
```

/// admonition | Note
    type: subtle-note
Argument autocomplete is **not** currently supported for resource
argument. The `autocomplete` field on `MCPResourceDefinition.spec.arguments[]`
is parsed but no suggestions are surfaced to MCP clients yet. The field
is accepted for forward-compatibility.
///

### Prompts

A prompt is rendered into one or more messages that the client can send to
its model. Each entry in `content` is **exactly one** of `text` or
`resource`, and both can be parameterized with `{{argName}}` placeholders
filled in from `arguments`.

#### Text content

A `type: text` entry expands `text.template` using the prompt's arguments
and emits a plain-text message. This is the most common pattern: write a
prompt that tells the model how to drive one or more of your registered
tools, and parameterize the user-supplied bits.

```yaml
apiVersion: ai.core.eda.nokia.com/v1
kind: MCPPromptTemplate
metadata:
  name: rotate-node-certificate
  namespace: eda-system
spec:
  title: Rotate Node Certificate
  description: >
    Rotate the certificate of a managed toponode.
  content:
    - type: text
      text:
        template: |
          You are a network automation assistant with access to the
          `rotate-node-certificate` MCP tool. The tool takes a namespace and a
          node name as its input and rotates the certificate of the node in the namespace.

          topoNodes can be listed with the `get-eda-resource` tool using
          `group=core.eda.nokia.com`, `version=v1`, `kind=toponode`.

          If the user does not provide a node name, you should ask for it.
          If the node name is not valid, you should ask the user to provide a valid node name.
          If the node exists in multiple namespaces, and the user does not provide a namespace, 
          you should ask the user to provide the namespace.
          If the namespace is not valid, you should ask the user to provide a valid namespace.
          If the namespace is valid, you should rotate the certificate of the node in the namespace.

          Important:
            Give the RotateCertificate Custom Resource a randomized name otherwise the rotation might fail.

          User inputs:
            - Node name: {{node_name}}
            - Namespace: {{namespace}}
  arguments:
    - name: node_name
      title: Node Name
      description: Name of the node.
      required: true
    - name: namespace
      title: Namespace
      description: EDA namespace where the node is located.
      required: false
```

#### Resource content

A `type: resource` entry emits a resource link whose URI is also
`{{...}}` expanded. The client can fetch that resource (typically an
`MCPResourceDefinition` you've registered) when rendering the prompt.
Text and resource entries can be combined in a single prompt to give the
model both inline instructions and pointers to live data — a typical
pattern is to attach app-specific reference docs alongside the
instructions, so the model has authoritative context to ground its
response in.

The example below drives a fabric deployment and attaches the
`fabric-docs` resource registered earlier (URI template
`eda://docs/fabric-docs/{version}`) as a reference the model can read:

```yaml
apiVersion: ai.core.eda.nokia.com/v1
kind: MCPPromptTemplate
metadata:
  name: deploy-fabric
  namespace: eda-system
spec:
  title: Deploy Fabric
  description: Deploy a new EDA Fabric, grounded in the Fabric App docs.
  arguments:
    - name: fabric_name
      title: Fabric Name
      description: Name of the Fabric to create.
      required: true
    - name: fabric_namespace
      title: Fabric Namespace
      description: EDA namespace where the Fabric will be created.
      required: true
  content:
    - type: text
      text:
        template: |
          Deploy a Fabric named {{fabric_name}} in namespace
          {{fabric_namespace}}. Use the attached Fabric App
          documentation as the authoritative reference for the Fabric
          spec, allocation pools, and underlay/overlay protocols.

          Dry-run the deployment first and ask the user to confirm
          before committing.
    - type: resource
      resource:
        uri: "eda://docs/fabric
```

When the client renders this prompt, it expands `{{fabric_app_version}}`
into the resource URI, fetches `eda://docs/fabric-docs/<version>` from
the EDA MCP server (resolved by the static `fabric-docs` resource
registered above), and ships the docs alongside the text instructions to
its model.

## Connecting a client

Point any MCP client at:

```
https://<eda-api-host>/core/mcp
```

The client speaks the MCP Streamable HTTP transport and authenticates with
a bearer token in the `Authorization` header. The sections below cover how
the server validates that token, how a discovery-aware client obtains one
automatically, how to test from the command line with a pre-issued token,
and how to provision a dedicated Keycloak client for headless agents.

### Authentication

Every request to `/core/mcp` is intercepted before it reaches the MCP layer:

1. The MCP service must be **enabled** (`MCPSettings.spec.enabled: true`),
   otherwise the request is rejected with `MCPServerNotEnabled`.
2. A `Bearer <token>` is extracted from the `Authorization` header. If
   absent, the server replies `401` plus a
   `WWW-Authenticate: Bearer resource_metadata=https://<host>/.well-known/oauth-protected-resource`
   header so the client can start the OAuth flow.
3. The token is validated through the standard EDA authorization stack.
   The resulting user identity is then used by tool and resource handlers
   for per-call authorization (for example, checking permission on the target CRD
   for workflow tools) and for forwarding the bearer to downstream EDA
   APIs when needed.

A client implementing **OAuth 2.1 with discovery** handles steps 2 and 3
automatically:

1. Issue an unauthenticated request and read the `WWW-Authenticate`
   header, which points to `/.well-known/oauth-protected-resource`.
2. Follow that to the protected-resource metadata, which advertises the
   EDA API server as the authorization server.
3. Discover the IdP via `/.well-known/openid-configuration` (proxied to
   the EDA Keycloak realm) and obtain a bearer token.
4. Call `/core/mcp` with `Authorization: Bearer <token>`.

Tokens issued to a normal EDA user work directly. The MCP server itself
does not add or relax any permissions; it only exposes the same surface
area the user already has on the EDA API server. Concretely:

- **Workflow-backed tools** are gated by an EDA RBAC `Create` check on
  the CRD that the referenced workflow targets. A user who cannot create
  that resource through the EDA API server cannot invoke the tool
  through MCP either.
- **Query-backed tools and resources** run the EQL query as the caller
  via `GET /core/query/eql`, so results are filtered by the same
  per-namespace and per-resource read permissions the user has in the
  EDA UI/API.
- **HTTP-backed tools and resources** with `includeEDAAuth: true`
  forward the caller's bearer to the target URL, so the downstream
  service applies its own authorization to the same identity. Without
  `includeEDAAuth`, the call is anonymous to the target.

### Quick local testing

For an interactive smoke test against a running MCP server, use the
official MCP Inspector with a pre-issued bearer:

```bash
TOKEN=$(eda token ...)   # any valid EDA bearer
npx @modelcontextprotocol/inspector \
  --transport Streamable HTTP \
  --url https://<eda-api-host>/core/mcp \
  --header "Authorization: Bearer $TOKEN"
```

### Provisioning a Keycloak client for MCP access

Many MCP clients (CI scripts, fixed-environment IDE integrations, headless
agents) cannot drive the interactive OAuth discovery flow. For those, the
recommended pattern is to provision a dedicated Keycloak client in the
EDA realm and exchange its credentials together with a user's
username/password for a bearer token via the password grant.

1. **Open the EDA Keycloak admin console.**
   `https://<eda-api-host>/core/proxy/v1/identity/admin/master/console/`.
2. **Switch to the `eda` realm** using the realm selector in the
   top-left of the admin console.
3. **Create a new client.** Under *Clients* → *Create client*, set:
    - Client type: `OpenID Connect`
    - Client ID: `eda-mcp` (or whatever name you prefer)
   Then, click *Next* and *Save* with the default settings.
4. **Enable client authentication and Direct access grants.** On the
   client's *Settings* tab, toggle on *Client authentication* and *Direct access grants* (under *Authentication flow*) and Save.
5. **Copy the client secret** from the *Credentials* tab.

Then, request a token with the password grant:

```bash
export EDA_HOST=https://<eda-api-host>
export EDA_MCP_CLIENT_ID=eda-mcp
export EDA_MCP_CLIENT_SECRET=<paste from step 6>
export MCP_USER=<EDA username>
export MCP_PASS=<EDA password>

TOKEN_RESPONSE=$(curl -sSLk -X POST \
  "${EDA_HOST}/core/httpproxy/v1/keycloak/realms/eda/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=${EDA_MCP_CLIENT_ID}" \
  -d "grant_type=password" \
  -d "scope=openid" \
  -d "username=${MCP_USER}" \
  -d "password=${MCP_PASS}" \
  -d "client_secret=${EDA_MCP_CLIENT_SECRET}")

TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r .access_token)
```

Use `$TOKEN` as the bearer in `Authorization: Bearer $TOKEN` when
calling `/core/mcp`. The token is bound to `MCP_USER`, so all EDA RBAC
checks apply to that user — provision a service-style account with the
exact set of namespaces and permissions the agent needs, rather than a
human's interactive account.

/// admonition | Warning
    type: warning
Keep the client secret and `MCP_PASS` out of version control and
out of long-lived shell history. Treat them like any other service
credential.
///

## Operational notes

- **Settings name is fixed**: only an `MCPSettings` whose `metadata.name` is
  `mcp-settings` is honored. Others are silently ignored.
- **Schema validation**: invalid `inputSchema`/`outputSchema` strings cause a
  warning to be logged and the tool is registered without that schema rather
  than failing outright.
- **Workflow timeout**: workflow-backed tools wait at most 30s for the
  workflow result.
- **Trust bundles**: HTTP providers default to the EDA API server trust
  bundle. To call other internal services with their own CA, set
  `trustBundle` to a `ConfigMap` name in the EDA namespace containing
  `trust-bundle.pem`.
