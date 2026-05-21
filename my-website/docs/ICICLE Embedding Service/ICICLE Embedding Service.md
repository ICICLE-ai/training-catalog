---
tags:
  - CI4AI
  - AI4CI
  - Software
  - Release 2026-05
---
# ICICLE AI Embed Service

FastAPI service that turns text into embedding vectors using **Qwen3-Embedding-0.6B** (GGUF quantized) via **llama-cpp-python**, designed for the **ICICLE AI** Tapis tenant. The service runs the model locally — no external API calls — so a single `.gguf` file plus a Tapis token is everything a deployment needs.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/icicle-ai-embed-service)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0)

</div>

:::tip API reference
This component exposes an HTTP API — see its [API documentation](/api/ICICLE%20Embedding%20Service/icicle-ai-embed-service) on this site.
:::



Pairs with the [ICICLE AI Vector Service](https://github.com/ICICLE-ai/icicle-ai-vector-service): this service produces vectors, that service stores and searches them.


## References

- [Qwen3-Embedding model card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)
- [Qwen3-Embedding GGUF repo](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tapis Project](https://tapis-project.org/)
- [Diataxis Framework](https://diataxis.fr/)

## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue Reporting

Please report issues via [GitHub Issues](https://github.com/ICICLE-ai/icicle-ai-embed-service/issues). Include steps to reproduce, expected behavior, and any relevant logs.
