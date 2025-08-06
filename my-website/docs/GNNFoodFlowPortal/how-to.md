---
tags:
  - Smart-Foodsheds
  - AI4CI
---


# How-To Guides
- Install Dependencies

- streamlit run app.py

### Downstream Use
- Spatial forecasting of trade changes under policy shifts
- Identifying critical counties for supply chain resilience

### Out-of-Scope Use
- Real-time food trade forecasting
- Non-U.S. geographic settings without retraining

## Bias, Risks, and Limitations
- **Bias**: Model predictions depend on historical FAF data and may not reflect unexpected future disruptions (e.g., disasters, pandemics)
- **Limitations**: Prediction is limited to predefined commodity codes (SCTG1-7)
- **Data quality**: Assumes accuracy of FAF flow data and economic indicators

### Data Sources
- **Trade Data**: [FAF5.6.1 SCTG1 commodity flow data](https://faf.ornl.gov/faf5/)