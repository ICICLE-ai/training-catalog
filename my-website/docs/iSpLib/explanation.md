---
tags:
  - CI4AI
  - AI4CI
---

# Explanation

## Convention and Usage

The current iSpLib has both regular and optimized SpMM operation for comparison purpose. The default operation is non-optimized. To use the optimized version, use the following code snippet for running the GNN model:

```
import builtins
builtins.FUSEDMM = True
```

FusedMM method is used as the optimized sparse kernel and it is generated when `./configure` command is run. See details here: [FusedMM Method](https://arxiv.org/abs/2011.06391).

**Note: If you are not using the optimized kernel, you will still have to explicitly mention `builtins.FUSEDMM = False` in the code, otherwise it will raise an error.**

## Performance and Testing

When compared to PyTorch Sparse, a 2-layer GCN implemention with 10 epochs is typically-

- **2.5x** faster on Cora dataset
- **2x** faster on Reddit dataset

[Note: The speed-up varies largly depending on the system condition]

To run the test code, use the command: `make test`. This runs the python script in `tests/GCN.py` and prints out the speed-up along with the accuracy. See `tests/Expected_GCN_output.txt` for reference.

```
