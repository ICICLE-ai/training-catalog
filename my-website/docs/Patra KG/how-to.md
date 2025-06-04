---
tags:
  - CI4AI
  - Software
  - PADI
---

# How-To Guide

### Prerequisites

#### System Requirements
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose) installed and running.
- Open network access to the following ports:
  - `7474` (Neo4j Web UI)
  - `7687` (Neo4j Bolt)
  - `5002` (REST Server)

#### Dependencies
- **Neo4j**: Version **5.21.0-community** is deployed via Docker (manual installation is not required).

Optional:
If the system needs to support Model Card similarities, you need to obtain a valid Open AI API key. 
This is disabled by default. If you need to enable it:
- **OpenAI API Key**: Obtain and configure a valid key. Refer to the [OpenAI documentation](https://platform.openai.com) for instructions.
- **Enable Similarity**: Set the environment variable ENABLE_MC_SIMILARITY to True and set the OPENAPI_API_KEY environment variable with your obtained key.
