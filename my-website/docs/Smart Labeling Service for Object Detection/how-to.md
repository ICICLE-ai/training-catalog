---
tags:
  - CI4AI
  - AI4CI
  - Software
---
# How-To Guides

## How to Import Existing Annotations

1. In the **Image Annotator** (Step 1), click **Import Annotations**.
2. Choose **Browse** to upload a local file, or enter a remote Tapis filesystem path.
3. Select the file format (**COCO JSON** or **Default JSON**) using the Format Switch.

![Import Annotations](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/annotator/import_annotations.png)

## How to Save and Download Annotations

Click **Save Annotations** to write to a remote Tapis path, or **Download** to export to your local machine.

![Save Annotations](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/annotator/save_annotations.png)

![Download Annotations](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/annotator/download_annotations.png)

Both options support **COCO JSON** and **Default JSON** formats via the Format Switch.

## How to Resume a Pipeline

From the **Dashboard**, use the search or filter controls to locate your pipeline. Click **Goto** to re-enter at the last completed step.

![Existing Pipelines](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images2/dashboard_existing_pipeline_sl.png)

![Search and Select Pipeline](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/create-select-job.png)

## How to Check Job Status and Logs

The **pipeline status bar** appears at the top of every step. Right-click any step chip to open the context menu.

![Status Bar](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/status_bar/status_bar.png)

![Status Bar Options](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/status_bar/status_bar_options.png)

- Select **Get Status** to poll the Tapis job and view status, condition, and last message.

![Get Status Modal](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/status_bar/status_bar_get_status.png)

- Select **Get Tapis Logs** to fetch and display `tapisjob.out` from the HPC run.

![Application Logs](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/status_bar/status_bar_application_logs.png)

## How to Use SAHI Tiling for Small Objects

Enable SAHI when your images are large and objects are small (e.g., aerial imagery, microscopy).

1. In **Step 2** or **Step 4**, toggle the **SAHI** switch.
2. Set a **Tile Size** (pixels) — a good starting point is `960`.
3. Set an **Overlap Ratio** (e.g. `0.25`) so adjacent tiles share context.
4. Submit as normal. Inference runs on each tile and results are merged with NMS.

## How to Use a Gated Hugging Face Model

Some models (e.g. BioClip, certain SAM variants) require a Hugging Face token.

1. When selecting a model in the Patra catalog, a prompt appears asking for your HF token.
2. Enter the token — it is stored securely in **Tapis Vault** and never exposed in logs.
3. On subsequent submissions the token is retrieved automatically from Vault and injected as `HF_TOKEN`.

## How to Export Results

1. In **Step 7**, click the **Download** icon in the results panel.
2. Choose **COCO JSON** for compatibility with tools like CVAT, Roboflow, or MMDetection.
3. Choose **Default JSON** for re-importing into a Smart Labeler pipeline.
4. Optionally save directly to a remote Tapis path instead of a local download.
