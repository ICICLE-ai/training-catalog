---
tags:
  - AI4CI
---
# Tutorials
### Quickstart Tutorial
1. Install dependencies with `pip install -r requirements.txt`.
2. Configure Azure/OpenAI environment variables.
3. Run Search -> Select -> Adapt pipeline scripts in order.
4. Verify `final_combined_training_data.jsonl` is generated.
5. Convert data format with `python convert_data_to_alpaca_format.py`.

### Prerequisites
- Python 3.10+
- Required Python packages from `requirements.txt`
- Valid API credentials for the configured LLM provider

### Expected End Result
You will get a structured training dataset of scientific coding tasks that can be used directly for supervised fine-tuning.

## How-To Guides
### How to run only one pipeline stage
- Search only: run `bash run_search.sh`
- Select only: run `bash run_crawl_files.sh`, `bash run_scientific_task_verify.sh`, `bash run_locate_dependencies.sh`, `bash run_prepare_env.sh`
- Adapt only: run `bash run_adapt_code.sh`, `bash run_generate_instruction.sh`

### How to fine-tune models
1. Prepare Alpaca-format training data.
2. Use LLaMA-Factory configs in `models/`.
3. Launch supervised fine-tuning with your selected config.

### Troubleshooting
- If API requests fail, verify endpoint, key, and API version.
- If scripts fail due to missing dependencies, reinstall via `pip install -r requirements.txt`.
- If outputs are empty, check logs and intermediate files under each pipeline stage.
