---
name: icicle-component-info
disable-model-invocation: false
description: Scaffold or update the component-info.yaml metadata file for an ICICLE-ai component repository. Produces a single-item YAML list entry describing the component (id, owner, primaryThrust, name, status, description, componentVersion, targetIcicleRelease, dependencies, licenseUrl, publicAccess, sourceCodeUrl, and the codeReview/tests/docs/tutorials flags) that the ICICLE component catalog consumes. Enforces that id equals name-without-spaces then a colon then componentVersion, validates status and primaryThrust against the ICICLE controlled vocabularies, treats targetIcicleRelease as a YYYY-MM release month, leaves trainingTutorialsUrl (and any catalog-hosted developerDocumentationUrl) out because those are filled in after the training-catalog is deployed, always asks the maintainer whether the component depends on other components before writing hasDependentComponents, and never commits or pushes without an explicit confirmation from the user. Use this whenever the user asks to create, scaffold, fix, or update a component-info or component metadata file for an ICICLE component, or mentions the ICICLE component catalog entry. Apply automatically only when the target repo is under github.com/ICICLE-ai/; otherwise run the confirmation gate first.
---

# ICICLE Component Info Skill

This skill produces a single `component-info.yaml` at the root of an ICICLE-ai
component repository. The file is one YAML list entry (note the leading `- `) of
metadata that the ICICLE **component catalog** consumes. It is a sibling to
`icicle-readme-skill`: that one writes the human-facing `README.md`; this one writes
the machine-facing catalog metadata.

## Confirmation gate — when this skill applies

**Apply automatically only if the target repo is under `https://github.com/ICICLE-ai/`.**
Any of these confirms an ICICLE-ai repo and you may proceed without prompting:

- `git remote -v` shows a URL containing `github.com/ICICLE-ai/` or `github.com:ICICLE-ai/`.
- The repo is a fresh checkout/working copy of an ICICLE-ai repo.
- The user explicitly states the project is or will be hosted under `ICICLE-ai`.

If none hold, **stop and ask before writing anything**: the `status`, `primaryThrust`,
and `targetIcicleRelease` taxonomies are ICICLE-specific and the file only means
something to the ICICLE catalog. Confirm the user still wants an ICICLE
`component-info.yaml` here, then continue.

## Output

A file named `component-info.yaml` at the **component repo root**, containing exactly
one list entry. Copy from [`templates/component-info.yaml`](templates/component-info.yaml)
and replace every `{{PLACEHOLDER}}`.

## The schema (field by field)

Order the keys as in the template. Every field below is required unless marked optional.

