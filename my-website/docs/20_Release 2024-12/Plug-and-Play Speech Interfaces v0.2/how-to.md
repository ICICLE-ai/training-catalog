---
tags:
  - Foundation-AI
---

# How-To Guides

## Installation

To set up the environment, follow these steps:

1. Create a virtual environment and install the required packages:

    ```bash
    python3.11 -m venv server
    source server/bin/activate
    pip install -r requirements.txt
    ```

    - If you are using the Nemo-based ASR model, use the following requirements file:

    ```bash
    pip install -r requirements_wx_nemo.txt
    ```

2. Add the following lines to `server/bin/activate` to ensure that the necessary libraries are accessible:

    ```bash
    export LD_LIBRARY_PATH=/path/to/environment/server/lib64/python3.11/site-packages/nvidia/cublas/lib:/path/to/environment/server/lib64/python3.11/site-packages/nvidia/cudnn/lib
    ```

    If you are using the Nemo version, also add the following:

    ```bash
    export CPATH=$HOME/python-dev/include:$CPATH
    ```

3. If Java 11.0 is not installed, set up the Java environment variables. Add the following to `server/bin/activate`:

    ```bash
    export JAVA_HOME=/path/to/java/installation/jdk-11.0.16.1+1
    export PATH=$JAVA_HOME/bin:$PATH
    ```
4. If ffmpeg 7.0.2 is not installed, you may need to download it from [here](https://ffmpeg.org/download.html#releases) and build it locally. Then, set up the enivronment variables:
    ```bash
    export JAVA_HOME=/path/to/java/installation/jdk-11.0.16.1+1
    export FFMPEG=/path/to/ffmpeg/installation/ffmpeg-7.0.2/build
    export PATH=$JAVA_HOME/bin:$FFMPEG/bin:$PATH
    ```
   ffmpeg 7.0.2 is very important to have if we want to make API calls to this server from the Safari browser.

Make sure to replace `/path/to/environment/` and `/path/to/java/installation/` with the actual paths to your environment and Java installation.

## Files Description

- `whisperx_model.py`: Contains the model definition.
- `whisperx_handler.py`: Handles data input/output operations.
- `archive.sh`: Used to create the `.mar` file for the model in the `model_store` folder.
- `config*.json`: Configuration for corresponding models.
- `client_webpage.html`: An example of a client-side HTML file to send audio this torchserve server and getting the transcription

## Browser integration

- The ASR models are being hosted right now on the slatelab server (need to change at some point)
- Port forwarding needed. First run `ssh -L 8080:localhost:8080 user@cse-d01187744s.coeit.osu.edu`
- Then run `client_webpage.html`. You will see a page like below.
![Alt text](https://raw.githubusercontent.com/ICICLE-ai/speech-server/main/webpage_look.png)

## Model Update Process

To update the model:

1. **Always archive the model first** by running:

    ```bash
    ./archive.sh
    ```

2. After archiving, **start the server** by running:

    ```bash
    ./start_server.sh
    ```

To stop the server, run:

```bash
./stop_server.sh
