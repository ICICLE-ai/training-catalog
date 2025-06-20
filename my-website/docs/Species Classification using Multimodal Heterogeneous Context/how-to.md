---
tags:
  - Foundation-AI
---

# How-To Guides

## Installation

```
pip install -r requirements.txt
```

### Species classification on a single image input
Note: Some sample camera trap species images are available in the dir. `data/sample_images/`. During training, we utlize multiple heterogeneous contexts in the multimodal KG. However, at inference time, only the image is used to perform species classification.

1. Download the required data `bash download_data.sh`.
2. Evaluate the pretrained model on a given image.
```
python eval_image.py --ckpt-path <PATH TO TRAINED CKPT> --img-path <PATH TO IMG FILE>
```

## Data Preprocessing
This will download the iWildCam2020-WILDS dataset and Open Tree of Life taxonomy and pre-process them.
```
bash preprocess.sh
```

Note: The dir. `data/iwildcam_v2.0/train/` contains images for all splits.

## Training a model from scratch

We consider different training settings that comprise of combination of different context types such as taxonomy, location, and time.

### Train using only images linked to species labels
```
python -u main.py --data-dir data/iwildcam_v2.0/ --img-dir data/iwildcam_v2.0/train/ --save-dir CKPT_DIR > CKPT_DIR/log.txt
```

### Train using species labels and taxonomy contexts
```
python -u main.py --data-dir data/iwildcam_v2.0/ --img-dir data/iwildcam_v2.0/train/ --save-dir CKPT_DIR --add-id-id > CKPT_DIR/log.txt
```

### Train using species labels and location contexts
```
python -u main.py --data-dir data/iwildcam_v2.0/ --img-dir data/iwildcam_v2.0/train/ --save-dir CKPT_DIR --add-image-location > CKPT_DIR/log.txt
```

### Train using species labels and time contexts
```
python -u main.py --data-dir data/iwildcam_v2.0/ --img-dir data/iwildcam_v2.0/train/ --save-dir CKPT_DIR --add-image-time > CKPT_DIR/log.txt
```

### Train using species labels, taxonomy, and time contexts
```
python -u main.py --data-dir data/iwildcam_v2.0/ --img-dir data/iwildcam_v2.0/train/ --save-dir CKPT_DIR --add-id-id --add-image-time > CKPT_DIR/log.txt
```

###  Train using species labels, taxonomy, and location contexts
```
python -u main.py --data-dir data/iwildcam_v2.0/ --img-dir data/iwildcam_v2.0/train/ --save-dir CKPT_DIR --add-id-id --add-image-location > CKPT_DIR/log.txt
```

### evaluate a model (specify split=val/test/id_val/id_test)
```
python eval.py --ckpt-path <PATH TO TRAINED CKPT> --split test --data-dir data/iwildcam_v2.0/ --img-dir data/iwildcam_v2.0/train/
```
