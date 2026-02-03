---
search:
  boost: 4
---

# Try EDA in Codespaces

Even though all it takes to [Try EDA on your own compute](try-eda.md) is a couple of commands, nothing beats an environment that one can run without fronting the hardware, anytime, with a single click and {==for free==}.

EDA in Codespaces is exactly that - the real "Try EDA" installation in a free[^1], cloud-based VM, available to everyone with a single-click spin up. All you need is a GitHub account and a web browser.

Here is how it works. When you see the "Run in Codespaces" button somewhere in our docs or in one of the repositories it invites you to spin up the EDA environment in the Github Codespaces.

<div align=center markdown>
<a href="https://github.com/codespaces/new?repo=1129099670&ref=main">
<img src="https://gitlab.com/-/project/7617705/uploads/3f69f403e1371b3b578ee930df8930e8/codespaces-btn-4vcpu-export.svg"/></a>

**Run EDA in Codespaces for free**.  
<small>Machine type: 4 vCPU · 16 GB RAM</small>
</div>

Clicking on a button will open up a GitHub web page asking you to confirm the creation of a Codespaces environment. Once you confirm, a VS Code window will open in your browser, and the EDA installation will kick off. Depending on the performance of the Codespaces VM, it may take anywhere between 10 to 20 minutes to have the full EDA environment up and running.

When the installation is complete, you will see the EDA welcome message in the terminal window, and the EDA GUI URL will be printed out for you to open in a separate browser tab. Now everything is ready, and you can start using EDA in your browser.

-{{video(url="https://gitlab.com/-/project/7617705/uploads/5a1460fb3e94efc4f557b632ad5c0ab3/eda-cs-demo.mp4", title="EDA in Codespaces demo")}}-

In the VS Code window in your browser you have the full access to the terminal where we preinstalled some EDA tools like `edactl`, `kubectl`, `k9s` and you can install other tools as you see fit. The Codespaces environment is a Debian Linux VM in the cloud, so you can use it as you would use any other Linux machine.

## Is It Free?

The best part about the [Github Codespaces][codespaces-doc] is that it offers a generous free tier - **120 cpu-hours for free each month**[^2] to all GitHub users. The "EDA in Codespaces" uses the 4vcpu/16GB RAM machine type, which means that you can run the EDA environment for 30 hours each month. For free.

The cpu-hours counter is reset at the beginning of each calendar month, so you can use the free plan every month.

> By default each GitHub user has a **$0** spending limit, and no payment method is required to start using Codespaces. You won't be charged unless you explicitly add a payment method and increase your spending limit.

[codespaces-doc]: https://github.com/features/codespaces

<div class="grid cards" markdown>

* :fontawesome-solid-route:{ .middle } **Where to next?**

    ---

    Is your codespaces environment up and running? Great! Time to learn some EDA basics.

    [:octicons-arrow-right-24: **Tour of EDA**](../tour-of-eda/index.md)

* :fontawesome-solid-question:{ .middle } **Learn mode about Codespaces**

    ---

    Want to learn how to control the Codespaces environment, manage its lifecycle, check the usage and customize it? We got you covered.

    [:octicons-arrow-right-24: **EDA in Codespaces docs**](../software-install/non-production/codespaces.md)

</div>

[^1]: Limited by the free tier offered by GitHub Codespaces.
[^2]: The terms of the free plan may be subject to change, consult with the [official documentation](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#monthly-included-storage-and-core-hours-for-personal-accounts) for the current terms and conditions.
