---
tags:
  - CI4AI
  - Software
  - PADI
---

# Tutorials

### Create a Model Card

Find the descriptions of the Model Card parameters in the [schema descriptions document](./docs/schema_description.md).

```python
from patra_toolkit import ModelCard

mc = ModelCard(
  name="UCI Adult Data Analysis model using Tensorflow",
  version="0.1",
  short_description="UCI Adult Data analysis using Tensorflow for demonstration of Patra Model Cards.",
  full_description="We have trained a ML model using the tensorflow framework to predict income for the UCI Adult Dataset. We leverage this data to run the Patra model cards to capture metadata about the model as well as fairness and explainability metrics.",
  keywords="uci adult, tensorflow, explainability, fairness, patra",
  author="Sachith Withana",
  input_type="Tabular",
  category="classification",
  foundational_model="None"
)

# Add Model Metadata
mc.input_data = 'https://archive.ics.uci.edu/dataset/2/adult'
mc.output_data = 'https://huggingface.co/Data-to-Insight-Center/UCI-Adult'
```

### Initialize an AI/ML Model

```python
from patra_toolkit import AIModel

ai_model = AIModel(
  name="UCI Adult Random Forest model",
  version="0.1",
  description="Census classification problem using Random Forest",
  owner="Sachith Withana",
  location="https://github.iu.edu/swithana/mcwork/randomforest/adult_model.pkl",
  license="BSD-3 Clause",
  framework="sklearn",
  model_type="random_forest",
  test_accuracy=accuracy
)

# Populate Model Structure
a i_model.populate_model_structure(trained_model)
mc.ai_model = ai_model

# Add Custom Metrics
ai_model.add_metric("Test loss", loss)
ai_model.add_metric("Epochs", 100)
ai_model.add_metric("Batch Size", 32)
ai_model.add_metric("Optimizer", "Adam")
ai_model.add_metric("Learning Rate", 0.0001)
ai_model.add_metric("Input Shape", "(26048, 100)")
```

### Run Fairness and Explainability Scanners

```python
# To assess fairness, provide the sensitive feature, test data, labels, and predictions
mc.populate_bias(X_test, y_test, predictions, "gender", X_test['sex'], clf)

# To generate explainability metrics, specify the dataset, column names, model, and number of features
mc.populate_xai(X_test, x_columns, model, top_n=10)
```

### Validate and Save the Model Card

```python
# Capture Python package dependencies and versions
mc.populate_requirements()

# Verify the model card content against the schema
mc.validate()
mc.save(<file_path>)
```

## Submit

Use `mc.submit()` to either upload just a model card, an AI model along with the model card, just the artifacts, or all at once!

```python
mc.submit(
    patra_server_url=<patra_server_url>,
    model=<trained_model>,
    file_format="pt",  # or "h5"
    model_store="huggingface",  # or "github"
    inference_labels="labels.txt",
    artifacts=[<artifact1_path>, <artifact2_path>],
    token=<optional_token>  # optional authentication token
)
```

The `token` parameter is **optional**. If your hosted Patra server requires authentication, provide a valid token.

If a name-version conflict arises, increment `mc.version`. In case of failure, `submit()` attempts partial rollbacks to avoid orphaned uploads.

## Authentication with TACC Credentials

To authenticate against a Patra server hosted in TAPIS, use Patra's built-in `authenticate()` method to obtain an access token:

```python
from patra_toolkit import ModelCard

mc = ModelCard(...)

tapis_token = mc.authenticate(username="<your_tacc_username>", password="<your_tacc_password>")
```

This will print and return a valid `X-Tapis-Token` (JWT). You can then pass this token to `mc.submit()`:

```python
mc.submit(
    patra_server_url=<tapis_hosted_patra_server_url>,
    model=<trained_model>,
    token=tapis_token
)
```

## Examples

Explore the following example notebooks and model cards to learn more about how to use the Patra Model Card Toolkit:
[Notebook Example](./examples/notebooks/GettingStarted.ipynb), [Model Card Example](./examples/model_cards/tesorflow_adult_nn_MC.json)
