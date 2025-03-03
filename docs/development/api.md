# API

## Overview

EDA includes an HTTP REST API to support software integration. By using the REST API, you can write your own software that can configure any feature of the EDA.

## General Concepts

The EDA API is following a very similar model as the [Kubernetes Resource Model](https://github.com/kubernetes/design-proposals-archive/blob/main/architecture/resource-management.md). Every custom resource that gets added through the installation of an App, will be available through the EDA API in a similar way as custom resources in Kubernetes are available through the Kubernetes API.

There are two major components to the EDA API, and a few internal components:

*Core API*
: The Core API is used to manage a few core concepts of EDA, like getting and posting `Transactions`, executing EQL `Queries` and getting `NodeConfigs` for specific nodes.

*Apps API*
: The Apps API is where every App installed into EDA, exposes its custom resources. That includes all the default installed Apps.

    /// admonition | EDA API vs Kubernetes API & `kubectl`
        type: note
In the current EDA model, both the EDA API and Kubernetes API (or `kubectl`) can be used to manage certain resources. However, be aware that anything that has been internally generated within EDA might not be fully visible to the Kubernetes environment and only available over the EDA API.
    ///

*OpenAPI API*
: This API provides access to OpenAPIv3 Specifications for the Core and Apps API.

*HTTPProxy API*
: The EDA API server acts as a transparent passthrough proxy for certain services, like Keycloak for authentication and other internal services. This is handled by the HTTPProxy API.

/// admonition | Do not change or manipulate any of the HTTPProxy API settings as this can break your EDA deployment.
    type: note
///

### Synchronous vs Asynchronous

All the API requests are handled as synchronous API requests. To make asynchronous API requests use the [`Transaction` API](#transactions) described later.

## Authentication

For authentication and authorization, EDA uses Keycloak as its backend. Keycloak is a proven and secure solution for Identity and Access management. EDA uses Keycloak through the OpenID Connect protocol where within the UI, the user is redirected to Keycloak for authentication and then send back with the necessary tokens for the API to authenticate and verify the user as a legitimate user. This is referred to as the Standard Flow (Authorization Code Flow in the OAuth2 specifications).

For the API, a similar workflow can be followed by using the Direct Access Grant flow (Resource Owner Password Credentials Grant in the OAuth2 specifications). In this case the API client directly authenticates with Keycloak, and uses the token received for further API calls to the EDA API. The API client is also responsible for refreshing or renewing their token.

The authentication request requires the following fields:

* `client_id`: Must be set to `eda`
* `grant_type`: Must be set to `password`
* `scope`: Must be set to `openid`
* `username`: The username for the user that needs to authenticate
* `password`: The password for the user that needs to authenticate
* `client_secret`: The Keycloak client secret for client ID `eda`[^1]

/// admonition | Some of the hardcoded settings might change in the future
    type: note
///

/// details | Getting the `client_secret`
    type: note
Every EDA deployment gets a unique client secret token generated during installtion for API clients. To retrieve it, follow these steps:

* Navigate to `{EDA_URL}/core/httpproxy/v1/keycloak` in your browser.
* Log in with the Keycloak administrator username and password (documented in the official User Guide).
* From the **Keycloak** drop-down list on the upper left, select **Event Driven Automation** (eda).
* Select **Clients** from the menu on the left.
* Select **eda** in the client table.
* Select **Credentials** in the tab bar on the top.
* Copy the **Client Secret**.

//// admonition | The official User Guide contains steps on how to change this client secret
    type: note
////

///

An example of using `curl` to authenticate and get an access token for the EDA API. Make sure to use your own EDA URL and Keycloak client secret.

```bash
curl -s https://eda.example.com:9443/core/httpproxy/v1/keycloak/realms/eda/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'client_id=eda' \
  --data-urlencode 'grant_type=password' \
  --data-urlencode 'scope=openid' \
  --data-urlencode 'username=<USERNAME>' \
  --data-urlencode 'password=<PASSWORD>' \
  --data-urlencode 'client_secret=<EDA CLIENT SECRET>'
```

/// details | Example output parsed using `jq`
    type: note

```bash
curl -s https://eda.example.com:9443/core/httpproxy/v1/keycloak/realms/eda/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'client_id=eda' \
  --data-urlencode 'grant_type=password' \
  --data-urlencode 'scope=openid' \
  --data-urlencode 'username=admin' \
  --data-urlencode 'password=admin' \
  --data-urlencode 'client_secret=9eGhwdAaox8bQ5DnfuUHuQTbOxhJxUwg' | jq -S
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJBTHBheFhxanhaYmY5Vy1Pb3JpVnoxSUNTUV9SLUNrc05jZzVGRGFadUI0In0.eyJleHAiOjE3MzM5OTMyNDcsImlhdCI6MTczMzk5Mjk0NywianRpIjoiZjExZTdmM2UtMzFkNi00NTQ0LWE3MDUtMjA2Mzg0ZTYyYmNiIiwiaXNzIjoiaHR0cHM6Ly9wbG0tc2Itazgubm92YWxvY2FsOjk0NDMvY29yZS9odHRwcHJveHkvdjEva2V5Y2xvYWsvcmVhbG1zL2VkYSIsInN1YiI6ImYyYTc1MDM1LTU2YTUtNGJhMC1iZTliLTUzZTEzNTEyNTliZSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImVkYSIsInNpZCI6ImYyZTU1YjQ2LWRiN2YtNGIwMi05ZTIwLTc2YTc2YWE0MDYwMSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiLyoiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImVkYXJvbGVfc3lzdGVtLWFkbWluaXN0cmF0b3IiLCJhZG1pbiJdfSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IkVEQSBhZG1pbiB1c2VyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJnaXZlbl9uYW1lIjoiRURBIiwiZmFtaWx5X25hbWUiOiJhZG1pbiB1c2VyIn0.ZH2vO1sbxm4tke2bE1fUdUbkCtHYo3bFUZpr0J46GL0lGpyIf0LkxOnosatjpLCQl7-CpExhZCv11SmUM6W6c4DoX6d90PKeC-t-GoSKshAxGIh7njtFt1_dYAf1NgF4EGOQMPINj-_n4igjU22Ef7aU8c05m-QkbIPykYFJ0BefqG_H8A1QzNvntADrEfrpHAudGFxB1Ei5FpBxIRfqX40B7_9brzWMlrRRXeWA9i-JVe-6JXQxTTqRKAF9sWGllTA-vbcl-MZ1WsGcC8yS-KQ9nyTrqkwT4Sh06Z7s8IpqBNPEcVJ8p_X65bblGoRKrXMSD0zEXM2zTsJRGd6JVA",
  "expires_in": 300,
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJBTHBheFhxanhaYmY5Vy1Pb3JpVnoxSUNTUV9SLUNrc05jZzVGRGFadUI0In0.eyJleHAiOjE3MzM5OTMyNDcsImlhdCI6MTczMzk5Mjk0NywianRpIjoiODM0MGVlMWQtOThkNC00ZmQ5LThhOTQtNTIwNTQ5YWJlMjE3IiwiaXNzIjoiaHR0cHM6Ly9wbG0tc2Itazgubm92YWxvY2FsOjk0NDMvY29yZS9odHRwcHJveHkvdjEva2V5Y2xvYWsvcmVhbG1zL2VkYSIsImF1ZCI6ImVkYSIsInN1YiI6ImYyYTc1MDM1LTU2YTUtNGJhMC1iZTliLTUzZTEzNTEyNTliZSIsInR5cCI6IklEIiwiYXpwIjoiZWRhIiwic2lkIjoiZjJlNTViNDYtZGI3Zi00YjAyLTllMjAtNzZhNzZhYTQwNjAxIiwiYXRfaGFzaCI6IlNJRUREbWdpb2xneXpPT2lqQ3ZHRWciLCJhY3IiOiIxIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiRURBIGFkbWluIHVzZXIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbiIsImdpdmVuX25hbWUiOiJFREEiLCJmYW1pbHlfbmFtZSI6ImFkbWluIHVzZXIifQ.a9946wNL4_UCfi9LmysRz6wiZG3Zgt84Vz6pa5HfxRcQj5tvFsoBVNCSWd07OzxAS_QuPsMESl9WM4WalUW4Ib6XyNEPENvJsQE8mRWSm-x1R0d1lqrGSaiOJzKX5XUNgZ1u7PRbG-jtlcY-Iaq3Ei7sfOWVmXz8mKOyGteRCa9MSrbD4oFe52DTPNV4EwHIbkI8hUuO9dvgu3MdX6OdLSU9FApDAQjrMo7dqF9_E5SfGvnIPWcAiPD2QyuTP6ZF2SBDEX0OIqn7LNiyyeg4t6RylCakgi31zi_cTY3SfeMhmc9_X4SOj0XbmqZYM7o_mCFxbXTjeSVLcJv4zvuMHg",
  "not-before-policy": 0,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI1NDRjYThkOC0yN2JkLTRlYTAtOGY2Ny1jOTkzYjExMDAwZDYifQ.eyJleHAiOjE3MzM5OTQ3NDcsImlhdCI6MTczMzk5Mjk0NywianRpIjoiZmE2OGQwYWEtNTcyOS00ZjhiLWE5OWUtNDQyNmY3ZWEwNzg5IiwiaXNzIjoiaHR0cHM6Ly9wbG0tc2Itazgubm92YWxvY2FsOjk0NDMvY29yZS9odHRwcHJveHkvdjEva2V5Y2xvYWsvcmVhbG1zL2VkYSIsImF1ZCI6Imh0dHBzOi8vcGxtLXNiLWs4Lm5vdmFsb2NhbDo5NDQzL2NvcmUvaHR0cHByb3h5L3YxL2tleWNsb2FrL3JlYWxtcy9lZGEiLCJzdWIiOiJmMmE3NTAzNS01NmE1LTRiYTAtYmU5Yi01M2UxMzUxMjU5YmUiLCJ0eXAiOiJSZWZyZXNoIiwiYXpwIjoiZWRhIiwic2lkIjoiZjJlNTViNDYtZGI3Zi00YjAyLTllMjAtNzZhNzZhYTQwNjAxIiwic2NvcGUiOiJvcGVuaWQgcm9sZXMgd2ViLW9yaWdpbnMgYWNyIGJhc2ljIHByb2ZpbGUgZW1haWwifQ.SQeRoXLXA61l8AozNH2iaOYR0lJVMYWTtbAEYKY4lREYYesAAMNRVk5wcLR1oKJrFzCFRnhMmIEZysQ7D_DDcw",
  "scope": "openid profile email",
  "session_state": "f2e55b46-db7f-4b02-9e20-76a76aa40601",
  "token_type": "Bearer"
}
```

///

## OpenAPI Specifications

Detailed information about all of the individual API calls is available in the OpenAPI (v3) formats. You can download OpenAPIv3 JSON files from your EDA deployment.

You can then use these files within your own tools that can work with the standard OpenAPI specifications.

### Listing the Available API Specifications

For each App deployed, and the core, individual API Specifications are available through API requests to the `openapi` endpoint. To list the available API Specifications and their relevant URLs, first make sure you get an `access_token` through the [Authentication](#authentication) process. Then you can execute the following curl command to get the list of APIs and OpenAPI Specification URLs per API. Make sure to use your own EDA host and port instead of `###EDA-HOST:PORT###` and your access token instead of `###ACCESS-TOKEN###`.

```bash
curl -s http://###EDA-HOST:PORT###/openapi/v3 \
  -H 'Authorization: Bearer ###ACCESS-TOKEN###' \
  -H 'Content-Type: application/json'
```

/// details | Example output parsed using `jq`
    type: note

```bash
$ curl -s http://eda.domain.tld:9200/openapi/v3 \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuNnV4VXVyODdyaHNYUEt6dHNlT1Qxc1lERVI5MVVlMXBzWnhhaEdQX19rIn0.eyJleHAiOjE3MTQ2MDMwNjAsImlhdCI6MTcxNDYwMjc2MCwianRpIjoiYzdiZjU3NGUtY2ZkNi00Nzk3LTk2NzItMWI5Y2E5YTg2NzQ2IiwiaXNzIjoiaHR0cDovL2hlbGl4Lm5va2lhLmRlbGxhZXJ0LmRldjo5MjAwL2NvcmUvaHR0cHByb3h5L3YxL2tleWNsb2FrL3JlYWxtcy9lZGEiLCJzdWIiOiJmMmE3NTAzNS01NmE1LTRiYTAtYmU5Yi01M2UxMzUxMjU5YmUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJlZGEiLCJzZXNzaW9uX3N0YXRlIjoiMTFkZjU2OWEtNTZhYi00NmMyLWJkOTItNTJkYTg1YzM4NzA4IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIvKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiYWRtaW4iXX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiIxMWRmNTY5YS01NmFiLTQ2YzItYmQ5Mi01MmRhODVjMzg3MDgiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIiwiZ2l2ZW5fbmFtZSI6IiIsImZhbWlseV9uYW1lIjoiIn0.bfTVRxe8KaVAqxjjDKIOJI6UGtJtpKc4W58ouvM1ILAVTiUtaWONT9xGIWDsUaEOzWQTlg-fjYWD3SmAMwPMo11wXafQkL7hTItj6Gs0DalwvmarXGetaVc7rVQhG5p3kvTQ0rNYqjE2bU763ml173kPXNKWUl7VXArCVK6uZ0azBDDX5uzlFBd5QEBtn1pH_-rATheCpvnkjC3s2WfJhDULfkix63N5MQWwhOajAKRe5mXTWLv9W9d_nwDsrHipPBtvAvG65I7s6tqjFH_M--PQPXifsl73v0hTnIHzC9ujpcGxkxctK9DvpwADF7TmuKVjbFHZqxp3FT7HxaK6Zg' \
  -H 'Content-Type: application/json' | jq -S
{
  paths: {
    apps/anomalies.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/anomalies.eda.nokia.com/v1alpha1
    },
    apps/appstore.eda.nokia.com/v1: {
      serverRelativeURL: /openapi/v3/apps/appstore.eda.nokia.com/v1
    },
    apps/bootstrap.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/bootstrap.eda.nokia.com/v1alpha1
    },
    apps/config.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/config.eda.nokia.com/v1alpha1
    },
    apps/connect.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/connect.eda.nokia.com/v1alpha1
    },
    apps/core.eda.nokia.com/v1: {
      serverRelativeURL: /openapi/v3/apps/core.eda.nokia.com/v1
    },
    apps/fabrics.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/fabrics.eda.nokia.com/v1alpha1
    },
    apps/filters.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/filters.eda.nokia.com/v1alpha1
    },
    apps/interfaces.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/interfaces.eda.nokia.com/v1alpha1
    },
    apps/lldp.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/lldp.eda.nokia.com/v1alpha1
    },
    apps/oam.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/oam.eda.nokia.com/v1alpha1
    },
    apps/protocols.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/protocols.eda.nokia.com/v1alpha1
    },
    apps/qos.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/qos.eda.nokia.com/v1alpha1
    },
    apps/routing.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/routing.eda.nokia.com/v1alpha1
    },
    apps/routingpolicies.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/routingpolicies.eda.nokia.com/v1alpha1
    },
    apps/services.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/services.eda.nokia.com/v1alpha1
    },
    apps/system.eda.nokia.com/v1alpha1: {
      serverRelativeURL: /openapi/v3/apps/system.eda.nokia.com/v1alpha1
    },
    core: {
      serverRelativeURL: /openapi/v3/core
    }
  }
}
```

///

### Fetching the API Specifications for an App

For each of the App/Version and the Core, the `serverRelativeURL` is the full URI to the API specifications for that specific App/Version. You can use that to fetch the full OpenAPIv3 Specifications for the resources used and exposed by that specific App and Version. Below is an example for the `connect` App. First make sure you get an `access_token` through the [Authentication](#authentication) process. Then you can execute the following curl command to get the list of APIs and OpenAPI Specification URLs per API. Make sure to use your own EDA host and port instead of `###EDA-HOST:PORT###` and your access token instead of `###ACCESS-TOKEN###`.

```bash
curl -s http://###EDA-HOST:PORT###/openapi/v3/apps/connect.eda.nokia.com/v1alpha1 \
  -H 'Authorization: Bearer ###ACCESS-TOKEN###' \
  -H 'Content-Type: application/json'
```

## Transactions

`Transactions` are groupings of replace (create/update) and/or delete actions of an arbitrary number of API resources as a single transaction. A `Transaction` can contain different types of API resources. A transaction either succeeds or fails, if it fails, it is entirely rolled back.

A transaction can also be executed in a dry-run mode, where all configurations are generated and validated, but the resulting configuration is not send to the different `Toponodes`. If the dry-run results are satisfactory, you can proceed to finalize the transaction, disabling the dry-run mode, to apply the changes to the production environment.

The result of a `Transaction` is stored in a `TransactionResult` resource, which would identify all of the resources that were directly or indirectly created, updated or deleted.

For some more details on `Transactions`, check the [Getting Started - Units of automation - Transactions](../getting-started/units-of-automation.md#transactions) page.

[^1]: Use the Keycloak administrator console to retreive the client secret. The secret can also be regenerated.

    1. Navigate in web browser to `{EDA_URL}/core/httpproxy/v1/keycloak`
    2. Login with the Keycloak administrator username and password.
    3. There is a dropdown in the upper left which will say "Keycloak". Select "Event Driven Automation eda" in that dropdown.
    4. Select "Clients" in the menu on the left.
    5. Select "eda" in the client table in the main web page area.
    6. Select "Credentials" in the Tab bar containing, "Settings/Keys/Credentials/Roles/..."
    7. The current "Client Secret" can be copied/viewed.
    8. The user can click on the "Regenerate" button to generate a new random value for the secret, which can then be copied/viewed.
