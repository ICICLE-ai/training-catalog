---
tags:
  - AI4CI
  - Software
---
# Tutorials

## Run the RAG playground end-to-end

This tutorial walks a first-time user from a clean checkout to chatting with their own document.

### Prerequisites

- macOS or Linux shell (the commands below are zsh/bash).
- [`uv`](https://docs.astral.sh/uv/) installed (`brew install uv` on macOS).
- A free account on the [ICICLE AI Tapis portal](https://icicleai.tapis.io) — TACC login, CILogon (university SSO), or self-signup all work.

### Steps

1. **Clone and enter the repo.**
   ```bash
   git clone https://github.com/thevyasamit/icicle-chatbook.git
   cd icicle-chatbook
   ```
2. **Sync the environment.** `uv` reads `pyproject.toml` + `uv.lock` and creates `.venv/` with `marimo` and `requests` pinned.
   ```bash
   uv sync
   ```
3. **Launch the notebook in app mode** (code hidden, chat-style UI):
   ```bash
   uv run marimo run notebooks/rag_chat_marimo.py
   ```
   Or in editor mode (code visible, hot-reload) while developing:
   ```bash
   uv run marimo edit notebooks/rag_chat_marimo.py
   ```
4. **Grab a Tapis access token** from [icicleai.tapis.io](https://icicleai.tapis.io) (click your username in the bottom-left → *Copy Access Token*), paste it into the token box, and click **🔐 Validate token**.
5. **Ingest a document** — paste any text into the textarea, then click **🚀 Ingest into vector store**.
6. **Ask questions** in the chat panel at the bottom. Each message embeds the question, retrieves the top-K nearest chunks, stitches them into a grounded prompt, and sends it to the chat model.

### End result

A working in-browser RAG demo backed by your own document. The notebook surfaces the retrieved chunks under each answer so you can see exactly what the model was given.
