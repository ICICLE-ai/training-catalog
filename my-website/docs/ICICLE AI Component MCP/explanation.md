---
tags:
  - Software
title: "ICICLE AI Component MCP: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for ICICLE AI Component MCP. ICICLE AI Component MCP lets developers use AI-powered IDEs to explore ICICLE components and then implement…"
---
# Explanation

## Overview

Core concepts:
- The server fetches a YAML catalog over HTTPS and exposes MCP tools and resources.
- Tools return compact summaries, while resources expose full component records.

Architecture:
- `server.py` defines the FastMCP server and tool handlers.
- An HTTP session handles retries and timeouts for the catalog fetch.
- Transport is stdio; messages are JSON-RPC 2.0 between the client and server.

Design decisions:
- stdio transport keeps integration simple for IDE-based MCP clients.
- Compact list/search responses reduce payload size and latency.

Conceptual flow:
```
[MCP Client] <-> stdio/JSON-RPC 2.0 <-> [FastMCP Server] -> HTTPS -> [Catalog YAML]
```
