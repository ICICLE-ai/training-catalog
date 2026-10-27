---
tags:
  - Software
title: "Cascade Configuration Service: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for Cascade Configuration Service. A Streamlit-based demo for the Cascade Configuration Service."
---
# How-To Guides

## Using the Service

The user provides two constraints:

- **Maximum Cost Budget (C)**
- **Maximum Error Budget (E)**

### Cost Budget

The cost budget specifies the maximum allowed execution cost for a cascade configuration. Cost is calculated from model service time, with different weights for edge and cloud execution. Edge model cost is weighted as 25% of its service time, while cloud model cost is weighted as 50% of its service time.

The cost does not represent a dollar amount. Network and queueing delays are not included in the cost calculation.

### Error Budget

The error budget specifies the maximum acceptable classification error. For example, an error budget of `0.10` allows configurations with an expected classification error of up to 10%.

A configuration is considered feasible when:

```text
cost <= user cost budget
error <= user error budget
```

Among the feasible configurations, the service selects the configuration with the lowest estimated latency.

The current service evaluates candidate cascade configurations using a predefined offline policy table containing measured or pre-computed configuration characteristics, including cost, classification error, and estimated latency.

The service returns:

- Execution policy
- Edge model(s)
- Cloud model
- Confidence threshold
- Estimated latency
- Expected error
- Dynamic execution-policy workflow

If no configuration satisfies the specified constraints, the user can adjust the cost or error budget and run the selection again.

## Policy Table

The service uses a predefined policy table located at:

```text
data/policy_table.csv
```

The policy table contains the candidate configurations used by the service.

The CSV contains fields such as:

```text
policy
edge_model
cloud_model
threshold
cost
error
estimated_latency_ms
```

The included CSV provides the configuration data required by the current demonstration.

## Check Service Health

When the service is running on port `8000`, the Streamlit health endpoint can be checked using:

```bash
curl http://localhost:8000/_stcore/health
```

A healthy service returns:

```text
ok
```
