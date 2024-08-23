# Generating topologies

You can override the topology used with the `TOPO=` argument, for example

```{.shell .no-select}
make TOPO=path/to/topo.yaml topology-load
```

Where the YAML file is a `ConfigMap` containing a JSON object describing the topology. You can use the example three node topology to build any topology you like, assuming you have the resources on your worker nodes to support the simulation of that topology.

## Topology generation

In order to assist with getting started, a topology generator is provided, this app allows you to define a topology in abstract terms, for example:

```{.json .no-select}
{
  "leaf": {
    "NodeCount": 2,
    "Platform": "7220 IXR-D3L",
    "LayerRole": "leaf",
    "NextLayerRole": "spine",
    "Uplinks": 2,
    "Downlinks": 2,
    "SlotCount": 1,
    "PodId": "1",
    "GenerateEdge": true,
    "NodeProfile": "srlinux-0.0.0",
    "Version": "0.0.0",
    "EdgeEncapType": "dot1q"
  },
  "spine": {
    "NodeCount": 1,
    "Platform": "7220 IXR-H2",
    "LayerRole": "spine",
    "NextLayerRole": "superspine",
    "Uplinks": 2,
    "Downlinks": 4,
    "SlotCount": 1,
    "PodId": "1",
    "NodeProfile": "srlinux-0.0.0",
    "Version": "0.0.0"
  }
}
```

This defines a three node topology with one spine and two leaves.

With this file, run the generator and point to it, from the `tools` pod:

```{.shell .no-select}
./eda-topo-generator -f <path-to-json>
```

By default this will generate the content `generated_topo_pod_<PodId>.json`.

## Topology deployment

Once you have a topology defined using the generator (or handcrafted!), you can use the `generator` to apply it to the cluster. The generator reads from two locations:

* A `ConfigMap` named `topo-config` (the example three node topology was loaded here).
* A passed in JSON file, when called with the `-f` flag. If you generated your own topology you'll want to use this approach.

The tool generates the following:
    * `TopoNode` resources matching the topology.
    * `TopoLink` resources matching the topology.
    * `Interface` resources for every interface in the topology.
    * Loopback `Interface` resource for every `TopoNode`.
    * An IRB `Interface` resource for every `TopoNode`.

You can execute the generator from the `tools` pod:

```{.shell .no-select}
./eda-topo-loader -f <path-to-json-topology>
```
