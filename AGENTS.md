# AGENTS.md — training-catalog

Guide for AI coding agents (Claude Code, Codex, Cursor, …) working in this repo.
Claude Code reads this via `CLAUDE.md`, which imports this file. Codex and Cursor
read `AGENTS.md` directly.

## What this repo is

The **ICICLE AI Institute Training Catalog**: a Docusaurus site that aggregates
component documentation, API documentation, education material, and workshops for
ICICLE. The deployed site lives at `https://ICICLE-ai.github.io/training-catalog/`.

## Layout

| Path | What it is |
|------|------------|
| `my-website/` | The Docusaurus site (all build/serve commands run from here) |
| `my-website/docs/` | Component docs — one folder per component, generated from READMEs |
| `my-website/api-docs/` | Generated OpenAPI docs — one folder per API |
| `my-website/api_config_files/` | OpenAPI v3 spec JSON files consumed by the openapi plugin |
| `my-website/docusaurus.config.js` | Site config; plugin instances incl. openapi-docs |
| `my-website/Education/`, `workshops/`, `other_resources/`, `sample_docs/` | Additional content-docs plugin roots |
| `.claude/skills/` | Project-local skills (auto-discovered by Claude in this repo) — all six live here |
| `.github/workflows/deploy.yml` | CI: builds and deploys to GitHub Pages on push to `docusaurus-demo` |

## Tooling & commands

Node `>=18`, npm. From `my-website/`:

```bash
npm install            # install deps (first run)
npm run start          # local dev server
npm run build          # production build — the gate for "done"; must exit clean
npm run serve          # serve the production build locally
npx docusaurus gen-api-docs <id> -p openapi-<id>     # generate OpenAPI docs (‑p required: multiple plugin instances; no --clean flag in 3.8)
npx docusaurus clean-api-docs <id> -p openapi-<id>   # remove generated OpenAPI docs for a spec
```

Python: deps are declared at the **repo root** in `pyproject.toml` + `uv.lock` (with a
plain `requirements.txt` mirror). `uv sync` provisions the repo-root `uv` virtualenv
(`.venv`, gitignored); run `readme_parser.py` via `../.venv/bin/python …`. The API
helper `api_parser.py` is standard-library only — run it with plain `python3` (no
venv). Set `GITHUB_PAT` to fetch READMEs from private repos.

`onBrokenLinks` / `onBrokenMarkdownLinks` are set to `warn`, so link problems don't
fail the build — but MDX compile errors do.

The `docusaurus-plugin-umami` analytics plugin requires `UMAMI_WEBSITE_ID`,
`UMAMI_ANALYTICS_DOMAIN`, and `UMAMI_DATA_HOST_URL` env vars; CI provides the real
secrets. For a local verification build, prefix `npm run build` with throwaway
placeholders (e.g. `UMAMI_WEBSITE_ID=local-verify UMAMI_ANALYTICS_DOMAIN=example.com
UMAMI_DATA_HOST_URL=https://example.com npm run build`) — never edit the plugin config
to dodge the missing-secret error.

## Skills

Six skills support this repo. All are **user-invoked** (`disable-model-invocation:
true`) — run them when the user asks, not automatically. `icicle-release` is the
top-level orchestrator; the rest are the building blocks it sequences (and which you
can also run on their own).

### `.claude/skills/icicle-tc-deploy-doc` — Component docs deploy
Fetches a component's GitHub README (single repo, or a batch **Excel/CSV** — e.g. the
release-testing catalog CSV), runs the bundled `readme_parser.py` to split it into
Docusaurus docs under `my-website/docs/<Component>/`, merges (never wipes) tags and
content, rewrites relative images→`raw.githubusercontent.com` and other relative
links→`github.com/.../blob/...`, then builds and fixes errors. Batch columns are
resolved tolerantly: `README`, a `Tags…` column, optional `Component` (the folder
name) and `Release Dates`. In the main doc it also standardizes badges (centered
block, GitHub + a license badge lifted from the README's License section) and, when
`api-docs/<Component>/` exists, adds a baseUrl-aware `:::tip` link to that API
reference page (best-effort, no ordering deadlock — re-run after API docs exist). The
parser (`readme_parser.py`) is bundled inside this skill folder. See its `SKILL.md`.

### `.claude/skills/icicle-tc-deploy-api` — API docs deploy
Takes a CSV of components (the release-testing catalog CSV: `Component`, `OpenAPI JSON`,
`Tags…`, `Release Dates` columns — only rows with an OpenAPI JSON produce docs), a
single spec link, or a local spec file; stages the JSON under `api_config_files/`,
wires a `docusaurus-plugin-openapi-docs` config entry, runs `gen-api-docs`, injects the
tag list into every generated `*.api.mdx` (gen-api-docs omits tags), then builds and
fixes errors. The `api-docs/<Name>/` folder comes from the CSV `Component` column (or a
Title-Cased repo name for a bare GitHub link). Repetitive Python work (read CSV rows,
stage+validate spec, print the config block, inject tags) is bundled as the
stdlib-only `api_parser.py` next to the skill. See its `SKILL.md`.

### `.claude/skills/icicle-tc-deploy-resource` — Resource-listing deploy
Adds/updates a resource link on the catalog's Resources page
(`my-website/other_resources/0_intro.md`). Takes a CSV with a `Resource Link` column
(plus `Component`, `Tags…`, `Release Dates`) or a single name/link, **verifies the
link resolves**, then inserts it at the correct **alphabetical** position — either as
a new top-level `## <Name>` product block or as a bold-bullet sub-entry inside an
existing container section such as `TACC and Tapis Resources`. **Idempotent**
(re-running replaces in place, never duplicates) and **never invents a version**.
Descriptions aren't in the CSV — the caller supplies one (fetched from the page or the
README). The stdlib-only helper `resource_parser.py` (`csv-rows`, `check-link`,
`insert`) is bundled next to the skill. See its `SKILL.md`.

