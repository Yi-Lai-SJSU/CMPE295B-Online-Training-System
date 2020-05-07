# CMPE295 - Online Machine Learning System Backend

### Introduction
This repo belonging to the master project of Online Machine Learning System completed by Yi Lai to provide online Machine Learning training and inference Services.
This repo contains only the backend side the Online Machine Learning system. The frontend side is designed and implemented Shikang Jin. The source code of the frontend side is availabel on the github https://github.com/ShikangNero/Edge-Computing/tree/master/frontend. 

### Backend Design
<div align=center><img width="500" height="300" src="https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System/blob/master/media/overall-architecure.png"/><div>
<div align=center><img width="480" height="300" src="https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System/blob/master/media/Module%20Design.png"/><div>



### How to start the code
Run the backend need to install and start docker 
```
git clone https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System.git
cd MachineLearningStudio
docker-compose up --build --force-recreate
```










1. Project module:
(1) API  - GET   http://localhost:8000/projects/all?user_id=25
     Description - Get all the projects under user(25)
(2) API -  POST http://localhost:8000/projects/all?user_id=25
      Description - Add a new project under user(25)
(3) API -  Get http://localhost:8000/projects/45
      Description - Get the information of project(45) 
(4) API -  Put http://localhost:8000/projects/45?description=My second project
      Description - Update the description of project(45) to "My second project"
(5) API -  Delete http://localhost:8000/projects/45
      Description - Delete the project(45) 
2. Videos module:
            (1) API  - GET   http://localhost:8000/videos/all?user_id=25&project_id=45
     Description - Get all the projects in project(45) under user(25)
(2) API -  POST http://localhost:8000/videos/all?user_id=25&project_id=45
      Description - Post a video for splitting and images prediction
(3) API -  Get http://localhost:8000/videos/125
      Description - Get the video by ID
(4) API -  Delete http://localhost:8000/videos/125
      Description - Delete the video by ID  
3. Models module:
(1) API  - GET   http://localhost:8000/models/all?user_id=25&project_id=45
     Description - Get all the models in project(45) under user(25)
(2) API -  POST http://localhost:8000/models/all?user_id=25&project_id=45&method=upload
      Description - Post a model in project(45) under user(25)
      Body：
               request.data['title']  
               request.data['description']
               request.data['type']     //Classification
               uploaded_files = request.FILES.getlist('files')  
               //  uploaded_files[0] is .h5 file,  uploaded_files[1] is classLabel.txt
(3) API -  POST http://localhost:8000/models/all?user_id=25&project_id=45&method=create
      Description - Train a new model
      Body：
                request.data['title']
                request.data['description']
                request.data['type']   //Classification
                uploaded_files = request.FILES.getlist('files')  
                // uploaded_files[0] is python file
            (4) API -  Get http://localhost:8000/models/60
      Description - Get the video by ID
(5) API -  http://localhost:8000/models/60
      Description - Delete the video by ID  
4. Images module:
(1) API  - GET  http://localhost:8000/images/all?user_id=25&project_id=45
     Description - Get all the images in project(45) under user(25)
(2) API  - Delete  http://localhost:8000/images/all?user_id=25&project_id=45
     Description - Delete all the images in project(45) under user(25)

(3) API -  GET http://localhost:8000/images/Cat?user_id=25&project_id=45
      Description - Get all the images tagged by Cat in project(45) under user(25)
(4) API -  POST http://localhost:8000/images/Cat?user_id=25&project_id=45
      Description - Post images into Cat folder in project(45) under user(25)
(5) API -  PUT http://localhost:8000/images/Cat?user_id=25&project_id=45&type=Student
      Description - Change all the images tagged by Cat to Student
(6) API -  DELETE http://localhost:8000/images/Cat?user_id=25&project_id=45
      Description - DELETE all the images tagged by Cat in project(45) under user(25)
(7) API -  Get http://localhost:8000/images/byVideo/121
     Description - Get all the images from video 121
(8) API - POST http://localhost:8000/images/predict
     Description - Predict all the tags by images
(9) API - GET  http://localhost:8000/images/type?user_id=25&project_id=45
     Description - GET all the tags
(10) API - GET http://127.0.0.1:8000/images/632
       Description - GET image by ID
(11) API - DELETE http://127.0.0.1:8000/images/632
       Description - Delete image by ID
(12) API - PUT http://127.0.0.1:8000/images/630?type=cat
       Description - change the tag of image(630) to cat
