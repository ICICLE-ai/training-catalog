---
tags:
  - AI4CI
  - CI4AI
  - Software
title: "Video Segmentation and Tracking: Tutorials"
sidebar_label: "Tutorials"
pagination_label: "Tutorials"
description: "Tutorials for Video Segmentation and Tracking. Segment objects in a video by annotating a few keyframes, then track every object through the whole video with…"
---
# Tutorials

### Tracking Your First Video

A complete walkthrough from a raw video to tracked masks in 5 steps.

#### Prerequisites

- A Tapis account with a valid Slurm account to charge
- A running SAM3 Video Service, reachable either through the deployment's auth gateway or an SSH tunnel to a GPU node (see [How to Connect to the SAM3 Video Service](#how-to-connect-to-the-sam3-video-service))
- A video file (MP4 recommended) on your computer or on a Tapis-connected HPC system
- (Optional) A Hugging Face token with SAM3 access, if your deployment downloads the model on your behalf — see [How to Set Up Hugging Face Access](https://github.com/ICICLE-ai/smart_labeler/blob/main/SEGMENTATION_README.md#how-to-set-up-hugging-face-access)

#### Getting Started

Navigate to the home page and click **Get Started** or **Dashboard**.

![Home Page](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/home_video.png)

On a segmentation deployment, the dashboard lists pipelines under two tabs: **Images** and **Videos**. Open the **Videos** tab to see existing video pipelines, each with its ID and an **Open Pipeline** button.


Click **+ New Pipeline** to open the creation modal. Provide a **Pipeline Name** and a **SLURM Account** (required). Under **What will you annotate?**, choose **Video — segment and track through a video**. This choice fixes which workspace the pipeline opens in and cannot be changed later. Add an optional **Description** and click **Create & Open**.

![New Video Pipeline Modal](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/new_pipeline_video.png)

The video workspace opens with a five-step guide across the top: **Upload video → Add objects → Annotate keyframes → Track → Review & export**. The hint under the stepper changes with the active step. Click the **?** icon for a short primer on how tracking works.

![Workflow Steps](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/workflow_steps.png)

#### Checking the Service Connection

Before anything else, the workspace contacts the SAM3 Video Service and shows the result under the stepper:

- **GPU service connected** — ready to go. The model backend, model ID, and device are shown alongside.
- **Signed in as \<user\>** — shown when the deployment uses the auth gateway.
- **Mock mode — placeholder masks, not real tracking** — the service is running without the model. Masks are not real.
- **Loading model weights — first track may be slow** — the service has just started. The first tracking job will wait for the model.
- **Video GPU service unavailable** — the service could not be reached. The message names the address tried. Fix the connection and click **Retry**.

![Service Connected](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/service_connected.png)


#### Step 1 — Upload Video

Choose where the video comes from:

- **This computer** — drag a video onto the drop zone, or click it to browse. A progress bar shows the upload.
- **HPC storage** — pick a **System**, then enter the **Video file path** or click the browse icon to find it. The video is downloaded from Tapis and sent on to the GPU service, with progress shown for both stages.

![Upload — HPC Storage](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/upload_hpc.png)

The service decodes the video and reports its frame count, resolution, and frame rate. Long videos are split into **chunks** of about a thousand frames.

If the upload fails, the message explains the cause. The most common one, **That video file looks incomplete**, means the MP4 is missing its index — usually because it was still being copied or recorded. Re-copy the file and try again.

#### Step 2 — Add Objects

Each thing you want tracked is an **object** with a label and a colour. Objects keep the same ID on every keyframe, which is how the tracker knows they are the same thing.

You can add objects up front in the **Objects** panel on the right, or let the workspace ask as you draw (see Step 3). From the panel you can rename an object, remove its mask on the current frame, or delete the object along with all its masks.

![Objects Panel](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/objects_panel.png)

#### Step 3 — Annotate Keyframes

You annotate a **few keyframes**, not every frame. The tracker follows each object through the rest of the video.

##### Browsing Frames

Use the frame browser under the canvas:

- **Chunk selector** — switch between chunks of a long video. Opening a new chunk extracts its frames on the service first, so the slider pauses briefly.
- **Frame slider** — the frame loads when you release the slider.
- **Previous / Next frame** buttons — step one frame at a time.
- **Keyframe markers** — frames you have already annotated are marked on the slider.

Frames are numbered by **decoded frame index**, straight from the service. The elapsed time shown is approximate on variable-frame-rate recordings; the frame number is the exact reference.

<!-- TODO: screenshot of the frame browser with keyframe markers -->
![Keyframe Annotation](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/keyframe_annotation.png)

##### Drawing Masks

Scrub to a frame where the object is clearly visible, then draw it with either tool:

- **Polygon tool** — click points around the object. Press **Enter** or click the first point to close the polygon.
- **SAM3 click** — click on the object and SAM3 generates its mask.

If an object is selected in the **Objects** panel, the new mask goes straight to that object. Otherwise the **Assign this region** dialog opens: pick an existing object, create a new one by typing a label (e.g. `torch`, `weld_pool`), or click **Discard region**.

![Assign Region Dialog](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/ai_assisted_annotation.png)

> **Tip:** Annotate a few keyframes spread across the video, especially where an object changes shape, is partly hidden, or reappears. An object can first appear on any keyframe; it is tracked backward from there too, so you do not need to find its first frame.

Keyboard shortcuts: **Enter** closes a polygon, **Esc** cancels the current tool, **Delete** removes the selected mask.

#### Step 4 — Track

In the **Track** panel:

- **Track both directions** (default) follows each object forward and backward from its keyframes. Switch it off to **Track forward only**.
- **Track a frame range only** limits tracking to a **Start** and **End** frame. The arrow buttons set either one to the frame currently on screen.

Click **Segment & track video**. Tracking runs on the GPU, one job at a time. Progress is shown by chunk and frame, and you can cancel the job at any time.

![Track Controls](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/track_controls.png)

![Tracking Progress](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/tracking_progress.png)

> **Note:** The first job after the service starts can sit at 0 frames for a minute or two while SAM3 loads. If a running job reports no progress for a long time, the panel shows a **No progress for a while** warning.

#### Step 5 — Review & Export

##### Reviewing Results

Scrub through the video to check the tracked masks. Toggle between:

- **Overlay** — masks drawn on top of the frame.
- **Side by side** — the masked frame next to the untouched frame for comparison.

![Results — Overlay](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/results_overlay.png)


If a mask drifted, go to that frame, correct it on the annotation canvas, and click **Track again**. The corrected frame becomes a new keyframe that re-anchors the object. Re-tracking starts a new job that replaces the previous results.

##### Exporting

The **Export** panel offers two files for a finished job. Each can be downloaded to your computer or sent **To HPC**:

- **Annotated MP4** — the video with masks drawn on it. The service renders it on first request, so expect a wait on long videos.
- **COCO JSON** — per-frame masks for every object, ready for training frameworks.

Choosing **To HPC** opens a dialog to pick a **System**, a **Destination folder** (blank for your home directory), and a **Filename**.

![Export Panel](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/export_panel.png)

##### Exporting a Dataset to HPC

To build a training dataset, use **Export dataset to HPC**. Pick a **System**, a **Destination folder**, and an **Archive name** (default `<video>_dataset.tar`). The gateway extracts every frame and, if a tracking job has finished, adds its masks and COCO JSON, then writes the `.tar` straight to HPC. Unpack it with `tar xf <file>`.

Progress moves through **Extracting frames from the video → Collecting masks and building the archive → Uploading to HPC**. The export runs on the server, so you can close the tab or switch pipelines; progress is picked back up when you return.
