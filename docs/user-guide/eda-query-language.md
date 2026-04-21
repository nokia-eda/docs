# EDA query language (EQL)

EDA supports queries using a syntax that is collectively referred to as the EDA Query Language, or EQL.

EQL allows the full surface area of the EDA API, its managed endpoints, and all state information in EDB to be queried and parsed in real time. Queries can be run during troubleshooting, providing instantaneous, streaming results across the entire fleet of the managed devices. Queries can as well be sourced as data for visualizations, and streamed via the API, allowing external applications to constrain event triggers.

/// details | EQL via REST API
    type: subtle-note
In addition to using the UI, EDA Query Language and Natural Query Language responses can be retrieved using API requests with media types of the following:

- `application/json` (default)
- `application/yaml`
- `text/csv`

The media type `application/xml` is not currently supported.

You can also perform EQL queries using EDA's `edactl` command-line interface.
///

In EDA, a query consists of:

- a **Table** that identifies the overall set of data being queried.

    /// admonition | Note
        type: subtle-note
    The Table is the only mandatory element of any query.
    ///

- a **Selector** that defines a set of fields to return (along with any functions to run on those fields).
- a **Filter** that restricts the set of results to return.
- a **Sort** that indicates the order in which results should be returned.
- a **Limit** that restricts the number of results to return.
- a **Frequency** that indicates the minimum period after which to automatically update the query results.

For example:

- `.namespace.alarms.current-alarm`
- `.namespace.alarms.current-alarm where (severity = "critical")`
- `.namespace.alarms.current-alarm where (severity = "critical") order by [type]`
- `.namespace.alarms.current-alarm where (severity = "critical") limit 5`
- `.namespace.alarms.current-alarm where (severity = "critical") order by [type] sample milliseconds 500`

