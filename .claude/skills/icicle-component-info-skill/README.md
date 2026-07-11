# icicle-component-info-skill

A reusable skill that scaffolds (or updates) the `component-info.yaml` catalog-metadata
file for an ICICLE component repository. It is the machine-facing sibling of
[`icicle-readme-skill`](../icicle-readme-skill): that skill writes the human-facing
`README.md`; this one writes the single-entry YAML the ICICLE **component catalog**
consumes.

## What it produces

One `component-info.yaml` at the component repo root — a single-item YAML list:

```yaml
- id: MyComponentName:0.1.0
  owner: Component Maintainer
  primaryThrust: core/CI4AI
  name: My Component Name
  status: BetaRelease
  description: One to three sentences on what the component does.
  componentVersion: 0.1.0
  targetIcicleRelease: "2026-05"
  hasDependentComponents:            # omit this key entirely if there are no dependencies
    - related_to: some-other-component:0.1.0
      relationship_type: DependsOn
  licenseUrl: https://github.com/ICICLE-ai/<repo>?tab=<LICENSE>-ov-file
  publicAccess: true
  sourceCodeUrl: https://github.com/ICICLE-ai/<repo>
  codeReviewConducted: true
  testsWritten: true
  developerDocumentationAvailable: true
  trainingTutorialsAvailable: true
  # trainingTutorialsUrl is filled in AFTER the training-catalog is deployed.
```

## Rules the skill enforces

- **`id` = `<name-without-spaces>:<componentVersion>`.** The version after the `:` must
  equal `componentVersion` exactly, and the prefix is `name` with spaces/punctuation
  stripped (`My Component Name` + `0.1.0` → `MyComponentName:0.1.0`).
  Bumping the version updates both in one edit.
- **`status`** is one of: `Unreleased`, `PrototypeRelease`, `AlphaRelease`,
  `BetaRelease`, `ProductionRelease`.
- **`primaryThrust`** is one of: `core/Software`, `core/CI4AI`, `core/AI4CI`,
  `core/FoundationAI`, `core/PADI`, `core/VA`, `useInspired/DA`, `useInspired/AE`,
  `useInspired/SF`.
- **`targetIcicleRelease`** is one of the official ICICLE release months from the
  `IcicleReleases` vocabulary — a quoted `YYYY-MM` value (e.g. `"2026-05"`) or `None` —
  asked for, never a guessed/invented month.
- **Existing files are never clobbered:** if a `component-info.yaml` *or* `component.yaml`
  already exists, the skill asks before updating it and edits it in place under its
  current name.
- **Version bumps are suggested, not silent:** when the version changes (or the repo's
  tags imply a newer one), the skill proposes the new `componentVersion`, asks you to
  confirm, and updates the `id` suffix in the same edit.
- **`licenseUrl`** is the GitHub license-tab URL
  (`…?tab=<LICENSE>-ov-file`).
- **`trainingTutorialsUrl` is left out** — it points at the training-catalog docs page,
  which only exists after the catalog is deployed, so it's added later. A
  catalog-hosted `developerDocumentationUrl` is treated the same way (omitted unless a
  real non-catalog dev-docs URL already exists).
- **Dependencies are always confirmed:** the skill asks whether the component depends on
  or relates to other components. If none, the `hasDependentComponents` key is omitted
  entirely; if some, it collects `related_to` (the other component's `id`) and
  `relationship_type` (usually `DependsOn`) for each.
- **Nothing is committed or pushed** without an explicit request from the user; the
  skill writes the file, shows it, and stops.

## Scope

Applies automatically only when the target repo is under
[`https://github.com/ICICLE-ai/`](https://github.com/ICICLE-ai/) (the status /
thrust / release taxonomies are ICICLE-specific). For any other repo it confirms first.

## How to use it

### With Claude Code

Auto-discovered via the YAML frontmatter on `SKILL.md`. Inside an ICICLE-ai component
repo, ask:

> "Use the icicle-component-info skill to create the component-info.yaml for this repo."

The skill infers what the repo already tells it (`sourceCodeUrl`, `owner`, `name`,
`description`, `componentVersion`, `licenseUrl`), asks for the rest and the dependency
question, writes the file, and shows it to you for review before any push.

### With Cursor / Continue / Windsurf / Copilot Chat

Point the assistant at this folder (or paste `SKILL.md` plus
`templates/component-info.yaml`) and ask it to scaffold or update the file.

### Manually

1. Copy [`templates/component-info.yaml`](templates/component-info.yaml) to the repo root.
2. Replace every `{{PLACEHOLDER}}`.
3. Remove the `hasDependentComponents` block if there are no dependencies.
4. Confirm the validation checklist in [`SKILL.md`](SKILL.md) (id/version match, valid
   status + thrust, `YYYY-MM` release, no `trainingTutorialsUrl`).

## Files in this skill

- [`SKILL.md`](SKILL.md) — skill definition (frontmatter, scope guard, schema, controlled
  vocabularies, dependency + push gates, validation checklist, steps).
- [`templates/component-info.yaml`](templates/component-info.yaml) — the file to copy and fill in.
