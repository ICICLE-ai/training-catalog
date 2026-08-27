---
tags:
  - Digital-Agriculture
  - Foundation-AI
---
# How-To Guides

### Problem Description

The model estimates county-level corn yield from weather and soil information.

The pretrained architecture expects structured numerical inputs rather than natural-language text. To make the model deployable through FlexServ's supported pipeline tasks, the model is exposed through the Hugging Face `text-classification` interface.

The structured yield input is serialized as a JSON string. The custom tokenizer parses this string and converts the weather, soil, crop, and cutoff information into the tensors expected by the pretrained model.

The resulting inference path is:

```text
JSON-formatted input string
        ↓
YieldTokenizer
        ↓
weather + soil + crop + cutoff tensors
        ↓
Yield Estimation Transformer
        ↓
scalar yield prediction
        ↓
YIELD_BU_ACRE score
```

The `score` returned by the pipeline is therefore a yield estimate in `bu/acre`, not a classification probability.

### Getting Started

The repository contains the files required for standalone Hugging Face and FlexServ inference:

```text
.
├── README.md
├── LICENSE
├── component-info.yaml
├── training_code/
├── config.json
├── configuration_yield.py
├── model.safetensors
├── modeling_yield.py
├── requirements.txt
├── sample_input_weekly.json
├── tokenization_yield.py
├── tokenizer_config.json
└── yield_transformer.py
```

A complete inference example is provided in:

```text
sample_input_weekly.json
```

Because the repository provides custom model configuration, tokenizer, and architecture code, Hugging Face loading requires:

```python
trust_remote_code=True
```

### Usage

#### Local Hugging Face Inference

Load the model through the Hugging Face `text-classification` pipeline:

```python
import json
from transformers import pipeline

pipe = pipeline(
    "text-classification",
    model="ICICLE-AI/yield-estimation",
    tokenizer="ICICLE-AI/yield-estimation",
    trust_remote_code=True,
)

with open("sample_input_weekly.json") as f:
    sample = json.load(f)

prediction = pipe(json.dumps(sample))

print(prediction)
```

Example output:

```python
[
    {
        "label": "YIELD_BU_ACRE",
        "score": 165.1769561767578
    }
]
```

The `score` is the predicted corn yield in bushels per acre.

#### Input Format

The structured input contains:

```json
{
  "crop": "corn",
  "weather_format": "weekly",
  "cutoff": 52,
  "weather": {
    "prcp": ["52 weekly values"],
    "srad": ["52 weekly values"],
    "swe": ["52 weekly values"],
    "tmax": ["52 weekly values"],
    "tmin": ["52 weekly values"],
    "vp": ["52 weekly values"]
  },
  "soil": {
    "bdod_mean_0-5cm": 0.0,
    "...": "remaining soil features"
  }
}
```

The complete set of 66 soil variables and their expected ordering are stored in `config.json`.

The tokenizer:

1. parses the JSON-formatted string,
2. validates the expected input fields,
3. constructs the weather, soil, crop, and cutoff tensors.

The Hugging Face pipeline then passes these tensors to the pretrained model for inference.

#### FlexServ Inference

The model has been tested for inference through FlexServ using:

```text
Task: text-classification
Model: ICICLE-AI/yield-estimation
```

FlexServ's `inputs` field expects a string. Therefore, the structured yield input must be supplied as a **JSON-formatted string**, rather than directly as a nested JSON object.

Conceptually, a FlexServ request has the following form:

```json
{
  "task": "text-classification",
  "inputs": "{\"crop\":\"corn\",\"weather_format\":\"weekly\",\"cutoff\":52,\"weather\":{...},\"soil\":{...}}",
  "parameters": {},
  "model": "ICICLE-AI/yield-estimation"
}
```

A successful response has the form:

```json
[
  {
    "label": "YIELD_BU_ACRE",
    "score": 165.1769561767578
  }
]
```

The returned `score` is the estimated yield in `bu/acre`.

#### Validation

The packaged model can be validated locally against the included sample:

```bash
python - <<'PY'
import json
from transformers import pipeline

with open("sample_input_weekly.json") as f:
    sample = json.load(f)

pipe = pipeline(
    "text-classification",
    model=".",
    tokenizer=".",
    trust_remote_code=True,
)

print(pipe(json.dumps(sample)))
PY
```

Expected output for the included sample is approximately:

```text
[{'label': 'YIELD_BU_ACRE', 'score': 165.1769561767578}]
```

### Training own model

#### Installation

Clone the model repository:

