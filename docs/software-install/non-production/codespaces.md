# EDA In Codespaces

Even though all it takes to [Try EDA on your own compute](../../getting-started/try-eda.md) is a couple of commands, nothing beats an environment that one can run without fronting the hardware, anytime, with a single click and {==for free==}.

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

## Control panel

Whenever you need to check what Codespaces environments you have running or created, you can do it in the [Codespaces panel][codespace-panel].

-{{image(url="https://gitlab.com/-/project/7617705/uploads/3f9c945ba979cd6052dc56364d2aefe5/CleanShot_2026-01-20_at_11.37.35.png", padding=20)}}-

The panel shows you all your existing Codespaces environments and their status. In the screenshot above there is one environment created from the `eda-labs/codespaces` repository, which is currently active (running).

Via the Control Panel users can manage their environments, including starting, stopping, and deleting them. For example, stopping an environment that is currently not in use will help save the cpu-hours quota. Users can start a stopped environment when they need it again.

> When the EDA environment in Codespaces is started from a previously stopped state, it will take around 5 minutes for the Kubernetes cluster and EDA applications to be fully operational.

-{{image(url="https://gitlab.com/-/project/7617705/uploads/c677d443225b21a7ed547ee23c0127e0/CleanShot_2026-01-20_at_11.37.42.png", padding=20, title="Environment actions")}}-

### Codespaces settings

Codespaces expose a set of user settings at [github.com/settings/codespaces](https://github.com/settings/codespaces) page. The following settings are worth mentioning:

//// define

Idle timeout and retention period

- Maybe the most important settings that you can configure in Codespaces. They allow you to control how long the environment will be running and when it will be deleted. Read more on this in [Billing](#billing) section

Secrets

- Secrets allow you to store sensitive information that will be available to your Codespaces environments. You can use them to store API keys, passwords, and other sensitive data that you don't want to expose in your code.

Setting Sync

- To make codespaces env feel like home, you can sync your settings across all your Codespaces environments. This includes themes, keybindings, and other settings that you have configured in your local VS Code instance.

Editor preference

- You can choose if you want to run the codespaces in a browser, in a local VS Code instance, or via a bridge to a JetBrains IDE.

////

### Billing

It is always a good idea to periodically check how much of the cpu-hours you've consumed and check the remaining quota. Your billing information is available in the [Billing settings][billing].

/// note
All users by default have a $0 spending limit[^2], which means that if you exceed the free tier limits, your environments will be stopped and you will **not** be charged. You can change this limit to a higher value if you want to be able to use Codespaces even after you exceed the free tier limits.
///

To avoid any surprises and lower your anxiety levels, GitHub Codespaces have two important settings that you configure at [github.com/settings/codespaces](https://github.com/settings/codespaces):

1. **[Idle timeout](https://docs.github.com/en/codespaces/setting-your-user-preferences/setting-your-timeout-period-for-github-codespaces)**  
    This setting allows you to "suspend" the running environment after a certain period of inactivity and defaults to 30 minutes. You can increase/decrease the timeout as you see fit. Consult with the docs to see what counts as activity and what doesn't.
2. **[Retention period](https://docs.github.com/en/codespaces/setting-your-user-preferences/configuring-automatic-deletion-of-your-codespaces)**  
    When you stopped the codespaces environment or it was suspended due to inactivity, it will be automatically deleted after a certain period of time. The default (and maximum) retention period is 30 days, but you can change it to a shorter period.  
    The stopped environment won't count against your cpu-hours quota, but it will still consume storage space, hence you might want to remove the stopped environments to free up the space.

/// admonition | Safe settings
    type: tip
To keep a tight control on the Codespaces free quota usage you can set the following in your [Codespaces Settings](https://github.com/settings/codespaces):

- Idle timeout to **15 minutes**
- Retention period to **1 day**

That way you can be sure that the environment is not running when you don't need it and it will be deleted after a day of inactivity saving up on the storage space.
///

[codespaces-doc]: https://github.com/features/codespaces
[billing]: https://github.com/settings/billing/usage?period=3&group=2&query=product%3Acodespaces
[codespace-panel]: https://github.com/codespaces

[^1]: Limited by the free tier offered by GitHub Codespaces.
[^2]: The terms of the free plan may be subject to change, consult with the [official documentation](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#monthly-included-storage-and-core-hours-for-personal-accounts) for the current terms and conditions.
