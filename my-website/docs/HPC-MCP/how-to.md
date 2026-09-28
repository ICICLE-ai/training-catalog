---
tags:
  - Software
  - AI4CI
title: "HPC-MCP: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for HPC-MCP. HPC-MCP is a service-based ICICLE software component that gives HPC users a natural-language interface to backend HPC utilities."
---
# How-To Guides

## Connect an MCP Client

Claude Code or another MCP client can connect through HTTP transport:

```bash
claude mcp add hpc-mcp-server --transport http https://hpcmcpservercpu.pods.icicleai.tapis.io/mcp
```

The service exposes two MCP tools:

- `chat`
- `predict_gpu_time`

To verify MCP initialization and tool discovery with MCP Inspector:

```bash
npx --yes --package @modelcontextprotocol/inspector -- \
  mcp-inspector --cli \
  https://hpcmcpservercpu.pods.icicleai.tapis.io/mcp \
  --transport http \
  --method tools/list
```

Set `MCP_PUBLIC_HOST` when deploying the service under a different public hostname.

## Use the HTTP API

Main endpoints:

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health check |
| `GET` | `/` | Service metadata |
| `GET` | `/about` | HTML service overview |
| `POST` | `/chat` | Natural-language chat with tool routing |
| `POST` | `/predict-gpu-time` | Direct distributed training-time prediction |
| `POST` | `/mcp` | MCP Streamable HTTP endpoint |

### `POST /predict-gpu-time`

Request:

```json
{
  "system": "vista"
}
```

Response:

```json
{
  "response": "...",
  "system": "vista",
  "config_path": "/app/vendor/distributed_training_estimator/Estimator/target_config/llemma_7b_4_2_2_V.yml"
}
```

Optional request field:

```json
{
  "system": "vista",
  "config_name": "llemma_7b_4_2_2_V.yml"
}
```

### `POST /chat`

Request:

```json
{
  "prompt": "Predict training time on Vista. Answer with microseconds and seconds.",
  "max_new_tokens": 120
}
```

Response:

```json
{
  "response": "..."
}
```

## Deploy with Tapis Pods

A working Tapis Pod configuration example is provided in:

```text
tapis-pod.example.json
```

Current deployment:

| Field | Value |
| --- | --- |
| Pod ID | `hpcmcpservercpu` |
| Base URL | `https://hpcmcpservercpu.pods.icicleai.tapis.io` |
| Container image | `ghcr.io/icicle-ai/hpc-mcp-server-cpu:0.1.0` |
| Release format | Service-only Tapis Pod deployment with source code in GitHub |
| ICICLEaaS category | AI-as-a-Service |

Environment variables:

```text
PORT=8000
LLM_BACKEND=transformers
MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct
HF_HOME=/models/.cache/huggingface
HF_LOCAL_FILES_ONLY=false
TORCH_DTYPE=float32
ESTIMATOR_DIR=/app/vendor/distributed_training_estimator/Estimator
GPU_MODEL_TIMEOUT_SECONDS=300
```

Optional CPU demo setting:

```text
TOOL_DECISION_MAX_NEW_TOKENS=8
```

If `MODEL_ID` is a local path, download the model to that path inside the pod before calling `/chat`. For production deployments, use a persistent Tapis volume for model storage.

## Run Locally for Development

Local development prerequisites:

- Python 3.11.
- `uv`.
- Enough disk space for Python dependencies, model files, and estimator assets.

Install dependencies:

```bash
uv sync --locked
```

Run the service locally:

```bash
export LLM_BACKEND=transformers
export MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct
export TORCH_DTYPE=float32
export HF_HOME=/tmp/huggingface
export ESTIMATOR_DIR=vendor/distributed_training_estimator/Estimator

uv run uvicorn hpc_mcp_server_cpu.main:app --host 127.0.0.1 --port 8000
```

Run tests:

```bash
uv run python -m unittest tests/test_mcp_transport.py
```

## Troubleshooting

If `/health` works but `/chat` fails with a model path error, check whether the configured model path exists inside the pod.

If `/chat` is slow on a CPU-only pod, use `/predict-gpu-time` for direct estimator calls or reduce `max_new_tokens` in the chat request.

If MCP clients reject the connection after redeployment under a new hostname, set `MCP_PUBLIC_HOST` to the public host and configure `MCP_ALLOWED_HOSTS` and `MCP_ALLOWED_ORIGINS` as needed.

If `curl` examples fail, make sure the JSON field is written as `max_new_tokens`, not `max\_new\_tokens`.
