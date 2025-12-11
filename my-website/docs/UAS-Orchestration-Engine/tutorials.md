---
tags:
  - Digital-Agriculture
---
# Tutorials

### Overview

This project provides an open-source orchestration engine designed to automate and scale the transformation of raw Unmanned Aerial Systems (UAS) imagery into structured, AI-ready datasets for agricultural research. The pipeline supports both High-Performance Computing (HPC) environments using SLURM and cloud platforms like Google Cloud Platform (GCP) Batch, enabling flexible deployment for different research needs.

The engine addresses the critical bottleneck of data processing for researchers, enabling them to move from raw aerial images to actionable, AI-driven phenotypic insights with minimal manual intervention.

### Prerequisites

**For SLURM/HPC Deployment:**
- HPC cluster with SLURM workload manager
- Singularity/Apptainer for container execution
- Conda for environment management

**For GCP Deployment:**
- Google Cloud Platform account with Batch API enabled
- `gcloud` CLI configured
- Docker for building container images
- `rclone` configured for Google Cloud Storage

**For Both:**
- Python 3.9+
- Sufficient storage for imagery and processing outputs

### Pipeline Steps

The orchestration engine supports the following processing steps:

### Orthomosaic-Based Workflow (SLURM & GCP)
1. **step1**: Orthomosaic generation using OpenDroneMap (RGB and multispectral)
2. **step2**: Orthomosaic alignment across time points using template matching
3. **step3**: Plot tile extraction from aligned orthomosaics
7. **step7**: Plot tile to patch conversion for AI models
9. **step9**: Growth stage inference (Vision Transformer model)
10. **step10**: Canopy cover inference (K-means clustering)
11. **step11**: Spectral reflectance inference (Random Forest)
14. **step14**: GeoJSON generation with phenotypic attributes
15. **step15**: Map tile generation for web visualization

### Direct Georeferencing Workflow (SLURM Only)
4. **step4**: Direct georeferencing (DGR) of individual images
5. **step5**: Image registration (IR) for temporal alignment
6. **step6**: Plot tile extraction from registered images
8. **step8**: Plot tile to patch conversion for AI models (DGR/IR pathway)
12. **step12**: Growth stage inference from DGR/IR pathway
13. **step13**: Canopy cover and spectral inference from DGR/IR pathway

Each step can be run independently or as part of a complete workflow pipeline. Steps can depend on outputs from previous steps (e.g., step2 requires step1, step9 requires step7).
