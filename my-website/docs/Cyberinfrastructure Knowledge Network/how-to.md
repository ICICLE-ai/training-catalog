---
tags:
  - CI4AI
  - Software
  - PADI
---
# How-To Guides

See the full [documentation](https://cyberinfrastructure-knowledge-network.readthedocs.io/en/latest/) for detailed instructions on creating custom plug‑ins and streaming events to the knowledge graph.

### Hosted Patra endpoints (Tapis Pods)

CKN itself is self‑hosted — you run the broker, knowledge graph, and dashboard on your own
infrastructure via `make up`. The [Patra Knowledge Base](https://github.com/Plale-Lab/patra-knowledge-base)
it reports model provenance to is hosted as [Tapis Pods](https://tapis.readthedocs.io/en/latest/technical/pods.html)
in the ICICLE tenant:

| Service | URL |
| ------- | --- |
| Patra REST API (stable) | `https://patrabackend.pods.icicleai.tapis.io` |
| Patra REST API (dev) | `https://patrabackend-dev.pods.icicleai.tapis.io` |
| Patra UI | `https://patra.pods.icicleai.tapis.io` |
| Tapis tenant | `https://icicleai.tapis.io` |

Point `patra_agent` and any Patra‑integrated plugin at the stable REST API. Writes require a
Tapis token from `https://icicleai.tapis.io/v3/oauth2/tokens`; the stable and dev backends share
one database, so treat writes to either as production writes.

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose) installed and running.
- Open network access to the following ports:
  - `7474` (Neo4j Web UI)
  - `7687` (Neo4j Bolt)
  - `2181` (ZooKeeper)
  - `9092` (Kafka Broker)
  - `8083` (Kafka Connect)
  - `8502` (CKN dashboard)

### Quick‑Start

#### 1. Clone the repository and start services

```bash
git clone https://github.com/Plale-Lab/cyberinfrastructure-knowledge-network.git
make up
```

After setup completes, verify that all modules are running:

```bash
docker compose ps
```

#### 2. Stream an example camera‑trap event

```bash
docker compose -f examples/docker-compose.yml up -d --build
```

View the streamed data on the [CKN dashboard](http://localhost:8502/Camera_Traps) or open the [neo4j browser](http://localhost:7474/browser/) and log in with the credentials mentioned in the docker-compose file. Run `MATCH (n) RETURN n` to view the streamed data.

Shut down services using:
```bash
make down
docker compose -f examples/docker-compose.yml down
```
