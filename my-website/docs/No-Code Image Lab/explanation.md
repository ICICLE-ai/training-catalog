---
tags:
  - CI4AI
  - Visual-Analytics
  - Software
title: "No-Code Image Lab: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for No-Code Image Lab. A browser-based OpenCV pipeline builder: build an image pre-processing pipeline in an interactive editor with live preview…"
---
# Explanation

## Available operations

Filters (Gaussian/median/bilateral blur, sharpen), edges (Canny, Sobel,
Laplacian), thresholding (binary, Otsu, adaptive), morphology (erode, dilate,
open, close), colour (grayscale, equalize, CLAHE, invert, channel/HSV adjust,
extract channel), geometry (resize, rotate, flip), and denoise (fast NL-means).
Full definitions live in [packages/core/src/registry.ts](https://github.com/ICICLE-ai/opencv-image-playground/blob/main/packages/core/src/registry.ts)
(TypeScript) and [packages/opencv-executor/opencv_executor/ops.py](https://github.com/ICICLE-ai/opencv-image-playground/blob/main/packages/opencv-executor/opencv_executor/ops.py)
(Python) — the two are kept in sync by op key.
