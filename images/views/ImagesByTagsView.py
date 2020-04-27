from django.db import transaction
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

# API: images/<string:image_tag>
# Usage: get:    get image by tag
#                http://localhost:8000/images/NewTest?user_id=25&project_id=45
#        delete: delete image by tag
#        put:    reclassify all images to a new tag
#                http://localhost:8000/images/NewTest?user_id=25&project_id=45&type=Student
class ImagesByTagsView(APIView):
    def get(self, request, image_tag):
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        images = MyImage.objects.filter(user=user, project=project, type=image_tag.lower())
        serializer = ImageSerializer(images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, image_tag):
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        uploaded_files = request.FILES.getlist('files')
        image_tag = image_tag.lower()
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"
        image_folder = settings.MEDIA_ROOT + project.location + "images/" + image_tag.lower() + "/"
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        fs = FileSystemStorage(location=image_folder)

        index = 0
        for image in uploaded_files:
            image_title = timestamp + str(index) + ".jpg"
            fs.save(image_title, image)
            new_image = MyImage(title=image_title,
                                location=project.location + "images/" + image_tag.lower() + "/" + image_title,
                                url=settings.MEDIA_URL_DATADASE + project.location + "images/" + image_tag.lower() + "/" + image_title,
                                description="default",
                                type=image_tag.lower(),
                                user=user,
                                project=project,
                                isTrain=True)
            new_image.save()
            index = index + 1
        all_New_Images = MyImage.objects.filter(title__startswith=timestamp)
        serializer = ImageSerializer(all_New_Images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, image_tag):
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        new_image_type = request.GET.get('type', '').lower()
        image_tag = image_tag.lower()
        print("Image tag: ", image_tag)
        images = MyImage.objects.filter(user=user, project=project, type=image_tag.lower())
        print(images)

        if image_tag.lower() == new_image_type.lower():
            return HttpResponse(content="Same collection", status="406")

        print("Old tag: ", image_tag)
        print("New tag: ", new_image_type)

        new_image_folder = settings.MEDIA_ROOT + project.location + "images/" + new_image_type + "/"
        old_image_folder = settings.MEDIA_ROOT + project.location + "images/" + image_tag.lower() + "/"
        if not os.path.exists(new_image_folder):
            os.makedirs(new_image_folder)
        with transaction.atomic():
            for image in images:
                new_image_path = settings.MEDIA_ROOT + image.project.location + "images/" + new_image_type + "/" + image.title
                old_image_path = settings.MEDIA_ROOT + image.project.location + "images/" + image_tag + "/" + image.title
                os.rename(old_image_path, new_image_path)

                image.type = new_image_type
                image.location = image.project.location + "images/" + new_image_type + "/" + image.title
                image.url = settings.MEDIA_URL_DATADASE + image.project.location + "images/" + new_image_type + "/" + image.title
                image.save()

        if not os.listdir(old_image_folder):
            print("Empty dir")
            os.rmdir(old_image_folder)

        images = MyImage.objects.filter(user=user, project=project, type=new_image_type)
        serializer = ImageSerializer(images, many=True)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, image_tag):
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        image_tag = image_tag.lower()
        images = MyImage.objects.filter(user=user, project=project, type=image_tag)
        with transaction.atomic():
            for image in images:
                os.remove(settings.MEDIA_ROOT + project.location + "images/" + image_tag + "/" + image.title)
                image.delete()
        os.rmdir(settings.MEDIA_ROOT + project.location + "images/" + image_tag + "/")
        return HttpResponse(content="Delete Successfully", status="200")