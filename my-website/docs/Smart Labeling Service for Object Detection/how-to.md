---
tags:
  - CI4AI
  - AI4CI
  - Software
title: "Smart Labeling Service for Object Detection: How-To Guides"
sidebar_label: "How-To Guides"
pagination_label: "How-To Guides"
description: "How-To Guides for Smart Labeling Service for Object Detection. A 7-step HPC-backed pipeline for few-shot object detection — from interactive image annotation…"
---
# How-To Guides

### How to Import Existing Annotations

1. In the **Image Annotator** (Step 1), click **Import Annotations**.
2. Choose **Browse** to upload a local file, or enter a remote Tapis filesystem path.
3. Select the file format (**COCO JSON** or **Default JSON**) using the Format Switch.

![Import Annotations](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/annotator/import_annotations.png)

After the import, a summary dialog reports how many images, annotations and labels the file contains, and how many of them landed on the images currently loaded:

- **Annotations imported** — the file matched your loaded images.
- If some entries belong to folders you have not opened yet, the dialog lists those folders' full paths. Paste one into **Source Image Directory** in the File Explorer and its annotations are applied.
- **Nothing to import** or **Import failed** — the dialog explains why, including when the file looks like the other format, with sample image paths from the file and from the explorer so a path mismatch is easy to spot.

You can import several files in one session. Each import is layered on top of the previous ones (later files win for the same image), and saving keeps the annotations for folders you never opened. The format of the pipeline's own annotation file is detected from its contents when the annotator opens, so a file saved in a different format still loads. An import you start yourself is never overwritten by the pipeline's annotation file loading late.

### How to Save and Download Annotations

Click **Save Annotations** to write to a remote Tapis path, or **Download** to export to your local machine.

![Save Annotations](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/annotator/save_annotations.png)

![Download Annotations](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/annotator/download_annotations.png)

Both options support **COCO JSON** and **Default JSON** formats via the Format Switch.

In **Save As**, click **Browse** to pick a folder on the system. The filename is filled in as `annotation_<YYYYMMDD-HHMMSS>.json` (or `.coco.json` in COCO mode). Switching the format updates the extension of a generated name but leaves a name you typed yourself alone. The annotation file can be on a different system from the images; Smart Labeler reads it back from the system it was saved to.

If a save fails, the message says why and names the folder and system — most often a **403**, meaning you do not have write access to that folder, so pick another one. The Save As dialog stays open on a failed save, and the pipeline is not pointed at a file that was never created.

### How to Resume a Pipeline

From the **Dashboard**, use the search or filter controls to locate your pipeline. Click **Goto** to re-enter at the last completed step.

![Existing Pipelines](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images2/dashboard_existing_pipeline_sl.png)

### How to Delete a Pipeline

From the **Dashboard**, click the delete icon on the pipeline card. The pipeline is deleted immediately — there is no confirmation step. If the pipeline cannot be deleted, a **Pipeline not deleted** message explains why (with the error code, or that the server could not be reached) and the pipeline stays in the list.

### How to Check Job Status and Logs

The **pipeline status bar** appears at the top of every step. Right-click any step chip to open the context menu.

![Status Bar](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/status_bar/status_bar.png)

![Status Bar Options](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/status_bar/status_bar_options.png)

- Select **Get Status** to poll the Tapis job and view status, condition, and last message.

![Get Status Modal](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/status_bar/status_bar_get_status.png)

- Select **Get Tapis Logs** to fetch and display `tapisjob.out` from the HPC run.

![Application Logs](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/status_bar/status_bar_application_logs.png)

### How to Use SAHI Tiling for Small Objects

Enable SAHI when your images are large and objects are small (e.g., aerial imagery, microscopy).

1. In **Step 2** or **Step 4**, toggle the **SAHI** switch.
2. Set a **Tile Size** (pixels) — a good starting point is `960`.
3. Set an **Overlap Ratio** (e.g. `0.25`) so adjacent tiles share context.
4. Submit as normal. Inference runs on each tile and results are merged with NMS.

### How to Set Up Hugging Face Access

Some models used by Smart Labeler (SAM3, DINOv3) are gated on Hugging Face and require an account, approved access, and a personal token. Complete all four steps in order.

#### Step 1 — Create a Hugging Face Account

Go to [huggingface.co](https://huggingface.co) and click **Sign Up**. Enter your email, choose a username and password, and verify your email address. Complete your profile (name, organization if applicable).

> **Tip:** Use a professional or institutional email address — it improves your chances of approval for gated models. If you already have an account, skip to Step 2.

#### Step 2 — Request Access to SAM3 and DINOv3

SAM3 and DINOv3 are gated models hosted by Meta. You must agree to their usage terms before you can use them. Approval for one model does **not** grant access to the other — request each separately.

**SAM3**

1. Open the SAM3 model page: [huggingface.co/facebook/sam3](https://huggingface.co/facebook/sam3)
2. Click **Request Access** and fill in your details (first name, last name, date of birth, country, affiliation, job title).
3. Accept the Meta Privacy Policy terms and click **Submit**.
4. You will see a confirmation that your request is pending review.
5. Once approved, the model page shows: *"Gated model — You have been granted access to this model."*

**DINOv3**

1. Open the DINOv3 model page: [huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m)
2. Repeat the same access request process as for SAM3.

> **Tip:** You will receive an email when approved. Check your spam folder if you don't see it after 24 hours.

#### Step 3 — Generate a Hugging Face Access Token

Once your access requests are approved, generate an API token so Smart Labeler can authenticate model downloads on your behalf.

1. Navigate to your token settings: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **+ Create new token**.
3. Set the **Token Type** to **Read** and give it a descriptive name (e.g., `ICICLE-TapisAccess`).
4. Click **Create token** and copy the value immediately — it is only shown once.

> **Warning:** Treat your token like a password. Do not share it or commit it to a repository. If you lose it, revoke it and generate a new one from the same settings page.

#### Step 4 — Add the Token in ICICLE / Tapis

With your token ready, add it to your ICICLE/Tapis credentials so it can be injected securely into HPC jobs.

1. Log in to your ICICLE/Tapis account.
2. Navigate to the **Settings** section indicated by 3 dots on the dashboard.
![Settings](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images2/hf/dashboard_settings.png)
3. Click on Access Key.
4. Paste your token and save.
5. Click on Revoke token to permanently delete the token.
![Add or revoke token](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images2/hf/add_or_revoke_hf.png)

---

### How to Use a Gated Hugging Face Model

Some models (e.g. DinoV3, certain SAM variants) require a Hugging Face token.

![Add token](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images2/hf/gated_model_support.png)

1. When selecting a model in the Patra catalog, a prompt appears asking for your HF token.
2. Enter the token — it is stored securely in **Tapis Vault** and never exposed in logs.
3. On subsequent submissions the token is retrieved automatically from Vault and injected as `HF_TOKEN`.
4. Click **How to create one** to know how to create a Hugging Face token.
5. Click on the Request access link to be redirected to the exact model link.

### How to Export Results

1. In **Step 7**, click the **Download** icon in the results panel.
2. Choose **COCO JSON** for compatibility with tools like CVAT, Roboflow, or MMDetection.
3. Choose **Default JSON** for re-importing into a Smart Labeler pipeline.
4. Optionally save directly to a remote Tapis path instead of a local download.
