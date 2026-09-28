---
tags:
  - Food-Access
  - Smart-Foodsheds
title: "FafFrontend: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for FafFrontend. This is intended as a helpful front end to a REST API to the US Bureau of Transportation Statistics (BTS) Feight Analysis…"
---

# Explanation

The Angular UI is structured around two primary sections: **Domestic Flow** and **Foreign Flow**, both accessible from the left-hand navigation menu. Each section is designed to support efficient exploration and analysis of freight data.

###  Domestic Flow

The **Domestic Flow** section contains two tabs:

#### 1. Domestic Import & Export
This tab allows for the generation of CSV files based on selected freight parameters. The following six fields must be specified via dropdown menus:

- Foreign Destination Mode  
- Commodity  
- Start Year  
- End Year  
- Origin  
- Destination  

Once these fields are selected, a CSV file can be generated containing the filtered data.

#### 2. State & Year Analysis
This tab presents state-level import and export data in the form of pie charts for a selected year, enabling quick visual analysis of freight distribution across states.


###  Foreign Flow

The **Foreign Flow** section includes two tabs:

#### 1. Foreign Import  
#### 2. Foreign Export  

These tabs mirror the functionality of the Domestic Import & Export section. Required values can be selected from the dropdown menus, and data can be exported in CSV format based on the selected criteria.
