---
tags:
  - AI4CI
  - Release 2025-07
---



# Distributed Training Estimator of LLMs

This component implements a time cost estimator for distributed training of large language models (LLMs). It is used to predict the time required to train one batch across multiple GPUs. The predictor module only requires at least a CPU. The computation sampling module needs one or more GPUs, while the communication sampling module requires multiple GPUs, depending on your computing platform.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/distributed_training_estimator_of_LLM)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*
