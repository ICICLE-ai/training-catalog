---
tags:
  - AI4CI
  - Software
---
# How-To Guides

## Backend Selection

ProofOfThought supports two execution backends:

```python
# SMT2 backend (default) - Standard SMT-LIB 2.0 via Z3 CLI
pot = ProofOfThought(llm_client=client, backend="smt2")

# JSON backend - Custom DSL via Python Z3 API
pot = ProofOfThought(llm_client=client, backend="json")
```

See [BACKENDS.md](https://github.com/ICICLE-ai/proofofthought/blob/main/BACKENDS.md) for details on choosing a backend.

## Postprocessing Techniques

Enhance reasoning quality with advanced postprocessing techniques:

```python
# Enable Self-Refine for iterative refinement
pot = ProofOfThought(
    llm_client=client,
    postprocessors=["self_refine"],
    postprocessor_configs={"self_refine": {"num_iterations": 2}}
)

# Use Self-Consistency for improved reliability via majority voting
pot = ProofOfThought(
    llm_client=client,
    postprocessors=["self_consistency"],
    postprocessor_configs={"self_consistency": {"num_samples": 5}}
)

# Chain multiple postprocessors
pot = ProofOfThought(
    llm_client=client,
    postprocessors=["self_refine", "self_consistency"]
)
```

Available techniques:
- **Self-Refine**: Iterative refinement through self-critique
- **Self-Consistency**: Majority voting across multiple reasoning paths
- **Decomposed Prompting**: Breaking complex questions into sub-questions
- **Least-to-Most Prompting**: Progressive problem solving from simple to complex

See [POSTPROCESSORS.md](https://github.com/ICICLE-ai/proofofthought/blob/main/POSTPROCESSORS.md) for complete documentation and usage examples.

## Batch Evaluation

```python
from z3adapter.reasoning import EvaluationPipeline, ProofOfThought

evaluator = EvaluationPipeline(proof_of_thought=pot, output_dir="results/")
result = evaluator.evaluate(
    dataset="data/strategyQA_train.json",
    question_field="question",
    answer_field="answer",
    max_samples=10
)
print(f"Accuracy: {result.metrics.accuracy:.2%}")
```

## Running Experiments

You can use this repository as a strong baseline for LLM+Solver methods. This code is generally benchmarked with GPT-5 on the first 100 samples of 5 datasets, as an indicator of whether we broke something during development. These numbers are not the best, and you can certainly get better numbers with better prompt engineering with this same tooling. Please feel free to put in a PR if you get better numbers with modified prompts.

To run all benchmarks with both backends and generate results:

```bash
python experiments_pipeline.py
```

This will:
- Run all 5 benchmarks (ProntoQA, FOLIO, ProofWriter, ConditionalQA, StrategyQA)
- Test both SMT2 and JSON backends
- Generate results tables in `results/`
- Automatically update the benchmark results section below
