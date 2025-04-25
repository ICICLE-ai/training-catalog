---
tags:
  - CI4AI
  - Animal Ecology
---

# Explanation

## Architecture Overview

`ctcontroller` is made up of two main subcomponents:

1. The Provisioner:
	1. TACC provisioner
	2. Chameleon provisioner
2. The Application Manager:
	1. Camera Traps controller

The provisioner handles the provisioning and deprovisioning of hardware and currently supports two sites: Chameleon Cloud and bare metal nodes at TACC. It can be extended to other sites by defining a new subclass of `Provisioner`.

The Application Controller handles the setup, running, shutting down, and cleaning up of the application that was provisioned by the `Provisioner`. It currently only supports the Camera Traps application but can be extended to other applications by defining a new class.


## Control Variables
`ctcontroller` accepts the following environment variables to be defined at runtime:

| Variable | Description | Required |
| ---------| ----------- | -------- |
| `CT_CONTROLLER_NUM_NODES` | number of nodes that will be provisioned | Yes |
| `CT_CONTROLLER_TARGET_SITE` | site where the nodes will be provisioned | Yes |
| `CT_CONTROLLER_NODE_TYPE` | identifier of the type of node that will be provisioned | Yes |
| `CT_CONTROLLER_GPU` | boolean which tells the provisioner if the node needs to have a GPU and the Application Controller needs to run the application on the GPU | Yes |
| `CT_CONTROLLER_CONFIG_PATH` | path to a config file | Yes |
| `CT_CONTROLLER_MODEL` | model used by the application | No |
| `CT_CONTROLLER_INPUT` | input images into the application | No |
| `CT_CONTROLLER_SSH_KEY` | path to the ssh key | No |
| `CT_CONTROLLER_KEY_NAME` | name of the ssh key (needed for OpenStack/Chameleon) | No |
| `CT_CONTROLLER_CT_VERSION` | version of the application to be run | No |
| `CT_CONTROLLER_TARGET_USER` | username to be used on target system | No |
| `CT_CONTROLLER_OUTPUT_DIR` | path to output directory | No |
| `CT_CONTROLLER_JOB_ID` | unique job ID to be used for provisioning hardware | No |
| `CT_CONTROLLER_ADVANCED_APP_VARS` | variables to be passed to application controller | No |

## Configuration File

The path to the configuration file is specified through the environment variable `CT_CONTROLLER_CONFIG_PATH`. `ctcontroller` expects this file to be a YAML file. [sample_config.yml](sample_config.yml) is a sample config file. Configuration files can be used to specify target host nodes to be provisioned, service account credentials, and authorized users.