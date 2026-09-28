---
tags:
  - Smart-Foodsheds
  - AI4CI
title: "Multi-Scale Food Flow Prediction using Graph Neural Networks: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for Multi-Scale Food Flow Prediction using Graph Neural Networks. A project leveraging Graph Neural Networks (GNNs) to predict food flows…"
---

# How-To Guides

### How to Implement a Hurdle Model for Trade Prediction
- **Problem**: Predicting trade flows with many zero values
- **Solution**: Implement a two-stage hurdle model that:
  1. First predicts whether trade exists between two regions
  2. Then estimates the volume of trade when it exists
- **Code example**: See the GAT model implementation in `code/model.py` https://github.com/GeoDS/GNNFoodFlow/blob/master/code/model.py
- **Results**: See the resulted models in `code/models`, https://github.com/GeoDS/GNNFoodFlow/tree/master/code/models note that models for different SCTG02 codes has to be trained separately

### Prerequisites
- Python 3.9+
- PyTorch (>=1.9.0)
- PyTorch Geometric (>=2.0.0)
- Other dependencies (see Hugging Face page for complete list)

### How to Incorporate Geographic and Economic Features
- **Problem**: Capturing complex relationships in trade networks
- **Solution**: Combine multiple feature types:
  - County-level economic indicators (population, employment_rate, median_income)
  - Geographic distance and transportation modes
  - Industry diversity metrics
