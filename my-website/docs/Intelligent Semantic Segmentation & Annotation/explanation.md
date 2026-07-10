---
tags:
  - AI4CI
  - Software
---
# Explanation

### Segmentation Pipeline Architecture

The Semantic Segmentation pipeline is a focused 2-step workflow optimized for mask-based annotation. Pipeline state is persisted in a PostgreSQL database and output files are stored on Tapis-connected HPC filesystems.

```
Step 1: Project Setup & Data Upload  → images staged to Tapis filesystem
Step 2: Interactive Image Segmentation → polygon/pixel masks (COCO JSON or Default JSON)
```

### Annotation Approach

The segmentation workflow uses **polygon masking** rather than bounding boxes, producing pixel-level boundaries for each object instance. Masks can be:

- **Drawn manually** by placing polygon points on the canvas.
- **Auto-generated** using SAM3 in Single Click or Text Prompt mode, with optional SAHI tiling for large images or small objects.

Each mask records point coordinates, bounding box, confidence score, and label. The right panel dynamically lists all masks with per-mask metadata and inline controls for editing, flagging, and deletion.

### Output Formats

Two export formats are supported throughout the pipeline:

- **COCO JSON** — standard format compatible with annotation tools (CVAT, Roboflow) and training frameworks (MMDetection, Detectron2).
- **Default JSON** — tool-native format for round-tripping annotations back into Smart Labeler.

### SAM3 and SAHI

SAM3 (Segment Anything Model 3) runs as an external microservice called synchronously from the annotation canvas. SAHI (Slicing Aided Hyper Inference) partitions large images into overlapping tiles before inference, then merges results — significantly improving recall for small or densely packed objects.

### Tapis Integration

The segmentation pipeline leverages the Tapis Files API for all remote file I/O, keeping image data and annotation outputs on the user's allocated HPC storage. The Upload Data modal on the dashboard provides a direct path to stage local data to any Tapis-connected system before annotation begins.
