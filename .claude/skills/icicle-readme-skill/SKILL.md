---
name: icicle-readme-skill
disable-model-invocation: true
description: Scaffold or restructure the top-level README.md for an ICICLE component repository so it matches the canonical ICICLE README template (project description + tags + license + references + acknowledgements + issue reporting, then Tutorials / How-To Guides / Explanation sections separated by `---` delimiters, following the Diátaxis framework). The README it produces carries the metadata the ICICLE training-catalog deploy pipeline consumes (canonical tags, license badge, NSF acknowledgement). Use this whenever the user asks to write, scaffold, or fix a README for an ICICLE component, mentions the ICICLE README template, or asks for the Diátaxis Tutorials/How-To/Explanation layout. ONLY apply this skill automatically when the target repo is under https://github.com/ICICLE-ai/. For any other repo, run the confirmation gate first: confirm they want the ICICLE-standard template at all, confirm whether they want the canonical ICICLE tags, and tell them the ICICLE NSF/AI acknowledgement line will be added because they are using this skill.
---

# ICICLE README Skill

This skill produces a single `README.md` for an ICICLE component repository, matching the canonical template that ICICLE projects follow. It is *not* a Docusaurus per-folder layout — it is one Markdown file that lives at the root of the component's GitHub repo.

## Confirmation gate — when this skill applies

**Apply automatically only if the target repo is under `https://github.com/ICICLE-ai/`.**

Before generating or editing a README, verify the repo origin. Any of the following counts as confirmation that you are inside an ICICLE-ai repo, and you may proceed without prompting:

- `git remote -v` shows a remote URL containing `github.com/ICICLE-ai/` or `github.com:ICICLE-ai/`.
- The repo is a fresh checkout/working copy of an ICICLE-ai repo.
- The user explicitly states the project is or will be hosted under `ICICLE-ai`.

### Non-ICICLE repos — confirm three things before doing anything

If none of the above are true, **stop and run this confirmation gate before writing or editing any README.** Ask all three together (one prompt is fine) and only proceed after the user answers:

1. **Template — confirm they want the ICICLE standard at all.**
   > "This skill builds a README to the ICICLE-ai standard (Diátaxis layout + ICICLE metadata). The current repo is `<origin>`, which is not under github.com/ICICLE-ai. Do you still want me to apply the ICICLE README template here?"
   If they decline, stop — don't write anything.

2. **Tags — confirm whether they want the canonical ICICLE tags.**
   > "Do you want the canonical ICICLE tags (e.g. Software, CI4AI, Smart-Foodsheds…) on this README, or should I leave the `**Tags:**` line out / use your own tags?"
   - If **yes**: include at least one tag from the canonical list (ask which if unclear), exactly as for an ICICLE repo.
   - If **no / their own**: drop the `**Tags:**` line or use the tag(s) they supply verbatim. For a non-ICICLE repo the canonical-tag hard requirement is **waived** based on this answer.

3. **Acknowledgement — tell them it will be added (this is a notice, not a question).**
   > "Heads up: because you're using the ICICLE README skill, the ICICLE NSF acknowledgement line will be added to the Acknowledgements section. You can keep your own funding sources above it."
   The acknowledgement line is part of this skill's identity and is **always** added when the skill runs — for ICICLE and non-ICICLE repos alike. Don't make it optional; just make sure a non-ICICLE user is told before you write it.

For an ICICLE-ai repo, all three are implied: canonical tags apply, the acknowledgement is mandatory, no gate is needed.

## Required structure

The output README **must** contain, in order:

1. `# {{ProjectName}}` — H1 title.
2. A short project description (1–3 sentences).
3. **At least one tag** chosen from the canonical list below. *(Mandatory for ICICLE-ai repos. For a non-ICICLE repo this is governed by the confirmation gate — required only if the user opted into canonical tags; otherwise omit the line or use their tags.)*
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

These are the same tags the **training-catalog deploy pipeline** keys on. This README is upstream metadata: when a component is deployed into the catalog, the `icicle-tc-deploy-doc` parser pulls the chosen tag(s) into the doc's YAML frontmatter (and adds a `Release <YYYY-MM>` tag at deploy time). Declaring a canonical tag here keeps the README and the catalog in sync; invented tags don't map and will be dropped.

### Required acknowledgement (verbatim, do not paraphrase)

> *National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*

This line is non-negotiable and must appear in every generated README, even if no other funding sources are listed. The OAC number `2112606` must be present exactly.

### Section delimiters

