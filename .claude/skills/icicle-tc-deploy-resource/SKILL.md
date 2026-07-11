---
name: icicle-tc-deploy-resource
disable-model-invocation: true
description: Add or update a resource link in the training-catalog Resources page (my-website/other_resources/0_intro.md). Accepts a CSV with a Resource Link column, or a single name/link, verifies the link resolves, then inserts it at the correct alphabetical position — either as a new top-level `## <name>` product block or as a bold-bullet sub-entry inside an existing container section such as "TACC and Tapis Resources". Idempotent: re-running replaces the existing entry in place rather than duplicating it. Never invents a version number. Reads the release-testing catalog CSV (Component, Resource Link, Tags, Release Dates columns; only rows with a Resource Link produce entries). Use when the user asks to add or update a resource/link on the catalog's Resources tab. This skill only makes sense inside the training-catalog repo.
---

# ICICLE Training-Catalog — Resource Listing Deploy

Adds a resource link to this repo's Resources page
(`my-website/other_resources/0_intro.md`), keeping the page's alphabetical order
and its two entry conventions, then verifies the site builds.

The helper that does the mechanics — `resource_parser.py` — lives **next to this
file** (`.claude/skills/icicle-tc-deploy-resource/resource_parser.py`). It is
**standard-library only**, so run it with plain `python3` (no venv). This skill's
job is to drive it correctly, supply a good description, and guarantee a clean
build.

## Scope

Run only inside the `training-catalog` repo — it edits
`my-website/other_resources/0_intro.md` and builds the Docusaurus site. If
`my-website/docusaurus.config.js` is not present, stop and tell the user this skill
must run from the catalog repo root. Run the parser from `my-website/` so the
default target path resolves.

## The page's two conventions (important)

`0_intro.md` starts with an H1 + intro sentence (the preamble), then a list of
level-2 `## ` sections **ordered alphabetically by name**. There are two entry
shapes:

- **Top-level product** — a `## <Name>` heading, then a `-` description bullet,
  then a raw `<a href="…" target="_blank" rel="noopener noreferrer">` block. Most
  entries are this shape. The version, if any, lives **in the heading text**
  (e.g. `## OpenPass v1.0.0`).
- **Container section sub-entry** — a few `## ` sections are *containers* that hold
  several **bold-named bullets**: `- **<Name>**`, an indented description, and an
  indented `<a href>` block. `## TACC and Tapis Resources` is the canonical one,
  and its bullets are themselves alphabetical.

The parser preserves both conventions and inserts at the right alphabetical slot.

## Steps

1. **Confirm location.** Ensure `my-website/docusaurus.config.js` exists. Run the
   parser from `my-website/`.

2. **Gather inputs.** Either a single resource or a batch CSV:
   - Single: the resource **name**, the **link**, and a one-sentence
     **description**. Optionally the container **section** to nest under and custom
     **link text**.
   - Batch: the release-testing catalog CSV. The parser reads (case-insensitive,
     prefix-matched): **Component** (the entry name), **Resource Link** *(required —
     rows without it are skipped)*, plus **Tags**/**Release Dates** (carried
     through, not currently rendered into the entry). Descriptions are **not** in
     the CSV — you supply one per row (see step 4).

   List the CSV rows that have a resource link:
   ```bash
   python3 ../.claude/skills/icicle-tc-deploy-resource/resource_parser.py \
     csv-rows --csv "../Release Testing(2026-07).csv"
   # targeted subset:
   #   ... csv-rows --csv "..." --only "FlexServe Inference, Smart Labeler"
   ```

3. **Verify the link resolves** before inserting (matches "check the link first"):
   ```bash
   python3 ../.claude/skills/icicle-tc-deploy-resource/resource_parser.py \
     check-link --url "<link>"
   ```
   Exit 0 + a `200`-ish status means good. A non-zero exit (dead host, or an HTTP
   ≥400) means **do not insert** — report it to the user and skip that entry.

4. **Write a description.** The CSV has no description column. Fetch the resource
   page (or read the component's README first section) and write **one factual
   sentence**. Do **not invent a version** — include a version in the name only if
   the source actually states one (e.g. don't append `v1.0` when the release sheet
   left Version blank).

5. **Decide placement.** Ask yourself (or the user if genuinely ambiguous):
   - Is this a Tapis/TACC-hosted tool or account resource? → nest under the
     existing `## TACC and Tapis Resources` container with `--section`.
   - Otherwise → a new **top-level** `## <Name>` product block (omit `--section`).

   Insert (idempotent — safe to re-run):
   ```bash
   # new top-level product block:
   python3 ../.claude/skills/icicle-tc-deploy-resource/resource_parser.py \
     insert --name "<Name>" --link "<link>" --description "<one sentence>"

   # bold-bullet inside a container section:
   python3 ../.claude/skills/icicle-tc-deploy-resource/resource_parser.py \
     insert --name "<Name>" --link "<link>" --description "<one sentence>" \
     --section "TACC and Tapis Resources"
   ```
   Optional: `--link-text "<anchor text>"` (defaults to `Link to <Name>`) and
   `--file <path>` (defaults to `other_resources/0_intro.md`).

6. **Sanity-check** the edit: the entry landed in the correct alphabetical position,
   the `<a href>` block is well-formed, and (on an update) the old entry was
   **replaced, not duplicated**.

7. **Build the site** from `my-website/` and fix any errors (this is a Markdown
   file, so failures are rare, but the build is still the gate):
   ```bash
   UMAMI_WEBSITE_ID=local-verify \
   UMAMI_ANALYTICS_DOMAIN=example.com \
   UMAMI_DATA_HOST_URL=https://example.com \
   UMAMI_DATA_DOMAINS=example.com \
   npm run build
   ```
   (These are throwaway placeholders for the required analytics env vars; the real
   secrets live in CI. Never edit the analytics config to dodge the missing-secret
   error.)

8. **Report** the entry added/updated and confirm the clean build. Do not commit,
   push, or deploy unless the user explicitly asks — pushing to `docusaurus-demo`
   triggers the live GitHub Pages deploy.

## Parser reference (subcommands)

| Subcommand | Purpose |
|------------|---------|
| `csv-rows --csv <path> [--only <names>]` | Emit resource-link rows (name/link/tags/release) as JSON; skips rows with no Resource Link. `--only` is comma-separated, case-insensitive. |
| `check-link --url <url> [--timeout <s>]` | Verify a URL resolves (follows redirects). Exit 0 when reachable; non-zero on a dead host or HTTP ≥400. |
| `insert --name <n> --link <url> --description <text> [--section <heading>] [--link-text <text>] [--file <path>]` | Insert/replace an entry at its alphabetical slot. With `--section`, nests as a bold bullet inside that container section; without it, adds a top-level `## <name>` block. Idempotent on name. |
