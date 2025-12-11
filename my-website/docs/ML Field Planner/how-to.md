---
tags:
  - Software
  - CI4AI
  - Animal Ecology
---
# How-To Guide

## How-To Run on the ICICLE Instance

The ICICLE instance of the ML Field Planner is accessible [here](https://icicleai.tapis.io/).

1. You can either login with your TACC account or via CILogin. ![Login](https://github.com/ICICLE-ai/mlfieldplanner/raw/main/imgs/login.png)
2. Once logged in, navigate to the Camera Traps Edge Simulator Dashboard by selected `ML Edge` on the left side menu and then clicking on the `Go to Analysis Environment` box. ![Edge simulation](https://github.com/ICICLE-ai/mlfieldplanner/raw/main/imgs/analysis.png)
3. To prepare an analysis run, first select a select. You can either choose a model from the dropdown menu or click the `provide model id` button above the dropdown. We currently only support Patra model card IDs, you can find a list of models by navigating to `ML Hub` --> `models` and choosing `Patra` as the `Platform`. ![ML Hub](https://github.com/ICICLE-ai/mlfieldplanner/raw/main/imgs/ml_hub.png)
4. After the model has been selected, choose a dataset to run the model against. There is a button to choose between a video or image dataset. For both, we provide example datasets, but if you would like to test against your own data, select `provide dataset id` and provide a url to your dataset.
5. Next, select a site to run the experiment from the dropdown. The ICICLE deployment of ML Field Planner has access to hardware at two sites, Chameleon and TACC, each with different types of hardware available.
6. After selecting the site, select the type of hardware to run on.
7. Finally, to run the ML pipeline with any advanced features provide a JSON in the `Advanced Config` text field. For a list of features supported by the Camera Traps Edge Software, see the [README](https://github.com/tapis-project/camera-traps/tree/main/installer/README.md).
8. Click the `Analyze` button to being the analysis. ![Example anaysis form](https://github.com/ICICLE-ai/mlfieldplanner/raw/main/imgs/analysis_filled.png)
9. You should see your analyses, including this one experiments under the submission button in the `Analyses` table. From the table, you can view the status of the job and even jump to an archive of the run directory. Note the `UUID` of the experiment. ![Submitted analysis jobs](https://github.com/ICICLE-ai/mlfieldplanner/raw/main/imgs/analyses.png)
10. To view metrics captured by the CKN, select the `CKN Dashboard` on the left menu and then select `Camera Traps`. Choose your username in the first dropdown and then choose your experiment UUID in the second dropdown. ![CKN dashboard](https://github.com/ICICLE-ai/mlfieldplanner/raw/main/imgs/ckn_dashboard.png)
