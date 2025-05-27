---
tags:
  - CI4AI
---

# How-To Guides

## Setting up cetus

### Requirements

For being able to set up and run cetus, the following tools are required.

1. Java JDK 1.8+ (JDK + JRE)
2. GCC 

### From packed binaries
For packed binaries, you will see the following files:
1. configure.sh
2. ```lib``` folder with:
   1. rsyntaxtextarea.jar
   2. smart-profiler.jar

For setting up the binaries we recommend to run the ```configure.sh``` within the same folder, it is located. 
It will create the ```profile.sh``` file, a single bash command to run the jar files properly.

Then we recommend setting up the main folder (i.e. ｐrofiler-release-1.0.0) to your PATH variable so you can call ```profiler.sh``` anywhere
when using the command line.

## Features

### Preprocessing C programs.
Cetus uses cpp preprocessor. If your program depends on several headers or is a multiple directories project, you can set the ```CPATH``` env variable and this will be used by the preprocessor.

### Cetus-Profiler.
Cetus profiler is a set of tools that performs static analysis of C programs.

### How to use it      
To activate static profiling within Cetus, you need to pass the flag -program_analysis

```bash
cetus -program-analysis program.c

# or if you have the ./profiler.sh
./profiler.sh -program-analysis program.c
```


Cetus will export the result of the static analysis into a CSV file. For this purpose, it is **required** to create a folder called **out** inside the workplace you will run Cetus program analysis.

### Extra parameters

For choosing the output file for the resulting static analysis you need to use the following flag:

```bash
-program-features-output=/path/to/directory/myoutput.csv
## Set output file for program features e.g., -program-features-output=myoutput.csv
```

if ```program-features-output``` is not set, Cetus will expect a folder called ```out``` and it will store the profiling results there in a CSV file.

If you desire to append the results of newly analyzed programs to a current CSV file containing information, you need to pass the following flag to Cetus
```bash
-append-program-features=true
## Change filemode to append to the output file for program featurese.g., -append-program-features=true
```

## Test cases
To test the validity of profiler binaries, we have provided several examples within the folder ```resources/profiler/tests```.

To validate the output of the tool, you need to verify the folder ```profiler/tests/test-results```, it has pre-generated profiling results from the examples in the ```tests``` folder. 

If the folder out does not exist, it is required to create it, by default the compiler will use the folder ```out``` in the current ($pwd) folder.

