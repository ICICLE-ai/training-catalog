---
tags:
  - CI4AI
  - Release 2025-05
  - Release 2025-08
  - Release 2026-10
---
# Smart Compiler Infrastructure

This project introduces an agentic approach for high-level and multi-purpose compilers.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/SMART-COMPILER)
[![License: BSD_3](https://img.shields.io/badge/License-BSD_3-yellow.svg)](https://opensource.org/license/BSD-3-clause)

</div>


This release connects that workflow to [Cetus](https://github.com/PAROT-Udel/The-Cetus-Project) optimization capabilities for C programs: parallel-aware tiling (PAW Tiling) to improve cache locality while preserving data dependencies and supporting parallel execution; improved loop interchange that checks legality and uses reuse analysis to choose loop order, including for symbolic loop bounds; and subscripted-subscript analysis for supported indirect accesses such as A[B[i]], helping identify additional parallelization opportunities.

![Version](https://img.shields.io/badge/Version-3.0-green)


## References

- To deploy a LLM using ollama first we need to install Ollama by following 
its [Official Documentation](https://ollama.com)

## Acknowledgements

- National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)
