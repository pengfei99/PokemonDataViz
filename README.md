# PokemonDataViz

In this project, we use plotly dash to show visualization of pokemon statistics which are stored inside a postgresql
server

## Application k8s deployment

The docker image does not contain the necessary env var to connect to a postgresql server. **So it won't work with a docker run.** 

This application is meant to run inside a k8s deployment. Before you apply the k8s deployment, you need to config serveral things
1. setup the db connection credentials in `secret.yaml`
2. setup the db server location (url, port, db_name, and table name) in `deployment.yaml`
3. setup the url of your app in `ingress.yaml`

After above config, you can run below command to deploy the application in the k8s cluster.
```shell
# If you have a kube client
kubectl apply -f k8s/.
```

## Data ingestion (etl) pipeline

As we mentioned before, this app read data from a database. If you don't know how to do etl, you can use the [etl pipeline](argo_workflow/pokemon_etl_data_pipeline.yaml) to populate your database server.

This pipeline requires argo workflow to run. So you need to install argo workflow on your k8s cluster.