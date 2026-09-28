---
tags:
  - CI4AI
  - AI4CI
  - Software
title: "ICICLE Embedding Service: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for ICICLE Embedding Service. FastAPI service that turns text into embedding vectors using Qwen3-Embedding-0.6B (GGUF quantized) via…"
---
# Tutorials

## Quickstart

### Prerequisites

- Python 3.11+
- A C/C++ toolchain and `cmake` (Xcode CLT on macOS: `xcode-select --install`; `build-essential cmake` on Debian/Ubuntu) — `llama-cpp-python` builds a native extension
- ~700 MB free disk for the default Q8_0 quant
- A valid ICICLE AI Tapis access token

### Step 1: Configure Environment

```bash
cp .env.example .env
```


| Variable                 | Required | Description                                                                                          |
| ------------------------ | -------- | ---------------------------------------------------------------------------------------------------- |
| `MODEL_PATH`             | no       | Absolute path to a local `.gguf` file. If set, overrides the Hugging Face download.                  |
| `MODEL_REPO`             | no       | Hugging Face repo id. Default `Qwen/Qwen3-Embedding-0.6B-GGUF`.                                      |
| `MODEL_FILE`             | no       | Quant file inside the repo. Default `Qwen3-Embedding-0.6B-Q8_0.gguf`.                                |
| `N_CTX`                  | no       | Context window in tokens. Default `8192`. Model max is `32768`.                                      |
| `N_THREADS`              | no       | CPU threads per worker, used for both generation and batch (prompt) processing. `0` = let llama.cpp pick. In containers, set it to the CPU limit; llama.cpp otherwise sees the host's cores. |
| `N_GPU_LAYERS`           | no       | Layers to offload to GPU. `-1` = all (default), `0` = pure CPU. On macOS this enables Metal.         |
| `N_BATCH`                | no       | Compute-graph batch size. Default `512`.                                                             |
| `MAX_INPUTS_PER_REQUEST` | no       | DOS guard. Cap on the number of strings per `/v1/embed` call. Default `256`.                        |
| `MAX_CHARS_PER_INPUT`    | no       | DOS guard. Cap on length of any single input string. Default `200000`.                              |
| `TAPIS_ISSUER`           | no       | JWT issuer to validate. Defaults to `https://icicleai.tapis.io/v3/tokens`.                           |
| `TAPIS_JWKS_URL`         | no       | JWKS endpoint for token signature verification. Defaults to ICICLE's JWKS endpoint.                  |
| `TAPIS_TENANT_ID`        | no       | Allowed Tapis tenant. Defaults to `icicleai`.                                                        |
| `APP_ENV`                | no       | `dev` or `prod`.                                                                                     |
| `ALLOWED_ORIGINS`        | no       | JSON array of CORS origins. Defaults to `["*"]`.                                                     |
| `CACHE_ENABLED`          | no       | Enable the Redis query-embedding cache. Default `true`. Fail-open — if Redis is down, embedding still works. |
| `REDIS_URL`              | no       | Redis connection URL. Default `redis://localhost:6379/0`.                                            |
| `REDIS_TIMEOUT_SECONDS`  | no       | Redis connect/command timeout (s). Default `0.5`, short so a slow cache can't stall a request.       |
| `CACHE_TTL_SECONDS`      | no       | TTL for cached vectors. Default `2592000` (30 days). LRU eviction is the real bound.                 |
| `CACHE_KEY_PREFIX`       | no       | Cache key prefix. Bump to invalidate the whole cache (e.g. after a model change). Default `emb:v1:`. |
| `REDIS_MAXMEMORY`        | no       | Redis memory budget (e.g. `800mb`). Blank = let the Redis/pod config own it.                         |
| `REDIS_MAXMEMORY_POLICY` | no       | Eviction policy when `maxmemory` is hit. Default `allkeys-lru`.                                       |
| `MLFLOW_ENABLED`         | no       | Log anonymous per-request metrics to MLflow. Default `false`. Fail-open — if MLflow is down, embedding still works. |
| `MLFLOW_TRACKING_URI`    | no       | MLflow server URL. Required when `MLFLOW_ENABLED=true`.                                              |
| `MLFLOW_EXPERIMENT`      | no       | MLflow experiment name. Default `icicle-ai-embed-service`.                                           |
| `MLFLOW_TIMEOUT_SECONDS` | no       | Timeout (s) for each MLflow call. Default `2.0`.                                                     |


### Step 2: Install and Run

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8001
```

First boot downloads the GGUF from Hugging Face (cached under `~/.cache/huggingface`). Subsequent boots load from cache in seconds.

### Step 3: Verify

```bash
curl http://localhost:8001/healthz
# {"status": "ok"}
```
