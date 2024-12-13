---
date: 2024-12-11
tags:
  - installation
authors:
  - rdodin
links:
  - Customize Install: user-guide/installation/customize-install.md
  - getting-started/try-eda.md
---

# Try EDA Like a Pro

Our tiny but mighty `make try-eda` command carries out the entire [EDA Playground](../../../getting-started/try-eda.md) installation. It installs a Kubernetes cluster, deploys the EDA core apps, and creates the necessary playground components along with a simulated network topology.  
Automation greatness, one click away. Just like we love it.

But as you build up your EDA experience, you may find yourself eager to step off the beaten path and start customizing your installation experience to your needs. In this blog post we share some new additions made to the Playground installation to make your Try EDA experience more enjoyable.

<!-- more -->

## Preferences file

Most likely you started your EDA journey by following our [quickstart](../../../getting-started/try-eda.md) guide and deployed your playground environment like this:

```shell
export EXT_DOMAIN_NAME=${DNS-name-or-IP} \
make try-eda
```

Yes, this is all you need to get the ball rolling, but providing the variable values inline is not always convenient. Often you want to store the values in a configuration file.

EDA's Playground config is powered by the make [preferences file](../../../user-guide/installation/customize-install.md) and we ship the instance of it - [`prefs.mk`][prefs-file] - within the [playground repo][pg-repo] itself.

[prefs-file]: https://github.com/nokia-eda/playground/blob/main/prefs.mk
[pg-repo]: https://github.com/nokia-eda/playground

The preferences file contains a selected set of the "most wanted" variables that you would want to tune for your playground installation. Things like the address you use to access the UI, the proxy settings, and kind cluster name.

You can of course edit the provided `prefs.mk` file, but what I like to do is to create a new file within the `./private` directory where I can store my values without changing the original file. There are a few reasons for this:

1. Keep the git repo clean, as the files in the `private` directory are not tracked by git.
2. Doing `git pull` won't overwrite the changes I made to a copy of the `prefs.mk` file.
3. I can create multiple preferences files for different installation scenarios.

If you opt in using a custom preferences file you would need to set the `PLAYGROUND_PREFS_FILE` environment variable to point to the file you want to use.

```shell title="Using a custom preferences file"
export PLAYGROUND_PREFS_FILE="private/kind-prefs.mk" #(1)!
make try-eda
```

1. Both absolute and relative paths are supported.

/// details | Spice it up with direnv
    type: subtle-note
