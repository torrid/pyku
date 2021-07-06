#!/bin/bash
# 

eval $(minikube docker-env) 

docker image rm load-and-stress
docker build -t load-and-stress .
kubectl replace --force -f deployment.yaml

