---
name: icicle-readme-skill
description: Scaffold or restructure the top-level README.md for an ICICLE component repository so it matches the canonical ICICLE README template (project description + tag + license + references + acknowledgements + issue reporting, then Tutorials / How-To Guides / Explanation sections separated by `---` delimiters, following the Diátaxis framework). Use this whenever the user asks to write, scaffold, or fix a README for an ICICLE component, mentions the ICICLE README template, or asks for the Diátaxis Tutorials/How-To/Explanation layout. ONLY apply this skill when the target repo is under https://github.com/ICICLE-ai/ — for any other repo, confirm with the user first before applying.
---

# ICICLE README Skill

This skill produces a single `README.md` for an ICICLE component repository, matching the canonical template that ICICLE projects follow. It is *not* a Docusaurus per-folder layout — it is one Markdown file that lives at the root of the component's GitHub repo.

## Scope guard — when this skill applies

**Apply automatically only if the target repo is under `https://github.com/ICICLE-ai/`.**

Before generating or editing a README with this template, verify the repo origin. Any of the following counts as confirmation that you are inside an ICICLE-ai repo:

- `git remote -v` shows a remote URL containing `github.com/ICICLE-ai/` or `github.com:ICICLE-ai/`.
- The repo is a fresh checkout/working copy of an ICICLE-ai repo.
- The user explicitly states the project is or will be hosted under `ICICLE-ai`.

**If none of those are true, stop and ask the user to confirm** that this template is the right one to apply, e.g.: "This skill is intended for repos under github.com/ICICLE-ai. The current repo is `<origin>` — do you still want me to apply the ICICLE README template?" Only proceed after explicit confirmation.

## Required structure

The output README **must** contain, in order:

1. `# {{ProjectName}}` — H1 title.
2. A short project description (1–3 sentences).
3. **At least one tag** chosen from the canonical list below.
4. (Optional) Diátaxis reference link.
5. `### License` — license badge or text.
6. `## References` — links and definitions.
7. `## Acknowledgements` — **must** include the ICICLE NSF acknowledgement line verbatim (see below). Other funding sources go above it.
8. `## Issue reporting` — how users report issues (GitHub Issues URL, support email, etc.).
9. A `---` horizontal-rule delimiter.
10. **At least one** of `# Tutorials`, `# How-To Guides`, `# Explanation`. Including all three is preferred but not mandatory; if the user only has material for one or two, include only those. Each included section is separated from the next by a `---` delimiter.

### Canonical tag list (pick at least one)

```
Software
CI4AI
AI4CI
Foundation-AI
PADI
Visual-Analytics
Digital-Agriculture
Animal-Ecology
Smart-Foodsheds
Food-Access
```

If the user's content does not clearly match any tag, ask which tag(s) to use — do not guess.

### Required acknowledgement (verbatim, do not paraphrase)

> *National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

This line is non-negotiable and must appear in every generated README, even if no other funding sources are listed. The OAC number `2112606` must be present exactly.

### Section delimiters

Between the top metadata block (description / license / references / acknowledgements / issue reporting) and the Diátaxis sections, and **between every Diátaxis section that is included**, insert a Markdown horizontal-rule line:

```
---
```

The `---` lines render as visual dividers in GitHub and other Markdown viewers and match the canonical template.

## Steps

1. **Check the repo origin** (see the scope guard above). If the repo is not under `github.com/ICICLE-ai/`, ask the user to confirm before continuing.
2. **Gather inputs** from the user or from existing repo content:
   - Project name (used in the H1).
   - Short description (1–3 sentences).
   - At least one tag from the canonical list.
   - License (name + URL).
   - References / external links.
   - Other funding sources (optional).
   - Issue-reporting channel (URL or email).
   - Which Diátaxis sections will be included (Tutorials / How-To / Explanation — at least one).
3. **Copy** `templates/README.md` to the repo root as `README.md` (or merge into an existing README).
4. **Replace** every `{{PLACEHOLDER}}` token with the gathered content.
5. **Drop** any Diátaxis section the user has no content for. Keep the `---` delimiters between the sections that remain. Do *not* leave empty section bodies.
6. **Verify** before finishing:
   - At least one canonical tag is present.
   - The exact ICICLE NSF acknowledgement line (with `OAC 2112606`) is present.
   - At least one of `# Tutorials`, `# How-To Guides`, `# Explanation` is present.
   - `---` delimiters separate each top-level section after the metadata block.

## Cross-platform usage

The skill is plain Markdown plus a single template file, so it works in:

- **Claude Code** — auto-discovered via the YAML frontmatter on this `SKILL.md`.
- **Cursor / Continue / Windsurf / Copilot Chat** — point the assistant at the `icicle-readme-skill/` folder and ask it to scaffold or fix a README.
- **Manual authoring** — open `templates/README.md`, copy it, and replace placeholders by hand.

## Template

See [`templates/README.md`](templates/README.md) for the file to copy and fill in.
