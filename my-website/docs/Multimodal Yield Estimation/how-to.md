---
tags:
  - Foundation-AI
title: "Multimodal Yield Estimation: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for Multimodal Yield Estimation. A transformer-based model that estimates plot-level corn yield (bu/acre) from weekly text captions of field…"
---
# How-To Guides

## Installation

```bash
pip install -r requirements.txt
```

Tested versions:

```text
torch==2.12.1
torchvision==0.27.1
transformers==5.13.0
sentence-transformers==5.7.0
safetensors==0.8.0
numpy==2.4.4
pandas==3.0.3
scikit-learn==1.9.0
pillow==12.2.0
```

## Prepare Input Data

### Input format

Both inference scripts use the same per-plot sample format:

```json
{
  "sample_id": "plot_001",
  "planting_date": "2024-05-16",
  "week": 12,
  "texts": [
    "<caption for week 0>",
    "<caption for week 1>",
    "..."
  ],
  "images": [
    {"path": "/path/to/images/plot_001_20240530.tif", "date": "2024-05-30"},
    {"path": "/path/to/images/plot_001_20240606.tif", "date": "2024-06-06"}
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `planting_date` | yes | `YYYY-MM-DD`. Weeks are counted from this date. |
| `week` | yes, unless `--week` is passed | Cutoff week, 1–22. |
| `texts` | yes | Weekly captions starting at week 0 (planting week). At least `week` captions are needed; at most 22 are used. |
| `images` | no | List of `{path, date}`. Order does not matter. An empty or missing list means no images. |
| `sample_id` | no | Copied to the output. |

- **Single inference**: one JSON object (see `examples/sample_input.json`).
- **Batch inference**: a JSONL file with one object per line (see `examples/sample_batch.jsonl`).

### Write the weekly captions

Week `w` covers days `7w` to `7w+6` after planting; the last week (week 21) covers days 147–149. Each caption describes:

- **11 weekly weather variables** (Daymet): day length, precipitation total, solar radiation, maximum, minimum and mean temperature, vapor pressure, GDD accumulation, and 3-, 7- and 14-day precipitation averages. Values are weekly means, except precipitation and GDD, which are weekly sums.
- **23 soil variables**: pH, buffer pH, organic matter, CEC, P, K, Mg, Ca, K/Ca/Mg TE, S, Zn, Fe, Mn, Cu, B, Na, clay, sand, silt, bulk density and available water capacity.
- **Topography**: elevation and slope.
- **Pre-plant soil moisture proxy**: mean precipitation over the 14 days before planting.
- **Hybrid/treatment** identifier.

Each numeric value is converted to `low`, `medium` or `high` using tertile thresholds computed on the full corn caption dataset (`not available` when missing). The hybrid/treatment value is written as is.

Example caption (one week of one plot):

```text
Weekly mean day length: medium. Weekly precipitation total: low. Weekly mean solar radiation: high. Weekly mean maximum temperature: high. Weekly mean minimum temperature: medium. Weekly mean vapor pressure: medium. Weekly mean temperature: high. Weekly GDD accumulation: high. Weekly mean 3-day precipitation average: medium. Weekly mean 7-day precipitation average: medium. Weekly mean 14-day precipitation average: high. Soil pH: low. Buffer pH: not available. Soil organic matter: low. Soil cation exchange capacity: high. Soil phosphorus: medium. Soil potassium: high. Soil magnesium: high. Soil calcium: high. Soil potassium TE: low. Soil calcium TE: high. Soil magnesium TE: low. Soil sulfur: high. Soil zinc: medium. Soil iron: high. Soil manganese: low. Soil copper: high. Soil boron: medium. Soil sodium: medium. Soil clay: high. Soil sand: medium. Soil silt: low. Soil bulk density: medium. Soil available water capacity: low. Elevation: low. Slope: low. Pre-plant soil moisture proxy: high. Hybrid/treatment: 100.0.
```

The model only learned this template. Captions should use the same wording, order and categories; free-form text produces embeddings the model has not seen. The caption generator and the tertile thresholds are not included in this repository.

### Prepare the UAS plot tiles

- RGB plot tiles (`.tif`) cropped from UAS orthomosaics, one tile per plot per flight date.
- Any size works: the DINOv3 image processor resizes and normalizes each image.
- Each image needs its capture `date`.

## Run Inference

Both scripts take raw captions and image files, compute the Qwen3 and DINOv3 embeddings, place the images on the weekly grid and predict yield. `--hf_model_dir` accepts a local checkpoint folder (use `.` from the repository root) or a Hub repo ID. The model is trained on weather/soil text caption and UAS plot images with 29.8 bu/acre RMSE yield error at evaluation.

### Single sample

```bash
python scripts/inference_single_hf.py \
  --hf_model_dir ICICLE-AI/multimodal-yield-estimation \
  --sample_json examples/sample_input.json \
  --week 12 \
  --output_json prediction.json
