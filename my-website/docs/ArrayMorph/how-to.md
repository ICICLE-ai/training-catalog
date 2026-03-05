---
tags:
  - CI4AI
---
# How-To Guides

## Install ArrayMorph

```bash
pip install arraymorph
```

Once installed, jump straight to [Configure credentials for AWS S3](#configure-credentials-for-aws-s3) or [Azure](#configure-credentials-for-azure-blob-storage) below.

If you need the standalone `lib_arraymorph` binary, you can [download a pre-built release](#download-a-pre-built-lib_arraymorph) or [build from source](#build-from-source).

## Configure credentials for AWS S3

Use the Python API before opening any HDF5 files:

```python
import arraymorph

arraymorph.configure_s3(
    bucket="my-bucket",
    access_key="MY_ACCESS_KEY",
    secret_key="MY_SECRET_KEY",
    region="us-east-1",
    use_tls=True,
)
arraymorph.enable()
```

Or set environment variables directly:

```bash
export STORAGE_PLATFORM=S3
export BUCKET_NAME=my-bucket
export AWS_ACCESS_KEY_ID=MY_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=MY_SECRET_KEY
export AWS_REGION=us-east-1
export HDF5_PLUGIN_PATH=$(python -c "import arraymorph; print(arraymorph.get_plugin_path())")
export HDF5_VOL_CONNECTOR=arraymorph
```

## Configure credentials for Azure Blob Storage

```python
import arraymorph

arraymorph.configure_azure(
    container="my-container",
    connection_string="DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net",
)
arraymorph.enable()
```

Or set environment variables directly:

```bash
export STORAGE_PLATFORM=Azure
export BUCKET_NAME=my-container
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;..."
export HDF5_PLUGIN_PATH=$(python -c "import arraymorph; print(arraymorph.get_plugin_path())")
export HDF5_VOL_CONNECTOR=arraymorph
```

## Use an S3-compatible object store (MinIO, Ceph, Garage)

Pass `endpoint`, `addressing_style=True`, and `use_signed_payloads=True` to match the requirements of most self-hosted S3-compatible stores:

```python
import arraymorph

arraymorph.configure_s3(
    bucket="my-bucket",
    access_key="MY_ACCESS_KEY",
    secret_key="MY_SECRET_KEY",
    endpoint="http://localhost:9000",
    region="us-east-1",
    use_tls=False,
    addressing_style=True,
    use_signed_payloads=True,
)
arraymorph.enable()
```

## Download a pre-built lib_arraymorph

Each [GitHub release](https://github.com/ICICLE-ai/ArrayMorph/releases) attaches standalone pre-compiled binaries of `lib_arraymorph` for all supported platforms:

| File                               | Platform            |
| ---------------------------------- | ------------------- |
| `lib_arraymorph-linux-x86_64.so`   | Linux x86_64        |
| `lib_arraymorph-linux-aarch64.so`  | Linux aarch64       |
| `lib_arraymorph-macos-arm64.dylib` | macOS Apple Silicon |

Download the file for your platform from the release assets and set `HDF5_PLUGIN_PATH` to the directory containing it before calling `arraymorph.enable()` or setting `HDF5_VOL_CONNECTOR` manually.

## Build from source

Use this path if you want to compile `lib_arraymorph` yourself — for example to target a specific platform, contribute changes, or build a custom wheel.

### Prerequisites

- [vcpkg](https://github.com/microsoft/vcpkg) — installs the AWS and Azure C++ SDKs via CMake
- [CMake](https://cmake.org) and [Ninja](https://ninja-build.org)
- [uv](https://docs.astral.sh/uv/) — Python package manager

### Step 1 — Clone and create a virtual environment

```bash
git clone https://github.com/ICICLE-ai/ArrayMorph.git
cd ArrayMorph
uv venv
source .venv/bin/activate
```

### Step 2 — Install h5py

`lib_arraymorph` links against an HDF5 shared library at build time. Rather than requiring a separate system-wide HDF5 installation, the build system points CMake at the `.so` / `.dylib` that h5py already bundles. Install h5py first so those libraries are present:

```bash
uv pip install h5py
```

On macOS the bundled libraries land in `.venv/lib/python*/site-packages/h5py/.dylibs/`; on Linux in `.venv/lib/python*/site-packages/h5py.libs/`.

### Step 3 — Configure and build the shared library

```bash
export HDF5_DIR=$(.venv/bin/python -c "import h5py,os; d=os.path.dirname(h5py.__file__); print(os.path.join(d,'.dylibs') if os.path.exists(os.path.join(d,'.dylibs')) else os.path.join(os.path.dirname(d),'h5py.libs'))")

cmake -B lib/build -S lib \
    -DCMAKE_TOOLCHAIN_FILE=${VCPKG_ROOT:-~/.vcpkg}/scripts/buildsystems/vcpkg.cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -G Ninja

cmake --build lib/build
```

This produces `lib/build/lib_arraymorph.dylib` on macOS or `lib/build/lib_arraymorph.so` on Linux.

### Optional — Python package

If you also want to use the Python API, install the package in editable mode:

```bash
HDF5_DIR=$HDF5_DIR \
CMAKE_TOOLCHAIN_FILE=${VCPKG_ROOT:-~/.vcpkg}/scripts/buildsystems/vcpkg.cmake \
uv pip install -e .
```

Or build a redistributable wheel:

```bash
HDF5_DIR=$HDF5_DIR \
CMAKE_TOOLCHAIN_FILE=${VCPKG_ROOT:-~/.vcpkg}/scripts/buildsystems/vcpkg.cmake \
uv build --wheel --no-build-isolation
```

The wheel is written to `dist/`. Install it in any environment with:

```bash
pip install dist/arraymorph-*.whl
```
