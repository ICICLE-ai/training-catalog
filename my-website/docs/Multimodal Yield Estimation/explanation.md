---
tags:
  - Foundation-AI
title: "Multimodal Yield Estimation: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for Multimodal Yield Estimation. A transformer-based model that estimates plot-level corn yield (bu/acre) from weekly text captions of field…"
---
# Explanation

## Problem Description

Given what is known about a corn plot up to a certain week of the season, estimate its final yield.

What is known each week is described in two ways:

- **Text**: a caption summarizing that week's weather and the plot's static soil, topography and treatment information.
- **Image**: UAS RGB images of the plot, taken on flight dates that do not line up with weeks (every 1–2 weeks during the season).

The model gives one yield estimate per plot for the requested cutoff week.

## Placing Images on the Weekly Grid

The inference scripts do this automatically:

- Image week = `(date − planting_date).days // 7`. Images before planting or after week 21 are ignored.
- Each week uses the latest image taken at or before that week (forward-fill). If two images fall in the same week, the later one is used.
- Weeks before the first image have no image (`has_image = 0`).
- The scripts also compute the image age: the number of weeks since the image in use was taken (0 = new image that week).

Example (flights in weeks 2, 3, 4, 6, 7, 9, 11, 14 and 15):

```text
week:       0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
has_image:  0 0 1 1 1 1 1 1 1 1  1  1  1  1  1  1  1  1  1  1  1  1
image_age:  0 0 0 0 0 1 0 0 1 0  1  0  1  2  0  0  1  2  3  4  5  6
```

## Multi-Temporal Yield Estimation

- Each week after planting is represented by a Qwen3 embedding of that week's caption and a DINOv3 embedding of the most recent UAS image, concatenated with a has-image flag and the image age.
- The model reads tokens for weeks `0 … cutoff−1`. A projection layer maps each token to 64 dimensions, then a week signal, a learned position embedding and a cutoff (horizon) embedding are added.
- A 2-layer causal transformer encoder (4 heads) processes the sequence. The causal mask and forward-fill mean that no week sees later captions or images.
- The last token, together with the horizon embedding, goes to a small regression head.
- During training, the loss is averaged over all cutoffs (4, 8, 12, 16, 20, 22) for each batch, so one checkpoint serves every cutoff.

## Features

- Text and image embeddings are concatenated per week.
- Inference starts from raw captions and UAS images: the scripts run Qwen3 and DINOv3, so no precomputed embeddings are needed.
- Missing weeks are handled with image forward-fill, a has-image flag and image age.
- One checkpoint predicts at any cutoff week from 1 to 22.
- The model is a standard Hugging Face `PreTrainedModel` and loads with `AutoModel.from_pretrained(..., trust_remote_code=True)`.
- Single-sample and batch inference scripts write JSON (and optionally CSV) outputs.

## Repository Structure

```text
config.json                        model config, including normalization statistics
model.safetensors                  trained weights
configuration_multimodal.py        HF config class (loaded by trust_remote_code)
modeling_multimodal.py             HF model class (loaded by trust_remote_code)
multimodal_concat_tf.py            temporal transformer module (loaded by trust_remote_code)
train_args.json                    arguments used to train the released checkpoint
hf/                                same model code, imported by the local scripts
data/embeddings.py                 Qwen3 / DINOv3 embedding and input building
data/multimodal_dataset.py         weekly image placement, dataset, split, normalization
scripts/inference_single_hf.py     single-sample inference
scripts/inference_batch_hf.py      batch inference (JSONL)
scripts/train_multimodal_hf.py     training
examples/                          sample_input.json, sample_batch.jsonl
multimodal_yield_estimation.slurm  SLURM example
component-info.yaml                ICICLE component catalog metadata
requirements.txt
LICENSE
```

## Training Details

- **Split**: by field. One `farm_field` is held out (`--test_field`, default: the last field in alphabetical order) and its plots are split 50/50 into validation and test; all other fields are used for training.
- **Loss**: MSE on standardized yield, averaged over all training cutoffs for each batch.
- **Defaults**: AdamW, lr 3e-4, weight decay 1e-2, batch size 16, up to 300 epochs, early stopping on mean validation RMSE with patience 30.
- **Checkpoint**: the epoch with the best validation RMSE is saved in Hugging Face format to `--out_dir`.

## Evaluation

The training script evaluates the best checkpoint on the validation and test plots at every cutoff, and writes:

- `metrics.json`: validation metrics at the best epoch
- `test_metrics.json`: validation and test RMSE, MAE, bias and R² per cutoff
- `test_predictions.csv`: per-plot predictions for the test plots
