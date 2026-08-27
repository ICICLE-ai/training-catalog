---
tags:
  - CI4AI
  - Digital-Agriculture
  - Software
  - Release 2026-08
---
# No-Code Workflow Studio

A browser-based workflow builder for the full ML lifecycle: wire up a pipeline in
a drag-and-drop canvas — data sources, pre-processing, annotation, training,
inference, visualization, sinks — then execute it as a graph of real Tapis jobs
on HPC, and watch every step's status, config and logs live on the same canvas.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/workflow-orchestrator)
[![License: BSD_3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>



## References

- [Tapis Jobs API](https://tapis-project.github.io/live-docs/?service=Jobs) — the HPC job submission service each step is submitted to.
- [README.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/README.md) — install and run the frontend + backend locally.
- [backend/INTEGRATION.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/backend/INTEGRATION.md) — Tapis credentials, app/system provisioning, and what the engine needs before a job can run.
- [docs/adding-a-step-form.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/docs/adding-a-step-form.md) — add a new step whose settings UI is auto-generated from its schema.
- [docs/adding-a-step-custom-ui.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/docs/adding-a-step-custom-ui.md) — add a step with a custom interactive panel (map, labeler, live preview).
- [frontend/app/pages/README.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/frontend/app/pages/README.md) — the step settings page contract (`StepPanelProps`).

## Acknowledgements

<!-- Please include other funding sources above this line. -->

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Please report issues via [GitHub Issues](https://github.com/ICICLE-ai/workflow-orchestrator/issues).
