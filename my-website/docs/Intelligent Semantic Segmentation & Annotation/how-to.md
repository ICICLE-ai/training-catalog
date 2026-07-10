---
tags:
  - AI4CI
  - Software
---
# How-To Guides

### How to Create a Segmentation Pipeline

1. From the **Dashboard**, click **+ New Pipeline**.
2. Enter a **Pipeline Name** and a valid **SLURM Account**.
3. Optionally add a **Description**.
4. Click **Create & Open** — the Image Annotator canvas opens immediately.

### How to Upload Images to the Cluster

1. From the **Dashboard**, click **Upload Data**.
2. Select a **Target System** from the dropdown (e.g. Pitzer (OSC)).
3. Enter or browse to an absolute **Destination Path** on that system.
4. Drag and drop files into the upload zone, or click **Select Files** / **Select Directory**.
5. Click **Upload** to transfer.

### How to Use Smart Click (SAM3-Assisted Masking)

1. Open an image in the annotation canvas.
2. Click the **Smart Click** tool (magic wand / wand-with-sparkle icon) in the toolbar.
3. Select **Single Click** mode and enter a label, then click on an object to generate its mask automatically.
4. Optionally enable **SAHI** and adjust **Crop Size** for better coverage of small objects in large images.
5. Click **Enter** to apply.

### How to Use Text Prompt Annotation

1. Open an image in the annotation canvas.
2. Click the **Smart Click** tool and switch mode to **Text Prompt**.
3. Enter a comma-separated list of class names (e.g. `zebra, giraffe`).
4. Optionally enable **SAHI** for improved small-object recall.
5. Click **Enter** — SAM3 generates masks for all detected instances of those classes.

### How to Flag Masks for Review

1. In the right panel, locate the mask in the **Masks** list.
2. Click the flag icon next to a mask entry to mark it as **Needs Review**.
3. Use the **Filter by Flag** section at the top of the right panel to show only flagged masks.
4. Add custom flag names using the **New flag name...** field and the **+** button.

### How to Filter Masks by Label or Flag

- Click any label chip in the **Filter by Label** section to show only masks of that class.
- Click any flag chip in the **Filter by Flag** section to show only masks with that flag.
- Clicking an active chip again deselects it and shows all masks.

### How to Remove Low-Confidence Masks

1. Adjust the **Confidence** slider in the right panel to the desired threshold.
2. Click **Remove masks below score: X.XX** to permanently delete all masks under that threshold.

### How to Save Annotations to the Cluster

1. Click the **Save** (floppy disk) icon in the toolbar.
2. Select a cluster system from the dropdown.
3. Enter the full remote **File Path** (e.g. `/path/to/save/annotations.json`).
4. Toggle **COCO JSON** on or off to select the output format.
5. Click **Save**.

### How to Import Existing Annotations

1. Click the **Import** (upload arrow) icon in the toolbar.
2. Select the cluster from the dropdown or click **Browse File** to upload from your local machine.
3. Enter the remote path in **Or Enter File Path** if the file is already on the cluster.
4. Toggle the format switch to match your file (**COCO JSON** or **Default JSON**).
5. Click **Upload**.

### How to Download Annotations Locally

Click the **Download** icon in the toolbar and select **COCO JSON** or **Default JSON**. The file is saved directly to your local machine.

### How to Resume a Segmentation Pipeline

From the **Dashboard**, find the pipeline by name or ID using the search bar. Click **Open Pipeline** on the pipeline card to return to the Image Annotator at the current state.

### How to Set Up Hugging Face Access

Some models used by Smart Labeler (SAM3) are gated on Hugging Face and require an account, approved access, and a personal token. Complete all four steps in order.

#### Step 1 — Create a Hugging Face Account

Go to [huggingface.co](https://huggingface.co) and click **Sign Up**. Enter your email, choose a username and password, and verify your email address. Complete your profile (name, organization if applicable).

> **Tip:** Use a professional or institutional email address — it improves your chances of approval for gated models. If you already have an account, skip to Step 2.

#### Step 2 — Request Access to SAM3

SAM3 is a gated model hosted by Meta. You must agree to their usage terms before you can use it.

1. Open the SAM3 model page: [huggingface.co/facebook/sam3](https://huggingface.co/facebook/sam3)
2. Click **Request Access** and fill in your details (first name, last name, date of birth, country, affiliation, job title).
3. Accept the Meta Privacy Policy terms and click **Submit**.
4. You will see a confirmation that your request is pending review.
5. Once approved, the model page shows: *"Gated model — You have been granted access to this model."*

> **Tip:** You will receive an email when approved. Check your spam folder if you don't see it after 24 hours.

#### Step 3 — Generate a Hugging Face Access Token

Once your access request is approved, generate an API token so Smart Labeler can authenticate model downloads on your behalf.

1. Navigate to your token settings: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **+ Create new token**.
3. Set the **Token Type** to **Read** and give it a descriptive name (e.g., `ICICLE-TapisAccess`).
4. Click **Create token** and copy the value immediately — it is only shown once.

> **Warning:** Treat your token like a password. Do not share it or commit it to a repository. If you lose it, revoke it and generate a new one from the same settings page.

#### Step 4 — Add the Token in ICICLE / Tapis

With your token ready, add it to your ICICLE/Tapis credentials so it can be injected securely into HPC jobs.

1. Log in to your ICICLE/Tapis account.
2. Navigate to the **Settings** section indicated by 3 dots on the dashboard.
3. Click on **Access Key**.
4. Paste your token and save.
5. Click on **Revoke token** to permanently delete the token if needed.
