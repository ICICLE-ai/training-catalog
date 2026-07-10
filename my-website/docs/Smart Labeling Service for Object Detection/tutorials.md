---
tags:
  - CI4AI
  - AI4CI
  - Software
---
# Tutorials

### Running Your First Detection Pipeline

A complete walkthrough from raw images to labeled detections in 7 steps.

#### Prerequisites

- Access to a Tapis-connected HPC system (Pitzer, Expanse, Ascend, or Cardinal)
- A Tapis account with a valid Slurm account to charge.
- A directory of images on a Tapis filesystem
- (Optional) A Hugging Face token for gated models such as SAM3 or BioClip

#### Getting Started

Navigate to the home page and click **Get Started** or **Dashboard**.

![Home Page](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images2/home_page_sl.png)

From the dashboard you can create a new pipeline or resume an existing one.

![Dashboard](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images2/dashboard_sl.png)

Click **Create New Pipeline**, enter a pipeline name, select the job type (*Object Detection*), and provide a Slurm account. Click **Create New Job**.

![Create New Pipeline](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images2/dashboard_new_pipeline_sl.png)

![Create New Pipeline Form](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images2/dashboard_create_new_sl.png)

In order to upload data from your system to HPC click on upload button.

![Upload Files](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images2/upload_files.png)

#### Step 1 — Annotate Images

Open **Step 1 — Image Annotator** from the pipeline navigation bar.

![Annotator Interface](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/annotator/Annotator-initial.png)

In the **File Explorer** panel, select a compute system and enter the path to your image directory. Click **Get Images**.

![File Explorer](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/annotator/File-explorer.png)

Click any image thumbnail to open it in the canvas. Draw bounding boxes by clicking and dragging on the canvas, then assign a label to each box.

![Annotation Canvas](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/annotator/annotator.png)

To use SAM3 assisted annotation, select **Single Click** mode, enter a label, then click an object in the image to auto-generate a box.

![SAM3 Single Click](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/annotator/SAM3-single-click.png)

Or use **Text Prompt** mode to run prediction over the whole image from a comma-separated label list.

![SAM3 Text Prompt](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/annotator/SAM3-text-prompt.png)

When finished, click **Save Annotations** and choose a remote Tapis path to store the COCO JSON file.

#### Step 2 — Generate Class Supports

Open **Step 2 — Generate Class Supports**.

![Generate Class Supports](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/class_supports/generate_class_support.png)

Enter a job name, select Proposer and Embedder models from the Patra catalog, and set crop/patch sizes (e.g. `[2048, 1024, 512]`). Click **Submit** and monitor job progress in the pipeline status bar.

#### Step 3 — Optimize Patch Size

Open **Step 3 — Optimize Patch Size** once the Step 2 job finishes. Use the File Explorer to navigate your images. Click each result file in the right panel to compare ground-truth vs. predicted boxes for each crop size.

![Optimize Patch Size](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/class_supports/optimize_patch_size.png)

Check the **IoU Graph** to identify which patch size produces the highest scores.

![IoU Graph](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/class_supports/optimize_patch_size_graph.png)

Note the optimal patch size and proceed to the next step.

#### Step 4 — Configure Detection Job

Open **Step 4 — Configure Detection Job**. Enter a configuration name, provide a query image path or directory, select models and thresholds, and optionally enable SAHI tiling. Click **Submit** to queue the detection job.

![Configure Detection Job](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/proposals/configure_detection_job.png)

![Configure Detection Job — Advanced](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/proposals/configure_detection_job_2.png)

![Configure Detection Job — HPC configuration](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images2/proposal_config_3.png)

#### Step 5 — Visualize Proposals

Open **Step 5 — Visualize Proposals** once the detection job completes. Select a proposal file from the right panel. Drag the objectness threshold slider to filter boxes in real time.

![Visualize Proposals](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/proposals/visualize_proposals.png)

Use the **Objectness Score Graph** to find a natural cutoff point.

![Objectness Score Graph](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/proposals/visualize_proposals_graph.png)

Click **Save** to store the threshold for use in classification.

#### Step 6 — Configure Classification Job

Open **Step 6 — Configure Classification Job**. Add one or more Proposal → Class Support tensor mappings using the **Add Mapping** button. Set a similarity threshold and click **Submit**.

![Configure Classification Job](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/classification/configure_classification_job.png)

#### Step 7 — Review Results

Open **Step 7 — Object Classification**. Select a result file from the right panel and navigate images using the File Explorer. Drag the similarity threshold slider to filter results in real time. Click **Download** to export as COCO JSON or pipeline-native JSON.

![Classification Results](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/doc/images/classification/visualize_classifications.png)
