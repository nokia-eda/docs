---
date: 2026-04-30
authors:
    - zenodhaene
---

# Bringing style to EDA 26.4

Today marks the [release date of EDA 26.4.1](eda-26.4.md), which brings a huge number of new features for you to play around with!

In this blog post, we would like to address the syntax changes that this version brings to most apps pre-packaged in EDA. As you may have noticed, some of your old automation scripts will no longer work with this release.

This is a necessary change that allows us, once and for all, to introduce a common resource syntax across all resources that come with EDA: by introducing syntax rules, we improve uniformity, clarity, and accuracy, which ultimately helps us deliver a quality product.

<!-- more -->

To minimize impact, we provide a feature to automatically convert your old resources to the new version: you can read all about it [below](#upgrade-resources-using-edactl). Of course, any resources that are part of your EDA deployment will automatically be converted to the new version during the upgrade procedure.

We don't enjoy breaking your automation scripts, nor do we plan on making this a habit of ours. Instead, we will follow our own rules for all the new features we still plan on bringing you in the coming years.

An example of a resource that was changed is the [`Interface`](../../../apps/interfaces.eda.nokia.com/docs/resources/interface.md). Take a look at the differences between versions `v1alpha1` and `v1` of an `Interface` CR:

/// tab | Interface version `v1alpha1`

An `Interface` resource in version `v1alpha1`:

```yaml hl_lines="1 10 12 14"
apiVersion: interfaces.eda.nokia.com/v1alpha1
kind: Interface
metadata:
  name: leaf-1-ethernet-1-1
  namespace: eda
  labels:
    app: red
    lldp: enable
spec:
  type: interface
  mtu: 2500
  encapType: dot1q
  ethernet:
    reloadDelayTimer: 5
  members:
    - node: leaf-1
      interface: ethernet-1-1
```

///

/// tab | Interface version `v1`

An `Interface` resource in version `v1`:

```yaml hl_lines="1 10 12 14"
apiVersion: interfaces.eda.nokia.com/v1
kind: Interface
metadata:
  name: leaf-1-ethernet-1-1
  namespace: eda
  labels:
    app: red
    lldp: enable
spec:
  type: Interface
  mtu: 2500
  encapType: Dot1q
  ethernet:
    reloadDelayTimerSeconds: 5
  members:
    - node: leaf-1
      interface: ethernet-1-1
```

///

## What changed?

* The `type` of an `Interface` is an enum, and its permitted values have been capitalized
* The `encapType` has undergone a similar change, replacing the old `dot1q` string value with `Dot1q`
* The `reloadDelayTimer` property has been renamed to `reloadDelayTimerSeconds`, which makes it clear how the value of this property should be interpreted

We drew on the [Kubernetes resource styling principles](https://github.com/kubernetes/community/blob/main/contributors/devel/sig-architecture/api-conventions.md) (with very few exceptions), and will continue to do so for any new features.

## Upgrade resources using edactl

[Edactl](../../../user-guide/command-line-tools.md#edactl) is the CLI tool to interact with EDA, and provides a helpful command to convert your old resources to their new versions: `edactl platform upgrade convert`

```bash
❯ edactl platform upgrade convert --help
Run the conversion script on the provided resources to convert them from their current version to the running version

Usage:
  edactl platform upgrade convert [flags]

Flags:
  -f, --filename strings   input file(s) containing resources to convert
  -h, --help               help for convert
      --overwrite          overwrite existing output files
  -R, --recursive          process directories recursively
  -w, --write string       directory to write converted output files
```

Example run, using the `v1alpha1` version of the `Interface` resource:

```bash
❯ edactl platform upgrade convert -f interface_v1alpha1.yaml
Processing: interface_v1alpha1.yaml
  - GVK: interfaces.eda.nokia.com/v1alpha1, Kind=Interface; Namespace: eda; Name: leaf-1-ethernet-1-1
apiVersion: interfaces.eda.nokia.com/v1
kind: Interface
metadata:
  labels:
    app: red
    lldp: enable
  name: leaf-1-ethernet-1-1
  namespace: eda
spec:
  enabled: true
  encapType: Dot1q
  ethernet:
    reloadDelayTimerSeconds: 5
  lldp: true
  members:
  - enabled: true
    interface: ethernet-1-1
    lacpPortPriority: 32768
    node: leaf-1
  mtu: 2500
  type: Interface
```
