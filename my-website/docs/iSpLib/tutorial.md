---
tags:
  - CI4AI
  - AI4CI
title: "iSpLib: Tutorial"
sidebar_label: "Tutorial"
pagination_label: "Tutorial"
description: "Tutorial for iSpLib. iSpLib is an accelerated sparse kernel library with PyTorch interface. This library has an auto-tuner which generates optimized custom…"
---

# Tutorial

### SpMM Example

The SpMM operation can also be used directly to multiply two compatible matrices. Following is an example of a sparse and dense matrix multiplication:

```
import builtins
from isplib.matmul import *
from isplib.tensor import SparseTensor
from scipy.sparse import coo_matrix
import torch 

index = torch.tensor([[0, 0, 1, 2, 2],
                      [0, 2, 1, 0, 1]])
value = torch.Tensor([1, 2, 4, 1, 3])
matrix = torch.Tensor([[90, 4], [2, 5], [3, 6]])

a = SparseTensor.from_scipy(coo_matrix((value, index), shape=(3, 3)))
b = matrix
builtins.FUSEDMM = True
print(spmm_sum(a, b))
