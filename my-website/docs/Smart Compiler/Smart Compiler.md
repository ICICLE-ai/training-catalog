---
tags:
  - CI4AI
  - Release 2025-05
  - Release 2025-08
  - Release 2026-10
  - Software
---
# SMART Compiler 3.0

SMART Compiler lets you request **C optimization** and **C/Python profiling** in natural language. Its conversational client connects a tool-capable language model to SMART's Model Context Protocol (MCP) tools, which run Cetus and the profilers. You can also call the server directly through its REST API for automation and testing.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/SMART-COMPILER)
[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-yellow.svg)](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/LICENSE)

</div>


This release adds Cetus profiles for OpenMP parallelization, parallel-aware tiling, loop interchange, and reuse-vector analysis. The Docker server image includes a pinned Cetus `release/3.0` build and **Java 21**. Native installations build Cetus separately.


## References

- [Cetus compiler source and documentation](https://github.com/PAROT-Udel/The-Cetus-Project)
- [Docker Compose documentation](https://docs.docker.com/compose/)
- [uv installation and dependency management](https://docs.astral.sh/uv/)
- [Ollama documentation](https://docs.ollama.com/) for the optional local model service
- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
- [IMT integration diagram 1](https://drive.google.com/file/d/1S5gRxw_vizR1XnmbiZnAH1yZnkB8Ep0_/view?usp=drive_link)
- [IMT integration diagram 2](https://drive.google.com/file/d/1tgCcINlzBUe6A1PCNX6R_ftAnb9WidcA/view?usp=sharing)
- [Diátaxis](https://diataxis.fr/), the framework used to separate tutorials, task guides, explanation, and technical reference

## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Report bugs, setup failures, and documentation problems through [SMART Compiler GitHub Issues](https://github.com/ICICLE-ai/SMART-COMPILER/issues). Include:

- The SMART revision, Docker or native setup, operating system, and architecture.
- The command or prompt, optimization profile, and a minimal input that reproduces the issue.
- Relevant error output and, for compiler failures, the Java and Cetus versions. Redact API keys and tokens from logs.

Check [troubleshooting](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/troubleshooting.md) for known Java, networking, source-path, and parser errors before reporting a new issue.
