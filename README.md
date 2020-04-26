docker-compose up --build --force-recreate


1. Project module:
(1) API  - GET   http://localhost:8000/projects/all?user_id=25
     Description - Get all the projects under user(25)
(2) API -  POST http://localhost:8000/projects/all?user_id=25
      Description - Add a new project under user(25)
(3) API -  Get http://localhost:8000/projects/45
      Description - Get the information of project(45) 
(3) API -  Delete http://localhost:8000/projects/45
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
(2) API -  POST http://localhost:8000/models/all?user_id=25&project_id=45
      Description - Post a model in project(45) under user(25)
(3) API -  PUT http://localhost:8000/models/all?user_id=25&project_id=45
      Description - Train a new model
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
