---
tags:
  - Smart-Foodsheds
  - AI4CI
  - Release 2025-05
  - Release 2025-08
---

# Multi-Scale Food Flow Prediction using Graph Neural Networks

A project leveraging Graph Neural Networks (GNNs) to predict food flows between counties and FAF zones for economic planning, infrastructure development, and policy-making. This model predicts food trade flows between U.S. counties and Freight Analysis Framework (FAF) zones using Graph Neural Networks (GNNs). It addresses the challenges of sparsity in trade data by applying a two-stage hurdle model that distinguishes between the presence and magnitude of trade.

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/GeoDS/GNNFoodFlow)

## References

### Data Sources
- **Trade Data**: [FAF5.6.1 SCTG1 commodity flow data](https://faf.ornl.gov/faf5/) (`code/data/FAF5_SCTG1.csv`)
- **Geographic Information**:
  - County shapefiles (`code/data/shapefiles/cb_2017_us_county_500k/cb_2017_us_county_500k.shp`)
  - State shapefiles (`code/data/shapefiles/cb_2018_us_state_20m/cb_2018_us_state_20m.shp`)
  - FAF zones shapefiles (`code/data/shapefiles/2017_CFS_Metro_Areas_with_FAF/2017_CFS_Metro_Areas_with_FAF.shp`)
- **Economic Indicators**: County-level economic data (`code/data/faf_features.csv`)
- **Distance Information**: FAF Distance Matrix (`code/data/FAF_Distance_Matrix.csv`)

## Acknowledgements
National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)

## Future Work
- Extending the model to handle inter-county food trade flow predictions
- Refining the model to capture more granular food trade patterns