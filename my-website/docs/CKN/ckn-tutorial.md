<div align="center">
  
# Cyberinfrastructure Knowledge Network

[![Documentation Status](https://img.shields.io/badge/docs-latest-blue.svg)](https://cyberinfrastructure-knowledge-network.readthedocs.io/en/latest/)
[![Build Status](https://github.com/Data-to-Insight-Center/cyberinfrastructure-knowledge-network/actions/workflows/ci.yml/badge.svg)](https://github.com/Data-to-Insight-Center/cyberinfrastructure-knowledge-network/actions)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>

The Cyberinfrastructure Knowledge Network (CKN) is an extensible and portable distributed framework designed to optimize AI at the edge, particularly in dynamic environments where workloads on the edge server may change suddenly, such as in response to motion detection. CKN enhances edge-cloud collaboration by using historical data, graph representations, and adaptable deployment of AI models to meet changing demands in accuracy and latency at edge devices.

CKN facilitates seamless connectivity between edge devices and the cloud through event streaming, enabling real-time data capture and processing. By leveraging event stream processing, CKN captures, aggregates, and stores historical data about system performance. This data is stored in a knowledge graph and used to model application behavior and optimize model selection and deployment at the edge.

The CKN framework includes several core components:

- **CKN Daemon:** A lightweight service that resides on each edge server, responsible for managing communications with edge devices, handling requests, capturing performance data, and deploying AI models as needed. The daemon connects with the cloud-based CKN system via a pub/sub system. This module captures real-time events from edge devices, augmenting them with details such as model usage, resource consumption, prediction accuracy, and latency. 

- **Event Streaming and Processing:** It uses stream processing techniques, like tumbling windows, to aggregate events and generate real-time alerts based on the streaming data from the edge.

- **Knowledge Graph:** A Neo4j Graph database that stores historical data and provenance information about the system, including applications, available models, and events from edge devices. This knowledge graph enables CKN to maintain a comprehensive view of system evolution, track model usage, and analyze performance over time.

The primary objective of CKN is to provide a robust framework that optimizes AI application deployment and resource allocation at the edge. By leveraging real-time event streaming and knowledge graphs, CKN creates a system capable of efficiently handling AI workloads, adapting to changing requirements, and supporting scalable edge-cloud collaboration.

Refer the [CKN paper](https://ieeexplore.ieee.org/document/10254827) for more information.


---

## Getting Started

Refer the [documentation](https://cyberinfrastructure-knowledge-network.readthedocs.io/en/latest/) for a detailed guide on creating a custom plugin and streaming events to the knowledge graph.

### Prerequisites

- Ensure **Docker** and **Docker Compose** are installed.
- Ensure the following ports are available: `7474`, `7687`, `2181`, `9092`, `8083`, `8502`.

### Quickstart

- **Clone the Repository and Start Services**
   ```bash
   git clone https://github.com/Data-to-Insight-Center/cyberinfrastructure-knowledge-network.git
   ```
   ```bash
   make up
   ```
   
   Once setup is complete, verify that all modules are running with `docker compose ps`

- **Stream an example [camera-trap event](examples/event.json)**
    ```bash
   docker compose -f examples/docker-compose.yml up -d --build
   ```
   
   You can view the streamed data on the [CKN dashboard](http://localhost:8502/Camera_Traps).
   
   Access the [Neo4j Browser](http://localhost:7474/browser/) using `neo4j`and `PWD_HERE` as the username and password. 
   Run ```MATCH (n) RETURN n``` to view the streamed data in the knowledge graph.

  Shut down the services using ```make down``` and ```docker compose -f examples/docker-compose.yml down```

---

## License
The Cyberinfrastructure Knowledge Network is copyrighted by the Indiana University Board of Trustees and is distributed under the BSD 3-Clause License. See `LICENSE.txt` for more information.

## Acknowledgements
This research is funded in part through the National Science Foundation under award #2112606, AI Institute for Intelligent CyberInfrastructure with Computational Learning in the Environment (ICICLE), and in part through Data to Insight Center (D2I) at Indiana University.

## Reference
S. Withana and B. Plale, "CKN: An Edge AI Distributed Framework," *2023 IEEE 19th International Conference on e-Science (e-Science)*, Limassol, Cyprus, 2023, pp. 1-10, doi: 10.1109/e-Science58273.2023.10254827.
