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

The configuration file consists of three parts: 
1. A description of the systems that can be accessed. Each system is given a unique identifier and contains the following attributes:
   1. `Name`, which expects a string corresponding to an identifier to for the ssh key for the system
   2. `Path`, which contains the path to the ssh key for the system
   3. `Hosts`, which is a dictionary whose keys are a hardware type and the values are lists of valid IP addresses for that host and the username on those hosts. For instance, `{'hardware_type': [{'IP': ip_address1, 'Username': username1}, {'IP': ip_address2, 'Username: username2}]}` would be a valid value for the `Hosts` attribute.
2. A list of authenticated users. The key is `Users` and authorized users must be a list
3. Advanced settings. The key is `Settings` and available settings are:
   1. `AuthenticateUsers=True|False`.