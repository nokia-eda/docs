---
title: NodeCertificateAudit
crd_path: docs/apps/certchecker.eda.nokia.com/crds/certchecker.eda.nokia.com_nodecertificateaudits.yaml
---

# NodeCertificateAudit

A **NodeCertificateAudit** resource triggers a TLS certificate audit against one
or more **TopoNodes** in the same Kubernetes namespace as the CR. The workflow
dials **cert-checker** (`AuditCertStream` with mTLS), streams per-node results
into `status.targetResults`, and sets `status.rpcError` for infrastructure-level
failures.

## Dependencies

- **cert-checker** must be reachable in-cluster (ClusterIP service and TLS trust
  material for the workflow pod).
- TopoNodes named in `spec.nodes` or matched by `spec.nodeSelectors` must exist
  in the CR's namespace.

## Spec

| Field | Type | Description |
|-------|------|-------------|
| `nodes` | `[]string` | Explicit TopoNode names to audit. |
| `nodeSelectors` | `[]string` | Kubernetes label selector strings; matched nodes are added to the target list and deduplicated with `nodes`. |

An empty `spec: {}` (both fields omitted) audits all TopoNodes in the namespace.

## Status

| Field | Description |
|-------|-------------|
| `targetResults` | One entry per audited node. |
| `rpcError` | Set when the workflow fails at the infrastructure level. |
| `observedGeneration` | Spec generation last fully processed. |

## Referenced resources

- `core.eda.nokia.com/TopoNode` — resolved in the CR namespace.

## Example

{{ include_snippet("nodecertificateaudit") }}

## CRD

{{ crd_viewer(app_group, "v1alpha1", "NodeCertificateAudit") }}
