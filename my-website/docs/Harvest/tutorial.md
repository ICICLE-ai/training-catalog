---
tags:
  - Digital-Agriculture
---

# Tutorial


- The prerequisites to use Harvest are an Internet browser and contacting us at icicle_harvest@osu.edu for a trial account.  

- [User guide with expected learning time estimates is available here.](https://icicle.osu.edu/media/document/2025-12-03/harvest_user_guide.pdf)

- The two main use cases for Harvest are:

	- Train a model with or with out preprocessing

	- Infer on a dataset with a model with or without preprocessing and visualization of the results

- To start using Harvest upload the images that you wish to use Harvest on and then log into https://icicleai.tapis.io/#/ and click on Harvest on the sidebar.
 ![Alt text for image](https://icicle.osu.edu/media/image/2025-12-11/image.png)

----------------------------------------------------------------------------------------------------------------------------		

- **Training Use Case**

	- On the dashboard page select Training and preprocessing if desired.  **PLEASE NOTE DATA FOR TRAINING JOBS MUST BE IN SCRATCH**
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

	- format for labeled image json is as follows ```{"class1":[images...],"class2":[images...],...}```
	- The labeler will first ask the user for their desired class labels type the desired labels one by one pressing the enter key in between examples of classes maybe "soil", "weed", "soybean", etc then hit the next button
	![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/tapsellabels.png)


	- A screen with images will appear and you will then need to drag and drop images into the box that you think exemplify the class label you have selected. For example if you have soil selected in the drop down you would drag images into the box that are soil. Once you have selected the required amount of images for each class you can hit the next button and the training will begin	![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/taplabeling.png)


	- After this you will be sent to an overview page while you wait for the training to take place please note this training could take a long time depending on queues and required compute time.
![Alt text for image](https://icicle.osu.edu/media/image/2025-04-29/tapoverview.png)
	- Once the training is done you will see that the model is downloadable from the overview page. This model will also show up as usable for inference when you start a inference job now that you have trained it

----------------------------------------------------------------------------------------------------------------------------

- **Inference Use Case**

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

----------------------------------------------------------------------------------------------------------------------------

- **Preprocessing**

	- It requires 3 inputs.

	- Image directory you wish to preprocess

	- Shape file of the plots you want to tie the images too (should be a directory)

	- csv file that contains drone data about pitch yaw roll along with gps coordinates that the images were taken at
	 ![Alt text for image](https://icicle.osu.edu/media/image/2025-04-30/tappreprocess.png)

----------------------------------------------------------------------------------------------------------------------------

- **Crop Images (Data preprocessing)** :

	- On the dashboard page, select "Crop Images".  **PLEASE NOTE DATA FOR TRAINING JOBS MUST BE IN SCRATCH**
	![Alt text for image](https://icicle.osu.edu/media/image/2025-07-25/screenshot-2025-07-25-1.34.55-pm.png)

	- Fill in all the requested information. All fields are required, and the job will not proceed if any are left blank.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-07-25/screenshot-2025-07-25-1.35.27-pm.png)
		- Training system : Select a training system (e.g., pitxer-tapis or expanse).
		- Source Image Directory : Define the directory containing the images to be cropped. Ensure there are a few sample images in the root directory.
			- After entering this information, click the "Load Images" button. This will load sample images into the bottom panel.
			![Alt text for image](https://icicle.osu.edu/media/image/2025-07-25/screenshot-2025-07-25-1.36.00-pm.png)
			- Click on one of the loaded images to open a modal with cropping functionality.
			![Alt text for image](https://icicle.osu.edu/media/image/2025-07-25/screenshot-2025-07-25-1.36.47-pm.png)
			- Crop the image as desired, then click "Close."
		- Destination Image Directory : Define the directory where the cropped images will be uploaded.

	- Click the "Submit" button. 

----------------------------------------------------------------------------------------------------------------------------

- **Extract frames from ARA-Harvest video stream (Data movement)** :

	- On the dashboard page, select "Extract Frames".
	![Alt text for image](https://icicle.osu.edu/media/image/2025-08-15/screenshot-2025-08-15-11.18.34-am.png)

	- Fill in all the requested information. All fields are required, and the job will not proceed if any are left blank.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-08-15/screenshot-2025-08-15-11.23.37-am.png)
		- Training system : Select a training system (e.g., pitxer-tapis or expanse).
		- Destination Image Directory : Specify the directory where the extracted frames will be saved.

	- Click the "Submit" button. 	

----------------------------------------------------------------------------------------------------------------------------


- **Visualization**

	- Requires that you run a Preprocessing step and a Inference step in the same pipeline.
![Alt text for image](https://icicle.osu.edu/media/image/2025-04-30/tapvis.png)

----------------------------------------------------------------------------------------------------------------------------

- **Object Detector:**

	- On the dashboard page, select "Object Detector". **PLEASE NOTE DATA FOR TRAINING JOBS MUST BE IN SCRATCH**
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-21/od_dash.png)

	- Fill in all the requested information. All fields are required, and the job will not proceed if any are left blank.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/od_1.png)
	
		- **Filesystem System**: Select a training system (e.g., expanse-tapis or pitzer-tapis).
		- **Input Path**: Define the directory containing the images to be analyzed. If the user hits browse a file explorer like tool will pop up for them to locate files or they can type in the path. Please note that the User must authenticate with the tapis systems or else the files will not show.
		- **Object Classes**: Configure one or more classes to detect. For each class, provide:
			- **Class Name**: A descriptive name for the class (e.g., "plant", "weed", "crop").
			- **Search Terms**: Comma-separated terms that describe the objects you want to detect. These terms help the system identify similar objects in your images.
		- **Confidence Threshold**: Set the minimum confidence score for detections (range: 0.01 - 1.0). Objects detected with confidence below this threshold will be filtered out.

	- Click the "Submit Detection Job" button. This will redirect to the progress page where you can monitor the job status in real time.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/od_2.png)

	- Once the object detection job is complete, you will be redirected to the results page. Here you can:
		- Download the JSON results file containing all detected objects with their bounding boxes, classes, and confidence scores.
		- View the output directory path where images are organized by detected class.
		- Access class-specific folders containing images where objects of that class were detected.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/od_3.png)

	- The output includes:
		- A JSON file with detection results including bounding box coordinates, class labels, and confidence scores.
		- Class-specific folders in the output directory, each containing images where objects of that class were detected.
		- Images may appear in multiple class folders if they contain objects from different classes.

----------------------------------------------------------------------------------------------------------------------------

- **Classifier:**

	- On the dashboard page, select "Classifier". **PLEASE NOTE DATA FOR TRAINING JOBS MUST BE IN SCRATCH**

	- The classifier module works in two steps:
    ![Alt text for image](https://icicle.osu.edu/media/image/2025-11-21/cl_dash.png)
	- **Step 1: Setup**
	
		- Fill in the initial configuration:
			- **Filesystem System**: Select a training system (e.g., expanse-tapis or pitzer-tapis).
			- **Input JSON Path (Object Detector Output)**: Path to the JSON file from the object detector module containing bounding boxes of detected objects.
			- **Input Images Directory**: Path to the directory containing the source images that were analyzed by the object detector.
			- **Number of Classes**: Specify how many different classes you want to classify (1-20).
			- For each class, provide:
				- **Class Name**: A descriptive name for the class (e.g., "healthy_plant", "diseased_plant", "weed").
				- **Source Image Path**: Path to a reference image containing an example of this class.
		- Click "Next: Crop Reference Patches" to proceed to the cropping step.

	- **Step 2: Crop Reference Patches**
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/cl_2.png)
		- For each class you defined, you will see the reference image you provided.
		- Click on each image to open a cropping modal.
		- Crop the region of interest from the reference image that best represents the class. This cropped patch will be used as a template for classification.
		- Navigate between classes using the "Previous" and "Next" buttons.
		- Once you have cropped patches for all classes, click "Submit Classification Job".
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/cl_3.png)

	- After submission, you will be redirected to the progress page where you can monitor the job status in real time.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/cl_4.png)

	- Once the classification job is complete, you will be redirected to the results page. Here you can:
		- Download the JSON results file containing classification results with class labels and confidence scores for each detected object.
		- View the base output directory path where classified images are stored.
		- Access class-specific folders containing images that were classified into each class.
		- View detailed results including original image names, detected classes, and confidence scores.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/cl_5.png)

	- The output includes:
		- A JSON file with classification results including class labels and confidence scores for each detected object from the input JSON.
		- Class-specific folders in the output directory, each containing images classified into that class.
		- If an image contains objects classified into multiple classes, it will be copied to each relevant class folder.

