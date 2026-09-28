---
tags:
  - Software
  - AI4CI
---
# Tutorials

## Tutorial: Test the Deployed Training-Time Prediction Service

This tutorial shows how to check the deployed HPC-MCP service and request distributed LLM training-time predictions for Vista and Perlmutter.

### Prerequisites

- Network access to the ICICLE Tapis Pod endpoint.
- A terminal with `curl`.
- 5 minutes to test the deployed HTTP service.

### Step 1: Set the Service URL

```bash
export HPC_MCP_URL=https://hpcmcpservercpu.pods.icicleai.tapis.io
```

### Step 2: Check Service Health

```bash
curl "$HPC_MCP_URL/health"
```

Expected response shape:

```json
{
  "status": "ok",
  "service": "hpc-mcp-server-cpu",
  "version": "0.1.0"
}
```

### Step 3: Request a Vista Prediction

```bash
curl --http1.1 --max-time 180 "$HPC_MCP_URL/predict-gpu-time" \
  -H "Content-Type: application/json" \
  --data-raw '{"system":"vista"}'
```

### Step 4: Request a Perlmutter Prediction

```bash
curl --http1.1 --max-time 180 "$HPC_MCP_URL/predict-gpu-time" \
  -H "Content-Type: application/json" \
  --data-raw '{"system":"perlmutter"}'
```

Supported `system` values:

- `vista`
- `perlmutter`

Common misspellings such as `permutter` and `permultter` are also accepted.

The response includes the selected system, estimator configuration path, and estimator output.

### Step 5: Ask Through Natural Language

Users can also request predictions through the `/chat` endpoint:

```bash
curl --http1.1 --max-time 180 "$HPC_MCP_URL/chat" \
  -H "Content-Type: application/json" \
  --data-raw '{"prompt":"Predict training time on Vista. Answer with microseconds and seconds.","max_new_tokens":120}'
```

Expected response shape:

```json
{
  "response": "System: vista\nConfig: /app/vendor/distributed_training_estimator/Estimator/target_config/llemma_7b_4_2_2_V.yml\nEstimated timecost: 4764606.22498043 us (4.765 seconds)."
}
```

The `/chat` endpoint loads the configured LLM backend. On CPU-only pods, responses can be slower than direct calls to `/predict-gpu-time`.
