---
sidebar_position: 1
---

# Patra Knowledge Base

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

The Patra Knowledge Base is a system designed to manage and track AI/ML models, with the objective of making them more accountable and trustworthy. It's a key part of the Patra ModelCards framework, which aims to improve transparency and accountability in AI/ML models throughout their entire lifecycle. This includes the model's initial training phase, subsequent deployments, and ongoing usage, whether by the same or different individuals.

At the heart of the Patra Knowledge Base is the concept of Model Cards. These cards are essentially detailed records that provide essential information about each AI/ML model. This information includes technical details like the model's accuracy and latency, but it goes beyond that to include non-technical aspects such as fairness, explainability, and the model's behavior in various deployment environments. This holistic approach is intended to create a comprehensive understanding of the model's strengths and weaknesses, enabling more informed decisions about its use and deployment

Key features and capabilities of the Patra ModelCards Framework include:

- **Semi-automated information capture:** Patra reduces the burden of manual documentation by automatically capturing information about model fairness, explainability, and performance in different deployment environments. This automation is facilitated by the [Model Card Toolkit](https://github.com/Data-to-Insight-Center/patra-toolkit)  , which invokes analysis tools and integrates the results directly into the Model Cards.
  
- **Graph-based knowledge representation:** Patra uses a graph database (Neo4j) to represent Model Cards and their relationships. This graph-based approach allows for efficient querying and inference, making it possible to track model evolution, identify similar models, and answer complex questions about model deployment and performance.
  
- **Provenance tracking:** Patra leverages the concepts of **forward and backward provenance** to comprehensively track the relationships between models, datasets, and deployment instances. This makes it possible to understand the lineage of models, trace their origins, and analyze their usage patterns.
  
- **Real-time deployment information:** Patra integrates with the [CKN Edge AI Framework](https://github.com/Data-to-Insight-Center/cyberinfrastructure-knowledge-network)  to capture real-time information about model execution in edge environments. This includes data on performance, resource usage, and other relevant metrics, which can be used to optimize deployments and gain insights into model behavior in real-world settings.
  
- **Machine-actionable API:** Patra provides a **machine-actionable API** that allows intelligent systems in the edge-cloud continuum to query the knowledge base and make informed decisions about model selection. This enables automated model selection based on various criteria, including fairness, explainability, and performance metrics, further enhancing accountability and transparency.
  
- **Versioning and Similarity Analysis:** Patra infers relationships between model cards such as **"alternateOf," "revisionOf," and "transformativeUseOf"** by leveraging embedding vectors and cosine similarity comparisons. This capability is essential for tracking model evolution, identifying different versions, and understanding how models are adapted and reused over time.

By combining these capabilities, the Patra Knowledge Base provides a robust foundation for **trustworthy and accountable AI/ML model management within the edge-cloud continuum**. This framework addresses crucial aspects of transparency, provenance tracking, and performance monitoring, ultimately contributing to more responsible and reliable AI deployments.

For more information, please refer to the [Patra ModelCards paper](https://ieeexplore.ieee.org/document/10678710).

## Patra Knowledge Base Server
The server is built using Flask and exposes a RESTful API for interaction with the Patra Knowledge Graph (KG).


| Endpoint                 | Method | Description                                                   |
|--------------------------|--------|---------------------------------------------------------------|
| `/upload_mc`             | POST   | Upload a model card to the Patra Knowledge Graph.             |
| `/update_mc`             | POST   | Update an existing model card.                                |
| `/upload_ds`             | POST   | Upload a datasheet to the Patra Knowledge Graph.              |
| `/search`                | GET    | Full-text search for model cards.                             |
| `/download_mc`           | GET    | Download a reconstructed model card from the Patra Knowledge Graph. |
| `/download_url`          | GET    | Retrieve the download URL for a given model ID.              |
| `/list`                  | GET    | List all models in the Patra Knowledge Graph.                 |
| `/model_deployments`     | GET    | Get all deployments for a given model ID.                     |
| `/update_model_location` | POST   | Update the model’s location in the graph.                     |
| `/get_hash_id`           | GET    | Return a unique hash ID for the provided combined string.     |

---

## Getting Started

### Prerequisites

Before starting, make sure the following are in place:

- **Docker** and **Docker Compose** are installed and running on your machine.
- Ensure that the following ports are available: `7474` (Neo4j Web UI), `7687` (Neo4j Bolt), `5002` (REST Server).
- An **OpenAI API Key** is required. Refer to the [OpenAI documentation](https://platform.openai.com) for instructions.

---

## Quickstart

### Set up Environment Variables
- Set your OpenAI API key using the following command:
    ```bash
    export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
    ```

### Launch the Patra Knowledge Base
- Start the Patra Knowledge Base using Docker Compose:
    ```bash
    make up
    ```
  
   The server will be running at port `5002`. To view Swagger documentation, navigate to `http://localhost:5002/swagger`.

   Once the containers are up, you can view the ingested model cards in the [Neo4j Browser](http://localhost:7474/browser/).
   - Login with the username `neo4j` and the password `PWD_HERE`.
   - Run the following query to view the model data:
     ```cypher
     MATCH (n) RETURN n
     ```
   

- To stop and remove all running containers, use:
    ```bash
    make down
    ```

---

## License

The **Patra Knowledge Base** is copyrighted by the **Indiana University Board of Trustees** and distributed under the **BSD 3-Clause License**. See the `LICENSE.txt` file for more details.


## Acknowledgements

This research is funded in part through the National Science Foundation under award #2112606, AI Institute for Intelligent CyberInfrastructure with Computational Learning in the Environment (ICICLE), and in part through Data to Insight Center (D2I) at Indiana University.


## Reference

S. Withana and B. Plale, "Patra ModelCards: AI/ML Accountability in the Edge-Cloud Continuum," *2024 IEEE 20th International Conference on e-Science (e-Science)*, Osaka, Japan, 2024, pp. 1-10, doi: 10.1109/e-Science62913.2024.10678710.