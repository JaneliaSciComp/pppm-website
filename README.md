# PPPM Website[![Picture](https://raw.github.com/janelia-flyem/janelia-flyem.github.com/master/images/HHMI_Janelia_Color_Alternate_180x40.png)](http://www.janelia.org)

[![GitHub last commit](https://img.shields.io/github/last-commit/JaneliaSciComp/pppm-website.svg)](https://github.com/JaneliaSciComp/pppm-website)
[![GitHub commit merge status](https://img.shields.io/github/commit-status/badges/shields/master/5d4ab86b1b5ddfb3c4a70a70bd19932c52603b8c.svg)](https://github.com/JaneliaSciComp/pppm-website)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)


## Summary
This repository contains the PatchPerPix website. 

## Configuration

This system depends on the [Centralized Config](https://github.com/JaneliaSciComp/Centralized_Config) system, and
will use the following configurations:
- rest_services
- servers

The location of the configuration system is in the config.cfg file as CONFIG.
If the config service is not available, provide a list of body mappings in api/pppm_bodies.json.

## Deployment

Clone the repo to the deployment system:
```
git clone https://github.com/JaneliaSciComp/pppm-website.git
```

To start the app:
```
cd /opt/flask/pppm-website
sh restart_production.sh
```

## Development

To run without docker:
```
cd api
python3 ppp_responder.py
```
If you don't have all of the required modules, it's recommended that you create a virtual environment and install them from requirements.txt.

## Author Information
Written by Rob Svirskas (<svirskasr@janelia.hhmi.org>)

[Scientific Computing](http://www.janelia.org/research-resources/computing-resources)  
