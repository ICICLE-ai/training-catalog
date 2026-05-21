---
tags:
  - AI4CI
  - Software
---
# How-To Guides

## Get a Tapis access token

1. Visit [icicleai.tapis.io](https://icicleai.tapis.io) and sign in (TACC account, fresh signup, or CILogon).
2. Click your **username** in the bottom-left corner.
3. Choose **Copy Access Token** and paste the JWT into the notebook.

![Where to copy your Tapis access token in the ICICLE AI portal](https://raw.githubusercontent.com/ICICLE-ai/icicle-chatbook/main/assets/access_token_ss.png)

> ⏰ Tokens expire after ~4 hours. If you start seeing `401 Token expired`, refresh the token from the Tapis UI and paste it again.

## Tune ingestion behaviour

Open the *⚙️ Ingestion settings* accordion in the notebook:

- **Collection / Topic / Source** — namespacing inside the vector store. Use a distinct collection per project so retrieval doesn't bleed across documents.
- **Chat model** — switch between `llama4-17b`, `llama-3-70b`, and `mistral-7b`.
- **Top-K retrieval** — how many chunks to pull back per question. Raise it for broader context; lower it to keep prompts tight.
- **Max chunk tokens / Chunk overlap tokens** — chunking budget. Larger chunks preserve more context per vector; overlap reduces "split at a bad spot" misses.

## Preload a token via environment variable

Skip the paste step by exporting `TAPIS_TOKEN` before launching marimo — the token input prefills from `os.environ["TAPIS_TOKEN"]`.

```bash
export TAPIS_TOKEN="eyJ..."
uv run marimo run notebooks/rag_chat_marimo.py
```

## Reset the local environment

If dependencies get out of sync or you want a clean rebuild:

```bash
rm -rf .venv uv.lock
uv sync
```
