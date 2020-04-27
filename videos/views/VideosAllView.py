import cv2
from ..models import Video
from django.contrib.auth.models import User
from projects.models import Project
from images.views.ImagePredictView import predictLabel
from images.serializers import ImageSerializer
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.views import APIView
from ..serializers import VideoSerializer
from django.http import HttpResponse, JsonResponse
from models.models import Model
from images.models import Image as MyImage
import tensorflow as tf
import os
import datetime
from ..objectDetection import objectDetectionLImages
import json
from django.core import serializers

# Create your views here.
class VideosAllView(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request):
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        videos = Video.objects.filter(user=user, project=project)
        serializer = VideoSerializer(videos, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        print("POST received - return done")
        # Get all the param
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        model_id = request.data['model_id']
        timeF = int(request.data['interval'])
        uploaded_file = request.data['file']
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        model = Model.objects.get(id=model_id)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"
        if project.type == "Classification":
            self.classifyImages(user, project, model, timeF, uploaded_file, timestamp)
        else:
            self.detectObjectImages(user, project, model, timeF, uploaded_file, timestamp)
        # response = dict()
        # response['images'] = MyImage.objects.filter(title__startswith=timestamp)
        # response['video'] = Video.objects.filter(title__startswith=timestamp)
        # print(json.dumps(response))
        response = dict()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^")
        images = MyImage.objects.filter(title__startswith=timestamp, user=user, project=project)
        # images = MyImage.objects.filter(user=user, project=project)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^")
        response['images'] = ImageSerializer(images, many=True).data
        print("^^^^^^^^^^^^^^^^^^^^^^^^^")
        video = Video.objects.filter(title__startswith=timestamp, user=user, project=project)[0]
        response['video'] = VideoSerializer(video, many=False).data
        print("^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(response)
        # # for image in predictedImage:
        # #     response['images'].append(image.url)
        # # response['video'] = Video.objects.filter(title__startswith=timestamp)
        # # print(response['images'])
        # # print(response['video'])
        return HttpResponse(json.dumps(response))

    def detectObjectImages(self, user, project, model, timeF, uploaded_file, timestamp):
        objectDetectionLImages(user, project, model, timeF, uploaded_file, timestamp)

    def classifyImages(self, user, project, model, timeF, uploaded_file, timestamp):
        locationOfVideos = settings.MEDIA_ROOT + project.location + "videos/"
        fs = FileSystemStorage(location=locationOfVideos)
        fs.save(timestamp + uploaded_file.name, uploaded_file)

        videoFile = locationOfVideos + timestamp + uploaded_file.name
        video = Video(title=timestamp + uploaded_file.name,
                      description="default",
                      location=project.location + "videos/" + timestamp + uploaded_file.name,
                      url=settings.MEDIA_URL_DATADASE + project.location + "videos/" + timestamp + uploaded_file.name,
                      type="unknown",
                      user=user,
                      project=project)
        video.save()

        vc = cv2.VideoCapture(videoFile)
        c = 1
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            print('openerror!')
            rval = False

        model_path = settings.MEDIA_ROOT + model.location
        keras_model = tf.keras.models.load_model(model_path)
        label_path = settings.MEDIA_ROOT + model.label_location
        print(model_path)

        while rval:
            rval, frame = vc.read()
            if c % timeF == 0:
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                # Predict the class of the frame
                predicted_label = predictLabel(frame, keras_model, label_path, True)
                print(predicted_label)
                print("LOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOGLOG")

                # Get the folder path to save the Frame, if not exited, create a new folder
                image_folder = settings.MEDIA_ROOT + project.location + "images/" + predicted_label + "/"
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                # Save the frame to the folder
                image_title = timestamp + str(int(c / timeF)) + '.jpg'
                image_path = image_folder + image_title
                cv2.imwrite(image_path, frame)

                # Save to the Image database
                new_image = MyImage(title=image_title,
                                    location=project.location + "images/" + predicted_label + "/" + image_title,
                                    url=settings.MEDIA_URL_DATADASE + project.location + "images/" + predicted_label + "/" + image_title,
                                    description="default",
                                    type=predicted_label,
                                    user=user,
                                    project=project,
                                    video=video,
                                    isTrain=True)
                new_image.save()
            c += 1
            cv2.waitKey(1)
        vc.release()
