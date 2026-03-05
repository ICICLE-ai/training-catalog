---
tags:
  - AI4CI
---
# How-To Guides
## Installation
Clone this repository and install the required packages:
```
git clone https://github.com/OSU-NLP-Group/AutoSDT
cd AutoSDT
pip install -r requirements.txt
```

## AutoSDT Pipeline
### Configure Azure endpoint and API key
```
vim ~/.bashrc
export AZURE_OPENAI_KEY=YOUR_AZURE_API_KEY
export AZURE_ENDPOINT=YOUR_AZURE_ENDPOINT
export AZURE_API_VERSION=YOUR_AZURE_API_VERSION
source ~/.bashrc
```

### AutoSDT-Search: Search for research related repositories
```
cd autosdt/scripts
bash run_search.sh
```

Specify discipline keywords in the `base_keywords` argument.

### AutoSDT-Select: Crawl python files, verify tasks, and prepare workspaces
```
bash run_crawl_files.sh
bash run_scientific_task_verify.sh
bash run_locate_dependencies.sh
bash run_prepare_env.sh
```

### AutoSDT-Adapt: Adapt programs and generate task instructions
```
bash run_adapt_code.sh
bash run_generate_instruction.sh
```

After the above steps, you should obtain a `final_combined_training_data.jsonl` containing generated instructions and code. Then run:
```
python convert_data_to_alpaca_format.py
```
