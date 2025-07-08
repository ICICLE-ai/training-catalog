---
tags:
  - Food-Access
  - Smart-Foodsheds
  - Release 2025-07
---

# FAF-API-ICICLE

## API access to the US Bureau of Transportation Statistics' Freight Analysis Framework dataset

This is a hosted REST API to the US Bureau of Transportation Statistics (BTS) Feight Analysis Framework (FAF) dataset. It has been developed by the Data To Insight Center (D2I) at Indiana University as part of the [NSF ICICLE AI Institute](https://icicle.osu.edu/) and in collaboration with the US Bureau of Transportation Statistics.  The API provides access to the dataset hosted in a remote MySQL server (called the FAF database as implemented in the `Data_Lookup.py` file located in the `src` folder at the root of the server). 

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/Data-to-Insight-Center/faf-api-ICICLE)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

The design of the FAF database API had the following objectives:

-   Prevent users from directly accessing the database, thereby safeguarding it against unauthorized modifications or manipulations.
-   Facilitate future updates by allowing modifications to the lookup tables when new data is added, rather than altering the physical queries. This approach will support automation in future development efforts.

The API accesses the following version of the FAF dataset:

Most recent: December 18, 2023.


## License
FAF API Server is developed by Indiana University and distributed under the BSD 3-Clause License.
## Acknowledgements
Thanks to colleagues at Texas Advanced Computing Center (TACC) who are hosting the FAF API as part of the NSF AI ICICLE Institute (OAC 2112606). Thanks to the US Bureau of Transportation Statistics Freight Analysis Framework for guidance.

## References
Freight Analysis Framework, Bureau of Transportation Statistics https://www.bts.gov/faf