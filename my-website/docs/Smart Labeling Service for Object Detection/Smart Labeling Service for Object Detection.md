---
tags:
  - CI4AI
  - AI4CI
  - Software
  - Release 2026-05
  - Release 2026-10
---
# Smart Labeling Service for Object Detection

A 7-step HPC-backed pipeline for few-shot object detection — from interactive image annotation through class support generation, proposal visualization, and Tapis-powered job execution — built to work across any research domain. Also includes a dedicated **Semantic Segmentation** pipeline for polygon and pixel-mask annotation with SAM3-assisted labeling.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/smart_labeler)
[![License: BSD_3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>


## References

- [Tapis v3 — HPC job execution framework](https://tapis-project.org)
- [Patra Model Registry — ICICLE AI model catalog](https://patra.pods.icicleai.tapis.io/)
- [SAHI — Slicing Aided Hyper Inference for small-object detection](https://github.com/obss/sahi)
- [COCO JSON format specification](https://cocodataset.org/#format-data)

## Project documentation

- [setup.md](https://github.com/ICICLE-ai/smart_labeler/blob/main/setup.md) — running the client and server locally
- [CONTRIBUTING.md](https://github.com/ICICLE-ai/smart_labeler/blob/main/CONTRIBUTING.md) — how to contribute and what a pull request should contain
- [docs/TESTING.md](https://github.com/ICICLE-ai/smart_labeler/blob/main/docs/TESTING.md) — how a change is verified before merge and before deployment
- [docs/user-tests/](https://github.com/ICICLE-ai/smart_labeler/blob/main/docs/user-tests) — the manual test record
- [docs/RELEASE_CHECKLIST.md](https://github.com/ICICLE-ai/smart_labeler/blob/main/docs/RELEASE_CHECKLIST.md) — the checklist to complete before a public release
- [docs/MAINTAINER_ROLES.md](https://github.com/ICICLE-ai/smart_labeler/blob/main/docs/MAINTAINER_ROLES.md) — maintainer responsibilities and decision rights
- [SECURITY.md](https://github.com/ICICLE-ai/smart_labeler/blob/main/SECURITY.md) — reporting a vulnerability
- [SEGMENTATION_README.md](https://github.com/ICICLE-ai/smart_labeler/blob/main/SEGMENTATION_README.md) — the semantic segmentation pipeline
- [packages/README.md](https://github.com/ICICLE-ai/smart_labeler/blob/main/packages/README.md) — the five publishable npm packages

## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Please open an issue at [github.com/OSU-SAI-Lab/smart-labeler/issues](https://github.com/OSU-SAI-Lab/smart-labeler/issues) with a description of the problem, steps to reproduce, and any relevant logs from the Tapis job status bar.
