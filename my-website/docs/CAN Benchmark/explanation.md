---
tags:
  - Foundation-AI
---
# Explanation
### Dataset Structure
The dataset consists of of two folders:
- `images`: You can find all the images from a camera trap CDB-D06
- `'30'`: You will find three json files in this folder. The whole camera trap dataset has been divided into 30 days interval, for continual learning.
   - `train.json` : Json file for training data divided into 30 days interval.
   - `train-all.json`:Json file containing all training data.
   - `test.json`: Json file containing all test data divided into 30 days interval.

### Dataset Overview

- **Total Size:** ~2.1 TB
- **Total Images:** 3,317,354
- **Regions Covered (17):** apn, cdb, eno, kar, kga, kru, mad, mtz, pln, rua, nz (excluding nz_bad), orinoquia, idaho, serengeti, wellington, caltech, na
- **Number of Cameras:** 546
- **File Format:** JPG
- **Image Resolution Range:** min 56×58, max 1920×2560
- **Average Classes per Dataset:** ~11

### Access

To request access to the full dataset, please contact the maintainers at: **jeon.193@osu.edu**
