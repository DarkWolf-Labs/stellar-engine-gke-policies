# stellar-engine-gke-policies

This repository provides configuration for the Google Kubernetes Engine (GKE) cluster set up through the Stellar Engine GKE blueprint(s).  Configured through Terraform, the GateKeeper system running on the cluster will periodically pull from this repo to manage configuration of the cluster.

## Contents

 - Constraints provided by Google at [Gke Policy Library](https://github.com/GoogleCloudPlatform/gke-policy-library/tree/main).
The constraints are in DRYRUN mode by default and do not hinder any workflows, but provide warnings to potential security risks.
 - Constraint Templates exported from the cluster with the template library deployed by Policy Controller.
 - Custom constraints and templates created to remediate violations found.
 - Scripts - helpful tools for interacting with the cluster.

## Custom Components

There are a number of different Kubernetes manafests within the custom folder.
 - Updated constraints or templates -
   These are copied from the policies/bundles/xxx folder and placed into a custom/bundles/xxx folder.
   The kusomization.yaml file in original folder is updated to skip deploying the file.
   A new kustomization.yaml file is created in the specific custom bundle folder to apply the new updated version.
 - New resources - 
   Additional folders are created in the custom folder to contain new resources (namespaces, daemonsets, etc.).
   
## Google GKE Dashboards

There are two pages in the Google Console [GKE page](https://console.cloud.google.com/kubernetes) that provide insight into the configuration and status of a cluster.

### Config Sync

[Config Sync](https://console.cloud.google.com/kubernetes/config_management) provides a dashboard view of the current configuration status of the configured clusters.  In the Packages tab, you can find a list of all resources applied to the cluster, as well if there are errors in the sync process.

### Policy Controller

[Policy Controller](https://console.cloud.google.com/kubernetes/policy_controller) provides a dashboard view of the policies applied to the cluster and any pass/fail results found.  In Violations tab, you can find details on count, affected resource types, and error messages.

## Scripts

The included scripts are provided as tools to export data from the cluster for constraint statuses, and template yaml.
The scripts should be run from the bastion vm with network access to the cluster.  Output output files can then be downloaded.