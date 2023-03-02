#!/bin/sh

sudo docker-compose down
sudo docker image ls | grep pppm | awk '{print $3}' | xargs sudo docker image rm
sudo docker volume rm pppm-website_static_volume
sudo docker-compose -f docker-compose-prod.yml up -d
