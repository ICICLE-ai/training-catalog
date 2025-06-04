---
tags:
  - Foundation-AI
---

# Tutorials 

### Basic Usage

```python
from forte_api import ForteOODDetector
import glob

# Collect in-distribution images
id_images = glob.glob("data/normal_class/*.jpg")

# Split for training and testing
train_images = id_images[:800]
test_id_images = id_images[800:]

# Collect OOD images
ood_images = glob.glob("data/anomalies/*.jpg")

# Create and train detector
detector = ForteOODDetector(
    batch_size=32,
    device="cuda:0",
    method="gmm"
)

# Train the detector
detector.fit(train_images)

# Evaluate performance
metrics = detector.evaluate(test_id_images, ood_images)
print(f"AUROC: {metrics['AUROC']:.4f}")
print(f"FPR@95TPR: {metrics['FPR@95TPR']:.4f}")

# Get predictions
predictions = detector.predict(ood_images)
```

### Complete Example with CIFAR-10/CIFAR-100

For a complete example using CIFAR-10 as in-distribution and CIFAR-100 as out-of-distribution data, see the [examples/cifar_demo.py](examples/cifar_demo.py) script in the repository.

### Experimenting with Different Methods

```python
# Try different detection methods
methods = ['gmm', 'kde', 'ocsvm']
results = {}

for method in methods:
    detector = ForteOODDetector(method=method)
    detector.fit(train_images)
    results[method] = detector.evaluate(test_id_images, ood_images)

# Compare results
for method, metrics in results.items():
    print(f"{method.upper()} - AUROC: {metrics['AUROC']:.4f}, FPR@95TPR: {metrics['FPR@95TPR']:.4f}")
```

## Model Details

### Feature Extraction Models

Forte uses three pretrained models for feature extraction:

1. **CLIP** (Contrastive Language-Image Pretraining): Captures semantic information aligned with natural language concepts
2. **ViT-MSN** (Vision Transformer with Masked Self-supervised Network): Captures fine-grained visual patterns
3. **DINOv2** (Self-supervised Vision Transformer): Captures hierarchical visual representations

You may modify the code to use your own encoder if you wish. This may be a CNN or a ViT. Anything you want.
