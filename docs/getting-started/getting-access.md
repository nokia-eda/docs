# Getting access to EDA

The EDA release is distributed via a set of git repositories hosted at [github.com/nokia-eda][gh-org], with the main entrypoint to installation in the [`playground` repository][playground-repo] which is currently private and requires a token for access. Contact your Nokia account representative, or reach out to us on the official [EDA Discord][eda-discord].

/// details | Known issues and limitations of the current release
    type: warning

- Using KinD on Ubuntu 23+ prevents SR Linux simulator pods from running. This issue will be addressed on the SR Linux side in the near future.
- For a complete set of known issues and changes in this release, refer to the [release notes][rn-24-8-1].
///

## Clone the playground repository

The [`playground` repository][playground-repo] contains a [`Makefile`][makefile] to assist with deployment. You will need `git`[^1] to clone it:

<!-- --8<-- [start:pull-playground] -->
```shell
export GH_RO_TOKEN=<token>
git clone https://${GH_RO_TOKEN}@github.com/nokia-eda/playground && \
cd playground
```
<!-- --8<-- [end:pull-playground] -->

If you got to here, you're mere minutes away from automation greatness.

[:octicons-arrow-right-24: Try EDA!](try-eda.md)

[gh-org]: https://github.com/nokia-eda
[playground-repo]: https://github.com/nokia-eda/playground
[makefile]: https://github.com/nokia-eda/playground/blob/main/Makefile
[rn-24-8-1]: https://documentation.nokia.com/aces/cgi-bin/dbaccessfilename.cgi/3HE209390001TQZZA_V1_Event%20Driven%20Automation%2024.8.1%20Release%20Notes.pdf
[eda-discord]: https://eda.dev/discord

[^1]: Many distributions come with `git` preinstalled, but if not you should install it via your package manager.  
    For instance with `apt`-enabled systems:

    ```shell
    sudo apt install -y git
    ```