### `.claude/skills/icicle-release` — Release orchestrator
End-to-end release workflow. Given the release-testing CSV (or a single component), it
drives the other skills **in order per component**: validate README structure
(`icicle-readme-skill`) → deploy docs (`icicle-tc-deploy-doc`) → deploy API docs if
there's an `OpenAPI JSON` (`icicle-tc-deploy-api`, then re-run the doc step for the
cross-link) → add the resource link if there's a `Resource Link`
(`icicle-tc-deploy-resource`) → validate/fill `component-info.yaml`
(`icicle-component-info-skill`: dependencies, version, `licenseUrl`). Then one global
site build gate, then it appends each component's catalog entry (fetched from the
**`Component Catalog YAML File`** GitHub link) to the external CI-Components-Catalog
repo's **`release_catalog.yml`** on its **`dev`** branch and, after an explicit
confirmation, pushes. Catalog flow is intentionally ICICLE-specific: single-maintainer,
direct push to `dev`, `master` unused. A final notebook/service-refresh step
(run notebook → GraphML → push → wait → restart; **never read the password file**) is a
**deferred Phase 2 stub**. Modular and idempotent — run it to publish or to update.
See its `SKILL.md`.

### `icicle-readme-skill` — Generic ICICLE README scaffolder
Scaffolds/updates a single top-level `README.md` for any `github.com/ICICLE-ai/`
component repo (Diátaxis: description + tags + license + acknowledgements, then
Tutorials / How-To / Explanation). Generic and repo-agnostic — the `icicle-release`
orchestrator reuses it to validate a component's upstream README before deploying.
Lives project-locally under `.claude/skills/icicle-readme-skill/`; a copy is also kept
installed globally (`~/.claude/skills/`) so it can be run standalone in any ICICLE-ai
component repo — keep the two in sync when editing. See its `SKILL.md`.

### `icicle-component-info-skill` — Generic ICICLE component-catalog metadata
Scaffolds/updates a single top-level `component-info.yaml` for any
`github.com/ICICLE-ai/` component repo — the machine-facing sibling of the README
skill. Produces one YAML list entry (`id`, `owner`, `primaryThrust`, `name`, `status`,
`description`, `componentVersion`, `targetIcicleRelease`, `hasDependentComponents`,
`licenseUrl`, `publicAccess`, `sourceCodeUrl`, and the codeReview/tests/docs/tutorials
flags) that the ICICLE component catalog consumes. Enforces `id ==
"<name-without-spaces>:<componentVersion>"`, validates `status` and `primaryThrust`
against ICICLE's controlled vocabularies (see the skill), treats `targetIcicleRelease`
as `YYYY-MM`, leaves `trainingTutorialsUrl` (and any catalog-hosted
`developerDocumentationUrl`) out because those are filled in after catalog deployment,
always asks about dependencies before writing `hasDependentComponents`, and never
commits/pushes without explicit user confirmation. Generic and repo-agnostic — reused
by the `icicle-release` orchestrator. Like the README skill it lives project-locally
under `.claude/skills/icicle-component-info-skill/`, with a global copy kept installed
(`~/.claude/skills/`) for standalone use in any ICICLE-ai component repo — keep the two
in sync when editing. See its `SKILL.md`.

## Canonical tag list

Component and API docs tag from this list (the README skill enforces it):

```
Software  CI4AI  AI4CI  Foundation-AI  PADI  Visual-Analytics
Digital-Agriculture  Animal-Ecology  Smart-Foodsheds  Food-Access
```

API docs additionally use the literal tag `API`. A `Release <YYYY-MM>` tag marks the
release a doc was generated for. Don't invent tags — ask the user if unclear.

## Conventions for agents

- Run build/gen commands from `my-website/`.
- Updating docs is **additive**: re-run the parser over an existing component folder
  rather than deleting it — tags accumulate and content refreshes in place. To update
  a subset (not the whole CSV), pass `--only "<Component>[, <Component>…]"` (comma-
  separated, case-insensitive) to the doc parser / `api_parser.py csv-rows`; then run a
  single global `npm run build`.
- Edit generated files narrowly; don't reformat unrelated content.
- **Release-testing CSV columns** (resolved case-insensitively / by prefix): `README`,
  `Tags…`, `Component`, `Release Dates`, `OpenAPI JSON`, plus two consumed only by the
  release workflow — **`Resource Link`** (→ `icicle-tc-deploy-resource`) and
  **`Component Catalog YAML File`** (a GitHub link to the component's
  `component-info.yaml`, → the `icicle-release` catalog step). Rows missing a given
  column are skipped by that step.
- **Do not commit, push, or deploy unless the user explicitly asks.** A push to
  `docusaurus-demo` triggers the live GitHub Pages deploy; a push to the external
  CI-Components-Catalog `dev` branch changes the live component catalog.
