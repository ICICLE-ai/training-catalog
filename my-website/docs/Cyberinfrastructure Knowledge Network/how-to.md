---
tags:
  - CI4AI
  - Software
  - PADI
---

# How-To Guide

See the full [documentation](https://cyberinfrastructure-knowledge-network.readthedocs.io/en/latest/) for detailed instructions on creating custom plug‑ins and streaming events to the knowledge graph.

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose) installed and running.
- Open network access to the following ports:
  - `7474` (Neo4j Web UI)
  - `7687` (Neo4j Bolt)
  - `2181` (ZooKeeper)
  - `9092` (Kafka Broker)
  - `8083` (Kafka Connect)
  - `8502` (CKN dashboard)

## Quick‑Start

1. **Clone the repository and start services**

   ```bash
   git clone https://github.com/Data-to-Insight-Center/cyberinfrastructure-knowledge-network.git
   make up
   ```

   After setup completes, verify that all modules are running:

   ```bash
   docker compose ps
   ```

2. **Stream an example camera‑trap event**

   ```bash
   docker compose -f examples/docker-compose.yml up -d --build
   ```

   * View the streamed data on the CKN dashboard: [http://localhost:8502/Camera\_Traps](http://localhost:8502/Camera_Traps)

   * Access the Neo4j Browser: [http://localhost:7474/browser/](http://localhost:7474/browser/) (username `neo4j`, password `PWD_HERE`). Run:

     ```cypher
     MATCH (n) RETURN n;
     ```

   * Shut down services:

     ```bash
     make down
     docker compose -f examples/docker-compose.yml down
     ```
