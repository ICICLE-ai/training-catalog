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

### Update-in-place, never destroy (important)

`save_file` is additive on metadata:

- **Tags merge.** Existing frontmatter tags in a file are read first, then new tags
  are appended and de-duplicated (first-seen order kept). Re-running with a new
  `--release` therefore *adds* `Release 2026-05` while keeping `Release 2025-07`.
- **Body content is refreshed** from the current README (so content edits flow
  through), while stray inline `tags:` lines are stripped and top badges are moved
  below the description.

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

```bash
pip install requests pandas openpyxl     # openpyxl only needed for Excel batch mode
```

For private repos, export a token first so the README fetch is authorized:

```bash
export GITHUB_PAT=<token>                 # or pass --github_pat
```

## Steps

1. **Confirm location.** Ensure `my-website/docusaurus.config.js` exists. All
   commands below run from the `my-website/` directory so output lands in
   `my-website/docs/`.

2. **Gather inputs from the user.** You need either a single repo or a batch file:
   - Single: the GitHub repo URL (root, `/blob/.../README.md`, or raw README URL).
     Optionally a component/folder name, one or more tags, and a release `YYYY-MM`.
   - Batch: an Excel file with required columns **README** and **Tags**
     (comma-separated), optional **Component**; `--release` applies to every row.

   If the user gives tags, they should come from the canonical ICICLE tag list
   (see the `icicle-readme-skill`): `Software, CI4AI, AI4CI, Foundation-AI, PADI,
   Visual-Analytics, Digital-Agriculture, Animal-Ecology, Smart-Foodsheds,
   Food-Access`. Don't invent tags — ask if unclear.

3. **Run the parser** from `my-website/`, pointing output at `docs`:

   Single repo:
   ```bash
   python3 ../.claude/skills/icicle-tc-deploy-doc/readme_parser.py \
     --repo_link "https://github.com/ICICLE-ai/<Repo>" \
     --project_name "<Component>" \
     --tags CI4AI Smart-Foodsheds \
     --release 2026-05 \
     --output_folder docs
   ```

   Excel batch:
   ```bash
   python3 ../.claude/skills/icicle-tc-deploy-doc/readme_parser.py \
     --excel_file "<path/to/components.xlsx>" \
     --release 2026-05 \
     --output_folder docs
   ```
   (In Excel mode do **not** pass `--tags` — tags come from the sheet.)

4. **Sanity-check the output.** Open the generated `docs/<Component>/<Component>.md`
   and confirm: frontmatter tags look right (old + new merged), the GitHub repo
   badge is present, images point at `raw.githubusercontent.com`, and other links
   point at `github.com/.../blob/...`. Verify `_category_.json` exists.

5. **Build the site** from `my-website/`:
   ```bash
   npm install        # first run only
   npm run build
   ```

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
| `--excel_file` | Batch mode; columns README, Tags, optional Component |
| `--tags` | Base tags (single mode only) |
| `--release` | `YYYY-MM`; added as `Release <value>` to main file(s) |
| `--output_folder` | Output root — use `docs` from `my-website/` |
| `--github_pat` | GitHub token (overrides `GITHUB_PAT` env var) |