```

### Batch

```bash
python scripts/inference_batch_hf.py \
  --hf_model_dir ICICLE-AI/multimodal-yield-estimation \
  --input_jsonl examples/sample_batch.jsonl \
  --output_json predictions.json \
  --output_csv predictions.csv
```

- The JSON output is a list with one object per sample, using the same fields as the single-sample output. `--output_csv` is optional.
- Each sample uses its own `week`; pass `--week` to use the same week for all samples.

| Option | Description |
|---|---|
| `--hf_model_dir` | Local checkpoint folder or Hub repo ID |
| `--sample_json` / `--input_jsonl` | Input file |
| `--week` | Cutoff week (1–22); overrides the sample's `week` |
| `--output_json` | Output JSON path (output folder must exist) |
| `--output_csv` | Batch only: optional CSV output |
| `--batch_size` | Batch only: model batch size (default 64) |

### On a SLURM cluster

`multimodal_yield_estimation.slurm` runs both inference scripts on one GPU. Fill in `--account`, the conda paths and the repository path before submitting:

```bash
sbatch multimodal_yield_estimation.slurm
```

## Load the Model from Python

The model uses custom code, so load it with `trust_remote_code=True`. The model takes embeddings, not raw text or images; use `data/embeddings.py` (as the inference scripts do) to build them. Run this from the repository root so `data/` can be imported.

```python
import torch
from transformers import AutoModel

from data.embeddings import ImageEmbedder, TextEmbedder, embed_samples

model = AutoModel.from_pretrained(
    "ICICLE-AI/multimodal-yield-estimation", trust_remote_code=True
).eval()

x = embed_samples(
    [sample],  # dict in the input format above
    TextEmbedder(model.config.text_model),
    ImageEmbedder(model.config.image_model),
)

with torch.no_grad():
    out = model(
        text=torch.from_numpy(x["text"]),
        image=torch.from_numpy(x["image"]),
        img_mask=torch.from_numpy(x["img_mask"]),
        img_age=torch.from_numpy(x["img_age"]),
        cutoff=int(x["week"][0]),
    )

print(out.predictions)  # bu/acre
```

Model inputs:

| Input | Shape | Description |
|---|---|---|
| `text` | `[B, T, 1024]` | Raw Qwen3 caption embeddings |
| `image` | `[B, T, 768]` | Raw DINOv3 features (any value where `img_mask` is 0) |
| `img_mask` | `[B, T]` | 1 if an image is available at or before that week |
| `img_age` | `[B, T]` | Weeks since that image was taken |
| `cutoff` | int | Number of weeks to use (defaults to `T`) |

Normalization statistics are stored in `config.json`, so inputs are passed un-normalized. The output has `predictions` (bu/acre) and `logits` (standardized yield).

## Train on Your Own Data

1. Build an `.npz` file of embeddings with these arrays:

   | Array | Shape | Description |
   |---|---|---|
   | `text` | `[N, 22, 1024]` float32 | Weekly Qwen3 caption embeddings |
   | `image` | `[N, 22, 768]` float32 | DINOv3 feature of the latest image at or before each week (zeros where none) |
   | `img_mask` | `[N, 22]` float32 | 1 if an image is available at or before that week |
   | `img_age` | `[N, 22]` float32 | Weeks since that image was taken |
   | `yield_` | `[N]` float32 | Yield (bu/acre) |
   | `farm_field`, `plot`, `planting_date`, `row_key` | `[N]` | Plot metadata |

   The image arrays can be built with `images_to_weeks()` in `data/multimodal_dataset.py`, which is the same function the inference scripts use.

2. Train. Your data needs at least two `farm_field` values; pass `--test_field <name>` to choose which one is held out.

   ```bash
   python scripts/train_multimodal_hf.py \
     --data /path/to/embeddings.npz \
     --out_dir checkpoints
   ```

   Other options: `--cutoffs`, `--epochs`, `--patience`, `--lr`, `--batch_size`, `--d_model`, `--num_layers`, `--dropout`, `--input_dropout`, `--seed`.

3. To train on SLURM, replace the inference commands in `multimodal_yield_estimation.slurm` with:

   ```bash
   python scripts/train_multimodal_hf.py --data /path/to/your.npz --out_dir checkpoints
   ```

4. Use the new checkpoint by passing `--hf_model_dir checkpoints` to the inference scripts.
