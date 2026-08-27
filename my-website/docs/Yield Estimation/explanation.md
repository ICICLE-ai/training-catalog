---
tags:
  - Digital-Agriculture
  - Foundation-AI
---
# Explanation

### Features

- **Transformer-Based Yield Estimation:** Uses a transformer architecture to model temporal weather information for corn yield prediction.
- **Weather and Soil Integration:** Combines six weekly weather variables with 66 static soil properties.
- **Multi-Temporal Inference:** Supports yield estimation at multiple seasonal cutoffs from week 20 through week 52.
- **Automatic Preprocessing:** The custom tokenizer converts JSON-formatted structured inputs into the tensors expected by the pretrained model.
- **Automatic Normalization:** Weather and soil features are normalized using statistics stored with the model configuration.
- **Regression Output:** Produces a scalar corn yield estimate in bushels per acre.
- **Hugging Face Integration:** Uses the standard Transformers pipeline interface with repository-provided model and tokenizer code.
- **FlexServ Deployment:** Uses the supported `text-classification` task to expose the regression model as a FlexServ inference service.
- **CPU and GPU Support:** Supports PyTorch inference on CPU and compatible CUDA GPUs.
- **Safetensors Weights:** Model weights are distributed using the Safetensors format.