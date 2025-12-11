---
tags:
  - Software
  - CI4AI
  - Animal Ecology
---
# Explanation

## Software COMPonents

The ML Field Planner is a framework consisting of the following software components:

- [`TapisBase`](https://github.com/tapis-project): Base ICICLE Tapis Software
- [`ctcontroller`](https://github.com/ICICLE-ai/ct-controller): Hardware and Software Provisioner
- [`EventEngine`](https://github.com/tapis-project/event-engine): Event Engine
- [`CameraTrapsEdgeSoftware`](https://github.com/tapis-project/camera-traps): Camera Traps Edge Software
- [`PatraKG`](https://github.com/Data-to-Insight-Center/patra-kg): Patra Model Card Knowledge Graph
- [`PatraToolkit`](https://github.com/Data-to-Insight-Center/patra-toolkit): Patra Model Card Toolkit.
- [`CKN`](https://github.com/Data-to-Insight-Center/cyberinfrastructure-knowledge-network): Cyberinfrastructure Knowledge Network
- [`FederatedAuthService`](https://github.com/tapis-project/authenticator): Tapis Federated Authentication Service
- [`TapisUI`](https://github.com/tapis-project/tapis-ui): Tapis User Interface
- [`icicleai-tapisui-extension`](https://github.com/ICICLE-ai/tapisui-extension-icicle): ICICLEAI TapisUI Extension
- [`CameraTrapsEdgeSimDashboard`](https://github.com/ICICLE-ai/tapisui-extension-icicle/tree/main/src/pages/MLEdge): Camera Traps Edge Simulator Dashboard

## Architectural Overview

![ML Field Planner Architecture Diagram](https://github.com/ICICLE-ai/mlfieldplanner/raw/main/imgs/ml_field_planner_arch.png)

The ML Field Planner provides an authenticated framework to submit ML pipelines to edge and cloud devices and analyze the results to make decisions on edge-to-center tradeoffs and text new algorithms.

The planner is powered by the Tapis framework [TapisBase], which provides an authenticated environment [FederatedAuthService], including the Camera Traps Edge Simulator Dashboard, a graphical user interface [TapisUI, icicleai-tapisui-extension, CameraTrapsEdgeSimDashboard] to submit jobs, as well as a dashboard to view job metrics (CKN).

Once the user selects the hardware, model, and dataset and submits the analysis run from the Camera Traps Edge Simulator Dashboard, a Tapis job is generated. This launches the hardware and software provisioner [CTController] on a backend node, which handles the provisioning of the hardware, setup and running of the ML pipeline, and shutting down the hardware.

The ML pipeline is launched from the dashboard is built using the Event Engine [EventEngine], which allows plugins to communicate with each other over `zmq` sockets. [CameraTrapsEdgeSoftware] is a set of plugins deployed a docker container that communicate across the Event Engine. When provided with a set of images or a prerecorded video, it can be run in simulation mode on the provisioned hardware to simulate a real ML-enabled camera trap.

As part of the setup that ctcontroller does to prepare the provisioned hardware for the pipeline, it sends a request to the [PatraKG] using the model id specified by the user, parsing the model card to obtain download model to the local device. New model cards can can created and added to the the Patra model card toolkit [PatraToolkit].

As the ML pipeline runs, a CKN daemeon streams metric data from the local to device to a CKN broker running on a backend node [CKN], including model and system performance, viewable from a dashboard in the graphical user interface [TapisUI, icicleai-tapisui-extension].
