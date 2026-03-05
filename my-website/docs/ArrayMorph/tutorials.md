---
tags:
  - CI4AI
---
# Tutorials

## Write and read a chunked array on AWS S3

This tutorial walks through writing a 2-D NumPy array to a cloud HDF5 file and reading a slice of it back.

### Prerequisites

- An AWS account with an S3 bucket, or an S3-compatible object store
- ArrayMorph installed (`pip install arraymorph`)

### Step 1 — Configure and enable ArrayMorph

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

`arraymorph.enable()` sets `HDF5_PLUGIN_PATH` and `HDF5_VOL_CONNECTOR` in the current process. Any `h5py.File(...)` call made after this point is routed through ArrayMorph.

### Step 2 — Write array data

```python
import h5py
import numpy as np

data = np.fromfunction(lambda i, j: i + j, (100, 100), dtype="i4")

with h5py.File("demo.h5", "w") as f:
    f.create_dataset("values", data=data, chunks=(10, 10))
```

Each 10×10 chunk is stored as a separate object in your S3 bucket.

### Step 3 — Read a slice back

```python
import h5py

with h5py.File("demo.h5", "r") as f:
    dset = f["values"]
    print(dset.dtype)           # int32
    print(dset[5:15, 5:15])     # fetches only the chunks that overlap this slice
```

Only the chunks that overlap the requested hyperslab are fetched from cloud storage — no full-file download occurs.
