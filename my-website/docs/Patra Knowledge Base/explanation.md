---
tags:
  - CI4AI
  - PADI
---
# Explanation

## Status Notice

Patra's active backend is now the **FastAPI + PostgreSQL** service under `rest_server/`.

The following Neo4j-based components are **retained only for archive/reference compatibility and are no longer part of the active backend path**:
- `legacy/legacy_server/`
- `mcp_server/`
- `legacy/ingester/neo4j_ingester.py`
- `legacy/reconstructor/mc_reconstructor.py`
- Neo4j-oriented Docker/Make targets

For all new development, deployment, integration, and operational work, use the PostgreSQL-backed REST API only.

At the heart of the Patra Knowledge Base is the concept of Model Cards. These cards are essentially detailed records that provide essential information about each AI/ML model. This information includes technical details like the model's accuracy and latency, but it goes beyond that to include non-technical aspects such as fairness, explainability, and the model's behavior in various deployment environments. This holistic approach is intended to create a comprehensive understanding of the model's strengths and weaknesses, enabling more informed decisions about its use and deployment

Key features and capabilities of the Patra AI Cards Framework include:

- **Semi-automated information capture:** Patra reduces the burden of manual documentation by automatically capturing information about model fairness, explainability, and performance in different deployment environments. This automation is facilitated by the [Model Card Toolkit](https://github.com/Plale-Lab/patra-toolkit)  , which invokes analysis tools and integrates the results directly into the Model Cards.
  
- **Relational system of record:** Patra's active backend now uses PostgreSQL as the system of record for model cards, datasheets, and protected asset ingestion APIs. Neo4j-era graph components are preserved only as legacy reference code and are no longer the supported runtime path.
  
- **Provenance tracking:** Patra leverages the concepts of **forward and backward provenance** to comprehensively track the relationships between models, datasets, and deployment instances. This makes it possible to understand the lineage of models, trace their origins, and analyze their usage patterns.
  
- **Real-time deployment information:** Patra integrates with the [CKN Edge AI Framework](https://github.com/Plale-Lab/cyberinfrastructure-knowledge-network)  to capture real-time information about model execution in edge environments. This includes data on performance, resource usage, and other relevant metrics, which can be used to optimize deployments and gain insights into model behavior in real-world settings.
  
- **Machine-actionable API:** Patra provides a **machine-actionable API** that allows intelligent systems in the edge-cloud continuum to query the knowledge base and make informed decisions about model selection. This enables automated model selection based on various criteria, including fairness, explainability, and performance metrics, further enhancing accountability and transparency.
  
- **Versioning and Similarity Analysis:** Patra infers relationships between model cards such as **"alternateOf," "revisionOf," and "transformativeUseOf"** by leveraging embedding vectors and cosine similarity comparisons. This capability is essential for tracking model evolution, identifying different versions, and understanding how models are adapted and reused over time.

By combining these capabilities, the Patra Knowledge Base provides a robust foundation for **trustworthy and accountable AI/ML model management within the edge-cloud continuum**. This framework addresses crucial aspects of transparency, provenance tracking, and performance monitoring, ultimately contributing to more responsible and reliable AI deployments.

For more information, please refer to the [Patra ModelCards paper](https://ieeexplore.ieee.org/document/10678710).

### Hosted Deployments (Tapis Pods)

Patra runs as [Tapis Pods](https://tapis.readthedocs.io/en/latest/technical/pods.html) in the
ICICLE tenant. Use these endpoints instead of a local stack when you just need to read or
submit records:

| Service | URL | Notes |
| ------- | --- | ----- |
| Patra UI | `https://patra.pods.icicleai.tapis.io` | Public web interface |
| REST API (stable) | `https://patrabackend.pods.icicleai.tapis.io` | Use this as `patra_server_url` / `PATRA_URL` |
| REST API (dev) | `https://patrabackend-dev.pods.icicleai.tapis.io` | Dev-only routes enabled; not for integrations |
| MCP server | `https://patramcp.pods.icicleai.tapis.io` | Legacy/archived — see the Status Notice above |
| Tapis tenant | `https://icicleai.tapis.io` | OAuth2 token endpoint at `/v3/oauth2/tokens` |

Quick check against the stable deployment:

```bash
export PATRA_URL=https://patrabackend.pods.icicleai.tapis.io
curl -s "$PATRA_URL/" | head
curl -s "$PATRA_URL/modelcards" | head
```

Reads of public records are unauthenticated. Private records and all write operations require
either an `X-Tapis-Token` or an org/API-key pair (see the Asset Ingest API section). Obtain a
Tapis token with your TACC credentials:

```bash
curl -X POST https://icicleai.tapis.io/v3/oauth2/tokens \
  -H "Content-Type: application/json" \
  -d '{"username": "<tacc-username>", "password": "<tacc-password>", "grant_type": "password"}'
```

The stable and dev backends share one PostgreSQL database, so treat writes against the dev pod
as writes against production data.

### Patra Servers

Patra provides multiple server implementations for different use cases.

#### 1. Primary REST API (FastAPI + PostgreSQL)

The primary REST API is implemented with FastAPI and backed by PostgreSQL. It is intended for new integrations and powers the privacy-aware model card and datasheet APIs.

- **Code location**: `rest_server/`
- **Default port**: `8000`
- **Example endpoints** (non-exhaustive):
  - `GET /` – Simple health/info endpoint.
  - `GET /modelcards` – List model cards (public-only by default; private when authorized).
  - `GET /modelcard/{id}` – Retrieve a single model card.
  - `PUT /modelcard/{id}` – Update a model card and its linked AI model (authenticated).
  - `GET /datasheets` – List datasheets (public-only by default; private when authorized).
  - `GET /datasheet/{identifier}` – Retrieve a single datasheet with normalized DataCite-style metadata.
  - `PUT /datasheet/{identifier}` – Update a datasheet, including title and description (authenticated).
  - `POST /v1/assets/model-cards` – Create a model card (protected asset ingest API, see below).
  - `POST /v1/assets/datasheets` – Create a datasheet (protected asset ingest API, see below).

The FastAPI app is exposed via the `rest_server` package (see `rest_server/main.py`) and is built into the Docker image `plalelab/patra-backend:latest` using `rest_server/Dockerfile` (see `scripts/build-push-backend.sh`).

#### 2. Legacy REST Server (Flask + Neo4j)

The legacy REST server is built using Flask and exposes a RESTful API for interaction with the Patra Knowledge Graph (KG) stored in Neo4j. It is retained in-repo for archive/reference purposes only and is not part of the active backend going forward.

- **Code location**: `legacy/legacy_server/`
- **Default port**: `5002`

Key endpoints include:

| Endpoint                                               | Method | Description                                                                                                  |
|--------------------------------------------------------|--------|--------------------------------------------------------------------------------------------------------------|
| `/modelcard`                                           | POST   | Create (upload) a model card.                                                                                |
| `/modelcard/{id}`                                      | GET    | Retrieve a model card.                                                                                       |
| `/modelcard/{id}`                                      | HEAD   | Return linkset relations via HTTP Link headers.                                                              |
| `/modelcard/{id}`                                      | PUT    | Update an existing model card.                                                                               |
| `/datasheet`                                           | POST   | Upload a datasheet.                                                                                          |
| `/modelcards/search?q=...`                             | GET    | Full-text search for model cards.                                                                            |
| `/modelcard/{id}/download_url`                         | GET    | Retrieve the download URL for a model artifact.                                                              |
| `/modelcards`                                          | GET    | List all model cards.                                                                                        |
| `/modelcard/{id}/deployments`                          | GET    | Retrieve deployments for a model.                                                                            |
| `/modelcard/{id}/location`                             | PUT    | Update the model's location.                                                                                 |
| `/modelcard/id`                                        | POST   | Generate a persistent model ID (PID) for author, name, version.                                             |
| `/modelcard/{id}/huggingface_credentials`              | GET    | Get Hugging Face credentials (if configured).                                                                |
| `/modelcard/{id}/github_credentials`                   | GET    | Get GitHub credentials (if configured).                                                                      |
| `/modelcard/{id}/linkset`                              | GET    | Retrieve linkset relations (same output as HEAD but with empty body & Link headers).                         |
| `/device`                                              | POST   | Register an edge device.                                                                                     |
| `/user`                                                | POST   | Register a user.                                                                                             |

#### 3. MCP (Model Context Protocol) Server, Suspended
The in-repo MCP server is Neo4j-backed legacy code retained for reference. It is not part of the active PostgreSQL backend path.

| Endpoint                                    | Type     | Description                                                                                                  |
|-------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------|
| `modelcard://{id}`                               | Resource | Retrieve a model card by ID.                                                                                 |
| `modelcard://{id}/download_url`                  | Resource | Retrieve the download URL for a model artifact.                                                              |
| `modelcard://{id}/deployments`                   | Resource | Retrieve deployments for a model.                                                                            |
| `modelcard://{id}/linkset`                       | Resource | Retrieve linkset relations for a model card.                                                                 |
| `create_edge`                                    | Tool     | Create an edge between two nodes in the Patra Knowledge graph.                                            |
| `search_modelcards`                              | Tool     | Full-text search for model cards.                                                                            |
| `list_modelcards`                                | Tool     | List all model cards.                                                                                        |
| `upload_modelcard`                               | Tool     | Upload a model card.                                                                                |
| `update_modelcard`                               | Tool     | Update an existing model card.                                                                               |
| `upload_datasheet`                               | Tool     | Upload a datasheet.                                                                                          |
| `update_model_location`                          | Tool     | Update the model's location.                                                                                 |
| `register_device`                                | Tool     | Register an edge device.                                                                                     |
| `register_user`                                  | Tool     | Register a user.                                                                                              |

The MCP server runs on port `8050` and uses Server-Sent Events (SSE) transport for communication.
