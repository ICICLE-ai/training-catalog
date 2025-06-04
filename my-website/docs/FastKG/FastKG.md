---
tags:
  - CI4AI
  - Release 2024-12
---


# FastKG

FastKG is a knowledge graph embedding training library. Knowledge Graph (KG) embeddings are a way to represent entities and relationships from a KG in a continuous vector space, enabling tasks like link prediction and reasoning. TransE, a popular model, represents relationships as translations in the embedding space, such that for a valid triplet (head, relation, tail), the embedding of the head plus the relation vector is close to the embedding of the tail. Training data for TransE is typically stored in a tab-separated values (TSV) format, where each line represents a triplet, e.g., `entity1\trelation1\tentity2`. For example a dummy train.tsv should look like this:


<pre>
    Paris   isCapitalOf     France

    Einstein    discovered    Relativity
</pre>


After training, the learned embeddings can be used to infer new triplets by calculating scores for candidate triplets. For instance, given embeddings for Paris, isCapitalOf, and Germany, we can calculate a score to determine if Paris isCapitalOf Germany is likely true.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?logo=github&style=flat-square)](https://github.com/ICICLE-ai/fastkg-icicle)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



# Acknowledgements

*This work has been funded by grants from the National Science Foundation, including the ICICLE AI Institute (OAC 2112606)*