Between the top metadata block (description / license / references / acknowledgements / issue reporting) and the Diátaxis sections, and **between every Diátaxis section that is included**, insert a Markdown horizontal-rule line:

```
---
```

The `---` lines render as visual dividers in GitHub and other Markdown viewers and match the canonical template.

## Operating modes

The skill has two modes. **Detect which one applies before doing anything else** by checking whether `README.md` exists at the repo root.

### Mode A — Scaffold (no README, or empty README)

Used when the repo has no `README.md`, or only a placeholder (e.g. just `# project-name`). Generate a fresh README from `templates/README.md`.

### Mode B — Update in place (README exists with real content)

Used when a real `README.md` already exists. **Do not regenerate the whole file.** The user may have added custom content over time — extra subsections, prose, badges, links, formatting tweaks — and rewriting from the template would silently destroy it.

Update rules:

1. **Read the existing `README.md` first** with the Read tool, in full.
2. **Identify only the sections that need to change** based on the user's stated intent and any recent code/content changes (e.g., new tutorial, license change, new contact, added dependency in a how-to). If the user did not say what changed, ask before editing.
3. **Edit narrowly** with the Edit tool — change only the affected text inside the affected sections. Do not touch unrelated sections.
4. **Preserve everything the user added**: custom H2/H3 subsections, extra prose, additional badges, extra links, reordered content within a section, formatting choices. The template is a *scaffold*, not a style guide to enforce retroactively.
5. **Add missing required pieces only.** If a hard requirement is missing (canonical tag, NSF acknowledgement line, at least one Diátaxis section, `---` delimiters), add only the minimum needed to satisfy the requirement — do not "tidy up" the rest of the file.
6. **Show a change summary before writing** when the edit touches more than one section: list the sections you intend to modify and what will change, and ask the user to confirm. For a single, obvious section edit, you can proceed without a confirmation prompt.

The template at `templates/README.md` is used in Mode B only as a reference for *missing* sections (e.g., if `## Acknowledgements` is absent and needs to be inserted). Do not pull placeholder text from the template into a section that already has real content.

## Steps

1. **Check the repo origin and run the confirmation gate** (see "Confirmation gate" above). If the repo is under `github.com/ICICLE-ai/`, proceed. If not, ask the three gate questions — (a) apply the ICICLE template at all? (b) canonical tags or not? (c) notice that the acknowledgement will be added — and only continue after the user answers (a). Carry their tag answer into steps 3 and 5.
2. **Detect the mode**: does `README.md` exist with real content? If yes → Mode B. If no or near-empty → Mode A.
3. **Gather inputs** from the user or from existing repo content. In Mode B, read first and only ask for what's actually missing or being changed.
   - Project name (used in the H1).
   - Short description (1–3 sentences).
   - Tag(s): at least one from the canonical list — required for ICICLE repos, and for non-ICICLE repos only if they opted in at the gate.
   - License (name + URL).
   - References / external links.
   - Other funding sources (optional; they go above the ICICLE acknowledgement line).
   - Issue-reporting channel (URL or email).
   - Which Diátaxis sections will be included (Tutorials / How-To / Explanation — at least one).
4. **Apply the mode**:
   - **Mode A**: copy `templates/README.md` to the repo root, replace every `{{PLACEHOLDER}}`, drop any Diátaxis section with no content.
   - **Mode B**: edit the existing file narrowly per the update rules above. Do not write a new file from the template.
5. **Verify the hard requirements** in the final file (in both modes):
   - At least one canonical tag is present — required for ICICLE repos; for non-ICICLE repos only if the user opted into canonical tags at the gate.
   - The exact ICICLE NSF acknowledgement line (with `OAC 2112606`) is present — always, including non-ICICLE repos.
   - At least one of `# Tutorials`, `# How-To Guides`, `# Explanation` is present.
   - `---` delimiters separate each top-level section after the metadata block.

   If any are missing in Mode B, add the minimum needed to satisfy them. Do not reformat existing content.

## Cross-platform usage

The skill is plain Markdown plus a single template file, so it works in:

- **Claude Code** — auto-discovered via the YAML frontmatter on this `SKILL.md`.
- **Cursor / Continue / Windsurf / Copilot Chat** — point the assistant at the `icicle-readme-skill/` folder and ask it to scaffold or fix a README.
- **Manual authoring** — open `templates/README.md`, copy it, and replace placeholders by hand.

## Template

See [`templates/README.md`](templates/README.md) for the file to copy and fill in.
