---
tags:
  - Digital-Agriculture
  - Foundation-AI
  - Release 2026-08
---
# Yield Estimation Transformer

A Hugging Face custom pipeline using Transformers model for county-level corn yield estimation using multi-temporal weather observations and static soil properties.

The model combines weekly weather time-series with static soil features to estimate corn yield in bushels per acre (`bu/acre`). It is packaged for inference using Hugging Face Transformers and has been tested for deployment through FlexServ.

The Hugging Face `text-classification` task is used as the FlexServ-compatible serving interface. The underlying model performs regression, and the returned `score` represents predicted corn yield in `bu/acre`.

The `training_code` directory composes the source code for data preparation, model training, evaluation, and inference.

<div align="center">

[![Hugging Face Model Card](https://img.shields.io/badge/Hugging%20Face-Model%20Card-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/ICICLE-AI/yield-estimation)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

:::tip Model card
This component is distributed on Hugging Face — see the full model card at [ICICLE-AI/yield-estimation](https://huggingface.co/ICICLE-AI/yield-estimation).
:::

### License

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
This project is released under the MIT License. The full text is available in [LICENSE](https://huggingface.co/ICICLE-AI/yield-estimation/blob/main/LICENSE).

## References

### USA County Level Crop Yield Dataset

This model uses the USA County Level Crop Yield Dataset. 

```bibtex

@article{Khaki2020CNNRNN,
  author    = {Khaki, Saeed and Wang, Liang and Archontoulis, Sotirios V.},
  title     = {A CNN-RNN Framework for Crop Yield Prediction},
  journal   = {Frontiers in Plant Science},
  volume    = {10},
  pages     = {1750},
  year      = {2020},
  doi       = {10.3389/fpls.2019.01750},
  publisher = {Frontiers Media SA}
}

```

### FlexServ

The model is packaged and validated for deployment with FlexServ.

FlexServ documentation: https://zhangwei217245.github.io/FlexServ/

## Acknowledgements

This work was developed as part of the ICICLE AI Institute.

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Contact:

For questions or support:

Sarikaa Sridhar: sridhar.86@buckeyemail.osu.edu
