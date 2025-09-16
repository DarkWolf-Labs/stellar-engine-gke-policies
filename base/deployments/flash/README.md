
## Flash Sample Deployment
This is a sample deployment of a FastApi app in a GKE using GitOps.

To create the CRDs for the Gateway and HTTPRoute, run
```
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v0.8.0/standard-install.yaml
```