----------------------------------------------------------------------------------------------------------------------------

  
- **Shapefile Generation:**

	- On the dashboard page, select "Shapefile Generation" if desired. **PLEASE NOTE DATA FOR TRAINING JOBS MUST BE IN SCRATCH**
	![Alt text for image](https://icicle.osu.edu/media/image/2025-08-13/selected_dash.png)

	- Fill in all the requested information. All required fields must be provided for the job to proceed.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/sh_1.png)
		- **Filesystem System**: Select a training system (e.g., expanse-tapis).
		- **Result JSON file**: Browse to and select the JSON file that contains the information about the images. The JSON file must include:
			- **Image name** (required): The name or path of the image file
			- **Label** (required): The classification label for each detection
			- **Bounding boxes** (required): Bounding box coordinates for each detected object. The bounding boxes are used to determine the spatial location of detections within images that have GPS coordinates.
			- The JSON file should be formatted as an array of objects, where each object represents a detection. This JSON format is typically generated by the Object Detector or Classifier modules. Select the whole .json file. The following is a demo JSON format we need:
			![Alt text for image](https://icicle.osu.edu/media/image/2025-11-21/json_ss.png)
		- **Images directory**: Browse to the directory containing the images on which the JSON is based, with matching image names. These images should contain GPS coordinates in EXIF/metadata, which are used to geolocate the bounding boxes and create the spatial shapefile.

	- **Grid Configuration:**
		- **Grid Width (feet)**: Define the width of each polygon in the grid (default: 30 feet). This determines the horizontal size of each grid cell in the generated shapefile.
		- **Grid Height (feet)**: Define the height of each polygon in the grid (default: 30 feet). This determines the vertical size of each grid cell in the generated shapefile.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/sh_1.png)

	- **Spray Level Configuration:**
		- You can choose between **Binary Mode** or **Custom Spray Levels** by checking/unchecking the "Use custom spray levels" checkbox:
			- **Binary Mode** (default, unchecked): When this mode is selected, the shapefile generates a binary classification where each grid cell is marked as either "Yes" (spray needed) if it contains any detections matching the label, or "No" (no spray needed) if it contains no detections. This is useful for simple spray/no-spray decisions.
			- **Custom Spray Levels** (checked): When you enable custom spray levels, you can define multiple spray intensity levels with corresponding threshold values. This allows for more granular control over spray recommendations:
				- Click "Add Level" to add spray levels (e.g., Low, Medium, High).
				- For each level, specify:
					- **Level Name**: A descriptive name (e.g., "Low", "Medium", "High", "Critical").
					- **Threshold Value**: A numeric threshold that determines the minimum number of detections required within a grid cell to qualify for that spray level.
				- The threshold values should be ordered from lowest to highest. For example:
					- Level 1: "Low" with threshold 5 (grid cells with 1-5 detections)
					- Level 2: "Medium" with threshold 15 (grid cells with 6-15 detections)
					- Level 3: "High" with threshold 50 (grid cells with 16-50 detections)
					- Level 4: "Critical" with threshold 999 (grid cells with 50+ detections)
				- Each grid cell is assigned to a spray level based on the count of bounding box detections within that cell's polygon. The system counts all detections matching the selected label that fall within each grid cell's boundaries.
				- You can remove spray levels using the "Remove" button (at least one level must remain).
	

	- After entering the information, click on "Start Generation". This will redirect to the loading (status) page. It will show the stages of the job in real time. After the job is completed, it will automatically redirect to the visualization page.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-08-12/3_status.png)

	- The visualization page contains:
		1) A section showing JSON entries that do not have corresponding images in the directory.
		2) A drop-down menu with the labels found in the JSON entries. The shapefile module generates a shapefile for each label, and you can select which one to view.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-11-19/sh_4.png)

	- Click on "Show Heatmap" to load the shapefile visualization on the map along with a grid of polygons sized according to your grid configuration. The heatmap displays different colors for each spray level:
		- **Binary Mode**: 
			- No color (No_spray) – grid cells with no detections matching the selected label
			- Colored (Spray) – grid cells containing at least one detection matching the selected label, indicating spray is needed
		- **Custom Spray Levels**: Each spray level you defined is displayed with a distinct color in the heatmap. The color mapping corresponds to the threshold ranges you configured:
			- Grid cells are assigned colors based on the count of bounding box detections within each polygon
			- Each custom spray level (e.g., Low, Medium, High) gets its own color, making it easy to visualize spray intensity across the field
			- For example, if you defined "Low" (threshold 5), "Medium" (threshold 15), and "High" (threshold 999):
				- Cells with 1-5 detections are colored for the "Low" spray level
				- Cells with 6-15 detections are colored for the "Medium" spray level  
				- Cells with 16+ detections are colored for the "High" spray level
			- This allows you to see at a glance which areas of the field require more intensive spray treatment
	 - You can use the + and – buttons on the map to zoom in and out to examine specific regions in detail.

	- "Download Shapefile" button will download the shapefile in ZIP format for feeding to agricultural machinery.
	![Alt text for image](https://icicle.osu.edu/media/image/2025-08-12/5_map.png)