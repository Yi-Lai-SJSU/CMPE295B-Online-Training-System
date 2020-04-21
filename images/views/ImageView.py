from django.conf import settings
from rest_framework.views import APIView
from images.serializers import ImageSerializer
from django.http import HttpResponse, JsonResponse
from images.models import Image as MyImage
import os

# API: images/<int:image_id>
# Usage: get:    get image by id
#                http://localhost:8000/images/642
#        delete: delete image by id
#                http://localhost:8000/images/642
#        put:    reclassify an image
#                http://localhost:8000/images/642?type=NewTiger
class ImageView(APIView):
    def get(self, request, image_id):
        image = MyImage.objects.get(id=image_id)
        serializer = ImageSerializer(image, many=False)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, image_id):
        print(image_id)
        image = MyImage.objects.get(id=image_id)
        new_image_type = request.GET.get('type', '')
        print(new_image_type)

        # Move in the file system
        new_image_folder = settings.MEDIA_ROOT + image.project.location + "images/" + new_image_type + "/"
        old_image_folder = settings.MEDIA_ROOT + image.project.location + "images/" + image.type + "/"
        new_image_path   = settings.MEDIA_ROOT + image.project.location + "images/" + new_image_type + "/" + image.title
        old_image_path   = settings.MEDIA_ROOT + image.project.location + "images/" + image.type + "/" + image.title
        print("new_image_path: " + new_image_path)
        print("old_image_path: " + old_image_path)

        if not os.path.exists(new_image_folder):
            os.makedirs(new_image_folder)
        os.rename(old_image_path, new_image_path)

        if not os.listdir(old_image_folder):
            print("Empty dir")
            os.rmdir(old_image_folder)

        # Update database:
        image.type = new_image_type
        image.location = image.project.location + "images/" + new_image_type + "/" + image.title
        image.url = settings.MEDIA_URL_DATADASE + image.project.location + "images/" + new_image_type + "/" + image.title
        image.save()
        serializer = ImageSerializer(image, many=False)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, image_id):
        image = MyImage.objects.get(id=image_id)
        image_folder = settings.MEDIA_ROOT + image.project.location + "images/" + image.type + "/"
        image_path = settings.MEDIA_ROOT + image.location
        print(image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            print("The file does not exist")

        if not os.listdir(image_folder):
            print("Empty dir")
            os.rmdir(image_folder)

        image.delete()
        return HttpResponse(content="Delete Successfully", status="200")