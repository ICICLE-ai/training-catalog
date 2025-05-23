---
tags:
  - Foundation-AI
---

# Explanation

## Data Preparation
You can run ScienceAgent on your own data by preparing a CSV file. Each entry should have at least the following columns:
- `task_inst`: task instruction
- `domain_knowledge`: optional domain knowledge, usually annotated by subject matter experts.
- `dataset_folder_tree`: folder tree structure of the dataset(s)
- `dataset_preview`: preview of a few entries in the dataset(s)

We provide an example task from ScienceAgentBench in `benchmark/ScienceAgentBench.csv`.The additional fields are for evaluation of agent performance, which is not covered by this repository. 
For a full evaluation on ScienceAgentBench, please refer to the [ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench) repo!
