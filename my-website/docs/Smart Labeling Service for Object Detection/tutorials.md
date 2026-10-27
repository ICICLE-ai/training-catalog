---
tags:
  - CI4AI
  - AI4CI
  - Software
title: "Smart Labeling Service for Object Detection: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for Smart Labeling Service for Object Detection. A 7-step HPC-backed pipeline for few-shot object detection — from interactive image annotation…"
---
# Tutorials

### Running Your First Detection Pipeline

A complete walkthrough from raw images to labeled detections in 7 steps.

#### Prerequisites

- Access to a Tapis-connected HPC system (Pitzer, Expanse, Ascend, or Cardinal)
- A Tapis account. Jobs are charged to a Slurm allocation — either your own, or the shared community allocation that is filled in by default (see below).
- A directory of images on a Tapis filesystem
- (Optional) A Hugging Face token for gated models such as SAM3 or BioClip

#### Getting Started

Navigate to the home page and click **Get Started** or **Dashboard**.

![Home Page](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images2/home_page_sl.png)

From the dashboard you can create a new pipeline or resume an existing one.

![Dashboard](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images2/dashboard_sl.png)

Click **Create New Pipeline**, enter a pipeline name, select the job type (*Object Detection*), and provide a Slurm account. Click **Create New Job**.

![Create New Pipeline](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images2/dashboard_new_pipeline_sl.png)


The **SLURM Account** field is pre-filled with `uot260`, a shared **community allocation** on **Expanse (SDSC)**. It is the quickest way to get started, but because it is shared, **data you upload under it can be seen by other users of the service**. For a private allocation of your own, use the request link in the form (it opens an email to the allocation contact), then enter your own account code. When you enter a different account, the form reminds you that jobs will be rejected if you do not have access to it.

In order to upload data from your system to HPC click on upload button.

![Upload Files](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images2/upload_files.png)

#### Step 1 — Annotate Images

Open **Step 1 — Image Annotator** from the pipeline navigation bar.

![Annotator Interface](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/annotator/Annotator-initial.png)

In the **File Explorer** panel, select a compute system and enter the path to your image directory. Click **Get Images**.

![File Explorer](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/annotator/File-explorer.png)

Click any image thumbnail to open it in the canvas. Each filename shows a badge with its annotation count, plus a flag icon when any annotation on it is flagged. Use the **Annotated** and **Flagged** filter chips above the list to show only those images; the arrow keys then step through just the filtered images.

Draw a bounding box either way — there is no mode to switch:

- **Two clicks** — click one corner, then the opposite corner. The box previews under the cursor in between. Press **Enter** to close it at the previewed corner, or **Esc** to abandon it.
- **Click-drag** — press, drag, and release.

Each new box asks for its label. To skip that question, pick a label under **Label for new annotations** in the right panel (or type a new label name to start a new class). Every box you draw then takes that label straight away. Click the armed label again to go back to being asked.
![Add Label](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/annotator/add_label.png)
![Annotation Canvas](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/annotator/annotator.png)

Clicking an annotation in the right panel pans the canvas until that annotation is centred, without changing the zoom. Selecting a box on the canvas scrolls its row into view in the panel. Panning is bounded, so the image can no longer be dragged out of view at high zoom, and wheel zoom anchors on the pointer.

The **confidence** slider starts at the lowest score on the current image, so no annotation is hidden when the image opens. It resets for each new image. If new results arrive that score lower than anything already on the image (for example a SAM3 run at a lower detection confidence), the slider moves down to include them.

**Delete all** and **delete all with this label** ask for confirmation first, stating how many annotations will be removed from the current image. Nothing is written to disk until you save.

To use SAM3 assisted annotation, select **Single Click** mode, enter a label, then click an object in the image to auto-generate a box.

![SAM3 Single Click](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/annotator/SAM3-single-click.png)

Or use **Text Prompt** mode to run prediction over the whole image from a comma-separated label list.

![SAM3 Text Prompt](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/annotator/SAM3-text-prompt.png)

The **Detection Confidence** and **Mask Precision** set in the SAM3 dialog are applied to both Single Click and Text Prompt requests.

When finished, click **Save Annotations** and choose a remote Tapis path to store the annotation file. See [How to Save and Download Annotations](#how-to-save-and-download-annotations).

#### Step 2 — Generate Class Supports

Open **Step 2 — Generate Class Supports**.

![Generate Class Supports](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/class_supports/generate_class_support.png)

Enter a job name, select Proposer and Embedder models from the Patra catalog, and set crop/patch sizes (e.g. `[2048, 1024, 512]`). Click **Submit** and monitor job progress in the pipeline status bar.

Before the job is sent to HPC, Smart Labeler checks with Tapis that the image and annotation paths exist and that you can read them, and that you have access to the output directory (it does not need to exist yet). If any path is unusable, the job is **not submitted** and one message lists every path that is wrong. See [Job Submission Checks](#job-submission-checks).

#### Step 3 — Optimize Patch Size

Open **Step 3 — Optimize Patch Size** once the Step 2 job finishes. Use the File Explorer to navigate your images. Click each result file in the right panel to compare ground-truth vs. predicted boxes for each crop size.

![Optimize Patch Size](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/class_supports/optimize_patch_size.png)

Check the **IoU Graph** to identify which patch size produces the highest scores.

![IoU Graph](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/class_supports/optimize_patch_size_graph.png)

Note the optimal patch size and proceed to the next step.

#### Step 4 — Configure Detection Job

Open **Step 4 — Configure Detection Job**. Enter a configuration name, provide a query image path or directory, select models and thresholds, and optionally enable SAHI tiling. Click **Submit** to queue the detection job. The query image path and the output directory are checked before submission, as in Step 2.

![Configure Detection Job](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/proposals/configure_detection_job.png)

![Configure Detection Job — Advanced](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/proposals/configure_detection_job_2.png)

![Configure Detection Job — HPC configuration](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images2/proposal_config_3.png)

#### Step 5 — Visualize Proposals

Open **Step 5 — Visualize Proposals** once the detection job completes. Select a proposal file from the right panel. Drag the objectness threshold slider to filter boxes in real time.

![Visualize Proposals](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/proposals/visualize_proposals.png)

Use the **Objectness Score Graph** to find a natural cutoff point.

![Objectness Score Graph](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/proposals/visualize_proposals_graph.png)

Click **Save** to store the threshold for use in classification.

#### Step 6 — Configure Classification Job

Open **Step 6 — Configure Classification Job**. Give the job a **Job Name**, add one or more Proposal → Class Support tensor mappings using the **Add Mapping** button, set a similarity threshold, and click **Submit**.

- The **class support** dropdown only offers files built with the same embedding model (e.g. DINOv3, BioClip) as the selected proposal tensor, since embeddings from different models cannot be compared. Changing the proposal clears a class support that no longer matches. If no class support file uses the proposal's embedder, every file is offered and the row says so.
- The section warns before you submit if a mapping is missing either file, or if the same proposal tensor is mapped twice, naming the rows to fix.
- The classification job keeps its own name; submitting it no longer renames the proposal configuration it runs against.

![Configure Classification Job](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/classification/configure_classification_job.png)

#### Step 7 — Review Results

Open **Step 7 — Object Classification**. Select a result file from the right panel and navigate images using the File Explorer. Drag the similarity threshold slider to filter results in real time. Click **Download** to export as COCO JSON or pipeline-native JSON.

![Classification Results](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images/classification/visualize_classifications.png)
