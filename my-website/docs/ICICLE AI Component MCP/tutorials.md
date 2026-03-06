---
tags:
  - Software
---
# Tutorials

## Get started

Prerequisites:
- Python 3.10+
- Internet access to fetch the catalog YAML

Steps:
1) Create and activate a virtual environment.
```bash
python3 -m venv .venv
source .venv/bin/activate
```
2) Install dependencies.
```bash
pip install -r requirements.txt
```
3) Run the MCP server.
```bash
python server.py
```
4) Connect your MCP client to the stdio server (Cursor MCP settings).

Expected results:
- MCP tools like `list_components` and `search_components` return catalog data.

## Connect from Cursor or Claude Desktop

Prerequisites:
- The server is installed and runnable with `python server.py`.

Steps (Cursor):
1) Create a local MCP config file at `.cursor/mcp.json`.
```json
{
  "mcpServers": {
    "icicle-catalog": {
      "command": "./.venv/bin/python",
      "args": ["./server.py"]
    }
  }
}
```
2) In Cursor, open MCP settings and enable the `icicle-catalog` server.
3) In chat, ask a question like: "List components in release 2025-07."

Steps (Claude Desktop):
1) Create a local MCP config file at `.claude/mcp.json`.
```json
{
  "mcpServers": {
    "icicle-catalog": {
      "command": "./.venv/bin/python",
      "args": ["./server.py"]
    }
  }
}
```
2) Enable the server in Claude Desktop MCP settings.
3) Ask: "Search components for Foundation AI."

Expected results:
- The IDE can call tools like `list_components` and `search_components` directly from chat.

Example chat request and response:
```
User: Show me ICICLE components related to Foundation AI.
Assistant: I found 7 components. Here are the top 3: [component list...]
```
