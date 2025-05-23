---
tags:
  - Foundation-AI
---

# How-To Guides

**Key Features inside Forte**

- **Multiple feature extractors**: Leverages CLIP, ViT-MSN, and DINOv2 models for robust semantic representation
- **Topology-aware scoring**: Uses Precision, Recall, Density, and Coverage (PRDC) metrics to capture manifold structure
- **Multiple detection methods**: Supports Gaussian Mixture Models (GMM), Kernel Density Estimation (KDE), and One-Class SVM (OCSVM)
- **Automatic hyperparameter selection**: Optimizes model hyperparameters using validation data
- **Caching for efficiency**: Saves extracted features to avoid redundant computation

## API Reference

### `ForteOODDetector`

The main class for OOD detection.

```python
detector = ForteOODDetector(
    batch_size=32,
    device=None,
    embedding_dir="./embeddings",
    nearest_k=5,
    method='gmm'
)
```

#### Parameters

- **batch_size** (int, default=32): Batch size for processing images during feature extraction
- **device** (str, default=None): Device to use for computation (e.g., 'cuda:0', 'cpu'). If None, uses CUDA if available
- **embedding_dir** (str, default='./embeddings'): Directory to store extracted features for caching
- **nearest_k** (int, default=5): Number of nearest neighbors for PRDC computation
- **method** (str, default='gmm'): Method to use for OOD detection. Options:
  - 'gmm': Gaussian Mixture Model (best for clustered data)
  - 'kde': Kernel Density Estimation (best for smooth distributions)
  - 'ocsvm': One-Class SVM (best for complex boundaries)

### Methods

#### `fit(id_image_paths, val_split=0.2, random_state=42)`

Fits the OOD detector on in-distribution data.

**Parameters:**
- **id_image_paths** (list): List of paths to in-distribution images
- **val_split** (float, default=0.2): Fraction of data to use for validation
- **random_state** (int, default=42): Random seed for reproducibility

**Returns:**
- The fitted detector object

**Process:**
1. Splits data into training and validation sets
2. Extracts features using pretrained models
3. Computes PRDC features
4. Trains the OOD detector (GMM, KDE, or OCSVM)

```python
detector.fit(id_image_paths, val_split=0.2, random_state=42)
```

#### `predict(image_paths)`

Predicts if samples are OOD.

**Parameters:**
- **image_paths** (list): List of paths to images

**Returns:**
- Binary array (1 for in-distribution, -1 for OOD)

```python
predictions = detector.predict(test_image_paths)
```

#### `predict_proba(image_paths)`

Returns normalized probability scores for OOD detection.

**Parameters:**
- **image_paths** (list): List of paths to images

**Returns:**
- Array of normalized scores (higher values indicate in-distribution)

```python
scores = detector.predict_proba(test_image_paths)
```

#### `evaluate(id_image_paths, ood_image_paths)`

Evaluates the OOD detector on in-distribution and out-of-distribution data.

**Parameters:**
- **id_image_paths** (list): List of paths to in-distribution images
- **ood_image_paths** (list): List of paths to out-of-distribution images

**Returns:**
- Dictionary of evaluation metrics:
  - **AUROC**: Area Under the Receiver Operating Characteristic curve
  - **FPR@95TPR**: False Positive Rate at 95% True Positive Rate
  - **AUPRC**: Area Under the Precision-Recall Curve
  - **F1**: Maximum F1 score

```python
metrics = detector.evaluate(id_image_paths, ood_image_paths)
print(f"AUROC: {metrics['AUROC']:.4f}")
```