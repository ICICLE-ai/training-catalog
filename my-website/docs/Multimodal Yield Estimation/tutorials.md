---
tags:
  - Foundation-AI
title: "Multimodal Yield Estimation: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for Multimodal Yield Estimation. A transformer-based model that estimates plot-level corn yield (bu/acre) from weekly text captions of field…"
---
# Tutorials

## Overview

| | |
|---|---|
| Task | Plot-level corn yield regression (bu/acre) |
| Text input | One caption per week after planting, embedded with [`Qwen/Qwen3-Embedding-0.6B`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) (1024-d) |
| Image input | UAS RGB plot tiles (`.tif`) with capture dates, embedded with [`facebook/dinov3-vitb16-pretrain-lvd1689m`](https://huggingface.co/facebook/dinov3-vitb16-pretrain-lvd1689m) (768-d) |
| Season length | 22 weeks (150 days) after planting |
| Cutoffs | Trained and evaluated at weeks `4, 8, 12, 16, 20, 22`; any week 1–22 can be estimated |

## Prerequisites

- Python 3.11 or newer
- A GPU is recommended. On CPU, the inference scripts take several minutes because they run Qwen3 and DINOv3.

## Getting Started: your first prediction

1. Clone the repository and install the dependencies:

   ```bash
   git clone https://huggingface.co/ICICLE-AI/multimodal-yield-estimation
   cd multimodal-yield-estimation
   pip install -r requirements.txt
   ```

2. Point the example at your images. `examples/sample_input.json` contains real weekly captions for one plot, but the UAS `.tif` tiles are not included. Each image entry has a placeholder path such as `/path/to/images/northwest_bftb_om_corn_rgb_101_20240530.tif`; replace `/path/to/images/` with the folder holding your tiles (or remove the `images` list to predict from text only).

3. Run single-sample inference at week 12:

   ```bash
   python scripts/inference_single_hf.py \
     --hf_model_dir ICICLE-AI/multimodal-yield-estimation \
     --sample_json examples/sample_input.json \
     --week 12 \
     --output_json prediction.json
   ```

4. Read the result, printed and saved to `prediction.json`:

   ```json
   {
     "sample_id": "northwest_bftb_2024_plot101",
     "week": 12,
     "has_image_by_week": true,
     "image_age_weeks": 0,
     "yield_pred_bu_per_acre": 175.66
   }
   ```
