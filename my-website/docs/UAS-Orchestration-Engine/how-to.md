---
tags:
   - Digital-Agriculture
---
# How-To Guides

### Problem Description:

This project provides an open-source orchestration engine designed to automate and scale the transformation of raw Unmanned Aerial Systems (UAS) imagery into structured, AI-ready datasets for agricultural research. The pipeline supports both High-Performance Computing (HPC) environments using SLURM and cloud platforms like Google Cloud Platform (GCP) Batch, enabling flexible deployment for different research needs.

The engine addresses the critical bottleneck of data processing for researchers, enabling them to move from raw aerial images to actionable, AI-driven phenotypic insights with minimal manual intervention.

### Getting Started

## Installation:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ICICLE-ai/UAS-Orchestration-Engine.git
   cd UAS-Orchestration-Engine
   ```

2. **Create the conda environment:**
   ```bash
   # For local development/SLURM
   conda env create -f environment_local.yml
   conda activate harvest

   # For Docker containers
   conda env create -f environment_docker.yml
   ```

3. **Configure rclone for cloud storage (GCP only):**
   ```bash
   rclone config
   # Set up Google Cloud Storage remote named 'gcs'
   ```

### Configuration

1. **Create a YAML configuration file** based on your deployment platform:
   - For SLURM: Use `yaml/uas_config.yaml` as a template
   - For GCP: Use `yaml/uas_config_gcp.yaml` as a template

2. **Key configuration sections:**
   ```yaml
   platform: 'gcp'  # or 'slurm'
   base_folder: ':gcs:data-uas/2025_poc/'  # Storage location

   flight_list:     # Define your fields and flights
     field_name:
       orthomosaic_name: []  # Empty list or boundary shapefile path

   plot_shapefiles: # Shapefile locations for plot boundaries
     field_name:
       crop_type: 'path/to/shapefile.shp'

   shapefiles_alignment_folder: 'shapefiles/alignment/'  # Required for step2
   shapefiles_alignment_format: '{om}_pts/{om}_pts.shp'

   uas_pipeline:    # Configure each processing step
     step1:
       resources:
         cpus: 16
         memory: 120
         machine_type: 'n2-highmem-16'  # GCP only
   ```

3. **Prepare required shapefiles:**
   - **Plot boundary shapefiles** (required): Define individual plot boundaries for each field and crop type
   - **Alignment point shapefiles** (required for step2): Control points for temporal registration of orthomosaics
   - **Boundary polygon shapefiles** (optional): Only needed when a single field contains multiple orthomosaics that need to be separated

### Docker Container Setup (GCP/Cloud)

1. **Build the worker container:**
   ```bash
   docker build -t us-central1-docker.pkg.dev/your-project/orchestration-images/uas-worker:latest .
   ```

2. **Push to container registry:**
   ```bash
   docker push us-central1-docker.pkg.dev/your-project/orchestration-images/uas-worker:latest
   ```

3. **Build the ODM container:**
   ```bash
   docker build -f Dockerfile.odm -t us-central1-docker.pkg.dev/your-project/orchestration-images/odm:latest .
   docker push us-central1-docker.pkg.dev/your-project/orchestration-images/odm:latest
   ```

## Usage

### Running on SLURM

1. **Initialize the environment:**
   ```bash
   source ~/miniconda3/etc/profile.d/conda.sh
   conda activate harvest
   ```

2. **Test individual steps:**
   ```bash
   cd execution
   python orchestrate.py \
       --config_file ../yaml/uas_config.yaml \
       --platform slurm \
       --steps step1 step2 \
       --dry_run
   ```

3. **Run the orthomosaic-based pipeline:**
   ```bash
   python orchestrate.py \
       --config_file ../yaml/uas_config.yaml \
       --platform slurm \
       --steps step1 step2 step3 step7 step9 step10 step11 step14 step15
   ```

4. **Run the direct georeferencing pipeline:**
   ```bash
   python orchestrate.py \
       --config_file ../yaml/uas_config.yaml \
       --platform slurm \
       --steps step4 step5 step6 step8 step12 step13 step14 step15
   ```

5. **Enable continuous processing (folder watcher):**
   ```bash
   # Edit orchestrate_ondemand.sh with your configuration
   sbatch orchestrate_ondemand.sh
   ```

### Running on GCP Batch

1. **Configure GCP credentials:**
   ```bash
   gcloud auth login
   gcloud config set project your-project-id
   ```

2. **Run the orchestration:**
   ```bash
   cd execution
   python orchestrate.py \
       --config_file ../yaml/uas_config_gcp.yaml \
       --platform gcp \
       --steps step1 step2 step3 step7 step9 step10 step11 step14 step15
   ```

   *Note: Direct georeferencing steps (4, 5, 6, 8, 12, 13) are currently only supported on SLURM*

3. **Monitor job status:**
   ```bash
   # View generated job tracking
   python ../utils/displayjson_jobid.py \
       --json_file ../profiling/job_id.json \
       --output_html_file ../profiling/report_job_status.html

   # Open the HTML report in a browser
   ```

## AI Models

The demo dataset listed at the beginning of this readme includes pre-trained models for:

- **Growth Stage Classification** (`models/growth_stage/`): Vision Transformer model for corn growth stage prediction
- **Canopy Cover Estimation** (`models/canopy_coverage/`): K-means clustering model for canopy coverage
- **Spectral Reflectance** (`models/spectral_reflectance/`): Random Forest model for NDVI and spectral indices

Models are automatically loaded by the inference scripts.

## Monitoring and Profiling

The orchestration engine provides built-in monitoring:

- **Job Status Tracking**: Documentation of pipeline execution status (`profiling/job_id.json`)
- **Flight Processing Status**: Track which flights have completed which steps (`profiling/flight_dict.json`)
- **Performance Logging**: Execution time and resource usage metrics (`processing/logs_perf/`)
- **HTML Reports**: Auto-generated status dashboards (`utils/displayjson_*.py`)

## Troubleshooting

### Common Issues

1. **"Config file not found"**: Ensure the `--config_file` path is correct and the YAML is valid
2. **"Model not found"**: Check that model files exist in `models/` directory or are embedded in Docker container
3. **GCP authentication errors**: Run `gcloud auth application-default login`
4. **Memory errors**: Increase memory allocation in config `resources.memory` section
5. **Storage path errors**: For GCP, ensure paths use `:gcs:` prefix; for SLURM, use absolute paths
6. **Missing alignment points**: Ensure alignment point shapefiles exist for step2 temporal registration

### Validation

Each step includes validation to check if outputs were created successfully. Check logs in:
- SLURM: `processing/logs_*/`
- GCP: Google Cloud Console → Batch → Jobs → Logs
