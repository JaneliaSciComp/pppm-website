#!/bin/sh

sudo /usr/local/bin/docker-compose down
sudo docker image ls | grep registry.int.janelia.org | awk '{print $3}' | xargs docker image rm
sudo docker volume rm pppm-website_static_volume
sudo docker pull registry.int.janelia.org/janeliascicomp/pppm-website
sudo /usr/local/bin/docker-compose up -d
