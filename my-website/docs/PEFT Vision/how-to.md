---
tags:
  - Foundation-AI
---


# How-To Guides

These are required setup steps to use PEFT methods in our codebase.

### Environment Setup  
```bash  
source env_setup.sh
```  
  
### Data Preparation
Details about how to prepare for common visual recognition datasets for PEFT,  including VTAB-1K, ImageNet-(Original, Sketch, Adversarial, V2, Rendition), CIFAR, RESISC45, Clevvr-Distance and how to add new datasets to the framework can be found [here](https://github.com/OSU-MLB/ViT_PEFT_Vision?tab=readme-ov-file).

### Pre-trained weights
Details about how to prepare for pre-trained vision backbones and add new backbones to the framework can be found [here](https://github.com/OSU-MLB/ViT_PEFT_Vision?tab=readme-ov-file).
  After the environment, dataset and pre-trained weights are set up. You can use any of the 21 methods (16 PEFT methods and 5 baselines) on low-shot datasets (VTAB-1K), many-shot datasets (CIFAR, RESISC45, Clevvr-Distance) and domain-shift datasets (ImageNet and variants). We provide an example for each setting below:
  
### Evaluate PEFT methods on one dataset in VTAB-1K
An example command to run one PEFT method (**AdaptFormer** ) on the DTD dataset in VTAB-1K. More argument options can be found in main.py. You can find commands for all 21 methods [here](https://github.com/OSU-MLB/ViT_PEFT_Vision?tab=readme-ov-file).

    CUDA_VISIBLE_DEVICES=0  python main.py --ft_mlp_module adapter --ft_mlp_mode parallel --ft_mlp_ln before --adapter_bottleneck 64 --adapter_init lora_kaiming --adapter_scaler 0.1 --data processed_vtab-dtd  
    
If you want to run hyper-parameter tuning on datasets, you can find details [here](https://github.com/OSU-MLB/ViT_PEFT_Vision?tab=readme-ov-file).


### Evaluate robustness of PEFT methods to domain shift  
We use the CLIP ViT-B/16 model and add an FC layer as the prediction head with zero-initialized bias and initialize weights using the class label text embedded by the text encoder. Subsequently, we discard the text encoder and apply PEFT methods to the visual encoder, fine-tuning only the PEFT modules and the head.

The code to generate the prediction head for CLIP can be found at [build_clip_zs_classifier.py](experiment/build_clip_zs_classifier.py).  

**Fine-tuning the CLIP on downstream data.** 

This is an example command to run a PEFT method (LoRA with dimension 32) for the 100-shot ImageNet dataset:
```bash
CUDA_VISIBLE_DEVICES=0  python main.py --data fs-imagenet --data_path data_folder/imagenet/images --warmup_lr_init 1.0e-7 --lr 0.00003 --wd 0.005 --eval_freq 1 --store_ckp --lora_bottleneck 32  --batch_size 256 --final_acc_hp --early_patience 10
```
If you want to run hyper-parameter tuning on datasets, you can find details [here](https://github.com/OSU-MLB/ViT_PEFT_Vision?tab=readme-ov-file).

**Evaluation of fine-tuned CLP on OOD data.**

To evaluate the performance of fine-tuned models on OOD data, here is an example command:

```bash  
for METHOD in rand_h_adapter_64 lora_16 ssf
do
  for dataset in fs-imagenet eval_imagenet-v2 eval_imagenet-r eval_imagenet-a eval_imagenet-s
    do
      CUDA_VISIBLE_DEVICES=0 python main_evaluate.py --test_data ${dataset} --bs 2048 --default experiment/config/clip_fs_imagenet.yml --tune experiment/config/method-imagenet/$METHOD.yml --data_path /research/nfs_chao_209/zheda
    done
done
```  
**Weight-Space Ensembles (WiSE) for PEFT.**

When it comes to applying WiSE to PEFT methods, there are two types of PEFT methods. 
- Methods that insert additional parameters to the model, such as Adapter.
-  Methods that directly fine-tuned existing parameters, such as BitFit. 

For the former, we use `merge_petl.py` and use `merge_model.py` for the latter. 

Example commands for each type:
```bash
CUDA_VISIBLE_DEVICES=0 python merge_model.py --bs 1024  --default experiment/config/clip_fs_imagenet.yml --tune experiment/config/method-imagenet/ln.yml
CUDA_VISIBLE_DEVICES=0 python merge_petl.py --bs 1024 --default experiment/config/clip_fs_imagenet.yml --tune experiment/config/method-imagenet/fact_tk_64.yml
```

To get the WiSE curve plots, you can use `WiSE_PETL.ipynb`.

### Evaluate PEFT methods on Many-shots Datasets
We use three datasets for mann-shot experiments: CIFAR100, Clevr-distance and RESISC.

Here is an example command to run the PEFT methods for the Clevr-distance dataset. Config files for CIFAR and RESISC can be found in the `experiment/config` folder.
```bash
for METHOD in rand_h_adapter_8 lora_8 fact_tk_8 
do
  for dataset in clevr
    do
      CUDA_VISIBLE_DEVICES=0 python main_tune.py --data ${dataset}  --default experiment/config/default_clevr.yml --tune experiment/config/method_clevr/$METHOD.yml --lrwd experiment/config/lr_wd_clevr.yml
    done
done
```


## To add new PEFT methods, hyper-parameter tuning setting, datasets and backbones
Details  can be found [here](https://github.com/OSU-MLB/ViT_PEFT_Vision?tab=readme-ov-file).