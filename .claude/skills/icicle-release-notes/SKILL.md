---
name: icicle-release-notes
disable-model-invocation: true
description: Draft the public ICICLE release-notes announcement for a given YYYY-MM release, from ICICLE-Release-Template.md plus the component catalog and the deployed training-catalog docs. Splits components into "New to ICICLE CI Catalog" (first ICICLE release) and "NSF ICICLE CI Components Changelog" (version upgrades / changes to components shipped in an earlier release), groups both by primaryThrust under the template's Intelligent Cyberinfrastructure and Use Inspired Science headings, renders each entry as a bolded name+version linked to its GitHub or Hugging Face source with an indented description, and writes ICICLE-Release-YYYY-MM.md at the repo root. Reads name/version/thrust/description/sourceCodeUrl from the component catalog entries and decides new-vs-changelog from prior `Release YYYY-MM` tags in the deployed docs. Use when the user asks to write, draft, or regenerate ICICLE release notes or a release announcement. Only makes sense inside the training-catalog repo.
---

# ICICLE Release Notes

Generates the public-facing release announcement for one ICICLE release.

**This is a sub-skill of `icicle-release`** — its final step, after the human gates.
It describes what was published, so everything it needs already exists by the time it
runs: the docs are deployed (`icicle-tc-deploy-doc`), the READMEs validated
(`icicle-readme-skill`), and the catalog entries appended from each component's
`component-info.yaml` (`icicle-component-info-skill`). It **re-derives nothing** —
name, version, description and source URL come straight from the catalog entries those
steps produced, and the new-vs-changelog split comes from the release tags the doc
parser merged. Running it standalone is fine too, as long as that release has already
been deployed.

## Scope

- Run only inside `training-catalog` (guard on `my-website/docusaurus.config.js`).
- **Read-only with respect to the release.** It never edits docs, the catalog, or
  `docusaurus.config.js`. Its only output is one Markdown file at the repo root.
- Output: `ICICLE-Release-<YYYY-MM>.md`. Gitignored — these drafts are reviewed and
  published elsewhere (website, mailing list), not committed to this repo.
- The template `ICICLE-Release-Template.md` is also gitignored.

## Inputs

| Input | Where from | Used for |
|-------|-----------|----------|
| Release `YYYY-MM` | ask the user, or the `icicle-release` run dir | title, tag link, which components |
| `ICICLE-Release-Template.md` | repo root | headings, preamble, footer boilerplate |
| `release_catalog.yml` | the `CI-Components-Catalog` clone | name, componentVersion, primaryThrust, description, sourceCodeUrl |
| `my-website/docs/<Component>/` | this repo | prior `Release` tags → new vs changelog |

If the template is missing, stop and say so — do not invent the boilerplate.

## The two sections

**`# New to ICICLE CI Catalog`** — components appearing in an ICICLE release for the
first time.

**`# NSF ICICLE CI Components Changelog`** — components that shipped in an earlier
release and are being updated (new version, new features, fixes).

### How to decide which

Use the **prior release tags on the deployed doc**, not the catalog id:

```
docs/<Component>/<Component>.md frontmatter tags
  contains a `Release <YYYY-MM>` other than this release  →  Changelog
  contains only this release's tag                        →  New
```

Catalog ids are **not** a reliable signal — a component can be re-ided between
releases (e.g. `PatraKnowledgeBase:1.0.0` → `PatraAICardsKnowledgeBase:1.0.0`) and
would look new when it is not. The doc's accumulated release tags survive renames
because `readme_parser.py` merges them.

**Both sections use the same heading/subheading structure** — the thrust groupings
below apply identically to each.

## Thrust → heading map

`primaryThrust` from the component's catalog entry decides placement:

| `primaryThrust` | Section | Subheading |
|---|---|---|
| `core/CI4AI` | Intelligent Cyberinfrastructure | `### CI-for-AI` |
| `core/AI4CI` | Intelligent Cyberinfrastructure | `### AI-for-CI` |
| `core/Software` | Intelligent Cyberinfrastructure | `### Software Architecture and Design` |
| `core/FoundationAI` | Intelligent Cyberinfrastructure | `### AI Foundations` |
| `useInspired/SF` | Use Inspired Science | `### Smart Foodsheds` |
| `useInspired/AE` | Use Inspired Science | `### Animal Ecology` |
| `useInspired/DA` | Use Inspired Science | `### Digital Agriculture` |

### Retired thrusts — `core/PADI` and `core/VA`

