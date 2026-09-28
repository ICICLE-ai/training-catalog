---
tags:
  - Foundation-AI
title: "ICICLE-Playgrounds: How To Guides"
sidebar_label: "How To Guides"
pagination_label: "How To Guides"
description: "How To Guides for ICICLE-Playgrounds. ICICLE Playgrounds is a Python SDK designed for working with AI plug-n-play frameworks powered by Tapis Workflows."
---

# How To Guides

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Make sure you have Python 3.12+ installed.

```bash
# Install using uv
uv add icicle-playgrounds

# Or install from source
git clone <repository-url>
cd icicle-playgrounds
uv sync
```

## Quick Start

```python
from icicle_playgrounds.pydantic.plug_n_play import Image, Tensor, DetectionResults
from icicle_playgrounds.pydantic.patra_model_cards import PatraModelCard

# Work with images and tensors
image = Image(...)
tensor = Tensor(...)

# Handle detection results
results = DetectionResults(...)

# Create model cards
model_card = PatraModelCard(...)
```
