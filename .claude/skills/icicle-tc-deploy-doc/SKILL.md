---
name: icicle-tc-deploy-doc
disable-model-invocation: true
description: Deploy ICICLE component documentation into the training-catalog Docusaurus site. Fetches a component's GitHub README, runs the bundled readme_parser.py to split it into well-structured Docusaurus docs (main + Tutorials / How-To / Explanation) under my-website/docs/<Component>/, merges (never wipes) existing tags and content, rewrites relative images to raw.githubusercontent.com and other relative links to github.com blob URLs so they stay clickable off-GitHub, then runs the production build and fixes any errors. Use when the user asks to add, update, or (re)generate component docs in the training-catalog site, or mentions the README parser / docs pipeline. This skill only makes sense inside the training-catalog repo.
---

# ICICLE Training-Catalog — Component Docs Deploy

Turns a component's GitHub `README.md` into Docusaurus docs inside this repo's
`my-website/docs/` tree, then verifies the site builds clean.

The script that does the parsing — `readme_parser.py` — lives **next to this
file** (`.claude/skills/icicle-tc-deploy-doc/readme_parser.py`). The skill's job
is to drive it correctly and then guarantee a clean build.

## Scope

Run this only inside the `training-catalog` repo (it writes into `my-website/docs/`
and builds the Docusaurus site there). If `my-website/docusaurus.config.js` is not
present, stop and tell the user this skill must run from the catalog repo root.

## What the parser produces

For each component it writes `my-website/docs/<Component>/`:

- `<Component>.md` — the first README section (title + description + badges). Gets
  a `Release <YYYY-MM>` tag added **only here** when `--release` is given.
- `tutorials.md`, `how-to.md`, `explanation.md` — filled from README sections whose
  heading matches `# Tutorials`, `# How-To Guides`, `# Explanation`. Sections are
  delimited in the README by lines containing only `---`.
- `_category_.json` — `{ "label": "<Component>", "link": {"type":"generated-index"} }`
  so the folder renders as a sidebar category.

### Badges & license (built in)

In the main `<Component>.md`, the parser standardizes the badge area (automatic — no
flags):

- All shield/badge images are collected and re-emitted as a **single
  center-aligned block** (`<div align="center">…</div>`) placed right after the
  description paragraph — never above the title or scattered through the body.
- A **GitHub Repo** badge linking to the component repo is added first.
- The **license** is read from the README's `## License` / `### License` section —
  whether it's a shields badge, a `[License: <name>](<link>)` link, or a "licensed
  under the <X> License … [LICENSE](…)" sentence — and re-emitted as one standardized
  `License: <name>` shields badge placed **right next to the GitHub badge**. The raw
  `License:` text / section is then removed from the body (it exists in the README
  only so we can lift the name + link). Order in the block: GitHub, License, then any
  other badges.

### API cross-link (built in)

If a component also has API docs on this site (`api-docs/<Component>/`, deployed by
the `icicle-tc-deploy-api` skill), the parser adds a Docusaurus `:::tip API reference`
callout to the main doc linking to that API reference page. The link is a
**root-relative, baseUrl-aware route** read from the generated API docs' `info_path`
(e.g. `/api/ICICLE%20Embedding%20Service/icicle-ai-embed-service`), so once deployed it
resolves to `…/training-catalog/api/…` and passes the broken-link checker.

- It matches by **folder name**: `api-docs/<Component>/` must exist for the same
  `<Component>` as the docs folder (both skills name the folder from the CSV
  `Component`, so they line up).
- **No ordering deadlock.** The check is best-effort: if the API folder isn't there
  yet, no link is added and nothing breaks. So you can run the skills in either order
  — but for the link to appear, **deploy the API docs first, or re-run this doc skill
  after** the API docs exist. Re-running never duplicates the callout (the body is
  rebuilt from the README each run).
- Override the location with `--api_docs_dir` (defaults to the `api-docs` sibling of
  `--output_folder`).

### Update-in-place, never destroy (important)

`save_file` is additive on metadata:

- **Tags merge.** Existing frontmatter tags in a file are read first, then new tags
  are appended and de-duplicated (first-seen order kept). Re-running with a new
  `--release` therefore *adds* `Release 2026-05` while keeping `Release 2025-07`.
- **Body content is refreshed** from the current README (so content edits flow
  through), while stray inline `tags:` lines are stripped and badges are recentered
  below the description (see "Badges & license" above).

Never hand-delete a component folder to "regenerate cleanly" unless the user asks —
re-running the parser over an existing folder is the supported update path and
preserves accumulated tags.

### Link & image rewriting (built in)

Before splitting, the parser rewrites relative references using the repo/branch it
resolved the README from:

