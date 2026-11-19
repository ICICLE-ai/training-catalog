---
tags:
  - Foundation-AI
  - Release 2026-11
---
# Multimodal Yield Estimation

A transformer-based model that estimates plot-level corn yield (bu/acre) from **weekly text captions** of field conditions (weather, soil chemistry, topography and treatment) and **UAS RGB images** of the plot, at any point in the growing season. This repository contains the trained checkpoint, inference scripts that compute the Qwen3 text and DINOv3 image embeddings and predict yield, and the training code.

<div align="center">

[![Hugging Face Repo](https://img.shields.io/badge/Hugging%20Face-Repository-yellow?logo=huggingface&style=flat-square)](https://huggingface.co/ICICLE-AI/multimodal-yield-estimation)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://huggingface.co/ICICLE-AI/multimodal-yield-estimation/blob/main/LICENSE)

</div>



## References

- [Qwen/Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B): text embedding model used for the weekly captions (1024-d).
- [facebook/dinov3-vitb16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vitb16-pretrain-lvd1689m): image backbone used for the UAS plot tiles (768-d).
- [Daymet](https://daymet.ornl.gov/): source of the daily weather variables summarized in the captions.
- [Hugging Face custom models](https://huggingface.co/docs/transformers/custom_models): how `trust_remote_code=True` loading works.
- **Cutoff**: the number of weeks after planting the model is allowed to see. Week 12 means the prediction uses captions and images from the first 12 weeks only.
- **UAS**: Uncrewed Aircraft System (drone) imagery.

## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

For questions, issues, or support, please contact:

Sarikaa Sridhar
sridhar.86@osu.edu
