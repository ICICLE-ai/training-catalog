---
tags:
  - Software
  - AI4CI
title: "HARP UI: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for HARP UI. HARP profiles scientific applications across high-performance computing (HPC) systems, builds regression models from the resulting…"
---
# How-To Guides

## Prerequisites

HARP UI performs application, job, and file operations through Tapis (Systems, Files, Apps, and Jobs); it never touches a cluster file system directly. The optional OSC queue validator separately runs only `sinfo` through a dedicated noninteractive SSH identity. Before profiling an application you need:

1. **Execution systems and credentials** registered in Tapis for each cluster (e.g. OSC Pitzer, TACC). The notebooks [`Executing_HARP_using_TAPIS*.ipynb`](https://github.com/ICICLE-ai/HARP-UI/blob/main/Notebooks) show how.
2. **An allocation account** on each system.
3. **A sweep container** for your application, and **a Tapis app** for it whose `notes.harp` block describes its command, work folder and parameters.

## Understand the system and queue lists

HARP asks Tapis which execution systems and logical queues are visible to the current user. Inventory, apps, campaigns, and jobs begin loading together so selectors can populate without waiting for profiling CSVs. Systems and partitions initially show **CHECKING**. After the essential page data appears, HARP performs the same read-only access check as TapisUI—one Tapis Files listing of `/` per system—in a controlled sequence so slow remote checks do not flood the Tapis session. Tapis provides the logical-queue definitions, while an optionally configured server-side probe validates OSC partitions against live Slurm state.

- A visible system may still require the user to finish cluster authentication or obtain an allocation.
- **AVAILABLE** on a system means the Files listing succeeded through Tapis. **UNAVAILABLE** can mean missing or invalid credentials, host downtime, or another Files/SSH failure; HARP preserves the returned Tapis detail for diagnosis.
- A visible logical queue may map to a scheduler partition that is temporarily inactive, drained, restricted, or unavailable for the requested resources.
- HARP does not submit probe jobs to discover queues. When the optional OSC queue probe is configured, the server runs the fixed, read-only command `sinfo --all --noheader --format='%P|%a|%t'` on Ascend, Pitzer, and Cardinal at startup and on a refresh interval. Live Slurm output—not the OSC documentation—is used to validate the mapped partition.
- The probe snapshot is saved under `HARP_SERVER_DATA`, reused after a Pod restart, refreshed once every 24 hours by default, and ignored after its configured maximum age. It uses the Pod's dedicated OSC SSH identity, independently of whoever signs in to HARP.
- A queue begins as **CHECKING**, becomes green **AVAILABLE** after system access and current live scheduler data agree, or becomes red **INVALID** / **UNAVAILABLE** when HARP cannot safely offer it. A missing or unavailable partition from a current live result is disabled only in HARP; HARP never changes or deletes the Tapis System definition.
- **Show unavailable** reveals disabled systems and queues for diagnosis without allowing them to be selected.
- Tapis logical queues are still configuration owned by the relevant Tapis system administrator and must be corrected there when a mapping is wrong.
- Queue limits published by Tapis are validation limits, not a promise that a matching node is free or that requesting the maximum will produce a valid node shape.

Every profiling job currently sends `nodeCount=1`. **Cores requested** maps to Tapis `coresPerNode`, **memory requested** maps to `memoryMB`, and **time limit requested** maps to `maxMinutes`. HARP defaults to one core, 4 GB per requested core, and `runs per job × run timeout + 10 minutes`, capped by the logical queue. GPU-labelled queues additionally request one GPU and launch Singularity/Apptainer with `--nv`.

For a first test, choose a system you already use successfully through Tapis, select a development or debug queue when appropriate, and request conservative resources.

> **Screenshot slot — `docs/images/howto-system-queue-status.png`:** Show system access/status indicators and configured queues. Include one usable and one unavailable example without exposing account details.

## Troubleshoot a failed Tapis job

Open **HARP Generate → Jobs**, expand **Failure details**, and locate the failed Tapis job. Preserve the job ID, selected system and queue, classified reason, Tapis condition, and raw message when asking an administrator for help.

| Message or category | What it usually means | What to try |
|---|---|---|
| Missing credentials or remote access failure | Tapis cannot authenticate to the execution system as the required effective user | Authenticate the system in Tapis or ask the system owner to verify its effective-user and credential configuration |
| Must specify account / invalid account | The scheduler account option is absent or invalid | Add the correct site allocation, such as `-A <project>`, and verify that your cluster identity belongs to it |
| Tapis queue maps to an unknown scheduler partition | The Tapis logical queue's `hpcQueueName` is absent from the current live Slurm partition list | This is a Tapis system configuration issue. Choose another available queue and report the Tapis queue → Slurm partition mapping to the system administrator |
| Required partition not available / inactive / drain | The mapped scheduler partition exists but is not currently accepting the job | Choose another **AVAILABLE** partition or ask the system administrator when it will return |
| Requested node configuration is not available | No node matches the requested cores, memory, GPU, or other resource shape | Reduce the request and use a configuration supported by that queue |
| `QOSMinGRES` / accounting-QOS policy | A GPU partition requires a GPU resource or the request violates that account's QOS limits | Select a GPU-labelled HARP queue so one GPU and `--nv` are requested, then verify the account/QOS with the system administrator |
| Job launch directory or working-directory failure | The Tapis System's `jobWorkingDir` / effective-user path is invalid for the remote host | This is a Tapis system configuration issue; report the execution system and failing path to its administrator |
| Out of memory | The launched application exceeded its memory allocation | Increase memory, reduce application batch size, or reduce concurrent work inside the job |
| Time limit | The scheduler stopped the job at its walltime | Increase the limit within the queue maximum or make the sweep smaller |
| Container launch | Apptainer/Singularity could not pull, convert, cache, or start the image | Verify the image is public and compatible; give the raw message to the system administrator if cache conversion failed |
| Application error | The job launched but the application returned a nonzero exit code | Open `tapisjob.out`, reproduce with one small parameter combination, and fix the application command or inputs |

The Jobs table uses short summaries such as **Tapis configuration issue**, **partition unavailable**, or **GPU/QOS request rejected**. The full Tapis and scheduler text remains under the expandable raw failure detail. A later successful status poll clears a transient connection error instead of leaving a completed job marked with the old polling failure.

> **Screenshot slot — `docs/images/howto-failure-details.png`:** Show the failure summary cards and one expanded raw message. Sanitize usernames, paths, job IDs, and allocations if the screenshot will be public.

## Find job output and profiling results

Each profiling job writes its live output under the Tapis job output directory. Tapis archives the job output into the campaign folder selected on **Review & submit**. HARP then merges successful profiling rows into the campaign CSV used by **Profiled data** and **HARP Build**.

Use the Jobs page for the Tapis job ID and status, the Profiled data page for successful timing rows, and the selected results folder for archived files such as `tapisjob.out`, progress and summary JSON, and profiling CSV data.

> **Screenshot slot — `docs/images/howto-results-location.png`:** Show the submitted campaign's results location and the corresponding Profiled data view. Use a non-sensitive example path.

## Recover after a token expires or HARP restarts

Jobs already accepted by Tapis continue running even when HARP loses its session. HARP pauses local tracking until the owner signs in again, then resumes polling and finalization from saved campaign state.

1. Start or reopen HARP.
2. Sign in with a current Tapis session.
3. Open **Jobs** and confirm the sweep resumes updating.
4. If the remote job already ended, allow HARP time to retrieve its final state and merge available results.

> **Screenshot slot — `docs/images/howto-resume-session.png`:** Show a paused or waiting-for-login sweep and the same sweep updating after login.

## Package your application for sweeps

1. Build and push the job container, starting from [`DockerFiles/Dockerfile_App_Template_Sweep`](https://github.com/ICICLE-ai/HARP-UI/blob/main/DockerFiles/Dockerfile_App_Template_Sweep) (the Euler example is [`Dockerfile_App_EulerNumber_Sweep`](https://github.com/ICICLE-ai/HARP-UI/blob/main/DockerFiles/Dockerfile_App_EulerNumber_Sweep)):
   ```bash
   docker build -f DockerFiles/Dockerfile_App_EulerNumber_Sweep -t <hub>/harp-sweep-eulernumber:1.0.0 .
   docker push <hub>/harp-sweep-eulernumber:1.0.0
   ```
   Make the image public so the clusters can pull it.
2. Register (or update) the Tapis app with [`Notebooks/Create_HARP_Sweep_App_TAPIS.ipynb`](https://github.com/ICICLE-ai/HARP-UI/blob/main/Notebooks/Create_HARP_Sweep_App_TAPIS.ipynb). It can also run one small test job.

Inside each job, [`job_runner/harp_job_runner.py`](https://github.com/ICICLE-ai/HARP-UI/blob/main/job_runner/harp_job_runner.py) runs its parameter combinations x repetitions, measures walltime and hardware, and writes `harp_profile.csv` and `harp_progress.json` to the Tapis output directory.

> **Screenshot slot — `docs/images/howto-register-sweep-app.png`:** Show the created Tapis app's image, runtime, command metadata, and `notes.harp` parameter definition. Do not include credentials.

## Register the build app (Tapis model training)

[`DockerFiles/Dockerfile_HARP_Build`](https://github.com/ICICLE-ai/HARP-UI/blob/main/DockerFiles/Dockerfile_HARP_Build) packages the pipeline and [`job_runner/harp_build_runner.py`](https://github.com/ICICLE-ai/HARP-UI/blob/main/job_runner/harp_build_runner.py). Push it as `harp-build:1.0.0` and register it with `Create_HARP_Sweep_App_TAPIS.ipynb` using `APP = "build"`; its notes carry `role: "build"`, which is how the UI finds it. Without it, builds can still run on the computer hosting the server.

## Run HARP UI as a shared HTTPS server

The server receives Tapis access tokens, so anything other than `localhost` must use HTTPS.

```bash
pip install -r harp_server/requirements.txt
cd harp_server
./scripts/make_dev_cert.sh certs <server-hostname>      # testing only: self-signed
HARP_SSL_CERT=certs/cert.pem HARP_SSL_KEY=certs/key.pem python3 -m harp_server.serve
```

Open `https://<server-hostname>:8443`. For real use, point `HARP_SSL_CERT` / `HARP_SSL_KEY` at an institutional or Let's Encrypt certificate. Behind nginx, Caddy or Apache, run `HARP_BEHIND_PROXY=1 HARP_PORT=8000 python3 -m harp_server.serve` and forward with an `X-Forwarded-Proto` header.

| Variable | Purpose | Default |
|---|---|---|
| `HARP_SSL_CERT`, `HARP_SSL_KEY` | Certificate and key (PEM) | required unless behind a proxy |
| `HARP_HOST`, `HARP_PORT` | Listen address | `0.0.0.0:8443` |
| `HARP_BEHIND_PROXY` | Serve plain HTTP and trust the proxy's forwarded headers | off |
| `HARP_SERVER_DATA` | Campaign and build state directory | `~/.harp_server` |
| `HARP_POLL_SECONDS` | Tapis polling interval | `15` |
| `HARP_TAPIS_BASE_URL` | Tenant used to validate tokens | `https://icicleai.tapis.io` |
| `HARP_PORTAL_ORIGINS` | Exact TapisUI origins allowed to frame HARP and hand off tokens | unset (framing disabled) |
| `HARP_SESSION_SAME_SITE` | Session cookie policy (`strict`, `lax`, `none`; `none` for the iframe) | |
| `HARP_ALLOW_HTTP` | Accept logins over plain HTTP (never on a shared server) | off |
| `HARP_OSC_QUEUE_PROBE` | Refresh live OSC Slurm partitions over noninteractive SSH | off |
| `HARP_OSC_SSH_USER` | OSC username used only by the live partition probe | unset |
| `HARP_OSC_SSH_KEY`, `HARP_OSC_SSH_KNOWN_HOSTS` | Mounted SSH key and pinned host-key files | unset |
| `HARP_QUEUE_REFRESH_SECONDS` | Live partition refresh interval | `86400` (24 hours) |
| `HARP_QUEUE_MAX_AGE_SECONDS` | Stop trusting a live snapshot after this age | `172800` (48 hours) |

## Deploy as an ICICLE Tapis Pod (TapisUI)

Build and publish the server image ([`harp_server/Dockerfile`](https://github.com/ICICLE-ai/HARP-UI/blob/main/harp_server/Dockerfile)), create the `harpdata` volume, and register the Pod template and Pod with [`deploy/deploy_pod.py`](https://github.com/ICICLE-ai/HARP-UI/blob/main/deploy/deploy_pod.py):

```bash
docker build -f harp_server/Dockerfile -t ghcr.io/icicle-ai/harp-ui:2.0.0 .
docker push ghcr.io/icicle-ai/harp-ui:2.0.0

export TAPIS_BASE_URL=https://icicleai.tapis.io
export TAPIS_ACCESS_TOKEN='<token>'
export HARP_IMAGE=ghcr.io/icicle-ai/harp-ui:2.0.0
python deploy/deploy_pod.py
curl https://harp.pods.icicleai.tapis.io/healthz      # {"status":"ok"}
```

Full steps, portal settings and operational constraints (run a single replica) are in [`deploy/README.md`](https://github.com/ICICLE-ai/HARP-UI/blob/main/deploy/README.md).

When configured, HARP runs `sinfo` on Ascend, Pitzer, and Cardinal at Pod startup and once every 24 hours. A successful snapshot remains usable for up to 48 hours, allowing one temporary probe failure without immediately hiding queue validation. Live Slurm output—not OSC's documentation—is used to validate each TAPIS `hpcQueueName`. The probe requires a dedicated Pod-mounted SSH identity and invokes only this fixed read-only command; HARP cannot derive SSH credentials from a TAPIS access token and never persists that token.

> **Screenshot slot — `docs/images/howto-pod-deployment.png`:** Show the HARP Pod or template in the Tapis Pods interface with a healthy status and the approved image reference. Redact tenant administration details.

## Run the tests

```bash
cd harp_server && python3 -m pytest -q tests
```

The tests use an in-memory fake of Tapis ([`tests/fake_tapis.py`](https://github.com/ICICLE-ai/HARP-UI/blob/main/harp_server/tests/fake_tapis.py)); the job runner is tested by really running the Euler example.

## Rebuild the offline demo

After changing [`profiling.html`](https://github.com/ICICLE-ai/HARP-UI/blob/main/profiling.html), regenerate the demo copy with `python3 DEMO/ui/build_demo.py`.
