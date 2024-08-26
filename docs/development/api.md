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
* `client_secret`: Must be set to `vKC0QRSZhcvHYXYTSLqjchmnKMWtBAZy`

/// admonition | Some of the hardcoded settings might change in the future
    type: note
///

An example of using `curl` to authenticate and get an access token for the EDA API. Make sure to use your own EDA host and port instead of `###EDA-HOST:PORT###`.

```bash
curl -s http://###EDA-HOST:PORT###/core/httpproxy/v1/keycloak/realms/eda/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'client_id=eda' \
  --data-urlencode 'grant_type=password' \
  --data-urlencode 'scope=openid' \
  --data-urlencode 'username=admin' \
  --data-urlencode 'password=admin' \
  --data-urlencode 'client_secret=vKC0QRSZhcvHYXYTSLqjchmnKMWtBAZy'
```

/// details | Example output parsed using `jq`
    type: note

```bash
$ curl -s http://eda.domain.tld:9200/core/httpproxy/v1/keycloak/realms/eda/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'client_id=eda' \
  --data-urlencode 'grant_type=password' \
  --data-urlencode 'scope=openid' \
  --data-urlencode 'username=admin' \
  --data-urlencode 'password=admin' \
  --data-urlencode 'client_secret=vKC0QRSZhcvHYXYTSLqjchmnKMWtBAZy' | jq -S
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuNnV4VXVyODdyaHNYUEt6dHNlT1Qxc1lERVI5MVVlMXBzWnhhaEdQX19rIn0.eyJleHAiOjE3MTQ1MTgyMzQsImlhdCI6MTcxNDUxNzkzNCwianRpIjoiYjZmYzhkNjktMWUwNy00N2NiLThjM2QtYjY3NTRmNWQzNjNjIiwiaXNzIjoiaHR0cDovL2hlbGl4Lm5va2lhLmRlbGxhZXJ0LmRldjo5MjAwL2NvcmUvaHR0cHByb3h5L3YxL2tleWNsb2FrL3JlYWxtcy9lZGEiLCJzdWIiOiJmMmE3NTAzNS01NmE1LTRiYTAtYmU5Yi01M2UxMzUxMjU5YmUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJlZGEiLCJzZXNzaW9uX3N0YXRlIjoiM2FiMWJiZTktZWZiNC00ZjQ3LTliZjktZWIyOWZjYWYzY2FlIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIvKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiYWRtaW4iXX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiIzYWIxYmJlOS1lZmI0LTRmNDctOWJmOS1lYjI5ZmNhZjNjYWUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIiwiZ2l2ZW5fbmFtZSI6IiIsImZhbWlseV9uYW1lIjoiIn0.FNToSlNG5cfIcxwtw5MOeWNACw7amXtgS4m-fyGZAjkuV56Nl28RAYQcI1qXW_kuGLRmFbSXep9jxfczLiVDkbfQyJKk4jyuBhcVz3ipad976Z_p8Tpky6y5qrfEc1djd7I498md2X0jjg7Ls3twlJE8fYtQrqxf-1sBF702zDMI8foKi6fXpGQE-gSlvtHDxiMuKlZIVO7jWvD4BObY3p_A-ftoBFmIEy-89MKtr2paFn9rd_H93F3eUh_quQBFGvT0HLFnZWL99GD-bXilu6HA0xdGwTkJ23-kv9dBn35TZn_X3wXtQYtstdgQiLMmKSL1GFdMEK1vlcCjylj0Og",
  "expires_in": 300,
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuNnV4VXVyODdyaHNYUEt6dHNlT1Qxc1lERVI5MVVlMXBzWnhhaEdQX19rIn0.eyJleHAiOjE3MTQ1MTgyMzQsImlhdCI6MTcxNDUxNzkzNCwiYXV0aF90aW1lIjowLCJqdGkiOiIzNjM1NWMxNy0zZjFiLTQ1Y2MtYTFhZC1lNDczOTIwMWE1YjUiLCJpc3MiOiJodHRwOi8vaGVsaXgubm9raWEuZGVsbGFlcnQuZGV2OjkyMDAvY29yZS9odHRwcHJveHkvdjEva2V5Y2xvYWsvcmVhbG1zL2VkYSIsImF1ZCI6ImVkYSIsInN1YiI6ImYyYTc1MDM1LTU2YTUtNGJhMC1iZTliLTUzZTEzNTEyNTliZSIsInR5cCI6IklEIiwiYXpwIjoiZWRhIiwic2Vzc2lvbl9zdGF0ZSI6IjNhYjFiYmU5LWVmYjQtNGY0Ny05YmY5LWViMjlmY2FmM2NhZSIsImF0X2hhc2giOiJraVZSZzduSHZOOVhSMHFEb2E5SUZBIiwiYWNyIjoiMSIsInNpZCI6IjNhYjFiYmU5LWVmYjQtNGY0Ny05YmY5LWViMjlmY2FmM2NhZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJnaXZlbl9uYW1lIjoiIiwiZmFtaWx5X25hbWUiOiIifQ.suc3gsvuryMbbA3k_se8E21UUOuTeFvWxlqU_oE_-zyBu_4wgh0dmVazKKHGE_Wj18w9kWLmlgwfVS9VaxjkzB3lsuRkEXZ5q6RfsfBgbKNQi9ddBY6kYkvr44Ksb7IJZPVqrEeDyxjd9PfFAE4WsWMpMneVfVcSVc1hXo31QMir3Ac2kmbyHqkc5c4I69JUrWWzpFB8PlQFTpPyohUaU4J8SdxPFDKVIyPTAMbx6REQopgIvdWs4cp5wUKGiJ7zP-ErCHtqtE54NE9UVi8Y5LeBM2dX3WAmPwxxg-wN6mM2dxbfSMAYAkkh9UpB8XKxnXGeVRKUjmTcUmx6jCWhEw",
  "not-before-policy": 0,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzMjM4MTJmNS1lNjNiLTQ2ZGMtOTFiNS0yZmM0M2YyNWE3OTMifQ.eyJleHAiOjE3MTQ1MTk3MzQsImlhdCI6MTcxNDUxNzkzNCwianRpIjoiZTA4MjZiY2UtYjIzMC00YTdmLWFiMDQtZjk1MjM1NTQzOTIwIiwiaXNzIjoiaHR0cDovL2hlbGl4Lm5va2lhLmRlbGxhZXJ0LmRldjo5MjAwL2NvcmUvaHR0cHByb3h5L3YxL2tleWNsb2FrL3JlYWxtcy9lZGEiLCJhdWQiOiJodHRwOi8vaGVsaXgubm9raWEuZGVsbGFlcnQuZGV2OjkyMDAvY29yZS9odHRwcHJveHkvdjEva2V5Y2xvYWsvcmVhbG1zL2VkYSIsInN1YiI6ImYyYTc1MDM1LTU2YTUtNGJhMC1iZTliLTUzZTEzNTEyNTliZSIsInR5cCI6IlJlZnJlc2giLCJhenAiOiJlZGEiLCJzZXNzaW9uX3N0YXRlIjoiM2FiMWJiZTktZWZiNC00ZjQ3LTliZjktZWIyOWZjYWYzY2FlIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInNpZCI6IjNhYjFiYmU5LWVmYjQtNGY0Ny05YmY5LWViMjlmY2FmM2NhZSJ9.M6CwX3XL7OHaf8BvYd9nH99l5q28eBxD6UdrB0obLew",
  "scope": "openid profile email",
  "session_state": "3ab1bbe9-efb4-4f47-9bf9-eb29fcaf3cae",
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

For some more details on `Transactions`, check the [Getting Started - Creating a resource](../getting-started/creating-a-resource.md) page and reference the [Updating a resource with a manual transaction](../getting-started/creating-a-resource.md#updating-a-resource-with-a-manual-transaction) section.
