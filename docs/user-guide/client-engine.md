# Client tables and insights

Nokia Event-Driven Automation (EDA) manages fabric state, but it does not automatically discover all traffic and every
endpoint connected to the network. EDA provides a centralized mechanism for EDA applications and external integrations
to publish endpoint metadata into *client tables*. You can then read a unified, correlated view of clients across the
network.

This allows operators to gain insight into what is going on in the network.

## Key concepts

| Term                     | Description                                                                                               |
|--------------------------|-----------------------------------------------------------------------------------------------------------|
| **Client**               | A record representing an endpoint on the network.                                                         |
| **Client table**         | A logical table that stores client records for a specific use case. Defined by a `ClientTable` CRD.       |
| **Client provider**      | A controller that collects client information from a source system and writes it to a client table.       |
| **Client consumer**      | A service that reads client information from a unified or normalized client table.                        |
| **Unified client table** | The consolidated table for a `ClientTable` CRD after providers have correlated and written their records. |
| **Normalized field**     | A field that EDA merges across providers into a single value in the normalized client table.              |
| **Confidence level**     | A value that indicates how reliable a normalized field value is.                                          |

## Client tables

A `ClientTable` CRD defines the keys used to correlate entries within a client table. The name of the `ClientTable` CR
is also the name of the client table in EDB. A `ClientTable` CR is not namespaced. The table itself however will live in
every namespace.

The `networks` client table will for example be accessible through the following path:

/// tab | EDB path

```.namespace.clienttables.networks```
///

/// tab | edactl command
```edactl query .namespace.clienttables.networks -o yaml```
///

## Client providers

Client providers are the pluggable components that collect endpoint information from their respective sources (for
example, the network fabric, a hypervisor, or a cloud platform).

Each provider:

1. Correlates its data against existing entries in the target client table.
2. Writes the correlated record to the unified client table in EDB through the EDK.

A `ClientProvider` CRD defines a provider that writes to a specific client table, along with the fields it contributes.
EDA combines field definitions from all providers that write to a table and builds the JSON schema you see in the API
and UI.

## Client table keys

Keys determine how client providers match new records to existing entries. Multiple client tables can exist for
different use cases, each with its own key set.

For the networks client table, correlation keys include:

- MAC address
- IP address
- BridgeDomain
- Router

## Normalized fields

Some fields represent the same endpoint attribute across multiple providers (for example, hostname or operating system).
In EDA, normalized fields provide you with a single merged value. A client provider application marks which of its
fields are normalized through annotations.

## Confidence levels

For each field, the client provider assigns a confidence level. When these fields are lifted into the normalized client
table, the confidence level is used to determine the value that is kept:

- When multiple providers report the same value, the confidence level is the highest confidence reported by any of those
  providers.
- When providers report different values at the same highest confidence level, the confidence level is `0`. EDA selects
  one value using the provider whose name sorts first alphabetically.

Fields that are not present in the normalized client table remain available under their originating client provider.

## EDA networks client provider

The `Services` app contains the Networks Client Provider, which populates the client table with the information that can
be discovered from within the network itself (from the SR Linux and SR OS systems managed by EDA). For details,
including how to view discovered endpoints, see the [app documentation](../apps/services.eda.nokia.com/index.md).
