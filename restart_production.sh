#!/bin/sh

sudo docker-compose -f docker-compose-prod.yml down
sudo docker container ls -a | grep pppm-website_app | awk '{print $3}' | xargs sudo docker container rm
sudo docker image ls | grep pppm-website_app | awk '{print $3}' | xargs sudo docker image rm
sudo docker volume rm pppm-website_static_volume
sudo docker-compose -f docker-compose-prod.yml up -d
