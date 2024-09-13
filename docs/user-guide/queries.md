# EQL - the EDA Query Language

A key philosophy of EDA is to make state streamable for further processing, where state can be sourced externally via gRPC, internally via core services, or locally via Kubernetes. Beyond being used as event triggers, state is incredibly useful for debugging, and so we required a means to allow humans to interact with it also. Enter the EDA Query Language, or EQL.

Loosely based on [Jira Query Language][jql-overview], EQL allows the full surface area of the EDA API, all state info in EDB, along with the full surface area of managed endpoints to be queried and parsed in real time. Queries can be made real time in the heat of troubleshooting, with instantaneous, streaming results. Queries can be sourced as data for visualizations, and streamed via the API or StateAggregator, allowing external applications to constrain event triggers.

The easiest way to interact with queries is via the UI - simply click `Queries` in the navigation menu. You optionally can use the REST API, or `edactl`.

A "query" consists of:

* A `Table`, being the only mandatory portion, e.g. `.node.srl.interface`.
* A `Selector` denoted by the `fields` keyword, defining an array of fields to return (along with any functions to run on said fields), e.g. `.node.srl.interface fields [oper-state, admin-state]`.
* A `Filter` denoted by the `where` keyword, defining an expression contained within parenthesis in which to include or exclude results, e.g. `.node.srl.interface where (admin-state = "disable" and .node.name = "leaf1")`.
* A `Sort`, denoted by the `order by` by keyword indicating the sorting that should be applied to the data before it is returned, e.g. `.node.srl.platform.control.process order by [memory-usage descending]`.
* A `Limit`, denoted by the `limit` keyword, limiting the number of results returned, e.g. `.node.srl.interface limit 10`.
* A `Frequency`, denoted by the `delta` or `sample` keywords, indicating the minimum update period for the query, e.g. `.node.srl.interface delta milliseconds 1000`, or the desire to receive data at a specified interval, irrespective of changes.

## Natural language

Shipping in this release is an implementation of queries using natural language. After opening the query interface in the UI, select the drop down and select `Natural Language`.

/// tip
Try `Show me my up interfaces`
///

/// note
You may need an API key configured in the `.spec.llm` context of your `EngineConfig`.
///

## Table

A `Table` is specified in jspath notation, with a boundary at all lists and containers within a endpoints schema, or within containers/lists provided by StateEngine scripts or external gRPC publishers via StateController.

In simple terms each 'node' within the jspath is its own table - `.node` is a table, `.node.srl` is a table, and `.node.srl.interface` is a table. Tables cannot currently be qualified with keys - instead a `where` should be used.

For example, to select all interfaces on a specific node:

```{.shell .no-select}
.node.srl.interface where (.node.name = "leaf1")
```

/// note
Note that `.node.srl` is only relevant for SR Linux devices. SR OS devices publish to `.node.sros`, and StateEngine apps that normalize data should publish to `.node.normal`.
///

## Selector

A `Selector` is denoted by the `fields` keyword, where the value is an array of fields to return, along with any functions to run. For example `.node.srl.interface FIELDS [admin-state, description] ORDER BY [oper-state ascending natural]`.

No fields other than those defined are returned, if no fields are selected then all fields from the table are returned.

The `fields` keyword must precede any `where` or `order by` keywords.

A set of functions should be available to assist with evaluation and aggregation, for example:
average() to evaluate the average of a field matching a Filter over time (the time window here is currently fixed to the current set of data).
count() to return the count of unique combinations matching a Filter.
sum() to sum the values for a given field matching a Filter.

## Filter

A `Filter` is a string defining any filters to use, a `Filter` is defined with a `where` term.

A `Filter` consists of an ordered set of fields, operators, values, and keywords. Keywords may be capitalized or may not, for example both `and` and `AND` are valid.

Operators include `=`, `!=`, `<=`, `>=`, `>`, `<`, `in`, `not in`.

* `in` is provided an array of values, for example `.node.srl.interface where (oper-state in ["up", "down"])`.
* `in` may also take the values of another field if that field is a leaf-list (i.e. an array).

A `Filter` may string together multiple criteria through the use of `()`, and the keywords `AND`, and `OR`. Note that even when using a single `where` statement it must be contained within `()`.

For example `.table where ((oper-state = "down" and mtu = 1500) or oper-state = "up")`.

A `Filter` may query ancestor keys and values by referencing their full jspath.

For example, to add `Filter` criteria for a parent key `.node.srl.interface.subinterface where (.node.name = "leaf1")`.

You may not currently filter on parent fields other than the key.

## Sort

A `Sort` is similar to a `Filter`, but rather than describing how to select data, it describes how to return data. A `Sort` is denoted by the `ORDER BY` keywords which control the ordering (sorting) of data.

A query may include a single `ORDER BY` keyword, where the value is an array of (fields, sorting algorithms, and directions) which are evaluated in the order they are presented.

For example `.node.srl.interface ORDER by [oper-state ascending natural]`.

The second value may be either `ascending` or `descending`.
The third value is optional and indicates the algorithm to use. Only `natural` is currently supported.

## Limit

A `Limit` is processed after any other operations (perhaps most relevant the `Sort` operation), denoted by the `limit` keyword, limiting the number of results that are returned.

`limit` accepts a single integer value. This can be combined with `Sort` to get the 'top' N results, or the 'bottom' N results, where N is the value provided to the `limit` keyword.

The maximum value for `limit` is `1000`, and the minimum value is `1`.

## Frequency

A `Frequency` allows an end user to control the rate at which data is returned, and is denoted by the `delta` keyword.

The `delta` keyword must be passed two values - one denoting the units used, and another the actual value.
For example `.node.srl.interface.traffic-rate where (in-bps != 0) delta milliseconds 1000`. Meaning do not update the client more than once every 1 second.

The value is the minimum period at which results will be updated for the query, or put another way it controls the maximum rate at which the client will be updated.

[jql-overview]: https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/
