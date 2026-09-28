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
- Ensures `tapis/tenant_id` is `icicleai`
- Extracts `tapis/username` for per-user data isolation

### How to get your access token

Log in to the [ICICLE AI Tapis UI](https://icicleai.tapis.io), click your username in the bottom-left corner, and select **Copy Access Token**.

![Getting your Tapis access token](https://raw.githubusercontent.com/ICICLE-ai/icicle-ai-vector-service/main/docs/images/tapis-access-token.png)


| Scenario                   | Status | Response                                                                        |
| -------------------------- | ------ | ------------------------------------------------------------------------------- |
| No `X-Tapis-Token` header  | `422`  | `"field required"`                                                              |
| Expired token              | `401`  | `"The access token has expired."`                                               |
| Wrong issuer               | `401`  | `"Invalid token issuer. Expected: ..."`                                         |
| Wrong tenant (e.g. `tacc`) | `403`  | `"Access denied. This service accepts tokens from the 'icicleai' tenant only."` |
| Invalid/malformed token    | `401`  | `"The access token could not be validated."`                                    |


## How to Store an Embedding

`collection` (required) is the broad domain. `topic` (optional) is a sub-category within it.

```bash
curl -X POST http://localhost:8000/v1/embeddings \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "embedding": [0.12, -0.34, ...],
    "collection": "biology",
    "topic": "plant",
    "chunks": ["Photosynthesis is the process by which green plants..."],
    "metadata": {"source": "biology_notes.pdf", "page": 1},
    "embedding_model": "gemini-embedding-001"
  }'
```

Response (`201`):

```json
{
  "id": "abc-123-def",
  "user_id": "thevyasamit",
  "collection": "biology",
  "topic": "plant",
  "created_at": "2026-04-03T10:30:00+00:00",
  "updated_at": "2026-04-03T10:30:00+00:00",
  "embedding_model": "gemini-embedding-001"
}
```

Without a topic (stored at the collection level):

```bash
curl -X POST http://localhost:8000/v1/embeddings \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "embedding": [0.12, -0.34, ...],
    "collection": "biology",
    "chunks": ["General biology overview..."],
    "embedding_model": "gemini-embedding-001"
  }'
```

## How to Search Embeddings

`collection` is required — it tells the service which Qdrant collection to search. `topic` is optional — it narrows results to a sub-category.

**Search entire collection:**

```bash
curl -X POST http://localhost:8000/v1/retrieve \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query_embedding": [0.12, -0.34, ...],
    "top_k": 5,
    "collection": "biology"
  }'
```

**Search within a specific topic:**

```bash
curl -X POST http://localhost:8000/v1/retrieve \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query_embedding": [0.12, -0.34, ...],
    "top_k": 5,
    "collection": "biology",
    "topic": "plant"
  }'
```

**Combine topic + metadata filter:**

```json
{
  "query_embedding": [0.12, -0.34, "..."],
  "top_k": 5,
  "collection": "biology",
  "topic": "plant",
  "filter": {
    "conditions": {"source": "biology_notes.pdf"}
  }
}
```

**Match any of several metadata values:**

```json
{
  "query_embedding": [0.12, -0.34, "..."],
  "top_k": 10,
  "collection": "biology",
  "filter": {
    "conditions": {"source": ["bio_notes.pdf", "plant_guide.pdf"]}
  }
}
```

Response:

```json
{
  "user_id": "thevyasamit",
  "top_k": 5,
  "results": [
    {
      "id": "abc-123-def",
      "score": 0.94,
      "collection": "biology",
      "topic": "plant",
      "text": null,
      "chunks": ["Photosynthesis is the process by which green plants..."],
      "metadata": {"source": "biology_notes.pdf", "page": 1}
    }
  ]
}
```

## How to Update an Embedding

Partial update — `collection` query param tells the service where to find the embedding. Send any combination of fields to update in the body.

```bash
curl -X PUT "http://localhost:8000/v1/embeddings/abc-123-def?collection=biology" \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "molecular-biology",
    "metadata": {"source": "updated_notes.pdf", "page": 5}
  }'
```

Response (`200`):

```json
{
  "id": "abc-123-def",
  "user_id": "thevyasamit",
  "collection": "biology",
  "topic": "molecular-biology",
  "created_at": "2026-04-03T10:30:00+00:00",
  "updated_at": "2026-04-03T11:00:00+00:00",
  "embedding_model": "gemini-embedding-001"
}
```

## How to Delete an Embedding

`collection` query param tells the service where to find the embedding.

```bash
curl -X DELETE "http://localhost:8000/v1/embeddings/abc-123-def?collection=biology" \
  -H "X-Tapis-Token: $TAPIS_TOKEN"
```

Response (`200`):

```json
{
  "id": "abc-123-def",
  "user_id": "thevyasamit",
  "deleted": true
}
```

Returns `404` if the embedding is not found in the specified collection.

## How to Rerank Results

Reranking fetches a wider shortlist (`fetch_k`) from the vector index, then
reorders it down to `top_k`. Three methods are available — ask the service which
ones this deployment actually supports:

```bash
curl http://localhost:8000/v1/rerank/methods -H "X-Tapis-Token: $TAPIS_TOKEN"
```


| Method           | Reads passage text? | Needs `query_text`? | What it does                                                                  |
| ---------------- | ------------------- | ------------------- | ----------------------------------------------------------------------------- |
| `mmr`            | no                  | no                  | Trades relevance for diversity so near-duplicates don't fill the results       |
| `cosine_rescore` | no                  | no                  | Recomputes exact cosine similarity and re-sorts                                |
| `cross_encoder`  | **yes**             | **yes**             | Scores the real query against each passage with a transformer — true relevance |

Every response item carries both `score` (the original vector similarity) and
`rerank_score` (what the ordering is based on), so you can see what the reranker
changed.

### MMR — diversity

```bash
curl -X POST http://localhost:8000/v1/rerank \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query_embedding": [0.12, -0.34, ...],
    "top_k": 5,
    "fetch_k": 50,
    "method": "mmr",
    "lambda": 0.7,
    "collection": "chemistry",
    "topic": "organic"
  }'
```

`lambda` is the trade-off: `1.0` is pure relevance (identical to the plain
vector ranking), `0.0` is pure diversity. Note MMR deliberately *gives up* some
relevance — it is for de-duplicating results, not for improving them.

### Cross-encoder — relevance

This is the only method that judges whether a passage actually answers the
query. It requires `query_text`, the raw query string:

```bash
curl -X POST http://localhost:8000/v1/rerank \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query_embedding": [0.12, -0.34, ...],
    "query_text": "What is the capital of France?",
    "top_k": 5,
    "fetch_k": 50,
    "method": "cross_encoder",
    "collection": "facts"
  }'
```

Response (`200`):

```json
{
  "user_id": "thevyasamit",
  "method": "cross_encoder",
  "model": "BAAI/bge-reranker-base",
  "top_k": 5,
  "fetch_k": 50,
  "results": [
    {
      "id": "xyz-456",
      "score": 0.9848,
      "rerank_score": 0.9998,
      "collection": "facts",
      "topic": null,
      "text": null,
      "chunks": ["Paris is the capital and most populous city of France."],
      "metadata": {}
    }
  ]
}
```

#### Why it helps

A bi-encoder turns the query and each passage into a vector *independently*,
then compares them once. Anything the vector failed to capture is gone before
the comparison happens. A cross-encoder feeds the pair through a transformer
*together*, so every query token attends to every passage token.

A measured example from this repo's test suite — the query is "What is the
capital of France?":

```
  pure vector ranking            cross-encoder reranking
  1. 0.9939  Eiffel Tower...     1. +7.61  Paris is the capital of France.
  2. 0.9848  Paris is the...     2. -2.95  Berlin is the capital of Germany.
  3. 0.9701  Berlin is the...    3. -7.98  Eiffel Tower...
```

The vector ranking put the Eiffel Tower first — it is lexically about Paris,
but it does not answer the question. The cross-encoder fixed it.

#### Choosing a model

Pass `rerank_model` to pick per request (it must be in `RERANK_ALLOWED_MODELS`),
or set `RERANK_MODEL` to change the default:

```json
{
  "query_embedding": [0.12, -0.34, "..."],
  "query_text": "How do plants turn sunlight into energy?",
  "method": "cross_encoder",
  "rerank_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
  "collection": "biology",
  "top_k": 5,
  "fetch_k": 50
}
```


| Model                                  | Params | RAM    | 50 candidates | Languages                     |
| -------------------------------------- | ------ | ------ | ------------- | ----------------------------- |
| `BAAI/bge-reranker-base` *(default)*   | 278M   | ~1.5GB | ~1.2s         | Multilingual (100+ languages) |
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | 23M    | ~0.3GB | ~0.2s         | **English only**              |

> **MiniLM is English-only — this is a hard limitation, not a preference.** It is
> a MiniLM cross-encoder trained solely on the MS MARCO passage corpus, which is
> English. Its tokenizer and training data have no meaningful coverage of other
> languages, so on non-English text it returns confident, meaningless scores
> rather than an obvious error. Use it when your corpus and queries are English
> and you want the ~6x speedup; use `bge-reranker-base` (trained multilingually
> on XLM-RoBERTa) for anything else, including mixed-language collections.

Latency measured on 6 CPU threads with ~400-token passages; scales roughly
linearly with `fetch_k`. Both models fit comfortably in a 10GB / 10-core pod,
and both can be loaded at once.

Operational notes:

- **Weights download on first use** (~1.1GB for bge, ~90MB for MiniLM). The first
  request after a pod restart pays that cost. Set `RERANK_PRELOAD=true` to load
  during startup instead, or mount a volume at `$HF_HOME` to cache across restarts.
- **`rerank_score` is not comparable across models.** `bge-reranker-base` emits
  sigmoid-normalised scores in `[0, 1]`; MiniLM emits raw logits, typically
  `[-11, +11]`. Compare scores only within one response.
- **Inference runs in a worker thread**, so a slow rerank never blocks other
  requests on the pod.
- `fetch_k` above `RERANK_MAX_CANDIDATES` (default 128) is truncated to the
  best-scoring candidates rather than rejected.

## How to List Your Collections

Returns only collections you have embeddings in, with counts scoped to you:

```bash
curl http://localhost:8000/v1/collections -H "X-Tapis-Token: $TAPIS_TOKEN"
```

Response (`200`):

```json
{
  "user_id": "thevyasamit",
  "count": 2,
  "total": 2,
  "detail": "basic",
  "next_offset": null,
  "collections": [
    { "collection": "biology", "points": 42, "vector_dim": 768,
      "topics": null, "embedding_models": null, "truncated": false },
    { "collection": "chemistry", "points": 17, "vector_dim": 768,
      "topics": null, "embedding_models": null, "truncated": false }
  ]
}
```

Stats for one collection, and a paginated listing of the embeddings inside it:

```bash
curl http://localhost:8000/v1/collections/biology -H "X-Tapis-Token: $TAPIS_TOKEN"

curl "http://localhost:8000/v1/collections/biology/embeddings?limit=50&topic=plant" \
  -H "X-Tapis-Token: $TAPIS_TOKEN"
```

The embeddings listing is cursor-paginated — pass the returned `next_offset`
back as `?offset=` to get the next page. It returns metadata only, never vectors.

## How to Delete in Bulk

### Delete everything you own in one collection

```bash
curl -X DELETE http://localhost:8000/v1/collections/biology \
  -H "X-Tapis-Token: $TAPIS_TOKEN"
```

```json
{
  "user_id": "thevyasamit",
  "collection": "biology",
  "deleted": 42,
  "collection_dropped": false
}
```

Only **your** points are removed. `collection_dropped` is `true` only when no
points from any user were left, in which case the Qdrant collection itself is
deleted. Another user's data in the same collection is never touched.

### Delete a selected subset

`POST /v1/embeddings/bulk-delete` takes a selector in the body — explicit ids,
or a topic/metadata predicate. (It is a POST because DELETE cannot carry a
request body portably.)

By id:

```bash
curl -X POST http://localhost:8000/v1/embeddings/bulk-delete \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"collection": "biology", "ids": ["abc-123", "def-456"]}'
```

By topic or metadata:

```bash
curl -X POST http://localhost:8000/v1/embeddings/bulk-delete \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "collection": "biology",
    "topic": "plant",
    "filter": {"conditions": {"source": "old_notes.pdf"}}
  }'
```

Everything in the collection:

```bash
curl -X POST http://localhost:8000/v1/embeddings/bulk-delete \
  -H "X-Tapis-Token: $TAPIS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"collection": "biology", "all": true}'
```

Ids you do not own are silently skipped — they are not found, so they are not
deleted, and `deleted` reflects only what was actually removed.

### Delete everything, everywhere

```bash
curl -X DELETE "http://localhost:8000/v1/collections?confirm=true" \
  -H "X-Tapis-Token: $TAPIS_TOKEN"
```

```json
{
  "user_id": "thevyasamit",
  "deleted": 59,
  "collections_affected": ["biology", "chemistry"],
  "collections_dropped": ["chemistry"]
}
```

Irreversible. `?confirm=true` is required — without it the request returns `400`,
so a stray `DELETE /v1/collections` cannot wipe your account by accident.

## How to Run the Tests

```bash
uv pip install -e ".[rerank,dev]" --extra-index-url https://download.pytorch.org/whl/cpu
pytest -q
```

The suite is hermetic — it runs against an in-memory Qdrant with a stubbed
current-user dependency, so it needs no Qdrant server, no Tapis token and no
network (beyond a one-time model download for the cross-encoder tests).

Without the `[rerank]` extra the cross-encoder tests skip and the rest still
pass, which is exactly the slim-install configuration the service supports.


The layout mirrors the source tree: `tests/unit/` covers modules in isolation,
`tests/v1/` drives the HTTP API end to end.

```
tests/
├── conftest.py                      in-memory Qdrant + switchable current user
├── unit/
│   ├── test_filters.py              the tenancy invariant, asserted directly
│   ├── test_security.py             token validation and every rejection path
│   ├── test_schemas.py              request validation
│   ├── test_vector_reranking.py     mmr and cosine_rescore maths
│   ├── test_cross_encoder.py        allowlist, candidate cap, dispatch (model stubbed)
│   ├── test_repository_helpers.py   slugs, projections, facet fallback
│   └── test_startup.py              lifespan, shared client, failure handling
└── v1/
    ├── test_isolation.py            ◄ the security boundary, end to end
    ├── test_embeddings.py           CRUD
    ├── test_collections.py          listing, pagination, bulk delete, purge
    ├── test_search.py               retrieve and filtering
    ├── test_rerank.py               all three methods through the API
    ├── test_health.py               the probe
    └── test_settings_behaviour.py   behaviour that changes with configuration
```

Coverage is enforced: `pytest --cov` fails below the floor set in
`pyproject.toml`, and CI runs it that way. The uncovered remainder is code that
only executes when torch is absent, or that wraps a live network call.

```bash
pytest -q --cov          # with coverage, as CI runs it
pytest tests/v1 -q       # just the API suite
pytest tests/unit -q     # just the unit suite (no model download)
```

After changing any route or schema, regenerate the committed spec:

```bash
python scripts/export_openapi.py
```

CI runs `--check` on that script and fails if `openapi.json` has drifted from
the app.

# Explanation

## Architecture

```
                      ICICLE AI Vector Service
                         ┌──────────────────────────────────────────────────┐
                         │                                                  │
  Client Request         │   FastAPI Application                            │
  (X-Tapis-Token)        │                                                  │
        |                │   ┌──────────┐    ┌───────────────────────────┐  │
        v                │   │  Auth    │    │   CRUD Layer              │  │
  ┌──────────┐           │   │  (JWKS)  │    │                           │  │
  │  POST    │──────────>│   │          │───>│  user_id extracted        │  │
  │ /v1/embed│           │   │ Verify   │    │  from JWT token           │  │
  │  dings   │           │   │ JWT sig  │    │                           │  │
  └──────────┘           │   │ Check    │    └───────────┬───────────────┘  │
                         │   │ expiry   │                │                  │
                         │   │ Validate │                v                  │
                         │   │ tenant   │    ┌───────────────────────────┐  │
                         │   └──────────┘    │  Qdrant Vector DB         │  │
                         │                   │                           │  │
                         │                   │  ┌─────────────────────┐  │  │
                         │                   │  │ Collection:"biology"│  │  │
                         │                   │  │                     │  │  │
                         │                   │  │  topic:"human"      │  │  │
                         │                   │  │  ┌───────────────┐  │  │  │
                         │                   │  │  │ alice, vec_1  │  │  │  │
                         │                   │  │  │ bob,   vec_2  │  │  │  │ 
                         │                   │  │  └───────────────┘  │  │  │
                         │                   │  │                     │  │  │
                         │                   │  │  topic:"plant"      │  │  │
                         │                   │  │  ┌───────────────┐  │  │  │
                         │                   │  │  │ alice, vec_3  │──┼──┼──┼──> HNSW Index
                         │                   │  │  │ bob,   vec_4  │  │  │  │   (Cosine Similarity)
                         │                   │  │  └───────────────┘  │  │  │
                         │                   │  │                     │  │  │
                         │                   │  │  topic: null        │  │  │
                         │                   │  │  ┌───────────────┐  │  │  │
                         │                   │  │  │ alice, vec_5  │  │  │  │
                         │                   │  │  └───────────────┘  │  │  │
                         │                   │  └─────────────────────┘  │  │
                         │                   │                           │  │
                         │                   │  ┌─────────────────────┐  │  │
                         │                   │  │Collection:"chemistry│  │  │
                         │                   │  │  topic:"organic"    │  │  │
                         │                   │  │  topic:"inorganic"  │  │  │
                         │                   │  └─────────────────────┘  │  │
                         │                   └───────────────────────────┘  │
                         └──────────────────────────────────────────────────┘
```

### How Collections and Topics Work

```
  collection = Qdrant collection (broad domain, has its own HNSW index)
  topic      = optional sub-category (payload filter within a collection)
  user_id    = data isolation (payload filter, from JWT)

  ┌──────────────────────────────────────────────────────────────┐
  │  Collection: "biology"                                       │
  │                                                              │
  │  topic:"human"    topic:"plant"    topic:"animal"   no topic │
  │  ┌──────────┐     ┌──────────┐     ┌──────────┐   ┌───────┐  │
  │  │alice v1  │     │alice v3  │     │bob   v5  │   │alice  │  │
  │  │bob   v2  │     │bob   v4  │     │alice v6  │   │v7     │  │
  │  └──────────┘     └──────────┘     └──────────┘   └───────┘  │
  │                                                              │
  │  alice searches collection="biology":                        │
  │    -> finds v1, v3, v6, v7  (all her vectors, all topics)    │
  │                                                              │
  │  alice searches collection="biology", topic="plant":         │
  │    -> finds v3 only  (her vectors in "plant" topic)          │
  │                                                              │
  │  bob's data is always invisible to alice.                    │
  └──────────────────────────────────────────────────────────────┘
```

## Search Algorithms


| Operation                   | Algorithm                                                                                                        | Description                                                                                                                                                                                              |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Indexing**                | [HNSW](https://arxiv.org/abs/1603.09320) (Hierarchical Navigable Small World)                                    | Qdrant builds an HNSW graph index per collection. This provides approximate nearest neighbor (ANN) search in logarithmic time, even over millions of vectors.                                            |
| **Similarity metric**       | **Cosine Similarity**                                                                                            | Measures the angle between two vectors. Score of 1.0 = identical direction, 0.0 = orthogonal. Configured per collection via `Distance.COSINE`.                                                           |
| **Retrieve**                | HNSW + Cosine                                                                                                    | Finds the `top_k` most similar vectors to the query embedding using the HNSW index with cosine distance. Payload filters (`user_id`, `topic`, `metadata`) are applied during the search, not after.      |
| **Rerank (MMR)**            | [Maximal Marginal Relevance](https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf) | Balances **relevance** (similarity to query) with **diversity** (dissimilarity between selected results). The `lambda` parameter controls the trade-off: `1.0` = pure relevance, `0.0` = pure diversity. |
| **Rerank (cosine_rescore)** | Cosine re-scoring                                                                                                | Recomputes the exact cosine similarity over the fetched vectors and re-sorts. Qdrant's HNSW search is *approximate*, so this can correct near-ties the ANN traversal ordered slightly wrong.             |
| **Rerank (cross_encoder)**  | [Cross-encoder](https://www.sbert.net/examples/applications/cross-encoder/README.html) re-ranking                | Feeds `(query_text, passage_text)` through a transformer **together**, so every query token attends to every passage token. The only method that judges true relevance rather than vector geometry.      |


### Bi-encoder vs. Cross-encoder

Everything Qdrant does is *bi-encoder* retrieval, and reranking with `mmr` or
`cosine_rescore` stays inside that world:

```
  BI-ENCODER (retrieve, mmr, cosine_rescore)      CROSS-ENCODER (cross_encoder)

  query ──> [encoder] ──> vector ─┐               query ──┐
                                  ├─> cosine               ├─> [transformer] ─> relevance
  passage ─> [encoder] ──> vector ┘               passage ─┘

  Encoded separately, compared once.              Encoded together, every query token
  Passage vectors precomputed at ingest,          attends to every passage token. Nothing
  so search is an index lookup: fast.             is precomputable: one forward pass per
  Anything the vector lost is lost                candidate, so it only runs over the
  before the comparison happens.                  shortlist retrieval already narrowed.
```

This is why the two stages compose rather than compete: the bi-encoder cheaply
narrows millions of vectors to ~50 candidates, and the cross-encoder spends real
compute ordering just those.

### Search Flow

```
  Query Embedding ──>  HNSW Index Lookup  ──>  Payload Filters   ──>  Results
  [0.12, -0.34, ...]   (ANN search,           user_id = "alice"      top_k sorted
                         cosine distance,       + topic = "plant"      by similarity
                         within collection)     + metadata filters
                              |
                              v
                    Optional: Rerank (fetch_k=50 -> top_k=5)
                    ┌──────────────────────────────────────────┐
                    │ mmr             relevance + diversity    │
                    │ cosine_rescore  exact cosine re-sort     │
                    │ cross_encoder   query_text x passage     │
                    │                 text through a model     │
                    └──────────────────────────────────────────┘
```

## Project Layout

Four layers, each depending only on the ones above it. Nothing under `api/`
imports `qdrant_client` directly — all storage goes through the repository, so
there is exactly one place where user scoping could be got wrong.

```
src/app/
├── main.py                  app wiring: CORS, lifespan, /healthz, mounts /v1
│
├── core/                    cross-cutting; knows nothing about HTTP or Qdrant
│   ├── settings.py          env-backed configuration
│   └── security.py          Tapis JWT -> UserContext (the only identity source)
│
├── schemas/                 request/response models, one module per resource
│   ├── common.py            MetadataFilter, HealthResponse
│   ├── embeddings.py        create/update/bulk-delete
│   ├── collections.py       listing, purge
│   └── search.py            retrieve, rerank
│
├── db/                      all persistence
│   ├── client.py            the shared AsyncQdrantClient
│   ├── filters.py           ◄ THE TENANCY BOUNDARY — every filter is built here
│   └── repository.py        every read and write, each scoped through filters
│
├── reranking/               result reordering
│   ├── __init__.py          rerank() dispatch
│   ├── vector.py            mmr, cosine_rescore (pure math, no model)
│   └── cross_encoder.py     cross_encoder (optional transformer)
│
└── api/v1/                  HTTP only: auth, logging, response shaping
    ├── __init__.py          declares the /v1 prefix
    ├── embeddings.py        /v1/embeddings/*
    ├── collections.py       /v1/collections/*
    └── search.py            /v1/retrieve, /v1/rerank
```

## How User Isolation Works

Each user's collections are physically separate Qdrant collections, so isolation is
a storage boundary first. A `user_id` filter is applied on every operation as well,
built in exactly one place, as defence in depth.

```
  Request ──> Tapis JWT ──> username ──> db/filters.py ──> Qdrant
              (core/security)            builds every
                                         filter, always
                                         pinning user_id
```

**Identity comes only from the signed token.** `user_id` is read from the
`tapis/username` claim. It is never taken from a request body, query string or
header, so a client cannot act as another user by asking to — a `user_id` key in
a store or update body is simply ignored, and the stored payload always carries
the caller's own name.

**Every query is scoped by construction.** `db/filters.py` is the only module
that builds Qdrant filters, and every function it exposes returns a filter with
`user_id` pinned in `must`. Client-supplied conditions are only ever *appended*
to `must` (logical AND), and never placed in `should` or `must_not`, so extra
conditions can only narrow a result set — never widen it past the caller's own
data.

**Metadata filters cannot escape.** Filter keys are namespaced under `metadata.`
before reaching Qdrant, so `{"conditions": {"user_id": "someone-else"}}` looks
for `metadata.user_id` and matches nothing.

**Deleting by id is filtered, not trusted.** Bulk delete ANDs `HasIdCondition`
with the owner condition rather than deleting the given ids outright, so an id
belonging to another user matches nothing instead of being removed.

**Collections are never dropped out from under another user.** Deleting "a
collection" removes only the caller's points. Dropping the emptied Qdrant
collection is **off by default** (`DROP_EMPTY_COLLECTIONS`): checking "is it
empty?" and dropping it are two separate round trips, and another user writing
their first point into that window would lose data that had just been written
successfully. Nothing the service can do makes that pair atomic, so the default
is to leave the empty collection in place. Even with the setting enabled, a
collection holding another user's points is never dropped.

**Existence is not observable.** Asking about a collection you own nothing in
returns `404` with the same message as a collection that does not exist, across
every endpoint — otherwise status codes alone would let one user enumerate
another's collection names.

**One user cannot monopolise the pod.** `RERANK_MAX_CANDIDATES` caps how many
candidates a single cross-encoder request may score, so a large `fetch_k` cannot
occupy the CPU indefinitely and slow everyone else down.

`tests/v1/test_isolation.py` asserts each of these end to end, and
`tests/unit/test_filters.py` asserts the filter invariant directly. Several
tests pair a negative assertion with a positive control (for example, a mixed
batch of ids must delete exactly one of two) so that a filter which silently
matched nothing would fail rather than pass.

### Dimensions are per collection, not global

A collection's vector dimension is fixed by its first embedding and cannot change.
Because collections are per user, this only ever constrains a user against their own
earlier choice - two users can hold `biology` at different dimensions, and one user
can hold `biology` at 768 and `biology-v2` at 1024.

Storing a mismatched width returns `409` with an explanation. To change a
collection's dimension, delete it and re-ingest.

See [Why Collections Are Per User](#why-collections-are-per-user) for why the service
is built this way and what it costs.


## Why Collections Are Per User

Qdrant's multitenancy guidance is to keep every tenant in **one** collection,
partitioned by a payload field. That is the right default for a product: tenants are
customers of the same application, running the same model, and the operator wants
many of them cheaply.

A research tenant is not that. Users arrive from different domains with an embedding
model already chosen by their science — Gemini at 768 dimensions, NVClip at 1024,
NV-Embed at 4096. A collection's vector dimension is fixed by its first embedding and
can never change, so a single shared collection would let whoever stores first fix
the dimension for everyone:

```
SHARED COLLECTION                       PER-USER COLLECTIONS
embeddings (768d, fixed globally)       alice_9f2a__bio    768d   ✓  Gemini
  alice, 768d   ✓                       bob_1110__bio     1024d   ✓  NVClip
  bob,  1024d   ✗                       carol_4d81__bio   4096d   ✓  NV-Embed
  carol, 4096d  ✗
```

Giving each user their own collections buys three things that matter for research
use:

- **Any model, any dimension**, chosen per collection rather than per deployment.
- **Side-by-side experiments** — the same corpus embedded two ways, held at once.
  This repository's own `benchmark/scripts/dim_sweep.sh` relies on it, running six
  collections from 768 to 4096 dimensions under a single account.
- **Structural isolation** — two users' vectors are never in the same index, so a
  missed filter on some future endpoint has nothing to leak into.

The cost is collection count: Qdrant Cloud caps a cluster at 1,000 by default, and
200 users with five collections each would reach it. Measurements show search and
write latency are unaffected by collection count, and listing is paginated, so the
ceiling is a Qdrant resource limit rather than a latency one (see
[benchmark/REPORT.md](https://github.com/ICICLE-ai/icicle-ai-vector-service/blob/main/benchmark/REPORT.md) §5.4).

If that ceiling is ever reached, the migration is one collection **per dimension**
partitioned by user — a handful of collections instead of one per user — which keeps
the dimension freedom. All naming lives in `db/naming.py` and all filtering in
`db/filters.py`, so that change is two modules, not the service.

## Design Decisions

- **Collection = broad domain, per user**: each of your domains (e.g. `biology`, `chemistry`) is its own Qdrant collection with its own HNSW index and vector dimension. Search only traverses vectors in that one collection, which keeps relevance high and queries fast.
- **Topic = optional sub-category**: Topics (e.g. `human`, `plant`, `organic`) are payload fields within a collection. They allow narrowing search results without creating separate collections. A collection can have embeddings with different topics, or no topic at all.
- **User isolation is physical, with a filter as backup**: each user's collections are separate Qdrant collections (see [Why Collections Are Per User](#why-collections-are-per-user)), so two users' vectors are never in the same index. Every query *also* filters by `user_id` from the JWT, which is defence in depth rather than the barrier itself.
- **No server-side embedding**: Clients provide pre-computed vectors. This keeps the service model-agnostic and lightweight — any embedding model works. The vector dimension is set per collection by the first embedding stored.
- **Dynamic vector dimensions**: There is no global `VECTOR_DIM` setting. Each collection's dimension is determined by the first embedding stored in it (e.g. 768 for Gemini, 1024 for NVIDIA NVClip, 4096 for NV-Embed-v1). All subsequent embeddings in the same collection must match that dimension — Qdrant enforces this automatically. The `embedding_model` field is required so the model that produced each vector is always tracked.
- **Metadata filtering at search time**: Qdrant applies payload filters during the HNSW traversal (not as a post-filter), so filtered searches remain efficient even on large collections.
- **Auth boundary**: JWKS-validated Tapis JWTs are the sole security gate. CORS is open by default (`*`) since the token is what matters, not the origin.
- **Update/Delete require collection**: Since Qdrant doesn't support global ID lookups across collections, the `collection` query param is required on update/delete to enable a direct O(1) lookup by embedding ID.
- **Deletes are scoped, and dropping is safe**: `DELETE /v1/collections/{collection}` removes only the caller's own collection. Because collections are per user, dropping it cannot affect anyone else, so `DROP_EMPTY_COLLECTIONS` defaults to on. Set it false to keep an emptied collection and preserve its vector dimension.
- **The collection namespace is isolated too**: `GET /v1/collections` is a prefix scan over the caller's own namespace, so users never learn which collections others created.
- **Bulk delete filters on `user_id`, including by id**: the by-id path ANDs `HasIdCondition` with the caller's `user_id` rather than deleting the ids outright, so passing another user's point id deletes nothing instead of succeeding.
- **Purge is opt-in**: `DELETE /v1/collections` requires `?confirm=true`, so an unqualified DELETE against the collection root cannot wipe an account.
- **Payload indexes on the filter fields**: `user_id`, `topic` and `embedding_model` get keyword indexes when a collection is created. Without them Qdrant does a full payload scan during HNSW traversal, which degrades as collections grow. Collections created before v1.0.0 are backfilled on startup, since creating an existing index is a no-op.
- **Reranking is optional and swappable**: the cross-encoder lives behind an optional `[rerank]` extra. Without it the service runs unchanged and only `method="cross_encoder"` returns `503`. Models are restricted to an allowlist so a client cannot make the pod download arbitrary weights.
- **Versioned router package**: endpoints live in `src/app/api/v1/`, with the `/v1` prefix declared in exactly one place (`api/v1/__init__.py`). Adding a v2 means a sibling package, not edits spread across handlers.
- **Layered, not flat**: configuration, schemas, persistence and reranking are separate packages rather than loose modules beside `main.py`. The point is the dependency direction — `api/` may import `db/`, never the reverse — which is what keeps the tenancy filter impossible to bypass from a handler.

> **Data storage notice:** Text chunks, metadata, and embeddings are stored **as-is** in Qdrant without encryption at rest. The service relies on JWT-based user isolation and network-level security (internal pod-to-pod communication) to protect data. If your use case requires encryption at rest, configure it at the Qdrant storage layer or the underlying volume/disk level.

---

# Reference

## API Endpoints

All endpoints (except `/healthz`) require the `X-Tapis-Token` header.


| Method   | Endpoint                                     | Description                                             |
| -------- | -------------------------------------------- | ------------------------------------------------------- |
| `GET`    | `/healthz`                                   | Health check (no auth)                                  |
| `POST`   | `/v1/embeddings`                             | Store a pre-computed embedding                          |
| `GET`    | `/v1/embeddings/{id}?collection=`            | Get one embedding's metadata                            |
| `PUT`    | `/v1/embeddings/{id}?collection=`            | Partial update of an embedding                          |
| `DELETE` | `/v1/embeddings/{id}?collection=`            | Delete one embedding                                    |
| `POST`   | `/v1/embeddings/bulk-delete`                 | Delete many by ids, topic/metadata predicate, or all    |
| `GET`    | `/v1/collections`                            | List your collections, paginated (25/page)              |
| `DELETE` | `/v1/collections?confirm=true`               | Delete **all** your embeddings across every collection  |
| `GET`    | `/v1/collections/{collection}`               | Stats for one collection                                |
| `GET`    | `/v1/collections/{collection}/embeddings`    | Paginated listing of your embeddings in a collection    |
| `DELETE` | `/v1/collections/{collection}`               | Delete your embeddings in one collection                |
| `POST`   | `/v1/retrieve`                               | Vector similarity search                                |
| `POST`   | `/v1/rerank`                                 | Rerank results (MMR, cosine rescore, or cross-encoder)  |
| `GET`    | `/v1/rerank/methods`                         | Which rerank methods and models this deployment offers  |

Interactive docs are served at `/docs`; the committed [`openapi.json`](https://github.com/ICICLE-ai/icicle-ai-vector-service/blob/main/openapi.json)
is the same spec, for client generation.


## Status Codes

| Code | Meaning | When |
| ---- | ------- | ---- |
| `200` | OK | Successful read, update, delete or search |
| `201` | Created | Embedding stored |
| `400` | Bad Request | Disallowed reranker model; purge without `confirm=true` |
| `401` | Unauthorized | Token missing a username, expired, malformed, or not an access token |
| `403` | Forbidden | Token is valid but belongs to another Tapis tenant |
| `404` | Not Found | Collection or embedding does not exist, or is not yours |
| `409` | Conflict | Embedding dimension does not match the collection's |
| `422` | Unprocessable Entity | Request body or query parameters failed validation |
| `503` | Service Unavailable | Cross-encoder requested but not installed in this deployment |

`404` is deliberately returned both for a resource that does not exist and for one
belonging to another user, with identical wording — distinguishing them would let
a caller discover other users' collection and embedding IDs.

## Request Fields

### Store (`POST /v1/embeddings`)


| Field             | Required | Description                                                                       |
| ----------------- | -------- | --------------------------------------------------------------------------------- |
| `embedding`       | yes      | Float array (any dimension — set per collection on first store)                    |
| `collection`      | yes      | Broad domain name — maps to a Qdrant collection (e.g. `"biology"`, `"chemistry"`) |
| `topic`           | no       | Sub-category within the collection (e.g. `"human"`, `"plant"`, `"organic"`)       |
| `chunks`          | yes      | At least one non-empty string                                                     |
| `metadata`        | no       | Free-form dict for extra info (`source`, `page`, etc.)                            |
| `embedding_model` | yes      | Name of the model used to generate the embedding (e.g. `"nvidia/nvclip"`)         |
| `token_ids`       | no       | Tokenizer output IDs (for debugging)                                              |


### Retrieve (`POST /v1/retrieve`)


| Field             | Required | Description                                          |
| ----------------- | -------- | ---------------------------------------------------- |
| `query_embedding` | yes      | Float array (must match the collection's dimension)  |
| `collection`      | yes      | Which collection to search                           |
| `top_k`           | no       | Number of results (default 10, max 100)              |
| `topic`           | no       | Narrow results to a specific sub-category            |
| `filter`          | no       | Metadata filter (`{"conditions": {"key": "value"}}`) |


### Rerank (`POST /v1/rerank`)


| Field             | Required | Description                                                   |
| ----------------- | -------- | ------------------------------------------------------------- |
| `query_embedding` | yes      | Float array (must match the collection's dimension)           |
| `collection`      | yes      | Which collection to search                                    |
| `top_k`           | no       | Final number of results (default 10, max 100)                 |
| `fetch_k`         | no       | Candidates to fetch before reranking (default 50, max 500)    |
| `method`          | no       | `"mmr"` (default), `"cosine_rescore"` or `"cross_encoder"`    |
| `query_text`      | cond.    | The raw query string. **Required** when `method="cross_encoder"`; ignored otherwise |
| `rerank_model`    | no       | Cross-encoder to use; must be in `RERANK_ALLOWED_MODELS`. Defaults to `RERANK_MODEL` |
| `lambda`          | no       | MMR trade-off: 1.0 = relevance, 0.0 = diversity (default 0.7) |
| `topic`           | no       | Narrow results to a specific sub-category                     |
| `filter`          | no       | Metadata filter                                               |


### Update (`PUT /v1/embeddings/{id}?collection=`)


| Field                      | Required | Description                               |
| -------------------------- | -------- | ----------------------------------------- |
| `collection` (query param) | yes      | Which collection the embedding belongs to |
| `topic`                    | no       | Update the sub-category                   |
| `embedding`                | no       | Replace the vector                        |
| `chunks`                   | no       | Replace the chunks                        |
| `metadata`                 | no       | Replace the metadata                      |
| `embedding_model`          | no       | Update the model name                     |
| `token_ids`                | no       | Update token IDs                          |


### Delete (`DELETE /v1/embeddings/{id}?collection=`)


| Field                      | Required | Description                               |
| -------------------------- | -------- | ----------------------------------------- |
| `collection` (query param) | yes      | Which collection the embedding belongs to |


### Bulk delete (`POST /v1/embeddings/bulk-delete`)

Exactly one selector: `ids`, or a `topic`/`filter` predicate, or `all`.


| Field        | Required | Description                                                            |
| ------------ | -------- | ----------------------------------------------------------------------- |
| `collection` | yes      | Which collection to delete from                                        |
| `ids`        | one of   | Explicit embedding ids, at most 1000. Ids you don't own are skipped    |
| `topic`      | one of   | Delete everything you own with this topic                              |
| `filter`     | one of   | Metadata predicate, combinable with `topic`                            |
| `all`        | one of   | `true` deletes everything you own in the collection. Cannot be combined |

Returns `{ "deleted": <int>, "collection_dropped": <bool> }`. Invalid selector
combinations return `422`.


### List embeddings (`GET /v1/collections/{collection}/embeddings`)


| Query param | Required | Description                                                  |
| ----------- | -------- | ------------------------------------------------------------- |
| `limit`     | no       | Page size, 1–500 (default 50)                                 |
| `offset`    | no       | Cursor from the previous page's `next_offset`                 |
| `topic`     | no       | Only embeddings with this topic                               |


### List collections (`GET /v1/collections`)


| Query param | Required | Description                                                   |
| ----------- | -------- | ------------------------------------------------------------- |
| `limit`     | no       | Page size, 1–100 (default 25)                                 |
| `offset`    | no       | Collections to skip (default 0)                               |
| `detail`    | no       | `basic` (default) returns names, point counts and dimensions. `full` also derives topics and embedding models, at two extra Qdrant calls per collection. |

Returns `total` (all collections you own) and `next_offset` (null on the last page).
Paginated because the endpoint's cost is proportional to the number of collections
returned; `basic` halves that cost again.

`topics` and `embedding_models` are capped at 100 distinct values. When the cap is
hit, `truncated` is `true` on that collection rather than the list silently being
short.

`GET /v1/collections/{collection}` always returns full detail, since it describes a
single collection.


### Purge (`DELETE /v1/collections`)


| Query param | Required | Description                                          |
| ----------- | -------- | ----------------------------------------------------- |
| `confirm`   | yes      | Must be `true`. Returns `400` otherwise               |
