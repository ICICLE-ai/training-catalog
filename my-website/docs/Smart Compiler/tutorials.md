---
tags:
  - CI4AI
  - Software
title: "Smart Compiler: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for Smart Compiler. SMART Compiler lets you request C optimization and C/Python profiling in natural language."
---
# Tutorials

## Optimize code with a natural-language request

**Goal:** type a request into SMART's conversational client and receive optimized C code.

The example below uses Docker and a local Ollama model. **Prerequisites:** Docker Engine/Desktop with Compose and a SMART-COMPILER checkout. Docker supplies the server, Cetus, Java 21, the model service, and the client; this local-model route needs no API key.

If you already have a native SMART server or another model host, use the [native client instructions below](#use-a-native-client-or-another-model-host) or the [client connection guide](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/connect-a-client.md).

For a better natural-language experience, we recommend a model with strong instruction-following and tool-calling capabilities. More capable models can help SMART interpret your requests and use the optimization and profiling tools more reliably.

### 1. Start SMART, the model service, and the client

Run this from your SMART-COMPILER checkout:

```bash
LLM_HOST=http://ollama:11434/v1 \
LLM_MODEL=llama3.1-smart-compiler:latest \
OPENAI_API_KEY= \
docker compose --profile llm up -d --build

docker compose --profile llm ps -a
docker compose --profile llm logs --tail=50 ollama_init
```

The first initialization downloads the base Llama model and creates `llama3.1-smart-compiler`. Wait for the server to become healthy and `ollama_init` to finish successfully before continuing. The explicit model settings above keep this Docker example independent of native-client settings in a host `.env`.

### 2. Open the chat terminal

Attach to the running interactive client:

```bash
docker compose attach --sig-proxy=false client
```

Enter natural-language requests in this attached terminal at the client's **`You:`** prompt. The client may already be waiting for input when you attach, so the prompt may have been printed before attachment. If the terminal is blank, type your request and press Enter; subsequent turns will display `You:`.

### 3. Type your optimization request at `You:`

The client prints the `You:` prefix; type the message after it, or start typing if the initial prompt is not visible:

```text
You: Please optimize the C file at /app/Testing_Examples/01_vector_scale.c using the parallel profile.
```

The model can read the file through SMART's MCP tools and call the optimization tool. Cetus runs inside the SMART server, and the client displays the returned C code in the conversation. Save that returned text if you want a file; MCP optimization does not create a persistent REST task result.

**Your prompt → language model → MCP tools → Cetus → optimized code in the client.**

The `/app/Testing_Examples` path is inside the Docker server. For your own C files, [mount their directory into the server](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-with-docker.md#make-host-source-files-available) and use the server-visible path in your prompt. See [available profiles](./explanation.md#available-optimization-profiles) for other optimization choices.

Use **Ctrl-p, Ctrl-q** to detach and return to your shell while leaving the client running, or type `quit` to stop the client. The [client guide](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/connect-a-client.md) explains how to restart it. The REST and shell-script examples below are separate automated runs you can perform from your shell.

### Use a native client or another model host

Complete the [native setup](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/run-native.md) and [client configuration](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/connect-a-client.md) first. Keep the SMART server and chosen model service running. Configure `MCP_SERVER_URL`, `LLM_HOST`, and `LLM_MODEL` for those services; set `OPENAI_API_KEY` only when the provider requires it.

In another terminal, from the SMART-COMPILER project root, start the client:

```bash
uv run --env-file .env python src/run_client.py
```

At its **`You:`** prompt, use the file's actual absolute path on the server. Replace the placeholder prefix in this example:

```text
You: Please optimize the C file at /absolute/path/to/SMART-COMPILER/Testing_Examples/01_vector_scale.c using the parallel profile.
```

For a Docker client using an existing model service instead of the bundled Ollama service, follow [Docker client with an existing model service](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/how-to/connect-a-client.md#docker-client-with-an-existing-model-service). Requests are entered at the same `You:` prompt.

## REST API and automated validation

Use this route for direct API access and repeatable checks. These requests and `.sh` scripts call SMART's REST API without an LLM or a natural-language prompt.

Run the following commands at your **shell prompt**, after detaching from or quitting the conversational client. They assume the SMART-COMPILER checkout as the working directory and require curl on the host.

If you completed the Docker conversation above, the server is already running. Otherwise, start the server-only deployment:

```bash
docker compose up -d --build
```

Check the REST endpoint and bundled compiler:

```bash
curl --fail http://127.0.0.1:8000/health

docker compose exec server java -version
docker compose exec server sh -lc '"$CETUS" -version'
```

If the health check runs before startup finishes, wait for `docker compose ps` to show a healthy server and retry it.

### Submit a REST request

This uploads a source file from the checkout on the machine running curl:

```bash
curl --fail-with-body -X POST http://127.0.0.1:8000/tasks \
  -F 'task_type=optimize' \
  -F 'language=c' \
  -F 'optimization_profile=parallel' \
  -F 'file=@Testing_Examples/01_vector_scale.c'
```

The response contains a task ID. Follow the [API reference](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/reference/api.md) to poll its status and download the result.

### Run the automated `.sh` examples

The included runner makes its own REST optimization request, downloads the generated C, compiles the original and transformed programs, and compares their output:

```bash
docker compose exec -e OMP_NUM_THREADS=2 server sh -lc \
  'cd /app/Testing_Examples && SMART_URL=http://127.0.0.1:8000 ./run_01_vector_scale.sh'
```

Success includes:

```text
PASS 01_vector_scale.c [parallel]: checksum=14999950000
```

This verifies the example's output equivalence. Inspect the transformed C to confirm the intended transformation; measure timings separately when evaluating performance.

Continue with the [complete REST validation tutorial](https://github.com/ICICLE-ai/SMART-COMPILER/blob/main/docs/tutorials/first-optimization.md), including output retrieval and all eight runs.
