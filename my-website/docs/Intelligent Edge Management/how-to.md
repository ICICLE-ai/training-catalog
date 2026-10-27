---
tags:
  - CI4AI
  - Software
  - AI4CI
title: "Intelligent Edge Management: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for Intelligent Edge Management. The Intelligent Edge Management Service (IEMS) is ICICLE's fleet control plane for deploying and operating AI…"
---
# How-To Guides

## How to deploy a new control-plane release on Tapis Pods

1. **Build and push the Docker image** for `linux/amd64` (required on Tapis Pods):

   ```bash
   cd edge_fleet_control_plane
   export IMAGE=YOUR_DOCKERHUB_USER/edge-control-plane:vNEXT
   chmod +x deploy/build-and-push.sh
   PUSH=true ./deploy/build-and-push.sh
   ```

2. **Allowlist the image** in Tapis Pods → Images for your tenant.

3. **Update secrets** in `deploy/env.production` (copy from `deploy/env.production.example`). Never commit real secrets.

4. **Update the pod spec** in `deploy/pod-edgecontrolplane.json`:
   - Set `image` to your new tag
   - Copy environment variables from `deploy/env.production`

5. **Register the OAuth callback** on the Tapis OAuth client `icicle-edge-control-plane`:

   ```text
   https://edgecontrolplane.pods.icicleai.tapis.io/auth/callback
   ```

6. **Create or update the pod** via the Tapis Pods UI or API.

7. **Verify** health at `https://edgecontrolplane.pods.icicleai.tapis.io/api/health`.

See [edge_fleet_control_plane/deploy/DEPLOY.md](https://github.com/ICICLE-ai/intelligent-edge-management-service/blob/main/edge_fleet_control_plane/deploy/DEPLOY.md) for troubleshooting (image allowlist, env var length limits, empty `command` arrays).

---

## How to enroll an edge device

1. In the control plane UI, go to **Devices → Register device**.
2. Follow the setup wizard to install the device agent on the Jetson (or supported hardware).
3. The agent enrolls over HTTPS, receives its identity, and subscribes to MQTT command topics.
4. Confirm the device appears online on the dashboard (heartbeats within `DEVICE_OFFLINE_AFTER_SECONDS`).

Agent install scripts live under `edge_fleet_control_plane/app/agent_package/`.

---

## How to deploy a model to a device

1. **Publish a model card** — define the container image, environment variables, mounts, ports, and compatible device generations.
2. **Select a deployment target** — a single device, a device group, or a device generation.
3. **Click Deploy** — the control plane records the deployment, publishes an MQTT command, and tracks status (`DELIVERING` → `RUNNING`).
4. **Monitor** the deployment detail page; status polls update automatically.
5. **Stop, restart, or delete** as needed. *Stop* keeps cached images on the device; *Delete* removes containers and portal records.

Example smart Docker apps (UNet live inference) are under `edge_fleet_control_plane/smart_docker_apps/`.

---

## How to configure portal iframe authentication

Set these environment variables on the control plane pod:

| Variable | Purpose |
|---|---|
| `TAPIS_PORTAL_ORIGINS` | Comma-separated parent origins allowed to embed IEMS (e.g. `http://localhost:3000,https://icicleai.tapis.io`) |
| `SESSION_SAME_SITE` | Set to `none` for cross-site iframe cookies in HTTPS production |
| `TAPIS_BASE_URL` | ICICLE tenant base URL |
| `TAPIS_CLIENT_ID` / `TAPIS_CLIENT_KEY` | OAuth client credentials |

The portal and control plane exchange messages using protocol version `1`:

- Request: `iems:portal-auth:request`
- Response: `iems:portal-auth:response` (includes Tapis `accessToken`)

Implementation: `edge_fleet_control_plane/app/static/js/portal-auth.js` (control plane) and `tapis-ui/packages/icicle-tapisui-extension/src/pages/IntelligentEdgeManagementService/` (portal).
