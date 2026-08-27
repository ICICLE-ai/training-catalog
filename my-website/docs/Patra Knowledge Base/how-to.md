---
tags:
  - CI4AI
  - Software
  - PADI
---
# How-To Guides

### Prerequisites

#### System Requirements
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose) installed and running.
- Open network access to the following ports:
  - `8000` (Primary REST API)
  - `5002` (legacy Flask server, suspended)
  - `8050` (legacy MCP server, suspended)

#### Dependencies
- **PostgreSQL**: Required for the active FastAPI backend.
- **Neo4j**: Legacy-only dependency retained for archived code paths; not required for new backend work.
- [Optional] **OpenAI API Key**: If the system needs to support Model Card similarities, you need to obtain a valid Open AI API key. Refer to the [OpenAI documentation](https://platform.openai.com) for instructions. This is disabled by default.


### 1. Set up Environment Variables

**Model Similarity (Optional)**  
To enable model similarity detection using OpenAI embeddings, set `ENABLE_MC_SIMILARITY` to `True` and provide your OpenAI API key:
```bash
export ENABLE_MC_SIMILARITY=True
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

**Hugging Face Integration (Optional)**  
To upload models and artifacts to Hugging Face, create a repository and generate an access token. Then, set the following environment variables:
```bash
export HF_HUB_USERNAME=<your-hf-username>
export HF_HUB_TOKEN=<your-hf-access-token>
```
Requires write access to the target Hugging Face repo.

**GitHub Integration (Optional)**  
To upload models and artifacts to GitHub, create a repository and generate an access token. Then, set the following environment variables:
```bash
export GH_HUB_USERNAME=<your-github-username>
export GH_HUB_TOKEN=<your-github-personal-access-token>
```
Requires `repo` scope enabled on the GitHub token.

### 2. Clone the repository and start services
```bash
git clone https://github.com/Plale-Lab/patra-knowledge-base.git
cd patra-knowledge-base
docker compose -f docker-compose.backend.yml up --build
```
  
The supported service stack is the PostgreSQL-backed FastAPI app under `rest_server/`, started with `docker-compose.backend.yml`.
Legacy Neo4j compose assets remain in the repository for archival reference only and should not be treated as the supported deployment path.

- To shut down services, use:
    ```bash
    docker compose -f docker-compose.backend.yml down
    ```

### 3. Creating Model Cards and Datasheets (Asset Ingest API)

External systems and partner organizations publish and manage model cards and datasheets through the protected asset ingest API on the primary REST server, mounted under `/v1/assets`:

| Endpoint                          | Method | Description                                                |
|------------------------------------|--------|--------------------------------------------------------------|
| `/v1/assets/model-cards`           | POST   | Create a model card.                                          |
| `/v1/assets/datasheets`            | POST   | Create a datasheet.                                            |
| `/v1/assets/model-cards/{asset_id}`| PATCH  | Update an existing model card.                                 |
| `/v1/assets/datasheets/{asset_id}` | PATCH  | Update an existing datasheet.                                  |
| `/v1/assets/records`               | GET    | List/search model cards and datasheets available for editing.  |

**Authentication**: send one of the following on every request:
- `X-Asset-Org: <org>` + `X-Asset-Api-Key: <secret>` (or `Authorization: Bearer <secret>`) — org/secret pairs are configured via the `PATRA_ASSET_INGEST_KEYS_JSON` environment variable.
- `X-Tapis-Token: <token>` — used by the Patra frontend for logged-in user submissions.

For brevity, the examples below set the org/key headers once as shell variables:
```bash
export PATRA_URL=http://localhost:8000
export ASSET_ORG=<your-org>
export ASSET_KEY=<your-secret>
```

**Create a model card:**
```bash
curl -X POST "$PATRA_URL/v1/assets/model-cards" \
  -H "X-Asset-Org: $ASSET_ORG" \
  -H "X-Asset-Api-Key: $ASSET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "External Model",
    "version": "1.0",
    "short_description": "Injected model card",
    "author": "Org A",
    "ai_model": {
      "name": "External Model Binary",
      "version": "1.0",
      "framework": "PyTorch",
      "model_type": "cnn",
      "model_metrics": {"top_1_accuracy": 0.92}
    }
  }'
