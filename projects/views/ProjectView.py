from rest_framework.views import APIView
from projects.models import Project
from django.contrib.auth.models import User
from projects.serializers import ProjectSerializer
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
import datetime
import shutil

# Create your views here.
class ProjectView(APIView):
    #example: http://localhost:8000/projects/45
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        serializer = ProjectSerializer(project, many=False)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, project_id):
        project = Project.objects.get(id=project_id)
        project.description = request.GET.get('description', '')
        project.save()
        serializer = ProjectSerializer(project, many=False)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, project_id):
        # print(request.data)
        project = Project.objects.get(id=project_id)
        print(settings.MEDIA_ROOT + project.location)
        shutil.rmtree(settings.MEDIA_ROOT + project.location)
        project.delete()
        return HttpResponse(content="Delete Successfully", status="200")