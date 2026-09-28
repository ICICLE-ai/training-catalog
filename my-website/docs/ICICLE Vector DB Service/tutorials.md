---
tags:
  - CI4AI
  - AI4CI
  - Software
title: "ICICLE Vector DB Service: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for ICICLE Vector DB Service. FastAPI + Qdrant vector storage and retrieval service for the ICICLE AI Tapis tenant."
---
# Tutorials

## Quickstart

### Prerequisites

- Python 3.13+
- Docker (for local Qdrant)
- A valid ICICLE AI Tapis access token

### Step 1: Start Qdrant

```bash
docker run --name qdrant -p 6333:6333 -p 6334:6334 -d qdrant/qdrant
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```


| Variable          | Required | Description                                                    |
| ----------------- | -------- | -------------------------------------------------------------- |
| `QDRANT_URL`      | yes      | Qdrant server URL (append `:443` if behind HTTPS proxy)        |
| `QDRANT_API_KEY`  | no       | Qdrant API key (if auth is enabled)                            |
| `APP_ENV`         | no       | `dev` or `prod`                                                |
| `TAPIS_ISSUER`    | yes      | JWT issuer to validate (`https://icicleai.tapis.io/v3/tokens`) |
| `TAPIS_JWKS_URL`  | yes      | JWKS endpoint for token signature verification                 |
| `TAPIS_TENANT_ID` | yes      | Allowed Tapis tenant (`icicleai`)                              |
| `ALLOWED_ORIGINS` | no       | JSON array of CORS origins. Defaults to `["*"]` (allow all).   |
| `DROP_EMPTY_COLLECTIONS` | no | `true` lets an emptied collection be dropped. Defaults to `false`; see [How User Isolation Works](#how-user-isolation-works). |

**Cross-encoder reranking** (all optional — the service runs fine without them):


| Variable                 | Default                                                          | Description                                                            |
| ------------------------ | ---------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `RERANK_MODEL`           | `BAAI/bge-reranker-base`                                         | Model used when a request does not name one                            |
| `RERANK_ALLOWED_MODELS`  | `["BAAI/bge-reranker-base","cross-encoder/ms-marco-MiniLM-L-6-v2"]` | JSON array. A request may only select a model from this list           |
| `RERANK_PRELOAD`         | `false`                                                          | Load the default model at startup instead of on first use              |
| `RERANK_THREADS`         | `0`                                                              | Torch intra-op threads. **Set this explicitly.** `0` lets torch read `nproc`, which in a container reports the *host's* CPU count, not the cgroup quota — oversubscribing threads and causing heavy throttling. Match it to the pod's actual CPU limit. |
| `RERANK_MAX_CANDIDATES`  | `128`                                                            | Hard cap on candidates scored per request                              |
| `RERANK_MAX_LENGTH`      | `512`                                                            | Token truncation length for each (query, passage) pair                 |



### Step 3: Install and Run

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Verify

```bash
curl http://localhost:8000/healthz
# {"status":"ok","version":"1.0.0","qdrant":"ok","cross_encoder":true}
```

`cross_encoder` reports whether cross-encoder reranking is available.

### Step 5 (optional): Enable cross-encoder reranking

Cross-encoder reranking needs PyTorch, which is not installed by default:

```bash
uv pip install -e ".[rerank]" --extra-index-url https://download.pytorch.org/whl/cpu
```

The CPU wheel index matters: the default PyPI `torch` wheel bundles roughly
2.5GB of CUDA libraries that are dead weight on a CPU-only deployment.
