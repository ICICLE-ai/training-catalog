---
tags:
  - CI4AI
---
# Explanation

## How ArrayMorph works

ArrayMorph is implemented as an HDF5 **Virtual Object Layer (VOL)** connector. The VOL is an abstraction layer inside the HDF5 library that separates the public API from the storage implementation. By providing a plugin that registers itself as a VOL connector, ArrayMorph intercepts every HDF5 file operation before it reaches the native POSIX layer.

When `arraymorph.enable()` is called:

1. `HDF5_PLUGIN_PATH` is set to the directory containing the compiled shared library (`lib_arraymorph.so` / `lib_arraymorph.dylib`).
2. `HDF5_VOL_CONNECTOR=arraymorph` tells HDF5 to load and activate that plugin for all subsequent file operations.

From this point, a call like `h5py.File("demo.h5", "w")` does not touch the local filesystem. Instead, the VOL connector:

1. Reads cloud credentials from environment variables and constructs an AWS S3 or Azure Blob client (selected by `STORAGE_PLATFORM`).
2. On dataset read/write, translates the HDF5 hyperslab selection into a list of chunks and dispatches asynchronous get/put requests against the object store — one object per chunk.

### Chunked storage model

HDF5 datasets are divided into fixed-size chunks (e.g. `chunks=(64, 64)` for a 2-D dataset). ArrayMorph stores each chunk as an independent object in the bucket. The object key encodes the dataset path and chunk coordinates, so a partial read only fetches the chunks that overlap the requested slice. For large chunks, ArrayMorph can issue byte-range requests to retrieve only the needed bytes within a chunk object.

### Async I/O

Both the S3 and Azure backends use asynchronous operations dispatched to a thread pool. This allows ArrayMorph to fetch multiple chunks in parallel, which is important for workloads that access many chunks per read (e.g. strided access patterns in machine learning data loaders).

### Compatibility

Because the interception happens at the VOL layer, no changes to application code are required. Any program that opens HDF5 files with h5py or the HDF5 C++ API will automatically use ArrayMorph once the plugin is loaded.
