#!/bin/sh

if [ -z "$1" ]
then 
  TAG="latest"
else
  TAG=$1
fi 

echo "Building $TAG"

docker build -t metadonors/odoo:$TAG odoo/
docker push metadonors/odoo:$TAG 
