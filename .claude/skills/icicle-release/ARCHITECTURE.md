# ICICLE Release — System Architecture

Multi-agent, agentic release system with human checks in the loop. It publishes (or
updates) a batch of ICICLE components into **two repos** — the `training-catalog`
Docusaurus site and the external `CI-Components-Catalog` — then lets CI sync the
component graph into Neo4j. The agent never handles secrets.

## Design principle

Per-component work is parallel **only where it writes to disjoint paths**
(`docs/<C>/`, `api-docs/<C>/`). Everything converges on **shared files**
(`docusaurus.config.js`, `other_resources/0_intro.md`, `release_catalog.yml`), a
**single global build**, and **gated pushes** — so the shape is **fan-out (MAP) →
gather (REDUCE) → human-gated push**, not N independent pipelines.

```mermaid
flowchart TB
    CSV["📄 Release CSV<br/>(README, OpenAPI, Resource Link,<br/>Component Catalog YAML File)"]

    subgraph MAP["🟢 MAP — up to 5 agents in parallel (one per component)"]
        direction LR
        A1["Agent · Component A<br/>readme-validate → deploy-doc<br/>→ deploy-api → resource-prep<br/>→ component-info-prep"]
        A2["Agent · Component B<br/>…"]
        A3["Agent · Component C<br/>…"]
        note1["writes ONLY disjoint<br/>docs/&lt;C&gt;/ , api-docs/&lt;C&gt;/<br/>emits a bundle of shared-file edits"]
    end

    subgraph REDUCE["🔵 REDUCE — single writer, sequential"]
        direction TB
        R1["Apply shared-file edits one at a time<br/>docusaurus.config.js · 0_intro.md · release_catalog.yml"]
        R2["ONE global npm run build<br/>(fix MDX until clean)"]
        R3["catalog_parser append<br/>(--release, --training-url)"]
        R4{"catalog_parser VALIDATE<br/>every related_to resolves?"}
        R1 --> R2 --> R3 --> R4
    end

    subgraph GATES["🟡 HUMAN CHECKS IN THE LOOP"]
        direction TB
        H1{{"H1 · review site diff<br/>+ clean build"}}
        H2{{"H2 · review release_catalog.yml diff<br/>+ validate = 0"}}
    end

    subgraph SITE["📘 training-catalog repo"]
        S1["push docusaurus-demo<br/>→ GitHub Pages deploy"]
    end
    subgraph CAT["📗 CI-Components-Catalog repo"]
        C1["push dev"]
    end

    subgraph CI["⚙️ CI (no agent, secrets in GitHub) — sync-neo4j.yml"]
        direction TB
        CI1["build_graphml.py<br/>yml → release_catalog.graphml (commit, SHA)"]
        CI2["load_neo4j.py<br/>wipe + APOC import (SHA-pinned URL)<br/>NEO4J_* from GitHub Secrets"]
        CI1 --> CI2
    end
    DB[("🗄️ Neo4j<br/>catalogdb pod")]

    CSV --> MAP
    A1 & A2 & A3 --> REDUCE
    R4 -- "fail: fix upstream component.yaml<br/>or correct ref, re-validate" --> R3
    R4 -- "pass" --> GATES
    H1 -- approve --> S1
    H2 -- approve --> C1
    C1 -- "push to dev triggers" --> CI
    CI2 --> DB

    classDef human fill:#fde68a,stroke:#d97706,color:#111;
    classDef gate fill:#dbeafe,stroke:#2563eb,color:#111;
    class H1,H2 human;
    class R4 gate;
```

## Human checkpoints

| Gate | When | What the human does |
|------|------|---------------------|
| **H1** | after the global build | Review the site `git diff` + confirm the build is clean → approve push to `docusaurus-demo` (live site deploy) |
| **H2** | after `catalog_parser validate` passes | Review the `release_catalog.yml` diff → approve `git push origin dev` |
| **(implicit)** | any ambiguity | Unresolved `validate`, uncertain versions, or dependency choices pause for the human |

The **`validate`** step is the automated guard between REDUCE and the human gate: a
`related_to` that doesn't resolve would crash `build_graphml.py` (`KeyError`) in CI, so
the release stops locally until it's fixed.

## Why not 10 fully-independent pipelines

Two agents writing `docusaurus.config.js` or `release_catalog.yml` at the same time
corrupt the file, and `hasDependentComponents` can point at another component in the
**same** batch — so the shared writes, the single build, and the dependency validation
must be one serial REDUCE. The cap is **5** MAP agents; for small batches, run MAP
inline (the bottleneck is the global build + human review, which don't parallelize).

## Secrets boundary

The agent leaves `release_catalog.yml` valid and pushed; **CI does the graph + DB
work** with `NEO4J_URI/USER/PASSWORD` and `GRAPHML_URL` from GitHub Secrets. The agent
never reads a `.env` or password file. Manual re-ingest = run `scripts/load_neo4j.py`
locally with a `.env` (agent must not read it).
```
