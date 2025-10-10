---
tags:
  - Food-Access
  - Smart-Foodsheds
  - Video
---
# Tutorials
<!-- [Click here](https://youtu.be/kltZCvLqHp0) for the video tutorial. -->


:::tip Video Tutorial
**FEAST Video tutorial**
<iframe 
  width="560" 
  height="315" 
  src="https://www.youtube.com/embed/kltZCvLqHp0" 
  title="FEAST Video tutorial"
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
  allowfullscreen>
</iframe>

:::

## Example Use Case

1. Add a Store: Place a new supermarket in an underserved area—for example, add
    "Charlie’s Market" to a park location.
2. Simulate: Step through multiple months to observe how the addition improves food
    access, particularly for households without vehicles.
3. Remove a Store: Remove "Charlie’s Market" and/or surrounding stores and examine
    how food access challenges re-emerge in the affected area.


# Explanation

## Introduction

The FEAST tool is a powerful resource for analyzing and
simulating the effects of adding or removing stores on household food access. This guide
provides clear, step-by-step instructions to help you navigate and utilize the tool effectively.

### Why Agent-Based Modeling for Food Access?
Traditional food access research relies on aggregate statistics and simple distance measurements. However, real household food shopping involve interactions between:
- **Individual Constraints:** Income, vehicle access, work schedules, family size
- **Geographic Factors:** Store locations, transportation networks, neighborhood characteristics
- **Economic Dynamics:** Price variations and store quality differences

## Key Features of the Interface

1. Map Overview
    -  Legend:
        -  Supermarkets: Represented by hexagons.
        - Convenience Stores: Represented by small triangles.
        - Households: Shaped like houses.
            - High Food Access: Green.
            - Medium Food Access: Orange/Yellow.
            - Low Food Access: Red.
    - The map is interactive, allowing you to navigate, zoom, and click on specific elements to
explore detailed information about stores and households.

2. Household Data

- Attributes available for each household include:
    - Income
        - Household size
        - Number of vehicles
        - Number of workers
        - Proximity to the nearest store (within a mile)
        - Transit time (public and private)
        - Food access score
    - Data is sourced from the Census Bureau and Google Maps, ensuring accuracy and
relevance. The data reflects real-world locations as closely as possible, with granularity
at the census tract level.

3. Community Data Bar

- Aggregated metrics displayed for the selected area:
    - Total number of households
    - Number of supermarkets and convenience stores
    - Average household income
    - Average number of household vehicles
