---
tags:
  - Foundation-AI
---

# Explanation

### Overview

- Clean, modular architecture under `src/`
- YAML-first configuration with CLI overrides
- Optional per-epoch validation and next-checkpoint testing
- Organized logging and results export

### Repository structure (what each part means)

```
├── main.py                    # Single entrypoint (parses args, sets up, runs training/eval)
├── configs/
│   └── training/
│       ├── zs.yaml           # Zero-shot (no training)
│       ├── oracle.yaml       # Oracle training on all data
│       └── accumulative.yaml # Accumulative training across checkpoints
├── src/
│   ├── config.py             # ConfigManager: loads YAML, exposes dict
│   ├── data/
│   │   └── dataset.py        # Minimal dataset/dataloader utilities used by training
│   ├── models/
│   │   └── factory.py        # create_model(config): BioCLIP/placeholder, etc.
│   ├── modules/
│   │   ├── ood.py            # OOD detection (pluggable, not required by default flow)
│   │   ├── active_learning.py# Active Learning strategies (pluggable)
│   │   ├── continual_learning.py # Continual Learning strategies (pluggable)
│   │   └── calibration.py    # Inference-time calibration (optional)
│   ├── training/
│   │   ├── common.py         # Shared loops (evaluate_epoch, dataloaders, helpers)
│   │   ├── oracle.py         # Oracle training loop + per-ckp evaluation
│   │   └── accumulative.py   # Accumulative training loop (rounds across ckp_N)
│   └── utils/
│       ├── logging.py        # Human-friendly logging helpers
│       ├── metrics.py        # MetricsCalculator (balanced accuracy, etc.)
│       ├── results.py        # Save/export results and summaries
│       ├── paths.py, gpu.py, seed.py, config.py  # Assorted helpers
└── logs/                     # Run logs and results
```

Notes
- The training flows primarily use `src/training/*` and `src/models/factory.py`.
- `src/modules/*` are optional/pluggable components for advanced workflows.

### Data expectation

Given `--camera <PROJECT_CAMERA>` (e.g., `ENO_C05`), data is read from:
- `data/<PROJECT>/<PROJECT_CAMERA>/30/train.json`
- `data/<PROJECT>/<PROJECT_CAMERA>/30/test.json`