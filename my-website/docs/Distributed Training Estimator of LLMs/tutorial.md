---
tags:
  - AI4CI
---

# Tutorials

### Enviroment
The software environment is determined by the specific training frameworks employed, such as the versions of CUDA, PyTorch, FlashAttention, and others. While the `requirements.txt` file enumerates the necessary packages, it is the user's responsibility to specify the appropriate versions required for their use case.

   ```bash
   cd distributed_training_estimator_of_LLM
   pip install -r requirements.txt
   ```

Or you can only install the pacakges for estimator, if you already have sampling data.
   
   ```bash
   cd distributed_training_estimator_of_LLM/Estimator
   pip install -r requirements-estimator.txt
   ```

### Predictor
In order to run Predictor, the training configurations, computing and communication operators' sampling data are required. In the `target_config` folder, there are two example configuration YAML files. The `regressors` folder contains the required data obtained from two real clusters as examples. This can run on any CPU from the past five years, as it only relies on Random Forest and XGBoost.
   ```bash
   cd Estimator
   python mml_3d_prediction.py --config_path <path_to_config.yml>
   ```
Commands to run two example configurations, providing sampling data of Perlmutter and Vista in `Estimator/regressors`.
   ```bash
   cd Estimator
   # One batch runtime estimator about llemma-7B with 4 pipline, 2 model and 2 data parallelism ways on Perlmutter. 
   python mml_3d_prediction.py --config_path ./target_config/llemma_7b_4_2_2_P.yml

   # One batch runtime estimator about llemma-7B with 4 pipline, 2 model and 2 data parallelism ways on Vista. 
   python mml_3d_prediction.py --config_path ./target_config/llemma_7b_4_2_2_V.yml

   # And will print out a message in the terminal like this:
   Estimated timecost of current training configs is 9480819.171239894 us.
   ```

The output can also be obtained using the function.
   ```python
   from mml_3d_prediction import one_batch_predict

   configs_path = 'path_to/training_config.yml'
   one_batch_cost = one_batch_predict(configs_path)   # microseconds
   ```

The output is the estimated time cost of a single parameter update, measured in microseconds.


### Computation Sampling
The computing operator sampling module requires the configuration of each operator in the form of a YAML file. The `/configs/collect` and `/configs/test` directories provide details about the configuration files. This can be run on a single GPU or multiple GPUs.
   ```bash
   cd Kernel_sampling
   ## For example sampling the baddbmm with fp16 
   python sampling_controller.py --config_path ./configs/collect/baddbmm.yml --precision fp16 
   ```
The files `run_collection.sh` and `run_test.sh` contain details about how to test and collect the sampling data for each operator. The `--parts` option specifies how many parts the sampling work should be split into, and the `--part` option specifies which part of the work is being processed on current GPU.


### Communication Sampling
This part, like the Operator Sampling, also requires the configuration of each communication operator in the form of a YAML file. The `/configs/collect` and `/configs/test` directories provide details about the configuration files. The example shows how to collect P2P communication between two nodes, with only one GPU being active on each node. 
   ```bash
    # Get master address and port
    nodes=( $( scontrol show hostnames $SLURM_JOB_NODELIST ) )
    nodes_array=($nodes)
    head_node=${nodes_array[0]}
    head_node_ip=$(srun --nodes=1 --ntasks=1 -w "$head_node" hostname --ip-address)

    # Get the number of nodes
    NNODES=$(scontrol show hostname $SLURM_NODELIST | wc -l)

    # Active GPU 0 of each node
    srun --export=ALL,CUDA_VISIBLE_DEVICES=0 torchrun \
    --nnodes $NNODES \
    --nproc_per_node 1 \
    --rdzv_id $RANDOM \
    --rdzv_backend c10d \
    --rdzv_endpoint $head_node_ip:29500 \
    sampling_controller.py \
    --config_path ./configs/test/p2p.yml \
    --precision fp16 \
    --parts 1 \
    --part 1
   ```
