---
tags:
  - AI4CI
  - Software
---
# Explanation

## What the playground does

The notebook is a thin client over three ICICLE Tapis services, glued together behind one access token. Each chat turn runs the full RAG loop:

| Step | Service | Endpoint | What happens |
| --- | --- | --- | --- |
| **1. Embed** | `icicleaiembedserver` | `POST /v1/embed` | Text → 1024-dim normalized vector (Qwen3-Embedding via `llama-cpp-python`). |
| **2. Store / retrieve** | `icicleaivecserver` | `POST /v1/embeddings`, `POST /v1/retrieve` | FastAPI + Qdrant; cosine similarity with MMR reranking. |
| **3. Chat** | `tapisagent` | `POST /chat` | Generates the final answer from the retrieved chunks. |

Every request carries the same `X-Tapis-Token` (sent as both header and cookie), so authenticating once unlocks the whole pipeline.

## Why marimo?

marimo gives a reactive, code-first notebook with first-class UI widgets (`mo.ui.text`, `mo.ui.chat`, `mo.ui.run_button`) and an "app mode" that hides cells — useful for handing the notebook to non-developers without exposing the implementation. Reactivity also means the validation, ingestion, and chat cells re-evaluate cleanly whenever the token or ingest state changes.

## Design choices worth knowing

- **Validate before ingest.** The token cell hits `/v1/model` once and only unlocks downstream cells on a 200. This catches expired or wrong-tenant tokens before any embedding API spend.
- **Token-budget chunking.** A naive word-split with configurable max/overlap. Good enough for demo content; swap in `tiktoken` or a recursive splitter for production-grade ingestion.
- **Source metadata is stored alongside vectors.** `doc_id`, `chunk_index`, `chunk_count`, and a free-form `source` label travel with each vector so retrieval results stay traceable.
- **Retrieved chunks are echoed under every answer** in a collapsible `<details>` block — the demo prioritizes legibility/auditability over a polished chat surface.

## Project layout

```
icicle-chatbook/
├── assets/                  # Images referenced by the notebook (logo, screenshot)
├── notebooks/
│   └── rag_chat_marimo.py   # The marimo notebook
├── pyproject.toml           # uv-managed project metadata + deps
├── uv.lock                  # Pinned dependency lockfile
└── README.md
```
