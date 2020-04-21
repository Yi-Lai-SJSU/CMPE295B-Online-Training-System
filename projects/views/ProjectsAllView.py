from rest_framework.views import APIView
from projects.models import Project
from django.contrib.auth.models import User
from projects.serializers import ProjectSerializer
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
import datetime

# Create your views here.
class ProjectsAllView(APIView):
    #example: http://localhost:8000/projects/all?user_id=25
    def get(self, request):
        user_id = request.GET.get('user_id', '')
        print(user_id)
        projects = Project.objects.filter(user=User.objects.get(id=user_id))
        print(projects)
        serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        # print(request.data)
        user_id = request.data['user_id']
        project_title = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-" + request.data['title']
        project_description = request.data['description']
        project_type = request.data['type']
        project_path = settings.MEDIA_ROOT + str(user_id) + "/" + project_title + "/"
        print(project_path)
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            video_path = project_path + "videos/"
            os.makedirs(video_path)
            image_path = project_path + "images/"
            os.makedirs(image_path)
            image_default_path = project_path + "images/unknown/"
            os.makedirs(image_default_path)
            model_path = project_path + "models/"
            os.makedirs(model_path)
            project = Project(title=project_title,
                              location=str(user_id) + "/" + project_title + "/",
                              description=project_description,
                              type=project_type,
                              user=User.objects.get(id=user_id)
                              )
            project.save()
            serializer = ProjectSerializer(project, many=False)
            return JsonResponse(serializer.data, safe=False)

