---
tags:
  - CI4AI
  - Digital-Agriculture
  - Software
title: "No-Code Workflow Studio: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for No-Code Workflow Studio. A browser-based workflow builder for the full ML lifecycle: wire up a pipeline in a drag-and-drop canvas — data…"
---
# Tutorials

## Build a workflow (canvas)

Open the app (locally, `http://localhost:5173` — see [README.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/README.md)).
The dashboard is the entry point: **Manage Templates** and **Past Runs**, with a
persistent *Templates* / *Runs* nav in the header and a ⚙ **Secrets** menu on
the right.

<img width="1917" height="1024" alt="Screenshot 2026-08-14 201354" src="https://github.com/user-attachments/assets/9ad74ca7-89ba-48ba-9886-e400dfc4d01e" />

Sign in first — the widget in the bottom-left corner shows your Tapis username,
or a **Login with Tapis** button if you aren't signed in yet. Nothing that
touches files or submits jobs works until you are (see
[Sign in to Tapis](#sign-in-to-tapis)).

1. **Create a template** — go to **Templates → Create New Template**. You land on
   an empty canvas with the step palette down the right-hand side.

   <img width="1919" height="1022" alt="Screenshot 2026-08-14 175050" src="https://github.com/user-attachments/assets/ca623631-9345-4e66-87d0-da70112da25d" />

2. **Add steps** — the palette groups every registered step into collapsible
   sections: **Data Sources** (green, dashed), the eight pipeline stages —
   *Data Collection, Data Creation, Data Pre-processing, Data Harmonization,
   Training, Inference, Visualization, Post-processing* (blue), and **Data
   Sinks** (amber, dashed). Drag a card onto the canvas to add it as a node.

   <img width="1919" height="1027" alt="Screenshot 2026-08-14 175711" src="https://github.com/user-attachments/assets/36b93d04-ebeb-4c9a-a738-a9720892a4ed" />

3. **Understand a node** — each node shows its display name, its **inputs** on
   the left (teal handles) and **outputs** on the right (violet handles), with a
   badge naming each port's data type. The header carries three actions:

   | Icon | Action |
   | --- | --- |
   | ⚙ (blue) | **Settings** — the step's own configuration (see step 5). |
   | 🖥 (purple) | **Run Configuration** — the compute this step requests. Hidden for design-time-only steps. |
   | 🗑 (red) | **Delete** the node and every edge attached to it. |

   <img width="1919" height="1028" alt="Screenshot 2026-08-14 175537" src="https://github.com/user-attachments/assets/ebea11ba-d984-4866-b054-aa6a8763f534" />

4. **Connect steps** — drag from an output handle to an input handle. Connections
   are **type-checked**: a link is only allowed when the source port's data type
   matches the target's, is a subtype of it, or the target declares a coercion
   from it. An incompatible drop is refused with a red *Invalid Connection*
   toast naming both ports and their types.

   <img width="1919" height="1017" alt="Screenshot 2026-08-14 175330" src="https://github.com/user-attachments/assets/866cc965-77b0-438a-8a46-e59f658dc41f" />

6. **Configure each step** — click ⚙ on a node. Most steps get a form generated
   straight from their schema (numbers, switches, dropdowns, text, a Tapis path
   picker, a secret selector). Steps with a richer UI — Smart Labeler, Zero-Shot
   Annotation, the Geospatial Map viewer, Flight Plan, Training, Visualization,
   PATRA publishing, the image pre-processing studio — open their own interactive
   panel instead, some of them full-screen. Press **Save Configuration** (or
   **Save & Close**) to write the values back onto the node.

   <img width="1919" height="1022" alt="Screenshot 2026-08-14 175807" src="https://github.com/user-attachments/assets/44895f1e-24f7-414c-a669-036aa73fef3b" />

7. **Set the compute (optional)** — click 🖥 on any step that submits a job to set
   node count, cores per node, memory, max runtime and GPUs. Leave *Execution
   system* empty to inherit the run's target; the badge in the corner tells you
   whether the step declares itself a **GPU step** or a **CPU step**. If you do
   pin a system, the queue dropdown loads that system's real queues and warns
   when a request exceeds the queue's limits.

   <img width="1903" height="1021" alt="Screenshot 2026-08-14 175952" src="https://github.com/user-attachments/assets/a40ef753-e9f9-426c-b2bc-16e84a8f879e" />

8. **Save the template** — click **Save Template**, give it a name, description
   and allocation account, then **Confirm Save**.

   - Saving is **blocked** while any required input port has no incoming edge;
     the drawer lists exactly which node is missing which input.
   - Saving **warns** (but lets you proceed with *Save Anyway*) when a node's
     output isn't wired to a sink — those results won't be written anywhere.

   <img width="1918" height="1026" alt="Screenshot 2026-08-14 200222" src="https://github.com/user-attachments/assets/ac2a3415-4d87-4b43-93e1-0f76409648cf" />


Reopening a template from **Templates → Edit Template** puts you back on the
canvas with its title showing `name vN`. Saving again creates a **new version**
rather than overwriting the old one, so earlier runs keep pointing at exactly the
graph they executed.

## Run the workflow on Tapis

### Sign in

Standalone, click **Login with Tapis** in the bottom-left widget: the backend
redirects you to your Tapis tenant, and back to the app with a session cookie.
Embedded inside TapisUI, the host already holds your token — you're signed in
automatically and the widget shows your username with no login/logout controls.

### Configure the run

With a saved template open, click **Run Workflow** (green, top right). The **Run
workflow** drawer opens, with three numbered sections.

<img width="1907" height="1020" alt="Screenshot 2026-08-14 200409" src="https://github.com/user-attachments/assets/abba229d-68ff-4533-bb39-db70dbd9b496" />

![Run Workflow Drawer](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/docs/images/run_workflow_drawer.png)

1. **Run type:** how the pipeline is sent to Tapis.
   - **One job per step** (default): each step gets exactly the resources it asks
     for. Best for mixed CPU/GPU pipelines and long steps.
   - **Single job**: the whole pipeline runs as one Tapis job, so there's one queue
     wait instead of many. Best for short pipelines. See [Run a whole pipeline as
     one Tapis job](#run-a-whole-pipeline-as-one-tapis-job).
2. **Where each step runs:** pick a system and queue for **CPU steps**, and for
   **GPU steps** if the canvas has any. Each card lists the steps it applies to,
   so Zero-Shot Annotation and Training can run on a GPU queue while Flight Plan
   and Geospatial run on a CPU queue **in the same run**. (In single-job mode this
   becomes **Where the job runs**.) A step's own Run Configuration overrides this.
3. **Charge account:** the allocation to charge, e.g. `PAS2699`. It's filled in
   from the template's allocation account.

Two optional sections sit below, closed by default:

- **Storage & archive:** where outputs are written (work dir, archive system,
  archive dir). The defaults are usually right.
- **Trigger with a webhook:** a URL that starts this workflow from outside the
  Studio. See [Trigger a workflow from outside
  (webhook)](#trigger-a-workflow-from-outside-webhook).

Field-by-field detail is in [Run settings reference](#run-settings-reference).

### Verify before launching

At the bottom of the drawer there are two buttons:

- **Verify** checks the run on Tapis without launching anything.
- **Verify & launch** runs the same checks, then launches only if nothing would
  stop the run.

![Verification](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/docs/images/verification.png)

The checks, grouped as they appear:

| Group | What's checked |
| --- | --- |
| **Account** | Your Tapis login is accepted. |
| **Plan** | The workflow has steps that submit jobs; in single-job mode, that it can run as one job. |
| **Compute** | Each system is reachable, each queue exists, and every step's request (nodes, cores, memory, time) fits the queue's limits. |
| **Apps** | Each step's Tapis app is registered and visible to you. |
| **Data** | Each input path exists, and the output folder can be created. |

Each check shows ✓ passed, ⚠ warning or ✗ problem, with a short reason. Then:

- **All passed** or **only warnings:** the run launches (or is ready to).
- **A problem:** the run is not launched. Fix it, or press **Launch anyway** if
  you know better.
- **Changed a setting after verifying?** The result is marked *settings changed —
  re-verify*, and **Verify & launch** checks again before launching.

These are the mistakes that used to fail a run minutes in: an output folder you
can't write to, an app that isn't registered, a queue that doesn't exist, a
request over a queue's limits, or a missing input. Verifying catches them before
the run is created.

Good to know:

- Verifying creates the base output folder if it doesn't exist (the first thing
  any run would do there). It's the only reliable way to test that you can write
  to it.
- With **unsaved changes**, the checks use the last saved version, and you're
  asked to save before the run starts. Either way **what runs is what's on
  screen**: you can keep the edits as a new version, or run them without
  recording one.

### Watch it run

Launching takes you straight to `/runs/{id}`: the same graph, read-only, with
each node tinted by its live status.

<img width="1919" height="1015" alt="Screenshot 2026-08-14 200544" src="https://github.com/user-attachments/assets/ba14988f-5699-41c8-9733-169e40e17f42" />

| Node state | Meaning |
| --- | --- |
| **Pending** (grey, faded) | Not started. Shows *Waiting on: …* while an upstream step is unfinished. |
| **Running** (blue) | The step's Tapis job is in flight. |
| **Completed** (green) | Finished; its outgoing edges start animating. |
| **Failed** (red) | The step errored — open its logs. |
| **Blocked** / **Cancelled** | Upstream failure, or the run was stopped. |

A second, smaller badge carries the raw **Tapis job status** — the full
vocabulary (`STAGING_INPUTS`, `QUEUED`, `RUNNING`, `ARCHIVING`, `FINISHED`, …) —
so a step that looks stuck can be told apart from one merely sitting in a queue.
The page polls every 2.5 s while the run is `RUNNING`; ⟳ in the header refreshes
on demand.

**Click any node** to open its logs: the step's resolved configuration, Tapis'
own outcome message, the orchestrator's error (if any), and the tail of the
container's `tapisjob.out`. Nodes that never submit a job (Smart Labeler, the
map viewer, …) open their own panel read-only against the run's resolved values
instead, so you can inspect what they produced.

<img width="1919" height="1025" alt="Screenshot 2026-08-14 200742" src="https://github.com/user-attachments/assets/e74402c1-d15e-43d7-82e7-694df2a15d1e" />

The ⚙ in the header shows the run's frozen launch configuration; **Edit Template**
jumps back to the canvas. A run that isn't in flight gets a **Resume** button —
carry on from where it stopped, or redo a chosen step and everything after it —
and a `FAILED` or `CANCELLED` one also gets **Start over**, which relaunches it
from the beginning as a new run with the same settings. See
[Stop, resume, and recover](#stop-resume-and-recover).

**Past Runs** (`/runs`) lists every run with its status, with a search box and
filters for status and ordering. Expand a finished run for its per-step
breakdown and logs, hit **View Live Graph** on an active one, **Stop** it — which
cancels the workflow and any in-flight Tapis job — or **Resume** a stopped or
failed one straight from the list.

<img width="1919" height="1019" alt="Screenshot 2026-08-14 200941" src="https://github.com/user-attachments/assets/faf7c864-693f-4d05-9289-4fadf44886f8" />

## Run the workflow on your own machine

Instead of submitting jobs to Tapis, you can run a saved workflow on a machine you
choose: an HPC node, a lab GPU box, or your own computer. You download one zip,
copy a few commands, and the workflow runs there. Nothing on that machine talks
back to the platform while it runs.

Open a saved template and click **Deploy to my node** (top right of the canvas).

![Deploy to my node button](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/docs/images/users_node/deploy_button.png)

The dialog has three steps.

![Deploy to my node dialog](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/docs/images/users_node/deploy_dialog.png)

### 1. Where will it run?

1. **Node:** pick the Tapis system your machine belongs to (e.g. `pitzer-tapis`).
   If it isn't on Tapis, pick **Other (my own machine)** and give it a name, like
   `lab-gpu-01`.
2. **My data is at the same paths as on the platform:** leave this **on** when
   your machine can see the same folders the workflow uses, for example a node on
   the same cluster. Turn it off only if you've copied the data somewhere else;
   then choose that folder as the **Data root**.
3. **Work dir:** the folder where results are written. It's created if it doesn't
   exist.

Use **Browse** to pick folders (Tapis systems only). Below the fields, a preview
shows exactly where each input will be read from. Check it before going on.

![Input path preview](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/docs/images/users_node/path_preview.png)

Your choices are saved for this workflow (you'll see *Saved for this workflow ✓*),
so they're filled in next time, on any browser, and for new versions.

### 2. Check the workflow

A summary shows the number of steps, container images, credentials needed and
any warnings, with a **Ready to run** or **Needs attention** badge. Read any
warnings before continuing. Steps that only run inside the platform are listed
here, since they can't run on your machine.

### 3. Run it

Pick a tab and follow its numbered steps. Every command has a copy button.

| Tab | Use it when |
| --- | --- |
| **Apptainer** | Your machine has Apptainer, which most HPC clusters do. Recommended on HPC. |
| **Docker** | Your machine has Docker and allows privileged containers. |
| **Offline zip** | Your machine has no network access. Download the zip here and copy it over. |

On the machine, the steps are the same for both Docker and Apptainer:

```bash
# 1. Download the zip (copy the exact command from the dialog)
curl -fL -o my-workflow-v3-deploy.zip '<link from the dialog>'

# 2. Unzip it and go into the folder
unzip my-workflow-v3-deploy.zip && cd my-workflow-v3

# 3. Run it. Apptainer route shown; the Docker tab gives its own command
./run.sh --data-root / --workdir /path/to/workdir --dry-run   # check first
./run.sh --data-root / --workdir /path/to/workdir             # then run
```

![Apptainer tab](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/docs/images/users_node/apptainer_tab.png)

Tips:

- **Download links work for one hour.** If one has expired, copy a fresh one from
  the dialog.
- **Start with `--dry-run`.** It checks that every input is found and prints what
  each step would run, without running anything.
- **Changed a path after unzipping?** No need to download everything again. Use
  the dialog's *Changed the paths after unzipping?* box to replace just
  `bundle.json`, then run again.
- **Credentials:** if the workflow needs any (e.g. `HF_TOKEN`), the dialog shows
  an `export` step. They are never stored in the download.
- **Results** go into the work dir: one folder per step, plus a
  `run-<id>-report.json` summary.
