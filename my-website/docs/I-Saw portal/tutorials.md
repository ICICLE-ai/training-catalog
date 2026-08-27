---
tags:
  - Software
  - Animal-Ecology
  - Visual-Analytics
---
# Tutorials

## Run the portal locally

This walkthrough takes you from a fresh clone to the portal running in your browser.

### Prerequisites

- **Node.js 20 or newer** (the Docker build uses `node:20-alpine`; the ICICLE service definition targets Node 24)
- **npm** (ships with Node.js)
- Git

### Steps

1. **Clone the repository and enter it.**

   ```bash
   git clone https://github.com/ICICLE-ai/I-SAW_Portal.git
   cd I-SAW_Portal
   ```

2. **Install dependencies.**

   ```bash
   npm install
   ```

3. **Start the development server.**

   ```bash
   npm run dev
   ```

   Vite serves the app on port `3000` and binds to `0.0.0.0`, so it is reachable both at `http://localhost:3000` and from other machines on your network.

4. **Open `http://localhost:3000`** in a browser.

### What you should see

A dark, full-screen single-page app with an animated canvas background and a three-tab header:

| Tab | Header label | Contents |
| --- | --- | --- |
| 1 | Project Vision & Strategic Pillars | The I-SAW mission plus three pillars — Networking, Smart Sensing, Innovative Hardware |
| 2 | Data Sandbox & Functional Capabilities | Sub-tabs for *The Smart Honeypot*, *Analytics*, and *Gesture Drone Control* |
| 3 | Onboarding Hub | Sub-tabs for *Quick Start*, *DIY Hardware*, and *Request Kit* |

On narrow screens the tab bar collapses into a dropdown selector.

## Take the guided tour of the sandbox

1. Open **Data Sandbox & Functional Capabilities → The Smart Honeypot.** Step through the honeypot slideshow to see the feeder illustration, the sensor deployment map, and the three-stage confirmation pipeline (visual detection → audio confirmation → footfall confirmation).
2. Switch to **Analytics.** You get metric cards (total visits, species detected, feed time, peak activity), a visits-over-time chart, an activity heatmap, a species visit summary table, and smart alerts — all rendered with Tailwind utilities and inline SVG, no charting library.
3. Switch to **Gesture Drone Control** for the interactive command matrix and the detection-engine specs.
4. Move to the **Onboarding Hub → Quick Start** and click *Get Deployment Package*. The browser generates and downloads `setup-drone.sh` client-side.
5. In **DIY Hardware**, click *Generate sample config.json file* to download a provisioning payload describing the MQTT broker, hardware modes, and cloud endpoint.

> All data shown in the sandbox is illustrative and generated in the browser. The portal does not currently connect to live sensors or a backend API.
