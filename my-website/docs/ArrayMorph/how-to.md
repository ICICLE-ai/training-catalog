---
tags:
  - CI4AI
---
# How-To Guides

## Install dependencies

It is recommended to use Conda (and conda-forge) for managing dependencies.

1. Install [Miniconda](https://docs.anaconda.com/miniconda/)  
2. Install [conda-build](https://docs.conda.io/projects/conda-build/en/stable/install-conda-build.html) for installing local conda packages
3. Create and activate environment with dependencies:
   ```bash
   conda create -n arraymorph
   conda activate arraymorph
   conda install -n arraymorph cmake conda-forge::hdf5=1.14.2 conda-forge::aws-sdk-cpp conda-forge::azure-core-cpp conda-forge::azure-storage-blobs-cpp conda-forge::h5py
   ```

## Install ArrayMorph via Conda
### Option 1: Build and Install from Source
Clone the repository and build the conda package locally:
   ```bash
    git clone https://github.com/ICICLE-ai/arraymorph.git
    cd arraymorph/arraymorph
    conda build -c conda-forge .
    conda install -n arraymorph arraymorph --use-local -c conda-forge
   ```

### Option 2: Install from Pre-built Local Package
We provide a pre-built conda package in the arraymorph_channel directory. Install it directly using:
   ```bash
   git clone https://github.com/ICICLE-ai/arraymorph.git
   cd arraymorph/arraymorph_channel
   conda index .
   conda install -n arraymorph arraymorph -c file://$(pwd) -c conda-forge
   ```

## Install ArryMorph from source code

### Build ArrayMorph
```bash
git clone https://github.com/ICICLE-ai/arraymorph.git
cd arraymorph/arraymorph
cmake -B ./build -S . -DCMAKE_PREFIX_PATH=$CONDA_PREFIX
cd build
make
```

### Enable VOL plugin:
```bash
export HDF5_PLUGIN_PATH=/path/to/arraymorph/arraymorph/build/src
export HDF5_VOL_CONNECTOR=arraymorph
```

## Configure Environment for Cloud Access
Create a JSON configuration file named `config` at `~/.arraymorph` with the following settings based on your cloud provider:
### AWS Configuration:
```json
{
    "STORAGE_PLATFORM": "S3",
    "BUCKET_NAME": "XXXXX",
    "AWS_ACCESS_KEY_ID": "XXXXX",
    "AWS_SECRET_ACCESS_KEY": "XXXXX",
    "AWS_REGION": "us-east-2"
}

```

### Azure Configuration:
```json
{
    "STORAGE_PLATFORM": "Azure",
    "BUCKET_NAME": "XXXXX",
    "AZURE_STORAGE_CONNECTION_STRING": "XXXXX"
}
```

### S3-compatible object store configuration (MinIO, Ceph, Garage):
Set `AWS_ENDPOINT_URL_S3`, `AWS_USE_PATH_STYLE`, and `AWS_SIGNED_PAYLOADS` to match the requirements of most self-hosted S3-compatible stores:
```json
{
    "STORAGE_PLATFORM": "S3",
    "BUCKET_NAME": "XXXXX",
    "AWS_ENDPOINT_URL_S3": "XXXXX",
    "AWS_S3_ADDRESSING_STYLE": "path",
    "AWS_ACCESS_KEY_ID": "XXXXX",
    "AWS_SECRET_ACCESS_KEY": "XXXXX",
    "AWS_REGION": "XXXXX",
    "AWS_USE_PATH_STYLE": "true",
    "AWS_USE_TLS": "true",
    "AWS_SIGNED_PAYLOADS": "true"
}
```

## Enable ArrayMorph with h5py in Python
To enable ArrayMorph when using h5py, import the `arraymorph` package BEFORE importing `h5py`:

```python
import arraymorph
import h5py
```
