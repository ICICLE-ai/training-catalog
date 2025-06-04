---
tags:
  - Animal-Ecology
---

# How-To Guides


## Step 1: Extract arrival rates from real ADAE Studies

We provide links to the raw data linked below. Alternatively, you have use the cleaned data provided in the [data](/data) directory and skip to Step 2.


### Camera trap dataset from LILA BC
Data: [Orinoquía Camera Traps](https://lila.science/datasets/orinoquia-camera-traps/) \
Code: [extract_camtrap.py](https://github.com/jennamk14/adae_model/blob/master/extract_camtrap.py)

### Drone dataset from KABR 
Data: [KABR Telemetry](https://huggingface.co/datasets/imageomics/KABR-telemetry) \
Code: [extract_kabr.py](https://github.com/jennamk14/adae_model/blob/master/extract_kabr.py)

## Step 2: Model ADAE workloads 
Use [change_points.py](https://github.com/jennamk14/adae_model/blob/master/change_points.py) to extract change points and arrival rates for the time-varying Poisson process.

Visualize and analyze data with the [Jupyter notebook](https://github.com/jennamk14/adae_model/blob/master/PlotADAEWorkloads.ipynb) provided.


## 

![Figure: ADAE Studies in the Field](https://raw.githubusercontent.com/jennamk14/adae_model/master/images/lit%20review%20graphics%20(3).png)
Figure 2: ADAE Studies in the field using networks of camera traps and drones 