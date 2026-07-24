---
tags:
  - CI4AI
  - Visual-Analytics
  - Software
  - Release 2026-07B
---
# No-Code Image Lab (Image Pre-processing Studio)

A browser-based OpenCV pipeline builder: build an image pre-processing
pipeline in an interactive editor with live preview, then run it at scale as
a Tapis batch job over every image in a folder tree — or standalone via CLI
or container.
Link to the hosted service: https://icicleai.tapis.io/#/no-code-image-lab
<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/opencv-image-playground)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ICICLE-ai/opencv-image-playground/blob/main/LICENSE)

</div>



## References

- [Tapis Jobs API](https://tapis-project.github.io/live-docs/?service=Jobs) — the HPC job submission service used for batch runs.
- [SETUP.md](https://github.com/ICICLE-ai/opencv-image-playground/blob/main/SETUP.md) — install, configuration, and deployment.
- [packages/core/src/registry.ts](https://github.com/ICICLE-ai/opencv-image-playground/blob/main/packages/core/src/registry.ts) — TypeScript operation registry (editor/CLI parity).
- [packages/opencv-executor/opencv_executor/ops.py](https://github.com/ICICLE-ai/opencv-image-playground/blob/main/packages/opencv-executor/opencv_executor/ops.py) — Python operation implementations.

## Acknowledgements

<!-- Please include other funding sources above this line. -->

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Please report issues via [GitHub Issues](https://github.com/ICICLE-ai/opencv-image-playground/issues).
