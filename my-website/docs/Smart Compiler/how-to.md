---
tags:
  - CI4AI
---

# How-To Guides

## Running the project
For running the project, once all dependencies and configurations are set, run the following command:

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


### Explanation

Details about the smart compiler can be found on the following diagramas:
- **Diagrams**:  
  - [Diagram 1](https://drive.google.com/file/d/1S5gRxw_vizR1XnmbiZnAH1yZnkB8Ep0_/view?usp=drive_link)  
  - [Diagram 2](https://drive.google.com/file/d/1tgCcINlzBUe6A1PCNX6R_ftAnb9WidcA/view?usp=sharing)


## Internal Notes

### To extract Modelfile

```ollama show --modelfile llama3.1 > Modelfile```

### To create from Modelfile

```ollama create llama3.1-tool -f Modelfile```