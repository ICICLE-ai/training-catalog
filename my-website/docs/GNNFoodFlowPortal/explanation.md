---
tags:
  - Smart-Foodsheds
  - AI4CI
---
# Explanation

## What Version 1.2.0 Adds

Version 1.2.0 incorporates a new FoodFlow portal workflow alongside the existing static parallel-model map and download tools.

- **Parallel Model Map:** explores precomputed SCTG-specific county-to-county food-flow predictions.
- **Parallel Model Guide:** explains how to use the static model filters, map, hover details, and export workflow.
- **Parallel Model Download:** exports filtered model rows and origin-destination summary statistics.
- **Multi-task One-to-One:** runs a scenario for a selected origin-destination county pair and compares baseline and modified flows.
- **Multi-task One-to-Many:** runs a scenario for one focus county against many partner counties and summarizes partner-level changes.
- **Vendored what-if assets:** includes multi-task model artifacts, feature metadata, county mappings, predictions, a model checkpoint, and inference code under `portal/whatif_demo`.

## Deployment Notes

The May 2026 Tapis deployment was rebuilt to include the new multi-task what-if workflows. Deployment updates include:

- The what-if workflow adds `torch`, `torch-geometric`, and `scikit-learn` to the portal dependency set.
- The container uses CPU-only PyTorch packages for the current non-GPU pod environment.
- The Docker build uses `python:3.11-slim-bookworm`, build-context exclusions, and cleanup steps to reduce image size.
- Security-related packages were updated, including GitPython, urllib3, pillow, tornado, and Streamlit.
- Container runtime fixes resolved path handling issues in `app.py` and `whatif_tabs.py`.
- The older parallel map workflow may load more slowly than the new scenario tabs in some environments, but it remains functional.

## Data and Artifacts

The repository includes the data and artifacts needed by the portal.

- `portal/cleaned_data`: precomputed parallel SCTG-specific model outputs.
- `portal/whatif_demo`: multi-task what-if artifacts, model checkpoint, metadata, and inference code.
- `portal/data`: county metadata and shapefile resources.
- `portal/files`: supporting files, including the project PDF and FAF metadata.
- `portal/image`: portal images and branding assets.

## Data Fields

The parallel model workflow uses county-level origin-destination rows with fields such as:

- `origin` and `dest`: county FIPS codes.
- `origin_x`, `origin_y`, `dest_x`, and `dest_y`: county coordinates.
- `predicted_value_original`: estimated kilotons of food shipped.
- `exist_prob`: probability that the predicted flow exists.
- `sctg`: food category code.

## Downstream Use

- Spatial forecasting of trade changes under policy shifts.
- Identifying critical counties for supply-chain resilience.
- Exploring food-flow sensitivity under county-level feature changes.
- Generating scenario comparison tables for research and planning.

## Out-of-Scope Use

- Real-time food trade forecasting.
- Non-U.S. geographic settings without retraining.
- Operational routing, procurement, or emergency decisions without external validation.

## Bias, Risks, and Limitations

- **Bias:** Model predictions depend on historical FAF data and may not reflect unexpected future disruptions, such as disasters, pandemics, or sudden policy changes.
- **Limitations:** Static parallel-model prediction is limited to predefined food SCTG categories 1-7.
- **Scenario uncertainty:** What-if outputs are model-based estimates and should be interpreted as exploratory analysis, not guaranteed causal effects.
- **Data quality:** Results assume the accuracy and coverage of FAF flow data, county metadata, economic indicators, and model artifacts.
