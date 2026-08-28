---
resource_name: RotateCertificate
resource_name_plural: rotatecertificates
resource_name_plural_title: Rotate Certificates
resource_name_acronym: RC
crd_path: docs/apps/bootstrap.eda.nokia.com/crds/bootstrap.eda.nokia.com_rotatecertificates.yaml
# 'auto-crd' will automatically select between the normal resource and workflow icon
icon: auto-crd
---

# Rotate Certificate

-{{% import 'icons.html' as icons %}}-

-{{ category(resource_name_plural) }}- → -{{ icons.circle(letter=resource_name_acronym, text=resource_name_plural_title) }}-

To connect securely to the nodes, EDA installs a TLS certificate on each node during onboarding. Depending on the operating system, that certificate is installed through gNOI (gRPC Network Operations Interface) or gNSI (gRPC Network Security Interface). The certificate must be rotated periodically, for example when the signing CA used by EDA is rotated.

Periodic rotation of the TLS certificate is done automatically, without operator intervention. To rotate earlier, run the `RotateCertificate` workflow.

## Certificate validation

After rotation, the new certificate is validated against EDA's node trust bundle. This check can be disabled with `skipCertificateValidation`.

## Dependencies

### `TopoNode`

Nodes can be selected explicitly by name, or through a label selector.

## Referenced resources

The `RotateCertificate` does not reference any other EDA resources.

## Examples

/// tab | YAML

```yaml
-{{ include_snippet(resource_name) }}-
```

///

/// tab | `kubectl`

```bash
cat << 'EOF' | kubectl apply -f -
-{{ include_snippet(resource_name) }}-
EOF
```

///

## Custom Resource Definition

To browse the Custom Resource Definition go to [crd.eda.dev](https://crd.eda.dev/-{{ resource_name_plural }}-.-{{ app_group }}-/-{{ app_api_version }}-).

-{{ crd_viewer(crd_path, collapsed=False) }}-
