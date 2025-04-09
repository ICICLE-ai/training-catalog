---
tags:
  - Smart-Foodsheds
  - AI4CI
---

# Multi-Scale Food Flow Prediction using Graph Neural Networks
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A project leveraging Graph Neural Networks (GNNs) to predict food flows between counties and FAF zones for economic planning, infrastructure development, and policy-making.

## References

### Data Sources
- **Trade Data**: FAF5 SCTG1 commodity flow data (`code/data/FAF5_SCTG1.csv`)
- **Geographic Information**:
  - County shapefiles (`code/data/shapefiles/cb_2017_us_county_500k/cb_2017_us_county_500k.shp`)
  - State shapefiles (`code/data/shapefiles/cb_2018_us_state_20m/cb_2018_us_state_20m.shp`)
  - FAF zones shapefiles (`code/data/shapefiles/2017_CFS_Metro_Areas_with_FAF/2017_CFS_Metro_Areas_with_FAF.shp`)
- **Economic Indicators**: County-level economic data (`code/data/faf_features.csv`)
- **Distance Information**: FAF Distance Matrix (`code/data/FAF_Distance_Matrix.csv`)

## Acknowledgements
National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)

## Future Work
- Extending the model to handle inter-county trade flow predictions
- Refining the model to capture more granular trade patterns
- Implementing visualization tools for inter-county trade networks