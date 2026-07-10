---
tags:
  - CI4AI
  - Software
---
# Explanation

## What IEMS is

IEMS solves fleet-scale edge AI operations. Without a control plane, deploying models to many field devices requires manual SSH access, file copies, and per-device Docker commands — slow, error-prone, and hard to audit.

IEMS replaces that with:

- A **central dashboard** (FastAPI + server-rendered HTML)
- A **device agent** on each edge node that executes commands
- **MQTT** for outbound commands (deploy, stop, restart, delete)
- **HTTPS** for inbound heartbeats and acknowledgements
- **PostgreSQL** (production) or **SQLite** (local dev) as the source of truth

## Architecture

```text
 Browser / TapisUI iframe
         │  HTTPS (Tapis OAuth or portal SSO)
         ▼
 ┌──────────────────────────┐       ┌─────────────┐
 │  Edge Control Plane      │◄─────►│ PostgreSQL  │
 │  (FastAPI, port 8765)    │       └─────────────┘
 └──────────────────────────┘
         │ MQTT commands
         ▼
 ┌──────────────────────────┐
 │  Edge devices + agents   │
 │  (Docker model containers)│
 └──────────────────────────┘
```

### Key concepts

| Term | Meaning |
|---|---|
| **Model card** | A deployable AI model plus its container spec (image, env, mounts, compatible device generations) |
| **Deployment** | One model card sent to a target (device, group, or generation) |
| **Device agent** | On-device program that runs containers and reports heartbeats |
| **Heartbeat** | Periodic device health message (CPU, memory, temperature, running containers) |

### Integrations

- **Tapis** — OAuth login, Pods hosting, tenant identity
- **Patra** — model card and artifact provenance (`PATRA_BASE_URL`)
- **MQTT broker** — command delivery to devices
- **MediaMTX / relay streaming** — live camera preview and inference streams (see `deploy/STREAMING.md`)
- **ICICLE TapisUI extension** — embeds the control plane in the ICICLE portal sidebar

### Repository layout

```text
intelligent-edge-management-service/
├── README.md                    # This file (ICICLE catalog + Diátaxis docs)
├── component-info.yaml          # ICICLE component catalog metadata
├── RELEASE.md                   # Release notes
└── edge_fleet_control_plane/    # Main application
    ├── app/                     # FastAPI app, routes, services, agent package
    ├── config/                  # Seed data (models, device generations)
    ├── deploy/                  # Pod specs, env templates, deployment guides
    ├── smart_docker_apps/       # Example edge inference containers
    ├── Dockerfile
    └── requirements.txt
```

For a longer-form briefing, read [edge_fleet_control_plane/deploy/SYSTEM_OVERVIEW.md](https://github.com/ICICLE-ai/intelligent-edge-management-service/blob/main/edge_fleet_control_plane/deploy/SYSTEM_OVERVIEW.md).
