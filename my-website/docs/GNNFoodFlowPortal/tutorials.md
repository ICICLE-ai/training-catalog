---
tags:
  - Smart-Foodsheds
  - AI4CI
---
# Tutorials

## Explore Parallel Model Food Flows

Use this tutorial to inspect precomputed county-to-county food-flow predictions.

1. Open the [live portal](https://gnnfoodflowportal.pods.icicleai.tapis.io/) or run the portal locally.
2. Start the app and move from the welcome story into the main portal.
3. Select **Parallel Model Map**.
4. In the sidebar, choose a food category from SCTG 1-7.
5. Select an origin county, a destination county, or choose **All** for broader patterns.
6. Adjust the number of top links and the flow-width scaling mode.
7. Hover over map arcs to inspect origin, destination, FIPS codes, and predicted kilotons shipped.
8. Open **Parallel Model Download** to export filtered rows or origin-destination summary statistics as CSV.

## Run a Multi-Task What-If Scenario

Use this tutorial to compare baseline food-flow estimates with scenario-adjusted estimates from the vendored multi-task GNN demo assets.

1. Open the main portal.
2. Select **Multi-task One-to-One** to compare one origin county with one destination county, or select **Multi-task One-to-Many** to compare one focus county with many partners.
3. Choose the county or counties for the scenario.
4. Adjust regional feature values in the scenario form.
5. Click **Run One-to-One** or **Run One-to-Many**.
6. Review the baseline, modified, and delta results.
7. Download the scenario CSV for downstream analysis.
