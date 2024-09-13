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

* `username`: The username for the user that needs to authenticate
* `password`: The password for the user that needs to authenticate

/// admonition | Some of the hardcoded settings might change in the future
    type: note
///

An example of using `curl` to authenticate and get an access token for the EDA API. Make sure to use your own EDA host and port instead of `###EDA-HOST:PORT###`.

```bash
curl -s https://###EDA-HOST:PORT###/auth/login \
  -d '{ "username": "admin", "password": "admin" }' \
  -X POST
```

/// details | Example output parsed using `jq`
    type: note

```bash
curl -s https://eda.domain.tld/auth/login \
  -d '{ "username": "admin", "password": "admin" }' \
  -X POST | jq -S
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuNnV4VXVyODdyaHNYUEt6dHNlT1Qxc1lERVI5MVVlMXBzWnhhaEdQX19rIn0.eyJleHAiOjE3MjU1NTE3MDgsImlhdCI6MTcyNTU1MTQwOCwianRpIjoiM2Q0ODk2MzQtNWM4Zi00MGY4LWJhNjgtNmNiMGFmNWIyOWZkIiwiaXNzIjoiaHR0cHM6Ly8xMzUuMjI3LjE0LjE5MC9jb3JlL2h0dHBwcm94eS92MS9rZXljbG9hay9yZWFsbXMvZWRhIiwic3ViIjoiZjJhNzUwMzUtNTZhNS00YmEwLWJlOWItNTNlMTM1MTI1OWJlIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYXV0aCIsInNpZCI6Ijg2OGJiOGVlLWZmNmQtNDk4Mi04OGQyLWE0YWE3OGM3MTNjNSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8xMzUuMjI3LjE0LjE5MCIsIioiLCJodHRwOi8vKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZWRhcm9sZV9zeXN0ZW0tYWRtaW5pc3RyYXRvciIsImFkbWluIl19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiRURBIGFkbWluIHVzZXIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbiIsImdpdmVuX25hbWUiOiJFREEiLCJmYW1pbHlfbmFtZSI6ImFkbWluIHVzZXIifQ.O0z4Q7-ZiN0SWIiT9_h1B47_v_WDp4Q4YAc9Y2k5s3Z7MCiT0wkJqSYHlL2cPLbGntIQ3SR_I0vDIBd7uRzh2wTdGltUdJTic_ZaHIhiwBRHqJEuiLu9deCVkjLGbLT12bzohbiWxFkBYCN-2aPn-l8gEbCzU549non2HUseYbwAX2jNY3nKayZvXF2Af1uL3W0uoN0VpVxFFz_CQa6aYLXuO6D0a9lL0i3wn6t19hiG1ABthqzx4w3IsC4vy2ujs1vNqKtxHQ2U0TTznnN0bCPrBIb3Z9-hMed6-FYyaYwc5Zm1O0vVFdQocQPaLPvM2Wzb_9Q2nxJY0SJ5OTB_BA",
  "expires_in": 300,
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJuNnV4VXVyODdyaHNYUEt6dHNlT1Qxc1lERVI5MVVlMXBzWnhhaEdQX19rIn0.eyJleHAiOjE3MjU1NTE3MDgsImlhdCI6MTcyNTU1MTQwOCwianRpIjoiN2EwMzBmMWYtNzIxYy00YzQzLWIxZWMtODIxZWI4OGYwMmU0IiwiaXNzIjoiaHR0cHM6Ly8xMzUuMjI3LjE0LjE5MC9jb3JlL2h0dHBwcm94eS92MS9rZXljbG9hay9yZWFsbXMvZWRhIiwiYXVkIjoiYXV0aCIsInN1YiI6ImYyYTc1MDM1LTU2YTUtNGJhMC1iZTliLTUzZTEzNTEyNTliZSIsInR5cCI6IklEIiwiYXpwIjoiYXV0aCIsInNpZCI6Ijg2OGJiOGVlLWZmNmQtNDk4Mi04OGQyLWE0YWE3OGM3MTNjNSIsImF0X2hhc2giOiJfRzloSUhDSmp3aHloRC1sVlVVUEV3IiwiYWNyIjoiMSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IkVEQSBhZG1pbiB1c2VyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJnaXZlbl9uYW1lIjoiRURBIiwiZmFtaWx5X25hbWUiOiJhZG1pbiB1c2VyIn0.G5e6cw0bQj7z_GSLZuxaVoAI4RAZ6VK856RnfurSInZTbi4DyBsIxEb3-YAJzQp9I0Dm8aHDVU98CpVsJBMr6o6PG0NcmfuyBr8wn86mIVBh9adJ4eaKrV-uRs1OX1Fmd0SBhDnujrdmaLAoGKddzRb-B4PEXDB4gBEiOIU35FgCmdyLXhtVBtXVMm4Eilmww8ezfYZG2nXBS_W_WELhuR0G1xoehCq12T_cRkbfBD-uFLzAbBUdkrl1A-KZSKsrHQU9xMmwxsIEenNWuou8K4VoizD8hdbAN6HlbxQZeaQ9soEP1r2pSJhFa6VJ9xFDpXKiESzNz2jRqJ7_D33WRg",
  "not-before-policy": 0,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIxNmFkMGE4My01MDk2LTQ3ZTUtOTJhZC0zY2RiMjlhN2I4M2UifQ.eyJleHAiOjE3MjU1NTMyMDgsImlhdCI6MTcyNTU1MTQwOCwianRpIjoiOTY5ZmU1MDgtNDdjZi00N2UzLWE3MzAtYWVlMDQwYmI1ZTFkIiwiaXNzIjoiaHR0cHM6Ly8xMzUuMjI3LjE0LjE5MC9jb3JlL2h0dHBwcm94eS92MS9rZXljbG9hay9yZWFsbXMvZWRhIiwiYXVkIjoiaHR0cHM6Ly8xMzUuMjI3LjE0LjE5MC9jb3JlL2h0dHBwcm94eS92MS9rZXljbG9hay9yZWFsbXMvZWRhIiwic3ViIjoiZjJhNzUwMzUtNTZhNS00YmEwLWJlOWItNTNlMTM1MTI1OWJlIiwidHlwIjoiUmVmcmVzaCIsImF6cCI6ImF1dGgiLCJzaWQiOiI4NjhiYjhlZS1mZjZkLTQ5ODItODhkMi1hNGFhNzhjNzEzYzUiLCJzY29wZSI6Im9wZW5pZCByb2xlcyB3ZWItb3JpZ2lucyBhY3IgYmFzaWMgcHJvZmlsZSBlbWFpbCJ9.Qaioh5oYqsi8ghXm3NpElBXGwIgXGShmMeBZNgbxFX9qpEWxMgNzINxoRU6fMnZovIDq26_MYalT4RqgF_MFQA",
  "scope": "openid profile email",
  "session_state": "868bb8ee-ff6d-4982-88d2-a4aa78c713c5",
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
