---
tags:
  - Software
  - Animal-Ecology
  - Visual-Analytics
---
# Explanation

## What I-SAW is

I-SAW ("Infrastructure for Sensing and Analytics on Wildlife") is an edge-networked wildlife observation stack. Its centerpiece is a **smart honeypot** — an open, see-through bird feeder with no cameras inside it, so birds stay in unobstructed natural context while surrounding sensors do the observing.

Three ideas drive the design:

- **Cross-modal wake-ups ("Bullseye Ambush").** Ultra-low-power audio sentinels listen continuously and wake high-power camera traps over a local MQTT channel only when something is detected. Power, not compute, is the binding constraint in the field.
- **Three-step verification.** A visit is confirmed by (1) visual detection from wide-angle AI edge cameras, (2) audio matching of bird song against species call libraries, and (3) footfall sensors on each perch proving a physical landing. Any one channel alone produces false positives; agreement across three modalities does not.
- **Privacy at the edge.** Reduction happens on-device, so raw imagery and audio need not leave the deployment site. Only reduced observations travel onward to the hosted cyberinfrastructure.

## What this repository is

This repository is the **portal**, not the sensing stack. It is a static React single-page app whose job is communication and conversion: explain the project to NSF program managers and K-12 camp counselors, demonstrate the analytics value with a realistic mockup, and hand developers a concrete next step. All sensor data in the sandbox is synthetic and generated in the browser.

## Architecture

```
index.html
└── src/main.tsx                     React 19 entry point
    └── src/App.tsx                  Layout, header, footer, tab state
        ├── components/CanvasBackground.tsx   Animated background (global)
        ├── components/TabVision.tsx          Tab 1 — vision & pillars
        ├── components/TabSandbox.tsx         Tab 2 — honeypot, analytics, drone
        └── components/TabOnboarding.tsx      Tab 3 — quick start, DIY, kit request
```

Tab state is a single `useState` in `App.tsx`; there is no router, no global store, and no data-fetching layer. Each tab owns its own sub-tab state locally. That flatness is intentional — it lets three people edit three files without stepping on each other.

Supporting files:

| File | Role |
| --- | --- |
| `vite.config.ts` | Vite + React + Tailwind v4 plugin, `@` path alias, HMR kill-switch |
| `Dockerfile` / `nginx.conf` | Two-stage build; nginx serves the SPA |
| `icicle-service.yaml` | ICICLE service identity and runtime declaration |
| `.github/workflows/deploy.yaml` | Deploys via the shared ICICLE CI/CD template |
| `CLAUDE.md` | Team ownership rules and design conventions |

## Design choices

- **Static over dynamic.** With no backend, the portal ships as an nginx-served bundle, deploys in seconds, and never exposes a data path that could leak field observations.
- **Tailwind-only visualization.** The dashboards, heatmaps, and feeder illustrations are hand-built with Tailwind utilities and inline SVG rather than a charting library. This keeps the bundle small, keeps the visuals on-brand ("nature meets edge AI": deep forest greens, stone/slate darks, glowing emerald accents), and avoids dependency churn in a repo edited by several people at once.
- **Client-side file generation.** `setup-drone.sh` and `backpack-config.json` are assembled in the browser with a `Blob` and an object URL, so downloads work with zero server involvement.
- **Motion, used sparingly.** `motion/react` handles tab cross-fades and slide transitions only.
- **A deliberately narrow dependency set.** React, Tailwind, `lucide-react`, and `motion`. New heavy dependencies require team permission.
