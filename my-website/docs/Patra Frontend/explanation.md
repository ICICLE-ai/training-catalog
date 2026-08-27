---
tags:
  - CI4AI
  - PADI
---
# Explanation

Patra Frontend is the web interface for the Patra AI Cards framework, giving users a way to browse, search, submit, and edit model cards and datasheets without calling the [Patra Knowledge Base](https://github.com/Plale-Lab/patra-knowledge-base) API directly.

- **Browse & filter** model cards and datasheets with search, category, framework, and visibility filters
- **Detail views** with model metadata, deployment history, accuracy rings, and DataCite-style datasheet rendering
- **Inline editing** (logged-in users) — edit all model card fields, AI model metadata, and datasheet properties directly from the detail page
- **Tapis OAuth2 login** via sidebar — two access tiers: anyone can browse public records; signed-in Tapis users also see private records and the Contribute section (Submit / Edit / Ask Patra)
- **Embedded ICICLE/Tapis login** through a strict, memory-only parent-portal handshake
- **Submit** new model cards and datasheets to Patra
- **Ask Patra** — conversational assistant that answers from the catalog and cites the records it references
- **Experiments** — browse edge-deployed experiments (Animal Ecology, Digital Agriculture) with per-image scoring data and power metrics
- **MCP Explorer** — connect to the Model Context Protocol server, browse tools, and execute them

### Embedded login integration

When enabled inside an iframe, Patra requests a short-lived Tapis token from
the parent portal using protocol-v1 `postMessage`. The response is accepted
only from `window.parent`, from an exact configured origin, and with the
matching single-use request ID. The portal token remains memory-only and takes
precedence over a persisted standalone session.

The parent portal must verify the exact Patra origin and iframe window, then
reply with `event.source.postMessage(response, event.origin)`. Never use `"*"`,
place tokens in URLs, persist handoff tokens, or log raw tokens.

Top-level Patra deployments retain standalone login. In embedded mode, a
failed or invalid parent handshake produces a controlled parent-session error
instead of exposing a second Patra login prompt or reusing a stale standalone
identity. API requests prefer `Authorization: Bearer <token>` and do not send
browser-derived username or role headers as authoritative identity. See
[docs/login_redesign.md](https://github.com/ICICLE-ai/patra-frontend/blob/main/docs/login_redesign.md) for the complete protocol,
portal handler, backend requirements, and verification checklist.
