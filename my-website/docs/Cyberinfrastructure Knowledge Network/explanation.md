---
tags:
  - CI4AI
  - Software
  - PADI
---

# Explanation

CKN facilitates seamless connectivity between edge devices and the cloud through event streaming, enabling real‑time data capture and processing. By leveraging event‑stream processing, it captures, aggregates, and stores historical system‑performance data in a knowledge graph that models application behaviour and guides model selection and deployment at the edge.

CKN comprises several core components:

* **CKN Daemon** – A lightweight service that resides on each edge server. It manages communication with edge devices, handles requests, captures performance data, and deploys AI models as needed. The daemon connects with the cloud‑based CKN system via a pub/sub system, capturing real‑time events from edge devices (model usage, resource consumption, prediction accuracy, latency, and more).
* **Event Streaming & Processing** – Stream‑processing techniques (for example, tumbling windows) aggregate events and generate real‑time alerts from edge‑device streams.
* **Knowledge Graph** – A Neo4j graph database that stores historical and provenance information about applications, models, and edge events. This comprehensive view of the system enables CKN to track model usage and analyse performance over time.

The primary objective of CKN is to provide a robust framework for optimising AI‑application deployment and resource allocation at the edge. Leveraging real‑time event streaming and knowledge graphs, CKN efficiently handles AI workloads, adapts to changing requirements, and supports scalable edge–cloud collaboration.

Refer to the CKN paper for more information: [https://ieeexplore.ieee.org/document/10254827](https://ieeexplore.ieee.org/document/10254827).

![CKN Design](https://raw.githubusercontent.com/Data-to-Insight-Center/cyberinfrastructure-knowledge-network/main/docs/ckn-design.png)

