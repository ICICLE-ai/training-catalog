---
tags:
  - CI4AI
---

# How-To Guides
## Running the project
For running the project, once all dependencies and configurations are set, run the following command:

## SERVER

Run the server

```bash
python src/server_main.py

```

## CLIENT
Run the client

```bash
python src/main.py

```

Then the smart compiler will ask the user to provide the folder of the project that the user will be working on. Please provide a path example : /home/directory/projectAI

Then the smart compiler will ask which specific file will the smart compiler work on: type the name fo the file, exmaple : api_server.py

Then the smart compiler will ask which specific task to do: Profile or Optimize. Type what you would like to do with the program.

### USE CASE
```bash
python src/main.py

Please provide the folder of your project: /home/user/Desktop/SmartCompiler/examples/jacobi-2d
Please provide the file you want to analyze: main.c
File 'main.c' found in the project.

What do you want to do with the file? (Profile or Optimize): Profile
```
The profile information or the optimize C application will be stored in the same folder where the target project is located.

## Running from containers
### Building images.
Build the smart compiler server and client by running the scripts:

```bash
docker build -f Server_dockerFile -t smart_server . #For SERVER
docker build -f Client_dockerfile -t smart_client . #For Client
```

**Note:** By default, the dockerfiles are configured for localhost deploy. If you are planning to deploy it in a distributed architecture, you need to make sure on setting up the proper env variables inside the dockerfiles.

### Running containers
For running the smart server you can run the following script.
```bash
docker run -d --name smart_server -p 8000:8000 smart_server #Server
docker run -it --name smart_client -p 8001:8001 smart_client #Client. Remember -it

```