---
name: icicle-tc-deploy-api
disable-model-invocation: true
description: Deploy OpenAPI v3 documentation into the training-catalog Docusaurus site. Accepts a CSV of GitHub OpenAPI-spec links (with tags), a single spec link, or a local spec file; stages the spec JSON under my-website/api_config_files/, wires a docusaurus-plugin-openapi-docs config entry, generates MDX under my-website/api-docs/<Name>/ with `npx docusaurus gen-api-docs`, injects the tag list into every generated *.api.mdx (gen-api-docs does not add tags), then builds and fixes errors. Reads the release-testing catalog CSV (Component, OpenAPI JSON, Tags, Release Dates columns; only rows with an OpenAPI JSON produce docs); the api-docs folder name comes from the Component column (Title-Cased repo name for a bare GitHub link). Use when the user asks to add or regenerate API docs in the training-catalog site. This skill only makes sense inside the training-catalog repo.
---

# ICICLE Training-Catalog — API Docs Deploy

Generates Docusaurus OpenAPI docs from one or more OpenAPI **v3** spec JSON files
and wires them into this repo's `my-website/api-docs/` tree, then verifies the
build.

## Scope

Run only inside the `training-catalog` repo — it edits
`my-website/docusaurus.config.js`, stages specs in `my-website/api_config_files/`,
and generates into `my-website/api-docs/`. If `my-website/docusaurus.config.js` is
absent, stop and say so. All commands run from `my-website/`.

## Helper: `api_parser.py`

The repetitive Python work is bundled in `api_parser.py` **next to this file**
(`.claude/skills/icicle-tc-deploy-api/api_parser.py`) — use it instead of writing
one-off scripts. It is **standard-library only**, so plain `python3` works (no venv
needed). Subcommands map to the steps below:

```bash
P=../.claude/skills/icicle-tc-deploy-api/api_parser.py   # from my-website/
python3 $P csv-rows  --csv "<csv>"                       # Step 1: list rows that have a spec
python3 $P stage     --source "<url|path>" --slug <slug> # Step 3: download/copy + validate v3
python3 $P config-snippet --name "<Name>" --slug <slug>  # Step 4: print the config.js block
python3 $P inject-tags --dir "api-docs/<Name>" --tags API <canonical...> "Release <YYYY-MM>"  # Step 6
```

## Targeted update — one component only

If the user only wants to (re)deploy specific component(s) — e.g. they pass name(s)
after the slash command, like `/icicle-tc-deploy-api ICICLE Embedding Service, ICICLE
Vector DB Service`, or a spec changed — **don't reprocess the whole CSV**. Get just
those rows with `--only` (comma-separated; names contain spaces), then run Steps 3–7
for each:

```bash
python3 ../.claude/skills/icicle-tc-deploy-api/api_parser.py \
  csv-rows --csv "../Release Testing(2026-05).csv" \
  --only "ICICLE Embedding Service, ICICLE Vector DB Service"
```

The plugin instance for that slug is likely already wired in `docusaurus.config.js`
(Step 4) — leave it. For a **changed spec**, regenerate cleanly so removed endpoints
don't linger, then re-tag (the build is global — one build at the end):

```bash
python3 .../api_parser.py stage --source "<url>" --slug <slug>       # restage spec
npx docusaurus clean-api-docs <slug> -p openapi-<slug>              # drop old MDX
npx docusaurus gen-api-docs   <slug> -p openapi-<slug>              # regenerate
python3 .../api_parser.py inject-tags --dir "api-docs/<Name>" --tags API <...> "Release <YYYY-MM>"
```

## Step 1 — Ask the user for the source

Ask which input they have (do not guess):

