---
tags:
  - CI4AI
---

# How-To Guides

## Installation

    

To install, first clone the repository and move into the folder `fastkg-icicle`. Then run: `pip install -e .`



# CPU/GPU Testing

To test fb15k dataset:



    cd ./tests

    python trans_e.py



# Speedup Comparison

The `./tests/comparison` compares the speedup with TorchKGE. To run comparison, do the following:



1. `pip install torchkge`

2. `cd ./tests/comparison`

3. `python trans_e_fastkg.py`

4. `python trans_e_torchkge.py`



# Custom Dataset

FastKG has in-built FB15k and PPOD dataset. To use your own dataset, modify line 35 of the file `./tests/trans_e.py`. Replace the line

    

    df = load_fb15k('train')



with the following snippet:



    from fastkg.utils import read_csv

    df = read_csv('your/tsv/train/file')



The tsv train file should have three columns separated by `\t` and sequenced in head-rel-tail order. The first line of the file should not contain any header column.



# Saving and loading trained model



The `model_sparse` in `./tests/trans_e.py` is a standard PyTorch model. It can be saved and loaded using the PyTorch functions.



    # Saving

    torch.save(model_sparse, "model.pth")



    # Loading

    model_sparse = torch.load("model.pth")





# Evaluation



To evaluate if a triplet is a probable KG candidate, use the `classify_triplet` function from the `model_sparse` when training is done.



    # Append this after ./tests/trans_e.py

    print(model_sparse.classify_triplet(h_idx=0, r_idx=0, t_idx=1, threshold=1.5))



This checks if the 1st entity, the 1st relation, and the 2nd entity make up a plaussible triplet for the KG or not. The threshold is typicall the loss margin used in training (1.5).