```bash
git clone https://huggingface.co/ICICLE-AI/yield-estimation
cd yield-estimation/training_code
```

Create and activate a Python environment:

```bash
conda create -n yield_hf python=3.10
conda activate yield_hf
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

#### Prerequisites

- Python 3.10+
- PyTorch
- Hugging Face Transformers
- Dependencies listed in `requirements.txt`

For GPU training, a CUDA-compatible PyTorch environment is recommended.

The included SLURM script can be used on a compatible HPC system.

#### Problem Description

The objective is to estimate county-level corn yield from weather and soil information.

Each sample contains two primary sources of information:

1. multi-temporal weather observations;
2. static soil properties.

The weather input is represented as:

```text
[K, W]
```

where:

- `K` is the number of temporal observations;
- `W = 6` is the number of weather variables.

The static soil input is represented as:

```text
[S]
```

where:

```text
S = 66
```

The model learns a regression function of the form:

```text
weather + soil + crop information
                ↓
        transformer model
                ↓
       predicted corn yield
```

The predicted value is expressed in bushels per acre (`bu/acre`).

The model supports multi-temporal estimation by evaluating the weather sequence at different seasonal cutoffs.

#### Repository Structure

The final repository is organized as follows:

```text
.
├── README.md
├── requirements.txt
├── training.slurm
│
├── checkpoints/
│   ├── config.json
│   ├── metrics.json
│   └── model.safetensors
│
├── config/
│   ├── __init__.py
│   └── config.py
│
├── data/
│   ├── __init__.py
│   ├── dataset.py
│   └── preprocessing.py
│
├── examples/
│   └── sample_input_weekly.json
│
├── hf/
│   ├── __init__.py
│   ├── auto.py
│   ├── configuration_yield.py
│   └── modeling_yield.py
│
├── models/
│   ├── __init__.py
│   └── unimodal_ws_crossattn.py
│
├── scripts/
│   ├── __init__.py
│   ├── prepare_cornbelt.py
│   ├── train_hf.py
│   ├── evaluate_hf.py
│   └── inference_hf.py
│
└── training/
    ├── __init__.py
    └── engine.py
```

The major components are:

- `data/` — dataset loading and preprocessing
- `models/` — core neural network architecture
- `training/` — training and evaluation utilities
- `hf/` — Hugging Face AutoClass-compatible regression wrapper used by the training repository
- `scripts/` — data preparation, training, evaluation, and inference entry points
- `checkpoints/` — final trained checkpoint and configuration
- `examples/` — example structured model input
- `training.slurm` — example HPC training job

#### Data Preparation

The USA County Level Crop Yield public dataset is used for training, validation and testing. The data preparation workflow is implemented in:

```text
scripts/prepare_cornbelt.py
```

After preparation, the expected dataset structure is:

```text
data/
└── cornbelt/
    ├── train.h5
    ├── val.h5
    └── test.h5
```

The model uses the following six weather variables:

```text
prcp
srad
swe
tmax
tmin
vp
```

The 66 soil variables used by the final checkpoint are recorded in the model configuration.

#### Training

The primary training entry point is:

```text
scripts/train_hf.py
```

The final model uses multi-cutoff training with:

```text
20,24,28,32,36,40,44,48,52
```

An example training command is:

```bash
python scripts/train_hf.py \
  --train_file data/cornbelt/train.h5 \
  --val_file data/cornbelt/val.h5 \
  --test_file data/cornbelt/test.h5 \
  --weather_vars prcp,srad,swe,tmax,tmin,vp \
  --soil_vars bdod_mean_0-5cm,bdod_mean_5-15cm,bdod_mean_15-30cm,bdod_mean_30-60cm,bdod_mean_60-100cm,bdod_mean_100-200cm,cec_mean_0-5cm,cec_mean_5-15cm,cec_mean_15-30cm,cec_mean_30-60cm,cec_mean_60-100cm,cec_mean_100-200cm,cfvo_mean_0-5cm,cfvo_mean_5-15cm,cfvo_mean_15-30cm,cfvo_mean_30-60cm,cfvo_mean_60-100cm,cfvo_mean_100-200cm,clay_mean_0-5cm,clay_mean_5-15cm,clay_mean_15-30cm,clay_mean_30-60cm,clay_mean_60-100cm,clay_mean_100-200cm,nitrogen_mean_0-5cm,nitrogen_mean_5-15cm,nitrogen_mean_15-30cm,nitrogen_mean_30-60cm,nitrogen_mean_60-100cm,nitrogen_mean_100-200cm,ocd_mean_0-5cm,ocd_mean_5-15cm,ocd_mean_15-30cm,ocd_mean_30-60cm,ocd_mean_60-100cm,ocd_mean_100-200cm,ocs_mean_0-5cm,ocs_mean_5-15cm,ocs_mean_15-30cm,ocs_mean_30-60cm,ocs_mean_60-100cm,ocs_mean_100-200cm,phh2o_mean_0-5cm,phh2o_mean_5-15cm,phh2o_mean_15-30cm,phh2o_mean_30-60cm,phh2o_mean_60-100cm,phh2o_mean_100-200cm,sand_mean_0-5cm,sand_mean_5-15cm,sand_mean_15-30cm,sand_mean_30-60cm,sand_mean_60-100cm,sand_mean_100-200cm,silt_mean_0-5cm,silt_mean_5-15cm,silt_mean_15-30cm,silt_mean_30-60cm,silt_mean_60-100cm,silt_mean_100-200cm,soc_mean_0-5cm,soc_mean_5-15cm,soc_mean_15-30cm,soc_mean_30-60cm,soc_mean_60-100cm,soc_mean_100-200cm \
  --crop corn \
  --time_agg weekly \
  --train_cutoffs 20,24,28,32,36,40,44,48,52 \
  --eval_cutoffs 20,24,28,32,36,40,44,48,52 \
  --epochs 30 \
  --lr 3e-5 \
  --batch_size 32 \
  --out_dir checkpoints
