---
tags:
  - CI4AI
---

# Explanation

### How ArrayMorph Works

ArrayMorph plugs into the HDF5 stack using a VOL (Virtual Object Layer) plugin that intercepts file operations and routes them to cloud object storage instead of local files. This allows existing HDF5 APIs (both C++ and h5py in Python) to operate on cloud-based data seamlessly, enabling transparent cloud access for scientific or ML pipelines.

It supports:
- Cloud backends: AWS S3 and Azure Blob
- File formats: Current binary data stream (we plan to extend to other formats like jpg in the future)
- Languages: C++ and Python (via h5py compatibility)

The system is designed to be efficient in latency-sensitive scenarios and aims to integrate well with large-scale distributed training and inference.