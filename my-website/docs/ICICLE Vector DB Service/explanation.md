---
tags:
  - CI4AI
  - AI4CI
  - Software
---
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
| **Rerank (cosine_rescore)** | Cosine re-scoring                                                                                                | Simply re-sorts the fetched candidates by cosine similarity score and returns the top_k.                                                                                                                 |


### Search Flow

```
  Query Embedding ──>  HNSW Index Lookup  ──>  Payload Filters   ──>  Results
  [0.12, -0.34, ...]   (ANN search,           user_id = "alice"      top_k sorted
                         cosine distance,       + topic = "plant"      by similarity
                         within collection)     + metadata filters
                              |
                              v
                    Optional: Rerank
                    ┌─────────────────────────┐
                    │  MMR: fetch_k=50        │
                    │  Select top_k=5 that    │
                    │  maximize relevance +   │
                    │  diversity              │
                    └─────────────────────────┘
```

## Design Decisions

- **Collection = broad domain**: Each domain (e.g. `biology`, `chemistry`) gets its own Qdrant collection with its own HNSW index. Similarity search only traverses vectors in the same domain, resulting in higher relevance and faster queries.
- **Topic = optional sub-category**: Topics (e.g. `human`, `plant`, `organic`) are payload fields within a collection. They allow narrowing search results without creating separate collections. A collection can have embeddings with different topics, or no topic at all.
- **User isolation via payload filter**: Collections are shared across all users, but every query automatically filters by `user_id` (extracted from the JWT). Users never see each other's data.
- **No server-side embedding**: Clients provide pre-computed vectors. This keeps the service model-agnostic and lightweight — any embedding model works. The vector dimension is set per collection by the first embedding stored.
- **Dynamic vector dimensions**: There is no global `VECTOR_DIM` setting. Each collection's dimension is determined by the first embedding stored in it (e.g. 768 for Gemini, 1024 for NVIDIA NVClip, 4096 for NV-Embed-v1). All subsequent embeddings in the same collection must match that dimension — Qdrant enforces this automatically. The `embedding_model` field is required so the model that produced each vector is always tracked.
- **Metadata filtering at search time**: Qdrant applies payload filters during the HNSW traversal (not as a post-filter), so filtered searches remain efficient even on large collections.
- **Auth boundary**: JWKS-validated Tapis JWTs are the sole security gate. CORS is open by default (`*`) since the token is what matters, not the origin.
- **Update/Delete require collection**: Since Qdrant doesn't support global ID lookups across collections, the `collection` query param is required on update/delete to enable a direct O(1) lookup by embedding ID.

> **Data storage notice:** Text chunks, metadata, and embeddings are stored **as-is** in Qdrant without encryption at rest. The service relies on JWT-based user isolation and network-level security (internal pod-to-pod communication) to protect data. If your use case requires encryption at rest, configure it at the Qdrant storage layer or the underlying volume/disk level.
