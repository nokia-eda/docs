# Kafka Importer Application

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [Nokia/catalog/kafka-importer ][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

Kafka Importer is an EDA application that imports data from Kafka brokers into **State-DB**.

Use **Consumer** for tenant-scoped imports (import paths are scoped to the CR's namespace). Use **Cluster Consumer** for operator-managed imports that may write to any user namespace in State-DB (full JsPath control). Cluster Consumer is reconciled only in the controller pod namespace and is not a Kubernetes cluster-scoped resource.

The application provides the following components:

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* Consumer

</div>
<div markdown>

* Cluster Consumer

</div>
</div>
///
