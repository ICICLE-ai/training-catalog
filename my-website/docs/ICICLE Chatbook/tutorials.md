---
tags:
  - AI4CI
  - Software
title: "ICICLE Chatbook: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for ICICLE Chatbook. An interactive marimo notebook that turns the ICICLE AI Tapis services into a hands-on RAG (retrieval-augmented generation)…"
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
4. **Grab a Tapis access token** from [icicleai.tapis.io](https://icicleai.tapis.io) (click your username in the bottom-left → *Copy Access Token*; screenshot in [Get a Tapis access token](#get-a-tapis-access-token)), paste it into the token box, and click **🔐 Validate token**. Deployed as a Tapis pod, this step disappears — see [Sign-in: pasted token or Tapis session](#sign-in-pasted-token-or-tapis-session).
5. **Give the chat something to search** — either:
   - **Ingest a document:** paste text or upload a file, check the collection name next to the button, and click **🚀 Ingest into vector store**. The chat switches to that collection automatically; or
   - **Reuse a saved one:** in **🗂️ Your collections**, select a row and click **💬 Use in chat**. No re-ingesting needed.
6. **Ask questions** in the panel at the bottom. Each message embeds the question, retrieves and reranks the nearest chunks, stitches them into a grounded prompt, and sends it to the chat model. Ask directly for back-and-forth, or turn on the **📚 Study mode** switch to keep notes beside the conversation while you read.

### End result

A working in-browser RAG demo backed by your own document. The notebook surfaces the retrieved chunks (with their scores) under each answer so you can see exactly what the model was given.

> 💾 **Chats aren't saved in this release.** Closing the tab or letting the session expire loses the conversation — use **⬇️ Export session (.md)** to keep a copy. Your ingested collections *are* kept.
