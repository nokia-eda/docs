# Allocation Pools

There comes a time where every automation platform needs to allocate addresses and indexes — Whether it’s an IP address, CIDR subnet, VLAN ID, subinterface index, autonomous system number, or more.

EDA provides users and app developers a simple framework for defining and consuming allocation pools.
Behind the scenes EDA ConfigEngine works to ensure:

* **Deterministic allocations** — If provided the same allocation input, the value of any previous allocation will be returned. No surprises!
* **Persist allocations** — Restarting the platform does not result in any re-indexing.
* **Implicit freeing of allocations** — If a resource is updated and no longer needs an allocation, it’s freed up for something else.

All of that while supporting the resizing of allocation pools, whether you need to grow or shrink them!

## Allocation Pool Types

EDA offers four types of allocation pools:

1. **Indices**
    * Specify a size and starting value
    * Return an integer on allocation
2. **IP Addresses**
    * Specify an IPv4 or IPv6 subnet including mask in CIDR format (e.g. `192.0.2.0/24`)
    * Return an address from the subnet on allocation, without any mask information (e.g. `192.0.2.1`)
3. **IP Addresses + Masks**
    * Specify an IPv4 or IPv6 subnet including mask in CIDR format (e.g. `192.0.2.0/24`)
    * Return an address from the subnet on allocation, with mask information (e.g. `192.0.2.1/24`)
    > By default, EDA will not allocate the first and last address in the subnet.  
    >
    > * To enable allocation of the first address, set 'Allocate Network Address' to True.
    > * To enable allocation of the last address, set 'Allocate Broadcast Address' to True.

4. **Subnets**
    * Specify an IPv4 or IPv6 subnet including mask in CIDR format (e.g. `192.0.2.0/24`), and a subnet length (e.g. `31`)
    * Return a subnet of the specified length from the provided subnet on allocation, with mask information (e.g. `192.0.2.8/31`)

## Allocation Pool Segments and Next Allocation

An allocation pool consists of a set of segments. You can think of a segment as a block of indexes — some indexes are taken (allocated) and some are free (either because they were freed or have yet to be used).

In a fresh system where no resources has been deleted, you would see allocations start in the first segment at index 0, and proceeding forwards by 1 for each allocation (i.e allocations within a segment are sequential and consecutive.)

Let’s look at an example. Suppose you have an index pool with two segments:

```yaml
apiVersion: core.eda.nokia.com/v1
kind: IndexAllocationPool
metadata:
  name: example
  namespace: eda
spec:
  segments:
  - start: 0
    size: 5
  - start: 100
    size: 5
```

Initially, the pool would look like this (where `X` represents an allocation):

```
| 0 | 1 | 2 | 3 | 4 | 100 | 101 | 102 | 103 | 104 |
|---|---|---|---|---|-----|-----|-----|-----|-----|
|   |   |   |   |   |     |     |     |     |     |
```

Assuming a resource was created and the config script requests one index, the resulting pool would look like this:

```
| 0 | 1 | 2 | 3 | 4 | 100 | 101 | 102 | 103 | 104 |
|---|---|---|---|---|-----|-----|-----|-----|-----|
| X |   |   |   |   |     |     |     |     |     |
```

If the user created five more instances of the resource, the resulting pool would look like:

```
| 0 | 1 | 2 | 3 | 4 | 100 | 101 | 102 | 103 | 104 |
|---|---|---|---|---|-----|-----|-----|-----|-----|
| X | X | X | X | X |  X  |     |     |     |     |
```

Now assume the resource driving the second instance of the script was deleted (which would result in an implicit free), the pool would look like:

```
| 0 | 1 | 2 | 3 | 4 | 100 | 101 | 102 | 103 | 104 |
|---|---|---|---|---|-----|-----|-----|-----|-----|
| X |   | X | X | X |  X  |     |     |     |     |
```

It is hopefully obvious that the next resource to use the same pool would get the index 1, rather than index 101. A more interesting exercise at this point is to introduce a new segment at the start of the pool:

```yaml
apiVersion: core.eda.nokia.com/v1
kind: IndexAllocationPool
metadata:
  name: example
  namespace: eda
spec:
  segments:
  - start: 200
    size: 5
  - start: 0
    size: 5
  - start: 100
    size: 5
```

The resulting pool would now look like:

```
| 200 | 201 | 202 | 203 | 204 | 0 | 1 | 2 | 3 | 4 | 100 | 101 | 102 | 103 | 104 |
|-----|-----|-----|-----|-----|---|---|---|---|---|-----|-----|-----|-----|-----|
|     |     |     |     |     | X |   | X | X | X |  X  |     |     |     |     |
```

Note that if any of the previous config scripts ran for any reason, they would get their existing allocations, as they have registered keys against them.

If a new allocation was performed now, it would be drawn from the new segment:

```
| 200 | 201 | 202 | 203 | 204 | 0 | 1 | 2 | 3 | 4 | 100 | 101 | 102 | 103 | 104 |
|-----|-----|-----|-----|-----|---|---|---|---|---|-----|-----|-----|-----|-----|
|  X  |     |     |     |     | X |   | X | X | X |  X  |     |     |     |     |
```

Adding or rearranging segments does not result in any allocation changes.

Now let's look at what happens when you shrink a pool by removing a segment:

```yaml
apiVersion: core.eda.nokia.com/v1
kind: IndexAllocationPool
metadata:
  name: example
  namespace: eda
spec:
  segments:
  - start: 200
    size: 5
  - start: 100
    size: 5
```

Allocations in the removed segment (indexes 0, 2, 3, and 4) are freed, and all config scripts dependent on this pool will rerun. The resulting pool would look like:

```
| 200 | 201 | 202 | 203 | 204 | 100 | 101 | 102 | 103 | 104 |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
|  X  |  X  |  X  |  X  |  X  |  X  |     |     |     |     |
```

Note that index 100 was not impacted by the change, nor was index 200.

While this example covers an IndexAllocationPool, the principles are the same across all pool types — the only difference is how you define the segment ranges.

## Segment (Pre-)Allocations & Reservations

Do you want to use allocation pools, but there are scenarios where you need to take the wheel and decide which IP address goes where?
'Allocations' and 'Reservations' options are available in all allocation pool segments to give the manual control you need.

* **Allocations** predefine an allocation against a given key.

* **Reservations** block a range within the segment, preventing it from being allocated by EDA.

/// admonition | Note
    type: subtle-note
The allocation mechanism is also how a default gateway can be provided via a pool and retrieved via an EDA app.
///

## Allocation Scope

Not every allocation needs to be global. For example, subinterface indexes in SR Linux are locally significant to their interface. A user shouldn't need to define separate allocation pools for each interface in the network.

This is where allocation scope comes in!

In EDA, every allocation pool supports scope. Think of the allocation pool resource as a template and the scope as an instance of that template.
By default, allocations use the 'global' scope but an app developer can define a scope based on their needs — whether it’s per interface, per node, or something entirely different. The possibilities are endless!
