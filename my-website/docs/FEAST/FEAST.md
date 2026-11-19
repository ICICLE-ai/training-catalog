---
tags:
  - Food-Access
  - Smart-Foodsheds
  - Release 2025-08
  - Release 2025-10
  - Release 2025-12
  - Release 2026-11
---
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

# The Food Equity Access Simulation Technology (FEAST)
The Food Equity Access Simulation Technology (FEAST) tool — previously known as the Food Access and Strategy Simulation (FASS) tool — is a powerful platform for analyzing how changes in the food retail landscape, such as adding or removing stores, affect household food access. FEAST enables users to simulate and evaluate strategies aimed at improving food equity across communities.

<div align="center">

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/Food-Access-Model)
[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-yellow.svg)](https://github.com/ICICLE-ai/Food-Access-Model/blob/main/LICENSE)

</div>

:::tip API reference
This component exposes an HTTP API — see its [API documentation](/api/FEAST/food-access-model-api) on this site.
:::




### Built With

* Python
* React.j
## References

- **ICICLE Institute** — [icicle.osu.edu](https://icicle.osu.edu/)
- **FASS-Frontend (companion React UI)** — [github.com/ICICLE-ai/FASS-Frontend](https://github.com/ICICLE-ai/FASS-Frontend)
- **Mesa / mesa-geo** — [projectmesa/mesa](https://github.com/projectmesa/mesa) — agent-based modeling framework.
- **OSMnx** — [gboeing/osmnx](https://github.com/gboeing/osmnx) — OpenStreetMap data retrieval.
- **US Census Bureau API** — [api.census.gov](https://api.census.gov/) — household demographics data source.
- **OpenStreetMap** — [openstreetmap.org](https://www.openstreetmap.org/) — store locations data source.

### Key terms

- **MFAI** — Modified Food Access Index; the per-household access score (0–100) the simulation outputs.
- **Simulation step** — one calendar month advancement of the model.
- **Convenience store (CSPM)** / **supermarket (SPM)** — the two store categories tracked, weighted differently in access scoring.

### Technical Resources
* **Spatial Analysis:** PostGIS for geographic database operations
* **Census Data Integration:** U.S. Census Bureau API documentation
* **Transportation Analysis:** Google Maps Distance Matrix API


### Key Terms and Concepts
* **Agent-based Model (ABM):** Computational model that simulates individual agents(households) and their interactions within a system
* **Food Access Score:** Composite metric measuring geographic accessibility, economic accessibility, and food quality options
* **Census Tract:** Geographic subdivision used by the U.S. Census Bureau, typically containing 1,200-8,000 residents
* **Food Desert:** Geographic area with limited access to affordable and nutritious fresh foods

## Acknowledgements
   
*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*
*Wisconsin Alumni Research Fund
*The Farm2Facts Gift Fund

## Issue Reporting
We welcome feedback and issue reports to help improve FEAST. Please use the following channels:
### GitHub Issues (Primary)
* **Bug Reports:** https://github.com/ICICLE-ai/Food-Access-Model/issues
- Use the "bug" label and bug report template
- Included system information, steps to reproduce, and error messages
* **Feature Requests:**  https://github.com/ICICLE-ai/Food-Access-Model/issues
- Use the "enhancement" label and feature request template
- Describe the proposed functionality and use case

<!--
### Email Support
* **Technical Support:**
* **Research Inquiries:**
* **Collaboration Opportunities:**
-->
### Before Reporting
1. **Check Existing Issues:** Search open and closed issues to avoid duplicates
2. **Review Documentation:** Ensure your question isn't answered in this README or linked resources
3. **Test with Latest Version:** Verify the issue persists in the most recent release
