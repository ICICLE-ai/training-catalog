---
tags:
  - CI4AI
  - Visual-Analytics
  - Software
---
# How-To Guides

## The pipeline file (`operations.json`)

```json
{
  "version": "1.0",
  "name": "My pipeline",
  "createdAt": "2026-01-01T00:00:00.000Z",
  "steps": [
    { "id": "a1", "op": "grayscale",     "params": {},            "enabled": true },
    { "id": "b2", "op": "gaussian_blur", "params": { "ksize": 5 }, "enabled": true }
  ]
}
```

Disabled steps are skipped. The same file drives the editor, the CLI, and the
Tapis job.

## Configure a batch job submission

| Field | Meaning |
| --- | --- |
| **Job name** | Optional label (auto-generated if blank). |
| **Source system** | Tapis system holding your input images. |
| **Input directory** | Folder of images — processed **recursively** (all subfolders). |
| **Output directory** | Where processed images are archived (mirrors the input tree). |
| **Archive system** | System the output directory lives on. |
| **Image extensions** | Optional filter, e.g. `.jpg,.png`. Blank = common defaults. |
| **Exec system** | Where the job runs. Determines the queue and working dirs (below). |
| **Allocation account (SLURM)** | Passed as `-A <account>`. |
| **Nodes / Cores / Mem / Minutes** | Compute limits. |

#### System-specific behaviour

The **exec system** you pick changes how the job is submitted:

| Exec system | Queue | Working dirs |
| --- | --- | --- |
| OSC (`pitzer` / `cardinal` / `ascend`) | `cpu` | `/fs/scratch/<account>/harvest_jobs/${JobUUID}` |
| Expanse (`expanse-*`) | `tapisShared` | app defaults (no scratch override) |

## Monitor, search, cancel jobs

The **Your jobs** table lists your `opencv-preprocess` jobs with live status
badges (auto-refreshes while any job is active). You can:

- **Search** by job name or UUID.
- **Filter** by status.
- **Cancel** a running/queued job with the ✕ button.

## Run the pipeline without the app (CLI / container)

The same processing engine runs standalone — handy for local batches or scripts.

### Python CLI

```bash
pip install -e packages/opencv-executor

# single image
opencv-executor run operations.json input.jpg output.jpg

# a flat folder
opencv-executor batch operations.json input_dir/ output_dir/
```

Recursive processing (all subdirectories, mirroring the tree) is what the Tapis
container uses:

```bash
python packages/tapis-job/preprocess.py \
  --input  input_dir/ \
  --output output_dir/ \
  --pipeline operations.json
```

### Container

```bash
apptainer run \
  --bind /data/in:/in --bind /data/out:/out \
  --bind "$PWD/operations.json:/pipeline.json" \
  preprocess.sif --input /in --output /out --pipeline /pipeline.json
```

Config can also come from env vars: `INPUT_DIR`, `OUTPUT_DIR`, `PIPELINE_FILE`,
`IMAGE_EXTENSIONS`.
