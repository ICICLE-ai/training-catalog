---
tags:
  - CI4AI
title: "Smart Compiler: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for Smart Compiler. This project introduces an agentic approach for high-level and multi-purpose compilers."
---

# How-To Guides

## Install the project
For dependency management and installation, this project uses ```uv```.
See [Astral Documentation](https://docs.astral.sh/uv) for installing the uv package manager.


## Project dependencies

### Create a virtual environment

In order to make a safe installation on the system, it is suggested to create a virtual envionment and install all the packages in this VE.
Let's create a virtual environment called SmartCompiler.
`python -m venv SmartCompiler`

Now, let's initiallize the virtual environment.
`source SmartCompiler/bin/activate`


### Packages
After installing **uv** run: ```uv sync``` for syncing project dependencies. 


If you do not want to use `uv` for dependencies maangement, you can install dependencies from the **requirements.txt** file. 
You can run `pip install -r requirements.txt` 

### Ollama
To deploy a LLM using ollama first we need to install Ollama by following 
its [Official Documentation](https://ollama.com).

Once Ollama is installed deploy the Ollama server (if it was not deployed by the installation).


### Quick Ollama deploy
1. Serve the Ollama server: ```ollama serve``` (if it is not already deployed).
2. Create LLM model using the SmartCompiler Modelfile: ```ollama create llama3.1-smart-compiler -f ollama-smart-compiler-Modelfile```.
3. Run the created LLM: ```ollama run llama3.1-smart-compiler:latest```.
4. If it opens a chat after running the LLM, just type ```/bye``` to close that chat.

#### Useful notes
##### To extract a Modelfile with ollama

```ollama show --modelfile llama3.1 > Modelfile```

###### To create from Modelfile with ollama

```ollama create llama3.1-tool -f Modelfile```



#### Setting up Environment variables
Set up the environment variables in a ```.env``` file.
An example of how this file looks like.
```
# For client, see envs/.client.example.env
# .env
LOG_LEVEL=INFO
OLLAMA_MODEL=llama3.1-smart-compiler:latest
OLLAMA_HOST=http://localhost:11434
MCP_SERVER_URL=http://localhost:8000/sse
ALLOWED_PATHS="/mnt/d/workspace/python/smart-compiler/examples"
```
In order to activate these client environment varibles , we must type :

`set -o allexport; source .env; set +o allexport`



```
For Server, see envs/.server.example.env
LOG_LEVEL=INFO
OLLAMA_MODEL=llama3.1:latest
OLLAMA_HOST=http://localhost:11434
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
MCP_SERVER_TRANSPORT=sse
ENABLE_REST_API=true
ALLOWED_PATHS="/mnt/d/workspace/python/smart-compiler/examples"

```
In order to activate these server environment varibles , we must type :

`set -o allexport; source .env; set +o allexport`

we can aslo do it with: export $(cat .env | xargs) on Linux to load the env variables or just source in Windows


## Option 1:  Running the project without Docker
For running the project, once all dependencies and configurations are set, run the following command:

### Cetus compiler

SMART uses Cetus as a separate compiler. Get it from the [Cetus project](https://github.com/PAROT-Udel/The-Cetus-Project). To clone and build it, run:

```bash
git clone https://github.com/PAROT-Udel/The-Cetus-Project.git
cd The-Cetus-Project
./build.sh bin
```

If you download an archive instead, extract it and run `./build.sh bin` from the extracted project root (the directory containing `build.sh`).

The build creates the Cetus launcher at `bin/cetus`. Set `CETUS` to the absolute path of that executable, for example `/path/to/The-Cetus-Project/bin/cetus`. Keep the checkout intact because the launcher uses supporting files from the same Cetus directory.

### SERVER (without Docker)

Before starting SMART, set `CETUS` to the absolute path of the `bin/cetus` executable built above, and set `CETUS_PROFILES_FILE` to the SMART-COMPILER profile file. Both variables are required for optimization requests; `CETUS_TIMEOUT_SECONDS` is optional and defaults to 300 seconds.

```bash
export CETUS="/path/to/The-Cetus-Project/bin/cetus"
export CETUS_PROFILES_FILE="/path/to/SMART-COMPILER/config/profiles.json"
export CETUS_TIMEOUT_SECONDS=300

# Confirm both configured paths exist and are usable.
test -x "$CETUS" || { echo "Cetus is missing or not executable: $CETUS"; exit 1; }
test -r "$CETUS_PROFILES_FILE" || { echo "Profiles file is missing or unreadable: $CETUS_PROFILES_FILE"; exit 1; }

python src/run_server.py
```

Replace the example paths with paths on the machine running SMART. Do not rely on a checked-in Cetus location. Docker Compose has its own host-path setup below.

### CLIENT
Run the client.

Note: This client is a simple version that extends Llama model for using tools. Since the client is not robust enough, we encourage you using other more robust tools such as Claude desktop, Copilot or ChatGPT with MCP tools.

Smart compiler client is a PoC.

```bash
python src/run_client.py

```

The client displays `You:` and accepts a natural-language request directly. It does not prompt separately for a project folder or file name. When asking it to optimize a file, include that C file's absolute path and the optimization profile. Replace `/path/to/SMART-COMPILER` in these examples with the location of your checkout.

Examples:

- **Parallelization:** `Please optimize the C file at /path/to/SMART-COMPILER/Testing_Examples/01_vector_scale.c using the parallel profile.`
- **Tiling:** `Please optimize the C file at /path/to/SMART-COMPILER/Testing_Examples/03_matrix_multiply.c using the paw_tiling_nt profile.`
- **Loop interchange:** `Please optimize the C file at /path/to/SMART-COMPILER/Testing_Examples/05_loop_interchange.c using the loop_interchange profile.`

To profile a code snippet, include its C source in the request, for example:

```text
Profile this C program and summarize its performance:
<paste C source here>
```


## Option 2: Cetus optimizer runtime (Docker Compose)

The server image includes a Java runtime for Cetus. Before starting Compose, set the host paths to the built Cetus checkout and SMART-COMPILER profile JSON. The checkout is mounted read-only at the absolute path embedded in its generated `bin/cetus` launcher; set `CETUS_CONTAINER_DIR` to that path. The profile file is mounted read-only into the server container. These values are supplied at runtime rather than baked into the image.

```bash
export CETUS_HOST_DIR="/path/on/host/The-Cetus-Project"
export CETUS_CONTAINER_DIR="/path/embedded/The-Cetus-Project"
export CETUS="$CETUS_CONTAINER_DIR/bin/cetus"
export CETUS_PROFILES_HOST_FILE="/path/on/host/SMART-COMPILER/config/profiles.json"
docker compose up -d --build
```

Replace the example paths with locations on your machine. `CETUS_CONTAINER_DIR` must match the checkout path embedded in the Cetus launcher. These shell exports do not modify an existing `.env` file or other user configuration. Compose passes `CETUS` and mounts the profile file as `CETUS_PROFILES_FILE` inside the server container.

The server keeps uploaded inputs, transformed outputs, and task records in named volumes mounted at `/app/files` and `/app/db`, so they survive container recreation.

## Invoking the Cetus optimizer

The optimizer accepts C source and applies one named profile from `SMART-COMPILER/config/profiles.json`. Available profiles are `parallel`, `paw_tiling_nt`, `paw_tiling_lrw`, `paw_tiling_fixed32`, `reuse_analysis`, and `loop_interchange`.

### MCP

Call the `optimize_code_snippet` tool with the C source and a profile. For example:

```json
{
  "code_snippet": "#include <stdio.h>\nint main(void) { return 0; }\n",
  "optimization_profile": "parallel"
}
```

The tool returns the transformed C source as text.

### REST API

Upload a `.c` file to `POST /tasks` as multipart form data. For example:

```bash
curl --fail -X POST http://localhost:8000/tasks \
  -F "task_type=optimize" \
  -F "language=c" \
  -F "optimization_profile=paw_tiling_nt" \
  -F "file=@input.c"
```

The response includes `task_id` and `task_status`. Poll `GET /tasks/{id}` until the status is `completed` or `failed`. On success, use `task_result.file_path` to download the transformed source:

```bash
FILE_PATH="<copy task_result.file_path from the response>"
curl --fail --get http://localhost:8000/files/download \
  --data-urlencode "file_path=${FILE_PATH}" \
  --output optimized.c
```

If the task fails, inspect `task_result.error` in the response.

`Regression-Test` checks transformed code against expected output and builds/runs benchmark programs for correctness. It does not measure execution speed or select the fastest profile; compare benchmark timings separately when evaluating performance.

## Option A: Running from a single container
### Building image.
Build the smart compiler server, client and Ollama by running the script:
```bash
docker compose up -d --build
```

### Start an interactive sesion.
```bash
docker attach smart_client
```

Start playing with the Smart Compiler!

## IMPORTANT NOTE: 

In case thwere is an error that says : "llama3.1-smart-compiler:latest" not found"
Type the following commands:
```bash
docker compose exec ollama sh -lc 'ollama pull llama3.1'
docker compose exec ollama sh -lc 'ollama create llama3.1-smart-compiler -f /workspace/ollama-smart-compiler-Modelfile'
```
And then restart the client:

```bash
docker compose restart client
```

and 

### Start an interactive sesion.
```bash
docker attach smart_client
```

Start playing with the Smart Compiler!


## Option B: Running from a two different containers

### Building images.

Build the smart compiler server and client by running the scripts:

```bash
docker build -f Dockerfile -t smart_server . #For SERVER
docker build -f Client_dockerfile -t smart_client . #For Client
```

**Note:** By default, the dockerfiles are configured for localhost deploy. If you are planning to deploy it in a distributed architecture, you need to make sure on setting up the proper env variables inside the dockerfiles.

### Running containers
For running the smart server you can run the following script.
```bash
docker run -d --name smart_server -p 8000:8000 smart_server #Server
docker run -it --name smart_client -p 8001:8001 smart_client #Client. Remember -it

```
