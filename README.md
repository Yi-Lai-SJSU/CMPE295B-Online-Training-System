# CMPE295 - Online Machine Learning System Backend

### Introduction
This repo belonging to the master project of Online Machine Learning System completed by Yi Lai to provide online Machine Learning training and inference Services.
This repo contains only the backend side the Online Machine Learning system. The frontend side is designed and implemented Shikang Jin. The source code of the frontend side is availabel on the github https://github.com/ShikangNero/Edge-Computing/tree/master/frontend. 

This Online Machine Learning System that can provide customers with services of building, improving, testing, and evaluating their image classification model and object detection models. The image classification model is trained to generate the labels of a given image and the object detection model is to identify the main object in an image and return the coordinates of the object detected.  The images used for training can be retrieved from the large file storage, like fastDFS bucket/Amazon S3, or be uploaded by the customers through the Front end. 


### System Architecture
<img width="800" height="500" src="https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System/blob/master/media/overall-architecure.png"/><div>

### Main Components of the Backend Server
<img width="480" height="300" src="https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System/blob/master/media/Module%20Design.png"/><div>
  
### How to start the code
Run the backend need to install and start docker 
```
git clone https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System.git
cd MachineLearningStudio
docker-compose up --build --force-recreate
```

### Machine Learning Training
<img width="500" height="250" src="https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System/blob/master/media/Training.png"/><div>
  
### Machine Learning Inference
<img width="500" height="300" src="https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System/blob/master/media/Object-Detection.png"/><div>
