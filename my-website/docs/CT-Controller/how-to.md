---
tags:
  - CI4AI
  - Animal Ecology
---

# How-To Guides

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

### Source/pip

If installation is via pip or source, export the variables described [below](#control_variables) to your path. For instance, to run on a non-GPU x86 node at TACC you might export:
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

### Docker image

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