- relative **images** (`![](images/x.png)`, `<img src="...">`) → `https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path>`
- relative **links** (`[text](docs/g.md)`, `<a href="...">`) → `https://github.com/<user>/<repo>/blob/<branch>/<path>`
- absolute URLs, `#anchors`, `mailto:` and fenced code blocks are left untouched.

This is automatic — no flags needed. It exists because the catalog is deployed off
GitHub, so relative paths would otherwise 404.

## Prerequisites

Dependencies are declared in the **project root** (`pyproject.toml` + `uv.lock`, with
a plain `requirements.txt` mirror) — not inside this skill. `uv sync` provisions the
repo-root `uv` virtualenv (`.venv`, gitignored); run the parser through it:

```bash
uv sync                                                  # from the repo root
# then invoke the parser with that interpreter, e.g.
#   ../.venv/bin/python ../.claude/skills/icicle-tc-deploy-doc/readme_parser.py ...
```

(`requests` + `pandas` are always needed; `openpyxl` only for `--excel_file` mode.)

For private repos, export a token first so the README fetch is authorized:

```bash
export GITHUB_PAT=<token>                 # or pass --github_pat
```

## Steps

1. **Confirm location.** Ensure `my-website/docusaurus.config.js` exists. All
   commands below run from the `my-website/` directory so output lands in
   `my-website/docs/`.

### Targeted update — one component only

If the user only wants to update specific component(s) (e.g. they pass name(s) after
the slash command, like `/icicle-tc-deploy-doc ICICLE Vector DB Service, Smart
Labeler`), **do not rerun the whole table** — pass `--only` to the batch CSV so just
those rows are processed. `--only` is **comma-separated** (names contain spaces, so
commas — not spaces — separate them); one name or several both work:

```bash
../.venv/bin/python ../.claude/skills/icicle-tc-deploy-doc/readme_parser.py \
  --csv_file "../Release Testing(2026-05).csv" \
  --release 2026-05 --output_folder docs \
  --only "ICICLE Vector DB Service, Smart Labeler, ICICLE Chatbook"
```

This is safe and cheap because updates are additive/idempotent (see below): only the
named folders are refreshed, tags merge, siblings are untouched. Names are matched
case-insensitively; an unmatched name is skipped with a warning, and if *none* match
the run stops and lists the available components. You still run **one** `npm run build` at the end (the build is
global). If only the README changed, this doc run is all you need; if the component's
OpenAPI spec also changed, also run `icicle-tc-deploy-api` for it.

2. **Gather inputs from the user.** You need either a single repo or a batch file:
   - Single: the GitHub repo URL (root, `/blob/.../README.md`, or raw README URL).
     Optionally a component/folder name, one or more tags, and a release `YYYY-MM`.
   - Batch (Excel **or** CSV): the release-testing catalog CSV is the common case.
     Columns are resolved case-insensitively and tolerantly:
     - **README** *(required)* — GitHub repo / blob / raw README URL. Rows with an
       empty README are skipped.
     - **Tags** *(required)* — comma-separated tags. Matched by **prefix**, so the
       catalog's `Tags: Training Catalog` header resolves here.
     - **Component** *(optional but used as the folder name)* — the component's
       `my-website/docs/<Component>/` folder is named from this column. If absent,
       the folder is derived from the repo URL.
     - **Release Dates** *(optional)* — `YYYY-MM`, used per row when `--release`
       is not passed. A CLI `--release` overrides it for all rows.
     - Other columns (OpenAPI JSON, Version, Source Code, …) are ignored — the
       OpenAPI column is handled by the `icicle-tc-deploy-api` skill.

   If the user gives tags, they should come from the canonical ICICLE tag list
   (see the `icicle-readme-skill`): `Software, CI4AI, AI4CI, Foundation-AI, PADI,
   Visual-Analytics, Digital-Agriculture, Animal-Ecology, Smart-Foodsheds,
   Food-Access`. Don't invent tags — ask if unclear.

