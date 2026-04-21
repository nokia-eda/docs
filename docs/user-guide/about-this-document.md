# About this document

The Event Driven Automation \(EDA\) **User Guide** describes the system's core graphical user interface \(GUI\) and its use to configure and manage resources. It provides some information about EDA's purpose, a brief summary of its architectural components and central concepts, and includes administration concepts and procedures for maintaining EDA and the network elements it can manage.

Many of the capabilities of EDA are provided by individual applications that can be installed, updated, or uninstalled independently of the core EDA software. For details about those capabilities, see the documentation for individual applications.

This document is intended for network technicians, administrators, operators, service providers, and others who use EDA.

**Note:** This manual covers the current release and may also contain some content to be released in later maintenance loads. See the **EDA Release Notes**for information about features supported in each load.

## Precautionary and information messages<span id="precautionary-messages"></span>

The following are information symbols used in the documentation.

DANGER

Danger warns that the described activity or situation may result in serious personal injury or death. An electric shock hazard could exist. Before you begin work on this equipment, be aware of hazards involving electrical circuitry, be familiar with networking environments, and implement accident prevention procedures.

**Warning:** Warning indicates that the described activity or situation may, or will, cause equipment damage, serious performance problems, or loss of data.

CAUTION:

Caution indicates that the described activity or situation may reduce your component or system performance.

**Note:** Note provides additional operational information.

**Tip:** Tip provides suggestions for use or best practices.

## <span id="whats-new"></span>What's new

This section lists the changes that were made in this release.

|Feature|Location|
|-------|--------|
|**GUI basics**|
|You can now view resource related targets.|LINK|
|You can now pause UI streaming using the Live/pause selector.|LINK|
|Multi-row actions are now supported for deleted resources.|LINK|
|The Space key is now available for row selection.|LINK|
|You can now use the split view panel to switch between YAML and JSON views.|LINK|
|Alarm counters are now displayed in resource data grids.|LINK|
|Deviation counters are now displayed in resource data grids.|LINK|
|**Dashboard Designer**||User-created dashboards can now be shared.|LINK|
|**Namespaces**||Enhancements were made for the consistent handling of base namespaces.|LINK|
|**Resources**||The UI now displays resource topologies.|LINK|
|**Workflows**||You can now stream logs from workflow executions using the `edactl` command.|LINK|
|Workflows now support bulk selection of resources.|LINK|
|You can now download workflow artifacts for some workflows.|LINK|
|The system now supports duplicating a workflow action.|LINK|
|**Alarms**|
|Alarms lists are now available for Last Acknowledged By, Last Suppressed By, and Targets Affected.|LINK|
|Alarm quick filters are now available.|LINK|
|You can now navigate from the Information panel JS Paths to Query Builder.|LINK|
|**EDA Query Language**|
|The regex comparison operator \(~\) is now supported with the Where clause.|LINK|
|Support is now available for "is set" and "is not set" with the Where clause.|LINK|
|The concat\(\) function is now supported.|LINK|
|**Topology**||You can now toggle between the horizontal and vertical layout.|LINK|
|**EDA applications**||In the UI, the EDA Store page now includes sorting capabilities.|LINK|
|App settings are now shown in the Summary page during installation.|LINK|
|**Security**||The User page now displays user log in information, including last successful login and number of failed logins since the last successful login.|LINK|
|Removed a note indicating that imported federated users must be deleted explicitly when a federation is deleted|LINK|
|Enhancements have been made for inferring table rules from resource rules.|LINK|
|**Administration**||You can now reset a user's storage.|LINK|
