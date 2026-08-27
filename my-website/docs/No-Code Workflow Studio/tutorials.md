---
tags:
  - CI4AI
  - Digital-Agriculture
  - Software
---
# Tutorials

## Build a workflow (canvas)

Open the app (locally, `http://localhost:5173` — see [README.md](https://github.com/ICICLE-ai/workflow-orchestrator/blob/main/README.md)).
The dashboard is the entry point: **Manage Templates** and **Past Runs**, with a
persistent *Templates* / *Runs* nav in the header and a ⚙ **Secrets** menu on
the right.

![Dashboard](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1917" height="1024" alt="Screenshot 2026-08-14 201354" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/9ad74ca7-89ba-48ba-9886-e400dfc4d01e" )

Sign in first — the widget in the bottom-left corner shows your Tapis username,
or a **Login with Tapis** button if you aren't signed in yet. Nothing that
touches files or submits jobs works until you are (see
[Sign in to Tapis](#sign-in-to-tapis)).

1. **Create a template** — go to **Templates → Create New Template**. You land on
   an empty canvas with the step palette down the right-hand side.

   ![Templates list](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1919" height="1022" alt="Screenshot 2026-08-14 175050" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/ca623631-9345-4e66-87d0-da70112da25d" )

2. **Add steps** — the palette groups every registered step into collapsible
   sections: **Data Sources** (green, dashed), the eight pipeline stages —
   *Data Collection, Data Creation, Data Pre-processing, Data Harmonization,
   Training, Inference, Visualization, Post-processing* (blue), and **Data
   Sinks** (amber, dashed). Drag a card onto the canvas to add it as a node.

   ![Step palette](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1919" height="1027" alt="Screenshot 2026-08-14 175711" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/36b93d04-ebeb-4c9a-a738-a9720892a4ed" )

3. **Understand a node** — each node shows its display name, its **inputs** on
   the left (teal handles) and **outputs** on the right (violet handles), with a
   badge naming each port's data type. The header carries three actions:

   | Icon | Action |
   | --- | --- |
   | ⚙ (blue) | **Settings** — the step's own configuration (see step 5). |
   | 🖥 (purple) | **Run Configuration** — the compute this step requests. Hidden for design-time-only steps. |
   | 🗑 (red) | **Delete** the node and every edge attached to it. |

   ![Node anatomy](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1919" height="1028" alt="Screenshot 2026-08-14 175537" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/ebea11ba-d984-4866-b054-aa6a8763f534" )

4. **Connect steps** — drag from an output handle to an input handle. Connections
   are **type-checked**: a link is only allowed when the source port's data type
   matches the target's, is a subtype of it, or the target declares a coercion
   from it. An incompatible drop is refused with a red *Invalid Connection*
   toast naming both ports and their types.

   ![Connecting nodes](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1919" height="1017" alt="Screenshot 2026-08-14 175330" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/866cc965-77b0-438a-8a46-e59f658dc41f" )

6. **Configure each step** — click ⚙ on a node. Most steps get a form generated
   straight from their schema (numbers, switches, dropdowns, text, a Tapis path
   picker, a secret selector). Steps with a richer UI — Smart Labeler, Zero-Shot
   Annotation, the Geospatial Map viewer, Flight Plan, Training, Visualization,
   PATRA publishing, the image pre-processing studio — open their own interactive
   panel instead, some of them full-screen. Press **Save Configuration** (or
   **Save & Close**) to write the values back onto the node.

   ![Step settings](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1919" height="1022" alt="Screenshot 2026-08-14 175807" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/44895f1e-24f7-414c-a669-036aa73fef3b" )

7. **Set the compute (optional)** — click 🖥 on any step that submits a job to set
   node count, cores per node, memory, max runtime and GPUs. Leave *Execution
   system* empty to inherit the run's target; the badge in the corner tells you
   whether the step declares itself a **GPU step** or a **CPU step**. If you do
   pin a system, the queue dropdown loads that system's real queues and warns
   when a request exceeds the queue's limits.

   ![Run configuration](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1903" height="1021" alt="Screenshot 2026-08-14 175952" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/a40ef753-e9f9-426c-b2bc-16e84a8f879e" )

8. **Save the template** — click **Save Template**, give it a name, description
   and allocation account, then **Confirm Save**.

   - Saving is **blocked** while any required input port has no incoming edge;
     the drawer lists exactly which node is missing which input.
   - Saving **warns** (but lets you proceed with *Save Anyway*) when a node's
     output isn't wired to a sink — those results won't be written anywhere.

   ![Saving a template](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1918" height="1026" alt="Screenshot 2026-08-14 200222" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/ac2a3415-4d87-4b43-93e1-0f76409648cf" )


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
Settings** drawer is where the run's Tapis targets are chosen.

![Run settings](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1907" height="1020" alt="Screenshot 2026-08-14 200409" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/abba229d-68ff-4533-bb39-db70dbd9b496" )

The run declares **two** execution targets, not one. Each step's definition says
whether it needs a GPU, and the engine routes it to the matching pair — so
Zero-Shot Annotation and Training can land on a GPU queue while Flight Plan and
Geospatial run on a CPU queue **in the same run**. The GPU target's description
names the GPU steps actually present on your canvas. Field-by-field detail is in
[Run settings reference](#run-settings-reference).

Click **Launch Run**. If the canvas differs from the last saved version (an
*Unsaved changes* badge is shown next to the buttons), you're asked first whether
to keep those edits as a new version or run them without recording one — either
way **what runs is what's on screen**, never a stale saved graph.

### Watch it run

Launching takes you straight to `/runs/{id}`: the same graph, read-only, with
each node tinted by its live status.

![Live run](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1919" height="1015" alt="Screenshot 2026-08-14 200544" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/ba14988f-5699-41c8-9733-169e40e17f42" )

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

![Step logs](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1919" height="1025" alt="Screenshot 2026-08-14 200742" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/e74402c1-d15e-43d7-82e7-694df2a15d1e" )

The ⚙ in the header shows the run's frozen launch configuration; **Edit Template**
jumps back to the canvas; a `FAILED` or `CANCELLED` run gets a **Re-run** button
that relaunches it with the same settings.

**Past Runs** (`/runs`) lists every run with its status. Expand a finished run
for its per-step breakdown and logs, hit **View Live Graph** on an active one, or
**Stop** it — which cancels the workflow and any in-flight Tapis job.

![Past runs](https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/img width="1919" height="1019" alt="Screenshot 2026-08-14 200941" src="https://raw.githubusercontent.com/ICICLE-ai/workflow-orchestrator/main/https:/github.com/user-attachments/assets/faf7c864-693f-4d05-9289-4fadf44886f8" )
