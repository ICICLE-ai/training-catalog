---
tags:
  - CI4AI
  - AI4CI
  - Software
---
# Explanation

## Pipeline Architecture

Smart Labeler is structured as a linear 7-step pipeline where each step produces outputs consumed by the next. The pipeline state is persisted in a PostgreSQL database and files are stored on Tapis-connected HPC filesystems, so work is never lost between sessions.

```
Step 1: Annotate          → ground-truth bounding boxes (COCO JSON)
Step 2: Class Supports    → embedding tensors per object class (.npz)
Step 3: Patch Optimizer   → optimal crop size for the dataset
Step 4: Detection Config  → detection job configuration snapshot
Step 5: Proposals         → raw object proposals + optimal objectness threshold
Step 6: Classification    → maps proposals to class supports, submits job
Step 7: Results           → final labeled detections, ready to export
```

## Few-Shot Detection Approach

Rather than fine-tuning a model from scratch, Smart Labeler uses a **few-shot, embedding-based** approach:

1. **Class supports** are embedding vectors extracted from annotated examples of each object class.
2. A **proposer model** (e.g., SAM3, OWLv2) generates candidate bounding boxes across the query images.
3. An **embedder model** (e.g., DINOv3, BioClip) embeds each proposal crop.
4. Proposals are **matched against class supports** by cosine similarity — no per-dataset retraining required.

This makes the pipeline domain-agnostic: the same workflow applies to wildlife camera traps, satellite imagery, microscopy slides, or any other image dataset.

## Tapis Integration

All compute-intensive steps run as **Tapis v3 batch jobs** on HPC clusters. Smart Labeler handles:

- Job definition and submission via the Tapis API
- Real-time status polling surfaced in the pipeline status bar
- Secure credential injection (Hugging Face tokens via Tapis Vault)
- File I/O through the Tapis Files API, keeping all data on the user's allocated storage

## SAM3 Inference Service

SAM3 (Segment Anything Model 3) runs as an **external microservice** separate from the HPC jobs. It is called synchronously during interactive annotation in Step 1. Two modes are supported:

- **Single Click** — user clicks a point on an object; SAM3 returns a bounding box.
- **Text Prompt** — user provides class names; SAM3 runs open-vocabulary detection across the full image.

Both modes optionally apply **SAHI tiling**, which partitions the image into overlapping crops before inference and merges the results — significantly improving recall for small or dense objects.

## Patra Model Registry

Proposer and embedder models are selected from the live **ICICLE AI Patra** model catalog. This means new models can be added to the catalog without any changes to Smart Labeler itself. Full model cards are accessible in-app via the info icon next to each model entry.
