---
tags:
  - PADI
  - Digital Agriculture
---

# How-To Guides

### How to Upload a Dataset

**Problem**: You need to upload agricultural data for analysis and model training.

**Solution**:
1. Navigate to the Home page
2. Click on "Finding Similar Farmers" function
3. In the left panel, use the upload form
4. Enter a dataset name
5. Select a CSV file with your agricultural data
6. Click "Upload Dataset"

**Troubleshooting**:
- Ensure your CSV file is properly formatted
- Check that the file size is within limits
- Verify that the dataset name is unique

### How to Train a Collaborative Model

**Problem**: You want to train a machine learning model using data from multiple farmers while preserving privacy.

**Solution**:
1. Navigate to "Collaborative Machine Learning"
2. Select a dataset from your uploaded datasets
3. Choose model parameters:
   - Model Name
   - Model Type (Dense, Conv1D, LSTM)
   - Model Visibility (Public/Private)
4. Review selected collaborators
5. Click "Start Training"

**Advanced Tips**:
- Use different model types for different data characteristics
- Consider privacy settings based on your data sensitivity
- Monitor training progress through the interface

### How to Analyze Model Privacy Risks

**Problem**: You need to assess the privacy risks associated with your trained models.

**Solution**:
1. Go to the Model Repository
2. Find your model in the list
3. Click the red privacy risk icon (GppMaybeIcon)
4. Review the risk analysis sections:
   - Model Logs
   - Model Activity
   - Risk Analysis (Membership Inference Attack accuracy)

**Troubleshooting**:
- If risk analysis is not available, ensure the model training completed successfully
- Check that the model has sufficient data for analysis
