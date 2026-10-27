---
tags:
  - AI4CI
  - CI4AI
  - Software
  - Release 2026-10
---
# Video Segmentation & Tracking

Segment objects in a video by annotating a few keyframes, then track every object through the whole video with the SAM3 Video Service running on a GPU node. Results export as an annotated MP4, COCO JSON, or a full frames-and-masks dataset written straight to HPC storage via Tapis.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/smart_labeler)
[![License: BSD_3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>


## References

- [Tapis v3 — HPC job execution framework](https://tapis-project.org)
- [SAM3 (Segment Anything Model 3) — Meta AI](https://github.com/facebookresearch/sam3)
- [COCO JSON format specification](https://cocodataset.org/#format-data)
- [Smart Labeler — Image Segmentation](https://github.com/ICICLE-ai/smart_labeler/blob/main/SEGMENTATION_README.md)
- [Video Segmentation changelog](https://github.com/ICICLE-ai/smart_labeler/blob/main/VIDEO_SEGMENTATION_CHANGELOG.md)

## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Please open an issue at [github.com/OSU-SAI-Lab/smart-labeler/issues](https://github.com/OSU-SAI-Lab/smart-labeler/issues) with a description of the problem, steps to reproduce, the service address shown in the status bar, and the tracking job id if a job failed.
