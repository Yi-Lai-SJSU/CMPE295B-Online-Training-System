import cv2
from django.db import transaction

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

# Create your views here.
class VideoView(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        videoSerializer = VideoSerializer(video, many=False)
        return JsonResponse(videoSerializer.data, safe=False)

    def delete(self, request, video_id):
        video = Video.objects.get(id=video_id)
        images = MyImage.objects.filter(video=video)
        video_path = settings.MEDIA_ROOT + video.location
        print(video_path)
        if os.path.exists(video_path):
            os.remove(video_path)
        else:
            print("The file does not exist")

        image_type_list = []
        with transaction.atomic():
            for image in images:
                os.remove(settings.MEDIA_ROOT + image.location)
                if image.type not in image_type_list:
                    image_type_list.append(image.type)
                image.delete()
        for image_type in image_type_list:
            os.rmdir(settings.MEDIA_ROOT + video.project.location + "images/" + image_type + "/")
        video.delete()
        return HttpResponse(content="Delete Successfully", status="200")