---
tags:
  - Software
  - AI4CI
title: "HPC-MCP: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for HPC-MCP. HPC-MCP is a service-based ICICLE software component that gives HPC users a natural-language interface to backend HPC utilities."
---
# Explanation

## What HPC-MCP Provides

HPC-MCP packages an LLM-assisted HPC utility workflow as an accessible service. Instead of requiring users to run the estimator manually inside an HPC software environment, the service exposes a small HTTP and MCP interface that can be used from command-line tools, web-facing workflows, or MCP-compatible agents.

The current release focuses on distributed training-time prediction for configurable model training workloads on Vista and Perlmutter. Future releases can add additional HPC tools, including command generation and user-guide question answering.

## How Prediction Requests Work

Direct prediction requests sent to `/predict-gpu-time` call the backend estimator with the selected system configuration. Natural-language requests sent to `/chat` first pass through the configured LLM backend for request understanding and tool routing. When the user asks for a supported training-time prediction, the service routes the request to the estimator and returns a summarized result.

The backend estimator is the Distributed Training Estimator of LLMs:

```text
https://github.com/ICICLE-ai/distributed_training_estimator_of_LLM
```

## Catalog and Release Notes

The component metadata file for catalog review is:

```text
component.yaml
```

The ICICLE software team should review the README, OpenAPI specification, and component metadata before catalog publication. Service name, ICICLEaaS category, and Tapis UI placement should be finalized through the ICICLE SDD/release process.
