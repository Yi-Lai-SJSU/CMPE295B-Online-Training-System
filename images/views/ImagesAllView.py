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
class ImagesAllView(APIView):
    # permission_classes = (IsAuthenticated, )
    def get(self, request):
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        images = MyImage.objects.filter(user=user, project=project)
        serializer = ImageSerializer(images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request):
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)

        images = MyImage.objects.filter(user=user, project=project)
        image_type_list = []
        with transaction.atomic():
            for image in images:
                os.remove(settings.MEDIA_ROOT + image.location)
                if image.type not in image_type_list:
                    image_type_list.append(image.type)
                image.delete()

        for image_type in image_type_list:
            os.rmdir(settings.MEDIA_ROOT + project.location + "images/" + image_type + "/")

        response = dict()
        response['message'] = "success"
        return HttpResponse(json.dumps(response))