```

The final checkpoint is stored in:

```text
checkpoints/
```

The checkpoint includes:

```text
config.json
model.safetensors
metrics.json
```
#### Training on Your Own Data

The training pipeline can also be used to train a new yield estimation model on a compatible dataset.

Prepare the dataset in the HDF5 format expected by `YieldDataset` and provide separate training, validation, and test files.

The weather and soil variables supplied to the training command must correspond to the variables available in the prepared dataset.

A general training command is:

```bash
python scripts/train_hf.py \
  --train_file <path/to/train.h5> \
  --val_file <path/to/val.h5> \
  --test_file <path/to/test.h5> \
  --weather_vars <comma-separated-weather-variables> \
  --soil_vars <comma-separated-soil-variables> \
  --crop <crop-name> \
  --time_agg weekly \
  --train_cutoffs <comma-separated-training-cutoffs> \
  --eval_cutoffs <comma-separated-evaluation-cutoffs> \
  --epochs <number-of-epochs> \
  --lr <learning-rate> \
  --batch_size <batch-size> \
  --out_dir <output-directory>
```

#### SLURM Training

An example SLURM job is provided in:

```text
training.slurm
```

Submit it using:

```bash
sbatch training.slurm
```

#### Evaluation

The trained checkpoint can be evaluated using:

```text
scripts/evaluate_hf.py
```

For the final multi-cutoff model:

```bash
python scripts/evaluate_hf.py \
  --hf_model_dir checkpoints \
  --test_file data/cornbelt/test.h5 \
  --cutoffs 20,24,28,32,36,40,44,48,52 \
  --batch_size 64 \
  --output_csv checkpoints/test_predictions.csv \
  --metrics_json checkpoints/test_metrics.json
```

Evaluation is performed independently at the configured seasonal cutoffs.

The evaluation process:

1. loads the final trained checkpoint;
2. loads the test dataset;
3. applies the normalization statistics stored in the checkpoint configuration;
4. performs inference at the requested cutoffs;
5. computes evaluation metrics;
6. save predictions and metrics to disk.

#### Inference

Inference using the trained checkpoint is implemented in:

```text
scripts/inference_hf.py
```

An example structured input is provided in:

```text
examples/sample_input_weekly.json
```

The sample follows the general structure:

```json
{
  "crop": "corn",
  "weather_format": "weekly",
  "cutoff": 52,
  "weather": {
    "prcp": [],
    "srad": [],
    "swe": [],
    "tmax": [],
    "tmin": [],
    "vp": []
  },
  "soil": {
    "bdod_mean_0-5cm": 0.0
  }
}
```

The complete sample file contains the required weather sequence and soil variables.

Run single-sample inference with:

```bash
python scripts/inference_hf.py \
  --hf_model_dir checkpoints \
  --single_sample_json examples/sample_input_weekly.json \
  --cutoff 52 \
  --output_csv inference_prediction.csv
```

The output contains the predicted yield for the requested cutoff.

For example:

```text
sample_idx,cutoff,y_pred
0,52,<predicted_yield>
```