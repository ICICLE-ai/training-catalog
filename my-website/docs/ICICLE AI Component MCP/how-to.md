---
tags:
  - Software
---
# How-To Guides

## Search by keyword

Problem:
- Find components matching a query string.

Steps:
1) Ask the IDE chat to search the catalog.

Example:
```
User: Find ICICLE components related to Foundation AI.
Assistant: I found 7 components. Here are the top 3: [component list...]
```
JSON tool call (advanced):
```json
{"tool": "search_components", "args": {"query": "Foundation AI"}}
```

Tips:
- Use broader terms to increase recall.

Troubleshooting:
- If results are empty, verify network access and catalog URL.

## Filter by release

Problem:
- List components for a target release.

Steps:
1) Ask the IDE chat to list components for a release.

Example:
```
User: List all ICICLE components in release 2025-07.
Assistant: I found 42 components in 2025-07. Here are the first 10: [component list...]
```
JSON tool call (advanced):
```json
{"tool": "list_components", "args": {"target_release": "2025-07"}}
```

Tips:
- Combine `primary_thrust` and `public_access` for narrower results.

Troubleshooting:
- If the request times out, retry or increase `CATALOG_TIMEOUT`.
