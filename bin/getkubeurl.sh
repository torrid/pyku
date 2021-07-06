#!/bin/bash

eval $(minikube docker-env) 
ps x | grep -v grep | grep "minikube tunnel" >/dev/null 2>&1 || minikube tunnel > /dev/null 2>&1 & 

url=$(kubectl get svc|grep load-and-stress|grep 8080| sed -e 's#  *#\t#gi'| cut -f 4,5 | cut -f 1 -d:| sed -e 's#\t#:#')
echo "http://${url}/"

