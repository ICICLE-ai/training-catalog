---
tags:
  - CI4AI
  - Visual-Analytics
  - Software
  - Release 2026-07B
  - Release 2026-11
---
# No-Code Image Lab (Image Pre-processing Studio)

A browser-based OpenCV pipeline builder: build an image pre-processing
pipeline in an interactive editor with live preview, then run it at scale as
a Tapis batch job over every image in a folder tree — or standalone via CLI
or container.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/opencv-image-playground)
[![License: BSD_3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)

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
