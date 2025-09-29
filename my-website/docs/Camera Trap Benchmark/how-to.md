---
tags:
  - Foundation-AI
---

# How-To Guides

### How to run (with validation and test per-epoch)

Use `--train_val --train_test` to enable per-epoch validation and per-epoch test.

Zero-shot (ZS)
```bash
python main.py --camera ENO_C05 \
	--config configs/training/zs.yaml \
	--train_val --train_test
```

Oracle training
```bash
python main.py --camera ENO_C05 \
	--config configs/training/oracle.yaml \
	--train_val --train_test
```

Accumulative training
```bash
python main.py --camera ENO_C05 \
	--config configs/training/accumulative.yaml \
	--train_val --train_test
```

Common CLI flags
- `--device cuda|cpu` (default: cuda)
- `--seed 42`
- `--timestamps` to include timestamps in console logs
- `--gpu_cleanup` to force periodic VRAM cleanup

### Current training settings (defaults from configs)

Shared defaults (oracle/accumulative)
- epochs: 30
- train_batch_size: 32
- eval_batch_size: 512
- optimizer: AdamW(lr=2.5e-5, weight_decay=1e-4)
- scheduler: CosineAnnealingLR(T_max=30, eta_min=2.5e-6)
- device: cuda (if available)
- seed: 42

Zero-shot (zs)
- epochs: 0 (no training; inference-only)

### Early stopping behavior

- Oracle mode (`src/training/oracle.py`)
	- Enabled only when `--train_val` is set and a validation loader exists.
	- Warm-up = first 10 epochs; Monitor window = next 5 epochs (epochs 11–15).
	- Decision point after epoch 15 (0-based index 14):
		- If monitor best > warm-up best → continue training up to max 30 epochs (or configured `epochs`).
		- Else → stop at 15 and pick the best epoch within the first 15.

- Accumulative mode (`src/training/accumulative.py`)
	- Enabled only when `--train_val` is set and a validation loader exists.
	- Runs 10 epochs initially. Decision at epoch 10:
		- If epoch 10 is best so far → continue up to 20 epochs max (or configured `epochs`, whichever is lower).
		- Else → stop at 10 and pick the best epoch found within the first 10.
	- Training restarts fresh for each round (`ckp_k` → validate on `ckp_k`, test on `ckp_{k+1}`).

Per-epoch testing
- If `--train_test` is provided:
	- Oracle: tests per-epoch over all test checkpoints (averaged report per epoch).
	- Accumulative: tests per-epoch on the next checkpoint of the current round.

### Outputs

- Logs and summaries are written under `logs/` (organized by camera and timestamp).
- Model checkpoints for best epochs per round (accumulative) or overall (oracle) are saved in the run output directory.

### Notes

- BioCLIP v2 weights are auto-discovered if present under `pretrained_weight/` or `ICICLE-Benchmark/pretrained_weight/`.
- If not found, a placeholder model is used with the correct number of classes (still useful for wiring tests).
