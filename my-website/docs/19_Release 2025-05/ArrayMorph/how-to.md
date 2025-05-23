---
tags:
  - CI4AI
---

# How-To Guides

## Install dependencies

It is recommended to use Conda (and conda-forge) for managing dependencies.

1. Install [Miniconda](https://docs.anaconda.com/miniconda/)  
2. Create and activate environment with dependencies:
   ```bash
   conda create -n arraymorph conda-forge::gxx=8
   conda activate arraymorph
   conda install -n arraymorph cmake conda-forge::hdf5=1.14.2 conda-forge::aws-sdk-cpp conda-forge::azure-storage-blobs-cpp conda-forge::h5py
   ```

## Build ArrayMorph

```bash
git clone https://github.com/ICICLE-ai/arraymorph.git
cd arraymorph/arraymorph
cmake -B ./build -S . -DCMAKE_PREFIX_PATH=$CONDA_PREFIX
cd build
make
```

## Configure Environment for Cloud Access

### Enable VOL plugin:
```bash
export HDF5_PLUGIN_PATH=/path/to/arraymorph/arraymorph/build/src
export HDF5_VOL_CONNECTOR=arraymorph
```

### AWS Configuration:
```bash
export BUCKET_NAME=XXXXXX
export AWS_ACCESS_KEY_ID=XXXXXX
export AWS_SECRET_ACCESS_KEY=XXXXXX
export AWS_REGION=us-east-2  # or your bucket's region
```

### Azure Configuration:
```bash
export AZURE_CONNECTION_STRING=XXXXXX
```