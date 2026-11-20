---
tags:
  - Software
  - AI4CI
title: "HARP UI: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for HARP UI. HARP profiles scientific applications across high-performance computing (HPC) systems, builds regression models from the resulting…"
---
# Explanation

## Why HARP

Each HPC workflow has its own compute, memory and I/O profile, and users routinely over- or under-request resources because they lack a history of runs to go by. HARP generates that history systematically, with many "scaled-down" (SD) runs, a few selective "full-scale" (FS) runs and held-out test_data runs, then trains regression models to estimate runtime for a target application on a given system and queue.

## From notebooks to the UI

Earlier versions ran the whole Cheetah campaign inside **one** container, so one Tapis job ran every sweep combination on one machine, driven from a notebook or an installed module. HARP UI keeps the same pipeline and data format but changes how the generate phase runs:

```
 Browser UI ──► HARP server ──► Tapis Jobs ──► job on system A ─┐
  (Generate,     expand combos,   (one job      job on system B ─┼─► harp_profile.csv per job
   Build,        split into jobs,  per chunk)   job on system C ─┘
   Estimate)     throttle, poll  ◄── Tapis Files: merge ──► <storage>/<campaign>/<app>_<timestamp>.csv
```

- **Split** spreads jobs round-robin over the selected systems; **replicate** runs every job on every system to profile across hardware.
- Each job's hardware comes from its queue (cores, memory, walltime) and is checked against the queue's Tapis limits before submission.
- The server respects each system's concurrent-job limit, reads live progress through Tapis Files, and merges CSVs when every job ends. Failed runs go to `harp_failures.csv`, so they never pollute training data.
- The merged CSV keeps the pipeline's columns (`run_config, run_type, sys_*, run_<param>, walltime`), so the existing build modules (`pipeline/modules/pipeline.py`: preprocessing with outlier removal, scaling and PCA, then model training) consume it unchanged.

## The three tabs

| Tab | Steps |
|---|---|
| **HARP Generate** | Configure sweeps → Review & submit → Jobs → Profiled data |
| **HARP Build** | Training data → Models & where → Trained models |
| **HARP Estimate** | Configure → Select model → Estimates |

The **?** buttons in the UI explain each term: SD / FS / test_data runs, sweeps and campaigns, models, training sets, and how models are scored (average error and how often a model predicts too low on test_data runs).

## Security and multi-user isolation

- HARP accepts Tapis access tokens only, never usernames or passwords. The token stays on the server; the browser gets an HttpOnly session cookie that JavaScript cannot read.
- Inside TapisUI, the iframe receives the token from its exact parent origin via `postMessage`. Tokens are never placed in URLs or browser storage.
- Every sweep, job, dataset and build belongs to the Tapis user **and** tenant that created it, and is read through that user's own token.
- When a token expires, running sweeps pause (`WAITING_FOR_LOGIN`) and resume once the user signs in again. Campaign state is stored as JSON, so it survives server restarts.

## Repository layout

| Path | Contents |
|---|---|
| [`profiling.html`](https://github.com/ICICLE-ai/HARP-UI/blob/main/profiling.html) | The single-page UI |
| [`harp_server/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/harp_server) | FastAPI server: plan, sweep, campaign tracking, Tapis gateway, builds, tests |
| [`job_runner/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/job_runner) | Code that runs inside profiling and build jobs |
| [`pipeline/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/pipeline) | HARP data preprocessing and model training modules |
| [`DockerFiles/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/DockerFiles) | Sweep, build and legacy HARP container definitions |
| [`deploy/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/deploy) | Tapis Pods templates and deployment script |
| [`Notebooks/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/Notebooks) | Tapis system/app registration notebooks |
| [`examples/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/examples) | Euler number and YOLO target applications |
| [`DEMO/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/DEMO) | Offline UI demo and screenshots |
| [`cheetah/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/cheetah), [`install-script-source/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/install-script-source), [`Post_Execution_Scripts/`](https://github.com/ICICLE-ai/HARP-UI/blob/main/Post_Execution_Scripts) | Used by the legacy container and module workflows |

## Supported systems

HARP UI runs jobs on any Tapis-registered execution system you have credentials and an allocation for. It has been used with OSC (Pitzer, Owens) and TACC systems, on CPU and GPU queues (GPU queues get `--nv` automatically).
