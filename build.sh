#!/bin/sh

if [ -z "$1" ]
then 
  TAG="latest"
else
  TAG=$1
fi 

echo "Building $TAG"

docker build --no-cache -t metadonors/odoo:$TAG .
docker push metadonors/odoo:$TAG 
