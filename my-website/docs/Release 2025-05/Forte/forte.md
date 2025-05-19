---
tags:
  - Foundation-AI
---

# Forte Overview
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


The Forte library provides robust out-of-distribution (OOD) detection capabilities through the `ForteOODDetector` class. The core algorithm is built on the principle of **F**inding **O**utliers using **R**epresentation **T**ypicality **E**stimation, which:

1. Uses self-supervised vision models to extract semantic features
2. Incorporates manifold estimation to account for local topology
3. Requires no class labels or exposure to OOD data during training

This makes Forte particularly useful for real-world applications where anomalous data may be unexpected or unknown at training time. Our goal is to provide a non-opinionated middleware for OOD detection that seamlessly integrates into your ML deployment pipelines.

**Why use Forte?**
Forte OOD Detection serves as middleware between your data ingestion and ML inference systems, by preventing models from making predictions on data they weren't designed to handle. 

### Acknowledgements
National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)