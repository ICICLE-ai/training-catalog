---
tags:
  - CI4AI
  - PADI
---
# How-To Guides

### Hosted deployments (Tapis Pods)

The frontend is deployed as a [Tapis Pod](https://tapis.readthedocs.io/en/latest/technical/pods.html)
in the ICICLE tenant. If you only want to use Patra, go here — no local setup required:

| Deployment | URL | Backend |
| ---------- | --- | ------- |
| Patra UI (stable) | `https://patra.pods.icicleai.tapis.io` | `https://patrabackend.pods.icicleai.tapis.io` |
| Patra UI (dev) | `https://patra-dev.pods.icicleai.tapis.io` | `https://patrabackend-dev.pods.icicleai.tapis.io` |

Both pods run the same `plalelab/patra-frontend` image; they differ only in runtime
configuration. Supporting services:

- MCP server — `https://patramcp.pods.icicleai.tapis.io`
- Tapis tenant (login) — `https://icicleai.tapis.io`

See [docs/DEPLOYMENT_TOPOLOGY.md](https://github.com/ICICLE-ai/patra-frontend/blob/main/docs/DEPLOYMENT_TOPOLOGY.md) for the per-pod environment,
and [docs/pod-config.patra-prod.json](https://github.com/ICICLE-ai/patra-frontend/blob/main/docs/pod-config.patra-prod.json) /
[docs/pod-config.patra-dev.json](https://github.com/ICICLE-ai/patra-frontend/blob/main/docs/pod-config.patra-dev.json) for complete pod payloads.
The image serves nginx on **port 80** — the pod's `networking.default.port` must match, or the
ingress returns `502 Bad Gateway`.

### Prerequisites

- Node.js 20+ (Vite 7)
- The Patra backend running on port `8000`

### Install

```bash
npm --prefix app install
```

### Run

```bash
cd app
npm run dev
```

The app opens at `http://localhost:5173`.

### Configuration

Create `app/.env` (see `app/.env.example`):

```env
VITE_LIVE_API_BASE_URL=http://localhost:8000
VITE_MCP_BASE_URL=http://localhost:8050
VITE_EMBEDDED_AUTH_ENABLED=false
VITE_PORTAL_AUTH_ORIGINS=
VITE_PORTAL_AUTH_TIMEOUT_MS=3000
```

To run the local UI against a hosted backend instead of a local one:

```env
VITE_LIVE_API_BASE_URL=https://patrabackend.pods.icicleai.tapis.io
VITE_MCP_BASE_URL=https://patramcp.pods.icicleai.tapis.io
```

Note that the stable and dev backends share one database — writes from a local dev server
pointed at either pod are writes against production data.

Feature areas (Ask Patra, Agent Toolkit, MCP Explorer, Domain Experiments) are gated by `VITE_SUPPORTS_*` flags — see `app/.env.example`.

### Configuring embedded login for deployment

Configure deployed containers at runtime:

```env
EMBEDDED_AUTH_ENABLED=true
PORTAL_AUTH_ORIGINS=https://portal.example.org
PORTAL_AUTH_TIMEOUT_MS=3000
```

A production runtime example for `https://icicleai.tapis.io` is provided in
[`docs/pod-config.patra-prod.json`](https://github.com/ICICLE-ai/patra-frontend/blob/main/docs/pod-config.patra-prod.json).
