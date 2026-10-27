---
tags:
  - CI4AI
  - Software
title: "KaiAir: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for KaiAir. KaiAir is predictable per-packet power control and scheduling implemented in the OCUDU 5G stack."
---
# How-To Guides

## Requirements

- OCUDU at the pinned base commit (see `patches/ocudu/BASE`), Linux, gcc 11 or newer,
  UHD 4.x.
- A COTS UE works for the UL direction and for CQI-based DL. The full DL true-SINR loop
  needs the patched OAI nrUE. Those patches target the tag in `patches/oai-nrue/BASE`.
- Multi-cell coordination needs a common 10 MHz and PPS reference for the radios
  (OctoClock or GPSDO) and PTP-synchronized hosts. ONAMA takes its global slot index from
  the host clock. A slot is 500 us, so host synchronization must be well under that. PTP
  with hardware timestamping ensures nanosecond sync.

## Install

Clone this repository and each upstream into one working folder, then run
`scripts/apply_patches.sh`. It checks out the pinned base commit (recorded in
`patches/ocudu/BASE` and `patches/oai-nrue/BASE`) and applies the KaiAir patch series
with `git am`, so git needs a user name and email set beforehand. Build with a job count
that fits your memory rather than your core count, `-j8` under an 8 GB limit. The full
walkthrough, including the host environment, configuration, and multi-cell bring-up, is
in [docs/BUILD_RUN.md](https://github.com/ICICLE-ai/kaiair/blob/main/docs/BUILD_RUN.md).

## Run

The gNB starts through the control agent, and a local web dashboard plots the live
telemetry. The agent HTTP API, the live control-file overlay, the telemetry JSON, and
the dashboard are documented in [docs/AGENT_API.md](https://github.com/ICICLE-ai/kaiair/blob/main/docs/AGENT_API.md).

---

## What is in this release

- UL per-packet power control
- DL per-packet power control
- GRK interference model, exclusion-region, K-adaptation
- Multi-cell measurement plane (neighbor RSRP via RRC, TDD-reciprocity gain map)
- Inter-gNB PktR-Signal exchange over Xn-AP PRIVATE MESSAGE (TS 38.423)
- Conflict graph and ONAMA slot gate with off, observe, and enforce modes
- Live control plane (HTTP agent plus control-file overlay)
- Telemetry (per-link JSON, web dashboard)

## Repository layout

```
patches/ocudu/       KaiAir gNB patch series against the pinned OCUDU base
patches/oai-nrue/    UE patch series against the pinned OAI tag
codesign-api/        per-node control agent (HTTP, stdlib Python) and peer bus
dashboard/           local web dashboard (live SINR, power, and coordination view)
configs/             known-good gNB YAMLs and UE configuration
scripts/             patch apply and build helpers
docs/                architecture, build and run guide, agent API
```

How KaiAir is organized, where every piece lives in the OCUDU tree, and what changed in
the OAI nrUE is covered in [docs/ARCHITECTURE.md](https://github.com/ICICLE-ai/kaiair/blob/main/docs/ARCHITECTURE.md).
