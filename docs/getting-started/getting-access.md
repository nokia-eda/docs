# Getting access to EDA

The EDA release is distributed via a set of git repositories hosted on the TODO. The entrypoint for an installation is in the [demo][demo-repo] repository.

/// details | Known issues and limitations of the currentnt release
    type: warning

<h4>Limitations</h4>

- TODO: use with the hw.
- The RAD (UI designer) is not provided. Watch this space!
- KinD cluster installation were tested and validated for this quickstart guide. You may still easily install EDA in a non-KinD environments, [here is how](../user-guide/install-advanced.md#eda-in-a-non-kind-cluster).

<h4>Known issues</h4>

- You may see one or more restarts of the keycloak and cert manager CSI driver pods during installation, this does not impact the install.
- Using KinD on Ubuntu 23+ prevents SR Linux simulator pods from running. This issue will be addressed on the SR Linux side in the near future.
///

## Clone the demo repository

The [`demo` repository][demo-repo] contains a [`Makefile`][makefile] to assist with deployment. You will need `git`[^1] to clone it:

```shell
git clone TODO
```

Change into the `demo` directory, as remaining steps will be completed from here.

```shell
cd demo
```

If you're good to here, you're mere minutes away from automation greatness.

[:octicons-arrow-right-24: Install!](install.md)

[demo-repo]: TODO
[makefile]: TODO

[^1]: Many distributions come with `git` preinstalled, but if not you should install it via your package manager.  
    For instance with `apt`-enabled systems:

    ```shell
    sudo apt install -y git
    ```
