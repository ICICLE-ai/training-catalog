---
tags:
  - CI4AI
  - Software
  - Release 2026-10
---
# KaiAir

KaiAir is predictable per-packet power control and scheduling implemented in the
[OCUDU](https://github.com/ocudu) 5G stack. KaiAir brings PktR&sup1; and LDP&sup2; into
the OCUDU 5G stack, providing per-packet transmission power control, GRK interference
modeling with K-adaptation, and multi-cell interference coordination built on
receiver-side exclusion regions and ONAMA slot scheduling. A companion patch set for
the OAI nrUE adds the fine-grained measurement and actuation path needed for power
control. The implementation has been verified and measured on real radios, USRP X310
and B210 deployments on the ARA wireless living lab.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/kaiair)
[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-yellow.svg)](https://github.com/ICICLE-ai/kaiair/blob/main/LICENSE)

</div>



## References

- &sup1;Zhibo Meng, Hongwei Zhang, Joint Scheduling and Power Control for Predictable Per-Packet Reliability in URLLC, IEEE International Conference on Network Protocols (ICNP), 2024
- &sup2;Zhibo Meng, Hongwei Zhang, Multi-Cell, Multi-Channel URLLC with Probabilistic Per-Packet Real-Time Guarantee, Technical Report ISU-DNC-TR-2020-01, Iowa State University, 2020
- [OCUDU](https://github.com/ocudu), the 5G O-DU/CU stack the gNB patch series applies to.
- [OpenAirInterface 5G RAN](https://gitlab.eurecom.fr/oai/openairinterface5g), the nrUE
  the UE patch series applies to.
- [ARA Wireless Living Lab](https://arawireless.org), the testbed the implementation was
  validated on.

## Acknowledgements

This work has been funded by grants from the National Science Foundation award 2130889
(ARA Wireless Living Lab) and NIFA award 2021-67021-33775.

*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

## Issue reporting

Report issues on the GitHub issue tracker at
https://github.com/ICICLE-ai/kaiair/issues.
