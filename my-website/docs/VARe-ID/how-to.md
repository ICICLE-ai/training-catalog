---
tags:
  - Software
  - Animal Ecology
---

# How-To Guides

This section walks through how to use this repository and its features. It is split into sections based on the types of tasks you're looking to accomplish.

## Setting up a Python Environment
You'll need to setup a python envionment that meets the requirements layed out in `environment.yaml`. There's several package managers that revolve around **conda** as well as the more-efficient reimplementation **mamba**. Pick your favorite and use its documentation to set up an environment. To setup the environment, you'll need to do a command similar to the following:

From the parent directory...

| Package Manager | Command |
| ----------- | ----------- |
| conda (Miniconda/Anaconda) | `conda env create -n [env name] -f environment.yaml` |
| mamba | `mamba create -n [env name] -f environment.yaml` |

The choice of what package manager to use is up to you.

### Activate your environment:
The commands to activate your envioronment are as follows:

| Package Manager | Command |
| ----------- | ----------- |
| conda (Miniconda/Anaconda) | `conda activate [env name]` |
| mamba | `mamba activate [env name]` |

## Setting up a Configfile
Please follow the instructions provided by comments in `config.yaml`. You can directly edit and use this file if you wish, but we **highly recommend** filling out a copy. This way, you can save the configs for each experiment and refer to them later (or run several experiments at once). 

Unless you'd like to customize the exact output filenames and directories, the following config fields matter the most:

The following fields are **required**:
- `data_dir_out`: This is the output directory to save to.
- `data_dir_in`: This is the input directory to read to.
- `data_video`: This is a boolean (True/False) specifying whether to process image or video data.

The following fields are **optional** and either have default (recommended) values already in the configfile or are blank (fully optional):
- `dt_gt_file` and `dt_filtered_out_file`: In the case that you're running image data with ground truth data, you can find and filter detections by IOU (Intersection over Union) with the ground truth detections.
- `fs_stage1_out_file`: This field, if supplied, will save an additional output from frame sampling after its first stage.
- `lca_separate_viewpoints`: This field specifies whether to split and save annotation files by each viewpoint or to save them alltogether. **In video mode, this MUST be True!**

## Running the Pipeline
To run the pipeline, you'll execute `snakefile.smk`. Remember: the pipeline does NOT run postprocessing. This is run separately.

**Please run the snakefile from the parent directory in this repository.** For more information on how to run a snakefile (e.g. available flags), please view the [Snakemake Docs](https://snakemake.readthedocs.io/en/stable/executing/cli.html). The most important flags you'll need to specify are as follows: 

| Flag | Function |
| ----------- | ----------- |
| -s | The path to the snakefile, which should be `snakefile.smk` |
| --cores | The number of CPU cores you'd like to run on. |
| --configfile | The path to the configfile you're using. Defaults to `config.yaml` if not provided. |

Put it together, your command will look like the following:

```
snakemake -s snakefile.smk --cores 1 --configfile path/to/your_config.yaml
```

Note that your configfile can be supplied by any filepath, relative or absolute.

**As long as you use separate config files between executions, it is safe to run several processes simultaneously.**

### The `--unlock` Flag:
Sometimes you won't be able to execute the snakefile and you'll get an error telling you to unlock the DAG (DAG is the workflow as a directed acyclic graph). This may happen if the process unexpectedly stops (such as timing out on a HPC cluster) and no error is reciprocated back to the snakefile. In order to solve this, you'll need to run a command similar to the following:

```
snakemake -s snakefile.smk --unlock
```

## Running an Algorithm Component in Isolation
Sometimes you don't want to run the full pipeline but rather just a specific algorithm step. There's two ways to do this:

### Using the driver script (RECOMMENDED)
We recommend executing specific algorithm components using their corresponding driver script in `VAREID/drivers/` for the simplicity of user input and consistent logging with a pipeline execution. **We highly recommend staying consistent with the formatting standards layed out by `config.yaml`!** This way, it's extremely easy to switch between executing stages via the pipeline and separately.

Driver scripts require a configfile structured like `config.yaml`. Once again, your configfile can be supplied by any filepath, relative or absolute.

Since the pipeline was installed as a module, you can easily execute the driver script through this module. No matter what directory you execute from, the path to the driver script will be the same (and relative to VAREID).
```
python -m VAREID.drivers.[driver_script] --config_path path/to/your_config.yaml
```
Notice that we didn't include the `.py` extension on the driver. This is because we're referencing it as a module. Think of this like an import statement, `import VAREID.drivers.[driver_script]`, but you're executing it as a script.

### Using the algorithm component itself
If you don't have a full configfile filled out or would rather not rely on it, you can directly execute each algorithm component using its executable script. Each algorithm component has a separate set of parameters documented with `argparse` Please follow these parameters for your desired component and supply the necessary paths, flags, etc.

Here is an example on how to run frame_sampling.py:

```
python -m VAREID.algo.frame_sampling.frame_sampling \
path/to/ia_filtered_annots.json \
  path/to/fs_annots.json \
  --json_stage1 path/to/stage1_fs_annots.json
```

## Running the Postprocessing Step
Postprocessing is not ran by the pipeline because it requires human interaction to resolve conflicts. To run postprocessing, you can use a driver (see **Running the Postprocessing Step** above). This driver runs the postprocessing script, waits for a SQLite database file to be created, and then opens a GUI. The GUI will checks the database file until conflicts are posted. Your job is to resolve these.

To run the postprocessing driver, use the following:
```
python -m VAREID.drivers.post_driver --config_path path/to/your_config.yaml
```
Wait for a prompt to open a web browser. This is the GUI. Once opened, you'll see a screen similar to the following:

![GUI Screen](https://github.com/user-attachments/assets/153efa29-cba5-4677-8157-f7c61f7019ec)
Use the GUI to resolve all conflicts. It will constantly refresh to check whether conflicts have been saved to the database file. Once all conflicts are resolved, the postprocessing script will end and automatically close the GUI.

### Finishing resolution later
When working with large datasets with many conflicts to resolve, you may have to stop filling out conflicts and come back later. All conflicts and their resolution status are saved to the database file, which **is not reset** on a new call to `post_driver.py`. Thus, you can simply rerun the driver and pick up where you left off.

### Executing without the driver script
If your output formatting is inconsistent with the pipeline you'll need to manually execute two scripts found in `VAREID/algo/postprocessing/`. These are `postprocessing.py` and `gui.py`. Please check their `argparse` parameters for more details.

You will need to execute `postprocessing.py` first and wait until it blocks on user input. For the database (GUI) method, this will look like the following:
```
Still waiting for cluster pair 1 - 0 - Checking again in 5 seconds...
```
At this point, start up `gui.py`.

### Classifying other species
Currently, this pipeline is best used on Grevys Zebras and Plains Zebras. However, it can be used for other species.

Every algorithm component in the pipeline has a configfile with some internal variables controlling how the script runs. These parameters can be coefficients, flags, labels, etc. **YOU SHOULD RARELY NEED TO CHANGE THESE PARAMETERS!** 

All config files are found in `VAREID/algo` within their corresponding algorithm component subfolders. Please refer to any comments in these files before making changes.

To modify the species labels the pipeline will classify into, modify the following fields:
1. `custom_labels` in `species_identifier_config.yaml`:
  
    This is a list of the species to classify annotations into. This is CLIP-based so you can format the names any way you wish.
   
2. `filtered_classes` in `viewpoint_classifier_config.yaml`: 
  
    This is a list of the species to generate viewpoint classifications for. This should match `#1`.


### Executing tools or any other scripts
Please see the documentation in these scripts, which is usually done via `argparse`.
