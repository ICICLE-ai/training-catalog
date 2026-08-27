---
tags:
  - Digital-Agriculture
  - Foundation-AI
---
# Tutorials

### Overview

The Yield Estimation Transformer is a pretrained model for in-season county-level corn yield estimation. It combines temporal weekly weather observations with static soil properties and produces a scalar yield prediction in bushels per acre.

The model accepts six weekly weather variables:

- `prcp`
- `srad`
- `swe`
- `tmax`
- `tmin`
- `vp`

It also uses 66 static soil features defined in `config.json`.

The model supports prediction cutoffs at:

```text
20, 24, 28, 32, 36, 40, 44, 48, 52
```

A cutoff determines how many weeks of weather information are available to the model. A cutoff of `52` represents full-season inference.

For deployment through FlexServ, the model uses the Hugging Face `text-classification` pipeline as its serving interface. This is an interface choice for inference compatibility; the underlying prediction task remains regression.