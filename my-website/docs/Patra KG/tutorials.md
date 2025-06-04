---
tags:
  - CI4AI
  - Software
  - PADI
---

# Tutorial

### Set up Environment Variables

#### **Model Similarity (Optional)**  
To enable automatic model similarity detection using OpenAI embeddings, set `ENABLE_MC_SIMILARITY` to `True` and provide your OpenAI API key:

```bash
export ENABLE_MC_SIMILARITY=True
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

#### **Hugging Face Integration (Optional)**  
To upload models and artifacts (e.g., model weights, cards) to the Hugging Face Hub:
```bash
export HF_HUB_USERNAME=<your-hf-username>
export HF_HUB_TOKEN=<your-hf-access-token>
```
Requires write access to the target Hugging Face repo.

#### **GitHub Integration (Optional)**  
To push models and artifacts (e.g., versioned cards, metadata) to a GitHub repository:
```bash
export GH_HUB_USERNAME=<your-github-username>
export GH_HUB_TOKEN=<your-github-personal-access-token>
```
Requires `repo` scope enabled on the GitHub token.

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
