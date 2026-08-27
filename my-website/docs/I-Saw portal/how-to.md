---
tags:
  - Software
  - Animal-Ecology
  - Visual-Analytics
---
# How-To Guides

## Build a production bundle

```bash
npm run build
```

The static site is emitted to `dist/`. Preview the built output with:

```bash
npm run preview
```

## Type-check the project

There is no separate test suite; type-checking is the gate:

```bash
npm run lint
```

This runs `tsc --noEmit` against `tsconfig.json`.

## Build and run with Docker

The `Dockerfile` is a two-stage build: Node builds the Vite bundle, then nginx serves `dist/` on port 80 with an SPA fallback (`try_files $uri $uri/ /index.html`, see `nginx.conf`).

```bash
docker build -t i-saw-portal .
```

```bash
docker run --rm -p 8080:80 i-saw-portal
```

Then open `http://localhost:8080`.

To stamp the image with the commit it was built from, pass the build argument:

```bash
docker build --build-arg BUILD_SHA=$(git rev-parse --short HEAD) -t i-saw-portal .
```

## Deploy to ICICLE infrastructure

Deployment is automated. `.github/workflows/deploy.yaml` runs on every push to `main` (and can be triggered manually from the Actions tab) and calls the shared reusable workflow `icicle-ai/cicd-templates/.github/workflows/deploy-service.yaml@main`.

The workflow needs three repository secrets:

- `TAPIS_TOKEN`
- `REGISTRY_USERNAME`
- `REGISTRY_PASSWORD`

Service identity and runtime come from `icicle-service.yaml`:

| Field | Value |
| --- | --- |
| `service-name` | `i-saw-frontend` |
| `service-version` | `0.1.0` |
| `project-name` | `icicle-project` |
| `pod-name` | `isawfrontendprod` |
| `runtime-type` | `node-frontend` |
| `runtime-version` | `24.18` |

Bump `service-version` in that file when you cut a new release.

## Configure environment variables

Copy the example file if you need local overrides:

```bash
cp .env.example .env
```

`.env.example` documents `GEMINI_API_KEY` and `APP_URL`, which the AI Studio hosting environment injects at runtime. Neither variable is read by the current `src/` code — the portal builds and runs without a `.env` file. Never commit real secrets.

## Disable hot module reload

Agent-driven editing environments can flicker under HMR. Set `DISABLE_HMR=true` before starting the dev server to turn off both HMR and file watching (see `vite.config.ts`):

```bash
DISABLE_HMR=true npm run dev
```

## Work on the right files (team ownership)

This repository enforces per-tab file ownership to avoid merge conflicts. Before editing, check `CLAUDE.md` for the current rules:

| Tab | Owner | Primary file |
| --- | --- | --- |
| 1 — Infrastructure / Vision | All team members | `src/components/TabVision.tsx` |
| 2 — Smart Honeypot & Analytics | Manas | `src/components/TabSandbox.tsx` |
| 3 — Onboarding Hub | Jacob | `src/components/TabOnboarding.tsx` |

`src/App.tsx` and `src/components/CanvasBackground.tsx` are global; change them only with team agreement.

## Troubleshooting

- **Port 3000 already in use** — edit the `dev` script in `package.json`, or run `npx vite --port=3001`.
- **A route 404s behind your own web server** — the app is a client-side SPA. Rewrite unknown paths to `index.html`, as `nginx.conf` does.
- **`npm run lint` fails after adding a package** — install the matching `@types/*` package.
- **New dependency rejected in review** — the project deliberately limits itself to React, Tailwind, `lucide-react`, and `motion`. Add heavier libraries only with team sign-off.
