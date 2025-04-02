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
