---
tags:
  - CI4AI
  - Software
title: "Smart Compiler: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for Smart Compiler. SMART Compiler lets you request C optimization and C/Python profiling in natural language."
---
# Explanation

The SMART server exposes compiler tools and owns the files those tools read. Cetus runs on that server and transforms C source according to its selected profile. A model host and conversational client are optional: direct REST optimization and classical profiling can call the tools without a model.

## Architecture diagram

![SMART Compiler architecture showing the conversational client, model service, MCP and REST APIs, compiler tools, and an external system](https://raw.githubusercontent.com/ICICLE-ai/SMART-COMPILER/main/diagrams/architecture.png)

The diagram illustrates a local Ollama deployment. Other compatible model hosts can fill the model-service role; Cetus and the profilers run through the SMART server's tools. The [IMT integration diagrams](./Smart%20Compiler.md#references) show the connection with ICICLE Middleware and Tools.

The Docker image builds Cetus and supplies its Java 21 runtime together, keeping the compiler's embedded paths and Java compatibility consistent. A native installation supplies that compiler checkout and toolchain separately.

The bundled CLI and external MCP clients are alternative ways to connect to the server; an editor does not require the bundled CLI to run alongside it. See the [architecture explanation](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/explanation/architecture.md) for component roles, request flow, input/header limitations, and the difference between correctness checks and performance measurement.

---

# Reference

| Technical reference | Contents |
|---|---|
| [Configuration](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/reference/configuration.md) | Client/server environment variables, defaults, runtime paths, and update behavior |
| [Optimization profiles](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/reference/optimization-profiles.md) | `profiles.json` fields, available profiles, custom entries, and tuning assumptions |
| [REST and MCP APIs](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/reference/api.md) | Tool arguments, file uploads, task polling, downloads, and output persistence |

## Available optimization profiles

| Profile | Purpose |
|---|---|
| `parallel` | OpenMP parallelization, including dependence, privatization, and reduction analyses |
| `paw_tiling_nt` | Parallel-aware tiling using NT tile selection |
| `paw_tiling_lrw` | Parallel-aware tiling using LRW/FindB tile selection |
| `paw_tiling_fixed32` | Parallel-aware tiling with fixed tile size 32 |
| `reuse_analysis` | Parallelization with explicit reuse-vector analysis |
| `loop_interchange` | Loop interchange with OpenMP generation disabled |

These entries are editable in SMART's own `config/profiles.json`. Read the [profile schema and customization guide](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/reference/optimization-profiles.md) before changing them. Upstream Cetus also supports subscripted-subscript analysis; SMART does not currently ship a dedicated profile or example for that analysis.
