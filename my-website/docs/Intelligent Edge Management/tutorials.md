---
tags:
  - CI4AI
  - Software
  - AI4CI
title: "Intelligent Edge Management: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for Intelligent Edge Management. The Intelligent Edge Management Service (IEMS) is ICICLE's fleet control plane for deploying and operating AI…"
---
# Tutorials

## Tutorial: Run the control plane locally

This walkthrough starts the Edge Fleet Control Plane on your laptop for development and smoke testing.

### Prerequisites

- Python 3.12+
- `git`
- (Optional) Docker, for building images or running edge model containers

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/ICICLE-ai/intelligent-edge-management-service.git
   cd intelligent-edge-management-service/edge_fleet_control_plane
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure local development**

   ```bash
   cp .env.example .env
   ```

   For local dev, keep `LOCAL_DEV_AUTH=true` (default in `.env.example`). This bypasses Tapis OAuth and logs you in as `local_tapis_user`.

4. **Start the server**

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open the dashboard**

   Visit [http://localhost:8000](http://localhost:8000). You should see the ICICLE Edge Control Plane dashboard.

6. **Run the smoke test (optional)**

   ```bash
   python tests/smoke_test.py
   ```

### Expected result

The dashboard loads, you can browse devices, model cards, and deployments. SQLite stores data under `data/edge_control_plane.db`.

---

## Tutorial: Access IEMS from the ICICLE portal (TapisUI)

The ICICLE TapisUI extension embeds the control plane in an iframe and passes the user's Tapis JWT via a `postMessage` handshake.

### Prerequisites

- A running TapisUI dev instance or access to `https://icicleai.tapis.io`
- Valid ICICLE tenant credentials
- Control plane deployed with `TAPIS_PORTAL_ORIGINS` including your TapisUI origin

### Steps

1. Log in to TapisUI on an ICICLE tenant (`https://icicleai.tapis.io` or local dev with `VITE_TAPIS_BASE_URL` set to an ICICLE URL).
2. Open the sidebar entry **Intelligent Edge Management Service**.
3. The portal iframe loads `https://edgecontrolplane.pods.icicleai.tapis.io` and exchanges a signed auth token with the parent window.
4. You are signed in to the control plane without a separate login prompt.

### Expected result

The full control plane UI appears inside TapisUI. If you see "Invalid JWT", log out of TapisUI and log back in to refresh the token.
