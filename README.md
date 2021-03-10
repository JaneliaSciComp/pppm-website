# PPPM Website[![Picture](https://raw.github.com/janelia-flyem/janelia-flyem.github.com/master/images/HHMI_Janelia_Color_Alternate_180x40.png)](http://www.janelia.org)

[![GitHub last commit](https://img.shields.io/github/last-commit/JaneliaSciComp/pppm-website.svg)](https://github.com/JaneliaSciComp/pppm-website)
[![GitHub commit merge status](https://img.shields.io/github/commit-status/badges/shields/master/5d4ab86b1b5ddfb3c4a70a70bd19932c52603b8c.svg)](https://github.com/JaneliaSciComp/pppm-website)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Requirements Status](https://requires.io/github/janelia-flyem/assignment-manager/requirements.svg?branch=master)](https://requires.io/github/JaneliaSciComp/pppm-website/api/requirements/?branch=master)

## Summary
This repository contains the PatchPerPix website. 

## Configuration

This system depends on the [Centralized Config](https://github.com/JaneliaSciComp/Centralized_Config) system, and
will use the following configurations:
- rest_services
- servers

The location of the configuration system is in the config.cfg file as CONFIG.

To rebuild the docker container:
```
docker build --tag registry.int.janelia.org/janeliascicomp/pppm-website.
docker push registry.int.janelia.org/janeliascicomp/pppm-website
```

## Deployment

After installing on the production server, set up the environment for Docker.
Rename env_template to .env, and change any values enclosed in angle brackets.

To create a new database instance:
```
sudo mkdir /data/mysql/
sudo chown mysql:mysqldba /data/mysql/assignment
docker-compose -f docker-compose-prod.yml up db
```

Take the following steps to start the system:
```
cd /opt/flask/assignment-responder
docker-compose -f docker-compose-prod.yml down
docker image ls
docker image rm <image id from above for assignment-manager>
docker volume rm assignment-manager_static_volume
docker pull registry.int.janelia.org/flyem/assignment-manager
docker-compose -f docker-compose-prod.yml up -d
```

## Development
1. Modify api/config.cfg to change MYSQL_DATABASE_HOST as needed
2. docker-compose up -d

## Author Information
Written by Rob Svirskas (<svirskasr@janelia.hhmi.org>)

[Scientific Computing](http://www.janelia.org/research-resources/computing-resources)  
