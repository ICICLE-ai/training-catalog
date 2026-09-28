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
| **2. Store / retrieve** | `icicleaivecserver` | `POST /v1/embeddings`, `POST /v1/retrieve`, `POST /v1/rerank`, `GET`/`DELETE /v1/collections` | FastAPI + Qdrant; private per-user collections, cosine search, and MMR / cosine-rescore / cross-encoder reranking. |
| **3. Chat** | `litellm` | `POST /v1/chat/completions` | OpenAI-compatible proxy on the `tacc` tenant. Generates the answer, and runs the G-Eval judge. |

Every request carries the same `X-Tapis-Token` (sent as both header and cookie), so authenticating once unlocks the whole pipeline — **including MLflow**, which is a Tapis-gated pod rather than a separate credential.

Note the two tenants: embed and vector are on `icicleai`, LiteLLM is on `tacc`. The notebook checks both when you validate and reports them separately, because a token can be good for one and not the other. A token that works for embed but not LiteLLM can still ingest.

## Why marimo?

marimo gives a reactive, code-first notebook with first-class UI widgets (`mo.ui.text`, `mo.ui.chat`, `mo.ui.run_button`) and an "app mode" that hides cells — useful for handing the notebook to non-developers without exposing the implementation. Reactivity also means the validation, ingestion, and chat cells re-evaluate cleanly whenever the token or ingest state changes.

## Design choices worth knowing

- **Validate before ingest.** The token cell hits `/v1/model` once and only unlocks downstream cells on a 200. This catches expired or wrong-tenant tokens before any embedding API spend.
- **Token-budget chunking.** A naive word-split with configurable max/overlap. Good enough for demo content; swap in `tiktoken` or a recursive splitter for production-grade ingestion.
- **Source metadata is stored alongside vectors.** `doc_id`, `chunk_index`, `chunk_count`, and a free-form `source` label travel with each vector so retrieval results stay traceable.
- **Reranking is a shortlist, not a second search.** The service retrieves `max(20, 5 × top-K)` candidates once and reorders them. That is enough headroom for reranking to change the answer, and small enough that the cross-encoder — one model pass per candidate — stays quick on CPU.
- **The chat is scoped to a collection you pick, not to this session's ingest.** Collections persist on the vector service, so a returning user picks one and starts asking. Each answer records the collection and topic it actually searched.
- **Chats live only in the browser session.** Nothing server-side stores the conversation in this release, which is why the export button sits right under the chat.
- **Retrieved chunks are echoed under every answer** in a collapsible `<details>` block — the demo prioritizes legibility/auditability over a polished chat surface.
- **The pad batches questions behind a confirmation gate.** It is deliberately not a chat box: questions accumulate while you read, and the send is a two-step action so a stray click can't spend API calls.
- **The chat surface is hand-rolled rather than `mo.ui.chat`.** That widget owns its history on the frontend with no Python-side injection, so batched questions could never join its conversation. Keeping history in `mo.state` gives one shared conversation, makes the Study mode switch a free re-render, and allows multi-turn memory.
- **Answer evaluation is experimental and follows the G-Eval baseline.** The judge uses the structure from the G-Eval paper: a task introduction, the scoring criteria, evaluation steps the judge writes itself, then a score. The evaluation steps depend only on the criteria, so they are generated once per session and reused, as in the paper. G-Eval also weights each score by the probability of the score token. The notebook does this when the model returns token probabilities (`logprobs`), giving scores such as `4.28`, and otherwise uses the whole-number score the judge wrote. The `geval_mode` tag records which method was used. The evaluation can be customized: the judge model is set with `ICICLE_JUDGE_MODEL` or in the app, and the criteria for each dimension are defined in `GEVAL_DIMENSIONS` in the notebook.
- **Each dimension is judged only on the inputs it needs.** Context relevance is scored without the answer, so it measures retrieval alone and a well-written answer cannot hide poorly retrieved passages.
- **MLflow is used to monitor answer quality and retrieval over time.** Metrics are sent through MLflow's REST API, the same approach as `icicle-ai-embed-service`, so the full `mlflow` package is not needed. Traces use the smaller `mlflow-tracing` package (about 5 MB, compared with about 1 GB for full MLflow). Each request is authenticated with the user's own Tapis token, so no separate service account is required.
- **Evaluation never blocks an answer.** If the judge fails, returns an unreadable score, MLflow is unreachable or the token has expired, the error is recorded with that turn and the answer is still shown. Scoring runs in the background, so it does not slow down answers.
- **Conversation memory is capped and clearly demoted.** Only the last three turns go into the prompt, each answer truncated, and the block is labelled as being for resolving references only — the retrieved chunks stay the sole source of facts.

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
