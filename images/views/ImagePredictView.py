from images.models import Image
import numpy as np
from keras.preprocessing import image
from PIL import Image
from django.contrib.auth.models import User
from projects.models import Project
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.views import APIView
from images.serializers import ImageSerializer
from django.http import HttpResponse, JsonResponse
from models.models import Model
from images.models import Image as MyImage
import tensorflow as tf
import os
import datetime

class ImagePredict(APIView):
    def post(self, request):
        print("receiving images....")
        model_id = request.data['model_id']
        uploaded_files = request.FILES.getlist('files')
        user_id = request.GET.get('user_id', '')
        project_id = request.GET.get('project_id', '')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "-"
        # https://stackoverflow.com/questions/13821866/queryset-object-has-no-attribute-name
        # model = Model.objects.filter(title=model_title) return a collection
        model = Model.objects.get(id=model_id)
        model_path = settings.MEDIA_ROOT + model.location
        print(model_path)
        # https://github.com/qubvel/efficientnet/issues/62 to fix ValueError: Unknown activation function:swish
        keras_model = tf.keras.models.load_model(model_path)
        index = 0
        for unPredictedImage in uploaded_files:
            # Get the predict result:
            label_path = settings.MEDIA_ROOT + model.label_location
            print("***********************************************")
            print(label_path)
            print(model_path)
            fr = open(label_path)
            dic = eval(fr.read())
            print(dic)
            label = predictLabel(unPredictedImage, keras_model, label_path, False)
            # Save the image to file-system according to the label:
            image_path = settings.MEDIA_ROOT + project.location + "images/" + label + "/"
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            fs = FileSystemStorage(location=image_path)
            image_title = timestamp + "-" + str(index) + ".jpg"
            fs.save(image_title, unPredictedImage)

            # Save the image to database:
            new_image = MyImage(title=timestamp + "-" + str(index) + ".jpg",
                                location=project.location + "images/" + label + "/" + image_title,
                                url=settings.MEDIA_URL_DATADASE + project.location + "images/" + label + "/" + image_title,
                                description="default",
                                type=label,
                                user=user,
                                project=project,
                                isTrain=True)
            new_image.save()
            index = index + 1

        predictedImage = MyImage.objects.filter(title__startswith=timestamp)
        serializer = ImageSerializer(predictedImage, many=True)
        return JsonResponse(serializer.data, safe=False)

# unpredictedImage: ImageFile, model: keras_model_file, label: path of label.txt;
def predictLabel(unpredictedImage, model, label, imageFormatIsNP):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(type(unpredictedImage))
    # https://stackoverflow.com/questions/22906394/numpy-ndarray-object-has-no-attribute-read
    if imageFormatIsNP:
        test_image = Image.fromarray(unpredictedImage).resize(size=(64, 64))
    else:
        test_image = image.load_img(unpredictedImage, target_size=(64, 64))
        test_image = image.img_to_array(test_image)

    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)
    print(result)
    classIndex = np.argmax(result)
    print("^&^&^&^&^&^^^^^^^^^^^^^^^^^&^&^&^&^&^&^&^&^&^&^&^&^&^&^&^&^&^&^&")
    fr = open(label)
    dic = eval(fr.read())
    fr.close()
    for key in dic:
        if dic[key] == classIndex:
            return key
    return "null"