---
tags:
  - CI4AI
  - Software
title: "Smart Compiler: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for Smart Compiler. SMART Compiler lets you request C optimization and C/Python profiling in natural language."
---
# How-To Guides

## Choose a setup

| Setup | What you install on the server machine | Start here |
|---|---|---|
| Docker, recommended for a first conversation | Docker Engine/Desktop with Compose | [Natural-language tutorial](./tutorials.md#optimize-code-with-a-natural-language-request) |
| Native Linux/WSL | Python 3.11+, uv, a C toolchain, and JDK 21 | [Native setup](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-native.md) |
| Existing model host or external MCP client | A reachable model supporting tool calling, plus the running SMART server | [Connect a client](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/connect-a-client.md) |

The Docker route needs **no host Java installation, host Cetus checkout, Ollama service, or API key** for direct REST optimization and classical profiling. Docker builds Cetus with JDK 21 and runs it with a Java 21 runtime.

Keep the native Cetus installation path free of spaces, including all parent directories. Its upstream build scripts and generated launcher do not support spaces in that path. SMART's project, input, profile, and result paths can contain spaces when quoted; see the [native build instructions](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-native.md#3-build-the-pinned-cetus-checkout).

For native Linux/WSL, complete the [native setup](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-native.md) first. With the server running on port 8000, run shell examples through `uv` so they can find the project's Python interpreter:

```bash
SMART_URL=http://127.0.0.1:8000 uv run bash Testing_Examples/run_01_vector_scale.sh
```

On macOS, native Cetus optimization can fail while preprocessing Apple SDK system headers, including inputs that use `<stdio.h>`. A successful `/health` response does not verify this compiler step. Use the [Docker setup](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-with-docker.md) for affected inputs; see the [native macOS preprocessing limitation](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-native.md#macos-preprocessing-limitation) for the observed errors.

## Complete a specific task

| Task | Guide |
|---|---|
| Build images, mount source files, or manage persistent results | [Run with Docker](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-with-docker.md) |
| Install and run without Docker | [Run natively](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-native.md) |
| Use the CLI, Ollama, another model host, or an external MCP client | [Connect a client](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/connect-a-client.md) |
| Submit a profiling task, check its status, and retrieve its report in Postman | [Profile with Postman](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/profile-with-postman.md) |
| Add a custom optimization profile | [Customize profiles](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/reference/optimization-profiles.md#add-a-custom-profile) |
| Diagnose Java, networking, path, profile, or parsing errors | [Troubleshooting](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/troubleshooting.md) |

## Where are my source files?

MCP file tools run **inside the SMART server**, so paths in prompts must be visible to that server.

| Source | Path used by the server |
|---|---|
| Checked-in examples in the Docker image | `/app/Testing_Examples/01_vector_scale.c` |
| Your directory mounted into the server | The mount destination you choose, such as `/workspace/input/main.c` |
| Native server | An absolute path on the machine running the server |

`/examples` is not a built-in alias. Mounting files only into a client container does not make them available to the server.

For REST requests, `curl -F 'file=@main.c'` reads `main.c` where curl runs and uploads its contents; a source mount is unnecessary. See [Docker source mounts](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-with-docker.md#make-host-source-files-available).
