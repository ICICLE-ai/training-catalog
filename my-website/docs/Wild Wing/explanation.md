---
tags:
  - Animal-Ecology
  - AI4CI
  - Software
  - Docs
---
# Explanation

## System Architecture and Design Philosophy

![Detailed overview of the WildWing control system, including drone, control software, and GPU laptop. The control software includes an illustration of video frames flowing into the navigation component and outputting commands. The navigation includes computer vision models and autonomous policy. The GPU laptop illustrates the live system system monitoring, including battery level and video stream.](https://raw.githubusercontent.com/jennamk14/wildwing-icicle/main/images/ww.png)

### Core Components

The WildWing system consists of three integrated components designed for autonomous animal behavior monitoring:

**1. Parrot Anafi Drone Platform**
The Parrot Anafi was chosen for its balance of affordability, stability, and video quality. Its lightweight design and excellent stabilization make it ideal for wildlife observation where minimal disturbance is crucial.

**2. Open-Source Control Software**
Built on the SoftwarePilot framework, the control software serves as the bridge between computer vision analysis and drone commands. This design pattern separates concerns, allowing researchers to modify tracking algorithms without touching flight control code.

**3. GPU-Enabled Ground Station**
The laptop serves dual purposes: running computationally intensive YOLO models for real-time animal detection and providing a monitoring interface for researchers to oversee mission progress.

### Autonomous Navigation Philosophy

The navigation system employs a reactive approach rather than pre-programmed flight paths. This design choice enables:
- **Adaptive tracking:** The drone responds to animal movement in real-time
- **Flexible deployment:** No need for extensive pre-mission planning or GPS waypoint programming
- **Robust operation:** The system handles unexpected animal behavior gracefully

### Computer Vision Integration

YOLO (You Only Look Once) models provide the detection backbone because they offer:
- **Real-time processing:** Fast enough for responsive drone control
- **Versatile detection:** Can be trained on multiple species with minimal modification
- **Resource efficiency:** Runs effectively on laptop GPUs

### Why This Architecture Works

This distributed approach (drone + ground processing) was chosen over onboard processing because:
- **Computational power:** Laptop GPUs significantly outperform drone processors
- **Upgradability:** Easy to improve detection models without hardware changes
- **Cost effectiveness:** Leverages existing research computing resources
- **Real-time monitoring:** Researchers maintain situational awareness throughout missions

![Map displaying drone missions with photos of the animals surveyed, including horses, giraffes, and zebras.](https://raw.githubusercontent.com/jennamk14/wildwing-icicle/main/images/maps.png)

The system has been successfully deployed across diverse species and habitats, demonstrating its flexibility and effectiveness for behavioral ecology research. The open-source nature encourages community contributions and adaptations for specific research needs.
