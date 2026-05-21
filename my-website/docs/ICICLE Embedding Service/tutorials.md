---
tags:
  - CI4AI
  - AI4CI
  - Software
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
| `N_THREADS`              | no       | CPU threads. `0` = let llama.cpp pick.                                                               |
| `N_GPU_LAYERS`           | no       | Layers to offload to GPU. `-1` = all (default), `0` = pure CPU. On macOS this enables Metal.         |
| `N_BATCH`                | no       | Compute-graph batch size. Default `512`.                                                             |
| `MAX_INPUTS_PER_REQUEST` | no       | DOS guard. Cap on the number of strings per `/v1/embed` call. Default `256`.                        |
| `MAX_CHARS_PER_INPUT`    | no       | DOS guard. Cap on length of any single input string. Default `200000`.                              |
| `TAPIS_ISSUER`           | no       | JWT issuer to validate. Defaults to `https://icicleai.tapis.io/v3/tokens`.                           |
| `TAPIS_JWKS_URL`         | no       | JWKS endpoint for token signature verification. Defaults to ICICLE's JWKS endpoint.                  |
| `TAPIS_TENANT_ID`        | no       | Allowed Tapis tenant. Defaults to `icicleai`.                                                        |
| `APP_ENV`                | no       | `dev` or `prod`.                                                                                     |
| `ALLOWED_ORIGINS`        | no       | JSON array of CORS origins. Defaults to `["*"]`.                                                     |


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
