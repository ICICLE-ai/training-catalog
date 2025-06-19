---
tags:
  - CI4AI
  - AI4CI
---

# How-To Guide

## System Requirements

Users need to have the following software/tools installed in their PC/server. The source code was compiled and run successfully in Linux (Ubuntu and Centos distributions).

```
Make >= 4.4
GCC >= 10.1 (Support for C++ >= 14)
OpenMP >= 4.5
Python >= 3.7
NumPy >= 1.21 (Or, Anaconda environment)
```


## Installation

To install the package, run the following commands:

- `git clone https://github.com/ICICLE-ai/iSpLib.git`: To clone this repository.
- `./configure`: To download and run the auto-tuner. This is a pre-requisite for the installation.
- Create a virtualenv as the packages might conflict.
- Install the dependencies `pip install torch torchvision scikit-learn torch-scatter`.
- `make`: To install the library.
- Finally install custom version of torch-geometric `pip install git+https://github.com/gamparohit/pytorch_geometric.git`

## Troubleshoot

- If `make` command exits with unknown error message, try running `pip3 install -e .` instead.
- If you are having trouble installing torch-scatter, install it with -f flag and torch version. 

```
import torch
print(torch.__version__)
!pip install torch-scatter -f https://data.pyg.org/whl/torch-{torch.__version__}.html
```
