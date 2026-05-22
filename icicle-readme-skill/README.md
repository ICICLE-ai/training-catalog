# icicle-readme-skill

A reusable skill that scaffolds the top-level `README.md` for an ICICLE component repository, matching the canonical ICICLE README template.

The structure follows the [Diátaxis](https://diataxis.fr/) framework: a metadata block (description, tag, license, references, acknowledgements, issue reporting) followed by Tutorials / How-To Guides / Explanation, separated by `---` delimiters.

## Scope & the non-ICICLE confirmation gate

**This skill applies automatically only when the target repository is under [`https://github.com/ICICLE-ai/`](https://github.com/ICICLE-ai/).**

For any **other** repo, the assistant runs a confirmation gate before writing anything and asks three things:

1. **Template** — do you want the ICICLE-standard README template applied at all? (If not, it stops.)
2. **Tags** — do you want the canonical ICICLE tags, or your own / none? (For non-ICICLE repos the canonical-tag requirement is waived per your answer.)
3. **Acknowledgement** — a heads-up that, because you're using the ICICLE README skill, the ICICLE NSF/AI acknowledgement line will be added to the Acknowledgements section.

The full gate is documented in [`SKILL.md`](SKILL.md).

## Metadata & the training-catalog pipeline

The README this skill produces is the upstream **metadata source** for the ICICLE training-catalog. The same canonical tags, license badge, and acknowledgement live here so that when the component is deployed, the catalog's `icicle-tc-deploy-doc` parser can lift the tag(s) into the doc's frontmatter (and add a `Release <YYYY-MM>` tag). Declaring canonical tags here keeps the README and the catalog in sync.

## Hard requirements the skill enforces

Every generated README will contain:

- **At least one tag** from the canonical list — one of:
  `Software`, `CI4AI`, `AI4CI`, `Foundation-AI`, `PADI`, `Visual-Analytics`, `Digital-Agriculture`, `Animal-Ecology`, `Smart-Foodsheds`, `Food-Access`.
  *(Required for ICICLE-ai repos; for non-ICICLE repos only if you opt in at the gate.)*
- **The ICICLE acknowledgement line, verbatim**, including the OAC number — added for every repo, ICICLE or not:
  > *National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*
- **At least one** of `# Tutorials`, `# How-To Guides`, or `# Explanation` — having all three is preferred but not mandatory.
- **`---` delimiters** between the metadata block and each included Diátaxis section.

## How to use it

### With Claude Code

The skill is auto-discovered via the YAML frontmatter on `SKILL.md`. Inside an ICICLE-ai repo, ask:

> "Use the icicle-readme-skill to scaffold the README for this component."

If the repo is not under `ICICLE-ai/`, the assistant will confirm with you before applying the template.

### With Cursor / Continue / Windsurf / Copilot Chat

Open this folder in the assistant's context (or paste `SKILL.md` plus `templates/README.md`), then ask the assistant to scaffold or fix a README using the template.

### Manually

1. Copy [`templates/README.md`](templates/README.md) to the root of your component repo.
2. Replace every `{{PLACEHOLDER}}` token.
3. Drop the Diátaxis sections you don't have material for, but keep at least one of Tutorials / How-To / Explanation.
4. Confirm the canonical tag, the verbatim acknowledgement line, and the `---` delimiters are all present.

## Files in this skill

- [`SKILL.md`](SKILL.md) — skill definition (frontmatter, scope guard, hard requirements, steps).
- [`templates/README.md`](templates/README.md) — the README template to copy and fill in.
