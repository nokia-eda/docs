---
title: PlatformCertificateAudit
crd_path: docs/apps/certchecker.eda.nokia.com/crds/certchecker.eda.nokia.com_platformcertificateaudits.yaml
---

# PlatformCertificateAudit

A **PlatformCertificateAudit** resource triggers a TLS certificate audit against
**EDA platform pods** in the EDA base namespace. The CR must be placed in the
EDA base namespace (`eda-system`); CRs in other namespaces are permanently
pending (the flow engine silently ignores them).

The workflow discovers pods labeled `eda.nokia.com/cert-check-port` and
`eda.nokia.com/app` in the EDA base namespace, dials **cert-checker** for each
distinct app label value, streams results into `status.targetResults`, and sets
`status.rpcError` for infrastructure-level failures.

## Dependencies

- **cert-checker** must be reachable in-cluster.
- The CR must be placed in the **EDA base namespace** (`eda-system`).

## Spec

The spec is intentionally empty (`spec: {}`). Target selection always audits all
discoverable EDA apps in the EDA base namespace — one result per distinct
`eda.nokia.com/app` label value (not per pod replica).

## Status

| Field | Description |
|-------|-------------|
| `targetResults` | One entry per audited EDA app. Each entry includes `podName` (`namespace/pod`). |
| `rpcError` | Set when the workflow fails at the infrastructure level. |
| `observedGeneration` | Spec generation last fully processed. |

## Referenced resources

None — pod discovery is performed directly in the EDA base namespace.

## Example

{{ include_snippet("platformcertificateaudit") }}

## CRD

{{ crd_viewer(app_group, "v1alpha1", "PlatformCertificateAudit") }}
