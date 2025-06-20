---
tags:
  - Foundation-AI
---

# How-To Guides

## Initial set-up
- Install Poetry: https://python-poetry.org/docs/#installation.
- Install Python 3.7, which is the version of Python that has been used for developing this repository.
- Install `pipx` so that we can install command-line dependencies: https://pypa.github.io/pipx/.

First, check that we are not unintentionally in a virtualenv.
Run `poetry env info`; under "Virtualenv", it should show `Path:           NA`.
If it displays the path to an existing virtualenv, deactivate it, for example by running `deactivate` or `conda deactivate`.

Then run the following to set up the package:
```
cd semantic_parsing_with_constrained_lm
poetry config virtualenvs.in-project true
poetry env use <path to python3.7>
poetry install
poetry shell
```

Before running any of the commands below, run `poetry shell` to activate the virtualenv where all packages have been installed. You can `exit` to deactivate the virtualenv.


## Running a command
To run this script, you first need to source and load the virtual environment through poetry:
source $HOME/.poetry/env
poetry shell


Afterwards you can run the script as follows:
bash runCompletePipeline.sh "Entery query here within quotations"

This will output a list of options which the user will have to select from. Currently output to output.json