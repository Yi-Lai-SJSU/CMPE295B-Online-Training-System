# CMPE295 - Online Machine Learning System Backend

[![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg?style=plastic)](https://badge.fury.io/py/tensorflow)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

### Introduction
This repo belonging to the master project of Online Machine Learning System completed by Yi Lai to provide online Machine Learning training and inference Services.
This repo contains only the backend side the Online Machine Learning system. The frontend side is designed and implemented Shikang Jin. The source code of the frontend side is availabel on the github https://github.com/ShikangNero/Edge-Computing/tree/master/frontend. 

This Online Machine Learning System that can provide customers with services of building, improving, testing, and evaluating their image classification model and object detection models. The image classification model is trained to generate the labels of a given image and the object detection model is to identify the main object in an image and return the coordinates of the object detected.  The images used for training can be retrieved from the large file storage, like fastDFS bucket/Amazon S3, or be uploaded by the customers through the Frontend.

#### Demo Video
##### Online Image Classification Training
#### Online Image classification 
#### Online Object Detection (click to watch the demo)
[![Watch the video](https://img.youtube.com/vi/8ZqswtNSvWg/hqdefault.jpg)](https://youtu.be/8ZqswtNSvWg)


### System Architecture
<img width="1000" height="600" src="https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System/blob/master/media/overall-architecure.png"/><div>

The backend of the Online Machine Learning System is mainly to provide online Machine Learning Training and Inference services. The Online Machine Learning Training which takes a long time is asynchronous tasks implemented by the Celery Server. Besides these two main tasks, the backend side also implements User account management, project management, and dataset management. There are two types of databases involved in the system.  The SQLite database in the local is responsible for saving all the metadata of images, videos, and models. The local file system serves as the cache storage of images and models during Machine Learning training and inference. All the historical images, videos, and models are stored in the Large File system (fastDFS) for downloading when necessary.  The technology we used in the implementation of the Online Machine Learning System is explained in detail below.

1.  [Django REST Framework](https://www.django-rest-framework.org/) + [Python](https://www.python.org/downloads/release/python-360/)

    We choose Django REST Framework to build the backend of our web application. The main reason we choose Django Framework in Python is still the most popular programming language for machine learning and deep learning projects. Django REST framework is a powerful and flexible toolkit for building Web APIs, and it is also a framework that Django relies on to extend Restful API, similar to Django's usage style.

2. [Celery + Redis](https://docs.celeryproject.org/en/stable/getting-started/brokers/redis.html) to implement an asynchronous Task

    It needs a large amount of training time to generate a good machine learning model. This kind of web request should be done outside of the immediate request-response cycle. So we import Celery as asynchronous workers and Redis as the message broker for all the model training tasks. All the requests of training a model will be handled by the Celery Server without blocking the main workflow.

3. [fastDFS](https://github.com/happyfish100/fastdfs) as Large File Storage

    FastDFS is an open-source, lightweight, distributed file system that is dedicated to large data storage and load balancing. This large file storage system is one of the best choices for online services involving video, images, or other files. In our program, all the images, videos, and models are uploaded onto the fastDFS storage and then the edge side can load these files when they need them.

4. [Tensorflow](https://www.tensorflow.org/) + Keras API, CNN and Transfer Learning

    TensorFlow is an end-to-end open-source platform for machine learning. Keras is a high-level neural network API based on the Tensorflow framework. In our project, we use Tensorflow and Keras API to build CNN networks and then train out an image classification model. We also use the transfer learning technology based on the resnet101 net to train out an object detection model. 
    
    For the object Detection, we call the API from [Keras implementation of RetinaNet object detection](https://github.com/fizyr/keras-retinanet).
    
5. Dockerization of the Backend side of the web application

    A common problem in the development process is the issue of environmental consistency. The Docker image provides a complete runtime environment in addition to the kernel, which ensures the consistency of the application runtime environment. Dockerization also enables more efficient and convenient ways to own local development environments that closely match the production environment. To facilitate the operation and maintenance of our project, we dockerize the backend of our web application.

### How to start the code
#### Prerequisite: Run the backend need to install and start docker 
```
git clone https://github.com/Yi-Lai-SJSU/CMPE295B-Online-Training-System.git
cd MachineLearningStudio
docker-compose up --build --force-recreate
```
### FAQ

