---
tags:
  - Smart-Foodsheds
  - AI4CI
---

# Explanation

### Graph Neural Networks for Trade Flow Prediction
Our approach uses Graph Neural Networks to model trade relationships between counties and FAF zones. The model architecture includes:
- Graph Attention Networks (GAT) to capture the importance of different connections
- Graph Convolutional Networks (GCN) for comparison
- A hurdle model approach that separates the prediction into classification and regression tasks

This design better handles the sparse nature of trade networks where many county pairs have zero trade. The model learns both from geographic proximity and economic similarity, providing more accurate predictions than traditional statistical methods.

## For Detailed Usage

- **Complete setup instructions**: [Hugging Face - Setup Instructions](https://huggingface.co/ICICLE-AI/FoodFlow_GNN_Model)
- **Data download links**: [FoodFlow Inference Data](https://drive.google.com/drive/u/0/folders/1mnlbiRvBHw4Hy2iU-i1IvElLw3Uuf0aV)
- **Information for Visualization portal**: [FoodFlowPortal](https://huggingface.co/ICICLE-AI/FoodFlow_GNN_Model)
- **Troubleshooting**: [Hugging Face - Troubleshooting](https://huggingface.co/ICICLE-AI/FoodFlow_GNN_Model)

### Direct Use
- Predicting food flows between regions using node (county/FAF zone) and edge features
- Modeling economic connectivity and transportation dependency

The visualization portal has moved!  
Please visit the new portal here: **[GNN Food Flow Portal](https://gnnfoodflowportal.pods.icicleai.tapis.io/)** for the latest interactive visualization and download features.

Please go to https://github.com/ICICLE-ai/GNNFoodFlowPortal/ for more updated information and better accessability

### Downstream Use
- Spatial forecasting of trade changes under policy shifts
- Identifying critical counties for supply chain resilience

### Out-of-Scope Use
- Real-time food trade forecasting
- Non-U.S. geographic settings without retraining

## Bias, Risks, and Limitations
- **Bias**: Model predictions depend on historical FAF data and may not reflect unexpected future disruptions (e.g., disasters, pandemics)
- **Limitations**: Prediction is limited to predefined commodity codes (SCTG1)
- **Data quality**: Assumes accuracy of FAF flow data and economic indicators

## Recommendations
Users should:
- Evaluate model generalizability before applying it to non-FAF settings
- Interpret sparse predictions carefully—zeros may result from missing data, not true absence