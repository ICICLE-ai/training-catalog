---
tags:
  - Smart-Foodsheds
---

# How-To Guides

### Repository Clone

To get started, first clone the GitHub repository:

```
bash
git clone https://github.com/ICICLE-ai/organization-sic-classifier-for-smart-foodsheds.git
cd organization-sic-classifier-for-smart-foodsheds
```
### Create and Activate Virtual Environment
Create a virtual environment:

```
bash
python3 -m venv venv
```

Activate the virtual environment:

- On macOS/Linux:
```
bash
source venv/bin/activate
```
- On Windows:
  
```
bash
venv\Scripts\activate
```
Install all required Python packages:

```
bash
pip install -r requirements.txt
```
### Dataset

The dataset is available on Hugging Face and must be downloaded before running any training or testing script.

### Dataset Download Instructions

```
bash
git lfs install
git clone https://huggingface.co/datasets/ICICLE-AI/organization-sic-code_smart-foodsheds

After downloading, extract and place the unzipped data/ folder in the root directory (next to src/).
```
### Dataset Variants

The dataset includes multiple variants based on the source of the organization descriptions:

- gsnip: Google search snippets  
- gptsummary: GPT-4o-mini generated summaries  
- llamasummary: LLaMA 3.1–8B Instruct generated summaries  
- gsnip+gptsummary: Combined inputs of google snippets + GPT-4o-mini generated summaries
- gsnip+llamasummary: Combined inputs of google snippets + LLaMA 3.1–8B Instruct generated summaries  

Each variant includes the following splits:

- train.csv
- dev.csv
- test.csv
