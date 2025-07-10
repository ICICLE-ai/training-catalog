---
tags:
  - Software
  - CI4AI
  - Animal-Ecology
  - Release 2025-07
  - Release 2024-12
  - Release 2024-09
  - Release 2023-10
  - Release 2023-06
  - Release 2023-04
---

# Camera-traps

The Camera Traps application is both a simulator and IoT device software for utilizing machine learning on the edge in field research. The first implementation specializes in applying computer vision (detection and classification) to wildlife images for animal ecology studies. Two operational modes are supported: "simulation" mode and "demo" mode. When executed in simulation mode, the software serves as a test bed for studying ML models, protocols and techniques that optimize storage, execution time, power and accuracy. It requires an input dataset of images to act as the images that would be generated an IoT camera device; it uses these images to drive the simulation. 

Conversely, when run in "demo" mode, the application serves as software that can be deployed onto actual, Linux-based camera trap devices in the wild. In this case, the Camera Traps software relies on a digital camera accessible over a Linux device mount (the default `/dev/video0` location can be re-configured), and it drives the camera directly using the Linux Motion activation software, which comes bundled with the as a plugin with Camera Traps. It includes a detection reporter plugin and MQTT component which coordinate to communicate in real time when a configurable object of interest has been detected (up to a configurable confidence threshold). As a proof of concept of the capabilities of the software, we are producing a demo integration with drone software developed by the Stewart Lab at OSU which enables the Camera Traps software to communicate over a local network to a nearby drone whenever an object of interest is detected. 


[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/tapis-project/camera-traps)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/tapis-project/camera-traps/blob/main/LICENSE)


# Acknowledgements

*This work has been funded by grants from the National Science Foundation, including the ICICLE AI Institute (OAC 2112606) and Tapis (OAC 1931439).*
