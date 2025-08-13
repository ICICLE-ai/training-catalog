---
tags:
  - Smart-Foodsheds
  - AI4CI
---


# How-To Guides

Follow these steps to set up and run the GNN Food Flow Portal locally.

### 1. Clone the repository
```bash
git clone https://github.com/ICICLE-ai/GNNFoodFlowPortal.git

cd GNNFoodFlowPortal

```

### 2. Create a Python environment & install dependencies
```bash
conda create -n gnnfoodflow python=3.10

conda activate gnnfoodflow

pip install -r requirements.txt
```
### 3. Prepare the data

This repo has included all necessary datasets for the portal

### 4. Run the portal locally
```bash
streamlit run app.py
```

### 5. Explore the portal
Use the filter panel to select:

- Commodity code (SCTG1-7)

- Origin/Destination county or state

Click Download Tab to export filtered flows as CSV for your research.

#### Filtered Results
Filtered results represent original datasets referenced by the models.

#### Summary Statistics
Summary Statistics are the necessary and simplified version for county-level food flows.



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

- **Shapefiles**: [USA Census Cartographic Boundary Files - Shapefile](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)