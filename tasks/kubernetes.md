# Create helm chart for the project

## Minimum must have
- Definition for the front-end back-end and database deployments
- possibility to modify docker images (tags, repositories)
- possibility to manage number of replicas for each deployment

## Nice to see and have
- declaration for readiness and livness probes
- making db deployment optional
- allowing to read configuration variables from configmaps / secrets
- Possibility to setup ingress for remote access on the cluster
