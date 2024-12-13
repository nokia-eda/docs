# Resetting the Playground

If you want to start fresh, or just shut down your playground, you can do so with the following commands:

```shell
make teardown-cluster
```

This will remove the KinD cluster and all the resources created by the EDA Playground.

Then you can remove the existing `kpt` packages:

```shell
rm -rf eda-kpt
```

And you are ready to start over!
