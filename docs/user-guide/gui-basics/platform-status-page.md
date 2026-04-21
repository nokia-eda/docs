# The Platform Status page

The second view available from the Home page of the EDA GUI is the Platform Status page.

-{{image(url="../graphics/sc0205.png", title="The Platform status page", shadow=true, padding=20)}}-

Clicking the **View** link from any dashlet opens the Alarms List.

Table: Elements of the Platform Status page

|Dashlet|Description|
|-------|-----------|
|EDA clusters|When configured for Geographic Redundancy, EDA maintains separate instances on independent clusters so that the backup cluster can take over if the primary fails. The primary and backup EDA clusters regularly synchronize so that the latest data is still being used after a switchover to the backup cluster. This dashlet indicates whether clusters are reachable, and whether the reachable clusters are correctly synchronized.|
|Git servers|Shows the reachability status of EDA's Git servers. These servers are used for persistent storage of resources, installed apps, and user settings.|
|App catalogs|An app catalog is a structured Git repository that contains all information about an app, including where to find the app image containers.|
|App registries|An app registry is an OCI-compliant container registry, and contains the actual app image containers.|
