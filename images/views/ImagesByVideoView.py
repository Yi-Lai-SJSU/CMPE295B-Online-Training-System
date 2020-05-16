from django.db import transaction
from django.contrib.auth.models import User
from projects.models import Project
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.views import APIView
from images.serializers import ImageSerializer
from django.http import HttpResponse, JsonResponse
from images.models import Image as MyImage
from videos.models import Video
import os
import datetime
import json

# API: images/<string:image_tag>
# Usage: get:    get image by tag
#                http://localhost:8000/images/NewTest?user_id=25&project_id=45
#        delete: delete image by tag
#        put:    reclassify all images to a new tag
#                http://localhost:8000/images/NewTest?user_id=25&project_id=45&type=Student
class ImagesByVideoView(APIView):
    def get(self, request, video_id):
        print(video_id)
        video = Video.objects.get(id=video_id)
        images = MyImage.objects.filter(video=video)
        serializer = ImageSerializer(images, many=True)

        response = dict()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^")
        if video.project.type == "Classification":
            response['type'] = "Classification"
        else:
            response['type'] = "Detection"

        response['date'] = serializer.data
        return HttpResponse(json.dumps(response))