---
tags:
  - CI4AI
  - Digital-Agriculture
  - Software
---
# How-To Guides

## Sign in to Tapis

| Situation | What happens |
| --- | --- |
| Standalone app | **Login with Tapis** → OAuth2 redirect → session cookie. **Logout** clears it. |
| Embedded in TapisUI | The host's Tapis token is picked up automatically; no login/logout is offered. |
| Local dev, no Tapis client | Set `TAPIS_USE_MOCK=true` in `backend/.env` and `/login` gives you a mock session so the app stays runnable. |

Your token is what the engine submits jobs *as*, so runs are owned by, and
charged to, the person who launched them.

## Point a step at files on Tapis

Any path field rendered by the generic form (schema type `tapis_path`) gives you
a **system** dropdown plus a path box with a **Browse** button that opens the
Tapis file explorer scoped to the selected system. Pick a file or a directory
depending on what the field wants; the chosen system is stored alongside the
path, and downstream steps receive the full `tapis://system/path` URI rather than
a bare path.

Available systems: `pitzer-tapis`, `cardinal-tapis`, `ascend-tapis`,
`expanse-tapis`, `expanse-tapis-static`.

## Store an API token as a secret

Some steps need a credential (Weights & Biases, Hugging Face, …). Never type it
into a config field — put it in the vault instead:

1. Click the ⚙ **Secrets** icon on the dashboard header.
2. Enter a **key** (e.g. `WANDB_API_KEY`), the **value**, and an optional
   description, then **Add secret**.

![Secrets menu](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1919" height="1025" alt="Screenshot 2026-08-14 201113" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/5652e8d3-ee19-4e1d-8d9b-88988258d85a" )

Secrets are shared across your team and **write-only** — the list never returns a
value again. A step field of type `secret` then offers a dropdown of keys, and
only the *key* is stored on the node, in the saved template, and in the run's
frozen config. The real value is resolved server-side and substituted into the
job spec at submission time only.

Steps that always need one specific secret can reference it directly in their job
template as `${secrets.KEY}`, with no per-node field at all — see
[docs/adding-a-step-form.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/docs/adding-a-step-form.md).

## Send GPU and CPU steps to different systems

1. In **Run Settings**, set the **CPU target** (exec system + queue) — every step
   with no GPU requirement follows it.
2. Set the **GPU target** — every step whose definition declares
   `"resources": {"gpu": true}` follows this one instead. The field's description
   lists which steps on your canvas that currently applies to.
3. To take one specific node off both, open its 🖥 **Run Configuration** and pick
   an **Execution system** there. That pins the step to its own system and queue,
   ignoring the run's targets. Clearing it returns the step to inheriting.

Archiving stays run-level regardless: a run whose GPU steps are on Expanse and
CPU steps on OSC still writes all its artifacts to one place.

## Run settings reference

| Field | Meaning |
| --- | --- |
| **CPU target — Exec system** | Where steps with no GPU requirement run. Also becomes the default archive system. |
| **CPU target — Queue** | Loaded live from the system's own batch queues; the description shows that queue's node/core/runtime limits. |
| **GPU target — Exec system** | Where steps declaring a GPU requirement run. |
| **GPU target — Queue** | As above, for the GPU system. |
| **Slurm account** | The allocation to charge (e.g. `PAS2699`). Prefilled from the template's allocation account. |
| **Work dir** | Derived automatically from the archive system, charge account and your Tapis username — read-only. |
| **Archive system** | Where step outputs are archived, unless a sink node overrides it. |
| **Archive dir** | Optional base directory on the archive system. Blank derives it from *Work dir*. |

Whatever you choose, each step archives under
`.../{run_id}/{step_type_key}/{node_id}`, so one run's artifacts never collide
with another's.

## Run configuration reference (per step)

| Field | Default | Meaning |
| --- | --- | --- |
| **Execution system** | *inherit* | Pin this step to its own system. Empty = follow the run's CPU or GPU target. |
| **Queue** | *system default* | Only selectable once a system is pinned. |
| **Node count** | 1 | Nodes requested. |
| **Cores per node** | 8 | Cores per node requested. |
| **Memory (MB)** | 64800 | Memory requested. |
| **Max runtime (minutes)** | 210 | Wall-clock limit. |
| **GPUs** | 0 | Becomes a `-G <n>` scheduler request. `0` on a GPU step removes it. |

These override whatever the step type's own job template specifies. When a queue
is pinned, over-requesting against its published limits is flagged here rather
than by a Tapis rejection minutes into the run.

## Fix a workflow that won't save

| Message | Fix |
| --- | --- |
| *"X" is missing required input "y"* | Connect that input to an upstream output or a data source. Optional inputs are never flagged. |
| *"X" output "y" is not saved to a sink* | Add a sink node (e.g. **💾 Write Results (JSON)**) and wire the output into it — or press **Save Anyway** if leaving it unconsumed is deliberate. |
| *Cannot connect: … is incompatible with …* | The two ports' data types don't match. Insert an adapter step, or use a port of the right type. |

## Stop, re-run, and recover

- **Stop** a running run from the *Past Runs* list. This cancels the durable
  workflow, its child step workflows, and any in-flight Tapis job. It can't be
  undone.
- **Re-run** appears on a `FAILED` or `CANCELLED` run's page and relaunches the
  same template version with the same Tapis options — no re-entering settings.
- To change something first, use **Edit Template** on the run page: it opens the
  exact version that ran.

## Add a new step type

Steps are registered from `backend/steps/<key>/step.json` — no frontend code is
needed for a step whose settings are ordinary fields.

- Form-rendered settings: [docs/adding-a-step-form.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/docs/adding-a-step-form.md)
- Custom interactive panel: [docs/adding-a-step-custom-ui.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/docs/adding-a-step-custom-ui.md)
