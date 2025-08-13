---
tags:
  - Software
  - Animal Ecology
  - Release 2025-08
---

# Video-Based Animal Re-Identification (VARe-ID) from Multiview Spatio-Temporal Track Clustering

This work presents a modular software pipeline and end-to-end workflow for video-based animal re-identification, which assigns consistent individual IDs by clustering multiview spatio-temporal tracks with minimal human intervention. Starting from raw video, the system detects and tracks animals, scores and selects informative left/right views, computes embeddings, clusters annotations by viewpoint, and then links clusters across time and varying perspectives using spatio-temporal continuity. Automated consistency checks resolve remaining ambiguities. Preliminary experiments demonstrate near-perfect identification accuracy with very limited manual verification. The workflow is designed to be generalizable across species. Currently, trained models support Grevy’s and Plains zebras, with plans to expand to a broader range of species.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ziesski/VARe-ID)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://github.com/user-attachments/assets/8ddd01a3-6511-40f7-b182-41c479ad447b" alt="image" width="862" height="896"/>
</p>


## References

### Links to related resources (libraries, tools, etc.) or external documentation
* [YOLOv10](https://github.com/THU-MIG/yolov10)
* [BioCLIP](https://github.com/Imageomics/bioclip)
* [MiewID](https://github.com/WildMeOrg/wbia-plugin-miew-id)
* [LCA](https://github.com/WildMeOrg/lca)

   
## Acknowledgements

* **National Science Foundation (NSF)** funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606).
* **Imageomics Institute (A New Frontier of Biological Information Powered by Knowledge-Guided Machine Learning)** is funded by the US National Science Foundation's Harnessing the Data Revolution (HDR) program under Award (OAC 2118240).
* Support from **Rensselaer Polytechnic Institute (RPI)**.
* Support from **Finnish Cultural Foundation**.
* Resources from **Ohio Supercomputer Center** made it possible to train and test algorithmic components.

## Citation

Ankit K. Upadhyay, Ekaterina Nepovinnykh, S. M. Rayeed, Aidan Westphal, Lawrence Miao, Julian Bain, Jaeseok Kang, Tuomas Eerola, Heikki Kälviäinen, Charles V. Stewart. *Animal Re-Identification via Multiview Spatio-Temporal Track Clustering*. Rensselaer Polytechnic Institute, LUT University, Brno University of Technology, CV4Animals, CVPR 2025.