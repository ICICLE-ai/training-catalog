---
tags:
  - Foundation-AI
  - Software
  - CI4AI
title: "ScienceAgent Interface: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for ScienceAgent Interface. Science Agent helps researchers carry out tasks using ICICLE services and resources through natural language."
---
# How-To Guides

## Configure and start

Set the backend's private `.env`:

```env
DATABASE_URL=postgresql://USER:PASSWORD@DB_HOST:5432/DB_NAME
SCIENCE_AGENT_POD_URL=https://YOUR_AGENT_POD_HOST
TAPIS_BASE_URL=https://icicleai.tapis.io
TAPIS_ALLOWED_TENANTS=icicleai
SMART_LABELER_BASE_URL=https://smartlabelerbackend.pods.icicleai.tapis.io
FRONTEND_ORIGINS=https://scienceagent.pods.icicleai.tapis.io
```

Replace the database URL and service addresses with the provisioned deployment values. The DB must be reachable from the container, and its account needs table creation, alteration, and read/write permissions. For local development, set `FRONTEND_ORIGINS` to the actual local frontend origin.

`SCIENCE_AGENT_POD_TOKEN` is optional and is needed only if the agent pod gateway requires separate authentication. It does not replace the user's Tapis cookie token. S3 credentials are selected per user, not configured as global backend environment values.

Start using Docker Compose:

```sh
docker compose up -d
```

Compose downloads Python, installs the locked dependencies and source package, and starts the backend on port 8000. PostgreSQL and the agent pod are external services. Tables and migration history are initialized automatically at startup; no manual table setup is needed.

For local development instead:

```sh
uv sync
uv run uvicorn science_agent_backend.main:app --host 127.0.0.1 --port 8000
```

Use one worker in this version. API documentation is available at `/docs`; `/health` reports application availability, not remote service readiness.
