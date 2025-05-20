---
tags:
  - Foundational-AI
---

# Explanation

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


| Endpoint                        | Method | Description                                                                                                            |
|---------------------------------|--------|------------------------------------------------------------------------------------------------------------------------|
| `/upload_mc`                    | POST   | Upload a model card to the Patra Knowledge Graph.                                                                      |
| `/update_mc`                    | POST   | Update an existing model card.                                                                                         |
| `/upload_ds`                    | POST   | Upload a datasheet to the Patra Knowledge Graph.                                                                       |
| `/search`                       | GET    | Full-text search for model cards.                                                                                      |
| `/download_mc`                  | GET    | Download a reconstructed model card from the Patra Knowledge Graph.                                                    |
| `/download_mc`                  | HEAD   | Retrieve the model card linkset through the header for the given model ID                                              |
| `/download_url`                 | GET    | Retrieve the download URL for a given model ID.                                                                        |
| `/list`                         | GET    | List all models in the Patra Knowledge Graph.                                                                          |
| `/model_deployments`            | GET    | Get all deployments for a given model ID.                                                                              |
| `/update_model_location`        | POST   | Update the model’s location in the graph.                                                                              |
| `/get_model_id`                 | GET    | Generates a model_id for a given author, name, and version.                                                            |
| `/get_huggingface_credentials`  | GET    | Get Hugging Face credentials for a given model ID.                                                                     |
| `/get_model_card_by_name`       | GET    | Get a model card by name.                                                                                              |
| `/modelcard_linkset` | GET | Returns the modelcard linkset in the header for a given modelcard id<br/>ex: &lt;server_url&gt;/modelcard_linkset?id=&lt;mc_id&gt; |

For more information on the server endpoints, please refer to the [API documentation.](https://github.com/Data-to-Insight-Center/patra-kg/blob/main/patra_openapi.json)