**Nothing is released under PADI or VA any more**, and the template has no heading for
either. A component still carrying one as its `primaryThrust` always carries at least
one other canonical tag, and **that tag decides its category.** Fall back to the
component's canonical README tags (read from the deployed doc's frontmatter), taking
the first in template order:

| Tag | Subheading |
|---|---|
| `CI4AI` | CI-for-AI |
| `AI4CI` | AI-for-CI |
| `Software` | Software Architecture and Design |
| `Foundation-AI` | AI Foundations |
| `Smart-Foodsheds` | Smart Foodsheds |
| `Animal-Ecology` | Animal Ecology |
| `Digital-Agriculture` | Digital Agriculture |

So `core/PADI` + tags `[CI4AI, PADI]` → **CI-for-AI**; `core/VA` + tags
`[Visual-Analytics, Digital-Agriculture]` → **Digital Agriculture**. `collect` prints a
`WHY` column recording which thrust or tag decided each placement, so the fallback is
auditable. The same fallback covers any thrust missing from the map.

Only if a component has neither a live thrust nor a mappable tag does `collect` stop
and ask — that shouldn't happen, and means the upstream tags need fixing.

The template lists `### Software Architecture and Design` **twice** under Intelligent
Cyberinfrastructure; the renderer emits it once.

**Omit any subheading with no components.** Do not emit empty headings.

## Entry format

Exactly as the template:

```markdown
- [**<name> v<componentVersion>**](<sourceCodeUrl>)
    - <description>
```

- **Name and version come from the component's catalog entry** (`name`,
  `componentVersion`) — never from the CSV or the folder name, which drift.
- Prefix the version with `v`. If `componentVersion` already starts with `v`, don't
  double it.
- **Link target is `sourceCodeUrl`** — GitHub for most components, **Hugging Face**
  for HF-hosted ones (e.g. `https://huggingface.co/ICICLE-AI/yield-estimation`).
  Use whatever the catalog entry carries; do not rewrite one host into the other.
- The description is the catalog entry's `description`, collapsed to a single line.
  Keep it as written — this is the maintainer's own copy.
- Indent the description bullet **4 spaces** to match the template.

## Placeholder substitutions

Replace every `YYYY-MM` in the template with the release month, including:

- the `# ICICLE Release YYYY-MM` title
- `***YYYY-MM** release of ICICLE CI components`
- the training-catalog tag link:
  `https://icicle-ai.github.io/training-catalog/docs/tags/release-<YYYY-MM>`

Leave the preamble, mailing-list paragraphs, and `# Acknowledgements` **verbatim**.
The NSF acknowledgement is non-negotiable, exactly as in the template.

## Helper: `release_notes.py`

Bundled next to this file, **standard library only** (plain `python3`, no venv). Run
from the repo root:

```bash
P=.claude/skills/icicle-release-notes/release_notes.py

# 1. Collect: classify components and pull their catalog fields
python3 $P collect --release 2026-08 \
  --catalog ../CI-Components-Catalog/release_catalog.yml \
  --docs my-website/docs \
  --out .release-run/2026-08/notes.json

# 2. Render: fill the template
python3 $P render --data .release-run/2026-08/notes.json \
  --template ICICLE-Release-Template.md \
  --out ICICLE-Release-2026-08.md
```

`collect` prints a per-component classification table so the split can be eyeballed
before rendering. It reads `release_catalog.yml` with a line-based parser (the file
is uniformly indented `  - id:` / `    key: value`); if that file's formatting ever
changes, use the catalog repo's own `catalog_parser.py` instead.

## Steps

1. **Confirm the release `YYYY-MM`.**
2. **Locate the catalog clone.** Same rule as `icicle-release`: find a local
   `CI-Components-Catalog` checkout; if absent, ask. Don't guess.
3. **`collect`** — review the printed new/changelog split. Any component whose
   `primaryThrust` is `core/PADI` or `core/VA` stops here for a heading decision.
4. **`render`** — writes `ICICLE-Release-<YYYY-MM>.md`.
5. **Read the output back** and check: no `YYYY-MM` placeholders survive, no empty
   subheadings, every entry has a resolving link, and no component in the release is
   missing from either section.
6. **Report** the counts per section and per thrust, and list anything skipped.

## Guardrails

- **Never invent a version or a description.** Both come from the catalog entry. If a
  component has no entry, report it as missing rather than writing a placeholder.
- **Never commit or push.** The output is gitignored and meant for review.
- A component deployed to docs but absent from `release_catalog.yml` is a **release
  bug** — surface it; it means the catalog append was skipped.
