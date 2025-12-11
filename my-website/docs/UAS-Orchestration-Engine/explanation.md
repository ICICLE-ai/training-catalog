---
tags:
  - Digital-Agriculture
---
# Explanation

### Background:

UAS Imagery is increasingly being used by farmers and agricultural researchers. While farmers commonly rely on commercial scouting services that have their own proprietary pipelines, these are unavailable to agricultural researchers who are looking to create novel approaches to weed detection, nutrient management, and plant disease utilizing AI phenotyping. In our case, a UAS pilot was able to conduct more than 400 flights across a total of 700 fields in the summer of 2025 across small-plot and on-farm research fields, generating nearly 4 TB of imagery utilizing both  RGB and multispectral sensors. Our workflow for generating AI phenotypes of canopy cover, spectral reflectance, and growth stage included 15 unique Python scripts. To process these manually would have involved thousands of unique interdependent jobs. We created a UAS orchestration engine to solve our problem of processing many terabytes of aerial imagery and running thousands of jobs using a directed acyclic graph (DAG) approach which maximizes parallel processing capability. While originally developed for SLURM HPC, it also contains an implementation for Google Cloud Platform and could be extended to other cloud platforms as needed. The UAS Orchestration Engine was built by researchers for researchers. It is open-source and modular, so that researchers can use many of the common building blocks such as orthomosaic creation and plot tile image extraction while adding steps that are unique to their own use case. 

### Key Features:

- **Multi-Platform Support**: Run on HPC clusters (SLURM) or cloud platforms (GCP Batch, with AWS/Azure support in development)
- **Scalable Architecture**: Process hundreds or thousands of flights in parallel using containerized workflows
- **On-Demand Processing**: Folder-watching capability automatically initiates processing as new imagery arrives
- **Modular Pipeline**: 15+ configurable processing steps from raw imagery to AI inference and visualization
- **Dual Georeferencing Pathways**: Supports both orthomosaic-based workflow and direct georeferencing with image registration
- **Automated Orthomosaic Generation**: Integration with OpenDroneMap for creating georeferenced mosaics
- **Temporal Alignment**: Automatic registration of multi-temporal imagery for consistent AI training datasets
- **AI Phenotyping**: Inference modules for crop growth stage, canopy cover, and spectral reflectance
- **GeoJSON Generation**: Automated creation of plot-level phenotypic data for visualization
- **Web-based Visualization**: Map tile generation for interactive web viewers
- **Docker Containerization**: Consistent execution environments across platforms

![The data processing workflow of the orchestration engine](https://github.com/ICICLE-ai/UAS-Orchestration-Engine/raw/main/steps_taxonomy.png)

*The data processing workflow of the orchestration engine, from raw imagery to visualization assets.*