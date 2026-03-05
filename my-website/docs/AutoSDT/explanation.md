---
tags:
  - AI4CI
---
# Explanation
AutoSDT is designed to maximize ecological validity of scientific programming tasks while minimizing manual curation cost.

- AutoSDT-Search improves repository recall by discipline-specific keyword generation.
- AutoSDT-Select improves data quality by verifying scientific-task relevance and isolating executable dependencies.
- AutoSDT-Adapt improves usability by converting fragmented code into standalone tasks with instructions.

This design supports both training (task-solution supervision) and evaluation (realistic scientific coding benchmarks).

## Training and Inference
### Supervised Fine-tuning
We use the [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) library for SFT. Example config files are provided in the `models/` folder.

### Inference and Evaluation
For ScienceAgentBench, follow its original repository instructions.

For DiscoveryBench, first start an LLM engine at localhost using [vllm](https://docs.vllm.ai/en/latest/), then run:
```
python evaluate_with_llm_engine.py
```

Then compute final metrics:
```
python cal_eval_avg.py
```

## Acknowledgements

This work is supported in part by the National Science Foundation (NSF) funded AI Institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) under award OAC 2112606.
