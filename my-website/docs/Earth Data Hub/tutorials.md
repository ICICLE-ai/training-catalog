---
tags:
  - CI4AI
  - Visual-Analytics
  - Software
---
# Tutorials

## Open Earth Data Hub

Open the Earth Data Hub interface.

![Earth Data Hub interface](https://raw.githubusercontent.com/ICICLE-ai/geoharmonizer-ui/main/docs/images/earth-data-hub.png)

The main interface provides access to the interactive map, boundary upload, Job Setup, and Jobs monitoring.

## Upload and Select an Area of Interest

Click **Upload Boundary** and upload a supported geospatial boundary file.

![Uploaded Area of Interest](https://raw.githubusercontent.com/ICICLE-ai/geoharmonizer-ui/main/docs/images/aoi-selection.png)

After the boundary is loaded:

1. The uploaded boundary appears on the map.
2. Select the field or polygon you want to use.
3. The selected area becomes the Area of Interest (AOI).

Earth Data Hub supports two AOI options:

- **Bounding box** — uses the geographic extent of the selected area.
- **Exact geometry** — uses the complete selected geometry.

The selected AOI is used for satellite availability checking and collection job submission.

## Configure Satellite Collection

Open **Job Setup** after selecting an AOI.

Configure the collection settings based on the satellite imagery you want to retrieve.

## Check Satellite Availability

Click **Check Availability** after configuring the collection.

![Satellite availability results](https://raw.githubusercontent.com/ICICLE-ai/geoharmonizer-ui/main/docs/images/availability.png)

Earth Data Hub displays the number of usable satellite scenes and their acquisition dates.

Review the availability results before submitting the collection job.

## Configure the Tapis Job

A valid Tapis session is required for job submission.

If an active Tapis session is available, Earth Data Hub recognizes it and loads the available execution systems and queues.

Configure the execution settings and review the generated GeoHarmonizer job arguments before submitting.

![Tapis collection job configuration](https://raw.githubusercontent.com/ICICLE-ai/geoharmonizer-ui/main/docs/images/job-submission.png)

## Submit the Collection Job

Click **Submit Collection Job**.

After Tapis accepts the request, Earth Data Hub displays a submission confirmation and Job ID.

The submitted job can then be monitored from the **Jobs** page.

## Monitor the Job

Open the **Jobs** page to view submitted GeoHarmonizer collection jobs.

![Tapis job monitoring](https://raw.githubusercontent.com/ICICLE-ai/geoharmonizer-ui/main/docs/images/jobs.png)

The Jobs page shows the current status of submitted jobs. Use the available filters and **Refresh** to retrieve the latest information.
