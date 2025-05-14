---
tags:
  - Foundational-AI
---

# Explanation

## Features

1. **Encourages Accountability**

   * Incorporate essential model information (metadata, dataset details, fairness, explainability) at training time, ensuring AI models remain transparent from development to deployment.

2. **Semi-Automated Capture**

   * Automated *Fairness* and *Explainability* scanners compute demographic parity, equal odds, SHAP-based feature importances, etc., for easy integration into Model Cards.

3. **Machine-Actionable Model Cards**

   * Produce a structured JSON representation for ingestion into the Patra Knowledge Base. Ideal for advanced queries on model selection, provenance, versioning, or auditing.

4. **Flexible Repository Support**

   * Pluggable backends for storing models/artifacts on **Hugging Face** or **GitHub**, unifying the model publishing workflow.

5. **Versioning & Model Relationship Tracking**

   * Maintain multiple versions of a model with recognized edges (e.g., `revisionOf`, `alternateOf`) using embedding-based similarity. This ensures clear lineages and easy forward/backward provenance.
