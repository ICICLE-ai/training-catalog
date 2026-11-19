---
tags:
  - Software
  - AI4CI
  - Release 2026-11
---
# HARP UI - HPC Application Runtime Predictor

HARP profiles scientific applications across high-performance computing (HPC) systems, builds regression models from the resulting execution history, and predicts application runtime and resource needs. **HARP UI** is the browser front end for that workflow: one web page, backed by a small FastAPI server, that turns a profiling sweep into many Tapis jobs across several systems, collects their results, trains runtime estimators, and lets you pick the best model, all through your own Tapis account. It runs on your computer, on a shared HTTPS server, or as an ICICLE Tapis Pod designed to be embedded in TapisUI.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/HARP-UI)
[![License: BSD_3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>


> Looking for the earlier notebook (Colab + Tapis container) workflow or installable OSC/Linux module (`module load harp`)? Start with the [legacy execution notebooks](https://github.com/ICICLE-ai/HARP-UI/blob/main/Notebooks) and [legacy HARP overview](https://github.com/ICICLE-ai/HARP-UI/blob/main/DEMO/readMe.md).


## References

- [HARP source repository](https://github.com/ICICLE-ai/HARP-UI)
- [Deployed HARP service](https://harp.pods.icicleai.tapis.io)
- [HARP sweep-server reference](https://github.com/ICICLE-ai/HARP-UI/blob/main/harp_server/README.md) (API, environment variables, internals)
- [Tapis Pods deployment guide](https://github.com/ICICLE-ai/HARP-UI/blob/main/deploy/README.md)
- [Tapis Pods Service API](https://tapis.readthedocs.io/en/latest/technical/pods.html)
- [Offline UI demo](https://github.com/ICICLE-ai/HARP-UI/blob/main/DEMO/ui/README.md)
- [Legacy HARP overview and notebook links](https://github.com/ICICLE-ai/HARP-UI/blob/main/DEMO/readMe.md)
- [Tapis documentation](https://tapis.readthedocs.io/)
- [CODAR Cheetah](https://github.com/CODARcode/cheetah)

## Acknowledgements

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Report defects and feature requests through [GitHub Issues](https://github.com/ICICLE-ai/HARP-UI/issues). Include the HARP version, where the UI runs (laptop, HTTPS server, Tapis Pod / TapisUI), the Tapis tenant, reproduction steps, and relevant logs. Never include access tokens or passwords.

## Start here

Choose the path that matches what you want to do:

| Goal | Recommended path | Tapis or HPC access required? |
|---|---|---|
| Explore the interface without submitting jobs | [Try the offline demo](./tutorials.md#explore-harp-without-tapis) | No |
| Profile an application on an HPC system | [Run your first profiling sweep](./tutorials.md#generate-build-and-estimate-runtime) | Yes |
| Develop or test HARP UI locally | [Run HARP UI on your computer](./tutorials.md#run-harp-ui-on-your-computer) | A token is needed for live Tapis data |
| Make an application available in HARP | [Package an application for sweeps](./how-to.md#package-your-application-for-sweeps) | Yes |
| Deploy or update the hosted service | [Deploy as an ICICLE Tapis Pod](./how-to.md#deploy-as-an-icicle-tapis-pod-tapisui) | Tapis Pods administration |

HARP's browser workflow has three stages:

1. **Generate:** run controlled application configurations through Tapis and collect timing and hardware data.
2. **Build:** train and compare runtime estimators from successful profiling runs.
3. **Estimate:** predict runtime for new parameter and hardware configurations.

HARP does not create cluster accounts, allocations, system credentials, or live scheduler partitions. Those must already be available through the selected Tapis tenant.
