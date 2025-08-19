---
tags:
  - CI4AI
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


## Running the project
For running the project, once all dependencies and configurations are set, run the following command:

### SERVER

Run the server

```bash
python src/run_server.py

```

### CLIENT
Run the client.

Note: This client is a simple version that extends Llama model for using tools. Since the client is not robust enough, we encourage you using other more robust tools such as Claude desktop, Copilot or ChatGPT with MCP tools.

Smart compiler client is a PoC.

```bash
python src/run_client.py

```

Then the smart compiler will ask the user to provide the folder of the project that the user will be working on. Please provide a path example : /home/directory/projectAI

Then the smart compiler will ask which specific file will the smart compiler work on: type the name fo the file, exmaple : api_server.py

Then the smart compiler will ask which specific task to do: Profile or Optimize. Type what you would like to do with the program.



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