| Field | Rule |
|-------|------|
| `id` | `"<name-with-spaces-removed>:<componentVersion>"`. Derive the prefix by removing spaces (and any punctuation that isn't alphanumeric) from `name`, preserving case. **The part after `:` MUST equal `componentVersion` exactly.** |
| `owner` | Maintainer's full name. Default to `git config user.name` and confirm. |
| `primaryThrust` | Exactly one value from the controlled vocabulary below. |
| `name` | Human-readable component name (spaces allowed). |
| `status` | Exactly one value from the status vocabulary below. |
| `description` | 1–3 sentences on what the component does. Lift from the README's opening paragraph if present. |
| `componentVersion` | Semver `X.Y.Z`. Must match the `id` suffix. Pull from the repo's latest tag / release / `pyproject.toml`/`package.json` if available. **Never bump it silently** — see "Version bumps" below. |
| `targetIcicleRelease` | One value from the `IcicleReleases` vocabulary below — a quoted `YYYY-MM` release month (e.g. `"2026-05"`) or `None`. Ask if unknown — do not guess a date. |
| `hasDependentComponents` | List of `{ related_to, relationship_type }`. **Omit the whole key if there are no dependencies.** See "Dependencies" below. |
| `licenseUrl` | GitHub license-tab URL: `https://github.com/ICICLE-ai/<repo>?tab=<LICENSE>-ov-file` (e.g. `?tab=GPL-3.0-1-ov-file`). Derive `<LICENSE>` from the repo's `LICENSE` file or the README License badge. |
| `publicAccess` | `true`/`false` — is the source publicly accessible. |
| `sourceCodeUrl` | The repo URL, e.g. `https://github.com/ICICLE-ai/<repo>`. Read from `git remote`. |
| `codeReviewConducted` | `true`/`false`. Ask the maintainer; do not assume. |
| `testsWritten` | `true`/`false`. Ask; a quick check for a `tests/` dir informs the default but the maintainer confirms. |
| `developerDocumentationAvailable` | `true`/`false`. |
| `developerDocumentationUrl` | **Optional.** Include only if dev docs already live at a stable URL. If the dev docs are the catalog's generated API-reference page, **leave it out** — it is filled in after the catalog is deployed. |
| `trainingTutorialsAvailable` | `true`/`false`. |
| `trainingTutorialsUrl` | **Do not set.** It points at the training-catalog docs page, which only exists after deployment. It is added later — never invent it now. |

### Controlled vocabulary — `status`

Pick exactly one. Reject anything not in this list (ask the user which fits):

- `Unreleased` — not available for use; may still be tracked to help cross-component design/planning.
- `PrototypeRelease` — little to no formal testing.
- `AlphaRelease` — incomplete functionality and/or significant potential for breaking API changes; some testing, often minimal external user testing.
- `BetaRelease` — functionally complete or nearly so; significant internal testing; some external testing likely; bugs/perf issues may exist; breaking API changes less likely.
- `ProductionRelease` — no known significant defects, stable interfaces/APIs; backwards-incompatible changes should produce a new release version.

### Controlled vocabulary — `primaryThrust`

Pick exactly one, `<layer>/<Thrust>` form. Reject anything not in this list:

```
core/Software   core/CI4AI   core/AI4CI   core/FoundationAI   core/PADI   core/VA
useInspired/DA   useInspired/AE   useInspired/SF
```

Note these differ from the README tag spellings: `core/FoundationAI` (Foundation-AI),
`core/VA` (Visual-Analytics), `useInspired/DA` (Digital-Agriculture),
`useInspired/AE` (Animal-Ecology), `useInspired/SF` (Smart-Foodsheds). If the user
gives a README-style tag, map it to the thrust code and confirm.

### Controlled vocabulary — `targetIcicleRelease` (`IcicleReleases`)

`targetIcicleRelease` must be one of the official ICICLE release months, written as a
**quoted `YYYY-MM` string**, or the literal `None`:

```
None
"2023-04"
"2023-06"
…and the later release months on the ICICLE release schedule
```

Rules:

- The value must match `^\d{4}-\d{2}$` (a year and a month, no day) — quote it so YAML
  keeps it a string, matching the vocabulary.
- Use `None` when the component is not tied to a specific release (e.g. `Unreleased`
  planning entries).
- **Do not invent a release month.** If the user gives one that isn't an established
  ICICLE release, or you're unsure of the current schedule, ask them to pick the
  correct value rather than guessing.

### Version bumps

If updating an existing entry (Mode B) and the version is changing — or if the repo's
tags/release suggest a newer version than what's in the file — **do not bump silently.**
State the current `componentVersion`, suggest the new one (with your reasoning, e.g.
"repo is tagged `v0.2.0` but the file says `0.1.0`"), and ask the user to confirm the
target version. When they confirm, update `componentVersion` **and** the `id` suffix in
the same edit so they stay in sync.

## Dependencies — always ask

Before writing the file, **explicitly ask the maintainer**:

> "Does this component depend on, or relate to, any other ICICLE components?"

- **If no:** omit the `hasDependentComponents` key entirely (do not emit an empty list).
- **If yes:** for each related component, collect from the user:
  - `related_to` — the other component's id, `"<name>:<version>"` (e.g. `icicleai-tapisui-extension:0.1.0`).
  - `relationship_type` — usually `DependsOn`. If the relationship is not a plain dependency, ask the user for the exact term rather than guessing.

  Emit one list entry per related component.

## Operating modes

Detect the mode before writing by checking whether a metadata file already exists at
the repo root. **Look for both `component-info.yaml` and `component.yaml`** (either name
counts as an existing entry).

### Mode A — Scaffold (no file, or empty file)

Copy `templates/component-info.yaml`, replace every `{{PLACEHOLDER}}`, and remove the
`hasDependentComponents` block if there are no dependencies.

### Mode B — Update in place (file exists with real content)

**If a `component-info.yaml` (or `component.yaml`) already exists with real content,
ask the user before changing it** — confirm they want it updated and what should change.
Do not overwrite or regenerate an existing file without that go-ahead. Then:

1. **Read the existing file first.** (Keep its filename — if the repo already uses
   `component.yaml`, update that file in place rather than creating a second one.)
2. Change only the fields the user asked to change (commonly `componentVersion` +
   the matching `id` suffix, `status`, `targetIcicleRelease`, or a new dependency).
3. **Edit narrowly** — keep any keys/values already there; do not reorder or reformat
   unrelated lines, and do not delete fields the user added.
4. When `componentVersion` changes, **suggest/ask before bumping** (see "Version
   bumps") and update the `id` suffix in the same edit so they stay in sync.
5. If the edit touches more than one field, show a short summary of what will change
   and confirm before writing.

## Steps

1. **Check repo origin** and run the confirmation gate if it is not an ICICLE-ai repo.
2. **Detect the mode** (does `component-info.yaml` *or* `component.yaml` exist with real
   content? If so, ask the user before updating it).
3. **Auto-fill what the repo already tells you**, then confirm each with the user:
   `sourceCodeUrl` and `owner` from `git remote`/`git config`; `name`/`description`
   from the README; `componentVersion` from tags/release/`pyproject.toml`/`package.json`;
   `licenseUrl` from the `LICENSE` file or README badge.
4. **Ask for what can't be inferred:** `primaryThrust`, `status`, `targetIcicleRelease`,
   `publicAccess`, `codeReviewConducted`, `testsWritten`,
   `developerDocumentationAvailable`, `trainingTutorialsAvailable`, and the
   **dependencies** question above.
5. **Write the file** (Mode A) or edit it narrowly (Mode B).
6. **Validate** (see below).
7. **Show the finished file to the user.** Then **stop.**
8. **Do not commit, push, or open a PR unless the user explicitly asks.** If they ask
   to push, confirm the target repo/branch first, then proceed. (A file in an
   ICICLE-ai component repo is pushed to *that* repo, not to training-catalog.)

## Validation checklist (run before showing the file)

- `id` splits on the last `:` into `<prefix>` and `<version>`; `<version>` equals
  `componentVersion` exactly; `<prefix>` equals `name` with spaces/punctuation removed.
- `status` is one of the five status values.
- `primaryThrust` is one of the nine thrust values.
- `componentVersion` is `X.Y.Z`.
- `targetIcicleRelease` is `None`, or a quoted `YYYY-MM` string that matches
  `^\d{4}-\d{2}$` and is a real `IcicleReleases` value (not an invented month).
- Every `*Available`/`publicAccess`/`codeReviewConducted`/`testsWritten` value is a
  bare `true` or `false` (not quoted, not `yes`/`no`).
- `hasDependentComponents` is present **only** when there is at least one dependency,
  and each entry has both `related_to` and `relationship_type`.
- `trainingTutorialsUrl` is **absent**. `developerDocumentationUrl` is absent unless a
  real, non-catalog dev-docs URL was supplied.
- The file is valid YAML and is a single-item list (starts with `- id:`).

If anything fails, fix it (Mode A) or ask the user (Mode B) before showing the file.

## Cross-platform usage

The skill is plain Markdown plus a single YAML template, so it works in Claude Code
(auto-discovered via this `SKILL.md`'s frontmatter), in Cursor/Continue/Windsurf/
Copilot Chat (point the assistant at this folder), or by hand (copy
`templates/component-info.yaml` and fill it in).

## Template

See [`templates/component-info.yaml`](templates/component-info.yaml).
