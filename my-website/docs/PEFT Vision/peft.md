---
tags:
  - Foundation-AI
---

# PEFT Vision

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Lessons and Insights from a Unifying Study of Parameter-Efficient Fine-Tuning (PEFT) in Visual Recognition
 
### A Systematic Framework for Parameter-Efficient Fine Tuning (PEFT) in Visual Recognition 

Parameter-efficient fine-tuning (PEFT) has attracted significant attention lately due to the increasing size of pre-trained models and the need to fine-tune them for superior downstream performance. This community-wide enthusiasm has
sparked a plethora of approaches. We provide a systematic and comprehensive code base implementing 16 PEFL methods, which serves as a valuable resource for researchers and enables **consistent and reproducible evaluations** of PEFT methods. We conduct a unifying empirical study of 16 representative PEFT approaches in **various scenarios**, including low shots, many shots, different domain gaps, and robustness between in-distribution and OOD. Our findings offer several insightful directions for future research, including **leveraging prediction differences** in other learning paradigms such as semi-supervised learning and domain adaptation, **robust fine-tuning with PEFT**, and  providing **empirical evidence for PEFT mechanism understanding**.

More details can be found in [our paper](https://arxiv.org/pdf/2409.16434) and [project page](https://zheda-mai.github.io/PEFT_Vision_CVPR25/). 


## Citation 

If you use this paper/code in your research, please consider citing us:

```
@article{mai2024lessons,
  title={Lessons learned from a unifying empirical study of parameter-efficient transfer learning (petl) in visual recognition},
  author={Mai, Zheda and Zhang, Ping and Tu, Cheng-Hao and Chen, Hong-You and Zhang, Li and Chao, Wei-Lun},
  journal={arXiv preprint arXiv:2409.16434},
  year={2024}
}
```

## References:
Detailed references  can be found [here](https://github.com/OSU-MLB/ViT_PEFT_Vision?tab=readme-ov-file).

## Acknowledgement
This work has been sponsored in part by grants from the National Science Fundation, including the ICICLE AI Institute (OAC 2112606), Amazon, and Ohio Supercomputer Center.