# PokemonDataViz

In this project, we use dash to show visualization of pokemon statistics which are stored inside a postgresql

The docker image does not contain the necessary env var to connect to a postgresql server. It meant to run inside
a k8s deployment
```shell
# If you have a kube client
cd k8s
kubectl apply -f .
```