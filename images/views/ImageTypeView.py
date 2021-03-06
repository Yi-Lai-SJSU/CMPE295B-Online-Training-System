from django.contrib.auth.models import User
from projects.models import Project
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.views import APIView
from images.serializers import ImageSerializer
from django.http import HttpResponse, JsonResponse
from images.models import Image as MyImage
import os
import datetime
from django.db import transaction
import json

# Create your views here.
class ImageTypeView(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request):
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        images = MyImage.objects.filter(user=user, project=project)
        image_type_dict = dict()
        for image in images:
            if image.type in image_type_dict:
                image_type_dict[image.type] = image_type_dict[image.type] + 1
            else:
                image_type_dict[image.type] = 1
        print(image_type_dict)
        response_data = list()
        for key in image_type_dict:
            item = dict()
            item["name"] = key
            item["count"] = image_type_dict[key]
            avatar_Image = MyImage.objects.filter(user=user, project=project, type=key)[0]
            item["avatarImage"] = ImageSerializer(avatar_Image, many=False).data
            print(item)
            response_data.append(item)
        print(response_data)
        return HttpResponse(json.dumps(response_data))