```
Returns `201 Created` with `{"asset_type": "model_card", "asset_id": <int>, "asset_uuid": <uuid>, "organization": "...", "created": true}`. A duplicate (same name/version/author) returns `409 Conflict`.

**Create a datasheet:**
```bash
curl -X POST "$PATRA_URL/v1/assets/datasheets" \
  -H "X-Asset-Org: $ASSET_ORG" \
  -H "X-Asset-Api-Key: $ASSET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "publication_year": 2025,
    "version": "1.0",
    "titles": [{"title": "Partner Dataset"}],
    "creators": [{"creator_name": "Org A"}]
  }'
```
Returns `201 Created` with `{"asset_type": "datasheet", "asset_id": <int>, ...}`, or `409 Conflict` on a duplicate.

**Update a model card or datasheet** (`PATCH`, full replacement of the asset's editable fields — send the complete payload, not a partial diff):
```bash
curl -X PATCH "$PATRA_URL/v1/assets/model-cards/123" \
  -H "X-Asset-Org: $ASSET_ORG" \
  -H "X-Asset-Api-Key: $ASSET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "External Model",
    "version": "1.1",
    "short_description": "Updated description",
    "author": "Org A"
  }'
```
```bash
curl -X PATCH "$PATRA_URL/v1/assets/datasheets/456" \
  -H "X-Asset-Org: $ASSET_ORG" \
  -H "X-Asset-Api-Key: $ASSET_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "publication_year": 2025,
    "version": "1.1",
    "titles": [{"title": "Partner Dataset (revised)"}],
    "creators": [{"creator_name": "Org A"}]
  }'
```
Returns `200 OK` with `{"asset_type", "asset_id", "organization", "updated": true}`.

**List/search editable records:**
```bash
curl -G "$PATRA_URL/v1/assets/records" \
  -H "X-Asset-Org: $ASSET_ORG" \
  -H "X-Asset-Api-Key: $ASSET_KEY" \
  --data-urlencode "q=titanic" \
  --data-urlencode "limit=20"
```
Returns `200 OK` with a JSON array of `{"asset_type", "asset_id", "title", "subtitle", "description", "kind_label", "updated_at"}`, covering both model cards and approved datasheets, newest-updated first. `q` is optional (omit it to list recent records) and `limit` defaults to 20 (max 100).

See `rest_server/asset_create_models.py` for the full set of optional fields (e.g. `bias_analysis`, `xai_analysis`, DataCite-style datasheet fields like `subjects`, `dates`, `funding_references`), and `examples/model_cards/` / `examples/datasheets/` for larger sample payloads.

### 4. Using the MCP Server (Optional)

This section describes the suspended in-repo Neo4j-based MCP server for archival/reference purposes only. It is not part of the active PostgreSQL backend and should not be used for new integrations.

The legacy MCP server provides:
- **4 Resources** for reading model card data by identifier
- **10 Tools** for operations, queries, and state modifications

**For Claude Desktop:**
1. Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

For the legacy archived MCP server:
```json
{
  "mcpServers": {
    "patra-kg": {
      "url": "http://localhost:8050/sse"
    }
  }
}
```

**For Custom AI Agents:**
Connect to the MCP server endpoint:
- MCP Server: `http://localhost:8050/sse` (legacy archived endpoint)

**Historical Example Usage:**

*With MCP Server:*
```
User: "Upload this model card and then search for similar models"
AI Assistant: [Uses upload_modelcard tool, then search_modelcards tool]
Result: Model card uploaded and similar models found
```

*Reading model card data:*
```
User: "Get information about model card test-mc-123"
AI Assistant: [Reads modelcard://test-mc-123 resource]
Result: Returns complete model card data
```