EDA also supports queries using [Natural Query Language](#natural-language-queries).

## Queries and namespaces

Query results are always constrained to the set of [namespaces](namespaces.md) to which the current user has access permissions. By default, a system administrator can see query results spanning all namespaces; but users with fewer namespace privileges see results from only some namespaces, or only a single namespace.

If you have permission to access multiple namespaces, you can cite one or more specific namespaces as part of the filter to constrain the result to those namespaces.

/// admonition | Note
    type: subtle-note
`.namespace.node.srl` is only relevant for SR Linux devices. SR OS devices publish to `.namespace.node.sros`, and StateEngine apps that normalize data should publish to `.namespace.node.normal`.
///

## Elements of a query

A query using EQL can include the following elements.

### Table

A Table is specified in JSPath notation, with a `Table` boundary at all lists and containers within a `TopoNode` schema, or within containers/lists provided by `StateEngine` scripts or external gRPC publishers via `StateController`.

In simple terms, each node within the JSPath file is its own table: `.namespace.node` is a table, `.namespace.node.srl` is a table, and `.namespace.node.srl.interface` is a table.

A `Table` can be identified in the format of a JSPath path without keys. For example: `.namespace.node.srl.interface.subinterface`

Tables cannot currently be qualified with keys. Instead, use a 'where' clause. For example, to select all interfaces on a specific node: `.namespace.node.srl.interface where (.node.name = "leaf1")`.

### Selector

A Selector is denoted by the `fields` keyword, where the value is an array of fields to return, along with any functions to run.

- These fields must exist in the `Table` that is being queried, or the query fails.
- For example, `.namespace.node.srl.interface FIELDS [admin-state, description] ORDER BY [oper-state ascending natural]`.
- No fields other than those defined are returned. If no fields are selected, then all fields from the table are returned.
- The `fields` keyword must precede any `where` or `order by` keywords.

A set of functions can assist with evaluation and aggregation. For example:

- `average()` to evaluate the average of a field matching a `Filter` over time (the time window here is currently fixed to the current set of data).
- `count()` to return the count of unique combinations matching a `Filter`.
- `sum()` to sum the values for a field matching a `Filter`.
- `max()` to return the maximum found value for a given field matching a `Filter`.
- `concat()` to merge multiple keys into a single field with a user defined delimiter.

    For example:

    ```
    fields [ concat(.namespace.name, "/", .namespace.node.name) as "Namespace/Node", .namespace.node.srl.interface.name as Interface ]
    ```

    /// admonition | Note
        type: subtle-note
    `concat()` is used for EDA dashboards when a chart requires a single unique key (or a primary and secondary key), but the EDB path includes three or more keys.
    ///

### Filter

A Filter is a string defining any filters to use. A Filter is defined with a `where` term. The following rules apply:

- A `Filter` consists of an ordered set of fields, operators, values, and keywords.
    - Keywords may be capitalized or not. For example, both `and` and `AND` are valid.
    - Operators include:
        - Comparison operators with `where` clause - `=`, `!=`, `<=`, `>=`, `>`, `<`
        - `and`, `or`, and grouping constructs within `where` clause
        - `in` operator, allowing an array of values to be provided for comparison
        - `not in` operator, allowing an array of values to be provided for exclusion in the comparison

- Field names in a `Filter` are unquoted, and values are quoted where they are strings, and unquoted when they are integers:
    - For example, `.namespace.node.srl.interface where (oper-state = "up")`.
    - For example, `.namespace.node.srl.interface where (ifindex = 49150)`.

- A Filter may string together multiple criteria through the use of `()`, and the keywords `AND`, and `OR`.

    /// admonition | Note
        type: subtle-note
    Even when using a single `where` statement, it must be contained within `()`.
    ///

- EQL Filters support the `is set` and `is not set` operators within a `where` clause.

    Evaluations against an unset field will yield `True` for not equal and NULL for equal.

    - The evaluation follows the three-valued logic of `True`, `False`, and `Null` to ensure logical consistency.
    - `not Null` is `Null`
    - `X and Null` is `Null`
    - `X or Null` is `X`

    - You can use `is set` and `is not set` to check for a field that is optional or has no default value. This comparison on a field checks whether the field has any value. If you want to include unset fields, you must also use `is not set`.

    - This can also be used to check for `Null`, such as in a case where `(mtu < 2000) is not set`, since it behaves like an unset field.

- A Filter can query ancestor keys and values by referencing their full JSPath.

    For example, to add Filter criteria for a parent key:  `.namespace.node.srl.interface.subinterface where (.node.name = "leaf1")`.

    You cannot currently filter on parent fields other than the key.

### Sort

A Sort is similar to a Filter, but instead of describing how to select data, it describes how to return data. A Sort is denoted by the `ORDER BY` keywords which control the ordering (sorting) of data.

A Query may include a single `ORDER BY` keyword, where the value is an array of fields, sorting algorithms, and directions which are evaluated in the order they are presented.

- For example, `.namespace.node.srl.interface ORDER BY [oper-state ascending natural]`.
- The second value may be either `ascending` or `descending`.
- The third value is optional but currently can only be `natural`.

### Limit

A Limit restricts the number of results that are returned. It is denoted by the `limit` keyword. A Limit is processed after any other operations (for example, the Sort operation).

- A `limit` accepts a single integer value.

- This can be combined with Sort to get the 'top' N results, or the 'bottom' N results, where N is the value provided to the `limit` keyword.

- The maximum value for `limit` is 1000, and the minimum value is 1. Any values above or below this return an error.

### Frequency

A Frequency allows you to control the rate at which data is returned, and is denoted by the `delta` keyword.

- The `delta` keyword must be passed two values; one denotes the units used, and the other the actual value.
- For example, `.namespace.node.srl.interface.traffic-rate where (in-bps != 0) delta seconds 1` means "do not update the client more than once every 1 second."
- The value is the minimum period at which results are updated for the query.
- Valid units are `seconds` and `milliseconds`.

### Regular expressions

Some EQL expressions need to match substring (or contains), prefix, and suffix matching on fields. To support these cases (among others), the `~` operator is supported. This allows the matching of regular expressions against values.

For example, the expression `.field where (fieldname ~ "regex-pattern")` would match all objects in the `.field` table, where those objects have a field named `fieldname` and that field contains the string value `regex-pattern`.

The right side of the `~` operator must be a quoted string. If quotes are required inside the regex (for example, to match a literal quote character), you must escape them with a backslash (`\`).

The following regex operations are supported:

- Basic match, where prefixes and wildcards are allowed. For example:

    `.namespace.node.srl.interface where (name ~ "^ethernet-1/")`

    This expression would match all interface names that start with `ethernet-1/`. The `.*` at the end is implied. If that is not wanted, use a `$` to match the end of a value.

- Character classes, where one character is matched from a set. For example:

    `.namespace.node.srl.interface where (name ~ "^ethernet-1/[1,4]$")`

    This expression would match all interface names that start with `ethernet-1/`, then include either a `1` or `4`, with no other characters following.

- Alternation, where one of several alternatives is matched. For example:

    `.namespace.node.srl.interface where (name ~ "^ethernet-1/[1,4]$|^ethernet-1/20")`

    This is similar to the previous example, but would also match any interfaces that start with `ethernet-1/20`.

- The `!~` operator is not supported, but an expression may be wrapped in `not()` to perform the same function. For example:

    `.namespace.node.srl.interface where (not(name ~ "^ethernet-1/[\\d]$|^ethernet-1/20"))`

- All other typical regex operators are supported:

    - `\\d` to match a digit.
    - `\\w` to match an entire word (to the next whitespace).
    - `\\s` to match whitespace.
    - `\\n` to match a newline.
    - `.` for matching any character except a newline.
    - `*`, `+`, `?` for matching the preceding element 0 or more, one or more, or zero or one respectively.
    - `^` to match the start of a string.
    - `$` to match the end of a string.

## Consolidated JSON to support EQL

It is common to query for values that are presented as a single object in the EDA GUI, but in fact span multiple containers or lists as they are normally stored within EDA. Such queries can exceed the usual supported scope of a single EQL query.

For example, a query like "show me all 100G interfaces that are enabled" requires data involving the `enabled` field which is stored as `.spec.enabled`, and the `speed` field stored as `.spec.ethernet.speed`.

To support such queries, Custom Resource (CR) entries are merged into a single nested table entry so that:

- all configuration and state are in the same table
- queries can thereby span all fields within an object

Queries against sub-tables of objects are not supported. Queries must start at the root of the object, with syntax resembling the following examples.

For the 100G speed and Enabled query described earlier:

```
.namespace.resources.cr.interfaces_eda_nokia_com.v1alpha1.interface where (spec.ethernet.speed = "100G" AND spec.enabled = "true")
```

To include "state" in the same query:

```
.namespace.resources.cr.interfaces_eda_nokia_com.v1alpha1.interface where (spec.ethernet.speed = "100G" AND spec.enabled = "true" AND .status.operationalState = "down")
```

## Natural-language queries

When creating a query in EDA, you also have the option of writing the query in natural language. With a natural-language query, you can ask questions of EDA such as:

- List all up interfaces
- List all interfaces that have an MTU of 9232, sorted by interface name
- What statistics are available on interfaces
- Show me any interfaces with error counters above 0
- Show me the unique reasons interfaces are down
- Show me the unique reasons interfaces are down, and count the unique values
- Show me all of my processes sorted by memory usage descending
- Show me the total numbers of packets sent on all interfaces
- Show me the number of MAC addresses on subinterfaces on "leaf-1-1", include the interface name

/// admonition | Note
    type: subtle-note

1. Natural-language support requires the LLM API key to be provided in the `.spec.llm.apiKey` of your `EngineConfig` resource.
2. Currently, natural-language queries are resolved only against the `.node.srl` table.
///

## Creating a query with EQL

1. Use the **Main** navigation panel to select **Queries** to open the Query Builder page.

2. In the query types drop-down list, click **EQL Query**.

3. Enter an expression using EDA Query Language (EQL), as described in [Elements of a query](#elements-of-a-query).

    - Begin the query with a period (`.`).
    - As you begin typing the query, EDA offers suggestions for the next element in the expression.
    - The finished query must specify a table in JSPath notation. This table identifies the overall set of data being queried. Optionally, the query can also include:
        - a Selector that defines a set of fields to return (along with any functions to run on said fields).
        - a Filter that restricts the set of fields to return.
        - a Sort that indicates the order in which data should be returned.
        - a Limit that restricts the number of results to return.
        - a Frequency that indicates the minimum period after which to automatically update the query results.
4. When you have completed the query expression, click **Query** to view the results.

    /// admonition | Note
        type: subtle-note
    Results are limited to the first 1,000 matches.
    ///

## Creating a query with natural language

1. Use the **Main** navigation panel to select **Queries** and open the Query Builder page.

2. In the query types drop-down list, click **Natural Language Query**.

3. Type your question using simple language (not necessarily English). Your question must specify something to return information about (such as nodes, links, or other network objects).

    /// admonition | Note
        type: subtle-note
    Currently, natural-language queries are resolved only against the `.node.srl` table.
    ///

    Optionally, your question can also specify:

    - conditions that those objects must meet.
    - ways to sort the returned data.
    - a limit on how many results to return.
    - a time period after which to automatically update the query results.

4. When you have finished typing your query, click **Query** to view the results.

    /// admonition | Note
        type: subtle-note
    EDA renders your natural language question in EDA Query Language, and displays the EQL expression immediately below the query field.
    ///

    /// admonition | Note
        type: subtle-note
    Results are limited to the first 1,000 matches.
    ///
