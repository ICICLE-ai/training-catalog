---
tags:
  - CI4AI
---

# Tutorials

This Smart Compiler uses AI models and traditional compiler techniques to enhance the performance scalability of C programs and Python programs. By profiling, and finding approaches for optimizations.

# Sofwate Requirements

## Install the project
For dependency management and installation, this project uses ```uv```.
See [Astral Documentation](https://docs.astral.sh/uv) for installing the uv package manager.


## Project dependencies

### Packages
After installing **uv** run: ```uv sync``` for syncing project dependencies.

### Ollama
To deploy a LLM using ollama first we need to install Ollama by following 
its [Official Documentation](https://ollama.com).

Once Ollama is installed deploy the Ollama server (if it was not deployed by the installation).



### Quick Ollama deploy
1. Serve the Ollama server: ```ollama serve``` (if it is not already deployed).
2. Create LLM model using the SmartCompiler Modelfile: ```ollama create llama3.1-smart-compiler -f ollama-smart-compiler-Modelfile```.
3. Run the created LLM: ```ollama run llama3.1-smart-compiler:latest```.
4. If it opens a chat after running the LLM, just type ```/bye``` to close that chat.

#### Setting up Environment variables
Set up the environment variables in a ```.env``` file.
An example of how this file looks like.
```
# .env
OLLAMA_MODEL=llama3.1-smart-compiler:latest
OLLAMA_HOST=http://localhost:11434
MCP_SERVER_SCRIPT_PATH=<project_folder>/src/server_main.py
MCP_SERVER_TRANSPORT=stdio
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
MCP_SERVER_TRANSPORT=stdio
MCP_SERVER_OLLAMA_MODEL=llama3.1:latest
LOG_LEVEL=INFO # OR DEBUG
```

Then type : export $(cat .env | xargs)