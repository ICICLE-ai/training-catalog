---
tags:
  - AI4CI
  - Software
---
# Explanation

## Architecture

The system has two layers:

1. **High-level API** (`z3adapter.reasoning`) - Simple Python interface for reasoning tasks
2. **Low-level execution** (`z3adapter.backends`) - JSON DSL or SMT2 backend for Z3

Most users should use the high-level API.

For full documentation, visit the [ProofOfThought Documentation Site](https://debarghag.github.io/proofofthought/).
