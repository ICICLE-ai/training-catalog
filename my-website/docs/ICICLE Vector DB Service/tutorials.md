---
tags:
  - CI4AI
  - AI4CI
  - Software
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
# {"status": "ok"}
```