1. **CSV file** of multiple components (the release-testing catalog CSV in the repo
   root is the common case, e.g. `../Release Testing(2026-05).csv`). Columns are
   resolved case-insensitively and tolerantly:
   - **OpenAPI JSON** *(required for a row to produce API docs)* — URL to an OpenAPI
     v3 spec JSON (GitHub blob or raw). Matched by prefix, so `OPENAPI JSON` or
     `OpenAPI JSON Link` both resolve. **Not every component has one — process only
     the rows where this cell is non-empty and silently skip the rest.**
   - **Component** *(used as the folder name)* — the `api-docs/<Component>/` folder
     and display label come from this column (e.g. `ICICLE Vector DB Service`). The
     spec filename / config key is a lowercase-hyphenated slug of it.
   - **Tags** *(required)* — comma-separated tags. Matched by prefix, so the catalog's
     `Tags: Training Catalog` header resolves here.
   - **Release Dates** *(optional)* — `YYYY-MM`, added as a `Release <value>` tag.
   Ask for the path to the CSV, then enumerate the spec-bearing rows with the helper
   (it already applies the column rules above and skips rows with no spec):
   ```bash
   python3 ../.claude/skills/icicle-tc-deploy-api/api_parser.py \
     csv-rows --csv "../Release Testing(2026-05).csv"
   ```
   Each row in the JSON gives `name` (folder), `slug`, `source` (spec URL), `tags`,
   and `release` — drive Steps 3–6 from that.
2. **Single link** to an OpenAPI v3 spec JSON. Also ask for the **tags** (from the
   canonical list below) and, if the link is not a GitHub repo, a **name** for the
   API (used as the folder/spec name).
3. **Local file** already on disk. Ask for the **path**, a **name**, and the **tags**.

### Tags

Tags come from the canonical ICICLE tag list (same as the `icicle-readme-skill`):
`Software, CI4AI, AI4CI, Foundation-AI, PADI, Visual-Analytics, Digital-Agriculture,
Animal-Ecology, Smart-Foodsheds, Food-Access`. Every API also gets the literal tag
`API`. A `Release <YYYY-MM>` tag is added from the row's **Release Dates** column (or
a release the user gives). For a CSV the tags come from the row's **Tags** column; for
single/local input, ask the user to pick from the list. Don't invent tags.

## Step 2 — Determine the folder/spec name

- **CSV row**: use the **Component** column value verbatim as the `api-docs/<Name>/`
  folder and display label — e.g. `ICICLE Vector DB Service`. This keeps the API
  folder aligned with the component's docs folder (same name).
- **Single GitHub link** (no Component given): derive the name from the **repo name**,
  Title-Cased — split on `-`, `_`, and spaces and capitalize each word. Examples:
  `faf-frontend` → `Faf Frontend`; `food_shed_api` → `Food Shed Api`.
- **Single non-GitHub link or local file**: use the **name** the user supplied.

Use a lowercase, hyphenated slug of the name as the spec filename and config key
(e.g. `ICICLE Vector DB Service` → `icicle-vector-db-service`; `Faf Frontend` →
`faf-frontend`).

## Step 3 — Stage the spec JSON under api_config_files/

Use the helper — it converts a GitHub blob URL to raw, downloads (or copies a local
file) to `api_config_files/<slug>.json`, and **validates the spec is OpenAPI v3**,
exiting with an error if not:

```bash
python3 ../.claude/skills/icicle-tc-deploy-api/api_parser.py \
  stage --source "<spec url or local path>" --slug <slug>
```

It prints the staged path, `openapi` version, and title. If it reports a v2/Swagger
spec, tell the user — this pipeline expects v3. For a CSV, run `stage` once per row
(`source` and `slug` come from the `csv-rows` output).

## Step 4 — Wire docusaurus.config.js

For each spec, add a `docusaurus-plugin-openapi-docs` plugin instance to the
`plugins` array in `my-website/docusaurus.config.js`, following the existing
`openapi` / `openapi-faf` entries. Generate the exact block to paste with the helper
(then insert it into the `plugins` array — the helper only prints, it does not edit
the config):

```bash
python3 ../.claude/skills/icicle-tc-deploy-api/api_parser.py \
  config-snippet --name "<Name>" --slug <slug>
```

Each instance needs a **unique plugin `id`** and a config whose **key is the spec
slug** (this key is the gen-api-docs id):

```js
[
  'docusaurus-plugin-openapi-docs',
  {
    id: 'openapi-<slug>',          // unique plugin id
    docsPluginId: 'api',           // always 'api' — ties into the api docs plugin
    config: {
      '<slug>': {                  // <-- this key is the gen-api-docs id
        specPath: 'api_config_files/<slug>.json',
        outputDir: 'api-docs/<Name>',     // Component name (CSV) or Title-Cased repo name
        sidebarOptions: { groupPathsBy: 'tag' },
      },
    },
  },
],
```

