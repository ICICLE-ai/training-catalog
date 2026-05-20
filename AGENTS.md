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
| `.claude/skills/` | Project-local skills (auto-discovered by Claude in this repo) |
| `icicle-readme-skill/` | Generic, distributable README skill (installed globally) |
| `.github/workflows/deploy.yml` | CI: builds and deploys to GitHub Pages on push to `docusaurus-demo` |

## Tooling & commands

Node `>=18`, npm. From `my-website/`:

```bash
npm install            # install deps (first run)
npm run start          # local dev server
npm run build          # production build — the gate for "done"; must exit clean
npm run serve          # serve the production build locally
npx docusaurus gen-api-docs <id> --clean   # generate OpenAPI docs for a spec
npx docusaurus clean-api-docs <id>          # remove generated OpenAPI docs for a spec
```

Python (for the README parser): `pip install requests pandas openpyxl`. Set
`GITHUB_PAT` to fetch READMEs from private repos.

`onBrokenLinks` / `onBrokenMarkdownLinks` are set to `warn`, so link problems don't
fail the build — but MDX compile errors do.

## Skills

Three skills support this repo. All are **user-invoked** (`disable-model-invocation:
true`) — run them when the user asks, not automatically.

### `.claude/skills/icicle-tc-deploy-doc` — Component docs deploy
Fetches a component's GitHub README, runs the bundled `readme_parser.py` to split it
into Docusaurus docs under `my-website/docs/<Component>/`, merges (never wipes) tags
and content, rewrites relative images→`raw.githubusercontent.com` and other relative
links→`github.com/.../blob/...`, then builds and fixes errors. The parser
(`readme_parser.py`) is bundled inside this skill folder. See its `SKILL.md`.

### `.claude/skills/icicle-tc-deploy-api` — API docs deploy
Takes a CSV of GitHub OpenAPI-spec links (with a `tags` column), a single spec link,
or a local spec file; stages the JSON under `api_config_files/`, wires a
`docusaurus-plugin-openapi-docs` config entry, runs `gen-api-docs`, injects the tag
list into every generated `*.api.mdx` (gen-api-docs omits tags), then builds and
fixes errors. GitHub sources get a Title-Cased repo-name folder. See its `SKILL.md`.

### `icicle-readme-skill` — Generic ICICLE README scaffolder
Scaffolds/updates a single top-level `README.md` for any `github.com/ICICLE-ai/`
component repo (Diátaxis: description + tags + license + acknowledgements, then
Tutorials / How-To / Explanation). Generic and repo-agnostic, so it's kept here as a
distributable folder and installed globally (`~/.claude/skills/`) rather than living
under `.claude/skills/`. See `icicle-readme-skill/SKILL.md`.

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
  rather than deleting it — tags accumulate and content refreshes in place.
- Edit generated files narrowly; don't reformat unrelated content.
- **Do not commit, push, or deploy unless the user explicitly asks.** A push to
  `docusaurus-demo` triggers the live GitHub Pages deploy.
