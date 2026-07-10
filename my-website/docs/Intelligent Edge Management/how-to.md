---
tags:
  - CI4AI
  - Software
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
