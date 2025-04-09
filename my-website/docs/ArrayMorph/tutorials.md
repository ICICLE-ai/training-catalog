---
tags:
  - CI4AI
---

# Tutorials

## Run a simple example: Writing and Reading HDF5 files from Cloud

### Prerequisites:
- AWS or Azure cloud account with credentials
- S3 bucket or Azure container
- ArrayMorph dependencies installed

### Steps:
1. Activate conda environment  
   ```bash
   conda activate arraymorph
   ```

2. Write sample HDF5 data to the cloud  
   ```bash
   cd examples/python
   python3 write.py
   ```

3. Read data back from cloud HDF5 file  
   ```bash
   cd examples/python
   python3 read.py
   ```