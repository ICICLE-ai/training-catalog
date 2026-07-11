---
name: icicle-release
disable-model-invocation: true
description: End-to-end, multi-agent ICICLE release workflow for the training-catalog. Given a release-testing CSV (or a single component), it fans out up to 5 parallel MAP agents (one component each — validate README structure via icicle-readme-skill, deploy docs via icicle-tc-deploy-doc, deploy API docs via icicle-tc-deploy-api when there's an OpenAPI spec, prep the resource link via icicle-tc-deploy-resource, prep component-info via icicle-component-info-skill) into disjoint per-component folders, then a single serial REDUCE step applies the shared-file edits (docusaurus.config.js, other_resources/0_intro.md, release_catalog.yml), runs one global build, appends+validates each catalog entry via catalog_parser.py, and — after explicit human approval at each gate — pushes the site repo and the external CI-Components-Catalog dev branch. Pushing release_catalog.yml triggers the catalog's sync-neo4j.yml workflow (graphml regen + Neo4j ingest) using GitHub Secrets, so the agent never handles the Neo4j password. Modular and idempotent: run to publish or update. Never commits or pushes without explicit user permission. Use when the user asks to run an ICICLE release / publish or update a batch of components. Only makes sense inside the training-catalog repo.
---

# ICICLE Release — Multi-Agent Orchestrator

One reusable workflow that publishes (or updates) a batch of ICICLE components into
the training-catalog **and** the external component catalog. It does **not**
re-implement anything — it **sequences the existing skills** and adds the two steps
that had no tooling (resource listing, catalog append/validate). Additive and
idempotent: same flow for an initial publish or an update.

## Architecture: MAP (parallel) → REDUCE (serial) → human-gated push

The per-component pipelines are independent **only for the work that writes to
disjoint paths**. Docs live in `docs/<Component>/` and API docs in
`api-docs/<Component>/` — safe to build in parallel. But every release also converges
on **shared files** — `docusaurus.config.js`, `other_resources/0_intro.md`,
`release_catalog.yml` — plus **one global `npm run build`** and **gated git pushes to
two repos**. Parallel writers to a shared file corrupt it, and `hasDependentComponents`
can reference another component in the **same** batch. So the design is fan-out/gather,
not N independent end-to-end pipelines.

```
                 ┌──────────── MAP: up to 5 agents in parallel ────────────┐
 release CSV ──► │ agent/comp: readme-validate → deploy-doc → deploy-api    │
 (one agent      │            → resource-PREP → component-info-PREP          │
  per component) │ writes ONLY disjoint docs/<C>/ , api-docs/<C>/            │
                 │ emits a "bundle": shared-file edits it needs (config      │
                 │ plugin block, 0_intro entry, catalog entry+URL+deps)      │
                 └──────────────────────────┬──────────────────────────────┘
                                            ▼
                 ┌──────── REDUCE: single writer, sequential ──────────────┐
                 │ apply bundles one at a time to the shared files          │
                 │ (docusaurus.config.js, 0_intro.md, release_catalog.yml)  │
                 │ → ONE global `npm run build` (fix MDX until clean)        │
                 │ → catalog_parser append + VALIDATE (deps must resolve)   │
                 └──────────────────────────┬──────────────────────────────┘
                                            ▼
        ┌──── HUMAN GATES (checks in the loop) ────┐
        │ H1 review site diff  → push docusaurus-demo (site deploy)         │
        │ H2 review release_catalog.yml diff → push CI-Components-Catalog dev│
        └──────────────────────────┬──────────────────────────────────────┘
                                   ▼
        CI takes over: push to dev fires sync-neo4j.yml
        (build_graphml.py → commit graphml → load_neo4j.py ingest,
         secrets from GitHub Secrets — agent never sees the Neo4j password)
```

**Scale note.** For a handful of components the MAP fan-out is optional — the
bottleneck is the single global build + human review + gated pushes, which don't
parallelize. Fan out (cap **5** concurrent agents) only when the batch is large; for a
few rows just run the MAP steps inline. The REDUCE step is always single-writer.

## Scope & guardrails

- Run only inside `training-catalog` (guard on `my-website/docusaurus.config.js`).
  Site build commands run from `my-website/`.
- **Never commit, push, or deploy without explicit user approval** — for **both** the
  site repo (`docusaurus-demo` → live site) and the catalog repo (`dev` → live
  catalog). Each push is its own human gate.
- **The agent never handles the Neo4j password.** The graph/DB sync runs in CI from
  GitHub Secrets (see "Graph & Neo4j sync"). Never read or print any `.env`/secret.
- MAP agents write only to their own `docs/<Component>/` and `api-docs/<Component>/`
  and must **not** edit shared files, run the global build, or run git. Those are
  REDUCE-only.

## Inputs

- **Batch:** the release-testing CSV. Columns (case-insensitive / prefix-matched):
  `Component`, `README`, `Tags…`, `Release Dates`, `OpenAPI JSON`, `Resource Link`,
  `Component Catalog YAML File` (a GitHub link to the component's `component.yaml`).
  Rows lacking a given column are skipped by that step.
- **Single component:** its GitHub README URL plus whatever applies.
- **Subset:** pass component names to each step's `--only` (comma-separated).

Confirm the release `YYYY-MM` up front.

## MAP — per component (parallel, cap 5; steps sequential within a component)

Each agent handles ONE component. Reuse each skill per its own `SKILL.md`.

1. **README structure check — `icicle-readme-skill`.** The doc parser splits on
   `# Tutorials` / `# How-To Guides` / `# Explanation` (delimited by `---`) and lifts
   tags + license, so the README must conform first. Fix upstream if needed.
2. **Deploy docs — `icicle-tc-deploy-doc`.** `readme_parser.py` (repo-root `.venv`),
   `--only "<Component>"`. Writes the disjoint `docs/<Component>/`.
3. **Deploy API docs — `icicle-tc-deploy-api`** (only if `OpenAPI JSON`). Stages the
   spec and writes `api-docs/<Component>/`. The **config-block edit and `gen-api-docs`
   run in REDUCE** (they touch shared `docusaurus.config.js`); the MAP agent just
   emits the config block to apply.
4. **Resource link PREP — `icicle-tc-deploy-resource`** (only if `Resource Link`).
   `check-link`, write the one-sentence description, decide placement. The actual
   `insert` into shared `0_intro.md` happens in REDUCE. **Never invent a version.**
5. **component-info PREP — `icicle-component-info-skill`.** Ensure the upstream
   `component.yaml` is valid: **ask about dependencies**, **confirm `componentVersion`**,
   fill `licenseUrl`. Leave `trainingTutorialsUrl` blank here — it's set catalog-side
   in REDUCE (the component's own repo can't know its catalog URL yet).

Each agent returns a **bundle**: the shared-file edits it needs (API config block,
resource entry, and the catalog entry: its `component.yaml` link, computed training
URL, and `dependsOn` list).

## REDUCE — single writer, sequential

1. **Apply shared-file edits one at a time:** paste each API config block into
   `docusaurus.config.js` and run `npx docusaurus gen-api-docs <slug> -p openapi-<slug>`;
   run each resource `insert` into `0_intro.md`; re-run the doc step for any API
   component so its `:::tip` cross-link resolves.
2. **One global build gate** from `my-website/`, fix MDX until clean:
   ```bash
   UMAMI_WEBSITE_ID=local-verify UMAMI_ANALYTICS_DOMAIN=example.com \
   UMAMI_DATA_HOST_URL=https://example.com UMAMI_DATA_DOMAINS=example.com \
   npm run build
   ```
3. **Catalog append + validate** (next section).
4. **Human gates, then pushes** (next section).

## Catalog append + validate (CI-Components-Catalog)

The catalog is a **separate repo**, and **`catalog_parser.py` lives there** —
`CI-Components-Catalog/scripts/catalog_parser.py`, next to `build_graphml.py` and
`load_neo4j.py` (it operates only on catalog files, and CI can call it too). There is
deliberately **no copy in training-catalog**. Run it from the catalog clone root.

> **ICICLE-specific note (by design).** Single-maintainer model, **direct push to
> `dev`**; **`master` is not used** for the component catalog as of writing. Revisit if
> governance changes (multiple maintainers, PR review, a promoted release branch).

1. **Locate the clone.** Find a local `CI-Components-Catalog` checkout; if absent, ask
   the user for a clone URL (then clone) or the existing path. Don't guess.
2. **Fresh `dev`.** `git checkout dev && git pull`; verify you're on `dev`.
3. **Append each entry — `release_catalog.yml` ONLY**, from the CSV's
   `Component Catalog YAML File` link:
   ```bash
   python3 scripts/catalog_parser.py append --catalog release_catalog.yml \
     --source <github blob link to component.yaml> \
     --release <YYYY-MM> \
     --training-url https://icicle-ai.github.io/training-catalog/docs/category/<slug>
   ```
   Idempotent: re-appending the same `id` replaces its block in place.
4. **Validate — the guard that prevents a CI crash:**
   ```bash
   python3 scripts/catalog_parser.py validate --catalog release_catalog.yml
   ```
   Every `related_to` must resolve to an existing `id`. `build_graphml.py` raises
   `KeyError` on an unknown ref, so a bad dep would crash `sync-neo4j.yml`. **Do not
   push until validate exits 0.**

### Catalog field rules (the lessons this workflow encodes)

- **`targetIcicleRelease` = the release you're deploying.** Pass `--release <YYYY-MM>`
  for any component being released/updated now. **Exception — rename-only:** when a
  *prior-release* component is merely renamed in the training catalog, **keep its
  original release** (omit `--release`; only change id/name/URLs).
- **`trainingTutorialsUrl` = the deployed category route**,
  `…/docs/category/<slug>`, where `<slug>` is the Docusaurus slug of the component
  folder (lowercase, spaces→`-`, `&`→dropped, e.g. `Intelligent Semantic Segmentation
  & Annotation` → `intelligent-semantic-segmentation--annotation`). **Verify it
  resolves** in the build output (`my-website/build/docs/category/<slug>.html`) — the
  canonical page is the base slug, not a `-1`/`-2` collision variant. Pass
  `--also-usage-url` if the entry's `usageDocumentationUrl` also points at a stale
  training-catalog link.
- **`dependsOn` must resolve — and source `component.yaml` files can be stale.** A
  component repo's `component.yaml` may carry an unresolvable `related_to` (seen:
  `Patra:0.1.0` where the real id is `PatraToolkit:0.2.0`; `icicleai-tapisui-extension:0.1.1`
  vs the real `:0.1.0`). `append` copies the source verbatim, so **`validate` will flag
  these** — resolve by fixing the upstream `component.yaml` (preferred) or correcting the
  ref in `release_catalog.yml`, pinning to the latest matching catalog id. Validate
  after **all** appends (a component may depend on another in the same batch).
- **Rename mechanics:** change `id` + `name` + URLs together; keep everything else
  (including `targetIcicleRelease`); confirm nothing else `related_to` the old id.

## Human gates & pushes

- **H1 — site.** Show the site `git diff` and the clean build. On approval, push the
  site repo (`docusaurus-demo` → live GitHub Pages deploy).
- **H2 — catalog.** Show the `release_catalog.yml` diff and the passing `validate`.
  On approval, `git push origin dev` on the catalog repo.

Never push either repo without its explicit approval. Any ambiguity (versions,
dependencies, unresolved `validate`) pauses for the human.

## Graph & Neo4j sync (CI — no agent involvement)

Pushing `release_catalog.yml` to `dev` triggers the catalog repo's
`.github/workflows/sync-neo4j.yml`:
1. `build_graphml.py` regenerates `release_catalog.graphml` from the yml and commits it
   back (`[skip ci]`), outputting the commit SHA.
2. `load_neo4j.py` wipes Neo4j and APOC-imports the graphml from a **SHA-pinned raw
   URL** (`GRAPHML_URL`), with `NEO4J_URI/USER/PASSWORD` from **GitHub Secrets**.

The agent's only job is to leave `release_catalog.yml` valid and pushed. It does **not**
run the notebook or touch the Neo4j password. If you need a manual re-ingest, run
`scripts/load_neo4j.py` locally with a `.env` (which the agent must not read).

## Order of operations

```
MAP (parallel, cap 5 — disjoint per-component work):
  per component: readme-validate → deploy-doc → deploy-api → resource-prep → info-prep
                 → emit bundle (shared-file edits + catalog entry/URL/deps)
REDUCE (serial, single writer):
  apply config/resource edits → ONE global npm run build (fix MDX)
  → catalog_parser append (--release, --training-url) → catalog_parser VALIDATE (must pass)
HUMAN GATES:
  H1 review site diff  → push docusaurus-demo
  H2 review release_catalog.yml diff (+ validate 0) → push CI-Components-Catalog dev
CI (automatic): sync-neo4j.yml → build_graphml → commit graphml → load_neo4j ingest
```

Do not commit/push either repo without explicit user permission.
