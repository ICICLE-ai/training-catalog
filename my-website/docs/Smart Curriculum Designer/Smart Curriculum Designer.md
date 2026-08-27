---
tags:
  - AI4CI
  - CI4AI
  - Foundation-AI
  - Visual-Analytics
  - Release 2026-08
---
# Smart Curriculum Designer

An AI-driven educational framework that integrates automated curriculum generation with an end-to-end computer vision pipeline, enabling learning for high school and undergraduate students combining domain agnostic datasets with machine learning and AI concepts.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/curriculum-generator)
[![License: BSD_3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](./LICENSE)

</div>


## References

- [Tapis v3 — HPC job execution framework](https://tapis-project.org)
- [DINOv2 — Learning Robust Visual Features without Supervision](https://github.com/facebookresearch/dinov2)
- [Segment Anything (SAM) — Meta AI Foundation Model](https://github.com/facebookresearch/segment-anything)
- [Ohio Supercomputer Center (OSC)](https://www.osc.edu/)
- [ICICLE AI Institute](https://icicle.ai/)

## Acknowledgements
*Developed at The Ohio State University (Systems and AI Lab, advised by Dr. Hari Subramoni), subsequently submitted to and implemented as part of the AI Presidential Challenge, with domain expertise and educator feedback from Dr. Scott Shearer and Dr. Lisa Abrams, and pilot deployment support from the Columbus School for Girls.*

## Issue reporting

Please open an issue at [github.com/ICICLE-ai/curriculum-generator/issues](https://github.com/OSU-SAI-Lab/curriculum_generator/issues) with a description of the problem, steps to reproduce, and any relevant logs from pipeline runs or cluster jobs.

## Tutorials

- **Step-by-Step Tutorials & Deployment:** [HOW_TO_USE.md](https://github.com/ICICLE-ai/curriculum-generator/blob/main/documentation/documentation/HOW_TO_USE.md)
- **YAML Configuration Guide & Reference:** [YAML_CONFIG_GUIDE.md](https://github.com/ICICLE-ai/curriculum-generator/blob/main/documentation/documentation/YAML_CONFIG_GUIDE.md)
- **Curriculum Module Reference:** [TEMPLATES_GUIDE.md](https://github.com/ICICLE-ai/curriculum-generator/blob/main/documentation/documentation/TEMPLATES_GUIDE.md)

---

### Project Philosophy: The Pipeline is the Curriculum

Traditional AI education frequently treats machine learning as a simplified black box using sterile datasets that mask real-world data science challenges. DigitalAgEdu adheres to the principle that **the pipeline itself is the curriculum**. 

Rather than working on generic toy examples, learners execute an end-to-end foundation model pipeline on authentic domain datasets (agriculture, dermatology, disaster response, etc.). The metrics, class imbalances, confusion matrices, and segmentation masks generated during execution are dynamically injected into scaffolded Python exercises. Students dissect, recreate, optimize, and explain the exact stages they just witnessed.

```
       Image Dataset (Any Domain)
                    │
                    ▼
    [1] Image Acquisition        (Validation, resolution check, class distribution)
                    │
                    ▼
    [2] DINOv2 Classification    (Transfer learning & robust visual representation)
                    │
                    ▼
    [3] SAM Segmentation         (Promptable region-of-interest mask extraction)
                    │
                    ▼
    [4] Phi-3-Vision VLM         (Multimodal reasoning & visual explanations)
                    │
                    ▼
    [5] Dynamic Curriculum       (Syllabus compilation, scaffolded coding exercises)
```

### End-to-End Architecture

The DigitalAgEdu architecture consists of decoupled modular systems:

- **Orchestrator & Scanner (`digitalagedu/core/`):** Ingests YAML configurations, parses image directories, computes class distributions, and validates execution readiness.
- **Model Execution Stages (`digitalagedu/stages/`):** Runs DINOv2 classification, SAM segmentation, and Phi-3-Vision reasoning.
- **Dynamic Curriculum Engine (`digitalagedu/core/practice_generator.py`):** Ingests execution metrics and injects domain data into student exercises and reference solutions.

### Computer Vision Foundation Models

- **DINOv2 (Vision Transformer Backbone):** Utilizes self-supervised Vision Transformers (ViT) to extract domain-invariant image representations. Enables high classification precision without requiring massive labeled training sets.
- **Segment Anything Model (SAM):** Generates zero-shot promptable segmentation masks to isolate regions of interest (e.g. lesion borders, leaf foliage, flood zones).
- **Phi-3-Vision (Multimodal VLM):** Provides natural language explanations grounded in visual evidence, teaching students how multimodal reasoning systems interpret complex imagery.

### Dynamic Exercise Generation Engine

The dynamic generator converts master templates in `digitalagedu/templates/` into grade-appropriate student assignments. Each module comprises:
- **`[topic]_exercise.py`:** Scaffolded student workspace with docstrings, type hints, and `# TODO` milestones.
- **`[topic]_solution.py`:** Fully implemented reference solution for instructors.
- **`[topic]_test.py`:** Automated unit tests verifying tensor dimensions, return types, and algorithmic accuracy.
- **`concepts.md` & `resource.md`:** Comprehensive theoretical background and curated reading materials.
