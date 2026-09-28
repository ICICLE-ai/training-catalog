---
tags:
  - AI4CI
  - Software
  - Release 2026-05
  - Release 2026-09
---
# ICICLE AI Chatbook

An interactive [marimo](https://marimo.io/) notebook that turns the ICICLE AI Tapis services into a hands-on RAG (retrieval-augmented generation) playground. Paste or upload a document (**PDF**, **DOCX**, **TXT**, **MD**, up to 2 MB) and chat against it — or come back later and chat against a collection you saved before. Every step is visible, from embeddings and chunking to retrieval, reranking, grounded prompting and LLM-as-judge evaluation, so newcomers to RAG can see how each piece works.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/icicle-chatbook)
[![License: GPL 3.0](https://img.shields.io/badge/License-GPL%203.0-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Launch on ICICLE AI Tapis](https://img.shields.io/badge/Launch-ICICLE%20AI%20Tapis-blue?style=flat-square)](https://icicleai.tapis.io/#/icicle-chatbook)

</div>



## References

- [ICICLE AI Tapis portal](https://icicleai.tapis.io) — where you log in and grab an access token.
- [Embedding service (`icicleaiembedserver`)](https://github.com/ICICLE-ai/icicle-ai-embed-service) — Qwen3-Embedding behind a JWT-gated FastAPI.
- [Vector service (`icicleaivecserver`) API docs](https://github.com/ICICLE-ai/icicle-ai-vector-service) — Qdrant-backed store with private per-user collections, cosine retrieval, and reranking (MMR, cosine rescore, cross-encoder).
- [marimo documentation](https://docs.marimo.io/) — the reactive Python notebook used to host this playground.
- [uv documentation](https://docs.astral.sh/uv/) — the package/env manager used to bootstrap the project.

## Acknowledgements

<!-- Please include other funding sources above this line. -->

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

File bugs, ideas, or questions on the [GitHub issues page](https://github.com/thevyasamit/icicle-chatbook/issues).
