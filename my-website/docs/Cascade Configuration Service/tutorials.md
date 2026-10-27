---
tags:
  - Software
title: "Cascade Configuration Service: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for Cascade Configuration Service. A Streamlit-based demo for the Cascade Configuration Service."
---
# Tutorials

## Running the Cascade Configuration Service Locally

### 1. Clone the repository

```bash
git clone https://github.com/ICICLE-ai/Cascade-Configuration-Service.git
cd Cascade-Configuration-Service
```

### 2. Install `uv`

This project uses `uv` for Python dependency management.

If `uv` is not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart the terminal or run:

```bash
source $HOME/.local/bin/env
```

Verify the installation:

```bash
uv --version
```

### 3. Install the project dependencies

```bash
uv sync
```

### 4. Start the service

Run the Streamlit application using:

```bash
uv run streamlit run src/cascade_configuration_service/app.py
```

By default, the application will be available at:

```text
http://localhost:8501
```

Open this address in a web browser to access the Cascade Configuration Service.

### 5. Run using the deployment entry point

The service can also be started using the deployment entry point:

```bash
PORT=8000 ./entrypoint.sh
```

The application will then be available at:

```text
http://localhost:8000
```
