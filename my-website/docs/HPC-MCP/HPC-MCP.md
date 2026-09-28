---
tags:
  - Software
  - AI4CI
  - Release 2026-09
---
# HPC-MCP: LLM-Assisted HPC Utility Server

HPC-MCP is a service-based ICICLE software component that gives HPC users a natural-language interface to backend HPC utilities. The current release provides distributed LLM training-time prediction for Vista and Perlmutter through HTTP endpoints and MCP clients.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/hpc-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ICICLE-ai/hpc-mcp-server?tab=MIT-1-ov-file)

</div>



## References

- Deployed service: `https://hpcmcpservercpu.pods.icicleai.tapis.io`
- MCP endpoint: `https://hpcmcpservercpu.pods.icicleai.tapis.io/mcp`
- OpenAPI specification: `docs/openapi.json`
- Live OpenAPI specification: `https://hpcmcpservercpu.pods.icicleai.tapis.io/openapi.json`
- Component metadata file: `component.yaml`
- Tapis Pod example: `tapis-pod.example.json`
- Upstream estimator: `https://github.com/ICICLE-ai/distributed_training_estimator_of_LLM`

## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Report bugs, documentation issues, or release questions through GitHub Issues:

```text
https://github.com/ICICLE-ai/hpc-mcp-server/issues
```

Release and ICICLE Training Catalog contacts:

- Carlos Guzman: `guzman.109@osu.edu`
- Amit Vyas: `vyas.154@osu.edu`
