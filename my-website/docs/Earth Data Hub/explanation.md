---
tags:
  - CI4AI
  - Visual-Analytics
  - Software
---
# Explanation

## Area of Interest

The Area of Interest (AOI) defines the geographic region used for satellite data discovery and collection.

Earth Data Hub allows users to upload geospatial boundaries and select a field or polygon from the interactive map.

The selected AOI can be represented as either a bounding box or exact geometry.

## Satellite Availability

Before submitting a collection job, Earth Data Hub can check whether satellite imagery is available for the selected AOI and collection settings.

```text
Earth Data Hub
      │
      ▼
GeoHarmonizer Availability Service
      │
      ▼
Earth Search STAC
```

The available scenes are returned to Earth Data Hub and displayed to the user before job submission.

## Tapis Collection Workflow

Earth Data Hub converts the selected AOI and collection configuration into a GeoHarmonizer collection job and submits it through Tapis.

```text
Earth Data Hub
      │
      ▼
Tapis Jobs API
      │
      ▼
HPC Execution System
      │
      ▼
geoharmonizer-collect
```

After submission, the job can be monitored from the **Jobs** page until the collection workflow completes.
