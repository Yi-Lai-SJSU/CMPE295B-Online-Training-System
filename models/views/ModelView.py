from django.conf import settings
from rest_framework.views import APIView
from ..models import Model
from ..serializers import ModelSerializer
from django.http import HttpResponse, JsonResponse
import os

# Create your views here.
class ModelView(APIView):
    def get(self, request, model_id):
        model = Model.objects.get(id=model_id)
        # https://my.oschina.net/esdn/blog/834943
        serializer = ModelSerializer(model, many=False)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, model_id):
        model = Model.objects.get(id=model_id)
        model_path = settings.MEDIA_ROOT + model.location
        print(model_path)
        if os.path.exists(model_path):
            os.remove(model_path)
        else:
            print("The file does not exist")
        model.delete()
        return HttpResponse(content="Delete Successfully", status="200")