Do not touch the unrelated plugin entries. Add one instance per spec.

## Step 5 — Generate the API docs

From `my-website/`, generate by the config key (the spec slug). **Because this repo
has several openapi plugin instances, you must pass the plugin id with `-p`** — without
it the CLI errors `OpenAPI docs plugin ID must be specified when more than one plugin
instance exists`:

```bash
npx docusaurus gen-api-docs <slug> -p openapi-<slug>
```

> Note: the installed `docusaurus-plugin-openapi-docs` (Docusaurus 3.8) has **no
> `--clean` flag** on `gen-api-docs`. To regenerate from scratch, clean first, then
> generate (both need `-p` here):
> ```bash
> npx docusaurus clean-api-docs <slug> -p openapi-<slug>
> npx docusaurus gen-api-docs   <slug> -p openapi-<slug>
> ```

This writes `api-docs/<Name>/`: one `*.api.mdx` per endpoint, a `*.info.mdx`, and a
`sidebar.ts`. The autogenerated API sidebar picks the folder up automatically.

## Step 6 — Inject tags into the generated MDX (required)

`gen-api-docs` does **not** add tags. The helper adds a `tags:` line to **every**
`*.api.mdx` in the folder (inserted right after `custom_edit_url:`, matching the FAF
APIs format) and is idempotent — it skips any file already tagged:

```bash
python3 ../.claude/skills/icicle-tc-deploy-api/api_parser.py \
  inject-tags --dir "api-docs/<Name>" --tags API CI4AI AI4CI Software "Release 2026-05"
```

- Always pass `API` first, then the canonical tags chosen for this spec (CSV **Tags**
  column, or what the user picked), plus `Release <YYYY-MM>` from the row's **Release
  Dates** column (or the release given). Result, e.g.:
  `tags: [API, Food-Access, Smart-Foodsheds, Release 2026-05]`.
- The `*.info.mdx` does not need tags (the FAF example has none) — the helper only
  touches `*.api.mdx`.

For a CSV, run `inject-tags` once per folder with that row's own tags.

## Step 7 — Build and fix

From `my-website/`:
```bash
npm install      # first run only
npm run build
```

**Secrets for a local verification build.** `docusaurus.config.js` enables the
`@dipakparmar/docusaurus-plugin-umami` analytics plugin, whose `websiteID`,
`analyticsDomain`, and `dataHostURL` are **required** and read from env vars. CI sets
the real values; locally they're unset, so a bare `npm run build` aborts config
validation with `"websiteID" is required` before any page is built. This is unrelated
to the API docs. Do **not** edit the analytics config to work around it — pass
throwaway placeholders for this verification build only (never committed; real secrets
live in CI):
```bash
UMAMI_WEBSITE_ID=local-verify \
UMAMI_ANALYTICS_DOMAIN=example.com \
UMAMI_DATA_HOST_URL=https://example.com \
UMAMI_DATA_DOMAINS=example.com \
npm run build
```
More generally: if the build fails a config/plugin validation purely for a missing
secret env var (not a spec/MDX error), supply a dummy value for that var and rebuild —
never weaken or remove the plugin config to make the build pass.

Fix any errors and rebuild until clean — the clean build is the gate, your job is
done only when `npm run build` exits with no errors. Common issues:
- A spec key in `docusaurus.config.js` whose `specPath` doesn't exist, or a typo in
  `id`/`docsPluginId` (must be `'api'`).
- An invalid or non-v3 spec failing generation — re-check the JSON.
- MDX errors in a generated file from odd characters in the spec descriptions.

Re-run `npm run build` after each fix.

## Step 8 — Report

List the API folder(s) created under `api-docs/`, the config keys added, and confirm
the clean build. Do not commit, push, or deploy unless the user explicitly asks —
pushing to `docusaurus-demo` triggers the GitHub Pages deploy workflow.

**Component docs cross-link.** The `icicle-tc-deploy-doc` skill adds a "see the API
documentation" link to a component's main doc when `api-docs/<Component>/` exists. So
after generating API docs here, **(re-)run the doc skill** for the same components to
add that link (it matches by the shared `Component` folder name). Running the doc skill
before these API docs exist is harmless — it just omits the link, no broken link.