A neat trick is to use [direnv](https://direnv.net/) tool and create an `.envrc` file in your working directory that would set the `PLAYGROUND_PREFS_FILE` variable to point to the file you want to use.

```shell title="<code>.envrc</code>"
export PLAYGROUND_PREFS_FILE="private/kind-prefs.mk"
```

///

## KPT Setters File

Alright, you noticed that the make preferences file contain only a handful of variables. But what if you want to customize the installation further?

For example, you might want to use EDA with a virtual topology built with Containerlab.  
To do that, you have to disable the EDA's "digital twin" feature by setting the `simulate = false` in the Engine Config resource. But this option is not exposed in the preferences file. What to do?

EDA uses the [kpt](https://kpt.dev/) to deploy and manage the configuration of its components. When browsing the [nokia-eda/kpt][kpt-repo] repository you may notice the `kpt-set` comments in various kubernetes manifests:

```yaml title="snippet from <code>eda-kpt-base/engine-config/engineconfig.yaml</code>"
apiVersion: core.eda.nokia.com/v1
kind: EngineConfig
metadata:
  name: engine-config # kpt-set: ${CLUSTER_MEMBER_NAME}
spec:
  # ...
  llm:
    apiKey: "" # kpt-set: ${LLM_API_KEY}
    model: gpt-4o # kpt-set: ${LLM_MODEL}
  simulate: true # kpt-set: ${SIMULATE}
```

[kpt-repo]: https://github.com/nokia-eda/kpt

These `kpt-set` comments are markers for the kpt tool that these values can set by Kpt using the `${VARIABLE_NAME}` syntax. How would you set the values of these variables you ask? Using the [Kpt setters file](../../../user-guide/installation/customize-install.md#kpt-setters-file).

/// admonition | Kpt Setters Reference
    type: subtle-note
We maintain [the reference](../../../user-guide/installation/customize-install.md#kpt-setters-reference) of all available setters in our docs.
///

The setters file allow you to specify the values for the setters that will be used when you install EDA Playground. For example, to disable the EDA network simulation, you would create a yaml file like this:

```yaml title="<code>my-setters.yml</code>"
apiVersion: v1
kind: ConfigMap #(1)!
metadata:
  name: my-setters
data:
  SIMULATE: false 
  LLM_API_KEY: my-openai-key-data #(2)!
  # your other setters here
```

1. As you can see, the setters file is a ConfigMap resource, but it is not applied to your cluster, it is only used by the kpt tool to read the values from it.
2. The setter's key must match the name of the setter variable in the manifest file. That is why the key is `LLM_API_KEY` and not `apiKey`.

Now that you have your setters file with the necessary values, you should set the path to it in the preferences file:

```makefile
KPT_SETTERS_FILE := private/my-setters.yml
```

And that's it! The kpt will read the values from the setters file and apply them to the manifests when you run the `make try-eda` command.

## Kind Config

The default EDA Playground installation deploys the platform on a KinD cluster. And by default we deploy a default KinD cluster using a barebones cluster configuration.

This works great for the most installation scenarios, but sometimes you need to customize the kind cluster configuration. For example, you may need to add extra bits of configuration to play with Ingress resources and expose additional ports for your cluster.

We allow you to use your own kind configuration file by setting the `KIND_CONFIG_FILE` variable in the preferences file pointing to the desired config file. Here is an example of a custom kind config file that I use to setup ingress nginx with kind:

///tab | kind config

```yaml title="<code>private/kind-ingress-config.yml</code>"
---
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  ipFamily: dual
  apiServerAddress: "127.0.0.1"
nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
```

///
/// tab | preferences file

```makefile
KIND_CONFIG_FILE := private/kind-ingress-config.yml
```

///

## LLM API Key

The Natural Language Query feature requires an OpenAI API key to be set in the EDA's Engine Config resource. You can provide the key directly in the preferences file using the `LLM_API_KEY` variable, but providing a "secret" in a file body is not the most secure way to do it.

Instead, you can set the environment variable under the same key `LLM_API_KEY` in your `.profile`, `.zshenv`, `.bashrc`, `.zshrc`, or any other file that your shell reads on startup. Make tool will read the env variable under this key by default, so you may leave the variable unset in the preferences file.

## Kind API Server Address

When we deploy a Kind cluster for EDA Playground, the k8s API server address is kept at its default value of `127.0.0.1`. The localhost nature of the address results in the k8s API server being inaccessible from outside the machine you run the cluster on.

We noticed that many users would like to spin up playground on a remote servers and access the k8s API server via a network. To support this use case, we added the `KIND_API_SERVER_ADDRESS` variable to the preferences file which allows you to set the non localhost IP address for the k8s API server. This effectively allows you to access the k8s API server from outside the machine you run the cluster on.

## More Permanent UI Access

And the last tip for today concerns the UI. Originally, you access the UI by forwarding the port of the `eda-api` service to your local machine using the `make start-ui-port-forward` command. This works great, but a slight inconvenience is that you need to keep your session open to keep the port forwarding alive.

In pursue of a more permanent port forwarding solution, we added the `enable-ui-port-forward-service` make target that will create a `eda-ui.service` systemd service that uses the same port forwarding logic, but will run in the background. Run this target once, and then you can access the UI anytime you want.

When your redeploy the cluster without changing the `EXT_HTTPS_PORT` you may just restart the service to get it up and running again.
