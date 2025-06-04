---
tags:
  - Smart-Foodsheds
  - AI4CI
---

# How-To Guides

### How to Implement a Hurdle Model for Trade Prediction
- **Problem**: Predicting trade flows with many zero values
- **Solution**: Implement a two-stage hurdle model that:
  1. First predicts whether trade exists between two regions
  2. Then estimates the volume of trade when it exists
- **Code example**: See the GAT model implementation in `code/model.py`

### How to Incorporate Geographic and Economic Features
- **Problem**: Capturing complex relationships in trade networks
- **Solution**: Combine multiple feature types:
  - County-level economic indicators (population, employment_rate, median_income)
  - Geographic distance and transportation modes
  - Industry diversity metrics