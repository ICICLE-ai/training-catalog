---
tags:
  - CI4AI
  - Animal-Ecology
---
# How-To Guide

## Installation

### From source

Download the release as source code and unzip it

```
wget https://github.com/ICICLE-ai/ct-controller/archive/refs/tags/${VER}.tar.gz
tar xf ${VER}.tar.gz
```
Then ensure that you run from the root of the ctcontroller repository

```
cd ct-controller-${VER}
```

or add the package to the `PYTHONPATH`

```
export PYTHONPATH:$PWD/ct-controller-${VER}/ctcontroller:$PYTHONPATH
```

### Pip

`ctcontroller` can also be installed via pip with:

```
pip install git+https://github.com/ICICLE-ai/ct-controller@${VER}
```


### Docker image

`ctcontroller` is also available [here](https://hub.docker.com/r/tapis/ctcontroller) as a docker image on Dockerhub. To pull down the latest version:

```
docker pull tapis/ctcontroller
```

## Running

### Simulation mode

Simulation mode is designed to be allow provisioning of a variety of remote hardware from a central location and the deployment and management of applications to aide in testing of an application on different hardware.

#### Source/pip

If installation is via pip or source, export the variables described below (control-variables) to your path. For instance, to run on a non-GPU x86 node at TACC you might export:
```
export CT_CONTROLLER_NUM_NODES=1
export CT_CONTROLLER_TARGET_SITE=TACC
export CT_CONTROLLER_NODE_TYPE=x86
export CT_CONTROLLER_GPU=0
export CT_CONTROLLER_CONFIG_PATH=./config.yml
export CT_CONTROLLER_OUTPUT_DIR=./output
```

Ensure that the output directory exists and is writable. Then, import and run the `ctcontroller` package:

```
python -c "import ctcontroller; ctcontroller.run()"
```

#### Docker image

If using the docker image, the environment variables should be passed via the command-line to the docker image. Also note that any external files will need to be mounted and paths. In particular, if you would like to save any of the output files make sure that the output directory is set to a path that will be available after the container shuts down. For instance, the same non-GPU x86 node at TACC might be run with:

```
docker run \
--mount type=bind,source="$HOME/.ssh",target=/ssh_keys \
--mount type=bind,source="./output",target=/output \
--mount type=bind,source="./config.yml",target=/config.yml \
-e CT_CONTROLLER_TARGET_SITE=TACC \
-e CT_CONTROLLER_NUM_NODES=1
-e CT_CONTROLLER_NODE_TYPE=x86 \
-e CT_CONTROLLER_GPU=0 \
-e CT_CONTROLLER_CONFIG_PATH=./config.yml \
-e CT_CONTROLLER_OUTPUT_DIR=/output \
tapis/ctcontroller
```

#### Demo mode

Demo mode is used to run and control an application running on the machine where `ctcontroller` is deployed. It creates an API server that listens to web requests, useful for deploying an application in the field. This mode runs requires running ctcontroller from a docker image.

#### Running as a service
The `install.sh` script will create and enable a systemd service that will run the `ctcontroller` in demo mode.
Note that this will only work on Linux machines.
After running `install.sh`, restart your machine or run `systemctl start ctcontroller.service` to start the service. You should then be able to access the server docs from `http://localhost:8080/docs`.

Check the server documentation for detailed documentation on the API endpoints, but broadly, you there are endpoints to:
1. startup and shutdown the server
2. start and stop the application
3. check the health of the hardware and application
4. download logs

#### Running manually

If you are unable or do not want to create a systemd service, you can manually launch the API server by running:

```
./systemd/start-ctcontroller-container.sh
docker start -a ctcontroller
```

Then to stop run `docker rm -f ctcontroller`.
