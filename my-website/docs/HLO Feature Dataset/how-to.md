---
tags:
  - AI4CI
  - Software
  - Visual-Analytics
title: "HLO Feature Dataset for AI Resource Estimation: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for HLO Feature Dataset for AI Resource Estimation. A dataset designed to support AI-driven resource estimation like runtime prediction to…"
---

# How-To Guides

## How to Predict Training Time Using Metadata

- **Problem:** Estimating runtime for deep learning models on HPC resources.
- **Steps:**
  1. Load `dataset-new.csv`.
  2. Select relevant features (`batch`, `epochs`, `gpu_core_count`, etc.).
  3. Train a regression model.
- **Advanced Tips:** Integrate HLO graph features for improved accuracy using GNNs.
- **Troubleshooting:** Ensure consistent preprocessing of categorical fields.
- **Example:** Refer to the [baseline notebook](https://huggingface.co/datasets/ICICLE-AI/ResourceEstimation_HLOGenCNN/blob/main/Baseline_XGBoost_Resource_Estimation.ipynb).