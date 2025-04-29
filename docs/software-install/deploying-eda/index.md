# Deploying EDA

These are the major steps for installing the EDA deployment. This applies to both Air-gapped installations and Internet based installations. Some steps will differ depending on the type of install, this will be clearly called out highlighting both options.

/// html | div.steps

1. [Preparing the EDAADM configuration file](setting-up-the-eda-virtual-machine-nodes.md#preparing-the-edaadm-configuration-file)  
    This task describes the details of the EDAADM configuration file and how to set it up.

2. [Generating the Talos machine configurations](setting-up-the-eda-virtual-machine-nodes.md#generating-the-talos-machine-configurations)  
    Using the EDA ADM tool and the configuration file, this task generates specific Talos machine configuration files for each Talos VM.

3. [Deploying the Talos virtual machines](setting-up-the-eda-virtual-machine-nodes.md#deploying-the-talos-virtual-machines)  
    This task describes how to use the Talos base image and machine configuration files to deploy the Talos VMs in your KVM or VMware vSphere environment.

4. [Bootstrap the Talos Kubernetes cluster](bootstrap-the-talos-kubernetes-cluster.md)  
    This task bootstraps the Talos Kubernetes environment using the VMs you have created.

5. [Installing the EDA application](installing-the-eda-application.md)  
    Using the EDA Installation playground, this step installs EDA on the Kubernetes environment in the EDA nodes.

///
