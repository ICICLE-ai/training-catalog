---
tags:
  - Smart-Foodsheds
  - Release 2025-07
---

# organization-sic-classifier-for-smart-foodsheds


This repository contains code for training and evaluating models that classify organizations into Standard Industrial Classification (SIC) codes based on different types of descriptive text.  This model is designed for researchers and data scientists who need to categorize unknown or newly listed organizations by business type. It can be applied to tasks such as food systems research, analyzing supply chains, and regional economic mapping, particularly in scenarios where structured corpora are unavailable. Given only an organization’s name and its description, the model predicts a high-level SIC category.

While the current focus is on SIC code classification, this framework can be adapted for any text-based classification task across domains, as long as an entity list and corresponding gold labels are available. The data used for training and evaluation is hosted on Hugging Face and should be downloaded separately.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/organization-sic-classifier-for-smart-foodsheds)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Acknowledgements
National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)