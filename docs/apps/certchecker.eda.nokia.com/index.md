# CertChecker

-{{% import 'icons.html' as icons %}}-

| <nbsp> {: .hide-th } |                                         |
| -------------------- |-----------------------------------------|
| **Group/Version**    | -{{ app_group }}-/-{{ app_api_version }}-   |
| **Supported OS**     | -{{ supported_os_versions() }}-  |
| **Catalog**          | [nokia/catalog/certchecker][manifest] |
| **Source Code**      | <small>coming soon</small>              |

[//]: # (Note: you should fill in the hyperlink to your published manifest in your public catalog)
[manifest]: https://docs.eda.dev/

CertChecker audits TLS certificates across EDA-managed topology nodes and EDA platform components. Two workflow resources are available:

- **NodeCertificateAudit** — audit TopoNode certificates in a user namespace.
- **PlatformCertificateAudit** — audit EDA platform pod certificates (must be placed in the EDA base namespace).

/// tab | Resources

<div class="grid" markdown>
<div markdown>

* [NodeCertificateAudit](resources/nodecertificateaudit.md)
* [PlatformCertificateAudit](resources/platformcertificateaudit.md)

</div>
</div>
///

/// tab | Workflows
<div class="grid" markdown>
<div markdown>

* certchecker-nodecertificateaudit-gvk
* certchecker-platformcertificateaudit-gvk

</div>
</div>
///
