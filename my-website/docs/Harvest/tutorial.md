---
tags:
  - Digital-Agriculture
---
# Tutorial

  

- The prerequisites to use Harvest are an Internet browser, Tapis account, project and user account on supported HPC resource (currently OSC and SDSC) and have these authenticated in the public tapis systems.

- The two main use cases for Harvest are:

	- Train a model with or with out preprocessing

	- Infer on a dataset with a model with or without preprocessing and visualization of the results

- To start using Harvest upload the images that you wish to use Harvest on and then log into https://icicleai.tapis.io/#/ and click on Harvest on the sidebar.
 ![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/tapside.png)

- Training Use Case

	- On the dashboard page select Training and preprocessing if desired
	![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/taptrain.png)

	- Fill in the requested information all required fields will be blank and any field with a default value can be left alone or altered to have a desired effect.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/taptrainmodelsel.png)

		- **Traning System and Data location**:  are where the data is located on hpc resource.  If the user hits browse a file explorer like tool will pop up for them to locate files or they can type in the path.  Please note that the User must authenticate with the tapis systems or else the files will not show
	  -   **Learning Rate**: Adjust the rate at which the model weights are updated during training. This controls the step size in the gradient descent process.
    
	     -   **Batch Size**: Set the number of training examples utilized in one iteration. A smaller batch size can lead to a more refined training process but will take longer.
    
		-   **Number of Training Epochs**: Define the number of complete passes through the entire training dataset. More epochs can improve model accuracy but may lead to overfitting.
    
		-   **Number of GPUs Used**: Specify how many GPUs will be utilized during training. This setting is critical for optimizing training speed and resource allocation.
    
		-   **Number of Labeled Images Per Class**: Particularly relevant for semi-supervised learning, this parameter determines how many labeled images are needed to train the model for each class.
    
		-   **Training Algorithm**: Choose between different learning paradigms, such as Supervised Learning(requiring fully labeled data) or Semi-Supervised Learning (which combines a small amount of labeled data with a large amount of unlabeled data).
        - **Base Deep Learning Model**: Select the underlying model architecture. We provide Transformer-based models and CNNs such as variants of ResNet
	 
	- Depending on if the user opts to upload a labeled images json file or not the next step will be to use the labeler to label the a subset of images in order for the training to start

	- If a labeled images json is provided training will automatically start

	- format for labeled image json is as follows {"class1":[images...],"class2":[images...],...}
	- The labeler will first ask the user for their desired class labels type the desired labels one by one pressing the enter key in between examples of classes maybe "soil", "weed", "soybean", etc then hit the next button
	![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/tapsellabels.png)


	- A screen with images will appear and you will then need to drag and drop images into the box that you think exemplify the class label you have selected. For example if you have soil selected in the drop down you would drag images into the box that are soil. Once you have selected the required amount of images for each class you can hit the next button and the training will begin	![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/taplabeling.png)


	- After this you will be sent to an overview page while you wait for the training to take place please note this training could take a long time depending on queues and required compute time.
![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/tapoverview.png)
	- Once the training is done you will see that the model is downloadable from the overview page. This model will also show up as usable for inference when you start a inference job now that you have trained it

- Inference Use Case

	- On the Dashboard page select Inference and Preprocessing/Visualization if desired(Please note preprocessing is required for the visualization)
![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/tapinfer.png)

	- Fill in requested information about your inference job. Please note for right now the only models available to users to infer on are models they trained themselves through the training process in Harvest.
	  - **Traning System and Data location**:  are where the data is located on hpc resource.  If the user hits browse a file explorer like tool will pop up for them to locate files or they can type in the path.  Please note that the User must authenticate with the tapis systems or else the files will not show
	  - **Inference Model Name**:  The name of the model created in the training step that you would like to use to infer upon
	  -  **Quantization and Inference Backend**:  These do not need to be changed normally and only change how the inference is done these can lead to lower accuracies if changed no reason.
![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/tapinfmodelsel.png)
	- After this is done you will be taken to an overview page while waiting for the inference job to complete. Please note this may take a while due to queues and required computation time.

	- Once the Inference step is done a json with the results will be available for download. If the user selected visualization they will also be able to proceed to the visualization.
![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/tapoverview.png)

  

- Preprocessing Step requires 3 inputs.

	- Image directory you wish to preprocess

	- Shape file of the plots you want to tie the images too

	- csv file that contains drone data about pitch yaw roll along with gps coordinates that the images were taken at
	 ![Alt text for image](https://icicle.osu.edu/media/image/2025-04-30/tappreprocess.png)

- Visualization

	- Requires that you have even more information about the geo spatial data that the drone collects this is required to construct the visualization. This geospatial file dir is only required if you want a heatmap visualization it has files such as .cpg .dbf .prj .sbn .sbx .shp .shx
![Alt text for image](https://icicle.osu.edu/media/image/2025-04-30/tapvis.png)