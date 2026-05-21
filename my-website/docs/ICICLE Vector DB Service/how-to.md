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

Log in to the [ICICLEaaS Portal](https://icicleai.tapis.io), click your username in the bottom-left corner, and select **Copy Access Token**.

![Getting your Tapis access token](https://raw.githubusercontent.com/ICICLE-ai/icicle-ai-vector-service/main/docs/images/tapis-access-token.png)


| Scenario                   | Status | Response                                                                        |
| -------------------------- | ------ | ------------------------------------------------------------------------------- |
| No `X-Tapis-Token` header  | `422`  | `"field required"`                                                              |
| Expired token              | `401`  | `"Token has expired. Please obtain a fresh access token."`                      |
| Wrong issuer               | `401`  | `"Invalid token issuer. Expected issuer: ..."`                                  |
| Wrong tenant (e.g. `tacc`) | `403`  | `"Access denied. This service only accepts tokens from the 'icicleai' tenant."` |
| Invalid/malformed token    | `401`  | `"Token validation failed. Ensure you are sending a valid Tapis access token."` |


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

Rerank search results using MMR (diversity + relevance) or cosine rescoring:

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

Response (`200`):

```json
{
  "user_id": "thevyasamit",
  "method": "mmr",
  "top_k": 5,
  "fetch_k": 50,
  "results": [
    {
      "id": "xyz-456",
      "score": 0.91,
      "collection": "chemistry",
      "topic": "organic",
      "text": null,
      "chunks": ["Covalent bonds form when atoms share electrons..."],
      "metadata": {"source": "chem_101.pdf"}
    }
  ]
}
```

## Troubleshooting

- **"Qdrant is not reachable"**: If Qdrant is behind an HTTPS reverse proxy (port 443), append `:443` to `QDRANT_URL` (e.g. `https://host.example.com:443`). The qdrant-client library defaults to port 6333 if no port is specified.
- **401/403 errors**: Ensure your Tapis token is fresh, from the `icicleai` tenant, and passed via the `X-Tapis-Token` header.
- **Dimension mismatch**: The `embedding` array length must match the collection's dimension (set by the first embedding stored in that collection).
- **"collection is required"**: All retrieve/rerank requests must specify which collection to query.
