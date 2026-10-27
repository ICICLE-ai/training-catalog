---
tags:
  - AI4CI
  - CI4AI
  - Software
title: "Video Segmentation and Tracking: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for Video Segmentation and Tracking. Segment objects in a video by annotating a few keyframes, then track every object through the whole video…"
---
# Explanation

### Architecture

```
Browser (Smart Labeler client)
  │  @icicle-ai/video-segmentation
  │
  ├── SAM3 Video Service (GPU node) ──── upload, frame extraction, tracking jobs,
  │      (optionally behind the            MP4 / COCO rendering
  │       auth gateway)
  │
  ├── Auth gateway ──────────────────── Tapis sign-in, dataset export to HPC
  │
  └── Tapis Files API ───────────────── HPC video download, MP4 / COCO save
```

![Architecture](https://raw.githubusercontent.com/ICICLE-ai/smart_labeler/main/docs/images_video_segmentation/architecture.svg)

The workspace is the `@icicle-ai/video-segmentation` package. The client route supplies only the pipeline ID and the Tapis token. All calls to the SAM3 Video Service go through one typed client, `sam3VideoClient.ts`.

### Keyframes and Tracking

You annotate a few keyframes; the SAM3 video tracker propagates each object's mask through the rest of the video. Each object has a stable ID shared across keyframes, which tells the tracker the masks belong to the same object. With **Track both directions**, an object is followed backward from its earliest keyframe as well as forward.

Tracking runs as a job on the service. Progress streams to the browser over Server-Sent Events and falls back to polling when a proxy buffers or strips the stream. A new job replaces the previous results.

### Frame Indexing and Chunks

Frames are addressed by the service's **decoded frame index**, never by timestamp × frame rate. That is why the workspace fetches frames as images rather than playing the video in a video element: on a variable-frame-rate recording, a timestamp would drift away from the frame the tracker means.

Long videos are split into chunks of about a thousand frames. Opening a chunk extracts its frames on the service. The frame browser fetches only the frame you settle on, cancels requests you have scrolled past, and pre-fetches neighbouring frames once the current one has loaded — frames often travel over an SSH tunnel.

### Authentication

On a direct connection, requests carry no credentials. The bare service allows any origin, and browsers refuse credentialed requests to a wildcard origin.

Behind the auth gateway, the Tapis token is exchanged for a session cookie, which also authenticates the progress stream (`EventSource` cannot send custom headers). The token is additionally sent as an `X-Tapis-Token` header on every request, so the workspace still works when embedded in another site that blocks third-party cookies. An expired session is renewed automatically.

### Output Formats

- **Annotated MP4** — the source video with coloured masks drawn on it, for review and sharing.
- **COCO JSON** — per-frame instance masks for every tracked object, compatible with tools such as CVAT and Roboflow and frameworks such as MMDetection and Detectron2.
- **Dataset archive (`.tar`)** — the extracted frames plus, when a tracking job has finished, its masks and COCO JSON. Built and written to HPC by the gateway so hundreds of megabytes never pass through the browser.

### Limitations

- Resume state lives in the browser's `localStorage`, so it does not follow you to another device.
- The service runs one tracking job at a time.
- The annotated MP4 is rendered on first request and can take several minutes for long videos.
- Dataset export to HPC requires the auth gateway.