3. **Run the parser** from `my-website/`, pointing output at `docs`.

   **First, ensure the venv is ready (do this every run — it's idempotent).** Run
   `uv sync` against the root project; it creates the repo-root `.venv` if absent and
   installs/refreshes deps from `uv.lock`. You don't need to *activate* it — invoking
   `../.venv/bin/python` uses that environment directly:
   ```bash
   # from my-website/ — provision/refresh the repo-root .venv from the root project
   [ -x ../.venv/bin/python ] || uv sync --project ..   # create if missing
   uv sync --project ..                                 # refresh deps (fast no-op if current)
   ```
   (Equivalently, `uv sync` run from the repo root.) Only after this should you run
   the parser.

   Single repo:
   ```bash
   ../.venv/bin/python ../.claude/skills/icicle-tc-deploy-doc/readme_parser.py \
     --repo_link "https://github.com/ICICLE-ai/<Repo>" \
     --project_name "<Component>" \
     --tags CI4AI Smart-Foodsheds \
     --release 2026-05 \
     --output_folder docs
   ```

   CSV batch (release-testing catalog — lives in the repo root):
   ```bash
   ../.venv/bin/python ../.claude/skills/icicle-tc-deploy-doc/readme_parser.py \
     --csv_file "../Release Testing(2026-05).csv" \
     --release 2026-05 \
     --output_folder docs
   ```

   Excel batch:
   ```bash
   ../.venv/bin/python ../.claude/skills/icicle-tc-deploy-doc/readme_parser.py \
     --excel_file "<path/to/components.xlsx>" \
     --release 2026-05 \
     --output_folder docs
   ```
   (In batch mode do **not** pass `--tags` — tags come from the table's Tags column.
   Omit `--release` to take the per-row `Release Dates` column instead.)

4. **Sanity-check the output.** Open the generated `docs/<Component>/<Component>.md`
   and confirm: frontmatter tags look right (old + new merged); the badge block is a
   center-aligned `<div align="center">` after the description holding the **GitHub**
   badge then the **License** badge; the raw `## License` section / `License:` text is
   gone from the body; images point at `raw.githubusercontent.com` and other links at
   `github.com/.../blob/...`. Verify `_category_.json` exists. If the component has API
   docs (`api-docs/<Component>/`), confirm the `:::tip API reference` callout links to
   `/api/<Component>/<info-id>`.

5. **Build the site** from `my-website/`:
   ```bash
   npm install        # first run only
   npm run build
   ```

   **Secrets for a local verification build.** `docusaurus.config.js` enables the
   `@dipakparmar/docusaurus-plugin-umami` analytics plugin, whose `websiteID`,
   `analyticsDomain`, and `dataHostURL` are **required** and read from env vars. CI
   sets the real values; locally they're unset, so a bare `npm run build` aborts
   config validation with `"websiteID" is required` *before any doc is processed*.
   This is unrelated to the docs. Do **not** edit the analytics config to work
   around it — instead pass throwaway placeholder values for this verification build
   only (they are never committed and the real secrets live in CI):
   ```bash
   UMAMI_WEBSITE_ID=local-verify \
   UMAMI_ANALYTICS_DOMAIN=example.com \
   UMAMI_DATA_HOST_URL=https://example.com \
   UMAMI_DATA_DOMAINS=example.com \
   npm run build
   ```
   More generally: if the build fails a config/plugin validation purely for a
   missing secret env var (not a doc/MDX error), supply a dummy value for that var
   and rebuild — never weaken or remove the plugin config to make the build pass.

6. **Fix any build errors and rebuild until clean.** The build is the gate — your
   job is done only when `npm run build` finishes with no errors. Common causes:
   - **MDX compile errors** from raw `<...>` in the README being read as JSX, or
     literal `{`/`}`. Fix by escaping or fencing the offending snippet in the
     generated `.md` (edit narrowly; don't rewrite the file).
   - **Broken-link / broken-anchor warnings** are set to `warn` in
     `docusaurus.config.js` and won't fail the build, but fix obviously wrong ones.
   - **Missing `_category_.json`** or an empty component folder — re-run the parser.

   Re-run `npm run build` after each fix. Done when it exits 0 with no errors.

7. **Report** the component(s) added/updated and confirm the clean build. Do not
   commit, push, or deploy unless the user explicitly asks — pushing to
   `docusaurus-demo` triggers the GitHub Pages deploy workflow.

## Parser reference (flags)

| Flag | Meaning |
|------|---------|
| `--repo_link` | GitHub repo / blob / raw README URL (single mode) |
| `--project_name` | Folder + main filename; derived from URL if omitted |
| `--excel_file` | Batch mode (Excel); columns README, Tags*, optional Component, Release Dates |
| `--csv_file` | Batch mode (CSV); same columns as `--excel_file` |
| `--tags` | Base tags (single mode only) |
| `--release` | `YYYY-MM`; added as `Release <value>` to main file(s); overrides per-row Release in batch |
| `--output_folder` | Output root — use `docs` from `my-website/` |
| `--only` | Batch mode: process only the row(s) whose Component matches (case-insensitive, **comma-separated**) — targeted subset update |
| `--api_docs_dir` | API-docs root for cross-linking; defaults to the `api-docs` sibling of `--output_folder` |
| `--github_pat` | GitHub token (overrides `GITHUB_PAT` env var) |
