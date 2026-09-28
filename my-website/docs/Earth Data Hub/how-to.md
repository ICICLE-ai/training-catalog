---
tags:
  - CI4AI
  - Visual-Analytics
  - Software
title: "Earth Data Hub: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for Earth Data Hub. A browser-based geospatial data discovery and collection interface for selecting an area of interest, checking satellite…"
---
# How-To Guides

## Run Earth Data Hub Locally

Install the frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Build the production frontend:

```bash
npm run build
```

## Run with Docker

Build the Earth Data Hub frontend image:

```bash
docker build -t earth-data-hub-ui:latest .
```

Run the container:

```bash
docker run --rm -p 8080:80 earth-data-hub-ui:latest
```
