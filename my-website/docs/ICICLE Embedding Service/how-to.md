---
tags:
  - CI4AI
  - AI4CI
  - Software
---
# How-To Guides

## Authentication

Every request (except `/healthz`) requires a valid **ICICLE AI tenant** Tapis access token in the `X-Tapis-Token` header. The service:

- Verifies the JWT signature via JWKS
- Checks the token is not expired
- Validates the issuer matches `TAPIS_ISSUER`
- Ensures `tapis/token_type` is `access`
- Ensures `tapis/tenant_id` is `icicleai`
- Extracts `tapis/username` for per-request logging

### How to get your access token

Log in to the [ICICLEaaS Portal](https://icicleai.tapis.io), click your username in the bottom-left corner, and select **Copy Access Token**.


| Scenario                   | Status | Response                                                                        |
| -------------------------- | ------ | ------------------------------------------------------------------------------- |
| No `X-Tapis-Token` header  | `422`  | `"field required"`                                                              |
| Expired token              | `401`  | `"Token has expired. Please obtain a fresh access token."`                      |
| Wrong issuer               | `401`  | `"Invalid token issuer. Expected issuer: ..."`                                  |
| Non-access token           | `401`  | `"Only Tapis access tokens are accepted..."`                                    |
| Wrong tenant (e.g. `tacc`) | `403`  | `"Access denied. This service only accepts tokens from the 'icicleai' tenant."` |
| Invalid/malformed token    | `401`  | `"Token validation failed. Ensure you are sending a valid Tapis access token."` |


## How to Embed a Document

Documents are embedded as-is — Qwen3-Embedding's instruction template is **not** applied, because the document side of an asymmetric retrieval pair shouldn't carry a query prompt.

```bash
curl -X POST http://localhost:8001/v1/embed \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Photosynthesis is the process by which green plants convert light into chemical energy.",
    "input_type": "document"
  }'
```

Response (`200`):

```json
{
  "model": "Qwen/Qwen3-Embedding-0.6B-GGUF/Qwen3-Embedding-0.6B-Q8_0.gguf",
  "dim": 1024,
  "input_type": "document",
  "normalized": true,
  "data": [
    { "index": 0, "embedding": [0.021, -0.084, "..."] }
  ]
}
```

## How to Embed a Query

For queries, set `input_type: "query"` so the service wraps the text with the Qwen3 retrieval-instruction template before embedding. This materially improves retrieval quality against documents embedded without the template.

```bash
curl -X POST http://localhost:8001/v1/embed \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "how do plants make food",
    "input_type": "query"
  }'
```

## How to Use a Custom Instruction

For non-retrieval tasks (clustering, classification, code search), override the default instruction. It only takes effect when `input_type="query"`.

```json
{
  "input": "how do plants make food",
  "input_type": "query",
  "instruction": "Given a biology question, retrieve passages that contain the answer"
}
```

## How to Batch Embed

Pass a list. Inputs are embedded serially against the shared llama.cpp context and returned in the same order.

```bash
curl -X POST http://localhost:8001/v1/embed \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      "first chunk of text",
      "second chunk of text",
      "third chunk of text"
    ],
    "input_type": "document"
  }'
```

The list is capped at `MAX_INPUTS_PER_REQUEST` items, and each string at `MAX_CHARS_PER_INPUT` characters. Oversized requests are rejected with `422` before the embedder is invoked.

## How to Use the Embedding with the Vector Service

The same Tapis token works against both services — embed here, store there.

```bash
# 1. Embed the passage
VEC=$(curl -s -X POST http://localhost:8001/v1/embed \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input":"Photosynthesis...","input_type":"document"}' \
  | jq -c '.data[0].embedding')

# 2. Store it in the vector service
curl -X POST http://localhost:8000/v1/embeddings \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"embedding\": $VEC,
    \"collection\": \"biology\",
    \"topic\": \"plant\",
    \"chunks\": [\"Photosynthesis...\"],
    \"embedding_model\": \"Qwen3-Embedding-0.6B-Q8_0\"
  }"
```

For retrieval, embed the query with `input_type: "query"` and POST the resulting vector to `/v1/retrieve` on the vector service.

## How to Pick a Quant

All files live in [`Qwen/Qwen3-Embedding-0.6B-GGUF`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF). Drop the filename into `MODEL_FILE`.


| File                              | Size    | RAM     | Quality vs fp16 | When to use                                       |
| --------------------------------- | ------- | ------- | --------------- | ------------------------------------------------- |
| `Qwen3-Embedding-0.6B-Q8_0.gguf`  | ~650 MB | ~800 MB | ~99.9%          | Default. Tight fidelity, low memory.              |
| `Qwen3-Embedding-0.6B-f16.gguf`   | ~1.2 GB | ~1.5 GB | 100%            | Reference / benchmarking.                         |


For larger Qwen variants, swap `MODEL_REPO` to `Qwen/Qwen3-Embedding-4B-GGUF` (dim 2560) or `Qwen/Qwen3-Embedding-8B-GGUF` (dim 4096) and pick a matching quant file.

## Troubleshooting

- **"Failed to initialise embedder" at startup**: the service exits if it can't load the model. Check `MODEL_PATH` (file exists?) or that you have network access to Hugging Face on first boot.
- **`401`/`403` errors**: ensure your Tapis token is fresh, from the `icicleai` tenant, and passed via the `X-Tapis-Token` header.
- **`422` "input list exceeds max_inputs_per_request"**: split the request, or raise `MAX_INPUTS_PER_REQUEST` if your deployment can absorb it.
- **`422` "input exceeds max_chars_per_input"**: chunk the text on the client; this service does no chunking.
- **Slow first request**: model load happens at startup, but the first embedding triggers JIT compilation of the compute graph. Subsequent requests are much faster.
- **High RAM**: lower `N_CTX` (e.g. `2048`) or move from f16 to Q8_0.
- **No GPU acceleration on Mac**: confirm `llama-cpp-python` was installed on Apple Silicon Python, not under Rosetta. `python -c "import platform; print(platform.machine())"` should print `arm64`.
