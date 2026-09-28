---
tags:
  - CI4AI
  - AI4CI
  - Software
  - Release 2026-05
  - Release 2026-09
---
# ICICLE AI Vector Service

FastAPI + Qdrant vector storage and retrieval service for the **ICICLE AI** Tapis tenant. Clients provide their own pre-computed embeddings — the service handles storage, filtered search, and reranking.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/icicle-ai-vector-service)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0)

</div>

:::tip API reference
This component exposes an HTTP API — see its [API documentation](/api/ICICLE%20Vector%20DB%20Service/icicle-ai-vector-service) on this site.
:::



Every request is authenticated with a Tapis access token, and `user_id` is taken from the token's `tapis/username` claim — never from the request body. Each user's collections are separate Qdrant collections, so users cannot see or affect each other's data, and each can choose their own embedding model and vector dimension.


## References

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tapis Project](https://tapis-project.org/)
- [Diataxis Framework](https://diataxis.fr/)

## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue Reporting

Please report issues via [GitHub Issues](https://github.com/ICICLE-ai/icicle-ai-vector-service/issues). Include steps to reproduce, expected behavior, and any relevant logs.
